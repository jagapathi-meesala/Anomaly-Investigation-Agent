import os
os.environ.setdefault("AGENT_LOG_LEVEL", "INFO")
os.environ.setdefault("AGENT_MAX_ROWS", "100000")
os.environ.setdefault("AGENT_Z_SCORE_THRESHOLD", "3.0")
os.environ.setdefault("AGENT_IQR_MULTIPLIER", "1.5")
os.environ.setdefault("AGENT_MAX_CANDIDATES", "5")
from core.agent_core import build_default_registry

def test_dynamic_registry_discovers_tools():
    registry=build_default_registry()
    assert registry.names()==["build-anomaly-report","detect-anomalies","investigate-root-cause"]
