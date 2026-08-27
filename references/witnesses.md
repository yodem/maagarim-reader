# Default Maagarim witnesses (first autocomplete hit)

| Search in חיבורים | misyzira (same as mishibbur) | Default mesira |
|-------------------|------------------------------|----------------|
| משנה | 31000 | Kaufmann A 50 |
| תוספתא | 28000 | Wien, Oesterreichische Nationalbibliothek, 46 |
| תלמוד בבלי, חגיגה | 80023 | Munich, Bayerische Staatsbibliothek, 6 |
| תלמוד בבלי, כתובות | 80025 | Vatican ebr. 130 |
| תלמוד בבלי, יבמות | 80024 | first hit (verify header) |
| תלמוד בבלי, קידושין | 80030 | first hit (verify header) |
| תלמוד בבלי, ראש השנה | 80019 | New York, JTS, EMC 270 |
| תלמוד ירושלמי, כתובות | 90025 | first hit (verify header) |

## Comment links (required format)

Use the site’s own permalink (`calcYziraLink`):

```
…/PMain.aspx?misyzira={ID}&mm15={code}
```

Encode the space in `mm15` as `%20`.

**Do not use** `?mishibbur=…&page=…` — often sticks in the URL but shows the empty homepage UI.  
**Do not use** FreeText `?query=` — ORA-04036.

### mm15 for משנה / תוספתא

Pattern: `0000{tractate}{chapter:03d}{unit×10:03d} 00`

| Tractate | code |
|----------|------|
| חגיגה | `023` |
| ראש השנה | `019` |
| כתובות | `025` |

Examples (חגיגה): א,א `000023001010 00` · א,ב `000023001020 00` · ב,א `000023002010 00` · ג,ח `000023003080 00`.

Same mm15 codes work for משנה **and** תוספתא — the `misyzira` id selects the book (31000 vs 28000).

Prefer reading `.esBlock[mm15]` from a live page when the unit has a variant (e.g. `…031` vs `…030`).

### Bavli

Use **`mishibbur`** (not `misyzira`) with **daf-mode** `mm15`:

```
000000000000{daf:04d}{amud:02d}
```

`amud`: `01` = עמוד א, `02` = עמוד ב.

| Location | Link |
|----------|------|
| חגיגה ב ע״א | `…?mishibbur=80023&mm15=000000000000000201` |
| חגיגה ה ע״ב | `…?mishibbur=80023&mm15=000000000000000502` |

Do **not** use perek/mishnah mm15 (`001001001010 00`) for a mid-sugya quote — that opens only at the start of פרק א משנה א (דף ב).

**How to look up:** open the `misyzira`+`mm15` link → confirm **המסירה** → טקסט חופשי with 3–6 words **inside** that composition. Agent path: `GetYziraFull` / `GetYzira` then compare locally.

**Skip silently:** Tanakh, ketubah formulas, paraphrases.
