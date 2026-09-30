import os
os.environ.setdefault("AGENT_LOG_LEVEL", "INFO")
os.environ.setdefault("AGENT_MAX_ROWS", "100000")
os.environ.setdefault("AGENT_Z_SCORE_THRESHOLD", "3.0")
os.environ.setdefault("AGENT_IQR_MULTIPLIER", "1.5")
os.environ.setdefault("AGENT_MAX_CANDIDATES", "5")
from core.agent_core import AnomalyInvestigationAgent

def test_end_to_end_investigation():
    rows=[
        {"timestamp":"1","value":10,"service":"api"},
        {"timestamp":"2","value":11,"service":"api"},
        {"timestamp":"3","value":10,"service":"api"},
        {"timestamp":"4","value":100,"service":"worker"},
    ]
    result=AnomalyInvestigationAgent().investigate(rows,"latency_ms")
    assert result["ok"] is True
    report=result["data"]["report"]
    assert report["anomaly_count"] >= 1
    assert report["metric"] == "latency_ms"
