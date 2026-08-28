"""Regression: working Maagarim permalinks must not change shape."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from maagarim_links import (  # noqa: E402
    BAVLI_BERAKHOT,
    BAVLI_HAG_MM15_5b,
    BAVLI_HAGIGAH,
    MISHNAH,
    TOSEFTA,
    TRACTATE_HAGIGAH,
    composition_link,
    mm15_bavli_daf,
    mm15_unit,
)


def test_mishnah_unit_hagigah_1_1() -> None:
    assert mm15_unit(TRACTATE_HAGIGAH, 1, 1) == "000023001010 00"


def test_tosefta_uses_same_mm15_different_id() -> None:
    mm = mm15_unit(TRACTATE_HAGIGAH, 1, 4)
    mishnah = composition_link(MISHNAH, mm15=mm)
    tosefta = composition_link(TOSEFTA, mm15=mm)
    assert "misyzira=31000" in mishnah
    assert "misyzira=28000" in tosefta
    assert "mm15=" in mishnah and "mm15=" in tosefta
    assert "query=" not in mishnah


def test_bavli_daf_mode_hagigah_5b() -> None:
    assert mm15_bavli_daf(5, 2) == "000000000000000502"
    assert mm15_bavli_daf(5, 2) == BAVLI_HAG_MM15_5b
    url = composition_link(BAVLI_HAGIGAH, mm15=BAVLI_HAG_MM15_5b)
    assert "mishibbur=80023" in url
    assert "misyzira=" not in url
    assert "000000000000000502" in url


def test_bavli_berakhot_uses_mishibbur() -> None:
    url = composition_link(BAVLI_BERAKHOT, mm15=mm15_bavli_daf(11, 1))
    assert BAVLI_BERAKHOT == 80001
    assert "mishibbur=80001" in url
    assert "000000000000001101" in url


def test_no_query_param_on_deep_links() -> None:
    url = composition_link(MISHNAH, mm15=mm15_unit("023", 1, 1))
    assert "?query=" not in url
    assert "&page=" not in url
