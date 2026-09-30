"""Shared validation and deterministic dataset helpers."""
from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from numbers import Real
from typing import Any

from contracts.tool_contract import ToolValidationError


def require_records(arguments: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = arguments.get("records")
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        raise ToolValidationError("records must be an array of objects")
    if not records:
        raise ToolValidationError("records must not be empty")
    normalized: list[dict[str, Any]] = []
    for i, record in enumerate(records):
        if not isinstance(record, Mapping):
            raise ToolValidationError(f"record at index {i} must be an object")
        normalized.append(dict(record))
    return normalized


def numeric_values(records: list[dict[str, Any]], field: str) -> list[float]:
    values: list[float] = []
    for record in records:
        value = record.get(field)
        if isinstance(value, Real) and not isinstance(value, bool) and math.isfinite(float(value)):
            values.append(float(value))
    return values


def missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())
