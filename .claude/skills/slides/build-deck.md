# Build a deck as code

When the user has agreed to "build the deck for me" (the **build mode** in [SKILL.md](SKILL.md)), produce a static React SPA — not slide copy in a doc. This file is the full technical playbook: stack, architecture, conventions, and the patterns that survive across multiple decks.

## Why code, not PowerPoint

- **Animation that explains.** Motion-orchestrated reveals build understanding step by step instead of flashing finished diagrams. PowerPoint's "fly in from left" is slop; a custom React diagram that draws itself is the point of the slide.
- **Custom demos.** Pipeline diagrams, state machines, mockups, sparklines — anything you'd struggle to fake in PowerPoint becomes a 100-line React component.
- **Deep-link & overview.** `#/12` jumps to slide 12. `Esc` opens a grid of all slides. PowerPoint can't.
- **Type safety + Zod.** Slide content is validated; typos in titles or missing assets fail at build time.
- **One source of truth for tokens.** Brand colours, fonts, spacing live in CSS variables — change one place, the whole deck updates.
- **Static deploy.** Vercel, Netlify, GitHub Pages, or just `npm run build` and host the `dist/` folder anywhere.

## The stage system — the single most important pattern

If you only take one thing from this doc, take this. It's what separates a real deck from a webpage that happens to have slides.

### The problem

Browser windows are not 16:9. They are 1366 × 768, 1920 × 1080, an external monitor at 2560 × 1440, a side-by-side window at 960 × 1080. If you build slides at "viewport size", every audience sees a different layout. Worse — long content overflows and gets cut off when the projector aspect ratio is wrong.

### The fix

Render every slide inside a **fixed logical canvas** (default `STAGE_W × STAGE_H = 1440 × 810`, i.e. 16:9) and apply a uniform `transform: scale(N)` so the canvas fits the actual window while keeping its proportions. Anything that doesn't fit inside the canvas is clipped.

```tsx
// src/components/SlideStage.tsx
export const STAGE_W = 1440
export const STAGE_H = 810

export function SlideStage({ children }: { children: ReactNode }) {
  const [scale, setScale] = useState(1)

  useEffect(() => {
    function fit() {
      const s = Math.min(
        (window.innerWidth - 24) / STAGE_W,
        (window.innerHeight - 24) / STAGE_H,
      )
      setScale(Math.max(0.2, s))
    }
    fit()
    window.addEventListener('resize', fit)
    return () => window.removeEventListener('resize', fit)
  }, [])

  return (
    <div className="fixed inset-0 flex items-center justify-center pointer-events-none">
      <div
        style={{
          width: STAGE_W,
          height: STAGE_H,
          transform: `scale(${scale})`,
          transformOrigin: 'center center',
        }}
        className="relative overflow-hidden flex flex-col pointer-events-auto"
      >
        {children}
      </div>
    </div>
  )
}
```

Three guard-rails make this work:

1. **`pointer-events: none` on the outer wrapper, `auto` on the inner stage** — so clicks on the letterbox bars don't intercept anything else.
2. **`overflow: hidden`** — slide content is clipped to the canvas. Designers can't accidentally bleed outside.
3. **`transformOrigin: center`** — the stage stays centred regardless of scale.

### Consequences for slide design

Inside the stage, you can pretend the viewport is *always* exactly 1440 × 810. That changes a few habits:

- **Use `rem` and fixed `px` for type sizes** — never `vw`/`vh`. Viewport units reference the actual window, not the stage, so they fight the scale transform.
- **Tailwind responsive prefixes (`md:`, `lg:`) still work**, but they react to actual viewport width, not stage width. Inside the stage you usually want a single intent — design for the 1440 layout and skip the small breakpoints.
- **Don't rely on scrolling.** A slide that doesn't fit in 810 px gets clipped. Either trim content or break across two slides.

## Stack

