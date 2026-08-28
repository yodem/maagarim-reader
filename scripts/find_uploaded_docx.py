#!/usr/bin/env python3
"""Find uploaded Word files even when Cowork mangles Hebrew names to underscores.

Prints one absolute path per line. Prefer the newest .docx that is not under output/.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKIP_DIR_NAMES = frozenset({".git", "output", "__pycache__", "node_modules"})


def find_docx(root: Path) -> list[Path]:
    root = root.resolve()
    hits: list[Path] = []
    for p in root.rglob("*.docx"):
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        if p.name.startswith("~$"):
            continue
        hits.append(p)
    hits.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Workspace root (default: cwd)",
    )
    args = ap.parse_args()
    hits = find_docx(args.root)
    if not hits:
        print("no .docx found", file=sys.stderr)
        return 1
    for p in hits:
        print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
