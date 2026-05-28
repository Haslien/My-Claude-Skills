---
name: index-all-md-files
description: Build a single dated index of every `.md` file in a repository, then iteratively read each file and fill in a short description for it. Use when the user wants a documentation timeline across a whole project, asks to "index all md files", "indekser alle md-filer", "lag oversikt over dokumentasjon", "map docs over time", or wants a one-page roster of every markdown file sorted by recency. The bundled Python script generates the skeleton with `TBD` placeholders; Claude then walks the table top-down, reading one file at a time and replacing its `TBD`, so context stays focused on a single document at a turn.
---

# Index All MD Files

Produces `MD_INDEX.md` at the root of a target directory: one row per `.md` file in the tree, with creation date, last-modified date, link, and a one-line description. Rows are sorted newest-modified first so the table doubles as a documentation timeline.

The skill has two phases:

1. **Script phase** — `index_md.py` walks the tree, collects dates from git (with a filesystem fallback), and writes a skeleton table where every description is `TBD`.
2. **Iterative phase** — Claude walks the table top-down: read one file, replace that row's `TBD` with a one-line description, save, then move to the next `TBD`. Never batch.

The iterative pattern exists for a reason: reading every file before writing anything blows out the context window and the later descriptions degrade. One file in, one description out.

```
index-all-md-files/
├── SKILL.md       (this file)
└── index_md.py    (the scanner)
```

## When to use

Trigger on intents like:

- "index all md files in this repo"
- "indekser alle .md filer"
- "lag oversikt over all dokumentasjon"
- "map our docs over time"
- "give me a timeline of every markdown file"

Do **not** use this skill for:

- Per-folder summaries → `index-content`
- Repo-wide AI navigation maps → `context-architect`
- Compiling project files into one LLM dump → `project-context-compiler`

## Workflow

### Step 1 — confirm target directory

If the user gave a path, use it. Otherwise default to the current working directory (which in a Claude Code session is normally the repo root).

If the path is not inside a git repository the script still works — it falls back to filesystem timestamps — but mention this to the user, since "created" then means "file birth time on disk" rather than "first commit".

### Step 2 — run the scanner

From the repo root:

```bash
python3 .claude/skills/index-all-md-files/index_md.py <target_dir>
```

(Use `python` if your system aliases that to Python 3 — on stock macOS the binary is `python3`.)

Common flags:

| Flag | Effect |
|------|--------|
| (no flag) | Writes `MD_INDEX.md` at the root of `<target_dir>` |
| `--name DOCS.md` | Changes the output filename |
| `--output /abs/path.md` | Writes to an explicit absolute or relative path |

The scanner skips obvious noise (`.git/`, `node_modules/`, `__pycache__/`, `dist/`, `build/`, `out/`, `target/`, `vendor/`, `.venv/`, `.next/`, `.nuxt/`, `coverage/`, `.turbo/`, `.cache/`, `.idea/`, `.gradle/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`). Dotfolders that are *not* in that list (e.g. `.github/`, `.claude/`) are kept on purpose — they usually contain real docs.

If `MD_INDEX.md` already exists, the scanner reuses any description whose row's modified date is unchanged. Files that were touched since the last scan are reset to `TBD` so Claude re-summarises them on the next pass.

### Step 3 — iterate file by file

Open the generated `MD_INDEX.md`. Then loop:

1. Find the **first row** whose description is `TBD`.
2. Read that file with the `Read` tool.
3. Write a **one-line description** (12–25 words) that says, specifically, what the document is — topic, role, what a reader would get out of it. Skip filler like "This document describes…".
4. Use `Edit` on `MD_INDEX.md` to replace that single row's `TBD` with the new description. Match the row uniquely on its `[path](path)` cell so you do not accidentally touch other rows.
5. Repeat until no `TBD` remains.

Do **not** read more than one file before writing back. Do **not** batch edits at the end. The whole point is to keep the working context focused on one document at a time.

If a file is empty, a stub, or only an auto-generated header, write that plainly (e.g. `Empty placeholder.` or `Auto-generated table of contents — no prose.`) and move on.

### Step 4 — report

When all `TBD`s are resolved, tell the user:

- Path to the generated index
- Total number of `.md` files indexed
- Date range (oldest created → newest modified)
- Anything that looked off — duplicate topics, suspiciously stale files, empty placeholders

## Description style

The description column is the only thing a future reader (human or agent) will look at to decide whether to open the file. Make it earn its row.

Good:

- `Drizzle ORM schema for the auth service — users, sessions, refresh tokens, with soft-delete on users.`
- `Post-mortem for the 2026-03 ingest outage: root cause, timeline, three follow-up actions.`
- `Trigger prompts and workflow for the cybersecurity audit skill (secrets, auth, GDPR, CVE scan).`

Avoid:

- `Documentation for the project.` (says nothing)
- `This document contains information about X.` (passive padding)
- `A markdown file describing Y.` (we know it's markdown — the table says so)

One sentence. No trailing period if the row already reads naturally without one. Pipes (`|`) in the description must be escaped as `\|` so the table does not break.

## Examples

**"indekser alle md-filer i dette repoet"**
→ Run `python .claude/skills/index-all-md-files/index_md.py .`
→ Open the new `MD_INDEX.md`, walk every `TBD` row top-down, fill each in turn.

**"lag en docs-tidslinje for /Users/me/work/api-service"**
→ `python .claude/skills/index-all-md-files/index_md.py /Users/me/work/api-service`
→ Iterate the resulting `MD_INDEX.md`.

**"re-index — vi har skrevet en del nytt"** (index already exists)
→ Re-run the script. Existing descriptions for unchanged files are kept; only files touched since the last scan come back as `TBD`. Fill those in.

## Notes

- Created/modified dates come from `git log --follow` when the target is inside a git repo; otherwise from `stat` (birth time + mtime).
- The script is pure standard library — no `pip install` needed.
- The output file is documentation in its own right; it is **not** added to `.gitignore`. Commit it like any other doc.
