"""Static readiness audit for the Agent Passport repository."""
from __future__ import annotations
import re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED_FILES=["agent.yaml","SOUL.md","README.md","AGENTS.md","DUTIES.md","RULES.md","EXPLAINABILITY.md",".env.example",".gitignore","requirements.txt","pytest.ini"]
REQUIRED_DIRS=["adapters","config","contracts","core","skills","tools","tests","verification"]
HEADINGS=["## Inputs and Data Sources","## Decision and Reasoning","## Limits and Constraints"]
CONFLICTING=["## Inputs","## Decision","## Limits"]
def section(text, heading):
    start=text.find(heading)
    if start<0:return ""
    remainder=text[start+len(heading):]
    match=re.search(r"\n## ",remainder)
    return remainder[:match.start()] if match else remainder
def audit():
    errors=[]
    for p in REQUIRED_FILES:
        if not (ROOT/p).is_file(): errors.append(f"Missing required file: {p}")
    for p in REQUIRED_DIRS:
        if not (ROOT/p).is_dir(): errors.append(f"Missing required directory: {p}")
    e=ROOT/"EXPLAINABILITY.md"
    if e.is_file():
        text=e.read_text(encoding="utf-8")
        for h in HEADINGS:
            if text.count(h)!=1: errors.append(f"Required heading must occur exactly once: {h}")
            body=section(text,h)
            if len([s for s in re.split(r"(?<=[.!?])\s+",body.strip()) if s.strip()])<2: errors.append(f"Section needs at least two sentences: {h}")
        for h in CONFLICTING:
            if re.search(rf"^{re.escape(h)}\s*$",text,re.M): errors.append(f"Conflicting exact heading found: {h}")
        if not text.startswith("# Explainability"): errors.append("EXPLAINABILITY.md must start with its title")
    manifest=(ROOT/"agent.yaml").read_text(encoding="utf-8") if (ROOT/"agent.yaml").is_file() else ""
    for skill in ("anomaly-detection","root-cause-analysis","anomaly-reporting"):
        if f"  - {skill}" not in manifest or not (ROOT/"skills"/skill/"SKILL.md").is_file(): errors.append(f"Skill declaration/file mismatch: {skill}")
    for tool in ("detect-anomalies","investigate-root-cause","build-anomaly-report"):
        if f"  - {tool}" not in manifest: errors.append(f"Tool not declared: {tool}")
    return not errors, errors
if __name__=="__main__":
    ok,errors=audit(); print("READINESS AUDIT: PASS" if ok else "READINESS AUDIT: FAIL"); [print(f"- {e}") for e in errors]; sys.exit(0 if ok else 1)
