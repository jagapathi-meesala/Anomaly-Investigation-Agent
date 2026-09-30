from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_skill_frontmatter_and_required_docs():
    for path in (ROOT / "skills").glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert "name:" in text.split("---", 2)[1]
        assert "description:" in text.split("---", 2)[1]
    for name in ["SOUL.md", "README.md", "AGENTS.md", "DUTIES.md", "RULES.md", "EXPLAINABILITY.md"]:
        assert (ROOT / name).is_file()
