# UI Polish — Micro-Details That Make Interfaces Feel Better

## Core Philosophy

Great interfaces rarely come from one thing. It's a collection of small, compounding details that
separate "functional" from "crafted." These patterns operate below the macro design layer — they
apply after typography, color, motion, and spatial decisions are made.

Apply this pass after Phases 2–6. Work through each category and check what's missing.

---

## Typography Polish

### Text Wrapping — Prevent Orphaned Words

A single word on the last line of a heading looks accidental.

```css
/* Distribute text evenly across lines */
h1,
h2,
h3,
p {
  text-wrap: balance;
}

/* Alternative: slower algorithm, also prevents orphans */
p {
  text-wrap: pretty;
}
```

Tailwind: `text-balance`, `text-pretty`

**When to use:** Headings and short paragraphs. Avoid on long body text (performance cost).

---

### Font Smoothing — Crisper Text on macOS

Default subpixel rendering makes text appear heavier than intended on macOS, especially for light
text on dark backgrounds.

```html
<body class="font-sans antialiased"></body>
```

```css
body {
  -webkit-font-smoothing: antialiased;
}
```

Tailwind: `antialiased` on `<body>` or layout root.

**When to use:** Always. Apply once at the layout root — it cascades to all text.

---

### Tabular Numbers — Prevent Shifting Digits

Numbers in counters, prices, or tables shift horizontally as values change because digits have
different widths by default.

```css
.counter,
.price,
td {
  font-variant-numeric: tabular-nums;
}
```

Tailwind: `tabular-nums`

**When to use:** Any number that updates dynamically or sits in a column. Note: Inter changes
numeral style when this property is applied — test visually.

---

## Spacing Polish

### Concentric Offset — Correct Nested Border Radii

When nesting a rounded element inside another, the inner radius should always be smaller than the
outer. The formula is simple:

```
outer_radius = inner_radius + padding
```

```css
.card {
  border-radius: 20px; /* outer */
  padding: 8px;
}

.card-inner {
  border-radius: 12px; /* = 20 - 8 */
}
```

Mismatched radii (e.g. both 12px when padding is 8px) is one of the most common unpolished details
in production interfaces. Fix it wherever elements are nested.

**When to use:** Buttons with icons, cards with image thumbnails, modals with inner panels.

---

### Optical Alignment — Geometric Isn't Always Correct

Geometric centering can look off-center to the eye, especially with icons and mixed-content buttons.
Compensate with small margin or padding adjustments.

```css
/* Geometric alignment (looks right-heavy with a Play icon) */
.btn {
  padding: 8px 12px;
}

/* Optical alignment (slightly less padding on icon side) */
.btn {
  padding: 8px 10px 8px 12px;
}
```

For SVG icons, fix it directly in the SVG `viewBox` so no extra CSS is needed.

**When to use:** Buttons with icons, icon-only buttons (triangles, arrows), mixed-weight text.

---

## Depth Polish

### Shadow as Border — Layered `box-shadow`

Solid borders break on non-white backgrounds. A three-layer `box-shadow` adapts to any background
because it uses transparency.

```css
/* Light mode — three layers: outline ring + close shadow + far shadow */
.card {
  box-shadow:
    0px 0px 0px 1px rgba(0, 0, 0, 0.06),
    0px 1px 2px -1px rgba(0, 0, 0, 0.06),
    0px 2px 4px 0px rgba(0, 0, 0, 0.04);
}

/* Light mode hover — same layers, slightly darker */
.card:hover {
  box-shadow:
    0px 0px 0px 1px rgba(0, 0, 0, 0.08),
    0px 1px 2px -1px rgba(0, 0, 0, 0.08),
    0px 2px 4px 0px rgba(0, 0, 0, 0.06);
  transition-property: box-shadow;
  transition-duration: 200ms;
}

/* Dark mode — depth shadows don't show on dark backgrounds, simplify to a single white ring */
@media (prefers-color-scheme: dark) {
  .card {
    box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.08);
  }
  .card:hover {
    box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.13);
  }
}
```

