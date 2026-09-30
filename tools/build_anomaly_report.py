"""Create a structured, evidence-traceable investigation report."""
from __future__ import annotations

from typing import Any, Mapping

from contracts.tool_contract import ToolContract, ToolMetadata, ToolValidationError, reject_unknown_fields, require_fields


class BuildAnomalyReportTool(ToolContract):
    metadata = ToolMetadata(
        name="build-anomaly-report",
        description="Build a concise structured report from detected anomalies and candidate causes.",
        input_schema={"type": "object", "required": ["metric", "anomalies", "candidate_causes"], "properties": {"metric": {"type": "string"}, "anomalies": {"type": "array"}, "candidate_causes": {"type": "array"}}},
        output_schema={"type": "object", "properties": {"report": {"type": "object"}}},
    )

    def validate(self, payload: Mapping[str, Any]) -> None:
        super().validate(payload)
        require_fields(payload, ("metric", "anomalies", "candidate_causes"))
        reject_unknown_fields(payload, {"metric", "anomalies", "candidate_causes"})
        if not isinstance(payload["metric"], str) or not payload["metric"].strip():
            raise ToolValidationError("metric must be a non-empty string")
        if not isinstance(payload["anomalies"], list) or not isinstance(payload["candidate_causes"], list):
            raise ToolValidationError("anomalies and candidate_causes must be lists")

    def execute(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        anomalies = payload["anomalies"]
        causes = payload["candidate_causes"]
        severity_counts = {"high": 0, "moderate": 0}
        for anomaly in anomalies:
            severity = anomaly.get("severity") if isinstance(anomaly, Mapping) else None
            if severity in severity_counts:
                severity_counts[severity] += 1
        conclusion = "No anomalies detected for the supplied metric." if not anomalies else f"Detected {len(anomalies)} anomalous observation(s) for {payload['metric']}."
        if causes:
            conclusion += " Candidate causes are ranked by observed association and require human/contextual confirmation."
        return {"report": {"metric": payload["metric"], "summary": conclusion, "anomaly_count": len(anomalies), "severity_counts": severity_counts, "candidate_causes": causes, "anomalies": anomalies, "confidence_note": "This report describes statistical evidence, not causal proof."}}


def create_tool() -> BuildAnomalyReportTool:
    return BuildAnomalyReportTool()
