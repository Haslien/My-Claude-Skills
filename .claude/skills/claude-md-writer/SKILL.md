---
name: claude-md-writer
description: Use when the user wants to create or improve a CLAUDE.md file for a project. Guides through WHY/WHAT/HOW analysis, keeps instructions lean and universally applicable, and structures progressive disclosure with agent_docs/. Trigger on phrases like "lag CLAUDE.md", "hjelp med CLAUDE.md", "write a CLAUDE.md", "create CLAUDE.md", "improve my CLAUDE.md".
---

# CLAUDE.md Writer Skill

## Overview

Creates high-leverage `CLAUDE.md` files that effectively onboard Claude into a codebase. Every line in `CLAUDE.md` cascades through research, planning, and implementation — so quality beats quantity.

**Core principle:** CLAUDE.md is not documentation. It is a stateless session bootstrap. Claude forgets everything between sessions and only knows what tokens you provide. This file is the primary delivery mechanism for persistent context.

**Key constraint:** Claude Code's system prompt already uses ~50 instructions. Frontier LLMs reliably follow 150–200 total. You have ~100–150 left — use them wisely.

## When to Use

- User wants to create a `CLAUDE.md` from scratch
- User wants to audit/improve an existing `CLAUDE.md`
- User says "what should be in my CLAUDE.md"
- User's project has no persistent Claude context

**DO NOT use for:**
- General project documentation
- README files
- Files that aren't `CLAUDE.md`

## Quick Start

**Required from user:**
1. Project root (or ask Claude to explore it)
2. A brief description of what the project does

**Workflow:**
1. Explore codebase to understand WHY / WHAT / HOW
2. Audit existing `CLAUDE.md` (if any)
3. Draft lean, universal instructions
4. Identify what belongs in `agent_docs/` instead
5. Write `CLAUDE.md` + optional `agent_docs/` files
6. User review checkpoint

---

## Implementation

### Phase 0: Codebase Exploration

Before writing anything, understand the project:

**Run in parallel:**
- Glob `**/*.md` — find existing docs
- Read `package.json` / `pyproject.toml` / `Cargo.toml` — identify stack
- Read existing `CLAUDE.md` if present — find what to keep or cut
- Check `docker-compose.yml`, `Makefile`, `.github/` — find workflows

**Extract:**
- Tech stack (languages, frameworks, tools)
- Project purpose (what it does, who uses it)
- Dev workflows (how to build, test, run)
- Monorepo structure (if applicable — critical for navigation)

**Checkpoint:**
```
"Here is what I found:

STACK: {tech}
PURPOSE: {purpose}
WORKFLOWS: {build/test/run commands}
STRUCTURE: {monorepo map or single-project}

Does this look right? Anything you want to add?"
```

Wait for user confirmation.

---

### Phase 1: WHY / WHAT / HOW Analysis

Structure all content around three pillars:

**WHY** — Project purpose and component roles
- Why does this project exist?
- What problem does each major component solve?
- What decisions were made deliberately?

**WHAT** — Tech stack and codebase map
- Languages, frameworks, key libraries
- Directory structure (especially for monorepos)
- Where to find things: config, tests, components, API routes

