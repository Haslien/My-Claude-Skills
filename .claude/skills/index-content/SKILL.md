---
name: index-content
description: Index and summarize a directory into an index.md file. Works for both document folders and code directories. Use when the user wants to create an overview of files, says "indekser", "indeksere", "index this folder", "lag en oversikt", or wants a summary index of a folder.
---

# Content Indexer

Create and maintain an `index.md` that summarizes all files in a directory. Works for two modes:

- **Document mode** — markdown, PDFs, notes, specs, plans. Sorted by date. Shows staleness.
- **Code mode** — source files, modules, components. Shows exports, key functions, and what each module does.

The mode is inferred automatically, or the user can specify it.

---

## Step 1: Determine target directory and mode

If the user did not specify a directory, ask.

**Detect mode** by scanning the file extensions in the target directory:

- Majority `.md`, `.pdf`, `.docx`, `.txt`, `.pptx` → **Document mode**
- Majority `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.swift`, etc. → **Code mode**
- Mixed → ask the user which mode they want, or offer both

---

## Step 2: Check for existing index

- **If `index.md` exists** → enter **Re-index mode** (Step 8)
- **If not** → continue to Step 3

---

## Step 3: Discover all files

Use `Glob` to find all files in the target directory (recursive). Exclude:

- `index.md` itself
- `.DS_Store`, `.gitkeep`, hidden files (starting with `.`)
- `node_modules/`, `__pycache__/`, `.git/`
- Build artifacts: `dist/`, `build/`, `.next/`, `*.pyc`

**Every file in every subdirectory gets its own entry.** Do NOT collapse a subdirectory into a single line. Group files under their folder heading:

```
## Root files

## components/

## utils/
```

---

## Step 4: Get file dates (document mode only)

Use `stat` to get created and modified dates for each file:

```bash
stat -f "%Sm %SB" -t "%Y-%m-%d %H:%M" "filepath"
```

In document mode, sort by **last modified date, newest first** within each group.

In code mode, sort **alphabetically** (dates are less important for code).

---

## Step 5: Write skeleton index.md

Write this immediately so the user sees progress.

### Document mode skeleton

```markdown
# Index: [directory name]

> Auto-generated content index. Last indexed: [YYYY-MM-DD]
> Root path: `[absolute path]`

## Key Facts

| | |
|---|---|
| **Total files** | [N] |
| **Oldest file** | [YYYY-MM-DD] ([filename]) |
| **Newest file** | [YYYY-MM-DD] ([filename]) |
| **Date span** | [X days/weeks/months] |
| **Last indexed** | [YYYY-MM-DD] |

> **Note on relevance:** In active planning and documentation work, files can be superseded within hours — not weeks. When multiple files appear to cover the same topic, the newest one is *likely* the most current truth, but this is not certain. Always check the "Modified" date relative to related files. The **Status** field in each description indicates the AI's best assessment: `Current`, `Superseded`, `Draft`, or `Historical` — but treat these as suggestions, not facts. When in doubt, ask the user.

## Overview

_Being generated..._

## Table of Contents

| # | File | Description | Modified | Created |
|---|------|-------------|----------|---------|
| 1 | [filename](relative-path) | _To be indexed..._ | YYYY-MM-DD | YYYY-MM-DD |
```

### Code mode skeleton

```markdown
# Index: [directory name]

> Auto-generated code index. Last indexed: [YYYY-MM-DD]
> Root path: `[absolute path]`

## Key Facts

| | |
|---|---|
| **Total files** | [N] |
| **Languages** | [e.g. TypeScript, Python] |
| **Last indexed** | [YYYY-MM-DD] |

## Overview

_Being generated..._

## Table of Contents

| # | File | Purpose | Exports / Key symbols |
|---|------|---------|-----------------------|
| 1 | [filename](relative-path) | _To be indexed..._ | — |
```

---

## Step 6: Iteratively index each file

For each file:

1. **Read** the file
2. **Write a summary** (see format below per mode)
3. **Update `index.md`** after each file — write to disk immediately, do not batch

### Document mode — per file

- One-line "what is this" description in the table
- Detailed section below the table:

```markdown
---

### N. [filename](relative-path)
**Modified**: YYYY-MM-DD | **Created**: YYYY-MM-DD

[2–5 sentences: purpose, key decisions, conclusions]

**Key points:**
- ...

**Related to:** [other files if applicable]
**Status:** current / superseded by X / draft / historical
```

### Code mode — per file

- One-line purpose in the table
- Exports / key symbols column: list exported functions, classes, types, constants (max 5–7, truncate with "…" if more)
- Detailed section below the table:

```markdown
---

### N. [filename](relative-path)

[1–3 sentences: what this module does, its role in the codebase]

**Exports:** `functionA`, `ClassB`, `TYPE_C`
**Dependencies:** imports from `../utils`, `react`, etc.
**Notes:** [anything notable — side effects, global state, gotchas]
```

Keep code descriptions technical and precise. Focus on what the module *does*, not how it works internally.

---

## Step 7: Finalize overview and key facts

After all files are indexed:

1. Update the **Key Facts** table with accurate values
2. Write the **Overview section** — 2–3 sentences on what the directory contains, general theme, and which files are most important

For document mode: if multiple files appear to cover the same topic, flag this explicitly in the Overview and in each affected file's **Related to** field. Note which file is newest, but do not assert it is correct — suggest the user verify.

---

## Step 8: Re-index mode

When `index.md` already exists:

1. Read the existing `index.md`
2. Discover current files (Step 3)
3. Compare:
   - **New files** → add
   - **Removed files** → remove
   - **Changed files** (modified date newer than "Last indexed") → re-summarize
   - **Unchanged files** → keep existing description
4. Update "Last indexed" timestamp
5. Re-sort (document mode: by modified date; code mode: alphabetically)
6. Update Key Facts and Overview

Only re-read files that are new or changed.

---

## File type handling

| Type | Handling |
|------|----------|
| `.md` | Read directly, summarize |
| `.pdf` | Use Read tool (supports PDF), summarize |
| `.txt`, `.csv`, `.json`, `.yaml` | Read and summarize |
| `.docx` | Use docx skill if available, else note as "Binary — manual review needed" |
| `.pptx` | Use pptx skill if available, else note as "Presentation — manual review needed" |
| `.png`, `.jpg`, `.svg` | Note as image, describe by filename context |
| Source code (`.ts`, `.py`, etc.) | Read and summarize exports and purpose |
| Binary/unknown | Note file exists, type, size — don't attempt to read |

---

## Output goal

The final `index.md` serves two audiences:

**Humans** — Someone unfamiliar with the directory should be able to read the index and understand what each file does, which ones are most relevant, and — in document mode — which ones may be outdated.

**AI agents** — This is equally important. An AI agent searching for information will typically list a directory, see `index.md`, read it, and use it to decide which files to open — without reading the entire codebase or document collection. The index must therefore be optimized for this use case:

- Descriptions must be specific enough that an agent can judge relevance from the index alone
- File paths must be accurate and relative so an agent can open them directly
- In document mode, topics and keywords should be explicit in descriptions — not vague summaries
- In code mode, exported symbols and module purpose must be clear so an agent knows what to import or read

Think of `index.md` as a routing layer: it should allow an AI agent to confidently say "I need files A and C, I can skip B and D" — without opening any of them first.
