"""Skill text must encode the Cowork failure modes (deterministic contract)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills" / "maagarim-reader" / "SKILL.md").read_text(encoding="utf-8")


def test_skill_forbids_fetch_summarize() -> None:
    assert "fetch and summarize" in SKILL.lower() or "fetch-and-summarize" in SKILL.lower()
    assert "comment-only" in SKILL.lower() or "comment only" in SKILL.lower()


def test_skill_has_lookup_budget() -> None:
    assert "lookup budget" in SKILL.lower() or "quote budget" in SKILL.lower()


def test_skill_points_at_failure_script() -> None:
    assert "report_skill_failure.py" in SKILL
    assert "MAAGARIM-READER-ACI-FAIL" in SKILL


def test_skill_hides_internals_from_user() -> None:
    assert "non-technical" in SKILL.lower() or "לא טכני" in SKILL
    assert "do not mention" in SKILL.lower() or "אל תספר" in SKILL


def test_skill_finds_docx_without_uuid() -> None:
    assert "find_uploaded_docx.py" in SKILL


def test_frontmatter_cowork_safe() -> None:
    # Cowork upload rejects extra YAML keys such as argument-hint.
    forbidden = (
        "argument-hint",
        "disable-model-invocation",
        "context: fork",
    )
    head = SKILL.split("---", 2)[1]
    for key in forbidden:
        assert key not in head
