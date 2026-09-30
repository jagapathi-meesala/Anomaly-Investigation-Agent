"""Detect point anomalies using robust IQR and standardized z-score evidence."""
from __future__ import annotations

from statistics import mean, pstdev
from typing import Any, Mapping

from config.settings import load_settings
from contracts.tool_contract import ToolContract, ToolExecutionError, ToolMetadata, ToolValidationError, ensure_number, reject_unknown_fields, require_fields


class DetectAnomaliesTool(ToolContract):
    metadata = ToolMetadata(
        name="detect-anomalies",
        description="Detect numeric time-series anomalies with z-score and IQR evidence.",
        input_schema={
            "type": "object",
            "required": ["rows", "metric"],
            "properties": {
                "rows": {"type": "array", "minItems": 3},
                "metric": {"type": "string", "minLength": 1},
                "value_key": {"type": "string", "default": "value"},
            },
        },
        output_schema={"type": "object", "properties": {"anomalies": {"type": "array"}, "statistics": {"type": "object"}}},
    )

    def validate(self, payload: Mapping[str, Any]) -> None:
        super().validate(payload)
        require_fields(payload, ("rows", "metric"))
        reject_unknown_fields(payload, {"rows", "metric", "value_key"})
        if not isinstance(payload["rows"], list) or len(payload["rows"]) < 3:
            raise ToolValidationError("rows must be a list containing at least 3 records")
        if not isinstance(payload["metric"], str) or not payload["metric"].strip():
            raise ToolValidationError("metric must be a non-empty string")
        key = payload.get("value_key", "value")
        if not isinstance(key, str) or not key.strip():
            raise ToolValidationError("value_key must be a non-empty string")
        settings = load_settings()
        if len(payload["rows"]) > settings.max_rows:
            raise ToolValidationError(f"rows exceeds configured limit of {settings.max_rows}")
        for index, row in enumerate(payload["rows"]):
            if not isinstance(row, Mapping):
                raise ToolValidationError(f"row {index} must be an object")
            if key not in row:
                raise ToolValidationError(f"row {index} is missing '{key}'")
            ensure_number(row[key], f"row {index}.{key}")

    def execute(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        values = [float(row[payload.get("value_key", "value")]) for row in payload["rows"]]
        avg = mean(values)
        sd = pstdev(values)
        ordered = sorted(values)
        q1 = _percentile(ordered, 0.25)
        q3 = _percentile(ordered, 0.75)
        iqr = q3 - q1
        lower, upper = q1 - load_settings().iqr_multiplier * iqr, q3 + load_settings().iqr_multiplier * iqr
        threshold = load_settings().z_score_threshold
        anomalies: list[dict[str, Any]] = []
        for idx, (row, value) in enumerate(zip(payload["rows"], values)):
            z = 0.0 if sd == 0 else abs(value - avg) / sd
            iqr_flag = value < lower or value > upper
            z_flag = sd > 0 and z >= threshold
            if iqr_flag or z_flag:
                evidence = []
                if iqr_flag:
                    evidence.append("iqr")
                if z_flag:
                    evidence.append("z_score")
                anomalies.append({
                    "index": idx,
                    "value": value,
                    "record": dict(row),
                    "z_score": round(z, 6),
                    "evidence": evidence,
                    "severity": "high" if len(evidence) == 2 else "moderate",
                })
        return {"anomalies": anomalies, "statistics": {"count": len(values), "mean": avg, "std_dev": sd, "q1": q1, "q3": q3, "iqr": iqr, "iqr_bounds": [lower, upper]}}


def _percentile(values: list[float], p: float) -> float:
    if not values:
        raise ToolExecutionError("Cannot calculate percentile of empty data")
    position = (len(values) - 1) * p
    low, high = int(position), min(int(position) + 1, len(values) - 1)
    fraction = position - low
    return values[low] + (values[high] - values[low]) * fraction


def create_tool() -> DetectAnomaliesTool:
    return DetectAnomaliesTool()
