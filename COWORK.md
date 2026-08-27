# Sharing Maagarim Reader in Claude Cowork

This folder is a **Cowork plugin** — a packaged skill plus scripts. Cowork does not use Cursor’s `.cursor/skills/` path.

## What colleagues install

One plugin named **maagarim-reader** with:

- Skill: check Mishnah/Talmud quotes against [Maagarim](https://maagarim.hebrew-academy.org.il)
- Scripts: optional Word annotator (`python-docx`)
- Browser: Maagarim lookups via **Claude in Chrome** (no Maagarim connector exists)

---

## Option A — Send a zip (fastest, small team)

1. Zip this folder (exclude `output/*.docx` if you like):

```bash
cd /path/to/parent
zip -r maagarim-reader.zip maagarim-reader -x "*.docx"
```

2. Colleague opens **Cowork → Customize → Plugins**.
3. **Upload** the zip (or a `.plugin` file if Cowork exported one from Customize).
4. Install **maagarim-reader** and enable the skill.

They invoke it by starting a Cowork task and naming the skill, e.g. “use maagarim-reader to check my Word file.”

---

## Option B — GitHub marketplace (best for updates)

1. Push this repo to **public GitHub** (Cowork directory submission requires public repos for the official catalog; private GitHub works for **Add marketplace** on Team/Enterprise).

```bash
cd maagarim-reader
git init
git add .claude-plugin skills scripts references SKILL.md COWORK.md README.md
git commit -m "Maagarim Reader Cowork plugin"
git remote add origin https://github.com/YOU/maagarim-reader.git
git push -u origin main
```

2. Colleague: **Customize → Plugins → Add marketplace**.
3. Enter `https://github.com/YOU/maagarim-reader` (or `YOU/maagarim-reader`).
4. Install **maagarim-reader** from the list.
5. **Update** the marketplace later to pull your commits.

The repo includes `.claude-plugin/marketplace.json` so Cowork discovers the plugin at the repo root.

---

## Option C — Organization marketplace (Team / Enterprise)

For your whole org (Academy, university, etc.):

1. **Organization settings → Plugins** (admin).
2. Create a marketplace and either:
   - **Upload** the plugin zip, or
   - **Connect a private GitHub repo** and sync.
3. Set visibility: **Available**, **Installed by default**, or **Required**.

Cowork and **Skills** must be enabled for the org. See [Manage plugins for your organization](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization).

Hand the packaged folder to whoever owns org plugins if you are not an admin.

---

## After install — how colleagues use it

1. Put the **`.docx`** in the Cowork workspace (upload).
2. Start a session with the **maagarim-reader** plugin enabled.
3. Prompt example:

   > Check all Mishnah and Talmud quotes in `my-article.docx` against Maagarim. Use the first witness when no manuscript is named. Add Hebrew comments and Word tracked changes where wording differs. Open Maagarim in Chrome for live lookups.

4. Open the result in **Word → Review → All Markup**.

Optional: `pip install -r requirements.txt` then:

```bash
python3 scripts/annotate_first_witness_docx.py --input my-article.docx
```

(Ketubot reference quote map only — see `examples/evals.md`.)

---

## Validate before sharing

If you have Claude Code CLI:

```bash
claude plugin validate
```

(run from this directory)

---

## Cursor vs Cowork

| | Cursor | Cowork |
|---|--------|--------|
| Install | `.cursor/skills/maagarim-reader/` | Plugin upload or GitHub marketplace |
| Invoke | `@maagarim-reader` | Enable plugin + describe task in Cowork |
| Maagarim | Browser / Playwright in agent | **Claude in Chrome** (recommended) |

The same `skills/maagarim-reader/SKILL.md` drives both; Cowork adds browser-first instructions at the top.
