---
name: context-architect
description: Maintain `CONTEXT.md` navigation maps at every meaningful folder — each listing 3–5 routes out — so any AI agent reaches a specific file in 2–3 clicks. Auto-fire whenever the structure changes: new file, new folder, move, restructure, new domain. Trigger phrases include "lag CONTEXT.md", "oppdater kart", "update the map", "architect the context", "lag agent-workspace". When unsure, fire — a stale map misleads worse than no map.
---

# Context Architect

The filesystem is the agent's map. This skill keeps that map drawn — and **redraws it on every structural change**, not just when asked.

## The map metaphor

Think of the project as a directory tree the agent clicks through:

```
You are here: project root
        │
        ▼
   ┌────────┐  Read CLAUDE.md (Layer 0): "this is what the project is"
   │  root  │  Read CONTEXT.md (Layer 1): "here are 3–5 routes out"
   └────────┘
        │
   ─────┼──────────────────
   │    │     │     │
   ▼    ▼     ▼     ▼
  web  api   db   docs        ← pick one route
   │
   ▼
 Read web/CONTEXT.md (Layer 2): "here are 3–5 routes out of web/"
   │
   ─────┼──────────────────
   │    │     │
   ▼    ▼     ▼
 routes/ components/ hooks/   ← pick again
   │
   ▼
 Read web/routes/CONTEXT.md: "here are the actual files"
   │
   ▼
 [the file the agent actually needed]
```

**The whole point:** the agent never has to scan the project. At every level it reads one short map, picks one of 3–5 routes, and descends. Three or four hops and it is at the file it needs — having read maybe 1500 tokens total, not the whole codebase.

This only works if the maps are **complete** and **fresh**. A missing route is a dead end. A stale route sends the agent to the wrong place. That is why this skill fires on every change, not on demand.

## Why this matters (read once, internalize)

- Bounded context is the binding resource for any LLM agent. The cheapest token is the one you never load.
- LLMs perform measurably worse when relevant info is buried in long contexts ("lost in the middle"). Pre-routing with maps prevents the bury.
- Fresh maps mean the next agent session — yours, your colleague's, a CI bot's — starts oriented instead of disoriented.
- Stale maps are worse than no maps. They mislead with confidence.

The two papers in [papers/](papers/) make the full case (MWP for the architectural pattern, Dive into Claude Code for the empirical pressure). Read [papers/index.md](papers/index.md) once if you need the deep reasoning. After that, the only thing that matters is keeping the maps current.

---

## Five layers (the spine)

```
Layer 0  CLAUDE.md            "Where am I?"        identity, project-wide rules
Layer 1  CONTEXT.md (root)    "Where do I go?"     top-level routes
Layer 2  CONTEXT.md (folder)  "What's in here?"    folder-level routes + files
Layer 3  references/*.md      "What rules apply?"  stable conventions, schemas, voice
Layer 4  output/* or actual   "What's the work?"   per-run artifacts or the source code
         source files
```

Layers 0–2 are the **map**. Layers 3–4 are the **content the map points at**.

The single most common architectural mistake is letting Layer 3 (stable rules) and Layer 4 (per-run or active code) mix in the same folder without separation. A subfolder full of voice guides, design conventions, and yesterday's draft script is a dead zone — the agent cannot tell rule from input. Keep them apart. When in doubt, ask: *does this file change every run?* Yes → Layer 4. No → Layer 3.

---

## When this skill fires (auto-trigger conditions)

Fire on **any** of the following. No need to wait for the user to ask.

| Trigger | Action |
|---|---|
| New file created | Update parent folder's `CONTEXT.md` to list it |
| New folder created | Create a `CONTEXT.md` inside it AND add a route from the parent |
| File moved or renamed | Update both the old and the new parent's `CONTEXT.md` |
| File deleted | Remove its entry from the parent `CONTEXT.md` |
| Significant code change (new module, new feature, new domain) | Re-read the affected `CONTEXT.md` and refresh the description if it lies now |
| Restructure (folder split, merge, hierarchy change) | Redraw the affected branch of the tree, top-down |
| Project bootstrapped (no maps yet) | Run the full bootstrap workflow once |
| User asks for the map, navigation, structure, or architecture | Treat as explicit trigger |

