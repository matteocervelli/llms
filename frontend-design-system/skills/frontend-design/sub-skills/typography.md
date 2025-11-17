# Typography Mastery

## Core Principles

Typography is the first dimension of visual design. Distinctive typeface choices transform bland interfaces into memorable experiences.

## Font Selection Strategy

### Avoid Generic Defaults

**Don't use:**
- Inter, Roboto, Arial (ubiquitous and forgettable)
- System fonts without intentional pairing
- Single-font designs (looks incomplete)

**Why it matters:** Generic fonts signal "I didn't think about this design." Distinctive fonts signal craft and intention.

### Choose Distinctive Pairs

Pair two contrasting typeface families to create visual hierarchy and depth.

#### Pairing Philosophy

**Display + Mono**
- Display: Serif or unique sans (e.g., Playfair Display, Bodoni Moda, Crimson Text)
- Mono: IBM Plex Mono, JetBrains Mono, Courier Prime
- Use: Headlines + Code/data

**Serif + Sans**
- Serif: Garamond, Crimson Text, Cormorant (traditional + elegant)
- Sans: Rubik, Syne, Space Mono (modern + clean)
- Use: Headlines + Body text

**Display + Display**
- Both distinctive but different weight ranges
- E.g., Playfair Display (thin 100–900) + Rubik (light 300–700)
- Use: Hierarchy through weight contrast, not family change

## Weight Extremes

Don't use middle ranges. Jump to extremes for impact.

### Recommended Strategy

**Display fonts:**
- 100–200 for subtle, elegant headlines
- 700–900 for bold, commanding headlines
- Avoid 400–600 (looks uncertain)

**Body text:**
- 300–400 for reading comfort
- 600–700 for emphasis/labels
- Avoid 500 (neither light nor bold)

**Mono fonts:**
- 400 for code
- 700 for inline emphasis

### Example Progression

```
Display (Playfair Display):
  100 → Thin, elegant
  700 → Bold, powerful

Body (Rubik):
  300 → Light, spacious
  400 → Regular, readable
  700 → Bold, emphasis
```

## Size Jumps (Scale)

Linear size progressions (1.5x) feel boring. Use aggressive jumps (3x+).

### Anti-Pattern

```
H1: 16px
H2: 24px (1.5x)
H3: 36px (1.5x)
Body: 14px
```
↑ Feels cramped and generic

### Better Pattern

```
Display (h1): 56px–80px
Large (h2): 32px–44px (1.5–2x from h1)
Medium (h3): 18px–24px (1.5x from h2)
Body: 14px–16px
Small: 12px
```
↑ Creates visual drama and hierarchy

## Pairing Strategies

### Serif + Mono Example
```
Display: Crimson Text (Serif)
  - H1: 900 weight, 72px
  - H2: 700 weight, 44px

Body: IBM Plex Mono
  - Body text: 400 weight, 16px
  - Code/labels: 600 weight, 14px
```

### Sans + Sans Example
```
Display: Space Mono
  - H1: 700 weight, 64px

Body: Rubik
  - Body text: 400 weight, 16px
  - Labels: 600 weight, 14px
```

## Readability on Colored Backgrounds

When text sits on non-white backgrounds:
- Increase weight (600+) for better contrast
- Reduce size slightly for visual compensation
- Add subtle text-shadow or background blur for legibility
- Test WCAG AA contrast minimum (4.5:1 for text)

## Google Fonts Integration

### Loading Strategy
```
https://fonts.googleapis.com/css2?family=Playfair+Display:wght@100;400;700;900&family=IBM+Plex+Mono:wght@400;700&display=swap
```

**Best practice:**
- Load only the weights you use (reduces file size)
- Use `display=swap` for performance (show fallback instantly)
- Limit to 2–3 typefaces maximum
- Load above-the-fold fonts in `<head>`

### Variable Fonts
Consider variable fonts to load entire weight range in one file:
- Playfair Display (variable: 100–900)
- Roboto Flex (variable: 25–151)
- Space Mono (limited weights: 400, 700)

## Responsive Typography

Scale typography proportionally at breakpoints:

```
Desktop (1024px+):
  H1: 64px
  Body: 16px

Tablet (768px–1023px):
  H1: 48px
  Body: 15px

Mobile (<768px):
  H1: 36px
  Body: 14px
```

## Anti-Patterns Checklist

- [ ] Font stack is generic (Inter, Roboto, Arial, system fonts)
- [ ] Font weights are limited (only regular and bold)
- [ ] Size progression is minimal (1.25–1.5x multiplier)
- [ ] No distinctive pairing strategy
- [ ] Poor readability on colored backgrounds
- [ ] All text sizes have equal visual weight
- [ ] No responsive typography scaling

## Success Metrics

After implementing distinctive typography:
- Typeface pairs feel intentional and memorable
- Size jumps create clear visual hierarchy
- Weight ranges emphasize important content
- Readability remains at WCAG AA+ levels
- Responsive scaling maintains hierarchy across devices

---

**For implementation guidance**, see:
- [react-typography.md](../../sub-skills/react-typography.md) for React/Tailwind
- [css-scss.md](../../sub-skills/css-scss.md) for CSS/SCSS
- [vue-typography.md](../../sub-skills/vue-typography.md) for Vue 3
- [svelte-typography.md](../../sub-skills/svelte-typography.md) for Svelte

**Reference data:**
- See `/design-references/typography/` for curated font pairing collections
