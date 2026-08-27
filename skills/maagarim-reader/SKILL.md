---
name: maagarim-reader
description: >-
  Checks verbatim Mishnah, Tosefta, and Talmud quotes in Word documents against
  Maagarim manuscript transcriptions. Adds short Hebrew RTL comments and Word
  tracked changes. Use for verify Talmud quotes, check nusach against manuscript,
  annotate docx with Maagarim, Kaufmann, Tosefta Wien, first witness, or
  maagarim-reader. Do not use for Sefaria-only checks, general proofreading, or
  non-verbatim quotes.
metadata:
  version: "1.1.0"
---

# Maagarim Reader

Verify **verbatim Mishnah, Tosefta, Bavli, Yerushalmi** quotes in a `.docx` against [Maagarim](https://maagarim.hebrew-academy.org.il). Output: **short Hebrew RTL comments** + **tracked changes** (Word → Review → All Markup).

## Verify loop

1. Extract verbatim quotes (Mishnah / Tosefta / Bavli / Yerushalmi only).
2. Lookup in Maagarim (browser): חיבורים → composition → המסירה → טקסט חופשי (3–6 words).
3. Compare raw strings.
4. Annotate: tracked change on diffs; short comment-only if witness not loaded; skip silently otherwise.

## Scope

| Include | Skip silently |
|---------|----------------|
| משנה | Tanakh |
| תוספתא | Ketubah formulas |
| בבלי / ירושלמי | Paraphrases, `[glosses]` |

## Default witnesses

See [references/witnesses.md](references/witnesses.md). Mishnah → Kaufmann A 50. Tosefta → Wien 46. Bavli tractate → first autocomplete hit.

## Comments — short, Hebrew RTL

- **2–4 lines max.** Templates: [references/comment-templates.md](references/comment-templates.md).
- Hebrew body is **RTL**. English only for MS names (Kaufmann, Wien, Vatican).
- **Links:** משנה/תוספתא `?misyzira=…&mm15=…`; בבלי `?mishibbur=…&mm15=` in **daf mode** (`000000000000`+daf+amud, e.g. ה ע״ב → `…000502`). Perek mm15 opens only block start — wrong for mid-sugya. Never FreeText `?query=` (ORA-04036).
- Protocol: [references/protocol-header.md](references/protocol-header.md).

## Word rules

1. If the file already has tracked changes, **accept them** into a clean backup first.
2. Enable track revisions. Comments first, then replacements.
3. Author: `Maagarim Reader`. Set `w:bidi` on Hebrew comment paragraphs.

## Maagarim lookup

1. Open `?misyzira=…&mm15=…` (or חיבורים → מסכת/פרק/משנה).
2. Confirm **המסירה:**.
3. Prefer **GetYzira** / **GetYziraFull** then search locally — same as טקסט חופשי inside the book. Corpus FreeText (`?query=` / GetMuvaot) often ORA-04036.
4. Compare raw strings; tracked change on diffs; never invent wording if text did not load.

## Troubleshooting

[references/troubleshooting.md](references/troubleshooting.md) — ORA-04036, homepage links, pre-existing revisions.
