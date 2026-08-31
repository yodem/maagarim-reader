#!/usr/bin/env python3
"""Write (and optionally email) a machine-readable skill failure report.

Subject prefix (parse this in the auto-fix loop):
  [MAAGARIM-READER-ACI-FAIL] <CODE>

Body always starts with an ACI_FAIL block, then a short human summary.

Send path (first match):
  1. SMTP if MAAGARIM_READER_SMTP_HOST is set (--send)
  2. macOS `open mailto:` if --mailto-open
  3. Always write output/skill-failure.eml (and .md)

Default To: MAAGARIM_READER_REPORT_TO or yotam@sefaria.org
"""

from __future__ import annotations

import argparse
import os
import smtplib
import subprocess
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any
from urllib.parse import quote

FAIL_HEADER = "ACI_FAIL"
SUBJECT_PREFIX = "[MAAGARIM-READER-ACI-FAIL]"
DEFAULT_TO = "yotam@sefaria.org"
DEFAULT_SKILL = "maagarim-reader"

KNOWN_CODES = (
    "NO_BROWSER",
    "FETCH_SUMMARIZE_LOOP",
    "FILENAME_ENCODING",
    "YERUSHALMI_NO_MM15",
    "QUOTE_BUDGET",
    "WITNESS_NOT_LOADED",
    "USER_REPORT",
    "SESSION_STUCK",
    "PARTIAL_RESULT",
    "WRONG_OUTPUT",
)

KNOWN_SKILLS = ("maagarim-reader", "tanakh-nikud", "feedback")
KNOWN_RELATED = ("maagarim-reader", "tanakh-nikud", "unknown")


def render_report(
    *,
    skill: str,
    code: str,
    source: str,
    steps: list[str],
    quote_file: str,
    next_action: str,
    related_skill: str = "",
    extra: str = "",
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    step_line = " | ".join(s.replace("\n", " ").strip() for s in steps if s.strip())
    lines = [
        FAIL_HEADER,
        "status: FAIL",
        f"skill: {skill}",
        f"code: {code}",
        f"source: {source}",
        f"quote_file: {quote_file}",
        f"steps: {step_line}",
        f"next_action: {next_action}",
        f"utc: {now}",
    ]
    if related_skill:
        lines.insert(5, f"related_skill: {related_skill}")
    lines.extend(["", extra.strip()])
    return "\n".join(lines).rstrip() + "\n"


def parse_aci_fail(body: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    if not body.startswith(FAIL_HEADER):
        raise ValueError("missing ACI_FAIL header")
    for line in body.splitlines()[1:]:
        if not line.strip():
            break
        if ": " not in line:
            continue
        k, v = line.split(": ", 1)
        parsed[k] = v
    return parsed


def build_message(
    *,
    to_addr: str,
    code: str,
    body: str,
    skill: str,
    from_addr: str | None = None,
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = f"{SUBJECT_PREFIX} {code}"
    msg["To"] = to_addr
    msg["From"] = from_addr or os.environ.get(
        "MAAGARIM_READER_REPORT_FROM", f"maagarim-reader@{to_addr.split('@')[-1]}"
    )
    msg["X-Maagarim-Reader-Skill"] = skill
    msg["X-Maagarim-Reader-Code"] = code
    msg.set_content(body)
    return msg


def write_report(
    out_dir: Path,
    *,
    skill: str,
    code: str,
    source: str,
    steps: list[str],
    quote_file: str,
    next_action: str,
    related_skill: str = "",
    extra: str = "",
    send: bool = False,
    mailto_open: bool = False,
) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    body = render_report(
        skill=skill,
        code=code,
        source=source,
        steps=steps,
        quote_file=quote_file,
        next_action=next_action,
        related_skill=related_skill,
        extra=extra,
    )
    to_addr = os.environ.get("MAAGARIM_READER_REPORT_TO", DEFAULT_TO)
    msg = build_message(to_addr=to_addr, code=code, body=body, skill=skill)
    eml_path = out_dir / "skill-failure.eml"
    md_path = out_dir / "skill-failure.md"
    eml_path.write_bytes(bytes(msg))
    md_path.write_text(body, encoding="utf-8")
    sent = "no"
    if send:
        host = os.environ.get("MAAGARIM_READER_SMTP_HOST")
        if host:
            port = int(os.environ.get("MAAGARIM_READER_SMTP_PORT", "587"))
            user = os.environ.get("MAAGARIM_READER_SMTP_USER")
            password = os.environ.get("MAAGARIM_READER_SMTP_PASSWORD")
            with smtplib.SMTP(host, port, timeout=30) as smtp:
                smtp.starttls()
                if user and password:
                    smtp.login(user, password)
                smtp.send_message(msg)
            sent = "smtp"
        elif mailto_open:
            subject = quote(str(msg["Subject"]))
            body_q = quote(body)
            url = f"mailto:{to_addr}?subject={subject}&body={body_q}"
            subprocess.run(["open", url], check=False)
            sent = "mailto"
    return {"eml": str(eml_path), "md": str(md_path), "sent": sent, "to": to_addr}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--code", required=True, choices=KNOWN_CODES)
    ap.add_argument(
        "--skill",
        default=DEFAULT_SKILL,
        choices=KNOWN_SKILLS,
        help="Reporting skill (default: maagarim-reader)",
    )
    ap.add_argument(
        "--related-skill",
        default="",
        help="Skill the user was running: maagarim-reader | tanakh-nikud | unknown",
    )
    ap.add_argument("--source", required=True, help="Exact skill/script location")
    ap.add_argument(
        "--step",
        action="append",
        dest="steps",
        default=[],
        help="One causal step (repeat)",
    )
    ap.add_argument("--quote-file", default="", help="User .docx name")
    ap.add_argument("--next-action", required=True)
    ap.add_argument("--extra", default="")
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Default: <repo>/output",
    )
    ap.add_argument("--send", action="store_true", help="SMTP if env is set")
    ap.add_argument(
        "--mailto-open",
        action="store_true",
        help="With --send, open a mailto: draft on macOS when SMTP is unset",
    )
    args = ap.parse_args()
    if not args.steps:
        print("at least one --step is required", file=sys.stderr)
        return 2
    repo = Path(__file__).resolve().parents[1]
    out_dir = args.out_dir or (repo / "output")
    paths = write_report(
        out_dir,
        skill=args.skill,
        code=args.code,
        source=args.source,
        steps=args.steps,
        quote_file=args.quote_file,
        next_action=args.next_action,
        related_skill=args.related_skill or "",
        extra=args.extra,
        send=args.send,
        mailto_open=args.mailto_open,
    )
    print(paths["md"])
    print(f"sent={paths['sent']} to={paths['to']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
