"""Repository readiness audit; exits non-zero when required checks fail."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "agent.yaml", "SOUL.md", "README.md", "AGENTS.md", "DUTIES.md", "RULES.md",
    "EXPLAINABILITY.md", ".env.example", ".gitignore", "requirements.txt", "pytest.ini",
]
REQUIRED_DIRS = ["adapters", "config", "contracts", "core", "skills", "tools", "tests", "verification"]
REQUIRED_HEADINGS = ["## Inputs and Data Sources", "## Decision and Reasoning", "## Limits and Constraints"]
FORBIDDEN_HEADINGS = ["## Inputs", "## Decision", "## Limits"]


def section_body(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    remainder = text[start + len(heading):]
    next_heading = re.search(r"\n## ", remainder)
    return remainder if not next_heading else remainder[:next_heading.start()]


def audit() -> tuple[bool, list[str]]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (ROOT / name).is_file():
            errors.append(f"missing file: {name}")
    for name in REQUIRED_DIRS:
        if not (ROOT / name).is_dir():
            errors.append(f"missing directory: {name}")
    for skill_dir in (ROOT / "skills").glob("*"):
        if skill_dir.is_dir() and not (skill_dir / "SKILL.md").is_file():
            errors.append(f"missing skill file: {skill_dir.name}/SKILL.md")
    explanation = ROOT / "EXPLAINABILITY.md"
    if explanation.exists():
        text = explanation.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if text.count(heading) != 1:
                errors.append(f"required heading count is not one: {heading}")
            body = section_body(text, heading)
            if len(re.findall(r"(?<=[.!?])\s+", body.strip())) < 2:
                errors.append(f"section has fewer than two sentences: {heading}")
        for heading in FORBIDDEN_HEADINGS:
            if re.search(rf"^{re.escape(heading)}\s*$", text, flags=re.MULTILINE):
                errors.append(f"conflicting heading present: {heading}")
        if not text.startswith("## Inputs and Data Sources"):
            errors.append("required explainability headings do not start the document")
    manifest = ROOT / "agent.yaml"
    if manifest.exists():
        raw = manifest.read_text(encoding="utf-8")
        if 'spec_version: "0.1.0"' not in raw:
            errors.append("agent.yaml does not declare OpenGAP 0.1.0")
        if "name: data-quality-agent" not in raw:
            errors.append("agent.yaml has incorrect name")
        for tool in ["profile_dataset.py", "validate_data.py", "detect_anomalies.py", "generate_report.py"]:
            if not (ROOT / "tools" / tool).is_file():
                errors.append(f"manifest tool missing: {tool}")
    return not errors, errors


if __name__ == "__main__":
    ok, errors = audit()
    result = {"ok": ok, "errors": errors}
    print(json.dumps(result, indent=2))
    sys.exit(0 if ok else 1)
