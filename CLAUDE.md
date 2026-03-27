# My Claude Skills

A personal collection of Agent Skills for Claude Code. Each skill encodes a repeatable workflow as a `SKILL.md` file that injects structured instructions into a Claude Code conversation when triggered.

## Structure

```
.claude/skills/
  {skill-name}/
    SKILL.md               # Skill instructions — trigger, workflow, and output format
    {optional sub-files}/  # Supporting docs or templates referenced by SKILL.md
```

## Skills

| Skill | What it does |
|---|---|
| `claude-md-writer` | Creates or audits `CLAUDE.md` files |
| `skill-writer` | Guides through writing new skills |
| `frontend-design` | Builds frontend components with real design quality |
| `stack-setup` | Scaffolds a standard monorepo |
| `type-safety` | Enforces strict typing and Zod schemas |
| `business-model-canvas` | Walks through a Business Model Canvas |
| `humanizer` | Rewrites AI-sounding text |

## Adding or editing skills

Use `/skill-writer` to create new skills — it walks through purpose, triggers, workflow, and output format.

## Conventions

- Each skill lives in its own folder under `.claude/skills/`
- `SKILL.md` is the only required file per skill
- Supporting files (PDFs, sub-docs) go in the skill's folder and are referenced from `SKILL.md`
- Skills should encode one repeatable workflow — no bloat