**Do not** fire for: trivial whitespace edits, comment tweaks, or content edits inside a file that don't change its role. The map describes *roles and routes*, not contents.

When in doubt — fire. A 30-second map refresh is cheaper than next session's wasted exploration.

---

## The CONTEXT.md template (this is the whole format)

Every CONTEXT.md follows the same shape, regardless of layer. Keep it short. A CONTEXT.md over 80 lines is a sign the folder should split, not that the map should expand.

```markdown
# CONTEXT.md — {folder name}

## What this folder is

{One sentence. What problem does this folder solve? What is its role in the
larger system? Not a summary of every file — a problem statement.}

## Routes from here

→ For **{topic A}**, see [`subfolder-a/`](subfolder-a/CONTEXT.md)
→ For **{topic B}**, see [`subfolder-b/`](subfolder-b/CONTEXT.md)
→ For **{topic C}**, see [`subfolder-c/`](subfolder-c/CONTEXT.md)

(3–5 routes max. If you need more, the folder is doing too many jobs and
should split.)

## Files in this folder

| File | Role |
|---|---|
| `foo.ts` | {one line — what role this file plays} |
| `bar.ts` | {one line} |
| `baz.ts` | {one line} |

## When working here, also load

- `../references/conventions.md` — naming, file layout
- `../CLAUDE.md` — global commands, run/test/build
- {any other file the agent will reliably need to do work in this folder}
```

The four sections in order: **purpose → outbound routes → local files → cross-cutting deps.** That ordering matches how an arriving agent reads: orient, decide where to go next, see what is here, know what else to load.

### A folder that is a leaf (no subfolders)

Drop the `## Routes from here` section. The `## Files in this folder` table becomes the routing table — each file is a destination.

### A folder that is a stage in a pipeline (sequential workflow)

Replace `## Files in this folder` with the MWP stage contract:

```markdown
## Inputs

- (working) `../01_research/output/research.md`
- (reference) `../_config/voice.md`
- (reference) `references/structure.md`

## Process

{Specific instructions. Cite reference files. State concrete limits.}

## Outputs

- `script.md` → `output/`
```

This is for sequential pipelines (research → script → production, ingest → transform → publish). For codebases, use the file-table version above.

---

## Workflow A — Bootstrap (first time, no maps yet)

Use when the project has no `CONTEXT.md` files at all.

1. **Confirm scope.** Read `CLAUDE.md` if it exists. If it doesn't, ask the user whether to bootstrap one first. Layer 0 is the foundation; the maps assume it exists.
2. **Walk the tree.** List top-level folders. Read enough of each to write a one-sentence "what this folder is for" statement. Identify the 3–5 major domains (frontend / backend / infrastructure / docs / etc.) — or, for a workflow project, the 3–5 sequential stages.
3. **Draw the root map.** Write the root `CONTEXT.md` with one route per domain or stage.
4. **Descend one level.** For each domain or stage, repeat: identify its 3–5 sub-parts, write the folder's `CONTEXT.md`.
5. **Stop at the right depth.** Most projects need 2 levels deep, occasionally 3. Beyond 3 you are documenting trivia. The leaf folders' CONTEXT.md becomes a file table — that's the bottom of the map.
6. **Set up `references/` and `output/` (or equivalents) where they earn their place.** Don't manufacture them. Add them when there is actual stable reference material to put in `references/` or actual per-run artifacts to put in `output/`.
7. **Walk the map as a test.** Pick a realistic task. Starting from `CLAUDE.md`, can you reach the right file in 2–3 hops? If not, the map is incomplete or misleading — fix it before declaring done.
8. **Tell the user what changed.** List every file created, what layer it belongs to, and one sentence on why.

## Workflow B — Maintenance (every structural change after bootstrap)

This is the **common case** and the reason this skill fires often. Most invocations are not bootstrapping a new map — they are keeping an existing one fresh.

When a structural change happens:

