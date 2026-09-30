import pytest

from core.agent_core import ToolRegistry
from tools.profile_dataset import create_tool


def test_duplicate_registration_rejected():
    registry = ToolRegistry()
    registry.register(create_tool())
    with pytest.raises(ValueError):
        registry.register(create_tool())


def test_unknown_tool_returns_structured_error():
    registry = ToolRegistry()
    result = registry.execute("missing", {})
    assert result["ok"] is False
    assert result["tool"] == "missing"
