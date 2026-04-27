---
name: slides
description: Design and write great presentation decks (PowerPoint, Keynote, Google Slides, pitch decks, conference talks, lectures). Synthesises lessons from Garr Reynolds (Presentation Zen), Nancy Duarte (slide:ology), and Cole Nussbaumer Knaflic (Storytelling with Data). Use when the user asks for slides, a deck, a pitch, a presentation, lysbilder, presentasjon, pitch deck, foredrag, or wants to turn data into a clear visual story. Covers preparation, story structure, slide design, data visualisation, and live delivery.
---

# Slides

This skill helps build presentations that actually move an audience — not slides that double as documents. It synthesises three books that already live in this repo: **Presentation Zen** (Reynolds), **slide:ology** (Duarte), and **Storytelling with Data** (Knaflic). Full per-chapter notes with page references are in [material/index.md](material/index.md).

## When to use this skill

Trigger on requests like: "make a deck", "design slides for X", "build a pitch deck", "lag en presentasjon", "improve these slides", "turn this report into a talk", "visualise this data for a board meeting", "we have a keynote next week", or any time the user shares slide content, an outline, a chart, or raw data and needs it presented.

## Ask first — before anything else

The **very first action** when this skill triggers — before any audience analysis, before any outline, before any "what's your topic" — is to ask the user *how they want the deck delivered*. Don't assume. Don't pick for them. Ask.

There are two ways forward, and the right answer depends on the user, not on you.

### Mode A — You build it yourself (PowerPoint, Keynote, Google Slides, Pitch, Tome…)

I write the deck plan — core message, three-act outline, slide-by-slide copy, asset checklist, optional handout outline. You take that plan into your tool of choice and assemble the actual slides yourself.

**Best for:**
- Internal decks reviewed in 30 minutes and forgotten.
- Academic talks, training sessions, status updates.
- Anything that has to be edited later by a designer, marketing team, or non-developer.
- Tight timelines where a written plan is enough and the visual production isn't the point.

### Mode B — We build it as code (the system we already have)

We have a complete, well-tested system for building real pitch decks as static React SPAs. It's not "spin up a React project and figure it out" — it's a documented playbook with a proven set of components, navigation patterns, and conventions. The user gets:

- A **fixed-aspect 16:9 stage** that scales to any window without reflowing — slides look the same on any projector or screen.
- **Keyboard navigation** — arrows, `Esc`/`O` for overview, `1`–`9` to jump, `#/12` deep-links, `B` for black screen.
- **Three-piece floating chrome** — progress bar, corner logo + counter, overview button. No toolbar competing with content.
- **Custom Motion-orchestrated reveals** — diagrams that draw themselves, state machines that animate, mockups that breathe. Things PowerPoint can't fake convincingly.
- **Type-safe slide registry** with Zod validation, so typos and missing assets fail at build time.
- **Graceful image placeholders** (`SmartImage`) so the deck looks intentional even before final assets land.
- **Narrative companion documents** — `PLAN.md`, `README.md`, optional `REDESIGN.md` — shipped alongside the code so non-developers can review the story without running it.

The full playbook is in [build-deck.md](build-deck.md). It covers the stack, brand discovery, theme tokens, typography, the slide primitive, the stage system, navigation, animations, demo conventions, the build workflow, and the components that reuse 100 % between decks.

**Best for:**
- High-stakes pitches: investor meetings, conference keynotes, sales pitches that need to land.
- Anything where production value is part of the message.
- Decks the user wants to deep-link, version-control, or deploy as a webpage.
- Anyone who'd rather present from a browser than from PowerPoint.

### The exact question to ask

Don't paraphrase. Use this — it gives the user a real choice with the trade-offs visible:

> "Before I dive in — quick question on how you want to deliver this:
>
> **(A)** You build it yourself in PowerPoint / Keynote / Google Slides, and I just hand you the plan (core message, slide-by-slide copy, assets to find). Lighter commitment, fine for internal stuff.
>
> **(B)** I build the actual deck for you using our React-based pitch-deck system — a real web app you run with `npm run dev` and present from a browser. Custom animations, keyboard nav, deep-linking, the works. We've got a polished playbook for it. Best for high-stakes pitches where production value matters.
>
> Which one?"

Then wait for the answer.

### If the user is undecided

Recommend based on stakes:

- **External audience, investor, conference, public launch, anything where a polished deck is part of the pitch** → recommend **(B)**.
- **Internal, quick turnaround, handoff to others, anything that has to live in `.pptx`** → recommend **(A)**.

If they still won't pick, default to **(A)** — it's the lighter commitment and you can always escalate to **(B)** later from the same plan.

### After they choose