**HOW** — Development workflows
- Build command
- Test command (and how to run a single test)
- Dev server / local run command
- Deploy command
- Linting / formatting (automated — not Claude's job)

**Instruction budget audit:**
For each instruction candidate, ask:
- Does this apply to EVERY session? → Include in `CLAUDE.md`
- Does this apply only sometimes? → Move to `agent_docs/`
- Can a deterministic tool do this? → Remove entirely (use hooks/formatters)

---

### Phase 2: Progressive Disclosure Architecture

**Content that belongs in `CLAUDE.md`:**
- Project purpose (1–3 sentences)
- Stack summary
- Codebase map / monorepo structure
- The 3–5 commands Claude will use in every session
- Critical conventions Claude must always follow (max 5–10)
- Pointers to `agent_docs/` files

**Content that belongs in `agent_docs/`:**
- Detailed build instructions
- Test conventions and patterns
- Database schema design decisions
- Deployment procedures
- Code style examples

**Reference pattern in `CLAUDE.md`:**
```markdown
For detailed build instructions, see `agent_docs/building.md`.
For test patterns, see `agent_docs/testing.md`.
```

Prefer `file:line` pointers over pasting code snippets — snippets go stale.

---

### Phase 3: Draft CLAUDE.md

**Target length:** Under 150 lines. Under 60 is ideal. Never over 300.

**Template:**

```markdown
# {Project Name}

{1–3 sentence description of what this project does and why it exists.}

## Stack

- **Frontend:** {e.g. React + Vite + TypeScript}
- **Backend:** {e.g. FastAPI + Python 3.12}
- **Database:** {e.g. PostgreSQL + SQLAlchemy}
- **Infra:** {e.g. Docker Compose, nginx}

## Project Structure

{Only include if non-obvious or monorepo}

```
src/
  components/   # React components
  api/          # API client
backend/
  routers/      # FastAPI route handlers
  models/       # SQLAlchemy models
```

## Development

```bash
# Install dependencies
{command}

# Run dev server
{command}

# Run tests
{command}

# Build
{command}
```

## Key Conventions

- {Convention 1 — e.g. "All API calls go through src/api/client.ts"}
- {Convention 2 — e.g. "Use UUIDv7 for all entity IDs"}
- {Convention 3 — max 5–10 total}

## Agent Docs

For detailed guidance on specific tasks:
- `agent_docs/building.md` — Build and deploy procedures
- `agent_docs/testing.md` — Test patterns and conventions
- `agent_docs/architecture.md` — Key design decisions
```

**Anti-patterns to avoid:**
- ❌ Style instructions ("always use 2 spaces") — use a formatter + hook
- ❌ Task-specific instructions that don't apply every session
- ❌ Code snippets that will go stale — use file:line pointers
- ❌ Auto-generated boilerplate — every line must be deliberate
- ❌ "Hotfix" reminders — they'll be ignored or exhaust the instruction budget

---

### Phase 4: agent_docs/ Files (Optional)

Create supporting files only when there's enough content to justify them.

**When to create `agent_docs/building.md`:**
- Build process has more than 3 steps
- Environment setup is non-trivial
- There are multiple build targets

**When to create `agent_docs/testing.md`:**
- Test setup requires fixtures, seeds, or environment
- Multiple test layers (unit, integration, e2e)
- Non-obvious test patterns

**Format for agent_docs files:** Concise, task-oriented. No fluff.

---

### Phase 5: User Review

Present the final `CLAUDE.md` to the user:

```
"Here is the proposed CLAUDE.md:

LENGTH: {N} lines
INSTRUCTIONS: ~{N} (budget remaining: ~{100–N})
agent_docs: {list of files, or "none"}

[CLAUDE.md content]

Would you like me to:
1. Write the files directly
2. Adjust something first
3. Review the agent_docs files as well"
```

---

## Quality Checklist

Before writing files, verify:

- [ ] Every line applies to every session (no task-specific content)
- [ ] Under 150 lines total (ideally under 60)
- [ ] WHY, WHAT, and HOW are all covered
- [ ] Style enforcement is delegated to tools, not Claude
- [ ] No copy-pasted code blocks that will go stale
- [ ] Monorepo structure is explicit (if applicable)
- [ ] `agent_docs/` referenced for task-specific details
- [ ] Manually crafted — not auto-generated from README

## Key Insight

> "CLAUDE.md represents the highest-leverage configuration point in your Claude Code setup. Each line cascades through research, planning, and implementation phases across every session."

Craft each line deliberately. Less is more — a 50-line `CLAUDE.md` that applies universally beats a 300-line file that's half ignored.
