"""Hebrew nikud / te'amim helpers for Tanakh quote pointing."""

from __future__ import annotations

import re
import unicodedata

# Cantillation (te'amim). Keep nikud (U+05B0–05BD, etc.).
# Mirrors Sefaria strip_cantillation(..., strip_vowels=False) ranges.
_TEAMIM = re.compile(r"[\u0591-\u05AF\u05C0\u05C4\u05C5]")

# Nikud / vowel points (+ shin/sin dots, rafe, qamats qatan).
_NIKUD = re.compile(r"[\u05B0-\u05BD\u05BF\u05C1\u05C2\u05C7]")

# Consonants only (for matching unpointed quotes to pointed verses).
_LETTERS = re.compile(r"[\u05D0-\u05EA]")

# Soft HTML from older Sefaria payloads (<big>, …).
_HTML = re.compile(r"<[^>]+>")

# Sof pasuq / paseq noise often omitted in prose quotes.
_VERSE_PUNCT = re.compile(r"[\u05C0\u05C3׃׃\.\,\;\:\"\'\«\»\(\)\[\]]+")


def normalize_nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s or "")


def strip_html(s: str) -> str:
    return _HTML.sub("", s or "")


def strip_teamim(s: str) -> str:
    """Keep nikud; drop te'amim (menukadim bli te'amim)."""
    return _TEAMIM.sub("", normalize_nfc(s))


def has_nikud(s: str) -> bool:
    return bool(_NIKUD.search(s or ""))


def has_teamim(s: str) -> bool:
    return bool(_TEAMIM.search(s or ""))


def letters_only(s: str) -> str:
    return "".join(_LETTERS.findall(s or ""))


def needs_nikud(s: str) -> bool:
    """True if the span has Hebrew letters but no nikud."""
    if not letters_only(s):
        return False
    return not has_nikud(s)


def needs_teamim_strip(s: str) -> bool:
    """True if pointed text still carries te'amim."""
    return has_nikud(s) and has_teamim(s)


def menukad_bli_teamim(s: str) -> str:
    """Normalize Sefaria verse → nikud, no te'amim, no HTML."""
    s = strip_html(s)
    s = strip_teamim(s)
    # Collapse odd spaces after mark removal.
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s


def match_unpointed_in_haystack(
    haystack: str,
    verse_pointed: str,
    *,
    min_letters: int = 8,
) -> list[tuple[int, int, str]]:
    """Find doc spans whose letters match a contiguous slice of the verse.

    Returns every non-overlapping match in *haystack* (full verse first, then
    longest remaining partials). Caller still filters by needs_nikud / te'amim.
    """
    verse = menukad_bli_teamim(verse_pointed)
    target = letters_only(verse)
    if len(target) < min_letters:
        return []

    letter_to_char: list[int] = []
    letters: list[str] = []
    for i, ch in enumerate(haystack):
        if _LETTERS.match(ch):
            letter_to_char.append(i)
            letters.append(ch)
    letter_str = "".join(letters)
    if len(letter_str) < min_letters:
        return []

    occupied: list[tuple[int, int]] = []  # letter-index ranges

    def letter_free(a: int, b: int) -> bool:
        for x, y in occupied:
            if not (b <= x or a >= y):
                return False
        return True

    def add_letter_span(a: int, b: int) -> tuple[int, int, str] | None:
        if not letter_free(a, b):
            return None
        occupied.append((a, b))
        c0 = letter_to_char[a]
        c1 = letter_to_char[b - 1] + 1
        return (c0, c1, haystack[c0:c1])

    hits: list[tuple[int, int, str]] = []

    # 1) Every full-verse occurrence
    start = 0
    while True:
        idx = letter_str.find(target, start)
        if idx < 0:
            break
        hit = add_letter_span(idx, idx + len(target))
        if hit:
            hits.append(hit)
        start = idx + 1

    # 2) Remaining longest partials (any substring of the verse)
    n = len(target)
    for length in range(n - 1, min_letters - 1, -1):
        for i in range(0, n - length + 1):
            chunk = target[i : i + length]
            start = 0
            while True:
                j = letter_str.find(chunk, start)
                if j < 0:
                    break
                hit = add_letter_span(j, j + length)
                if hit:
                    hits.append(hit)
                start = j + 1

    return hits
