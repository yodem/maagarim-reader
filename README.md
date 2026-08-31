# Maagarim Reader

Cowork plugin with **three skills**:

- **maagarim-reader** — Mishnah / Talmud quotes vs [Maagarim](https://maagarim.hebrew-academy.org.il)
- **tanakh-nikud** — Tanakh quotes → nikud without te'amim via [Sefaria](https://www.sefaria.org)
- **feedback** — report a problem or unclear result (דיווח)

## Validation (maintainer)

```bash
./scripts/validate.sh
```

Runs skill contract tests (forbids fetch-and-summarize, quote budget, failure-report headers).

## Share in Claude Cowork

This repo is a **Cowork plugin**. See **[COWORK.md](COWORK.md)** for:

- **Zip upload** — Customize → Plugins → Upload
- **GitHub marketplace** — Add marketplace URL, teammates install and update
- **Org marketplace** — Team/Enterprise admin provisions to everyone

Quick share: zip the folder and send it, or push to GitHub and share the repo URL.

## Tanakh nikud skill

Enable **tanakh-nikud** (not maagarim-reader) for Bible pointing. See [skills/tanakh-nikud/SKILL.md](skills/tanakh-nikud/SKILL.md).

```bash
python3 scripts/nikud_tanakh_docx.py --input path/to/article.docx
python3 scripts/nikud_tanakh_docx.py --input path/to/article.docx --dry-run
```

Overwrites the same `.docx` with tracked changes (author **Tanakh Nikud**). Backup: `<name>-pre-nikud-backup.docx`.

## Quick start (Maagarim — local script)

1. Install: `pip install -r requirements.txt`
2. Put a clean source copy at `examples/fixtures/ketubot-source.docx` (or pass `--backup`)
3. Run:

```bash
python3 scripts/annotate_first_witness_docx.py --input path/to/article.docx
```

4. Open in Word → **Review → All Markup**

The bundled script is a **Ketubot reference run** (hardcoded quote map). Cowork users should follow the skill workflow in the browser for arbitrary documents.

## Cursor skills

Copy each skill into `.cursor/skills/`:

- `skills/maagarim-reader/SKILL.md` → `@maagarim-reader`
- `skills/tanakh-nikud/SKILL.md` → `@tanakh-nikud`
- `skills/feedback/SKILL.md` → `@feedback`

## What maagarim-reader does

- Finds **verbatim Mishnah/Talmud quotes** only (skips Tanakh, ketubah, paraphrases)
- Compares against the **first Maagarim witness** when no manuscript is specified
- Adds **Hebrew comments** with working Maagarim search links
- Applies **tracked changes** where wording differs (suggestion mode)

## Share this folder

The whole directory is self-contained: skill, scripts, reference tables, and output backups.
