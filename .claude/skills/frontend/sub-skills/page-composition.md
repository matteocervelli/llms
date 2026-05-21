# Page Composition

## Purpose

Where the other dimensions (typography, color, motion, spatial) define _how_ elements look,
page composition defines _what goes where_ and _why_. This is the layer that separates
a collection of polished elements from a coherent page.

## Landing Page Narrative Sequence

Every landing page is a story. Default to this sequence:

1. **Hero** — establish identity and promise (brand, headline, image, CTA)
2. **Support** — one concrete feature, offer, or proof point
3. **Detail** — atmosphere, workflow, product depth, or story
4. **Social proof** — establish credibility (testimonials, logos, numbers)
5. **Final CTA** — convert interest into action

Do not skip stages. Do not merge stages. Each section has one job.

## Hero Rules

The hero is a poster, not a document. These rules are non-negotiable on branded landing pages:

**Viewport budget** — the first screen must contain only:

- The brand or product name (loudest text)
- One headline (2-3 lines on desktop)
- One short supporting sentence
- One CTA group (primary + optional secondary)
- One dominant visual (full-bleed image or visual plane)

Anything else — stats, schedules, logo clouds, pill clusters, promo stickers — belongs in later sections.

**Full-bleed visual** — hero image runs edge-to-edge with no inherited page gutters, framed container,
or shared max-width. Constrain only the inner text/action column.

**Viewport math** — if using `100vh`/`100svh` with a sticky header, always subtract header height:

```css
.hero {
  height: calc(100svh - var(--header-height));
}
/* or overlay the header instead of stacking it in normal flow */
```

**Brand hierarchy** — brand or product name must be the dominant visual signal, not just nav text.
A headline should never overpower the brand name on a branded page.

**Banned in the hero**: inset/side-panel/rounded-card heroes, floating badges/stickers/info chips,
hero dashboards, tiled collages, stat strips, address blocks, event listings, logo clouds.

## Brand Hierarchy Test

Apply this after building the first viewport:

> Remove the navigation bar. If the first viewport could now belong to a different brand,
> the branding is too weak. Strengthen the brand signal before proceeding.

## Card Philosophy

**Default: no cards.**

Cards are allowed only when the card _is_ the interactive unit (clicking/selecting the card itself
does something meaningful). If removing the border, shadow, background, or radius does not hurt
the user's ability to interact or understand, it is not a card — it is content wearing card clothes.

Apply this test before adding any card treatment:

> "If I remove the border, shadow, and background-color from this card, does the user lose
> the ability to interact or understand what they're looking at?"
>
> - No → do not use a card. Use sections, columns, dividers, or media blocks instead.
> - Yes → a card is justified here.

Cards are **never** appropriate in the hero, regardless of the brief.

## Section Discipline

Each section gets exactly:

- One purpose
- One dominant visual idea
- One headline (or a clear primary label)
- One short supporting sentence (optional but constrained)
- One primary takeaway or action

A section that needs multiple competing text blocks, icon rows, or nested callouts has not been
sufficiently scoped. Split it or cut it.

## App UI vs Landing Page

These are different surfaces with different rules:

| Surface                  | Goal                | Copy style                     | Card usage                   |
| ------------------------ | ------------------- | ------------------------------ | ---------------------------- |
| Landing page / marketing | Convert or inform   | Aspirational, brand voice      | None by default              |
| Dashboard / product UI   | Operate and monitor | Utility: status, action, scope | Only when card = interaction |

**For app UI** — default to calm surface hierarchy:

- dense but readable
- strong typography and spacing
- minimal chrome
- few colors, one clear accent for action/state

**For app UI copy** — if a heading could appear in a homepage hero or ad, rewrite it.
Good app headings: "Selected KPIs", "Plan status", "Top segments", "Last sync".
Bad app headings: "Unlock your potential", "Seamlessly integrated insights".

Litmus: if an operator scans only headings and labels, can they immediately understand what to do?

## Hard Rules

- No hero cards, ever.
- No center-column hero when full-bleed is appropriate.
- No stat strips, pill clusters, or logo clouds in the hero.
- No section should contain multiple competing text blocks.
- No headlines that overpower the brand on branded pages.
- No filler copy. If a sentence adds no information, delete it.
- No split-screen hero unless text sits on a calm, unified side of the image.
