"""Hebrew / mangled Cowork filenames must still resolve to a .docx."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from find_uploaded_docx import find_docx  # noqa: E402


def test_finds_hebrew_filename(tmp_path: Path) -> None:
    hebrew = tmp_path / "ברכות 4 אוגוסט 2026.docx"
    hebrew.write_bytes(b"PK\x03\x04")
    hits = find_docx(tmp_path)
    names = [p.name for p in hits]
    assert "ברכות 4 אוגוסט 2026.docx" in names


def test_finds_underscore_mangled_name(tmp_path: Path) -> None:
    mangled = tmp_path / "____ _ _______ ____.docx"
    mangled.write_bytes(b"PK\x03\x04")
    hits = find_docx(tmp_path)
    assert mangled.resolve() in [p.resolve() for p in hits]


def test_skips_output_dir(tmp_path: Path) -> None:
    (tmp_path / "output").mkdir()
    skip = tmp_path / "output" / "annotated.docx"
    skip.write_bytes(b"PK\x03\x04")
    keep = tmp_path / "article.docx"
    keep.write_bytes(b"PK\x03\x04")
    hits = find_docx(tmp_path)
    assert keep.resolve() in [p.resolve() for p in hits]
    assert skip.resolve() not in [p.resolve() for p in hits]
