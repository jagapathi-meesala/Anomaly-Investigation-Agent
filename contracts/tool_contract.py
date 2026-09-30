"""Framework-independent contract for agent tools."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping


class ToolValidationError(ValueError):
    """Raised when tool input violates its contract."""


class ToolExecutionError(RuntimeError):
    """Raised when a validated tool cannot complete execution."""


@dataclass(frozen=True)
class ToolMetadata:
    name: str
    description: str
    input_schema: Mapping[str, Any]
    output_schema: Mapping[str, Any]


@dataclass
class ToolResult:
    ok: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: dict[str, Any] | None = None


class ToolContract:
    """Base interface independent of any model or agent framework."""

    metadata: ToolMetadata

    def validate(self, payload: Mapping[str, Any]) -> None:
        if not isinstance(payload, Mapping):
            raise ToolValidationError("Input must be a mapping/object")

    def execute(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def run(self, payload: Mapping[str, Any]) -> ToolResult:
        try:
            self.validate(payload)
            return ToolResult(ok=True, data=self.execute(payload))
        except ToolValidationError as exc:
            return ToolResult(ok=False, error={"type": "validation_error", "message": str(exc)})
        except (ToolExecutionError, ValueError, TypeError) as exc:
            return ToolResult(ok=False, error={"type": "execution_error", "message": str(exc)})


def require_fields(payload: Mapping[str, Any], required: tuple[str, ...]) -> None:
    missing = [key for key in required if key not in payload]
    if missing:
        raise ToolValidationError(f"Missing required fields: {', '.join(missing)}")


def reject_unknown_fields(payload: Mapping[str, Any], allowed: set[str]) -> None:
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise ToolValidationError(f"Unexpected fields: {', '.join(unknown)}")


def ensure_number(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ToolValidationError(f"{field_name} must be a number")
    return float(value)
