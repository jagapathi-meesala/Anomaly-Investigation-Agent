"""Rank candidate causes by comparing contextual fields around anomaly records."""
from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from config.settings import load_settings
from contracts.tool_contract import ToolContract, ToolMetadata, ToolValidationError, ensure_number, reject_unknown_fields, require_fields


class InvestigateRootCauseTool(ToolContract):
    metadata = ToolMetadata(
        name="investigate-root-cause",
        description="Rank observable categorical or numeric contextual factors associated with anomaly records.",
        input_schema={
            "type": "object",
            "required": ["rows", "metric", "anomalies"],
            "properties": {
                "rows": {"type": "array"},
                "metric": {"type": "string"},
                "value_key": {"type": "string", "default": "value"},
                "anomalies": {"type": "array"},
            },
        },
        output_schema={"type": "object", "properties": {"candidate_causes": {"type": "array"}}},
    )

    def validate(self, payload: Mapping[str, Any]) -> None:
        super().validate(payload)
        require_fields(payload, ("rows", "metric", "anomalies"))
        reject_unknown_fields(payload, {"rows", "metric", "value_key", "anomalies"})
        if not isinstance(payload["rows"], list) or not isinstance(payload["anomalies"], list):
            raise ToolValidationError("rows and anomalies must be lists")
        if not isinstance(payload["metric"], str) or not payload["metric"].strip():
            raise ToolValidationError("metric must be a non-empty string")
        key = payload.get("value_key", "value")
        if not isinstance(key, str):
            raise ToolValidationError("value_key must be a string")
        for row in payload["rows"]:
            if not isinstance(row, Mapping) or key not in row:
                raise ToolValidationError(f"each row must contain '{key}'")
            ensure_number(row[key], key)
        for anomaly in payload["anomalies"]:
            if not isinstance(anomaly, Mapping) or "index" not in anomaly:
                raise ToolValidationError("each anomaly must contain index")

    def execute(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        rows = payload["rows"]
        anomaly_indices = {int(item["index"]) for item in payload["anomalies"]}
        if not anomaly_indices:
            return {"candidate_causes": [], "method": "No anomalies were supplied; no causal ranking was attempted."}
        factors: dict[str, list[Any]] = {}
        for row in rows:
            for key, value in row.items():
                if key == payload.get("value_key", "value") or key in {"timestamp", "time", "date", "id"}:
                    continue
                factors.setdefault(key, []).append(value)
        ranked: list[dict[str, Any]] = []
        for field, values in factors.items():
            baseline = [row.get(field) for i, row in enumerate(rows) if i not in anomaly_indices and field in row]
            anomalous = [row.get(field) for i, row in enumerate(rows) if i in anomaly_indices and field in row]
            if not anomalous or not baseline:
                continue
            score, explanation = _association_score(baseline, anomalous)
            if score > 0:
                ranked.append({"factor": field, "association_score": round(score, 6), "anomalous_values": anomalous, "baseline_summary": explanation})
        ranked.sort(key=lambda item: (-item["association_score"], item["factor"]))
        return {"candidate_causes": ranked[:load_settings().max_candidates], "method": "Association ranking only; correlation is not proof of causation."}


def _association_score(baseline: list[Any], anomalous: list[Any]) -> tuple[float, str]:
    if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in baseline + anomalous):
        base_mean = sum(float(v) for v in baseline) / len(baseline)
        anomaly_mean = sum(float(v) for v in anomalous) / len(anomalous)
        scale = max(abs(base_mean), 1.0)
        return min(abs(anomaly_mean - base_mean) / scale, 1.0), f"baseline_mean={base_mean:.6g}; anomaly_mean={anomaly_mean:.6g}"
    base_counts, anomaly_counts = Counter(baseline), Counter(anomalous)
    base_mode = base_counts.most_common(1)[0][0]
    anomaly_mode = anomaly_counts.most_common(1)[0][0]
    score = 1.0 if anomaly_mode != base_mode else min((anomaly_counts[anomaly_mode] / len(anomalous)) * 0.5, 0.5)
    return score, f"baseline_mode={base_mode!r}; anomaly_mode={anomaly_mode!r}"


def create_tool() -> InvestigateRootCauseTool:
    return InvestigateRootCauseTool()
