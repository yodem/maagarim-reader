"""feedback skill contract."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills" / "feedback" / "SKILL.md").read_text(encoding="utf-8")


def test_feedback_points_at_report_script() -> None:
    assert "report_skill_failure.py" in SKILL
    assert "--skill feedback" in SKILL


def test_feedback_hebrew_user_flow() -> None:
    assert "דיווח" in SKILL or "תודה" in SKILL
    assert "לא טכני" in SKILL or "non-technical" in SKILL.lower()


def test_feedback_codes_include_user_report() -> None:
    assert "USER_REPORT" in SKILL
    assert "SESSION_STUCK" in SKILL


def test_plugin_lists_three_skills() -> None:
    index = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "maagarim-reader" in index
    assert "tanakh-nikud" in index
    assert "feedback" in index
