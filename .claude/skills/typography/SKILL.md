---
name: typography
description: Apply professional-grade typography to UI/frontend design. Use when selecting fonts, building type scales, setting line-height/tracking/spacing, or when the user asks about typography, font pairing, or wants to avoid generic AI aesthetics in text-heavy interfaces.
---

# Typography

This skill governs every typographic decision in a UI: font selection, scale, spacing, and micro-typography. The goal is interfaces with a distinct voice — not generic defaults.

## 1. Font Selection — Anti-Slop Rules

**NEVER** use: Inter, Roboto, Open Sans, Arial, system-ui, Space Grotesk, or any other "AI default" font. These signal zero creative effort.

**DO** select fonts based on the aesthetic direction:

| Tone | Font Category | Examples |
|---|---|---|
| Luxury / Editorial | High-contrast Serif | Bodoni, Garamond, Playfair Display |
| Industrial / Utilitarian | Heavy Grotesque or Monospace | JetBrains Mono, Barlow Condensed |
| Modern / Contemporary | Geometric or Neo-Grotesque | Neue Haas Grotesk, DM Sans, Outfit |
| Retro / Expressive | Slab Serif or Display | Rokkit, Zilla Slab, Abril Fatface |
| Swiss / Precise | Neo-Grotesque | Aktiv Grotesk, Hanken Grotesk |

**Pairing rule**: Use at most 2 fonts. Pair across categories — a high-contrast Serif display font + a clean Sans body font. If using one font, vary by weight instead.

**Display fonts** (Bodoni, Abril, etc.) are for H1–H2 only. Never use them for body text.

**Always explain the choice**: When selecting a font, state why — e.g. "Choosing Playfair Display for its editorial tension between thick and thin strokes, evoking a 1980s magazine."

## 2. Type Scale

Use a **mathematical ratio**, not arbitrary sizes. Define as CSS variables.

Recommended ratios:
- **Major Third (1.250)**: Subtle, refined — good for dense UIs
- **Augmented Fourth (1.414)**: Dramatic contrast — good for editorial/hero layouts
- **Perfect Fifth (1.500)**: High contrast — use sparingly for very expressive designs

```css
/* Example: Major Third (1.250) base 16px */
--text-xs:   0.64rem;   /* ~10px */
--text-sm:   0.8rem;    /* ~13px */
--text-base: 1rem;      /* 16px  */
--text-lg:   1.25rem;   /* ~20px */
--text-xl:   1.563rem;  /* ~25px */
--text-2xl:  1.953rem;  /* ~31px */
--text-3xl:  2.441rem;  /* ~39px */
--text-4xl:  3.052rem;  /* ~49px */
```

Minimum body text: **1rem (16px)**. Never go below 0.875rem (14px) for any readable content.

## 3. Weight Contrast — Skip a Weight

Never pair adjacent weights (Regular + Medium). The difference is invisible.

**Skip at least one step:**
- Light (300) → Bold (700) ✅
- Regular (400) → Extra Bold (800) ✅
- Regular (400) → Medium (500) ✗

For buttons: use a heavier weight than body text, then compensate with slightly increased `letter-spacing`.

## 4. Inverse Spacing Laws

These rules are the mark of professional typography.

### Line Height (Leading)
Inversely proportional to font size:

| Text Size | Line Height |
|---|---|
| Hero titles (3xl+) | 1.0–1.1 |
| Headings (xl–2xl) | 1.15–1.25 |
| Subheadings (lg) | 1.3–1.4 |
| Body text (base) | 1.5–1.65 |
| Small/caption (sm) | 1.6–1.75 |

### Letter Spacing (Tracking)
Also inversely proportional:

| Text Size | Letter Spacing |
|---|---|
| Hero titles | `-0.02em` to `-0.04em` |
| Headings | `-0.01em` to `-0.02em` |
| Body text | `0` (default) |
| Small caps / labels | `+0.05em` to `+0.1em` |
| All-caps labels | `+0.08em` to `+0.15em` |

Tight tracking on large text makes it feel "designed". Positive tracking on small/caps text prevents bleeding.

## 5. Line Length & Alignment

**The Measure**: Body text should be **45–75 characters** per line (roughly 10–14 words). Use `max-width: 65ch` as a sensible default.

**Alignment**: Left-align all body text (for LTR languages). Never center large paragraphs — it breaks the eye's vertical anchor.

Center alignment is acceptable for: short headlines, captions, CTAs, and UI labels only.

**Clean the Rag**: Review the ragged right edge of left-aligned text. Avoid shapes that look like stairs or have a single very short line.

**Widows & Orphans**:
- Widow: a single word alone on the last line of a paragraph — avoid with `text-wrap: balance` or manual `<br>` on headings
- Orphan: first line of a paragraph isolated at bottom of a column — fix with `orphans: 2` in CSS

```css
h1, h2, h3 {
  text-wrap: balance; /* prevents ugly single-word last lines */
}

p {
  orphans: 2;
  widows: 2;
}
```

## 6. Accessibility

- **Body text contrast**: minimum 4.5:1 (WCAG AA)
- **Large text (18px+ bold or 24px+)**: minimum 3:1
- **Target**: 7:1 for small text whenever the aesthetic allows
- **Never** embed text in images — always use real HTML/CSS text

## 7. Micro-Typography Checklist

Before finalizing any typographic implementation:

- [ ] No generic/AI-default fonts used
- [ ] Font choice explained in context of aesthetic direction
- [ ] Type scale uses a mathematical ratio with CSS variables
- [ ] Weight contrast skips at least one step
- [ ] Line heights follow inverse proportionality
- [ ] Letter spacing follows inverse proportionality (negative on large, positive on small/caps)
- [ ] Body text max-width set (~65ch)
- [ ] `text-wrap: balance` on headings
- [ ] `orphans: 2; widows: 2` on paragraphs
- [ ] Contrast ratios meet WCAG AA minimum
- [ ] Buttons use heavier weight + slightly increased tracking
- [ ] All text is real HTML — no text-as-image

## 8. Font Sources

Prefer: Google Fonts (free), Bunny Fonts (privacy-first), Adobe Fonts (if available), or self-hosted variable fonts.

For variable fonts, use `font-variation-settings` to access intermediate weights and reduce HTTP requests.

```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=DM+Sans:wght@300;400;700&display=swap');
```
