"""Framework-independent anomaly investigation runtime and dynamic registry."""
from __future__ import annotations

from importlib import import_module
from typing import Any, Mapping

from contracts.tool_contract import ToolContract


class ToolRegistry:
    """Dynamic registry that discovers tool classes from modules."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolContract] = {}

    def register(self, tool: ToolContract) -> None:
        name = tool.metadata.name
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = tool

    def discover(self, module_names: list[str]) -> list[str]:
        discovered: list[str] = []
        for module_name in module_names:
            module = import_module(module_name)
            factory = getattr(module, "create_tool", None)
            if factory is None:
                continue
            tool = factory()
            self.register(tool)
            discovered.append(tool.metadata.name)
        return discovered

    def names(self) -> list[str]:
        return sorted(self._tools)

    def get(self, name: str) -> ToolContract:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"Unknown tool: {name}") from exc

    def execute(self, name: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        result = self.get(name).run(payload)
        return {"ok": result.ok, "data": result.data, "error": result.error}


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.discover([
        "tools.detect_anomalies",
        "tools.investigate_root_cause",
        "tools.build_anomaly_report",
    ])
    return registry


class AnomalyInvestigationAgent:
    """Small orchestration layer that stays independent of LLM frameworks."""

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or build_default_registry()

    def investigate(self, rows: list[Mapping[str, Any]], metric: str, value_key: str = "value") -> dict[str, Any]:
        detection = self.registry.execute("detect-anomalies", {
            "rows": rows,
            "metric": metric,
            "value_key": value_key,
        })
        if not detection["ok"]:
            return detection
        causes = self.registry.execute("investigate-root-cause", {
            "rows": rows,
            "metric": metric,
            "value_key": value_key,
            "anomalies": detection["data"]["anomalies"],
        })
        if not causes["ok"]:
            return causes
        return self.registry.execute("build-anomaly-report", {
            "metric": metric,
            "anomalies": detection["data"]["anomalies"],
            "candidate_causes": causes["data"]["candidate_causes"],
        })