Three layers create: outline ring (depth 0) + close shadow + far shadow. The combination reads as a
border but with natural depth. In dark mode, only the ring layer is visible so simplify to one.

**Do not apply** to dividers or layout separators — those should stay as `border`. Shadows are for
elements that need depth or sit on varied backgrounds.

**When to use:** Cards, inputs, dropdowns, images — any element that needs a border on variable
backgrounds.

---

### Image Outline Overlay — Consistent Edge Depth

Images on complex backgrounds can lose their edge. A 1px inset outline adds just enough definition.

```css
.image-with-border {
  outline: 1px solid rgba(0, 0, 0, 0.1);
  outline-offset: -1px; /* inset — doesn't add to layout */
}

@media (prefers-color-scheme: dark) {
  .image-with-border {
    outline-color: rgba(255, 255, 255, 0.1);
  }
}
```

**Color rule (non-negotiable):** Use pure `rgba(0,0,0,0.1)` in light mode and pure
`rgba(255,255,255,0.1)` in dark mode. Never use tinted neutrals (slate-900, zinc-900, `#111827`,
`#0a0a0a`). Tinted outlines pick up the surrounding surface hue and look like dirt on the image edge.

Why `outline` instead of `border`: `outline` doesn't affect layout dimensions, and `outline-offset: -1px`
keeps the stroke inset so images stay their intended size.

Tailwind: `outline outline-1 -outline-offset-1 outline-black/10 dark:outline-white/10`

**When to use:** Photos, avatars, cards with image thumbnails. Works best in design systems where
other elements also use borders — it creates visual consistency.

---

## Motion Polish

### CSS Transitions vs Keyframe Interruptibility

These behave differently when interrupted mid-animation:

- **`transition`** — interpolates toward the latest state. If you interrupt, it smoothly retargets.
- **`@keyframes`** — runs on a fixed timeline. Interrupting restarts or glitches.

```css
/* Interruptible — good for hover, toggle, open/close */
.panel {
  transition:
    transform 300ms ease-out,
    opacity 300ms ease-out;
}

/* Not interruptible — good for staged sequences that run once (loaders, onboarding) */
.loader {
  animation: spin 1s linear infinite;
}
```

**Rule of thumb:** Use `transition` for anything users can trigger repeatedly. Use `@keyframes` for
sequences that run once and complete.

---

### Icon State Transitions — opacity + scale + blur

Swapping icons abruptly (e.g. copy → check) feels jarring. Animate the transition with three
properties simultaneously.

```css
.icon-enter {
  animation: icon-in 200ms ease-out both;
}

@keyframes icon-in {
  from {
    opacity: 0;
    scale: 0.7;
    filter: blur(4px);
  }
  to {
    opacity: 1;
    scale: 1;
    filter: blur(0px);
  }
}
```

With Framer Motion / Motion:

```tsx
<motion.div
  key={isCopied ? "check" : "copy"}
  initial={{ opacity: 0, scale: 0.7, filter: "blur(4px)" }}
  animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
  transition={{ type: "spring", duration: 0.2, bounce: 0 }}
>
  {isCopied ? <CheckIcon /> : <CopyIcon />}
</motion.div>
```

---

### Entrance Decomposition — Animate Elements, Not Containers

Animating one big container feels sluggish. Break it into individual elements with staggered delays.

```css
@keyframes enter {
  from {
    transform: translateY(8px);
    filter: blur(5px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    filter: blur(0px);
    opacity: 1;
  }
}

.animate-enter {
  animation: enter 800ms cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  animation-delay: calc(var(--delay, 0ms) * var(--stagger, 0));
}
```

```html
<div class="animate-enter" style="--stagger: 1">Title</div>
<div class="animate-enter" style="--stagger: 2">Description</div>
<div class="animate-enter" style="--stagger: 3">Buttons</div>
```

