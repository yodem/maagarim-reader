---
name: feedback
description: >-
  Report a problem or unclear result from maagarim-reader or tanakh-nikud in plain
  Hebrew. Sends a structured report to the maintainer. Use for feedback, something
  went wrong, the check did not finish, report issue, or דיווח תקלה.
metadata:
  version: "1.0.0"
---

# Feedback (דיווח)

For **non-technical researchers** after a Cowork session that failed, stalled, or produced unclear results.

You are **not** fixing the document here — you are collecting what happened and filing a report the maintainer can act on.

## When to use

- Maagarim or nikud check ran a long time with **no finished Word file**
- Output looks wrong but the user cannot say why technically
- User says «זה לא עבד» / «לא קיבלתי קובץ» / «לא בטוחה בתוצאה»
- **Proactively** after another skill hits a blocker (run feedback in the same session if possible)

## What to ask the user (Hebrew, 3 questions max)

1. **איזה קובץ?** (שם ה-Word שהעלית)
2. **מה ציפית שיקרה?** (משפט אחד)
3. **מה קרה בפועל?** (משפט אחד — זמן המתנה, בלי קובץ, הערות מוזרות, וכו')

Do **not** ask about sandboxes, APIs, or skill names.

## Agent steps

1. Note which skill they were using: **maagarim-reader**, **tanakh-nikud**, or **unknown**.
2. Resolve the file name if needed:
   ```bash
   python3 scripts/find_uploaded_docx.py --root .
   ```
3. Pick the closest **code** (see table below).
4. File the report:
   ```bash
   python3 scripts/report_skill_failure.py \
     --skill feedback \
     --related-skill maagarim-reader \
     --code USER_REPORT \
     --source "skills/feedback/SKILL.md" \
     --step "<user: what they expected>" \
     --step "<user: what actually happened>" \
     --step "<agent: technical cause if known>" \
     --quote-file "<docx name>" \
     --next-action "<one line for maintainer>" \
     --extra "<optional: session duration, quotes checked, etc>" \
     --send --mailto-open
   ```
5. Tell the user (Hebrew):

   > תודה — דיווחתי ליוטם. נחזור אלייך אחרי שנבדוק. אם נשמר קובץ חלקי, הוא ב-output.

## Codes (pick one)

| Code | User said / you observed |
|------|---------------------------|
| `USER_REPORT` | General problem; user-initiated feedback |
| `SESSION_STUCK` | Long wait (e.g. 10+ min), no clear progress message |
| `PARTIAL_RESULT` | Some checks done but no final annotated `.docx` |
| `WRONG_OUTPUT` | File returned but comments/changes look wrong |
| `NO_BROWSER` | Maagarim could not load (no Chrome) |
| `FETCH_SUMMARIZE_LOOP` | Agent summarized pages instead of real witness text |
| `FILENAME_ENCODING` | Hebrew filename showed as underscores |
| `QUOTE_BUDGET` | Too many lookups, never delivered |
| `WITNESS_NOT_LOADED` | Diff suggested without loaded המסירה |

## Maintainer email

- Subject: `[MAAGARIM-READER-ACI-FAIL] <CODE>`
- Machine block: `ACI_FAIL` in `output/skill-failure.md`
- Details: [references/failure-reporting.md](references/failure-reporting.md)

## Do not

- Promise a fix timeline
- Debug Maagarim in front of the user for more than 2 minutes
- Re-run a full maagarim-reader check inside feedback — only report
