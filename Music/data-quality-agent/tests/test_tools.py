from core.agent_core import DataQualityAgent


def test_validation_finds_missing_required_value():
    agent = DataQualityAgent()
    result = agent.execute("validate-data", {"records": [{"id": 1}, {"id": 2, "email": "bad"}], "required_fields": ["email"], "email_fields": ["email"]})
    assert result["ok"] is True
    assert result["violation_count"] == 2


def test_anomaly_detection_is_deterministic():
    agent = DataQualityAgent()
    args = {"records": [{"x": 1}, {"x": 1}, {"x": 1}, {"x": 10}], "fields": ["x"], "z_threshold": 1.0}
    assert agent.execute("detect-anomalies", args) == agent.execute("detect-anomalies", args)


def test_report_preserves_components():
    agent = DataQualityAgent()
    profile = {"row_count": 4}
    validation = {"violation_count": 1}
    anomalies = {"anomaly_count": 1}
    result = agent.execute("generate-quality-report", {"profile": profile, "validation": validation, "anomalies": anomalies})
    assert result["status"] == "review"
    assert result["source_results"]["profile"] == profile
