"""Failure reports must stay machine-parseable for the auto-fix loop."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from report_skill_failure import (  # noqa: E402
    FAIL_HEADER,
    SUBJECT_PREFIX,
    parse_aci_fail,
    render_report,
)


def test_header_block_parses() -> None:
    body = render_report(
        skill="maagarim-reader",
        code="NO_BROWSER",
        source="skills/maagarim-reader/SKILL.md verify loop",
        steps=[
            "User uploaded a Hebrew-named .docx",
            "Agent had no Chrome",
            "Agent fetched Maagarim HTML and asked a summarizer",
        ],
        quote_file="ברכות 4 אוגוסט 2026.docx",
        next_action="Fail closed: comment-only + stop fetch loop",
    )
    assert body.startswith(FAIL_HEADER)
    parsed = parse_aci_fail(body)
    assert parsed["status"] == "FAIL"
    assert parsed["skill"] == "maagarim-reader"
    assert parsed["code"] == "NO_BROWSER"
    assert "Hebrew-named" in parsed["steps"]
    assert parsed["next_action"].startswith("Fail closed")


def test_subject_prefix() -> None:
    assert SUBJECT_PREFIX == "[MAAGARIM-READER-ACI-FAIL]"


def test_feedback_skill_with_related() -> None:
    body = render_report(
        skill="feedback",
        related_skill="maagarim-reader",
        code="USER_REPORT",
        source="skills/feedback/SKILL.md",
        steps=["User expected annotated docx", "Waited 16 minutes"],
        quote_file="ברכות.docx",
        next_action="Review session logs",
    )
    parsed = parse_aci_fail(body)
    assert parsed["skill"] == "feedback"
    assert parsed["related_skill"] == "maagarim-reader"
    assert parsed["code"] == "USER_REPORT"


def test_write_eml(tmp_path: Path) -> None:
    from report_skill_failure import write_report

    paths = write_report(
        tmp_path,
        skill="maagarim-reader",
        code="FILENAME_ENCODING",
        source="Cowork upload path",
        steps=["Hebrew characters became underscores"],
        quote_file="____.docx",
        next_action="Glob *.docx; do not assume UUID names",
        send=False,
    )
    eml = Path(paths["eml"])
    text = eml.read_text(encoding="utf-8")
    assert f"Subject: {SUBJECT_PREFIX} FILENAME_ENCODING" in text
    assert "X-Maagarim-Reader-Code: FILENAME_ENCODING" in text
    assert FAIL_HEADER in text
