"""Deterministic numeric anomaly detection using a configurable z-score threshold."""
from __future__ import annotations

import math
from typing import Any, Mapping

from contracts.tool_contract import Tool, ToolMetadata
from tools.common import numeric_values, require_records


class DetectAnomaliesTool(Tool):
    metadata = ToolMetadata(
        name="detect-anomalies",
        description="Detects unusually distant numeric values using a z-score threshold.",
        input_schema={"type": "object", "required": ["records", "fields"], "properties": {"records": {"type": "array"}, "fields": {"type": "array"}}},
    )

    def validate(self, arguments: Mapping[str, Any]) -> None:
        require_records(arguments)
        fields = arguments.get("fields")
        if not isinstance(fields, list) or not fields or not all(isinstance(x, str) and x for x in fields):
            raise ValueError("fields must be a non-empty array of strings")
        threshold = arguments.get("z_threshold", 3.0)
        if not isinstance(threshold, (int, float)) or isinstance(threshold, bool) or threshold <= 0:
            raise ValueError("z_threshold must be a positive number")

    def execute(self, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        records = require_records(arguments)
        threshold = float(arguments.get("z_threshold", 3.0))
        findings: list[dict[str, Any]] = []
        for field in arguments["fields"]:
            nums = numeric_values(records, field)
            if len(nums) < 2:
                continue
            mean = sum(nums) / len(nums)
            variance = sum((x - mean) ** 2 for x in nums) / len(nums)
            std = math.sqrt(variance)
            if std == 0:
                continue
            for row, record in enumerate(records):
                value = record.get(field)
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    continue
                z = (float(value) - mean) / std
                if abs(z) >= threshold:
                    findings.append({"row": row, "field": field, "value": value, "z_score": round(z, 6), "threshold": threshold})
        return {"ok": True, "anomaly_count": len(findings), "anomalies": findings}


def create_tool() -> Tool:
    return DetectAnomaliesTool()
