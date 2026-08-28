# Failure reporting (ACI_FAIL)

For the maintainer auto-fix loop — not shown to non-technical users.

## Trigger

Run `scripts/report_skill_failure.py` when the agent would otherwise:

- loop on Maagarim without a deliverable `.docx`
- use fetch-and-summarize instead of witness text
- guess a UUID filename while the upload is Hebrew-named
- invent a diff without loaded המסירה

## Email headers

| Header | Value |
|--------|--------|
| Subject | `[MAAGARIM-READER-ACI-FAIL] <CODE>` |
| `X-Maagarim-Reader-Skill` | `maagarim-reader` |
| `X-Maagarim-Reader-Code` | e.g. `NO_BROWSER` |

## Body format (parse line-by-line until blank line)

```
ACI_FAIL
status: FAIL
skill: maagarim-reader
code: NO_BROWSER
source: skills/maagarim-reader/SKILL.md verify loop
quote_file: ברכות 4 אוגוסט 2026.docx
steps: User uploaded Hebrew .docx | Cowork sandbox had no Chrome | Agent used fetch-and-summarize on Maagarim HTML
next_action: Fail closed: comment-only; forbid summarizer; require GetYzira or Chrome
utc: 2026-08-27T20:14:00Z
```

## Codes

| Code | Typical root cause | Skill fix |
|------|-------------------|-----------|
| `NO_BROWSER` | Cowork sandbox, no Claude in Chrome | Deliverable-first + comment-only; report; do not summarize HTML |
| `FETCH_SUMMARIZE_LOOP` | Secondary model read wrong section | Forbid fetch-and-summarize; string compare only |
| `FILENAME_ENCODING` | `____.docx` vs real Hebrew name | `find_uploaded_docx.py` at session start |
| `YERUSHALMI_NO_MM15` | No chapter mm15 for Yerushalmi | Comment-only template; no diff |
| `QUOTE_BUDGET` | >10m verify, no annotated file | Quote budget + progress updates |
| `WITNESS_NOT_LOADED` | המסירה not seen | Comment-only; no tracked change |

## Example: Berakhot Aug 2026 session (customer)

**Observed:** 16+ minutes “Working through a complex response”, file `ברכות 4 אוגוסט 2026.docx`, message about mangled underscores vs UUID.

**Causal chain:**

1. `FILENAME_ENCODING` — agent assumed UUID storage name instead of running `find_uploaded_docx.py`.
2. `NO_BROWSER` — Cowork session had no interactive Maagarim browser.
3. `FETCH_SUMMARIZE_LOOP` — agent used fetch-and-summarize; re-queried same mishnah; plausible but unverified variants.
4. `QUOTE_BUDGET` — ~20 quotes, ~2/3 verified, **no annotated Word file yet**.
5. `YERUSHALMI_NO_MM15` — expected; comment-only is correct.

**Example report command:**

```bash
python3 scripts/report_skill_failure.py \
  --code FETCH_SUMMARIZE_LOOP \
  --source "Cowork maagarim-reader session" \
  --step "Hebrew docx ברכות 4 אוגוסט 2026.docx uploaded" \
  --step "No Chrome; agent used fetch-and-summarize on Maagarim" \
  --step "16m+ without annotated docx deliverable" \
  --quote-file "ברכות 4 אוגוסט 2026.docx" \
  --next-action "Enforce quote budget; deliver partial docx; forbid summarizer" \
  --send
```
