#!/usr/bin/env python3
"""List Mishnah / Tosefta / Bavli / Yerushalmi quote candidates in a Word doc.

Academic articles often split quotes across paragraphs with empty "" markers.
This script builds a numbered inventory for the maagarim-reader verify loop.

Usage:
  python3 scripts/list_docx_quotes.py --input article.docx
  python3 scripts/list_docx_quotes.py --input article.docx --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from hebrew_nikud import letters_only  # noqa: E402

CITE_TAIL = re.compile(
    r"\((?:משנה|תוספתא|בבלי|ירושלמי|תלמוד)[^)]{0,80}\)\s*$"
)
CITE_INLINE = re.compile(
    r"\((?:משנה|תוספתא|בבלי|ירושלמי)\s+[^)]+\)"
)
TANU_RABANAN = re.compile(r"^תנ[״\"']?\s*ו\s+רבנן")
AMAR_OPEN = re.compile(r"^(?:אמר|א\"?מ|ד?אמר)\s+")
HEBREW_LETTER = re.compile(r"[\u05D0-\u05EA]")


def _has_hebrew(s: str) -> bool:
    return bool(HEBREW_LETTER.search(s or ""))


def _clean_para(text: str) -> str:
    return (text or "").replace("\u00a0", " ").strip()


def _extract_ref(text: str) -> str | None:
    m = CITE_TAIL.search(text)
    if m:
        return m.group(0).strip("() ")
    m = CITE_INLINE.search(text)
    return m.group(0).strip("() ") if m else None


def _quote_body(text: str) -> str:
    t = _clean_para(text)
    m = CITE_TAIL.search(t)
    if m:
        t = t[: m.start()].strip()
    return t


def _is_quote_start(text: str) -> bool:
    t = _clean_para(text)
    if not _has_hebrew(t):
        return False
    if TANU_RABANAN.search(t):
        return True
    if CITE_TAIL.search(t) and len(letters_only(_quote_body(t))) >= 12:
        return True
    if AMAR_OPEN.search(t) and CITE_INLINE.search(t):
        return True
    if re.search(r"^(?:בית|ורבי|רבי|משנה|האומ)", t) and CITE_TAIL.search(t):
        return True
    return False


def _continues_quote(prev_body: str, text: str) -> bool:
    t = _clean_para(text)
    if not _has_hebrew(t):
        return False
    if _is_quote_start(t):
        return False
    if CITE_TAIL.search(t):
        return True
    if prev_body and not t.startswith("(") and len(letters_only(t)) >= 8:
        return True
    return False


def collect_quotes(doc: Document) -> list[dict]:
    paras = [_clean_para(p.text) for p in doc.paragraphs]
    quotes: list[dict] = []
    i = 0
    while i < len(paras):
        if not _is_quote_start(paras[i]):
            i += 1
            continue
        start = i
        parts = [_quote_body(paras[i])]
        ref = _extract_ref(paras[i])
        i += 1
        while i < len(paras) and _continues_quote(parts[-1], paras[i]):
            body = _quote_body(paras[i])
            if body:
                parts.append(body)
            r2 = _extract_ref(paras[i])
            if r2:
                ref = r2
            i += 1
        full = " ".join(p for p in parts if p).strip()
        if len(letters_only(full)) < 8:
            continue
        corpus = "unknown"
        if ref:
            if ref.startswith("משנה"):
                corpus = "mishnah"
            elif ref.startswith("תוספתא"):
                corpus = "tosefta"
            elif ref.startswith("בבלי"):
                corpus = "bavli"
            elif ref.startswith("ירושלמי"):
                corpus = "yerushalmi"
        elif TANU_RABANAN.search(full):
            corpus = "bavli"
        quotes.append(
            {
                "id": len(quotes) + 1,
                "start_para": start,
                "end_para": i - 1,
                "ref": ref or "",
                "corpus": corpus,
                "preview": full[:120],
                "letters": len(letters_only(full)),
                "text": full,
            }
        )
    return quotes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", "-i", required=True, type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    path = args.input.expanduser().resolve()
    if not path.exists():
        print(f"missing input: {path}", file=sys.stderr)
        return 1
    doc = Document(str(path))
    quotes = collect_quotes(doc)
    if args.json:
        print(json.dumps(quotes, ensure_ascii=False, indent=2))
        return 0
    print(f"Found {len(quotes)} quote candidate(s)\n")
    for q in quotes:
        ref = q["ref"] or "(no ref — verify manually)"
        print(f"{q['id']:3d}. [{q['corpus']}] paras {q['start_para']}–{q['end_para']} | {ref}")
        print(f"     {q['preview']}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
