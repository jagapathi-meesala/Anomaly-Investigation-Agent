from adapters.registry import AdapterRegistry
from core.agent_core import DataQualityAgent


def test_all_named_adapters_share_registry_boundary():
    agent = DataQualityAgent()
    adapters = AdapterRegistry(agent.registry)
    assert adapters.names() == ("claude", "crewai", "lyzr", "openai")
    result = adapters.get("openai").invoke("profile-dataset", {"records": [{"x": 1}]})
    assert result["ok"] is True
