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
  version: "1.2.0"
---

# Maagarim Reader

Verify **verbatim Mishnah, Tosefta, Bavli, Yerushalmi** quotes in a `.docx` against [Maagarim](https://maagarim.hebrew-academy.org.il). Output: **short Hebrew RTL comments** + **tracked changes** (Word → Review → All Markup).

## Non-technical users (לא טכני)

The person who uploaded the file is **not technical**. Do not mention sandboxes, UUIDs, fetch-and-summarize, HTML, APIs, or model names unless they ask.

**Say this (Hebrew) when you are still working:**

> אני בודק את הציטוטים מול המסירה במאגרים. אעדכן כשקובץ ה-Word עם ההערות והשינויים המוצעים מוכן.

**Say this when blocked (no browser / cannot load witness):**

> לא הצלחתי לפתוח את המאגרים באופן אמין בסביבה הזו, ולכן לא אוסיף שינויי נוסח שלא נבדקו. אפשר לנסות שוב עם Claude in Chrome מחובר, או לשלוח את הקובץ למי שמריץ את הבדיקה ב-Cursor.

**Do not** send long technical post-mortems to the user. File an internal failure report instead (below).

## Session start (Cowork / Cursor)

1. **Find the file** — never assume a UUID upload name. Hebrew titles may appear as underscores in tool output.
   ```bash
   python3 scripts/find_uploaded_docx.py --root .
   ```
   Use the **newest** path printed (not under `output/`).

2. **Backup** if the doc already has tracked changes (accept into a clean copy first).

3. **List quotes** (Mishnah / Tosefta / Bavli / Yerushalmi only) with tractate + ref. Tell the user the **count** in plain Hebrew.

4. **Deliverable-first:** start writing comments + tracked changes to the `.docx` **after the first 3 verified quotes**, then continue. Do not spend the whole session only “checking” without an annotated file.

## Quote budget (lookup budget)

| Rule | Limit |
|------|--------|
| Maagarim lookups per quote | **≤ 2** (one deep link + one retry) |
| Progress update to user | every **5 quotes** or **5 minutes**, whichever comes first |
| Max verification-only time before partial deliverable | **10 minutes** |
| Yerushalmi without working mm15 | **comment-only** — no invented diffs |

If a quote exceeds the budget → comment-only for that quote and move on.

## Verify loop

1. Extract verbatim quotes (Mishnah / Tosefta / Bavli / Yerushalmi only).
2. Lookup in Maagarim:
   - **Preferred:** Claude in Chrome on a `misyzira`/`mishibbur` + **mm15** deep link → confirm **המסירה** → טקסט חופשי (3–6 words) **inside** that composition.
   - **Agent path (no click UI):** `GetYzira` / `GetYziraFull` on the open composition, then **string compare locally**.
3. Compare raw strings.
4. Annotate: tracked change on diffs; short comment-only if witness not loaded; skip silently otherwise.

### Forbidden — causes false variants and 15+ minute loops

- **Do not** use **fetch-and-summarize** (or any “load page and ask another model what it says”) for Maagarim text. That is not verification.
- **Do not** use corpus FreeText `?query=` (ORA-04036).
- **Do not** invent manuscript wording if the witness text did not load.
- **Do not** re-query the same page more than twice hoping for a different summary.

If you have **no browser** and **no GetYzira/GetYziraFull** → stop verification and file **`NO_BROWSER`** (below). Comment-only + link is OK; fake diffs are not.

## Scope

| Include | Skip silently |
|---------|----------------|
| משנה | Tanakh |
| תוספתא | Ketubah formulas |
| בבלי / ירושלמי | Paraphrases, `[glosses]` |

## Default witnesses

See [references/witnesses.md](references/witnesses.md).

| Corpus | Default mesira |
|--------|----------------|
| משנה | Kaufmann A 50 (`31000`) |
| תוספתא | Wien 46 (`28000`) |
| בבלי ברכות | Oxford Bodleian 366 (`80001`) |
| בבלי כתובות | Vatican ebr. 130 (`80025`) |
| תלמוד ירושלמי | Leiden Scaliger 3 (first hit) — **comment-only** when mm15 missing |

### Yerushalmi

There is **no reliable chapter/halakha mm15** in Maagarim for Yerushalmi in most tractates. For Yerushalmi quotes:

- Add a **short Hebrew comment** with composition + witness name + deep link to tractate start if known.
- Text: «לא הושוו מילים במסירה בבדיקה זו».
- **No** tracked-change wording unless you loaded the witness string via GetYzira.

If you catch yourself searching for a Yerushalmi mm15 pattern → file code **`YERUSHALMI_NO_MM15`** once per session (informational) and continue comment-only.

## Comments — short, Hebrew RTL

- **2–4 lines max.** Templates: [references/comment-templates.md](references/comment-templates.md).
- Hebrew body is **RTL**. English only for MS names (Kaufmann, Wien, Vatican).
- **Links:** משנה/תוספתא `?misyzira=…&mm15=…`; בבלי `?mishibbur=…&mm15=` in **daf mode** (`000000000000`+daf+amud). Never FreeText `?query=`.
- Protocol: [references/protocol-header.md](references/protocol-header.md).

Helper (print links only, no fetch):

```bash
python3 scripts/maagarim_links.py bavli-daf --daf 11 --amud 1 --id 80001
python3 scripts/maagarim_links.py mishnah-unit --tractate 001 --chapter 1 --unit 3
```

## Word rules

1. If the file already has tracked changes, **accept them** into a clean backup first.
2. Enable track revisions. Comments first, then replacements.
3. Author: `Maagarim Reader`. Set `w:bidi` on Hebrew comment paragraphs.

## Failure report (for maintainer auto-fix loop)

When any blocker below happens, **before** ending the session run:

```bash
python3 scripts/report_skill_failure.py \
  --code <CODE> \
  --source "skills/maagarim-reader/SKILL.md" \
  --step "<what happened>" \
  --step "<next causal step>" \
  --quote-file "<original .docx name>" \
  --next-action "<what the skill should do instead>" \
  --send
```

Email subject prefix (parse in your loop): **`[MAAGARIM-READER-ACI-FAIL]`**  
Body starts with **`ACI_FAIL`** block (machine-readable). Also written to `output/skill-failure.eml` and `output/skill-failure.md`.

| Code | When |
|------|------|
| `NO_BROWSER` | No Chrome / no GetYzira; agent considered fetch-and-summarize |
| `FETCH_SUMMARIZE_LOOP` | Used or attempted page summarization instead of witness text |
| `FILENAME_ENCODING` | Assumed UUID name; Hebrew path mangled to underscores |
| `YERUSHALMI_NO_MM15` | Yerushalmi — comment-only path (informational) |
| `QUOTE_BUDGET` | Exceeded lookup budget / 10m without deliverable |
| `WITNESS_NOT_LOADED` | המסירה not confirmed; would have invented a diff |

Env for SMTP `--send`: `MAAGARIM_READER_SMTP_HOST`, `MAAGARIM_READER_SMTP_PORT`, `MAAGARIM_READER_SMTP_USER`, `MAAGARIM_READER_SMTP_PASSWORD`, `MAAGARIM_READER_REPORT_TO` (default `yotam@sefaria.org`). Without SMTP, add `--mailto-open` on macOS to draft mail.

Details: [references/failure-reporting.md](references/failure-reporting.md).

## Troubleshooting

[references/troubleshooting.md](references/troubleshooting.md) — ORA-04036, homepage links, pre-existing revisions, Cowork filename mangling.

## Validation (maintainer)

```bash
python3 -m pytest tests/ -q
```

Contract tests ensure this skill forbids fetch-and-summarize, defines quote budget, and points at failure reporting.
