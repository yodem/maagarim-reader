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


def test_write_eml(tmp_path: Path) -> None:
    from report_skill_failure import write_report

    paths = write_report(
        tmp_path,
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