For word-level animation, split text into `<span>` per word, each with its own stagger.

---

### Exit Animation Subtlety — Exits Should Be Quieter Than Entrances

Exits don't need the same movement as entrances. A large exit `y` value demands attention the
leaving element doesn't deserve.

```tsx
// Enter: full travel distance
initial={{ opacity: 0, y: "calc(-100% - 4px)", filter: "blur(4px)" }}
animate={{ opacity: 1, y: 0,                   filter: "blur(0px)" }}

// Exit: subtle fixed value (not full travel)
exit={{   opacity: 0, y: "-12px",              filter: "blur(4px)" }}
```

Keep some motion on exit to indicate direction, but reduce it significantly. A fixed `12px` is
enough. Don't remove it entirely — zero motion on exit feels like a cut, not a transition.

---

## Interaction Polish

### Scale on Press — Tactile Button Feedback

A subtle scale-down on `:active` gives buttons physical weight. Use `scale(0.96)` — perceptible
but not dramatic.

```css
.btn {
  transition-property: scale;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}

.btn:active {
  scale: 0.96;
}
```

Don't apply to every interactive element. Skip it on form inputs, text areas, toggles, and any
element where the motion would feel distracting. A good rule: if the element "fires" a discrete
action (button, link), it benefits from press scale. If it's a continuous control (slider, input),
skip it.

---

### Minimum Hit Area — Don't Punish Accurate Fingers

Interactive elements need at least 40×40px to be reliably tappable. If the visible element is
smaller, extend with a pseudo-element that doesn't affect layout.

```css
.icon-btn {
  position: relative;
  width: 20px;
  height: 20px;
}

.icon-btn::after {
  content: "";
  position: absolute;
  inset: 50% auto auto 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
}
```

If extending the hit area would overlap an adjacent interactive element, shrink the pseudo-element
until they no longer collide — but make it as large as possible without overlapping.

**When to use:** Any icon button, checkbox, radio, or close button whose visible area is under 40px.

---

## Polish Checklist

Run this after Phases 2–6 before moving to implementation:

**Typography**

- [ ] Headings use `text-wrap: balance` (no orphaned words)
- [ ] Layout root has `antialiased` font smoothing
- [ ] All dynamic numbers use `tabular-nums`

**Spacing**

- [ ] All nested rounded elements satisfy `outer = inner + padding`
- [ ] Icon-adjacent buttons checked for optical alignment

**Depth**

- [ ] Cards and inputs use layered `box-shadow` instead of solid borders (where applicable)
- [ ] Images on variable backgrounds have 1px inset `outline`

**Motion**

- [ ] Hover/toggle states use `transition`, not `@keyframes`
- [ ] State-swapping icons use opacity + scale + blur transition
- [ ] Entrance animations decompose into individual elements with stagger
- [ ] Exit animations use reduced travel distance vs entrance

**Interaction**

- [ ] Action buttons use `scale(0.96)` on `:active` (not on form controls)
- [ ] Icon buttons and small controls have ≥40×40px hit area

---

## Anti-Patterns

- [ ] Single orphaned word on last line of heading — use `text-wrap: balance`
- [ ] Inner and outer border radii are equal — apply concentric offset
- [ ] Icon swaps are instant (no transition)
- [ ] Counters/prices shift width as values change — use `tabular-nums`
- [ ] Keyframe animations used for hover states (can't be interrupted)
- [ ] Enter and exit animations are identical in scale — exit should be subtler
- [ ] Solid `border` on components shown over images or gradients — use `box-shadow`
- [ ] Dark mode shadow still uses 3-layer depth formula — simplify to single ring
- [ ] Text weight looks heavier than designed on macOS — add `antialiased`
- [ ] Image outline uses tinted neutral (slate, zinc) instead of pure black/white
- [ ] Buttons have no `:active` feedback — add `scale(0.96)` press
- [ ] Small icon buttons have hit area under 40px — extend with `::after`
