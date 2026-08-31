"""Full-block compare — Berakhot miss regression cases (Yedidya review)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from compare_quote_span import (  # noqa: E402
    diff_spans,
    needs_tracked_change,
    normalize_for_compare,
)


def test_match_when_letters_identical() -> None:
    doc = "כל אדם קורין כדרכן"
    witness = "כל אדם קורין כדרכן"
    assert not needs_tracked_change(doc, witness)
    assert diff_spans(doc, witness) == []


def test_hen_hen_vs_hen_bavli_15a() -> None:
    doc = "אחר כונת הלב הן הן הדברים"
    witness = "אחר כונת הלב הן הדברים"
    assert needs_tracked_change(doc, witness)
    diffs = diff_spans(doc, witness)
    assert diffs
    assert normalize_for_compare(doc) != normalize_for_compare(witness)


def test_haomanin_vs_haamanim_mishnah_2_4() -> None:
    doc = "האומנין קורין בראש האילן"
    witness = "האמנים קורין בראש האילן"
    assert needs_tracked_change(doc, witness)


def test_bar_mar_missing_in_witness() -> None:
    doc = "אמר רב נתן בר מר עוקבא אמר רב יהודה"
    witness = "אמר רב נתן בר עוקבא אמר רב יהודה"
    assert needs_tracked_change(doc, witness)
    assert len(normalize_for_compare(doc)) > len(normalize_for_compare(witness))
    diffs = diff_spans(doc, witness)
    assert any(d["kind"] == "delete" and d["witness"] == "" for d in diffs)


def test_betokh_arba_vs_barba() -> None:
    doc = "מכאן שאסור לישב בתוך ארבע אמות של תפילה"
    witness = "מכאן שאסור לישב בארבע אמות של תפילה"
    assert needs_tracked_change(doc, witness)


def test_kedei_she_vs_ela_mishnah_opening() -> None:
    doc = "למה קדמה פרשת שמע כדי שיקבל עליו"
    witness = "למה קדמה פרשת שמע אלא שיקבל עליו"
    assert needs_tracked_change(doc, witness)


def test_brackets_stripped_before_compare() -> None:
    doc = "כדי שיקבל עליו [עול] מלכות שמים"
    witness = "כדי שיקבל עליו מלכות שמים"
    assert not needs_tracked_change(doc, witness)
