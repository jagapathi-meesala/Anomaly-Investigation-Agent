import os
os.environ.setdefault("AGENT_LOG_LEVEL", "INFO")
os.environ.setdefault("AGENT_MAX_ROWS", "100000")
os.environ.setdefault("AGENT_Z_SCORE_THRESHOLD", "3.0")
os.environ.setdefault("AGENT_IQR_MULTIPLIER", "1.5")
os.environ.setdefault("AGENT_MAX_CANDIDATES", "5")
from pathlib import Path
from verification.readiness_audit import audit
ROOT=Path(__file__).resolve().parents[1]

def test_readiness_audit_passes():
    ok,errors=audit()
    assert ok, errors

def test_skill_frontmatter_and_tool_files_exist():
    for skill in ["anomaly-detection","root-cause-analysis","anomaly-reporting"]:
        text=(ROOT/"skills"/skill/"SKILL.md").read_text()
        assert text.startswith("---\n") and "name:" in text and "description:" in text
    for tool in ["detect-anomalies","investigate-root-cause","build-anomaly-report"]:
        assert (ROOT/"tools"/(tool+".yaml")).is_file()
