# Troubleshooting

## ORA-04036 / PGA_AGGREGATE_LIMIT

Oracle error from Maagarim’s server: FreeText over the **whole corpus** used too much PGA memory and was killed.

**Cause:** links like `?query=…` (טקסט חופשי on everything).

**Avoid:** use composition deep links with **mm15**:

| Composition | Reliable link |
|-------------|---------------|
| משנה חגיגה א,א (Kaufmann) | `…PMain.aspx?misyzira=31000&mm15=000023001010%2000` |
| תוספתא חגיגה א,ד (Wien) | `…PMain.aspx?misyzira=28000&mm15=000023001040%2000` |
| בבלי חגיגה ה ע״ב (Munich) | `…PMain.aspx?mishibbur=80023&mm15=000000000000000502` |

Then inside the open composition: **טקסט חופשי** with 3–6 words (do not paste a corpus-wide `?query=` URL).

## How to search משנה / תוספתא on the site

1. Open a `?misyzira=…&mm15=…` link (or חיבורים → composition → מסכת/פרק/משנה).
2. Confirm **המסירה**.
3. **טקסט חופשי** inside that חיבור (3–6 words).

**Agent path:** `GetYzira` / `GetYziraFull` loads the witness; search/compare locally (avoids FreeText OOM). Read `mm15` from `.esBlock` for comment links.

## Homepage / empty UI (0 blocks)

| URL style | Typical result |
|-----------|----------------|
| `?query=…` | ORA-04036 |
| `?mishibbur=…` alone | Opens ברכות (start of משנה/תוספתא) |
| `?mishibbur=…&page=…` | Often **homepage bounce** — URL sticks, 0 blocks |
| `?misyzira=…` alone | Same as mishibbur alone on multi-tractate books |
| `?misyzira=…&mm15=…` | **Works** — site’s own `calcYziraLink` format |

**Fix:** always use `misyzira` + `mm15`. Do not rely on `page=` as a permalink.

## Cowork: Hebrew filename → underscores

Cowork may show a Hebrew upload as `____ _ _______ ____.docx` in tool logs. **Do not** guess a UUID path.

```bash
python3 scripts/find_uploaded_docx.py --root .
```

Use the newest `.docx` returned. If none → tell the user (in Hebrew) the file was not found and ask them to re-upload.

## Tracked changes look wrong / stacked

Accept existing ins/del into a clean backup before annotating.
