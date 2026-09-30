"""Portable adapter interface with no framework dependency."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping


class PortableAdapter(ABC):
    """Translate framework-neutral agent calls into a target runtime shape."""

    name: str

    @abstractmethod
    def invoke(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        raise NotImplementedError


class OpenAIAdapter(PortableAdapter):
    name = "openai-sdk"

    def __init__(self, registry):
        self.registry = registry

    def invoke(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.registry.execute(tool_name, arguments)


class CrewAIAdapter(PortableAdapter):
    name = "crewai"

    def __init__(self, registry):
        self.registry = registry

    def invoke(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.registry.execute(tool_name, arguments)


class ClaudeCodeAdapter(PortableAdapter):
    name = "claude-code"

    def __init__(self, registry):
        self.registry = registry

    def invoke(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.registry.execute(tool_name, arguments)


class LyzrAdapter(PortableAdapter):
    name = "lyzr"

    def __init__(self, registry):
        self.registry = registry

    def invoke(self, tool_name: str, arguments: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.registry.execute(tool_name, arguments)
