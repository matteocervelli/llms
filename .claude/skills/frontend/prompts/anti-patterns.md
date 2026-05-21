# Anti-Patterns: What to Avoid

## Overview

These are the predictable defaults that appear in generic AI-generated design. Actively rejecting these patterns is the first step toward intentional design.

## Mode

Some patterns apply differently by design mode:

- **(brand)** — marketing pages, landing pages, portfolios, editorial
- **(product)** — app UI, dashboards, admin panels, tools
- **(both)** — applies universally; no tag = both

In **brand mode**, prioritize: personality, differentiation, emotional impact, dramatic hierarchy.
In **product mode**, prioritize: clarity, information density, consistency, functional hierarchy.

## Typography Anti-Patterns (both)

### Generic Font Choices

**Avoid**:

```
- Inter for everything (default AI choice)
- Roboto for everything (default Android)
- Open Sans for everything (neutral = forgettable)
- Lato for everything (too friendly, lacks edge)
- System fonts (-apple-system, system-ui)
```

**Result**: Immediately reads as "default AI design," no personality.

### Incremental Size Jumps

**Avoid**:

```
H1: 48px
H2: 40px (83% of H1 - feels too close)
H3: 32px (80% of H2 - still feels similar)
Body: 16px (50% jump is jarring)
```

**Better**:

```
Display: 88px (5.5x body)
Headline: 48px (3x body)
Sub: 28px (1.75x body)
Body: 16px (1x)
Caption: 12px (0.75x body)
```

### Mid-Range Font Weights Only

**Avoid**:

```
- Using only weights 400, 500, 600 (all feel samey)
- No visual distinction between hierarchy levels
- Everything feels medium-weight
```

**Better**:

```
- Display: 300 or 700
- Body: 400
- Emphasis: 800/900
- Creates real visual contrast
```

### Overused "Trendy" Fonts (both)

**Avoid** (these cycle through AI-generated sites in waves):

```
- Fraunces (quirky serif — overused in "playful brand" contexts)
- Geist / Geist Mono (Vercel ecosystem default)
- Mona Sans (GitHub's open-source face — everywhere in dev tools)
- Plus Jakarta Sans (rounded friendly sans — SaaS default since 2023)
- Recoleta (retro-friendly serif — used on every "warm" brand)
- Instrument Sans (Google variable font — the new Inter)
```

**Note**: These fonts are fine as secondary or body faces when paired with a distinctive display face. The anti-pattern is using them as the sole typeface or as the display face.

## Color & Theme Anti-Patterns (both)

### Cliché Color Schemes

**Avoid**:

