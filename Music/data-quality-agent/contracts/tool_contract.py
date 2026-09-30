"""Framework-independent tool contract."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping


class ToolContractError(Exception):
    """Base error for contract violations."""


class ToolValidationError(ToolContractError):
    """Raised when input does not satisfy a tool contract."""


class ToolExecutionError(ToolContractError):
    """Raised when a validated tool fails during execution."""


@dataclass(frozen=True)
class ToolMetadata:
    name: str
    description: str
    input_schema: Mapping[str, Any]


class Tool(ABC):
    metadata: ToolMetadata

    @abstractmethod
    def validate(self, arguments: Mapping[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        raise NotImplementedError

    def run(self, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        if not isinstance(arguments, Mapping):
            raise ToolValidationError("Tool arguments must be an object")
        self.validate(arguments)
        try:
            result = self.execute(arguments)
        except ToolContractError:
            raise
        except Exception as exc:
            raise ToolExecutionError(f"{self.metadata.name} failed: {exc}") from exc
        if not isinstance(result, Mapping):
            raise ToolExecutionError(f"{self.metadata.name} returned a non-object result")
        return dict(result)