1. **Identify the affected folders.** Which folders did the change touch? (The folder containing the new/moved/deleted file, and any folder whose role description might be falsified by the change.)
2. **Update the most local map first.** Open the parent folder's `CONTEXT.md`. Add, remove, or update the relevant entry in `## Files in this folder` or `## Routes from here`.
3. **Bubble up only as far as needed.** If the change introduced a new sub-domain or shifted what the folder is *for*, update the parent's `## What this folder is` and any route descriptions one level up that mention this folder. Don't bubble all the way to the root unless the change really did shift the project's top-level shape.
4. **Check for collateral lies.** Skim the affected `CONTEXT.md` for sentences that are no longer true. Fix them.
5. **Verify the path still works.** Walk from the project root down to the changed file using only the maps. Three hops or fewer. If the path is broken, fix the map.
6. **Stop.** Do not redraw maps that the change did not touch. Maintenance is local.

A maintenance pass on a small change should take under a minute. If it takes longer, either the change was bigger than it looked (good — you caught it), or the existing map was already broken (also good — fix it now).

## Workflow C — Refresh (the map drifted, fix it)

When a CONTEXT.md is clearly out of date — names of files that don't exist, routes pointing to deleted folders, descriptions that no longer match — refresh it:

1. List actual current files and subfolders via the filesystem.
2. Compare against the CONTEXT.md.
3. Reconcile: add new entries, remove dead ones, rewrite descriptions that lie.
4. Bubble up only if the folder's *role* changed, not just its contents.

Refresh is bigger than maintenance, smaller than bootstrap. Trigger it when a CONTEXT.md is clearly behind reality.

---

## Anti-patterns

These are concrete failure modes. Each one breaks the map.

| Anti-pattern | Why it breaks the map | Fix |
|---|---|---|
| `CONTEXT.md` lists every file with a paragraph each | Now it's a documentation file, not a navigation map; the agent reads more than it would have without it | Compress to one line per file, role-focused |
| `CONTEXT.md` over 80 lines | The folder has too many jobs; the map can't fit | Split the folder, split the map |
| Dead routes (point to folders or files that don't exist) | Worse than no map — actively misleads | Refresh the map; this is exactly what Workflow C is for |
| One `CONTEXT.md` per source file | Wrong granularity; map levels should match folder levels | Collapse to one CONTEXT.md per folder |
| `CONTEXT.md` duplicates `CLAUDE.md` | Wastes tokens; Layer 1 should *route to* Layer 0, not restate it | Reference Layer 0 by name, don't copy |
| Reference and per-run files mixed in the same folder | Agent can't tell stable rule from current input | Split into `references/` (Layer 3) and `output/` (Layer 4) |
| Routes vague ("see helpers/ for utilities") | Forces the agent to dig blindly anyway | Make each route specific: "for date parsing, see helpers/dates.ts" |
| New file added without updating the parent CONTEXT.md | The map drifts; next agent session is lying to itself | This skill exists to prevent exactly this — fire on every file creation |

---

## Edit-source, not edit-output

If the same kind of mistake keeps showing up in the agent's work — wrong file location, wrong convention, wrong style — that is a signal that the map or a Layer 3 reference file is underspecified. Don't keep correcting the output. Trace it back to the source map and fix it there. One source edit prevents many output edits.

---

## Quality check (run mentally before declaring done)

- [ ] Every meaningful folder has a `CONTEXT.md`
- [ ] Every `CONTEXT.md` has the four sections: what / routes / files / cross-cutting
- [ ] No `CONTEXT.md` is over 80 lines
- [ ] No folder offers more than 3–5 routes (if it does, the folder should split)
- [ ] An agent starting at `CLAUDE.md` can reach any specific file in ≤ 3 hops
- [ ] Reading the maps top-down, every sentence is currently true
- [ ] Reference and per-run material are in different folders
- [ ] The user gets a list of changed files at the end of the run

---

## Key insight

> "The folder structure tells the agent what to do at each step, and if the agent delegates sub-tasks, the same folder structure determines what context those sub-agents receive."
>
> — *Interpretable Context Methodology*, page 1

The map is not a deliverable. It is a living layer of the project that has to stay synchronized with the code. Keep it fresh on every change and the agent — every agent, every session — starts oriented. Let it drift and the project gets harder to work in until someone redraws it.

Fire often. Keep the map current. That is the whole job.
