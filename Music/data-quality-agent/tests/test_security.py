from core.agent_core import DataQualityAgent


def test_malformed_records_are_rejected():
    agent = DataQualityAgent()
    result = agent.execute("profile-dataset", {"records": ["not-an-object"]})
    assert result["ok"] is False


def test_missing_records_are_rejected():
    agent = DataQualityAgent()
    result = agent.execute("profile-dataset", {})
    assert result["ok"] is False


def test_secret_like_values_are_not_logged_or_returned_by_validation():
    agent = DataQualityAgent()
    secret = "super-secret-token"
    result = agent.execute("validate-data", {"records": [{"token": secret}]})
    assert result["ok"] is True
    assert secret not in str(result.get("violations", []))