- **If Mode A:** continue with the workflow below and produce the artefacts in [Output format (Mode A)](#output-format-mode-a).
- **If Mode B:** switch to the playbook in [build-deck.md](build-deck.md). The workflow below still applies — Mode B isn't a different *strategy*, it's a different *artefact* — but the build steps in build-deck.md take over once the plan is approved.

## Core philosophy

Three principles the books agree on, kept short:

1. **Restraint in preparation.** Plan analog. Find the one core message before opening slideware.
2. **Simplicity in design.** Slides amplify the speaker; they are not the document. If a slide can stand alone, the speaker is redundant.
3. **Naturalness in delivery / data.** Story over data dump. The audience can listen *or* read — never both.

The single most important diagnostic question to ask the user up-front: **"If the audience remembers only one thing, what should it be?"** Everything in the deck must support that answer.

## Workflow

Walk through these four phases in order. Don't skip prep — the most common failure mode is jumping straight to slide #1.

### Phase 1 — Prepare (away from the slideware)

Before opening any tool, get answers to:

- **Audience.** Who are they? What do they already know? What do they care about? What will they push back on?
- **Time / venue.** How long is the slot? Live, recorded, hybrid? Big screen, laptop, Zoom?
- **Outcome.** What should the audience *do, think, or feel* after? ("Approve the budget", "fund the round", "change the policy", "trust me with this project".)
- **Core message.** One sentence. If you can't pass the elevator test (sell it in 30–45 seconds), the deck isn't ready.
- **The "so what?"** ("Dakara nani?") For every section, ruthlessly ask why the audience should care. If you can't answer, cut it.

Sketch the structure on paper, post-its, or a whiteboard. Three "acts" is a manageable default: setup → tension → resolution.

→ Deeper: [Presentation Zen, Ch. 3 Planning Analog](material/index.md#presentation-zen--garr-reynolds), [slide:ology, Ch. 2 Creating Ideas, Not Slides](material/index.md#slideology--nancy-duarte), [SWD, Ch. 1 Context](material/index.md#storytelling-with-data--cole-nussbaumer-knaflic).

### Phase 2 — Story

Slides without a narrative arc are just bullets in a Powerpoint costume. Build the spine first.

- **SUCCESs** (Heath brothers, via Reynolds): Simple, Unexpected, Concrete, Credible, Emotional, Story.
- **Three-act spine.** Setup the world the audience lives in → introduce the tension or problem → resolve with your idea / recommendation.
- **One idea per slide.** If a slide tries to make two points, split it.
- **Use real stories, not abstractions.** "100 grams of fat" → a photo of a plate of fries. "Faster onboarding" → "Mira closed her first deal on day three."
- **The slideument trap.** Slides for talking ≠ documents for reading. If the user wants both, write them as **two artefacts**: a clean deck for the live talk + a separate written leave-behind (PDF, doc) with the detail.
  - Rule of thumb (Duarte): **>75 words on a slide and it's a document, not a slide.**

### Phase 3 — Design

Default to clean. Decoration is not design.

**Layout fundamentals (the Big Four, Reynolds + Duarte):**

- **Contrast.** If two things differ, make them *clearly* different — not slightly. Size, weight, colour, position.
- **Repetition.** A consistent colour palette, type system, and visual motif binds the deck.
- **Alignment.** Nothing placed randomly. Use a grid; everything snaps to invisible lines.
- **Proximity.** Group related items; separate unrelated. The eye should never have to guess what belongs together.

**Anti-slop rules:**

- One idea per slide. Aim for **≤6 words** (Godin's rule, used by Reynolds) when the slide is purely a backdrop. Headlines can be longer if they *are* the point.
- **No bullet-point templates.** If you need a list, use it sparingly; prefer images, single statements, or built diagrams.
- **No 3-D, no drop shadows, no gradients on charts, no clip art.**
- **No logo on every slide.** First and last is enough.
- **Empty (negative) space is structural, not wasted.** If the slide feels crowded, delete things until it breathes.
- **Asymmetric > symmetric** for energy. Centred designs feel formal and static.
- **Full-bleed photography** beats inset thumbnails. Place text in the empty area of the photo, not next to it.
- **Rule of thirds.** Place the focal point at one of the four crossing points of a 3×3 grid, not dead centre.

**Typography:** if the project also has a typography skill, defer to it. Otherwise: max two typefaces, generous line-height, ≥24 pt for body in a presentation context, much larger for keywords. Title case in headings is an AI tell — prefer sentence case.

**Colour:** define a deliberate palette. Default body to a neutral (grey/charcoal/off-white). Reserve one accent colour for the thing you want the audience to look at. Test with colour-blindness in mind — never encode meaning by colour alone.

→ Deeper: [Presentation Zen, Ch. 5–6](material/index.md#presentation-zen--garr-reynolds), [slide:ology, Ch. 5–8](material/index.md#slideology--nancy-duarte).

### Phase 4 — Data (when the deck contains charts)

This is where Knaflic's *Storytelling with Data* takes over. Most "data slides" fail because the chart shows everything and emphasises nothing.

**The six lessons (use them in order):**

1. **Understand the context.** Same data → different chart depending on audience and decision. Don't reuse the exploratory chart you used to find the insight; redesign it for explanation.
2. **Choose an effective visual.** A small set of charts solves almost everything:
   - **Simple text** — when the headline *is* one number ("$2.4M ARR").
   - **Bar chart** (vertical or horizontal) — the workhorse. Baseline must start at zero.
   - **Line chart** — continuous data, especially time series.
   - **Slopegraph** — before / after comparison, two points only.
   - **Heatmap / table** — when the audience needs to read across rows.
   - **Waterfall** — start value → changes → end value.
   - **Avoid:** pie charts, donut charts, dual y-axes, secondary axes, 3-D anything, stacked bars with > 3 segments.
3. **Eliminate clutter.** Kill chart borders, default gridlines, redundant legends, diagonal axis labels, decorative backgrounds. Apply Gestalt principles (proximity, similarity, enclosure) to group without ink.
4. **Focus attention.** Use **pre-attentive attributes** — size, colour, position, intensity — to point at the one thing that matters. Default everything to grey; a single accent colour says "look here". The "where do my eyes go first?" squint test is the gut-check.
5. **Think like a designer.** Form follows function. Annotate the chart in plain language ("Tickets backlog grew here after two people quit in May"). Title = takeaway, not topic ("Approve 2 hires" beats "Ticket Volume Trend").
6. **Tell a story.** A chart slide needs a narrative arc just like the deck does: tension (the problem the data reveals) → resolution (what you're recommending). Annotations carry the story when the speaker isn't there.

→ Deeper: [Storytelling with Data, Ch. 1–7](material/index.md#storytelling-with-data--cole-nussbaumer-knaflic).

### Phase 5 — Deliver

If the user asks for slides only, this section is optional — but flag it in the final summary.

- **Hara hachi bu** (Reynolds): finish at 90–95 % of allotted time. Never run over.
- **Step away from the lectern.** It's a wall between presenter and audience.
- **Keep the lights on.** The audience must be able to see the speaker's face.
- **Use a small remote.** Forward / back / black-screen, nothing more. Don't return to the laptop between slides.
- **Animation = clarification.** Build complex diagrams or charts in steps. No spins, dissolves, bounces.
- **Black slide ("B" key).** When the audience needs to look at *you*, not the slide, hide the slide.

## Output format (Mode A)

When the user picks **draft mode**, return artefacts in this order, unless they ask for less:

1. **One-line core message.** "If they remember one thing…"
2. **Three-act outline.** Setup / tension / resolution, one line each.
3. **Slide-by-slide list.** For each slide: a headline, a one-sentence description of the visual, and a one-line speaker note. No fluff.
4. **Asset checklist.** Photos to find / charts to build / quotes to verify, with sources.
5. **Optional leave-behind plan.** If a written handout makes sense, sketch a short outline so it isn't smuggled into the slides as walls of text.

For *redesigns* of existing slides: show before / after for each slide and explain the *why* in one line per change ("Removed 3-D, switched to grey + one accent on May → because that's the moment the audience needs to notice").

## Output format (Mode B)

When the user picks **build mode**, the artefact is a working static React deck. Follow the playbook in [build-deck.md](build-deck.md). The order of operations is:

1. **A `PLAN.md` first** — full audience analysis, three-act outline, slide-by-slide narrative with copy and demo specs. *Do not write a single line of TSX before the plan is approved.*
2. **Bootstrap the Vite project** — Tailwind, fonts, theme tokens, Lucide, Motion, Zod.
3. **Slide shell + Zod-validated registry + keyboard nav + overview grid.**
4. **All copy as plain text-only slides first** — story before decoration. Run each slide's copy through the [`humanizer`](../humanizer/SKILL.md) skill before committing.
5. **Custom demo components** in priority order — most central diagram first.
6. **Polish pass** — stagger timings, hover states, atmosphere, `prefers-reduced-motion`.
7. **A `README.md`** — setup, scripts, navigation, slide map.

## Reference material

Full notes — chapter titles, page numbers, key principles, quotes — live in [material/index.md](material/index.md). Three sources currently indexed:

- **Presentation Zen** (Garr Reynolds, 2008) — restraint, simplicity, naturalness; visual storytelling fundamentals.
- **slide:ology** (Nancy Duarte, 2008) — design discipline; diagrams; the document/teleprompter/presentation spectrum.
- **Storytelling with Data** (Cole Nussbaumer Knaflic, 2015) — chart selection, decluttering, pre-attentive attributes, narrative for analysts.

When in doubt about a specific principle, *consult the index first* before generating advice from general training. Cite by chapter and page when you can.

## Recommended companion skills

Slide headlines, speaker notes, and leave-behind documents are prime AI-tell territory — phrases like "leveraging synergies", "in today's evolving landscape", "underscoring its importance", and the rule-of-three closer all signal generated text. After drafting copy for a deck, run it through `humanizer` to strip those patterns out.

If the user is in **Mode B** (build-as-code), there are two more companion skills worth surfacing — `typography` for the deck's type system and `frontend-design` for the overall visual quality. Both are documented in [build-deck.md](build-deck.md#recommended-companion-skills).

Use the [`reference-skill`](../reference-skill/SKILL.md) template when surfacing any of these to the user. Render the block, then *stop and ask for consent* before installing anything — the user must explicitly say `yes` (project), `yes personal`, or `no`.

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
