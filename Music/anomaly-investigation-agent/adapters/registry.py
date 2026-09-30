"""Adapter registry with explicit framework-neutral names."""
from __future__ import annotations

from .portable_adapter import AgentAdapter, ClaudeCodeAdapter, CrewAIAdapter, LyzrAdapter, OpenAIAdapter


class AdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, AgentAdapter] = {}

    def register(self, adapter: AgentAdapter) -> None:
        if adapter.name in self._adapters:
            raise ValueError(f"Adapter already registered: {adapter.name}")
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> AgentAdapter:
        return self._adapters[name]

    def names(self) -> list[str]:
        return sorted(self._adapters)


def build_adapter_registry() -> AdapterRegistry:
    registry = AdapterRegistry()
    for adapter_cls in (OpenAIAdapter, CrewAIAdapter, ClaudeCodeAdapter, LyzrAdapter):
        registry.register(adapter_cls())
    return registry
