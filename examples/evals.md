# Eval scenarios (smoke tests before team rollout)

Grade **outcomes**, not step order. An agent may find quotes in any sequence.

## 1. Mishnah diff → tracked change

**Input:** Verbatim quote with Vilna spelling `בתולה נשאת ליום… השני` (משנה כתובות א, א).

**Expected:**
- Comment in Hebrew naming Kaufmann A 50
- Tracked change: `נישאת` / `ביום` / `השיני`
- Comment includes working `?query=` link (not `?mishibbur=`)

## 2. Bavli diff → tracked change

**Input:** `שקדו חכמים על תקנת בנות ישראל…` (בבלי כתובות ב ע"א).

**Expected:**
- Comment names Vatican ebr. 130
- Tracked change to Vatican-readable clause (no invented «על תקנת בנות ישראל» inside Vatican text)
- `w:trackRevisions` enabled

## 3. Tanakh → silent skip

**Input:** `וְכִי יְפַתֶּה אִישׁ בְּתוּלָה…` (שמות כב).

**Expected:** No comment, no tracked change.

## 4. Paraphrase → silent skip

**Input:** «המשנה במסכת כתובות (ה, ב) מספרת על המנהג…» (not verbatim).

**Expected:** No comment.

## 5. Unfetched Bavli daf → comment only

**Input:** Quote from בבלי כתובות מז ע"ב, witness not loaded in session.

**Expected:**
- Hebrew comment: tractate/daf, witness name, «בבדיקה זו לא הושוו מילים במסירה»
- **No** invented tracked-change wording

## Automated check (reference script)

After running the Ketubot reference annotator:

```bash
python3 scripts/annotate_first_witness_docx.py \
  --input examples/fixtures/ketubot-source.docx \
  --output /tmp/ketubot-out.docx
```

Verify: `comments >= 15`, `w:ins` present on mishnah 1:1 and Bavli 2a paragraphs, zero comments on Tanakh paragraphs.

Fixture: copy your clean source to `examples/fixtures/ketubot-source.docx` (not committed if private).
