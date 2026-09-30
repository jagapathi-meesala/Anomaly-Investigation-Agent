"""Data validation tool."""
from __future__ import annotations

import re
from typing import Any, Mapping

from contracts.tool_contract import Tool, ToolMetadata
from tools.common import missing, require_records


class ValidateDataTool(Tool):
    metadata = ToolMetadata(
        name="validate-data",
        description="Checks required fields, allowed values, numeric ranges, and email-like values.",
        input_schema={"type": "object", "required": ["records"], "properties": {"records": {"type": "array"}}},
    )

    def validate(self, arguments: Mapping[str, Any]) -> None:
        require_records(arguments)

    def execute(self, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        records = require_records(arguments)
        required_fields = arguments.get("required_fields", [])
        if not isinstance(required_fields, list) or not all(isinstance(x, str) and x for x in required_fields):
            raise ValueError("required_fields must be an array of non-empty strings")
        ranges = arguments.get("numeric_ranges", {})
        if not isinstance(ranges, Mapping):
            raise ValueError("numeric_ranges must be an object")
        allowed = arguments.get("allowed_values", {})
        if not isinstance(allowed, Mapping):
            raise ValueError("allowed_values must be an object")
        email_fields = arguments.get("email_fields", [])
        if not isinstance(email_fields, list) or not all(isinstance(x, str) for x in email_fields):
            raise ValueError("email_fields must be an array of strings")

        violations: list[dict[str, Any]] = []
        for index, record in enumerate(records):
            for field in required_fields:
                if missing(record.get(field)):
                    violations.append({"row": index, "field": field, "rule": "required", "message": "value is missing"})
            for field, bounds in ranges.items():
                if field not in record or missing(record[field]):
                    continue
                if not isinstance(bounds, (list, tuple)) or len(bounds) != 2:
                    raise ValueError(f"range for {field} must contain [min, max]")
                value = record[field]
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    violations.append({"row": index, "field": field, "rule": "numeric", "message": "value is not numeric"})
                    continue
                if bounds[0] is not None and value < bounds[0] or bounds[1] is not None and value > bounds[1]:
                    violations.append({"row": index, "field": field, "rule": "range", "message": f"value outside [{bounds[0]}, {bounds[1]}]"})
            for field, values in allowed.items():
                if field in record and not missing(record[field]) and record[field] not in values:
                    violations.append({"row": index, "field": field, "rule": "allowed_values", "message": "value is not allowed"})
            for field in email_fields:
                value = record.get(field)
                if not missing(value) and (not isinstance(value, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value)):
                    violations.append({"row": index, "field": field, "rule": "email", "message": "invalid email-like value"})
        return {"ok": True, "valid": not violations, "checked_rows": len(records), "violation_count": len(violations), "violations": violations}


def create_tool() -> Tool:
    return ValidateDataTool()
