# Slides — Reference Material Index

Library of books, PDFs, and other source material the `slides` skill can
draw on. Every entry follows the same format so it's easy to add new
sources over time.

## How to use this file

- Browse to the source under "Sources" and find the topic you need.
- Page numbers refer to the **book's printed page numbers** (not the PDF's
  page numbers), unless noted otherwise.
- For deeper reading: open the file via `Path` with the Read tool and use
  `pages` (PDF) or `offset/limit` (text) to jump straight to the chapter.

## Sources at a glance

Quick lookup of every source. Line numbers point to where each entry starts in this `index.md`.

| # | Title | Author | Year | Line |
|---|---|---|---|---|
| 1 | [Presentation Zen](#presentation-zen--garr-reynolds) | Garr Reynolds | 2008 | L62 |
| 2 | [slide:ology](#slideology--nancy-duarte) | Nancy Duarte | 2008 | L294 |
| 3 | [Storytelling with Data](#storytelling-with-data--cole-nussbaumer-knaflic) | Cole Nussbaumer Knaflic | 2015 | L452 |

## Template for new entries

When you add a new book/PDF, copy the template below and fill in the fields.
Then add a row to the **Sources at a glance** table above with the line
number where the new entry starts.

```markdown
## {Title} — {Author}

- **File:** `{filename}`
- **Path:** `.claude/skills/slides/material/{filename}`
- **Author:** {name}
- **Publisher / year:** {publisher, year}
- **Type:** {book / article / whitepaper / slide deck / ...}
- **Language:** {en / no / ...}
- **Core idea:** {1–2 sentences on what the book contributes to the slides skill}

### Contents (chapters / main sections)

| Ch. | Title | Page |
|---|---|---|
| 1 | ... | p. X |

### Key points

- **{Concept}** (p. X) — {short explanation + why it's useful for slides}
- ...

### Quotes worth remembering

- "..." — {author}, p. X
```

---

# Sources

## Presentation Zen — Garr Reynolds

- **File:** `presentation_zen_design_by_Garr_Reynolds.pdf`
- **Path:** `.claude/skills/slides/material/presentation_zen_design_by_Garr_Reynolds.pdf`
- **Author:** Garr Reynolds
- **Publisher / year:** New Riders, 2008 (1st ed.)
- **Type:** Book (PDF, ~230 pages)
- **Language:** English
- **Note:** The filename contains "design", but the actual content is the
  first edition of *Presentation Zen: Simple ideas on presentation design
  and delivery* — not the follow-up *Presentation Zen Design* (2009).
- **Core idea:** Three principles run through the whole book — **restraint**
  in preparation, **simplicity** in design, **naturalness** in delivery.
  Slides should *amplify* the speaker, not double as a document. Learn from
  Japanese aesthetics (kanso, shizen, shibumi, wabi-sabi), documentary film,
  and comics — not from PowerPoint templates.

### Contents (chapters)

| Part | Ch. | Title | Page |
|---|---|---|---|
| Introduction | 1 | Presenting in Today's World | p. 5 |
| Preparation | 2 | Creativity, Limitations, and Constraints | p. 31 |
| Preparation | 3 | Planning Analog | p. 45 |
| Preparation | 4 | Crafting the Story | p. 75 |
| Design | 5 | Simplicity: Why It Matters | p. 103 |
| Design | 6 | Presentation Design: Principles and Techniques | p. 119 |
| Design | 7 | Sample Slides: Images & Text | p. 165 |
| Delivery | 8 | The Art of Being Completely Present | p. 185 |
| Delivery | 9 | Connecting with an Audience | p. 201 |
| The Next Step | 10 | The Journey Begins | p. 217 |

### Key points

#### Ch. 1 — Presenting in Today's World (p. 5)

- **The bento analogy** (p. 5–6) — content should be packed like a Japanese
  bento: appropriate amount, balanced, nothing superfluous, nothing missing.
- **Three guiding principles** (p. 7) — restraint in preparation, simplicity
  in design, naturalness in delivery.
- **Death by PowerPoint** (p. 10–13) — the tool is not the problem; the
  habits are. Bullet templates and text mirroring the speaker is documented
  ineffective (cognitive load, John Sweller).
- **Six aptitudes** from Daniel Pink's *A Whole New Mind* (p. 14–19) —
  design, story, symphony, empathy, play, meaning. The framing for the
  whole book.
- **Seth Godin essay** (p. 20–21) — "no more than six words on a slide.
  EVER." Use a separate leave-behind document for detail.
- **Slides ≠ document** (p. 22) — modern slides have more in common with
  documentary film and comics (image + narrative) than with business documents.

#### Ch. 2 — Creativity, Limitations, and Constraints (p. 31)

- **Beginner's mind / shoshin** (p. 33–34) — Shunryu Suzuki: "In the
  beginner's mind there are many possibilities, in the expert's mind
  there are few."
- **You are creative** (p. 35) — every profession needs right-brain
  thinking, not just artists (Apollo 13 example).
- **Working with restrictions** (p. 38–41) — references John Maeda's *Laws
  of Simplicity*: "with more constraints, better solutions are revealed."
- **PechaKucha** (p. 41) — 20 slides × 20 seconds = 6:40. Training in
  editorial discipline.
- **In sum** (p. 43) — three keywords: simplicity, clarity, brevity.

#### Ch. 3 — Planning Analog (p. 45)

- **Go analog** (p. 45–50) — pen + paper, whiteboard, Post-its *before* you
  open slideware. The computer should be a "bicycle for the mind", not a car.
- **Slow down to see** (p. 55–58) — busyness kills creativity; carve out
  time alone to find the core message.
- **Wrong vs. right questions** (p. 59–61) — wrong: "how many bullets /
  slides?". Right: how much time, what's the venue, who is the audience,
  what do they expect, *what is the absolutely central point?*
- **Dakara nani? / "So what?"** (p. 64) — ask the relevance question for
  every single slide. Cut what doesn't support the core.
- **Elevator test** (p. 64) — can you sell the point in 30–45 seconds?
- **The slideument trap** (p. 66–71) — slides and documents are different
  formats. Make a *separate* written leave-behind so the slides can stay
  visual. Three components: slides, presenter's notes, handout.

#### Ch. 4 — Crafting the Story (p. 75)

- **SUCCESs** from the Heath brothers' *Made to Stick* (p. 76–79) —
  Simplicity, Unexpectedness, Concreteness, Credibility, Emotions, Stories.
- **Curse of Knowledge** (p. 76) — the expert can't imagine not knowing
  what they know, so the message goes abstract.
- **Authenticity over memorization** (p. 80–81) — internalize the story,
  don't memorize line by line.
- **Information ≠ meaning** (p. 82) — facts are free on Google; what the
  audience wants is context, perspective, and *story*.
- **Four-step process** (p. 85–89) — (1) brainstorm analog, (2) group and
  identify the core, (3) storyboard on Post-its / paper, (4) build the
  storyboard in Slide Sorter / Light Table view.
- **Bumper slides** (p. 88) — Jerry Weissman's section dividers; use a
  contrasting color so they stand out in Slide Sorter.
- **Editing like Lucas** (p. 95–96) — be ruthless. When in doubt: cut it.

#### Ch. 5 — Simplicity: Why It Matters (p. 103)

- **Simple ≠ simplistic** (p. 103–104) — synonymous with clarity,
  directness, subtlety, essentialness, minimalism. Einstein: "as simple as
  possible but no simpler."
- **Steve Jobs vs. Bill Gates** (p. 105–106) — contrast in visual style.
- **Kanso, Shizen, Shibumi** (p. 107–108) — Zen aesthetic principles:
  - **Kanso** = simplicity (Koichi Kawana: "maximum effect with minimum means").
  - **Shizen** = naturalness (forbids elaborate decoration; demands restraint).
  - **Shibumi** = elegance (subtle refinement, the original "less is more").
- **Wabi-sabi** (p. 109–110) — beauty in the simple, irregular, impermanent.
- **The Fish Story** (p. 111) — illustrates reduction: the sign "We Sell
  Fresh Fish Here" is reduced step by step to nothing.
- **Amplification through simplification** (p. 113–115) — from Scott
  McCloud's *Understanding Comics*: simplification amplifies meaning.

#### Ch. 6 — Presentation Design: Principles and Techniques (p. 119)

The book has seven design principles. **The last four make up "the big four".**

- **Signal vs. Noise Ratio** (p. 122–129) — remove anything that doesn't
  contribute: 3D effects (p. 128), logos on every slide (p. 129),
  unnecessary grid lines. Edward Tufte's "smallest effective difference".
- **Bullet points** (p. 130–131) — use *rarely*, not never. The 1-7-7 rule
  is wrong. Compare text-heavy slides with their visual counterparts.
- **Picture Superiority Effect** (p. 132–139) — pictures are remembered
  better than words > 30 seconds after exposure. Pictures + words together
  give optimal recall.
  - **Going Visual** (p. 132): replace descriptive text with photos.
  - **Image sources** (p. 140): iStockphoto, Dreamstime, Fotolia, Flickr CC,
    Morgue File, Stock.xchng, Everystockphoto.
- **Quotes / text within images** (p. 141–143) — place the quote *inside*
  a full-bleed image with good contrast and empty space.
- **Empty Space** (p. 145–147) — negative space isn't "wasted"; it lets
  the few elements breathe. Trapped space (gaps between elements) is often
  worse than clean space surrounding the design.
- **Balance: symmetrical vs. asymmetrical** (p. 148–149) — symmetrical =
  formal and static; asymmetrical = dynamic and more interesting. Mix.
- **Grids and Rule of Thirds** (p. 151–152) — derived from the golden
  mean; place the main subject at one of four crossing points instead of
  dead center.
- **The Big Four** (p. 153–160):
  - **Contrast** (p. 153–154) — make differences *clearly* different.
    Achieved via space, color, type, size, position. Gives the design a
    focal point.
  - **Repetition** (p. 155) — repeating elements (color, font, a motif)
    binds a deck together visually.
  - **Alignment** (p. 157) — no element placed randomly; everything is
    visually connected via an (invisible) line. Use a grid.
  - **Proximity** (p. 157–160) — group related items; separate unrelated
    ones. The audience should never have to guess what belongs together.

**In sum** (p. 163) — design = clarity, not decoration. Remove noise, use
strong visuals, learn to see empty space, apply the four principles.

#### Ch. 7 — Sample Slides: Images & Text (p. 165)

Gallery of examples from different presenters (Jeff Brenman, Chris Landry,
Guy Kawasaki, Pam Slim, Sangeeta Kumar, Merlin Mann, etc.). Common traits
(p. 179):

- Simple visual priorities.
- Visual theme, no overused templates.
- Few or no bullet points.
- High image quality.
- Complex graphics built (animated) in steps.
- "Maximum effect with minimum means."
- Conscious use of empty space.

#### Ch. 8 — The Art of Being Completely Present (p. 185)

- **Mindfulness in delivery** (p. 185–186) — don't be mentally "somewhere else."
- **Steve Jobs as swordsman** (p. 187–188) — looks effortless because he
  prepares and rehearses like mad. *Mushin no shin* — "the mind that is no mind".
- **Lost in the moment** (p. 189) — Brenda Ueland: play *in* the music,
  not *at* it.
- **Jigoro Kano's five judo principles** (p. 193) as delivery advice:
  (1) Carefully observe yourself, others, the environment; (2) Seize the
  initiative; (3) Consider fully, act decisively; (4) Know when to stop;
  (5) Keep to the middle.
- **Presenting under fire** (p. 194) — a hostile audience is won with
  composure and respect, not aggression.
- **Contribution > impression** (p. 195) — Ben Zander: "We are about
  contribution. That's what our job is."
- **One-buttock playing** (p. 196–197) — Zander: let passion move your body;
  if you're truly in the moment, you can't be a "two-buttock" player. Risk
  making mistakes.
- **Don't take yourself so seriously** (p. 198) — humor as a way out of
  what Rosamund Zander calls the "calculating self".

#### Ch. 9 — Connecting with an Audience (p. 201)

- **Hara hachi bu** (p. 203–204) — "eat until 80% full". Finish 90–95% of
  your allotted time; never run over. Leave the audience just a bit hungry
  for more.
- **Remove barriers** (p. 205) — avoid the lectern/podium where possible;
  stand front and center, near the edge of the stage.
- **Stand, Deliver, Connect** (p. 207) — TED examples: the 18-minute limit
  forces clarity. Hans Rosling shows the "don't stand in front of the
  screen" rule can be broken when you connect energetically with the data.
- **Keep the lights on** (p. 208–209) — the audience must see your face;
  visual cues reinforce auditory ones.
- **Use a remote** (p. 210) — small, simple, just forward / back / black.
  You should never walk back to the laptop.

#### Ch. 10 — The Journey Begins (p. 217)

- There's no quick fix; it's a journey (p. 217).
- Read widely, just do it (Toastmasters), exercise the right brain, get out
  of your comfort zone, learn from your surroundings (p. 218–220).
- Conclusion (p. 221): let **restraint, simplicity, naturalness** be your
  guide.

### Quotes worth remembering

- "Simplicity is the ultimate sophistication." — Leonardo da Vinci, p. 1
- "When forced to work within a strict framework the imagination is taxed
  to its utmost — and will produce its richest ideas." — T. S. Eliot, p. 38
- "If you have the ideas, you can do a lot without machinery. ... Most
  ideas you can do pretty darn well with a stick in the sand." — Alan Kay, p. 49
- "Do only what is necessary to convey what is essential." — Richard Powell
  (*Wabi Sabi Simple*), quoted p. 41
- "Emptiness which is conceptually liable to be mistaken for sheer
  nothingness is in fact the reservoir of infinite possibilities."
  — Daisetz Suzuki, p. 144
- "By stripping down an image to essential meaning, an artist can amplify
  that meaning." — Scott McCloud, p. 112
- "The more strikingly visual your presentation is, the more people will
  remember it. And more importantly, they will remember you." — Paul Arden, p. 162
- "Make everything as simple as possible but no simpler." — Einstein,
  paraphrased p. 104
- "A journey of a thousand miles begins with a single step." — Lao Tzu, p. 222

---

## slide:ology — Nancy Duarte

- **File:** `slide_ology.pdf`
- **Path:** `.claude/skills/slides/material/slide_ology.pdf`
- **Author:** Nancy Duarte
- **Publisher / year:** O'Reilly Media, 2008
- **Type:** Book (PDF, ~270 pages — very image-heavy; most teaching is in
  visual examples, so the PDF rewards browsing the actual pages, not just
  the index)
- **Language:** English
- **Core idea:** Slides are the **last branding frontier** and a high-stakes
  visual medium that most professionals were never trained for. The book is
  *not* a PowerPoint manual — it teaches the timeless principles of visual
  communication: ideate first, design second; treat each slide as a visual
  aid, not a document; learn to think like a designer.

### Contents (chapters)

| Ch. | Title | Page |
|---|---|---|
| — | Introduction | p. xviii |
| 1 | Creating a New Slide Ideology | p. 1 |
| 2 | Creating Ideas, Not Slides | p. 25 |
| 3 | Creating Diagrams | p. 43 |
| 4 | Displaying Data | p. 63 |
| 5 | Thinking Like a Designer | p. 81 |
| 6 | Arranging Elements | p. 91 |
| 7 | Using Visual Elements: Background, Color, and Text | p. 113 |
| 8 | Using Visual Elements: Images | p. 157 |
| 9 | Creating Movement | p. 179 |
| 10 | Governing with Templates | p. 203 |
| 11 | Interacting with Slides | p. 217 |
| 12 | Manifesto: The Five Theses of the Power of a Presentation | p. 251 |
| — | References | p. 263 |
| — | Index | p. 265 |

### Key points

#### Ch. 1 — Creating a New Slide Ideology (p. 1)

- **Career suislide** (p. 2–3) — bad slides quietly damage your career;
  visual communication has become a job requirement, not a bonus.
- **Presentation as the last branding frontier** (p. 4–5) — slides are
  often the final touchpoint before a buying decision, yet companies invest
  millions in ad campaigns and almost nothing in the deck.
- **Document / Teleprompter / Presentation spectrum** (p. 6–7) — pick the
  right format. Rule of thumb:
  - **Document / "slideument":** > 75 words per slide → it's a document;
    treat it as one (circulate as PDF, hold a meeting to discuss).
  - **Teleprompter:** ~50 words per slide → presenter crutch; audience reads
    ahead, presenter turns their back. Avoid.
  - **Presentation:** few words; slides reinforce a spoken message.
  - "The audience will either read your slides or listen to you. They will
    not do both."

#### Ch. 2 — Creating Ideas, Not Slides (p. 25)

- Step away from the software. Brainstorm on paper, sticky notes, or a
  whiteboard before opening PowerPoint/Keynote.
- Identify the **big idea** of the talk in one sentence before designing
  any slide.
- Audience-first thinking: who are they, what do they care about, what do
  you need them to do, think, or feel?

#### Ch. 3 — Creating Diagrams (p. 43)

- Diagrams turn abstract relationships into recognizable shapes (process,
  flow, hierarchy, matrix, segment).
- Pick the diagram type that matches the **relationship in the data**, not
  the one that's most ornate.
- Build complex diagrams in steps (animate in) so the audience follows the
  logic instead of decoding a finished blob.

#### Ch. 4 — Displaying Data (p. 63)

- Choose the chart type that fits the **question**, not the dataset.
- Strip 3-D, gradients, drop shadows, gridlines, and other "chart junk".
- Make the *one number that matters* clearly stand out — color, size, or
  annotation, not five legend entries fighting for attention.

#### Ch. 5 — Thinking Like a Designer (p. 81)

- Designers solve communication problems; they don't decorate. Treat each
  slide like a poster: a single dominant message and a clear visual entry
  point.
- Embrace constraints — limits force creativity (echoes Maeda).

#### Ch. 6 — Arranging Elements (p. 91)

- Layout fundamentals: **flow, hierarchy, contrast, unity, white space,
  proximity, alignment**. The eye should know where to go first, second,
  third.
- Use grids; align everything to invisible lines.
- White space is structural, not leftover.

#### Ch. 7 — Using Visual Elements: Background, Color, and Text (p. 113)

- **Background:** rarely should it compete with content. Solid or subtle
  beats busy.
- **Color:** define a deliberate palette tied to brand and message.
  Use color to *signal*, not to fill space. Account for color blindness and
  for projector accuracy.
- **Text/typography:** pick one or two typefaces and stick to them; use
  weight and size for hierarchy. Type that's easily read at the back of the
  room (rule of thumb: ~24 pt min for body, larger for keywords).

#### Ch. 8 — Using Visual Elements: Images (p. 157)

- Photography, illustration, and video carry emotion words can't.
- Stay away from clip art and "two hands shaking in front of a globe"-style
  stock metaphors.
- Full-bleed images with text laid over empty space tend to outperform
  inset thumbnails.

#### Ch. 9 — Creating Movement (p. 179)

- Animation is for **clarification**, not decoration. Use it to reveal
  parts of a complex idea sequentially, build a chart point by point, or
  emphasize a change.
- Cut spins, dissolves, and bounces.

#### Ch. 10 — Governing with Templates (p. 203)

- Corporate templates often *cause* bad slides. A good template is a
  flexible system (master slides, type scale, color palette, image
  treatments) — not a fill-in-the-blanks form.

#### Ch. 11 — Interacting with Slides (p. 217)

- Be the focal point — the slide is the supporting actor.
- Don't read slides; talk to the audience while the slide reinforces what
  you're saying.
- Practice transitions, pacing, and the use of black slides ("B" key) to
  return attention to you.

#### Ch. 12 — Manifesto: The Five Theses of the Power of a Presentation (p. 251)

Closing manifesto on why presentations matter as a communication form, and
a call to raise the bar.

### Quotes worth remembering

- "We've become the tool of our tools." — Henry David Thoreau, quoted
  in the foreword (p. xii)
- "The best way to paralyze an opposition army is to ship it PowerPoint."
  — attributed to PowerPoint's inventors, quoted in the introduction (p. xviii)
- "Communication is about getting others to adopt your point of view, to
  help them understand why you're excited (or sad, or optimistic, or
  whatever else you are). If all you want to do is create a file of facts
  and figures, then cancel the meeting and send in a report." — Seth Godin,
  quoted p. 6
- "The audience will either read your slides or listen to you. They will
  not do both." — Nancy Duarte, p. 7
- "Every presenter has the potential to be great; every presentation is
  high stakes; and every audience deserves the absolute best." — p. xix

---

## Storytelling with Data — Cole Nussbaumer Knaflic

- **File:** `storytelling_with_data_by_Cole_Nussbaumer_Knaflic.pdf`
- **Path:** `.claude/skills/slides/material/storytelling_with_data_by_Cole_Nussbaumer_Knaflic.pdf`
- **Author:** Cole Nussbaumer Knaflic
- **Publisher / year:** John Wiley & Sons, 2015
- **Type:** Book (PDF, ~270 pages)
- **Language:** English
- **Core idea:** Almost no one is taught how to tell stories *with numbers*.
  This book closes that gap with **six practical lessons** that turn raw
  data into communication that drives a decision. Tool-agnostic; examples
  built in Excel.

### Contents (chapters)

| Ch. | Title | Page |
|---|---|---|
| — | Foreword | p. ix |
| — | Acknowledgments | p. xi |
| — | About the author | p. xiii |
| — | Introduction | p. 1 |
| 1 | The Importance of Context | p. 19 |
| 2 | Choosing an Effective Visual | p. 35 |
| 3 | Clutter is Your Enemy! | p. 71 |
| 4 | Focus Your Audience's Attention | p. 99 |
| 5 | Think Like a Designer | p. 127 |
| 6 | Dissecting Model Visuals | p. 151 |
| 7 | Lessons in Storytelling | p. 165 |
| 8 | Pulling It All Together | p. 187 |
| 9 | Case Studies | p. 207 |
| 10 | Final Thoughts | p. 241 |
| — | Bibliography | p. 257 |
| — | Index | p. 261 |

### The six lessons (book's organizing framework)

Stated explicitly in the introduction (p. 11–12). The first five chapters
each cover one lesson; ch. 7 covers the sixth.

1. **Understand the context** (Ch. 1, p. 19)
2. **Choose an appropriate visual display** (Ch. 2, p. 35)
3. **Eliminate clutter** (Ch. 3, p. 71)
4. **Focus attention where you want it** (Ch. 4, p. 99)
5. **Think like a designer** (Ch. 5, p. 127)
6. **Tell a story** (Ch. 7, p. 165)

### Key points

#### Introduction (p. 1)

- **"Showing data" ≠ "storytelling with data"** — most people stop at the
  first; the gap is what this book closes.
- **Tools don't know your story** (p. 13) — Excel/Tableau will produce a
  default chart; *you* must add context, ordering, color, and annotation.
- The classic before/after pattern (p. 4–6, Figures 0.2–0.7) — same data,
  rethought with the six lessons, becomes a clear recommendation.

#### Ch. 1 — The Importance of Context (p. 19)

- **Exploratory vs. explanatory** — exploratory analysis is for *you*;
  explanatory communication is for *them*. Most communication mistakes
  come from showing exploratory work to an explanatory audience.
- **Who, what, how** — three questions to answer before you build anything:
  Who is the audience? What do you need them to know or do? How will you
  use the data to make the case?
- **The 3-minute story and the Big Idea** — be able to state the takeaway in
  one breath and one sentence.

#### Ch. 2 — Choosing an Effective Visual (p. 35)

Knaflic's go-to chart types — most problems are solved by a small set:

- **Simple text** (a single big number with context).
- **Table** — when the audience will read across rows; never put a table
  on a live slide for live commentary.
- **Heatmap** — table where color encodes magnitude.
- **Line chart** (continuous data, especially time series).
- **Slopegraph** — two-point line for before/after comparison.
- **Bar chart** (vertical or horizontal) — the workhorse; baseline must
  start at zero.
- **Stacked bar / 100% stacked bar** — use sparingly; comparisons across
  stacks get hard.
- **Waterfall** — for showing how a starting value becomes an ending value.
- **Square area chart** — for huge magnitude differences.
- **Avoid:** pie charts, donut charts, secondary y-axes, 3-D anything.

#### Ch. 3 — Clutter is Your Enemy! (p. 71)

- **Cognitive load** — every element on a slide costs the viewer mental
  energy. Strip what isn't doing work.
- **Gestalt principles** for visual perception: proximity, similarity,
  enclosure, closure, continuity, connection. Use them to group and
  separate without adding ink.
- **Alignment** and clean **white space** do the structural work that
  borders, gridlines, and shading otherwise try (and fail) to do.
- **Kill** chart borders, redundant labels, default gridlines, dual axes,
  diagonal axis labels.

#### Ch. 4 — Focus Your Audience's Attention (p. 99)

- **Pre-attentive attributes** — size, color, position, intensity. The eye
  notices these *before* conscious thought; use them, sparingly, to point
  at the one thing that matters.
- **Color is your most powerful tool — and your most overused.** Default
  to grey; reserve a single accent color for the point you want made.
- **The "where are your eyes drawn?" test** — squint at your chart. If
  the answer isn't your main point, redesign.

#### Ch. 5 — Think Like a Designer (p. 127)

- **Form follows function** — design serves communication, not aesthetics.
- **Affordances** — visual cues that signal what the chart is "for"
  (titles, labels, annotations).
- **Accessibility** — text at readable size, no color-only encoding,
  plain language.
- **Aesthetics** — clean layout earns trust; messy layout costs
  credibility.
- **Acceptance** — bring stakeholders along; explain *why* you simplified.

#### Ch. 6 — Dissecting Model Visuals (p. 151)

Five worked-through "model" charts where Knaflic narrates her design
choices step by step. Read this chapter for *thinking out loud* over real
examples.

#### Ch. 7 — Lessons in Storytelling (p. 165)

- Borrows from screenwriting and Aristotle: **plot → twists → end**
  (setup, conflict/tension, resolution).
- **Narrative flow** — written narrative for documents, spoken narrative
  for live talks; both need a clear arc.
- **Repetition** — use it deliberately; restate the takeaway when you
  open, when you transition, when you close.
- **Tactics for live presentations:** pacing, signposting, calls to action.

#### Ch. 8 — Pulling It All Together (p. 187)

End-to-end walkthrough of one analysis from raw data to final
recommendation, applying all six lessons in sequence.

#### Ch. 9 — Case Studies (p. 207)

Real before/afters across industries (tech, education, consumer products,
nonprofit). The richest section for "what does this look like in my
domain?"

#### Ch. 10 — Final Thoughts (p. 241)

- Closing call: rid the world of bad data viz, one chart at a time.
- Practice deliberately, seek feedback, build and iterate.

### Quotes worth remembering

- "Power Corrupts. PowerPoint Corrupts Absolutely." — Edward Tufte, quoted
  on p. ix
- "Don't be a data fashion victim." / "Simple beats sexy." — Cole's mantras
  at Google, paraphrased in the foreword (p. x)
- "There is a story in your data. But your tools don't know what that story
  is." — p. 3
- "The audience will either read your slides or listen to you." — paraphrase
  shared with Duarte, p. 7

