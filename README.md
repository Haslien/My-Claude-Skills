# My Claude Skills

A personal collection of Agent Skills for Claude Code, by [Mathias Haslien](https://mathias-haslien.no/). Each skill encodes a workflow — something I kept doing the same way, often enough that it was worth writing down once and automating.

The list grows as new patterns become repeatable.

## Skills

| Skill | What it does |
|---|---|
| [`claude-md-writer`](.claude/skills/claude-md-writer/SKILL.md) | Creates or audits `CLAUDE.md` files — the context file that bootstraps Claude into a codebase |
| [`skill-writer`](.claude/skills/skill-writer/SKILL.md) | Guides you through writing new skills |
| [`frontend-design`](.claude/skills/frontend-design/SKILL.md) | Builds frontend components with real design quality, not generic AI output |
| [`stack-setup`](.claude/skills/stack-setup/SKILL.md) | Scaffolds a monorepo: React+Vite, React Native+Expo, Fastify, PostgreSQL, MongoDB, Qdrant |
| [`type-safety`](.claude/skills/type-safety/SKILL.md) | Enforces strict typing, Zod schemas, and ESLint/Pyright config across a monorepo |
| [`business-model-canvas`](.claude/skills/business-model-canvas/SKILL.md) | Walks through a Business Model Canvas using the Osterwalder framework |
| [`humanizer`](.claude/skills/humanizer/SKILL.md) | Rewrites AI-sounding text so it reads like a person wrote it |
| [`cybersecurity`](.claude/skills/cybersecurity/SKILL.md) | Structured security audit — secrets in git, auth flaws, injection, GDPR, CVE scan, and more |
| [`index-content`](.claude/skills/index-content/SKILL.md) | Creates a navigable `index.md` for a folder of documents or code |
| [`typography`](.claude/skills/typography/SKILL.md) | Professional type systems — font selection, scale, line-height, tracking, micro-typography |
| [`slides`](.claude/skills/slides/SKILL.md) | Designs presentation decks. Synthesises Reynolds, Duarte, and Knaflic. Asks first whether you want a written plan for PowerPoint/Keynote, or a code-built React SPA deck for high-stakes pitches |
| [`reference-skill`](.claude/skills/reference-skill/SKILL.md) | Generates a standardized, consent-gated reference block when one skill should recommend installing another from this repo |

## How it works

Skills are markdown files that inject structured instructions into a Claude Code conversation when triggered. They live in `.claude/skills/` and activate automatically when Claude recognizes the right context, or explicitly via `/skill-name`.

To use these: clone the repo and point Claude Code at it, or copy individual skill folders into your own project's `.claude/skills/` directory.

## Adding new skills

Run `/skill-writer`. It walks through purpose, triggers, workflow, and output format — and writes the `SKILL.md` for you.