- **Vite + React 18 + TypeScript (strict)** — single-page app, no router beyond a URL hash.
- **Tailwind CSS** with CSS variables for theming. Tokens defined once in `src/theme.css`.
- **[Motion](https://motion.dev/)** (the successor to Framer Motion) for reveals, transitions, and demo animations. No scroll-trigger — everything is driven by slide change.
- **Lucide React** for every icon. Never emoji, never Font Awesome, never Material Icons.
- **Zod** validates the slide registry shape so typos don't ship.
- **Google Fonts** via `<link rel="preconnect">` + `display=swap`.

No backend, no database, no Docker. The whole deck is a static SPA.

## Repo layout

A flat Vite project — not a pnpm monorepo (overkill for a single deck):

```
deck-name/
├── public/
│   ├── logo_full.png
│   ├── logo_icon.png            # also used as favicon
│   └── images/                  # slide imagery — keep an images/README.md listing expected files
├── src/
│   ├── main.tsx                 # entry point
│   ├── theme.css                # tokens, fonts, atmosphere, type primitives
│   ├── app/
│   │   ├── App.tsx              # composition: chrome + stage + overview
│   │   └── useDeck.ts           # state, keyboard nav, URL hash sync
│   ├── components/
│   │   ├── SlideStage.tsx       # ⭐ scale-to-fit canvas
│   │   ├── DeckChrome.tsx       # progress bar + corner logo + overview button
│   │   ├── SlideOverview.tsx    # Esc / O grid view
│   │   ├── Slide.tsx            # generic slide wrapper
│   │   ├── Logo.tsx             # variant=full|icon, size=sm|md|lg
│   │   ├── SmartImage.tsx       # graceful image fallback
│   │   └── StatCard.tsx         # primitive cards used inside slides
│   ├── slides/
│   │   ├── index.ts             # ⭐ registry — array of slides + Zod schema
│   │   └── NN_Title.tsx         # one file per slide, default-export a component
│   └── demos/                   # custom visual components per slide
├── index.html
├── tailwind.config.ts           # tailwind + theme bindings
├── postcss.config.js
├── tsconfig.json
├── vite.config.ts
└── package.json
```

The two ⭐ files (`SlideStage.tsx` and `slides/index.ts`) are the spine. Everything else hangs off them.

## Brand discovery — ask before you open `theme.css`

Before writing a single CSS variable, you need a handful of answers. Some you'll already have from earlier in the conversation — *skip those* and tell the user what you've inferred. Ask only the unknowns, and **always pair every question with a recommendation**. Never throw a blank-slate survey at the user.

### What you need to know

- **The organisation / product / audience.** Sets the whole tone. A fintech and a bouldering gym should not get the same deck.
- **Existing brand assets.** Logo files, hex codes, registered fonts, an existing website to match.
- **Imagery.** What's available, what needs placeholders.
- **The mood.** Luxury, technical, friendly, urgent, formal, playful, clinical.
- **Light or dark deck.** Default light for a pitch; dark only when the brand or venue earns it.

### How to ask: lead with a recommendation

Don't ask "what colour palette do you want?" — that's a blank canvas, and the user will hate it. Ask:

> "Since you're [an early-stage SaaS / a regional consultancy / a healthcare startup], I'd lean toward [a neutral palette with one bold accent / a warm editorial palette / a clinical near-white with a single trust-blue]. Headlines in [a high-contrast serif / a heavy grotesque / a soft humanist sans], body in [DM Sans / Hanken Grotesk / Inter Tight]. Atmosphere [subtle gradient / quiet near-flat]. Sound right, or is there a brand book I should follow instead?"

The user can then react to a concrete proposal — agree, tweak one axis, or hand over an existing brand book — instead of inventing a visual identity from scratch.

If they already have a brand book, palette, or website to match: *skip the recommendation and use what they have.* The ask becomes "drop the hex codes and font names and I'll wire them in."

### Quick suggestive map by organisation type

Starting points to *propose*, not rules. If a user lands somewhere unusual (a fintech that wants editorial warmth, an industrial brand that wants luxury), follow them — these are vibes, not laws.

| Organisation / context | Palette direction | Type direction | Atmosphere |
|---|---|---|---|
| Early-stage tech / SaaS | Off-white bg + 1 saturated accent | Geometric sans display + clean sans body | Subtle gradient |
| Enterprise / B2B | Cool neutrals + corporate blue/teal | Neo-grotesque or humanist sans | Minimal noise |
| Fintech / banking | Near-white + deep accent (navy / forest) | Editorial serif display + sans body | Quiet, restrained |
| Healthcare / wellness | Warm off-white + soft green/blue accent | Humanist sans throughout | Soft glow, no hard edges |
| Luxury / lifestyle | Cream or warm bg + jewel accent | High-contrast serif + clean sans | Strong noise overlay |
| Industrial / hardware | Charcoal bg + safety-orange or yellow | Heavy grotesque or condensed | Hard edges, monospace data |
| Editorial / media | Cream + bold accent | Display serif + sans body + mono | Warm, paper-feeling |
| Public sector / NGO | Sober neutrals + one trust colour | Humanist sans, very legible | Calm, no flash |
| Creative agency / brand | Whatever they brought | Whatever they brought | Theirs entirely |

### Imagery discovery

- "Do you have a folder of brand photography or product shots? Drop the path and I'll wire it in."
- "Any specific hero image you want on the title slide?"
- "Anything I should *avoid* — stock-photo clichés the brand has burned on, or anything off-brand?"

If they have nothing yet: ship the deck with `SmartImage` placeholders (see [Image handling](#image-handling--graceful-placeholders)). They look intentional. Drop a `public/images/README.md` listing the shots that would help, so a designer can fill them in later without reading code.

### When to skip discovery

You don't need to ask if:

- The user uploaded a brand book or visual identity guide → use it.
- The repo already has a `theme.css` → match the existing tokens.
- The user said "match my website / our other deck / Brand X" → mirror that.
- The earlier conversation already covered the topic → use what they said.

A skipped question is a faster build. Confirm what you've inferred in one line and move on:

> "I'll use the palette and fonts from your landing page (`#0e0d0c` background, `#c83a3a` accent, Syne / DM Sans). Shout if that's wrong."

### Lock the answers into a brief

Once the user confirms, write the answers into the project's `PLAN.md` under a "Brand" or "Visual direction" heading. That becomes the single source of truth — every future tweak references it instead of re-litigating the choice.

## Theme tokens

Define everything in `src/theme.css` as CSS variables. Tailwind reads them via `tailwind.config.ts`. The deck has *one* place to change colour, type, or spacing — never duplicate in component files.

```css
:root {
  /* Brand — pick a deliberate palette */
  --brand-bg:       #fafafa;        /* page background */
  --brand-surface:  #ffffff;        /* cards, panels */
  --brand-border:   #e5e5e3;
  --brand-text:     #2d2d2a;        /* primary text */
  --brand-muted:    #7a7a75;
  --brand-accent:   #7a021d;        /* the one colour that says "look here" */
  --brand-accent-2: #f1b341;        /* secondary, used sparingly */

  /* Type — display + body + mono */
  --font-display: 'Syne', system-ui, sans-serif;
  --font-body:    'DM Sans', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', ui-monospace, monospace;
}
```

**Atmosphere** — every slide sits on a subtle radial gradient (accent-tinted) plus a ~3 % noise overlay (pseudo-element with a tiny SVG noise pattern). Without it, slides feel flat. The gradient and noise live at body level so they show through to the letterbox bars too — what stops the deck from feeling like a Notion page.

```css
body::before {
  content: '';
  position: fixed; inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 100% 0%,
      color-mix(in oklab, var(--brand-accent) 12%, transparent) 0%,
      transparent 50%);
  pointer-events: none;
}
body::after {
  content: '';
  position: fixed; inset: 0;
  background-image: url("data:image/svg+xml,...noise...");
  opacity: 0.03;
  pointer-events: none;
}
```

Also define a small set of **typographic primitives** as utility classes here — `.eyebrow`, `.display-hero`, `.display-h1`, `.body-md`, `.data`, `.label`. Slides reference them by class, so a global type tweak propagates everywhere.

## Typography

Pick three families: **display + body + mono**. Avoid Inter, Roboto, Open Sans, system-ui (the AI-default tells). Pair across categories.

| Tone | Display | Body | Mono |
|---|---|---|---|
| Editorial / contemporary | Syne | DM Sans | JetBrains Mono |
| Industrial / technical | Barlow Condensed | Hanken Grotesk | IBM Plex Mono |
| Luxury | Bodoni Moda | Inter Tight | Space Mono |
| Soft / warm | Fraunces | Manrope | DM Mono |

For scale, line-height, weight pairing, and tracking, defer to the `typography` companion skill (block at the [bottom of this file](#recommended-companion-skills)). Quick fallback if the user doesn't want to install it: ≥24 pt body in a presentation context, ratio 1.25–1.414, skip a weight when pairing (Regular → Bold, never Regular → Medium). Headings in **sentence case**, not Title Case (Title Case is an AI tell).

## Chrome — three small floating elements

A pitch deck *is* the slide. Chrome (header, navigation, branding) should be present but never compete with content. The pattern that works:

1. **Progress bar** — 2 px tall, top edge of viewport, fills with the accent colour as you advance.
2. **Logo + counter** — bottom-left, 24 px logo, monospace `01 / 27` counter next to it.
3. **Overview button** — bottom-right, 28 × 28 px Lucide grid icon.

That's everything. No top header bar, no bottom toolbar, no slide title duplicated above the slide.

```tsx
// src/components/DeckChrome.tsx — total under 60 lines
<>
  <div className="fixed top-0 left-0 right-0 h-[2px]"> {/* progress */} </div>
  <div className="fixed bottom-4 left-5 flex items-center gap-2"> {/* logo + counter */} </div>
  <button className="fixed bottom-4 right-5 w-7 h-7"> {/* overview */} </button>
</>
```

All three are `position: fixed` to viewport coords, so they stay in the screen corners regardless of stage scale. They live *outside* the stage's `overflow: hidden`, so they never get clipped.

## Navigation — keyboard-first

The deck is keyboard-driven. Mouse / touch are fallbacks.

| Input | Action |
|---|---|
| `→` · `Space` · `PgDn` | Next slide |
| `←` · `PgUp` | Previous slide |
| `Home` / `End` | First / last |
| `Esc` · `O` | Toggle overview grid |
| `1`–`9` | Jump to slide N |
| `B` | Black screen (talk-to-audience moment) |
| `#/12` in URL | Deep-link to slide 12 |

Implement in a single `useDeck()` hook (~80 lines) that owns:

- `index` state.
- URL-hash sync — read `#/3` on load, write back on change, listen to `hashchange`.
- `keydown` event listener with all the bindings above.
- `overviewOpen` state for the grid view.

```ts
// src/app/useDeck.ts — the deck's brain
export function useDeck() {
  const [index, setIndex] = useState(() => readHash())
  const [overviewOpen, setOverviewOpen] = useState(false)
  // ... keydown listener, hashchange sync, prev/next/goto/first/last
  return { index, total, next, prev, goto, first, last,
           overviewOpen, openOverview, closeOverview }
}
```

The whole deck UI is then `const deck = useDeck()` plus rendering. Mirror the URL hash both ways — typing `#/5` and pressing arrow keys both update state and URL.

## The Slide primitive

About 90 % of slides follow the same shape: eyebrow + title + subtitle + body + footer. Write one component and reuse it:

```tsx
// src/components/Slide.tsx
type SlideProps = {
  eyebrow?: string;       // small kicker above the title
  title: string;          // big H1
  subtitle?: string;      // secondary line under the title
  body?: ReactNode;       // diagram, demo, content
  footer?: ReactNode;     // attribution, source line, closing line
};

<Slide
  eyebrow="Step 7"
  title="The headline goes here"
  subtitle="An optional subtitle clarifies the angle."
  footer="Source: ..."
>
  <YourDemo />
</Slide>
```

Built-in **orchestrated reveal**: eyebrow at 0 ms → title at 70 ms → subtitle at 140 ms → body → footer. Each element wraps in a Motion `motion.div` with delay tied to its position. New slides inherit a coherent rhythm without touching motion code.

For slides that need a different layout (the title slide, the closing CTA), skip `<Slide>` and write a free-form layout directly. Both patterns coexist.

## Slide registry + Zod

Slides are not scrolling routes. They're an ordered array.

```ts
// src/slides/index.ts
import { z } from 'zod';
import Slide01Title from './01_Title';
// ...

const SlideEntry = z.object({
  id: z.string().min(1),
  act: z.enum(['I', 'II', 'III', 'IV', 'V']).optional(),
  title: z.string().min(1),
  subtitle: z.string().optional(),
  component: z.custom<ComponentType>(),
});

export const deck = z.array(SlideEntry).parse([
  { id: 'title',     act: 'I', title: 'Title',                 component: Slide01Title },
  { id: 'problem',   act: 'I', title: 'The problem',           component: Slide02Problem },
  // ...
]);
```

Each entry has a stable `id`, a human title for the overview grid, an optional act tag for grouping, and a default-exported component. **Adding a slide = create a file + add a line. Reordering = move a line.**

The Zod parse runs at build time. A missing field or a typo = build fails before the deck ships.

## Animations

- **Slide enter:** title fades in at 0 ms, body elements stagger from 100 ms with 60–80 ms gaps. Use Motion's `staggerChildren` on a wrapping `motion.div`.
- **Slide change:** cross-fade ~250 ms, no harsh cuts.
- **Hover on interactive elements:** `translateY(-2px)` + a subtle accent-coloured glow.
- **Demo components:** loop their auto-play subtly when it serves the metaphor (a sync diagram pulses indefinitely, a state machine highlights its current node).
- **Reduced motion:** respect `prefers-reduced-motion` — disable transforms, keep opacity fades only.

Animation is for **clarification**, not decoration (Knaflic's rule). Build a complex chart point by point. Don't spin, dissolve, or bounce.

## Demos — the visual language

The slide is the wrapper; the visual *story* is told by a demo component. Demos live in `src/demos/` and follow a few conventions:

- **One file per demo**, named after what it shows — `PipelineDiagram.tsx`, not `Diagram1.tsx`.
- **SVG for diagrams**, not D3 or Three.js. Hand-position nodes by percent inside a fixed `viewBox`. Animate `pathLength`, `opacity`, and `transform` with Motion.
- **Lucide icons** for every iconic element. Never emoji.
- **Stagger reveals** with `transition={{ delay: 0.2 + i * 0.1 }}`. The mind builds the diagram piece by piece.
- **Hover tells**, not click tells. A pitch flows forward; clicks are reserved for navigation.

Common demo shapes worth knowing — copy the closest one when starting a new demo:

| Shape | When to reach for it |
|---|---|
| **Orbital** — central node + ring of related items | "X has many Y" relationships, swarms of small entities around a hub |
| **Linear flow** — left → centre → right | step-by-step pipelines, before-during-after |
| **Node-graph** — multiple verbs between nodes | rich relationships (e.g. semantic graphs, dependency maps) |
| **Editorial split** — two sides connected by a verb arc | before / after, then / now, vs comparisons |
| **Dashboard stripe** — animated bar / radar / state machine | system behaviour over time, live metrics |
| **Timeline track** — events along a horizontal axis | sequence, history, roadmap |

If you need a new shape, copy the closest existing demo and adapt — keep them as small files with no shared abstraction. Premature abstraction across demos is the fastest way to make the codebase brittle.

## Image handling — graceful placeholders

Decks need images, and images aren't always ready when the deck is being built. Build a `SmartImage` component:

```tsx
<SmartImage
  src="/images/product.jpg"
  alt="Product hero shot"
  placeholderLabel="Product"
  aspect="1/1"
  hueSeed={7}
/>
```

If the image is at the path, it loads. If not, it falls back to a stable, hue-seeded gradient placeholder with the label printed in the corner. The deck looks intentional even before assets land — no broken-image icons.

Alongside it, ship a `public/images/README.md` listing every filename a slide expects. Non-developers can drop assets into the right place without reading code.

## Design rules when coding

These translate the SKILL.md design phase into concrete component decisions:

- **Asymmetric > symmetric.** Don't centre everything. Push hero numbers into one corner, let an oversized element bleed past the column.
- **Big icons as graphics**, not badges. 48–80 px Lucide icons are *the slide*, not 18 px decorations on a card.
- **Big numbers.** Display font, weight 800, very large, lots of empty space around. One stat per slide whenever you can.
- **Diagrams over card grids.** If there's a flow or a relationship, draw it. Animate the arrows. Don't bullet it.
- **Full-bleed photography** with text laid into the empty area of the photo, never inset thumbnails.
- **Charts:** strip 3-D, drop shadows, gridlines, default legends. One accent colour for the point you want made; everything else greyscale.
- **No clip art, no emoji, no Font Awesome, no Microsoft templates.** Lucide-only.
- **Logo:** full lockup on title and close slide; small icon-only mark in the bottom-left chrome on every other slide. Same component, two `variant` props.
- **Footer source lines** in monospace small caps. Cite numbers; readers will check.

## Build workflow

The order matters. Don't skip step 5.

1. **Plan first, in markdown.** Before a single React file, write `PLAN.md` covering audience, narrative, slide-by-slide outline, source material, and open questions. Iterate with the user until the narrative flows.
2. **Brand discovery.** Run through [Brand discovery — ask before you open `theme.css`](#brand-discovery--ask-before-you-open-themecss). Lead every question with a recommendation. Lock the agreed palette + fonts + mood into `PLAN.md` under a "Visual direction" heading. Skip questions you already have answers to.
3. **Bootstrap the stack.** Vite + React 18 + TypeScript strict, Tailwind, Motion, Lucide React, Zod. Pick a port that doesn't collide with anything else in the dev environment.
4. **Theme tokens first.** `theme.css` with the CSS vars from the discovery step, font imports, body atmosphere, type primitive utility classes. Build a `Logo` component and a couple of card primitives before any slide.
5. **Deck shell.** `useDeck` hook + `DeckChrome` (start minimal — three floating elements). `SlideStage` with scale-to-fit. `Slide.tsx` generic wrapper. `SlideOverview` for the grid view.
6. **Registry + N dummy slides.** Each is a single file with placeholder text, registered in `slides/index.ts`. The whole deck navigates end-to-end before any visual work.
7. **Write all copy as plain text.** Fill the slides with real text. No demos yet. This proves the narrative flows on plain content. **Run every slide's copy through the `humanizer` skill before committing** (see [Recommended companion skills](#recommended-companion-skills)) — strip em-dash overuse, "stands as / serves as", -ing-ending fake analyses, rule-of-three closers, copula avoidance, generic positive endings. The deck must have a voice, not sound like ChatGPT.
8. **Build the wow demos first.** Identify the 3–4 slides that have to land — the ones a viewer will remember. Build those demos before any cleanup.
9. **Build remaining demos in priority order.** Each demo gets its own file, its own Motion animation. No shared abstraction.
10. **Visual polish pass.** Drop card grids where icons can be larger. Replace mock data with editorial typography. Add real images via `SmartImage`. Run a fresh humanizer pass on slide copy.
11. **Verify continuously.** `npm run typecheck && npm run build` every few changes. Open the dev server and click through the deck end-to-end before declaring anything done.

## What this approach does NOT do

These are tempting choices that have been considered and rejected. Listed so future-you doesn't burn a day re-litigating them.

- **No backend / API / database.** A pitch deck is content. Pulling live data into a deck makes it brittle and slow.
- **No real ML or video processing in the browser.** Demos are *visual illustrations* with semantically correct mock data, not live systems.
- **No video playback on slides.** Use static stills or animated SVG mockups. Looping video at the start was tempting; in practice it pulls focus and adds megabytes to first paint.
- **No router.** A deck is one page with a slide index in URL hash. Adding TanStack Router for 27 slides is overkill and breaks deep-link simplicity.
- **No CMS-style content config.** Content is colocated with components. Editors edit React directly. The Zod-validated registry prevents typos without forcing a JSON layer.
- **No theme switcher.** Decks are pitched in one mode. Variant proliferation is presenter cognitive load.
- **No mobile-first.** A pitch deck is presented on a laptop or projector. Sub-768 px viewports get a workable downscaled stage but aren't a target.
- **No print stylesheet.** Export to PDF via the browser's built-in fullscreen capture if needed. Print CSS for an animated deck is its own project.
- **No PowerPoint / Keynote export.** The deck *is* a web app. If the user needs `.pptx`, that's a different tool entirely.
- **No hosting / deploy automation in scope.** That's a separate task once the deck is content-complete.

## Documents to write alongside the code

When building a new deck, ship these markdown files in the project root next to `package.json`. They're worth more than the slides themselves — they're how the deck stays editable and how a non-developer reviews the narrative without running it.

1. **`PLAN.md`** — *the document to draft before writing a single line of TSX.* It covers:
   - Audience analysis (who they are, what they care about, what they'll push back on).
   - Stack rationale (what was picked, why, what we deliberately *don't* do).
   - The full slide list with copy and demo specs, organised by act.
   - Source material — every claim, statistic, or quote in the deck cited back to a primary source. The reader of the plan should be able to verify any number on any slide.
   - Open questions for the user that need resolving before build.
2. **`README.md`** — setup, scripts, navigation, project structure, slide map. Short. Someone else should be able to clone the repo and run `npm run dev` from the README alone.
3. **`REDESIGN.md`** *(optional, after the first build)* — slide-by-slide visual upgrade pass. Useful when the v1 deck reads as a "card grid" and needs to push to "visual first" (oversize numbers, real diagrams, animated reveals, less text). Each entry is *before / what's wrong / what to do instead.*

## Reuse between decks

A clean separation between bones (reuse) and content (rewrite) makes the next deck a 30-minute swap.

| Component | Reuse rate | What you change |
|---|---|---|
| `SlideStage` | 100 % | Maybe `STAGE_W` / `STAGE_H` if 4:3 |
| `useDeck` | 100 % | Nothing |
| `DeckChrome` | ~95 % | Logo path |
| `SlideOverview` | 100 % | Nothing |
| `Slide` | ~95 % | Maybe padding for branded margins |
| `SmartImage` | 100 % | Nothing |
| `Logo` | 30 % | Asset paths + sizing rules |
| `theme.css` | 30 % | All colours, fonts, atmosphere |
| `slides/*` | 0 % | Everything — content is the deck |
| `demos/*` | 20 % | Some shapes reusable; most are one-shot |
| `PLAN.md` | 0 % | New narrative |

The 100 %-reuse pieces are the bones. Everything else is content. Keeping a `deck-template` repo around as the starting fork is the cheapest way to ship new decks.

**Fork-and-rip workflow for a new deck:**

1. Copy the repo under a new name.
2. `rm -r src/slides src/demos` and start `slides/index.ts` from scratch.
3. Swap theme tokens in `theme.css` (colours, fonts, logo paths).
4. Replace logos in `public/`.
5. **Keep:** `SlideStage`, `useDeck`, `DeckChrome`, `SlideOverview`, `Slide`, `Logo`, `SmartImage`. These are the bones.
6. Plan the new deck in a fresh `PLAN.md` before writing slides.

If the bones don't fit a particular brief, the three to question first are: the stage transform, the `useDeck` hook, and the slide registry. Those three together make every later choice cheaper.

## Recommended companion skills

A code-built deck leans on three sibling skills from the same collection. When the user reaches the relevant step, surface the reference block below and **stop and ask for consent** before installing — they must explicitly say `yes` (project), `yes personal`, or `no`. Don't run install commands on silence or "sure".

These blocks follow the [`reference-skill`](../reference-skill/SKILL.md) template.

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

### Recommended skill: `frontend-design`

**What it does:** Generates distinctive, production-grade frontend code with creative aesthetic choices — exactly the layer above raw Tailwind/Motion that lifts a deck out of generic-template territory.

**Author:** [@Haslien](https://github.com/Haslien) on GitHub

**Source:** https://github.com/Haslien/My-Claude-Skills/tree/main/.claude/skills/frontend-design

**Install (project-scoped, committed to your repo):**
```bash
git clone --depth=1 https://github.com/Haslien/My-Claude-Skills.git /tmp/haslien-skills
mkdir -p .claude/skills
cp -r /tmp/haslien-skills/.claude/skills/frontend-design .claude/skills/
rm -rf /tmp/haslien-skills
```

**Or personal (available across all your projects):**
```bash
git clone --depth=1 https://github.com/Haslien/My-Claude-Skills.git /tmp/haslien-skills
mkdir -p ~/.claude/skills
cp -r /tmp/haslien-skills/.claude/skills/frontend-design ~/.claude/skills/
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

### When to surface each block

- **`frontend-design`** — early, before component-level styling decisions. Right after Step 2 (Brand discovery), so the recommended visual direction has the skill's polish behind it.
- **`typography`** — also at Step 2 (Brand discovery), when picking the display + body + mono trio. Right before writing `theme.css` and the type scale.
- **`humanizer`** — Step 7, on every commit of slide copy. Also any time you regenerate body text or the leave-behind document.
