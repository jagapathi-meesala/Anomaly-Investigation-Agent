"""Dynamic tool registry and agent core."""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, Mapping

from contracts.tool_contract import Tool, ToolExecutionError, ToolValidationError


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        name = tool.metadata.name
        if not name or not name.strip():
            raise ValueError("Tool name cannot be empty")
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = tool

    def discover(self, module_names: list[str]) -> None:
        for module_name in module_names:
            module = importlib.import_module(module_name)
            factory = getattr(module, "create_tool", None)
            if factory is None:
                raise ValueError(f"Module {module_name} does not expose create_tool")
            self.register(factory())

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._tools))

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"Unknown tool: {name}") from exc

    def execute(self, name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        try:
            return self.get(name).run(arguments)
        except (ToolValidationError, ToolExecutionError, KeyError) as exc:
            return {"ok": False, "tool": name, "error": str(exc)}


class DataQualityAgent:
    def __init__(self, registry: ToolRegistry | None = None):
        self.registry = registry or ToolRegistry()
        if not self.registry.names():
            self.registry.discover([
                "tools.profile_dataset",
                "tools.validate_data",
                "tools.detect_anomalies",
                "tools.generate_report",
            ])

    def execute(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.registry.execute(tool_name, arguments)
