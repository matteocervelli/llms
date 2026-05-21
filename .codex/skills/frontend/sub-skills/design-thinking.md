# Design Thinking Framework

## Purpose

Establish a consistent foundation before implementing any visual design. This pre-coding phase ensures design choices are deliberate, contextual, and aligned with the product's core identity.

## The 4 Pillars

### 1. Purpose

Define why the design exists and what problem it solves.

- What is the core mission of this product/page?
- Who benefits from this design?
- What emotion or action should it evoke?

**Worksheet:**

```
Product Purpose: ________________________________
Target Benefit: ________________________________
Desired Emotion: ________________________________
Success Metric: ________________________________
```

### 2. Tone

Establish the personality and voice through visual language.

- Is it playful, serious, minimal, ornate, cutting-edge, timeless?
- How does tone influence font choice, color, motion, spacing?
- Should the design feel premium, approachable, trustworthy, innovative?

**Tone Dimensions:**

- Formal ↔ Casual
- Minimal ↔ Ornate
- Modern ↔ Classic
- Warm ↔ Cool
- Energetic ↔ Calm

### 3. Constraints

Understand the structural and brand limitations.

- What brand guidelines must be respected?
- What technical constraints exist (browser support, performance, accessibility)?
- What audience demographics and cultural contexts apply?
- Are there content or functionality requirements?

**Worksheet:**

```
Brand Requirements: ________________________________
Technical Limits: ________________________________
Audience: ________________________________
Content Structure: ________________________________
```

### 4. Differentiation

Identify what makes this design distinctive vs competitors.

- What visual elements will stand out in the market?
- What conventions will be broken intentionally?
- What unexpected details create delight?
- How does this reflect the brand's unique value?

**Worksheet:**

```
Competitor Visual Patterns: ________________________________
Intentional Breaks: ________________________________
Delightful Details: ________________________________
Unique Value Reflection: ________________________________
```

## Workflow

1. **Define** (5 minutes): Answer all 4 pillars explicitly
2. **Research** (10 minutes): Study competitors, cultural aesthetics, mood boards
3. **Sketch** (10 minutes): Low-fidelity exploration of concept
4. **Validate** (5 minutes): Does the direction align with all 4 pillars?
5. **Implement** (apply the 5 design dimensions)

## Pre-Implementation Checklist

- [ ] Purpose statement written and agreed upon
- [ ] Tone personality clearly defined
- [ ] All constraints documented
- [ ] Differentiation strategy identified
- [ ] Mood board or reference designs collected
- [ ] Typography direction sketched (not fonts yet, but pairing philosophy)
- [ ] Color philosophy established (not palette yet, but dominant/accent concept)

## Output Artifact

Create a brief **Design Brief** (1 page max):

```
## DESIGN BRIEF

**Product**: [Name]
**Purpose**: [Core Mission]
**Target Tone**: [Personality]
**Key Constraint**: [What limits us]
**Differentiation**: [What makes us unique]
**Color Philosophy**: [Dominant/Accent concept]
**Typography Philosophy**: [Pairing philosophy]

## Working Model

**Visual thesis**: [One sentence: mood, material, energy — e.g. "warm editorial luxury with quiet restraint"]
**Content plan**: Hero → [what it shows] → Support → [proof point] → Detail → [depth] → CTA → [action]
**Interaction thesis**: [2-3 motion ideas — e.g. "hero parallax, section reveals, hover shimmer on CTA"]
```

The Working Model answers: what does this _feel_ like before you write a line of code?
It prevents dimension-by-dimension work from producing a technically correct but tonally incoherent result.

This brief guides all subsequent dimension-specific work.

---

**Next Steps**: With design thinking established, proceed to the 5 dimensions:

- Typography (visual hierarchy and distinctive pairing)
- Color Theme (emotional depth and accessibility)
- Motion (orchestrated reveals and interaction)
- Spatial Composition (layout and intentional asymmetry)
- Backgrounds (atmospheric depth and visual interest)

## Persist to .design/system.md

After completing the Design Brief, create or update `.design/system.md` in the project root:

```markdown
# Design System — [project name from Design Brief]

> Auto-maintained by /frontend design. Commit this file. Load at session start.

## Mode

[brand | product]

## Identity

- Purpose: [one sentence from Design Brief]
- Tone: [3-5 adjectives from Design Brief]
- Differentiation: [the unforgettable element]

## Typography

- Display: [font, weight]
- Body: [font, weight]
- Mono: [font, weight if applicable]
- Scale: [display]px / [headline]px / [sub]px / [body]px / [caption]px

## Color

- Primary: [name] [#hex]
- Accent: [name] [#hex]
- Neutral: [warm|cool] — [range description]
- Background: [hex or description]

## Spacing

- Grid: [8px | 4px]
- Scale: [comma-separated values]

## Depth

- Treatment: [shadows | borders | flat]
- Card shadow: [description or CSS snippet]

## Motion

- Easing: [function]
- Enter: [ms]
- Exit: [ms]
- Stagger: [ms]

## Decisions Log

<!-- Append-only. Record non-obvious choices and their rationale. -->

- [today's date] Initial design system created from Design Brief
```
