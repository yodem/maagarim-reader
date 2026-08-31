"""tanakh-nikud skill contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills" / "tanakh-nikud" / "SKILL.md").read_text(encoding="utf-8")


def test_skill_names_script() -> None:
    assert "nikud_tanakh_docx.py" in SKILL
    assert "sefaria_client.py" in SKILL


def test_skill_not_maagarim() -> None:
    assert "not maagarim" in SKILL.lower() or "not maagarim" in SKILL
    assert "maagarim-reader" in SKILL


def test_skill_scope_tanakh_only() -> None:
    assert "tanach with nikkud" in SKILL.lower() or "tanach with nikud" in SKILL.lower()
    assert "find-refs" in SKILL.lower() or "find_refs" in SKILL


def test_skill_non_technical() -> None:
    assert "לא טכני" in SKILL or "non-technical" in SKILL.lower()


def test_maagarim_skill_points_to_tanakh_nikud() -> None:
    maagarim = (ROOT / "skills" / "maagarim-reader" / "SKILL.md").read_text(encoding="utf-8")
    assert "tanakh-nikud" in maagarim
