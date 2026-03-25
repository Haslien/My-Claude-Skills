# My Claude Skills

A personal collection of Agent Skills for Claude Code, by [Mathias Haslien](https://mathias-haslien.no/). Each skill encodes a workflow — something I kept doing the same way, often enough that it was worth writing down once and automating.

The list grows as new patterns become repeatable.

## Skills

| Skill | What it does |
|---|---|
| `claude-md-writer` | Creates or audits `CLAUDE.md` files — the context file that bootstraps Claude into a codebase |
| `skill-writer` | Guides you through writing new skills |
| `frontend-design` | Builds frontend components with real design quality, not generic AI output |
| `stack-setup` | Scaffolds a monorepo: React+Vite, React Native+Expo, Fastify, PostgreSQL, MongoDB, Qdrant |
| `type-safety` | Enforces strict typing, Zod schemas, and ESLint/Pyright config across a monorepo |
| `business-model-canvas` | Walks through a Business Model Canvas using the Osterwalder framework |
| `humanizer` | Rewrites AI-sounding text so it reads like a person wrote it |

## How it works

Skills are markdown files that inject structured instructions into a Claude Code conversation when triggered. They live in `.claude/skills/` and activate automatically when Claude recognizes the right context, or explicitly via `/skill-name`.

To use these: clone the repo and point Claude Code at it, or copy individual skill folders into your own project's `.claude/skills/` directory.

## Adding new skills

Run `/skill-writer`. It walks through purpose, triggers, workflow, and output format — and writes the `SKILL.md` for you.
