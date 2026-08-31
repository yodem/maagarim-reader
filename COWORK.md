# Sharing Maagarim Reader in Claude Cowork

This folder is a **Cowork plugin** — a packaged skill plus scripts. Cowork does not use Cursor’s `.cursor/skills/` path.

## What colleagues install

One plugin named **maagarim-reader** with **three skills**:

| Skill | Task |
|-------|------|
| **maagarim-reader** | Mishnah / Talmud quotes vs [Maagarim](https://maagarim.hebrew-academy.org.il) |
| **tanakh-nikud** | Tanakh nikud (bli te'amim) via Sefaria |
| **feedback** | Report a problem or unclear result (דיווח) |

- Scripts: `python-docx` annotators under `scripts/`
- Maagarim: **Claude in Chrome** (no Maagarim connector)

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
git add .claude-plugin skills scripts references examples SKILL.md COWORK.md README.md
git commit -m "Maagarim Reader Cowork plugin"
git remote add origin https://github.com/yodem/maagarim-reader.git
git push -u origin main
```

`.claude-plugin/marketplace.json` must list the plugin with a **GitHub object** source
(not `"."`), e.g. `{"source":"github","repo":"yodem/maagarim-reader"}`. String/`./`
sources work in the Claude Code CLI but make Cowork report **Marketplace sync failed**.

2. Colleague: **Customize → Plugins → Add marketplace**.
3. Enter `yodem/maagarim-reader` (owner/repo).
4. Install **maagarim-reader** from the list.
5. **Update** / re-sync later to pull new commits.

If sync still fails, use **Option A (zip)** — that bypasses the marketplace service.

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
2. Start a session with the plugin enabled and pick the skill:

   **Maagarim:**
   > Check all Mishnah and Talmud quotes in `my-article.docx` against Maagarim…

   **Tanakh nikud:**
   > Add nikud without te'amim to all Bible quotes in `my-article.docx` using Sefaria.

   **Feedback:**
   > השתמשי ב-feedback — הבדיקה על הקובץ שלי לא הסתיימה כמו שציפיתי.

3. Open the result in **Word → Review → All Markup**.

Optional Maagarim reference script:

```bash
python3 scripts/annotate_first_witness_docx.py --input my-article.docx
```

(Ketubot reference quote map only — see `examples/evals.md`.)

Optional Tanakh nikud:

```bash
python3 scripts/nikud_tanakh_docx.py --input my-article.docx
```

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
| Invoke | `@maagarim-reader`, `@tanakh-nikud`, or `@feedback` | Enable plugin + pick skill |
| Maagarim | Browser / Playwright in agent | **Claude in Chrome** (recommended) |

The `skills/` folder holds all three skill files; Cowork discovers every `skills/*/SKILL.md`.