- **Material Design Trinity**: Blue, Red, Green as primary, secondary, accent
- **Default SaaS Colors**: Cool blues (#0099ff, #0066cc) everywhere
- **Rainbow Palette**: Every color at full saturation
- **Pure Grays**: #999999, #CCCCCC without personality
- **Inverted Black/White**: No mid-tones or color

**Identifies as**: "I used the default design system"

### Monochrome Everything

**Avoid**:

```
Background: #f5f5f5
Text: #333333
Accent: #0099ff
All grays in between
```

**Result**: Feels corporate and soulless.

### Oversaturated Accent Colors

**Avoid**:

```
- Neon colors at 100% saturation
- Colors that don't exist in real life
- Accents that compete with content
```

### Predictable "Dark Mode"

**Avoid**:

```
Light mode: White background, black text
Dark mode: Black background, white text (inverted)
No color adjustments, just inversion
```

**Result**: Dark mode feels like a checkbox feature, not intentional.

### Purple Gradients and Gradient Text (brand)

**Avoid**:

- Purple-to-blue or purple-to-pink hero gradients (the "AI startup" look)
- `background-clip: text` gradient fills on headings (every AI landing page)
- Gradient text as the primary visual signature

**Result**: Immediately reads as "we used AI to design this."

### AI-Generated Color Palettes (both)

**Avoid**:

- Palettes that feel algorithmically balanced (equal saturation across all hues)
- Coolors.co / AI-suggested palettes used without modification
- Any palette where all colors sit at the same lightness/saturation band

**Better**: Start from one real-world color reference (a photo, a material, a place) and derive the palette from that anchor.

## Layout & Spatial Anti-Patterns (both)

### Cookie-Cutter Centered Layout

**Avoid**:

```
- Everything centered
- Symmetrical on both sides
- Predictable grid alignment
- "Stacked boxes" arrangement
```

**Reads as**: "Default SaaS dashboard"

### Uniform Padding Everywhere

**Avoid**:

```
- Same padding on all elements
- No variation in spacing
- Everything feels equally distant
- No visual hierarchy through space
```

### Predictable Component Patterns

**Avoid**:

- Card with image on top, text below (default layout)
- 3-column grid (most common layout)
- Left sidebar + right content (standard pattern)
- Center-aligned everything

### Nested Card Layouts — "Cardocalypse" (both)

**Avoid**:

- Cards inside cards inside cards
- Every piece of content wrapped in its own card container
- Card as the default layout primitive for all content types

**Result**: Depth signals compete with each other. Nothing has real elevation.

### Side-Stripe Border Cards (product)

**Avoid**:

```css
.card {
  border-left: 4px solid var(--accent);
}
```

- Colored left-border as the sole visual differentiation between card types
- Overused in dashboards, notification systems, and sidebars

### Body Text Running to Viewport Edges (both)

**Avoid**:

- Paragraphs without a `max-width` constraint (~75ch is the optimal reading width)
- Text that fills the full viewport on wide screens
- No visual container or column constraint for body copy

## Motion & Animation Anti-Patterns (both)

### Linear Timing on Everything

**Avoid**:

```css
.element {
  transition: all 0.3s linear;
}
```

**Result**: Feels robotic and mechanical.

### No Animation at All

**Avoid**:

- Instant page loads (feels cold)
- No hover feedback (feels broken)
- Transitions that snap instantly

### Animation-Heavy Design

**Avoid**:

- Animating every element on the page
- Multiple simultaneous animations (chaos)
- Animation that distracts from content
- Auto-playing animations (annoying)

### Slow, Sluggish Motion

**Avoid**:

```css
.element {
  transition: all 2s linear;
}
```

**Result**: Feels like the app is struggling to load.

## Background & Visual Details Anti-Patterns (both)

### Bland White Background

**Avoid**:

- Pure white (#ffffff) with no texture
- No variation or personality
- Feels institutional and cold

### Obvious Gradients

**Avoid**:

- Rainbow gradients (kitsch)
- High-contrast gradients (0% to 100%)
- Gradients at 45° angle (default direction)
- Multiple competing gradients

**Better**:

- Subtle 2-3 color gradients
- Minimal contrast (40-60° angles)
- Gradients that support, not distract

### Busy, Distracting Patterns

**Avoid**:

- Patterns with high contrast
- Patterns that compete with content
- Repeated small patterns that feel cheap
- Patterns that serve no purpose

### Generic Illustration Style

**Avoid**:

- Adobe Illustrator default symbols
- 3D isometric cubes (overused)
- Flat unshaded circles and rectangles
- Placeholder illustration libraries

## Copy & Content Anti-Patterns (both)

### Generic Placeholder Text

**Avoid**:

```
"Lorem ipsum dolor sit amet..."
"[Your title here]"
"Learn more →"
"Click here"
```

### Cliché Microcopy

**Avoid**:

```
"Elevate your experience"
"Seamlessly integrated"
"Cutting-edge technology"
"Game-changing solution"
"Synergize your workflow"
```

### Vague CTAs

**Avoid**:

- "Submit"
- "Click here"
- "Go"
- "Next"

**Better**:

- "Start free trial"
- "Build my design"
- "Claim your spot"
- "See what's possible"

## Visual Hierarchy Anti-Patterns (both)

### Everything Emphasized Equally

**Avoid**:

```
- Same font size for everything important
- Multiple colors of equal weight
- All elements at same contrast level
- No clear visual entry point
```

### Lack of Contrast

**Avoid**:

- Light gray text on light background
- Similar colors throughout
- No visual distinction between states
- Weak hierarchy signals

### Italic-Serif Display Heroes (brand)

**Avoid**:

- Large italic serif text as the sole hero element
- Playfair Display Italic as the entire personality of a page

**Result**: Reads as "fancy AI template."

### Hero Eyebrow Chips (brand)

**Avoid**:

- Small uppercase label in a pill/chip above the headline ("NEW", "INTRODUCING", "BETA")
- Rounded-full pill with accent background as the first element users see

**Result**: Every SaaS landing page since 2022.

## Structural Anti-Patterns (brand)

### Symmetrical Everything

**Avoid**:

- Everything centered
- Perfect mirroring on left/right
- Predictable alignment

**Better**:

- Asymmetrical compositions
- Off-center focal points
- Unexpected alignment

### Standard "Above The Fold" Design

**Avoid**:

```
Hero section with centered headline and CTA
Followed by 3-column feature cards
Testimonials section
Footer
```

**Result**: Could describe every SaaS landing page.

## Interactive Anti-Patterns (both)

### Hover States That Do Nothing

**Avoid**:

- Links without underline on hover
- Buttons that don't give feedback
- No visual indication of interactivity

### Predictable Micro-interactions

**Avoid**:

- Button scale 1.05 on hover (everyone does this)
- Color change with no other feedback
- Opacity change only

**Better**:

- Unexpected animation (rotate, shimmer)
- Transform + shadow + color shift
- Delightful easter eggs

## Surface Treatment Anti-Patterns (both)

### Thick Borders as Primary Depth

**Avoid**:

- `border: 2px solid` or thicker as the primary depth mechanism on cards and panels
- Borders on every interactive element
- Thick borders instead of layered `box-shadow` (see `ui-polish.md`)

**Better**: Use layered box-shadow for depth — it adapts to any background.

### Glassmorphism as Primary Aesthetic

**Avoid**:

- `backdrop-filter: blur()` with semi-transparent backgrounds as the signature design element
- Frosted-glass cards where there's no strong background visual to blur against

**Result**: Peaked in 2021-2022, now reads as dated trend-following.

## Checklist: Have You Avoided These?

- [ ] Rejected Inter, Roboto, Open Sans as primary fonts?
- [ ] Chosen typefaces with personality and intention?
- [ ] Used size jumps of 3x+, not incremental scaling?
- [ ] Avoided Material Design color trinity?
- [ ] Created custom color palette with personality?
- [ ] Rejected centered, symmetrical layouts?
- [ ] Used easing functions, not linear timing?
- [ ] Added motion that serves a purpose?
- [ ] Avoided generic gradients and patterns?
- [ ] Would you describe this as "generic" or "intentional"?
- [ ] No purple gradient or gradient-text headings?
- [ ] No nested cards (card inside card — cardocalypse)?
- [ ] No side-stripe border cards?
- [ ] Body text constrained to ~75ch max width?
- [ ] No hero eyebrow chip/pill?
- [ ] No thick-border-only depth treatment (use layered shadows instead)?
- [ ] No glassmorphism as primary aesthetic?

## When You Break These Rules

It's okay to use a "forbidden" pattern if you do it intentionally:

**✓ Good**: "I used Inter because I paired it with Playfair Display and added custom color system"
**✓ Good**: "I used a blue accent because it's unexpected in this context"
**✓ Good**: "I centered the layout because the content demands symmetry"

**✗ Bad**: Justifying generic choices by saying "that's what the default is"

## The Real Rule

**Don't make decisions because they're default. Make decisions because they're right for your design.**

If you're choosing a typeface, color, layout, or animation because it's the easiest option, you're designing like an AI. Choose deliberately instead.
