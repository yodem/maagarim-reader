"""Compare a document quote span to a loaded Maagarim witness string.

Full-block rule: normalize to Hebrew letters, diff the entire quoted span — not a
3–6 word search hit. Used by maagarim-reader agents after GetYzira / browser load.
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from hebrew_nikud import letters_only  # noqa: E402

_BRACKETS = re.compile(r"\[[^\]]*\]")
_QUOTE_MARKS = re.compile(r'[""«»„‟]')


def normalize_for_compare(text: str) -> str:
    """Letters-only, no nikud/te'amim, no editorial brackets."""
    s = _BRACKETS.sub("", text or "")
    s = _QUOTE_MARKS.sub("", s)
    return letters_only(s)


def diff_spans(doc_span: str, witness_span: str) -> list[dict[str, str]]:
    """Return letter-level diff chunks when doc and witness disagree."""
    doc = normalize_for_compare(doc_span)
    witness = normalize_for_compare(witness_span)
    if doc == witness:
        return []

    sm = difflib.SequenceMatcher(None, doc, witness, autojunk=False)
    out: list[dict[str, str]] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        out.append(
            {
                "kind": tag,
                "doc": doc[i1:i2],
                "witness": witness[j1:j2],
            }
        )
    return out


def needs_tracked_change(doc_span: str, witness_span: str) -> bool:
    """True when letter-normalized spans differ."""
    return normalize_for_compare(doc_span) != normalize_for_compare(witness_span)


def main() -> int:
    import argparse
    import json

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--doc", required=True, help="Quote text from the article")
    ap.add_argument("--witness", required=True, help="Witness text from Maagarim")
    ap.add_argument("--json", action="store_true", help="Print diff as JSON")
    args = ap.parse_args()
    diffs = diff_spans(args.doc, args.witness)
    if args.json:
        print(json.dumps(diffs, ensure_ascii=False, indent=2))
    else:
        if not diffs:
            print("match")
        for d in diffs:
            print(f"{d['kind']}: doc={d['doc']!r} witness={d['witness']!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
