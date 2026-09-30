import os

os.environ.setdefault("AGENT_LOG_LEVEL", "INFO")
os.environ.setdefault("AGENT_MAX_ROWS", "100000")
os.environ.setdefault("AGENT_Z_SCORE_THRESHOLD", "3.0")
os.environ.setdefault("AGENT_IQR_MULTIPLIER", "1.5")
os.environ.setdefault("AGENT_MAX_CANDIDATES", "5")

from adapters.registry import build_adapter_registry

def test_adapter_registry_contains_declared_boundaries():
    registry=build_adapter_registry()
    assert registry.names()==["claude-code","crewai","lyzr","openai"]

def test_adapter_invocation_is_framework_neutral():
    request={"rows":[{"value":1},{"value":2},{"value":1},{"value":20}],"metric":"m"}
    response=registry=build_adapter_registry().get("openai").invoke(request)
    assert response.ok is True
