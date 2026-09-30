"""Structured data quality report generator."""
from __future__ import annotations

from typing import Any, Mapping

from contracts.tool_contract import Tool, ToolMetadata, ToolValidationError


class GenerateReportTool(Tool):
    metadata = ToolMetadata(
        name="generate-quality-report",
        description="Combines profiling, validation, and anomaly results into a deterministic quality report.",
        input_schema={"type": "object", "required": ["profile", "validation", "anomalies"], "properties": {}},
    )

    def validate(self, arguments: Mapping[str, Any]) -> None:
        for key in ("profile", "validation", "anomalies"):
            if not isinstance(arguments.get(key), Mapping):
                raise ToolValidationError(f"{key} must be an object")

    def execute(self, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        profile = arguments["profile"]
        validation = arguments["validation"]
        anomalies = arguments["anomalies"]
        row_count = int(profile.get("row_count", 0))
        violation_count = int(validation.get("violation_count", 0))
        anomaly_count = int(anomalies.get("anomaly_count", 0))
        issue_count = violation_count + anomaly_count
        score = 100.0 if row_count == 0 else max(0.0, round(100.0 * (1.0 - issue_count / max(row_count, 1)), 2))
        status = "pass" if issue_count == 0 else "review"
        return {"ok": True, "status": status, "quality_score": score, "row_count": row_count, "violation_count": violation_count, "anomaly_count": anomaly_count, "source_results": {"profile": profile, "validation": validation, "anomalies": anomalies}}


def create_tool() -> Tool:
    return GenerateReportTool()
