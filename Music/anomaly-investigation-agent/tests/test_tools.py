import os
os.environ.setdefault("AGENT_LOG_LEVEL", "INFO")
os.environ.setdefault("AGENT_MAX_ROWS", "100000")
os.environ.setdefault("AGENT_Z_SCORE_THRESHOLD", "3.0")
os.environ.setdefault("AGENT_IQR_MULTIPLIER", "1.5")
os.environ.setdefault("AGENT_MAX_CANDIDATES", "5")
from tools.detect_anomalies import create_tool
from tools.investigate_root_cause import create_tool as create_rca
from tools.build_anomaly_report import create_tool as create_report

def rows():
    return [{"value":10,"service":"api"},{"value":11,"service":"api"},{"value":10,"service":"api"},{"value":100,"service":"worker"}]

def test_detection_finds_outlier():
    result=create_tool().run({"rows":rows(),"metric":"latency"})
    assert result.ok and result.data["anomalies"]

def test_rca_ranks_context():
    anomalies=[{"index":3,"value":100,"severity":"high"}]
    result=create_rca().run({"rows":rows(),"metric":"latency","anomalies":anomalies})
    assert result.ok and result.data["candidate_causes"]

def test_report_is_structured():
    result=create_report().run({"metric":"latency","anomalies":[],"candidate_causes":[]})
    assert result.ok and result.data["report"]["anomaly_count"] == 0
