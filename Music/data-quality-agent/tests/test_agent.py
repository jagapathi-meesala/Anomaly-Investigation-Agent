from core.agent_core import DataQualityAgent


def test_agent_discovers_all_tools():
    agent = DataQualityAgent()
    assert agent.registry.names() == ("detect-anomalies", "generate-quality-report", "profile-dataset", "validate-data")


def test_agent_executes_profile():
    agent = DataQualityAgent()
    result = agent.execute("profile-dataset", {"records": [{"id": 1}, {"id": 2, "name": "A"}]})
    assert result["ok"] is True
    assert result["row_count"] == 2
