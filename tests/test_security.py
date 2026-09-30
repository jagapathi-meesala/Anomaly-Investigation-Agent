from tools.detect_anomalies import create_tool

def test_missing_required_field_rejected():
    result=create_tool().run({"metric":"latency"})
    assert not result.ok and result.error["type"]=="validation_error"

def test_unexpected_field_rejected():
    result=create_tool().run({"rows":[{"value":1},{"value":2},{"value":3}],"metric":"m","secret":"x"})
    assert not result.ok and "Unexpected fields" in result.error["message"]

def test_non_numeric_input_rejected():
    result=create_tool().run({"rows":[{"value":1},{"value":"bad"},{"value":3}],"metric":"m"})
    assert not result.ok

def test_oversized_input_is_bounded(monkeypatch):
    monkeypatch.setenv("AGENT_MAX_ROWS","3")
    rows=[{"value":1},{"value":2},{"value":3},{"value":4}]
    result=create_tool().run({"rows":rows,"metric":"m"})
    assert not result.ok
