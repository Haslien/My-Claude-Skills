---
name: project-context-compiler
description: Compile every relevant file in a project into one .txt file for pasting into an LLM. Use when the user wants to share full project context, says "kompiler kontekst for [sti]", "lag prosjektfil for X", "compile context for Y", "make a context file", "kompiler [navn]", or asks to generate/run a Project Context Compiler config. Also handles per-stack ignore rules (TypeScript, JavaScript, Python, Go, Rust, Java, Ruby, PHP) and optional layer scoping (api, frontend, backend, db).
---

# Project Context Compiler

A self-contained replacement for the standalone Project Context Compiler tool. Generates JSON configs and runs the bundled `compile.py` to produce one big `.txt` file per project — ready to paste into an LLM.

Everything lives inside this skill folder:

```
project-context-compiler/
├── SKILL.md          (this file)
├── compile.py        (the compiler)
├── projects/         (JSON configs — committed)
│   └── example.json
└── output/           (generated .txt — gitignored)
```

## When to use this skill

Trigger on any of these intents:

- **Create a config** — "lag prosjektfil for [sti]", "create context config for X", "make a project file for Y"
- **Run the compiler** — "kompiler [navn]", "compile [name].json", "run the compiler for X"
- **Both at once** — "kompiler kontekst for [sti]", "compile context for [path]" → create config, then run

## Workflow

### Step 0 — confirm output is gitignored

Before doing anything else, verify the repo root has a `.gitignore` containing the line:

```
.claude/skills/project-context-compiler/output/
```

If it does not, add it. The `output/` folder must never be committed — it can contain large source dumps.

### Step 1 — figure out what the user wants

| User intent | What to do |
|---|---|
| Provided an absolute path, no existing config | Go to step 2 (create config), then step 5 (run) |
| Named an existing config in `projects/` | Skip to step 5 (run) |
| Asked to edit/extend a config | Read the existing JSON, modify, then step 5 |

Resolve `target_dir` (absolute path) and an optional `scope` (e.g. `api`, `frontend`, `backend`, `web`, `client`, `server`, `db`, `shared`, `core`). Ask only if the path is ambiguous.

### Step 2 — explore the target directory

Use Glob/Bash to list the top of `target_dir` and detect the stack:

| Marker | Stack |
|---|---|
| `package.json` + `tsconfig.json` | TypeScript / Node |
| `package.json` (no tsconfig) | JavaScript / Node |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml` / `build.gradle` | Java / Kotlin |
| `composer.json` | PHP |
| `Gemfile` | Ruby |

Note whether `.gitignore` exists at the target root — `compile.py` will read it automatically when `use_gitignore: true`.

### Step 3 — build the ignore list

Always include:

```
.git/
.DS_Store
*.log
.env
.env.*
```

Then append stack-specific patterns:

- **TypeScript / JavaScript:** `node_modules/`, `dist/`, `build/`, `.next/`, `.nuxt/`, `out/`, `coverage/`, `.turbo/`, `.cache/`, `*.tsbuildinfo`
- **Python:** `__pycache__/`, `*.pyc`, `*.pyo`, `.venv/`, `venv/`, `env/`, `dist/`, `build/`, `*.egg-info/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`
- **Go:** `vendor/`
- **Rust:** `target/`
- **Java / Kotlin:** `target/`, `build/`, `.gradle/`, `out/`
- **Ruby:** `vendor/`, `.bundle/`
- **PHP:** `vendor/`

### Step 4 — pick the files

**Always include (when present at root):** `README.md`, the dependency manifest (`package.json`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.), root config (`tsconfig.json`, `vite.config.*`, `next.config.*`, `eslint.config.*`, `tailwind.config.*`, `docker-compose.yml`, `Dockerfile`), and `.env.example` if it exists. Use Glob to confirm before adding.

**No scope:** add recursive globs for the source dirs that exist (`src/**`, `app/**`, `lib/**`, `packages/**`).

**Scope provided:** only include the matching layer plus root files.

| Scope | Look for |
|---|---|
| api, backend, server | `api/`, `backend/`, `server/`, `app/api/`, `src/api/`, `src/server/` |
| frontend, web, client, ui | `frontend/`, `web/`, `client/`, `ui/`, `app/`, `src/app/`, `src/pages/`, `src/components/`, `src/views/` |
| shared, common, lib, utils | `shared/`, `common/`, `lib/`, `utils/`, `src/lib/`, `src/utils/` |
| db, database, models | `db/`, `database/`, `models/`, `src/models/`, `src/db/` |
| core, domain | `core/`, `domain/`, `src/core/`, `src/domain/` |

Add matched directories as glob patterns (`api/**`, `src/api/**`). The compiler expands these and applies ignore rules.

### Step 5 — write the JSON config

Save to `.claude/skills/project-context-compiler/projects/<name>.json`:

```json
{
  "title": "<ProjectName>",
  "absolute_path": "<target_dir with forward slashes, no trailing slash>",
  "start_prompt": "Please get acquainted with this project's structure and source files. I will send you multiple files in sequence — review and understand their contents. Once you have absorbed the overall context, wait for my instructions before performing any specific tasks.\n\n",
  "start_text": "-- Begin file \"{file}\" --\n",
  "stop_text": "-- End file \"{file}\" --\n",
  "use_gitignore": true,
  "ignore": [],
  "files": []
}
```

Naming:
- Full project: `<project-folder-lowercase-hyphenated>.json`
- Scoped: `<project-folder>-<scope>.json` (e.g. `myapp-frontend.json`)

Title: title-case the folder name; append ` – API`, ` – Frontend`, etc. for scoped configs.

Files ordering: root files first (alphabetical), then source globs (alphabetical). All paths use forward slashes, relative to `absolute_path`.

### Step 6 — run the compiler

From the repo root:

```bash
python .claude/skills/project-context-compiler/compile.py <name>.json
```

The script reads `projects/<name>.json` and writes `output/<name>.txt`. Optional dependencies (`pathspec` for richer .gitignore matching, `Pillow` for image dimensions) improve output but are not required.

### Step 7 — confirm to the user

Tell them:

- Config saved to `.claude/skills/project-context-compiler/projects/<name>.json`
- Output written to `.claude/skills/project-context-compiler/output/<name>.txt`
- Approximate file count and total size of the output
- That `output/` is gitignored — paste from the file directly into the LLM

## Examples

**"lag prosjektfil for C:/Users/mathi/code/ai-pipeline-v2"**
→ Detected Python project
→ Saves `projects/ai-pipeline-v2.json` with Python ignores and `src/**` (or top-level `*.py`)
→ Runs `python .claude/skills/project-context-compiler/compile.py ai-pipeline-v2.json`

**"kompiler kontekst for /home/user/myapp, bare frontend"**
→ Saves `projects/myapp-frontend.json` with frontend dirs only
→ Runs the compiler

**"kompiler myapp-api"** (config already exists)
→ Skips creation, runs `compile.py myapp-api.json`

## Notes

- The compiler is bundled as `compile.py` inside this skill folder, so the user does not need the standalone `Project-context-compiler` repo cloned anywhere.
- If `pathspec` is missing, the compiler falls back to a simpler `fnmatch`-based matcher — install with `pip install pathspec` for full .gitignore semantics.
- Binary files are written as a one-line metadata stub (`*** image 1920x1080px, 1.2 MB ***`) instead of raw bytes.
