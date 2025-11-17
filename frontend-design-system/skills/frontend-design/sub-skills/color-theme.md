# Color & Theme Strategy

## Core Principle

Color isn't decoration. Color is emotion, accessibility, and usability. Thoughtful color systems create coherence and personality.

## Color System Architecture

### CSS Custom Properties Foundation

Define colors as variables for consistency and maintainability across all frameworks.

**Primary variable naming:**
```
--primary: [Main brand color]
--secondary: [Supporting brand color]
--accent: [Emphasis/CTA color, highest contrast]
--surface: [Backgrounds, containers]
--surface-secondary: [Cards, subtle backgrounds]
--text-primary: [Body text]
--text-secondary: [Labels, captions]
--border: [Dividers, subtle separation]
```

## Dominant + Accent Strategy

### 70-20-10 Color Rule

**Don't use:** 5+ primary colors distributed evenly (confusing, chaotic)

**Use instead:**
- **70%** Dominant color (background, base surfaces)
- **20%** Secondary color (supporting elements, subtle contrast)
- **10%** Accent color (CTAs, highlights, emphasis)

### Choosing Dominant Color

The dominant color should reflect the brand's visual direction:
- Dark neutrals (charcoal, navy, black) → Modern, professional, elegant
- Warm neutrals (cream, beige, tan) → Approachable, classic, warm
- Saturated colors (navy, teal, forest) → Distinctive, memorable, bold

### Accent Color Selection

The accent must provide sharp contrast for visibility and emphasis.

**Rule:** Accent should complement, not match, the dominant color.

Examples:
- Dark charcoal + Bright orange/coral (high contrast)
- Navy blue + Gold (elegant, premium)
- Forest green + Cream (natural, sophisticated)
- White background + Deep purple (dramatic)

**Avoid:** Purple gradients on white (cliché, over-used)

## IDE Themes & Cultural Aesthetics

### Dark Mode Context

Dark interfaces (charcoal, near-black) work exceptionally well for:
- Developer tools and technical products
- Creative/design software
- 24/7 monitoring dashboards
- Night-mode user bases

**Dark mode palette approach:**
```
Background: #0a0a0a or #1a1a1a (nearly black)
Surface: #2a2a2a or #3a3a3a (subtle elevation)
Text: #f5f5f5 (off-white, not pure white)
Accent: [Saturated color for emphasis]
```

### Light Mode Context

Light interfaces work for:
- Content-first products (blogs, news, documentation)
- Collaborative/social platforms
- Professional/corporate products
- Accessibility for users with vision sensitivities

**Light mode palette approach:**
```
Background: #ffffff or #fafafa (white/off-white)
Surface: #f5f5f5 or #efefef (subtle background)
Text: #1a1a1a or #242424 (dark, readable)
Accent: [Saturated color for emphasis]
```

### Cultural Color Meanings

Be aware of color symbolism:
- **Red**: Danger, urgency, or luck (culture-dependent)
- **Green**: Growth, health, go/success
- **Blue**: Trust, stability, corporate (over-used in Western business)
- **Yellow**: Caution, warmth, or wealth
- **Purple**: Creativity, luxury, spirituality (tech default, consider alternatives)
- **Orange**: Energy, enthusiasm, playfulness

**For distinctive design:** Choose colors that break Western tech conventions.

## Anti-Patterns to Avoid

- [ ] Purple/blue gradient on white (ubiquitous, lazy)
- [ ] No CSS custom properties for theming
- [ ] Evenly distributed color palette (5+ primary colors)
- [ ] No dedicated accent color for emphasis
- [ ] Insufficient contrast in interactive elements (< 4.5:1)
- [ ] No dark mode support or theme variants
- [ ] Text color doesn't adjust for background luminance
- [ ] Hover states use barely-visible color shifts

## Accessibility Requirements

### WCAG AA Contrast Minimum

All text must meet minimum contrast ratios:
- **Normal text:** 4.5:1 (foreground vs background)
- **Large text (18px+):** 3:1
- **UI components:** 3:1 (borders, outlines)

### Testing Contrast

Use tools like:
- WebAIM Contrast Checker
- Coolors.co accessibility validator
- Browser DevTools (Accessibility panel)

### Color Blindness Consideration

~8% of men and ~0.5% of women have color blindness. Don't rely on color alone:
- Pair color with icons, patterns, or text
- Test with color-blindness simulation tools
- Use sufficient contrast for users with low vision

## Theme Variants

### Light/Dark Theme Toggle

Create complementary palettes that maintain personality in both modes:

**Dark Variant:**
```
Primary: #f5f5f5 (light text)
Surface: #1a1a1a (dark background)
Accent: [Same accent, often lighter shade]
```

**Light Variant:**
```
Primary: #1a1a1a (dark text)
Surface: #ffffff (light background)
Accent: [Same accent, often darker shade]
```

## Color Psychology in Motion

When combining color with animation:
- Warm colors (orange, red) feel energetic, use for exciting transitions
- Cool colors (blue, teal) feel calm, use for subtle, professional movement
- Grayscale motion feels refined; saturated motion feels playful

## Reference & Implementation

**For color palette JSON references:**
- See `/design-references/color-palettes/` for pre-built palettes
- See `/design-references/color-palettes/accessible/` for WCAG-validated schemes

**For implementation guidance:**
- [react-color.md](../../sub-skills/react-color.md) for React themes
- [css-scss.md](../../sub-skills/css-scss.md) for CSS variables
- [vue-theme.md](../../sub-skills/vue-theme.md) for Vue provide/inject
- [svelte-stores.md](../../sub-skills/svelte-stores.md) for Svelte theme stores

## Success Metrics

After implementing color strategy:
- Design feels cohesive with intentional dominant/accent relationship
- All text meets WCAG AA contrast minimums
- Theme supports both light and dark modes
- Accent color is used deliberately, not overly
- Color choices reflect brand personality and differentiation
- Colorblind users can distinguish all UI elements

---

**Cultural context matters.** Consider your audience's aesthetic preferences and color associations.
