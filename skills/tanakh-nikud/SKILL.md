---
name: tanakh-nikud
description: >-
  Adds nikud without te'amim to unpointed Tanakh (Bible) quotations in Word
  documents, using Sefaria. Use for menukadim bli te'amim, auto-nikud, Tanakh
  pointing, Bible quotes in docx, or tanakh-nikud. Do not use for Mishnah,
  Talmud, Maagarim manuscript checks, or general proofreading.
metadata:
  version: "1.0.0"
---

# Tanakh Nikud (מנוקד בלי טעמים)

Add **nikud without te'amim** to unpointed **Tanakh** quotations in a `.docx`. Source: [Sefaria](https://www.sefaria.org) edition **Tanach with Nikkud**. Output: Word **tracked changes** (author **Tanakh Nikud**).

**Not Maagarim.** For Mishnah / Tosefta / Bavli manuscript checks, use **maagarim-reader**.  
If something went wrong, use **feedback** (דיווח).

## Non-technical users (לא טכני)

Do not mention APIs, Sefaria internals, or script names unless asked.

**While working (Hebrew):**

> אני מוסיף ניקוד לציטוטי תנ״ך בקובץ. אעדכן כשהגרסה עם השינויים המוצעים מוכנה.

**If blocked:**

> לא הצלחתי להשלים את הניקוד אוטומטית. אפשר לנסות שוב או לבדוק ידנית מול ספריא.

## Session start

1. **Find the file** (Hebrew names may show as underscores in Cowork):
   ```bash
   python3 scripts/find_uploaded_docx.py --root .
   ```

2. **Prefer the script** (deterministic, fast):
   ```bash
   pip install -r requirements.txt   # once
   python3 scripts/nikud_tanakh_docx.py --input <path>.docx --dry-run
   python3 scripts/nikud_tanakh_docx.py --input <path>.docx
   ```

   Overwrites the same file with **tracked changes** (suggestion mode). Backup: `<name>-pre-nikud-backup.docx`.

3. Open result in Word → **Review → All Markup**.

## What the script does

1. `POST /api/find-refs` (he + en) → Tanakh citation spans
2. `GET /api/texts/…?vhe=Tanach with Nikkud` per ref
3. Match unpointed (or trop-bearing) Hebrew in the doc
4. Replace with **menukadim bli te'amim** via tracked changes

Flags: `--dry-run` (plan only) · `--no-strip-teamim` (only fill missing nikud) · `--min-letters 8`

## Agent path (no script)

If you cannot run Python:

1. Extract body text from the `.docx`
2. Call Sefaria `find-refs` for Tanakh hits only
3. Fetch **Tanach with Nikkud** for each ref (`vhe=Tanach with Nikkud`)
4. Strip te'amim (U+0591–U+05AF) if present; keep nikud
5. Apply tracked changes in reverse character order (longest spans first)

Do **not** invent nikud — only text that matches Sefaria letter-for-letter after stripping punctuation.

## Scope

| Include | Skip |
|---------|------|
| Verbatim Tanakh quotes (pointed or unpointed) | Mishnah, Tosefta, Bavli, Yerushalmi |
| Partial quotes next to a citation (e.g. `בראשית א,א`) | Paraphrases |
| Strip te'amim when `--strip-teamim` (default) | Ketubah formulas |

## Helpers

- `scripts/nikud_tanakh_docx.py` — main annotator
- `scripts/sefaria_client.py` — find-refs + Tanach with Nikkud fetch
- `scripts/hebrew_nikud.py` — nikud vs te'amim Unicode
- `scripts/find_uploaded_docx.py` — resolve Hebrew upload paths

Fixture: `examples/fixtures/tanakh-nikud-sample.docx`

## Validation

```bash
./scripts/validate.sh
```
