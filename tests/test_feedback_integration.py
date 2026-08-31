"""End-to-end feedback skill: report_skill_failure CLI + ACI_FAIL parse."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from report_skill_failure import FAIL_HEADER, SUBJECT_PREFIX, parse_aci_fail  # noqa: E402


def test_feedback_cli_writes_parseable_report(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "report_skill_failure.py"),
        "--skill",
        "feedback",
        "--related-skill",
        "maagarim-reader",
        "--code",
        "SESSION_STUCK",
        "--source",
        "skills/feedback/SKILL.md",
        "--step",
        "User expected Maagarim-checked docx for Berakhot",
        "--step",
        "Waited 16+ minutes with no finished file",
        "--step",
        "FILENAME_ENCODING → NO_BROWSER → FETCH_SUMMARIZE_LOOP",
        "--quote-file",
        "ברכות 4 אוגוסט 2026.docx",
        "--next-action",
        "Review session; ensure Chrome; use find_uploaded_docx",
        "--extra",
        "pytest integration (Berakhot scenario)",
        "--out-dir",
        str(out_dir),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    md_path = out_dir / "skill-failure.md"
    assert md_path.exists()
    assert str(md_path) in proc.stdout

    body = md_path.read_text(encoding="utf-8")
    assert body.startswith(FAIL_HEADER)
    parsed = parse_aci_fail(body)
    assert parsed["skill"] == "feedback"
    assert parsed["related_skill"] == "maagarim-reader"
    assert parsed["code"] == "SESSION_STUCK"
    assert "ברכות" in parsed["quote_file"]
    assert "16+ minutes" in parsed["steps"]

    eml = (out_dir / "skill-failure.eml").read_text(encoding="utf-8")
    assert f"Subject: {SUBJECT_PREFIX} SESSION_STUCK" in eml
    assert "X-Maagarim-Reader-Skill: feedback" in eml
