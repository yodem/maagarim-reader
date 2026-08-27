# Comment templates (Hebrew, RTL, short)

**2–4 short lines.** Hebrew body; English only for MS names.

## Diff + suggestion mode

```
שונה מ-[witness] ([ציטוט]).
במאמר: … | במסירה: …
https://maagarim.hebrew-academy.org.il/Pages/PMain.aspx?misyzira=[ID]&mm15=[CODE]
בתוך החיבור → טקסט חופשי: «[3–6 מילים]»
```

Encode the space in `mm15` as `%20` (e.g. `000023001010%2000`).

## Comment only (witness not loaded)

```
[ציטוט] מול [witness].
לא הושוו מילים במסירה בבדיקה זו.
https://maagarim.hebrew-academy.org.il/Pages/PMain.aspx?misyzira=[ID]&mm15=[CODE]
בתוך החיבור → טקסט חופשי: «[3–6 מילים]»
```

IDs: משנה `31000` · תוספתא `28000` · בבלי חגיגה `80023` · כתובות `80025`  
חגיגה mm15: א,א `000023001010 00` · ב,א `000023002010 00` (same codes for משנה/תוספתא; `misyzira` picks the book).

## Protocol (title)

```
בדיקת ציטוטי משנה / תוספתא / תלמוד במאגרים.
עדות ראשונה אם לא צוין כתב יד. Word → סקירה → כל הסימונים.
```

## Do not

- FreeText `?query=` links (ORA-04036)
- `?mishibbur=…&page=…` (homepage bounce)
- Long navigation essays
