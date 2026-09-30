from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_static_open_gap_requirements():
    manifest = yaml.safe_load((ROOT / "agent.yaml").read_text(encoding="utf-8"))
    assert manifest["spec_version"] == "0.1.0"
    assert manifest["name"] == "data-quality-agent"
    assert manifest["version"] == "1.0.0"
    assert isinstance(manifest["skills"], list)
    assert isinstance(manifest["tools"], list)
    assert all(isinstance(item, str) for item in manifest["skills"] + manifest["tools"])
    for skill in manifest["skills"]:
        assert (ROOT / "skills" / skill / "SKILL.md").is_file()
    for tool in manifest["tools"]:
        assert (ROOT / tool).is_file()
