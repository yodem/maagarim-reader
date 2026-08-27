"""Maagarim link helpers for Word comments.

Deep links (site permalinks):
  משנה / תוספתא: ?misyzira={id}&mm15={code}   (calcYziraLink)
  בבלי / ירושלמי: ?mishibbur={id}&mm15={code}  (GetUrlForHibur; misyzira often
                                                homepage-bounces on Bavli)

Do NOT use:
  - ?query=…  — corpus FreeText → ORA-04036
  - ?mishibbur=…&page=… without mm15 — often empty homepage UI
  - ?misyzira=… alone on multi-tractate books — opens at ברכות
"""

from __future__ import annotations

from urllib.parse import quote

SITE = "https://maagarim.hebrew-academy.org.il/Pages/PMain.aspx"

# First-autocomplete compositions (agent + comment links OK)
MISHNAH = 31000  # Kaufmann A 50
TOSEFTA = 28000  # Wien 46
BAVLI_HAGIGAH = 80023  # Munich 6
BAVLI_RH = 80019  # JTS EMC 270

# Tractate codes (mm dropdown) — same for משנה / תוספתא
TRACTATE_HAGIGAH = "023"
TRACTATE_RH = "019"

# Bavli Hagigah Munich — daf-mode mm15 (UI: מסכת → דף): 12×0 + daf + amud
# Prefer this over perek/mishnah mm15 (that opens only at the start of the long block).
BAVLI_HAG_MM15_2a = "000000000000000201"  # דף ב עמ' א
BAVLI_HAG_MM15_5b = "000000000000000502"  # דף ה עמ' ב


def mm15_bavli_daf(daf: int, amud: int) -> str:
    """Bavli daf-mode mm15: ``000000000000`` + ``{daf:04d}`` + ``{amud:02d}``.

    ``amud``: 1 = עמוד א, 2 = עמוד ב.
    Example: Hagigah 5b → ``mm15_bavli_daf(5, 2)`` → ``000000000000000502``.
    """
    if amud not in (1, 2):
        raise ValueError("amud must be 1 (א) or 2 (ב)")
    return f"{'0' * 12}{int(daf):04d}{int(amud):02d}"


def _id_param(composition_id: int) -> str:
    """Bavli/Yerushalmi permalinks use mishibbur; Mishnah/Tosefta use misyzira."""
    return "mishibbur" if int(composition_id) >= 80000 else "misyzira"


def mm15_unit(
    tractate: str,
    chapter: int,
    unit: int,
    *,
    bavli: bool = False,
    suffix: str = "00",
) -> str:
    """Build an mm15 locator.

    Mishnah/Tosefta: ``0000{TT}{CCC}{UUU} {suffix}``
      e.g. חגיגה א,א → ``000023001010 00`` (tractate 023, ch 1, unit 1→010).

    Prefer reading ``.esBlock[mm15]`` from a live page when unsure.
    """
    tt = str(tractate).zfill(3)[-3:]
    ch = f"{int(chapter):03d}"
    uu = f"{int(unit) * 10:03d}"
    core = f"{tt}{ch}{uu}"
    if bavli:
        return f"001{core} {suffix}"
    return f"000{core} {suffix}"


def composition_link(
    composition_id: int,
    *,
    mm15: str | None = None,
    page: int | None = None,
) -> str:
    """Deep link into a composition.

    **Always pass mm15 when known.** Bavli uses ``mishibbur``; משנה/תוספתא use
    ``misyzira``. ``page`` alone is unreliable.
    """
    mid = int(composition_id)
    key = _id_param(mid)
    if mm15:
        return f"{SITE}?{key}={mid}&mm15={quote(mm15, safe='')}"
    if page is not None:
        return f"{SITE}?{key}={mid}&page={int(page)}"
    return f"{SITE}?{key}={mid}"


def find_instructions(
    *,
    composition: str,
    mesira: str,
    search_phrase: str,
    mishibbur: int,
    cite: str | None = None,
    page: int | None = None,
    mm15: str | None = None,
) -> str:
    """Short Hebrew nav + working deep link + FreeText phrase to type inside."""
    words = search_phrase.strip().split()
    short = " ".join(words[:5]) if len(words) > 5 else search_phrase.strip()
    link = composition_link(mishibbur, mm15=mm15, page=page)
    line = f"{link}\nבתוך החיבור → טקסט חופשי: «{short}»"
    head = f"{cite} | {composition} ({mesira})" if cite else f"{composition} ({mesira})"
    return f"{head}\n{line}"


def search_link(phrase: str, *, page: int = 1) -> str:
    """Deprecated FreeText URL — often ORA-04036. Prefer composition_link(mm15=…)."""
    return f"{SITE}?query={quote(phrase)}&page={page}"
