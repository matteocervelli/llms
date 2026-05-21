# Motion & Micro-Interaction Principles

## Core Philosophy

Motion transforms interfaces from static to alive. Thoughtful animation reveals information, guides attention, and delights users. Generic motion annoys.

## Orchestrated Page Load

### Principle: Coordinated Reveals

When a page loads, don't fade everything in at once. Orchestrate reveals to guide the user's eye and create narrative.

**Pattern:**
1. Hero/background appears first (sets context)
2. Title/heading appears second (draws attention)
3. Supporting content staggers in (fills detail)
4. CTAs appear last (guides action)

**Duration:** 400–800ms total (fast enough to feel responsive)

**Easing:** ease-out (decelerating, feels natural)

## Staggered Reveals

### Concept: Sequential Animation with Delays

Items in lists, grids, or sequences should not all animate simultaneously. Small delays (100–300ms between items) create:
- Visual interest without overwhelming
- Guide through content order
- Feel of orchestrated choreography

### Delay Calculation

For each item in sequence:
```
animation-delay = item-index × 100ms
```

Example for 5 list items:
```
Item 1: 0ms
Item 2: 100ms
Item 3: 200ms
Item 4: 300ms
Item 5: 400ms
```

### Container Stagger Pattern

Orchestrate list reveals by defining delays relative to container visibility:
- Container enters first (fades in)
- Children stagger in with cumulative delays
- Optional: Delay children until container is fully visible

## Scroll-Triggered Animation

### Principle: Reveal on Scroll

Reveal content as user scrolls into view. Creates sense of discovery and paces information consumption.

**Common patterns:**
- Fade-in-up (opacity + subtle translateY)
- Scale-in (opacity + scale from 0.8 to 1)
- Slide-in from side (opacity + translateX)

**Trigger point:** Center of viewport or 75% down element

**Duration:** 600–1000ms (slower than page load, user is in control)

## Hover Surprises

### Concept: Micro-Interactions on Interactive Elements

Hover states should delight, not just indicate interactivity.

**Standard hover pattern:**
- Color change or opacity increase (indicates clickability)

**Surprise pattern:**
- Subtle scale shift (1 → 1.05)
- Icon rotation or animation (e.g., arrow rotates 90°)
- Text color change with slight glow
- Background color with smooth transition

**Duration:** 200–300ms (fast response to cursor)

**Important:** Only apply to genuinely interactive elements (buttons, links, form inputs)

### Example Hover Effects

**Button hover:**
- Scale: 1.0 → 1.03
- Shadow depth increases
- Text might glow subtly
- Duration: 200ms

**Link hover:**
- Underline animates in
- Color transitions smoothly
- Optional icon appears/changes
- Duration: 150ms

**Card hover:**
- Scale: 1.0 → 1.02
- Shadow intensifies
- Image might parallax slightly
- Duration: 300ms

## Easing Functions

### Common Easing Patterns

**Entrance (things appearing):**
- `ease-out`: Decelerating, natural, friendly
- `cubic-bezier(0.34, 1.56, 0.64, 1)`: Bouncy, playful
- `cubic-bezier(0.43, 0.13, 0.23, 0.96)`: Smooth, elegant

**Exit (things disappearing):**
- `ease-in`: Accelerating, purposeful
- `ease-in-out`: Smooth both directions
- Avoid linear (feels mechanical)

**Hover/interaction:**
- `ease-out`: Responsive, immediate
- `ease-in-out`: Smooth back-and-forth

### Rule of Thumb

- Never use `linear` for natural motion
- `ease-out` for entrances (feels responsive)
- `ease-in` for exits (feels deliberate)
- `ease-in-out` for oscillating/back-and-forth

## Anti-Patterns to Avoid

- [ ] No page load animations (static, boring)
- [ ] No staggered reveals for lists (all items load at once)
- [ ] Hover states missing or uninspired (no feedback)
- [ ] No scroll interactions (scroll feels inactive)
- [ ] Abrupt transitions between states (no easing, jarring)
- [ ] Missing micro-interactions on buttons/forms (impersonal)
- [ ] Animations faster than 150ms or slower than 1200ms (uncomfortable)
- [ ] No consideration for reduced-motion preferences

## Accessibility Considerations

### Respect `prefers-reduced-motion`

Some users have vestibular disorders or epilepsy and need animation disabled.

**Pattern:** Check user preference, disable animations accordingly:
- Reduce duration to 10ms (instant, not animated)
- Use `opacity` changes only (no transforms)
- Respect dark/light mode combined with motion preference

### Duration Guidelines

- Page load: 400–800ms
- Hover/interaction: 150–300ms
- Scroll reveal: 600–1000ms
- Page transitions: 300–600ms
- Never exceed 1500ms for any single animation

## Principles Checklist

- [ ] Page load has orchestrated reveals (hero → title → content → CTA)
- [ ] Lists/grids use staggered delays (100–300ms between items)
- [ ] Scroll reveals content with `fade-in-up` or similar pattern
- [ ] Hover states have subtle surprises (scale, glow, icon animation)
- [ ] Easing is natural (ease-out for entrance, ease-in for exit)
- [ ] All animations respect `prefers-reduced-motion`
- [ ] Animation durations are between 150–1200ms
- [ ] Motion guides attention, not distracts

## Reference & Implementation

Motion is implemented differently per framework:

**For React/Tailwind:**
- [react-motion.md](../../sub-skills/react-motion.md) – Framer Motion, CSS animations
- [tailwind-motion.md](../../sub-skills/tailwind-motion.md) – Tailwind animation utilities

**For Vue:**
- [vue-motion.md](../../sub-skills/vue-motion.md) – Vue Transition, composition hooks

**For Svelte:**
- [svelte-motion.md](../../sub-skills/svelte-motion.md) – Svelte transitions, animations

**For CSS/SCSS:**
- [css-scss.md](../../sub-skills/css-scss.md) – @keyframes, transitions

## Success Metrics

After implementing motion:
- Page load feels choreographed and intentional
- List reveals feel rhythmic, not chaotic
- Hover states provide delightful feedback
- Scroll interactions reveal content naturally
- Users experience easing as natural, not mechanical
- Animation respects accessibility preferences
- No user reports motion sickness or distraction
