# Maagarim Reader

Check Mishnah and Talmud quotes in Word documents against [Maagarim](https://maagarim.hebrew-academy.org.il) manuscript transcriptions.

## Share in Claude Cowork

This repo is a **Cowork plugin**. See **[COWORK.md](COWORK.md)** for:

- **Zip upload** — Customize → Plugins → Upload
- **GitHub marketplace** — Add marketplace URL, teammates install and update
- **Org marketplace** — Team/Enterprise admin provisions to everyone

Quick share: zip the folder and send it, or push to GitHub and share the repo URL.

## Tanakh nikud (bli te'amim)

Add nikud without cantillation to unpointed Bible quotes in a `.docx`, using Sefaria
(`find-refs` + `Tanach with Nikkud`):

```bash
python3 scripts/nikud_tanakh_docx.py --input path/to/article.docx
python3 scripts/nikud_tanakh_docx.py --input path/to/article.docx --dry-run
```

Output defaults to `output/nikud-tanakh.docx` (tracked changes; author **Tanakh Nikud**).
See `examples/fixtures/tanakh-nikud-sample.docx` for a smoke-test input.

## Quick start (local script)

1. Install: `pip install -r requirements.txt`
2. Put a clean source copy at `examples/fixtures/ketubot-source.docx` (or pass `--backup`)
3. Run:

```bash
python3 scripts/annotate_first_witness_docx.py --input path/to/article.docx
```

4. Open in Word → **Review → All Markup**

The bundled script is a **Ketubot reference run** (hardcoded quote map). Cowork users should follow the skill workflow in the browser for arbitrary documents.

## Cursor skill

Copy `skills/maagarim-reader/SKILL.md` to `.cursor/skills/maagarim-reader/SKILL.md`, or attach `@maagarim-reader` in chat.

## What it does

- Finds **verbatim Mishnah/Talmud quotes** only (skips Tanakh, ketubah, paraphrases)
- Compares against the **first Maagarim witness** when no manuscript is specified
- Adds **Hebrew comments** with working Maagarim search links
- Applies **tracked changes** where wording differs (suggestion mode)

## Share this folder

The whole directory is self-contained: skill, scripts, reference tables, and output backups.
