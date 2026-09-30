"""Adapter registry for framework-neutral execution."""
from __future__ import annotations

from .portable_adapter import ClaudeCodeAdapter, CrewAIAdapter, LyzrAdapter, OpenAIAdapter


class AdapterRegistry:
    def __init__(self, tool_registry):
        self._adapters = {
            "openai": OpenAIAdapter(tool_registry),
            "crewai": CrewAIAdapter(tool_registry),
            "claude": ClaudeCodeAdapter(tool_registry),
            "lyzr": LyzrAdapter(tool_registry),
        }

    def get(self, name: str):
        key = name.strip().lower()
        if key not in self._adapters:
            raise KeyError(f"Unsupported adapter: {name}")
        return self._adapters[key]

    def names(self):
        return tuple(sorted(self._adapters))
