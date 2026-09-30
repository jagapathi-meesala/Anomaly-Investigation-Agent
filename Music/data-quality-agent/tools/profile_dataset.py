"""Dataset profiling tool."""
from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from contracts.tool_contract import Tool, ToolMetadata, ToolValidationError
from tools.common import missing, numeric_values, require_records


class ProfileDatasetTool(Tool):
    metadata = ToolMetadata(
        name="profile-dataset",
        description="Profiles fields for completeness, uniqueness, types, and numeric statistics.",
        input_schema={"type": "object", "required": ["records"], "properties": {"records": {"type": "array"}}},
    )

    def validate(self, arguments: Mapping[str, Any]) -> None:
        require_records(arguments)

    def execute(self, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        records = require_records(arguments)
        fields = sorted({key for record in records for key in record})
        profiles: dict[str, Any] = {}
        for field in fields:
            values = [record.get(field) for record in records]
            non_missing = [v for v in values if not missing(v)]
            type_counts = Counter(type(v).__name__ for v in non_missing)
            numeric = numeric_values(records, field)
            profile: dict[str, Any] = {
                "row_count": len(records),
                "missing_count": len(values) - len(non_missing),
                "missing_rate": round((len(values) - len(non_missing)) / len(values), 6),
                "distinct_count": len({repr(v) for v in non_missing}),
                "unique_rate": round(len({repr(v) for v in non_missing}) / len(non_missing), 6) if non_missing else 0.0,
                "types": dict(sorted(type_counts.items())),
            }
            if numeric:
                profile["numeric"] = {
                    "min": min(numeric),
                    "max": max(numeric),
                    "mean": round(sum(numeric) / len(numeric), 6),
                }
            profiles[field] = profile
        return {"ok": True, "row_count": len(records), "column_count": len(fields), "columns": profiles}


def create_tool() -> Tool:
    return ProfileDatasetTool()
