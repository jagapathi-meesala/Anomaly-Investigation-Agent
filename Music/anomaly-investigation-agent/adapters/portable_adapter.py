"""Framework-neutral adapter boundary; no vendor SDK imports are required."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping

from core.agent_core import AnomalyInvestigationAgent


@dataclass(frozen=True)
class AdapterResponse:
    ok: bool
    payload: dict[str, Any]


class AgentAdapter(ABC):
    """Minimal contract that can be wrapped by OpenAI, CrewAI, Claude Code, or Lyzr."""

    name: str

    def __init__(self, agent: AnomalyInvestigationAgent | None = None) -> None:
        self.agent = agent or AnomalyInvestigationAgent()

    @abstractmethod
    def invoke(self, request: Mapping[str, Any]) -> AdapterResponse:
        """Translate a host-framework request into the core contract."""


class OpenAIAdapter(AgentAdapter):
    name = "openai"

    def invoke(self, request: Mapping[str, Any]) -> AdapterResponse:
        return _invoke_core(self.agent, request)


class CrewAIAdapter(AgentAdapter):
    name = "crewai"

    def invoke(self, request: Mapping[str, Any]) -> AdapterResponse:
        return _invoke_core(self.agent, request)


class ClaudeCodeAdapter(AgentAdapter):
    name = "claude-code"

    def invoke(self, request: Mapping[str, Any]) -> AdapterResponse:
        return _invoke_core(self.agent, request)


class LyzrAdapter(AgentAdapter):
    name = "lyzr"

    def invoke(self, request: Mapping[str, Any]) -> AdapterResponse:
        return _invoke_core(self.agent, request)


def _invoke_core(agent: AnomalyInvestigationAgent, request: Mapping[str, Any]) -> AdapterResponse:
    if not isinstance(request, Mapping):
        return AdapterResponse(False, {"error": "Request must be an object"})
    try:
        payload = agent.investigate(
            rows=request["rows"], metric=request["metric"], value_key=request.get("value_key", "value")
        )
    except (KeyError, TypeError) as exc:
        return AdapterResponse(False, {"error": str(exc)})
    return AdapterResponse(bool(payload.get("ok")), payload)
