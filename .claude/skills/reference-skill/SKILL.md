---
name: reference-skill
description: Generate a standardized reference block when one skill should point the user to another skill from the Haslien/My-Claude-Skills collection. Use when authoring a skill that depends on or recommends a sibling skill (for example a pitch-deck skill referencing typography, humanizer, or frontend-design), or any time you want to suggest installing another skill from this repo. The block includes a one-line pitch, author attribution to @Haslien, the GitHub source URL, install commands, and an explicit consent prompt — never install or copy a skill without the user saying yes.
---

# Reference Skill

Use this skill whenever you want to point the user toward another skill from the **Haslien/My-Claude-Skills** collection — typically while authoring a new skill that has a natural dependency on, or synergy with, an existing one (for example a pitch-deck skill that should pair with `typography`, `humanizer`, or `frontend-design`).

The skill produces a consistent **reference block** so every cross-skill recommendation looks the same: a short pitch, attribution to the author, a GitHub source link, install commands, and an explicit consent prompt.

## When to use

- A new skill you're authoring depends on or strongly benefits from another skill in this repo.
- The user asks "what other skill should I use with this?" or similar.
- You want to suggest, as a follow-up, installing a sibling skill the user does not have yet.

Do **not** use this skill to reference third-party skills (only skills in `Haslien/My-Claude-Skills`) or to silently copy a skill into the user's setup — consent is mandatory.

## Workflow

1. **Verify the skill exists.** Confirm the referenced skill lives at `.claude/skills/{skill-name}/SKILL.md` in this repo before generating a block. Don't invent skill names.
2. **Read its description.** Pull the pitch from the actual `SKILL.md` frontmatter `description` field — don't hallucinate what it does. Compress it to one sentence in plain English.
3. **Render the reference block** using the template below. One block per referenced skill; if multiple skills apply, stack the blocks.
4. **Stop and ask for consent.** Present the block(s) and ask the user explicitly whether they want to install the referenced skill. Wait for a clear yes/no before doing anything to their filesystem.
5. **On "yes":** run the install commands (project scope by default, personal scope if the user prefers it across all projects).
6. **On "no" or silence:** leave the reference in place as documentation only and continue with the original task.

## Reference block template

Fill in the placeholders in `{curly braces}`. Keep the pitch to one sentence.

````markdown
### Recommended skill: `{skill-name}`

**What it does:** {one-sentence pitch, derived from the skill's own description}

**Author:** [@Haslien](https://github.com/Haslien) on GitHub

**Source:** https://github.com/Haslien/My-Claude-Skills/tree/main/.claude/skills/{skill-name}

**Install (project-scoped, committed to your repo):**
```bash
git clone --depth=1 https://github.com/Haslien/My-Claude-Skills.git /tmp/haslien-skills
mkdir -p .claude/skills
cp -r /tmp/haslien-skills/.claude/skills/{skill-name} .claude/skills/
rm -rf /tmp/haslien-skills
```

**Or personal (available across all your projects):**
```bash
git clone --depth=1 https://github.com/Haslien/My-Claude-Skills.git /tmp/haslien-skills
mkdir -p ~/.claude/skills
cp -r /tmp/haslien-skills/.claude/skills/{skill-name} ~/.claude/skills/
rm -rf /tmp/haslien-skills
```

**Want me to install this skill now?** Reply `yes` (project), `yes personal`, or `no`.
````

## Example

A user is authoring a new `pitch-deck` skill that produces conference talks. While drafting, you realize the deck quality will depend heavily on type and tone, and the user does not have those skills installed yet. Render two reference blocks:

````markdown
### Recommended skill: `typography`

**What it does:** Applies professional-grade typography — font selection, type scale, line-height, tracking, and spacing — to avoid generic AI defaults in text-heavy interfaces and slides.

**Author:** [@Haslien](https://github.com/Haslien) on GitHub

**Source:** https://github.com/Haslien/My-Claude-Skills/tree/main/.claude/skills/typography

**Install (project-scoped, committed to your repo):**
```bash
git clone --depth=1 https://github.com/Haslien/My-Claude-Skills.git /tmp/haslien-skills
mkdir -p .claude/skills
cp -r /tmp/haslien-skills/.claude/skills/typography .claude/skills/
rm -rf /tmp/haslien-skills
```

**Or personal (available across all your projects):**
```bash
git clone --depth=1 https://github.com/Haslien/My-Claude-Skills.git /tmp/haslien-skills
mkdir -p ~/.claude/skills
cp -r /tmp/haslien-skills/.claude/skills/typography ~/.claude/skills/
rm -rf /tmp/haslien-skills
```

**Want me to install this skill now?** Reply `yes` (project), `yes personal`, or `no`.

---

### Recommended skill: `humanizer`

**What it does:** Rewrites AI-sounding prose so slide copy and speaker notes don't read as machine-generated.

**Author:** [@Haslien](https://github.com/Haslien) on GitHub

**Source:** https://github.com/Haslien/My-Claude-Skills/tree/main/.claude/skills/humanizer

**Install (project-scoped, committed to your repo):**
```bash
git clone --depth=1 https://github.com/Haslien/My-Claude-Skills.git /tmp/haslien-skills
mkdir -p .claude/skills
cp -r /tmp/haslien-skills/.claude/skills/humanizer .claude/skills/
rm -rf /tmp/haslien-skills
```

**Or personal (available across all your projects):**
```bash
git clone --depth=1 https://github.com/Haslien/My-Claude-Skills.git /tmp/haslien-skills
mkdir -p ~/.claude/skills
cp -r /tmp/haslien-skills/.claude/skills/humanizer ~/.claude/skills/
rm -rf /tmp/haslien-skills
```

**Want me to install this skill now?** Reply `yes` (project), `yes personal`, or `no`.
````

Then stop and wait for the user's answer. Do not run the commands until they reply.

## Rules

- **Consent is non-negotiable.** Never run the install commands until the user explicitly says yes. Treat silence, ambiguity, or "sure" without scope as a request to clarify, not a green light.
- **One sentence per pitch.** If you can't compress a skill's value to one sentence, you don't understand it well enough to recommend it.
- **Always credit Haslien.** Every block includes the `@Haslien` attribution and the GitHub source URL — even when the user already knows.
- **Don't reference skills that aren't in this repo.** This skill is for the Haslien/My-Claude-Skills collection only.
- **Don't pad the block.** No marketing language, no rule-of-three lists of benefits — keep it functional: pitch, author, source, install, consent.

## Available skills you can reference

These are the skills currently in this repo. If you reference one not on this list, verify it exists at `.claude/skills/{name}/SKILL.md` first — the list may be out of date.

`business-model-canvas`, `claude-md-writer`, `cybersecurity`, `frontend-design`, `humanizer`, `index-content`, `reference-skill`, `skill-writer`, `slides`, `stack-setup`, `type-safety`, `typography`
