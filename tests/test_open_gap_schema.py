import os
os.environ.setdefault("AGENT_LOG_LEVEL", "INFO")
os.environ.setdefault("AGENT_MAX_ROWS", "100000")
os.environ.setdefault("AGENT_Z_SCORE_THRESHOLD", "3.0")
os.environ.setdefault("AGENT_IQR_MULTIPLIER", "1.5")
os.environ.setdefault("AGENT_MAX_CANDIDATES", "5")
from pathlib import Path
import re
import yaml

ROOT=Path(__file__).resolve().parents[1]
ALLOWED={"spec_version","name","version","description","author","license","model","extends","dependencies","skills","tools","agents","delegation","runtime","a2a","compliance","registries","tags","mcp_servers","metadata"}

def test_manifest_matches_open_gap_01_shape():
    manifest=yaml.safe_load((ROOT/"agent.yaml").read_text())
    assert manifest["spec_version"]=="0.1.0"
    assert re.fullmatch(r"^[a-z][a-z0-9-]*$",manifest["name"])
    assert re.fullmatch(r"^\d+\.\d+\.\d+$",str(manifest["version"]))
    assert set(manifest)<=ALLOWED
    assert all(re.fullmatch(r"^[a-z][a-z0-9-]*$",x) for x in manifest["skills"]+manifest["tools"])
    assert len(manifest["skills"])==len(set(manifest["skills"]))
    assert len(manifest["tools"])==len(set(manifest["tools"]))

def test_manifest_references_real_skills_and_tools():
    manifest=yaml.safe_load((ROOT/"agent.yaml").read_text())
    for skill in manifest["skills"]:
        assert (ROOT/"skills"/skill/"SKILL.md").is_file()
    for tool in manifest["tools"]:
        assert (ROOT/"tools"/(tool+".yaml")).is_file()
