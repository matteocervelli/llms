# Spatial Composition & Layout Design

## Core Philosophy

Spatial composition is how content is arranged in two-dimensional space. Distinctive design breaks predictable, centered layouts and uses asymmetry, overlap, and intentional whitespace to create visual interest and guide the eye.

## Asymmetric Layouts

### Principle: Break Symmetry Intentionally

Centered, symmetrical layouts feel safe and corporate. Asymmetry feels modern, distinctive, and guides attention.

**Anti-pattern:**
```
┌─────────────────────┐
│    Center Title     │
│   Centered Content  │
│  Centered Elements  │
└─────────────────────┘
```
→ Feels static and corporate

**Better pattern:**
```
┌─────────────────────────────┐
│ Title in upper left         │
│ Content flows under         │
│       (offset right)        │
└─────────────────────────────┘
```
→ Feels intentional and modern

### Asymmetry Techniques

- **Text + Image Offset:** Text left-aligned, image positioned right (offset vertically)
- **Uneven Columns:** 60/40 grid instead of 50/50
- **Staggered Cards:** Grid items at different heights/positions
- **Diagonal Flow:** Elements arranged along 45° axis (tilted rotations or positioning)

## Overlap Techniques

### Principle: Layer Content Intentionally

Overlapping elements create depth and visual interest without adding real estate.

**Techniques:**

**Image Overlap:**
- Hero image overlaps text/heading
- Text sits on top with semi-transparent background or backdrop blur
- Creates dramatic composition

**Card Overlap:**
- Cards at same z-index but positioned to overlap slightly
- Reveals layering and spatial depth
- Works well for testimonials, features, or case studies

**Element Stack:**
- Multiple elements (shadows, images, graphics) offset slightly
- Creates 3D effect without actual 3D transforms
- Use 10–20px offsets for subtle depth

**Z-index Layering:**
- Background layer (image or gradient)
- Mid layer (semi-transparent overlay)
- Text/content layer on top
- Creates readable hierarchy

## Diagonal Flow

### Principle: Guide Eye Along 45° Angle

Diagonal compositions feel dynamic and modern.

**Techniques:**

**Rotated Elements:**
- Tilt containers, images, or text boxes 1–5 degrees
- Subtle rotation feels intentional, not broken
- Use sparingly (max 2–3 rotated elements per page)

**Diagonal Grid:**
- Arrange items along 45° axis
- Cards positioned to follow diagonal line
- Creates visual momentum

**Curved or Angled Sections:**
- Use CSS clip-path or SVG shapes to create diagonal section breaks
- Guides user eye from top-left to bottom-right (natural reading direction)

## Grid-Breaking

### Principle: Intentionally Violate Grid Rules

Perfect grid alignment feels boring. Strategic breaks create visual intrigue.

**Techniques:**

**Span Variations:**
- Some grid items span 1 column, others span 2
- Creates irregular, interesting grid (not monotonous)

**Content Overflow:**
- Text or images bleed beyond their container
- Creates sense of abundance and overflow

**Uneven Gutters:**
- Spacing between items varies intentionally
- Some items closer, others farther apart
- Guides attention through rhythm

**Half-Width Elements:**
- Elements positioned at 50% off-grid
- Creates visual tension and modernity

## Negative Space Strategy

### Generous Negative Space

Negative space is design's most powerful tool. It allows elements to breathe and prioritizes content.

**Principle:** More whitespace = more premium, sophisticated feel

**Techniques:**

**Breathing Room:**
- Content takes up 40–50% of viewport
- Remaining 50–60% is negative space
- Forces hierarchy and prevents cognitive overload

**Vertical Rhythm:**
- Line-height and section spacing follow consistent ratio (1.5x, 2x)
- Creates mathematical harmony

**Margins > Padding:**
- Large margins between sections
- Smaller padding within containers
- Creates clear visual separation

### Controlled Density

In contrast, some designs need controlled density (information-heavy dashboards, data tables).

**Principle:** When density needed, group content clearly

**Techniques:**
- Generous spacing between groups
- Compact spacing within groups
- Use cards/containers for visual grouping

## Alignment & Baseline Grid

### Rule: Align to Invisible Grid, but Break It Intentionally

Design should feel structured (align to baseline grid for readability), but with strategic breaks for visual interest.

**Implementation:**
- Base unit: 8px or 16px
- All spacing multiples of base unit (8, 16, 24, 32, 48, 64…)
- Intentional exceptions for dramatic elements
- Baseline grid for typography (line-height based alignment)

## Anti-Patterns to Avoid

- [ ] Centered, symmetrical layouts throughout
- [ ] Predictable margins and padding everywhere
- [ ] No intentional asymmetry in component layouts
- [ ] Grid-aligned everything (no visual breaking)
- [ ] Single-column or evenly-spaced multi-column layouts
- [ ] No layering or depth through overlap
- [ ] Minimal or excessive whitespace (not calibrated)
- [ ] All elements same size in grid (monotonous)
- [ ] No diagonal or organic flow

## Accessibility Considerations

While breaking layout rules, maintain:
- **Reading order:** Content flows logically top-to-bottom, left-to-right
- **Focus visibility:** Interactive elements remain keyboard-navigable
- **Semantic structure:** HTML maintains logical document structure
- **Mobile responsiveness:** Layout adaptations preserve usability

## Responsive Spatial Adaptation

Spatial patterns must adapt across breakpoints:

**Desktop (1024px+):**
- Asymmetric multi-column layouts
- Generous negative space
- Overlapping elements at full scale

**Tablet (768–1023px):**
- Reduce asymmetry slightly (narrower viewport)
- Maintain breathing room
- Stagger vertically instead of horizontally if needed

**Mobile (<768px):**
- Single-column layouts (maintain hierarchy)
- Collapse overlaps into stacked layout
- Preserve padding/margin rhythm at smaller scale

## Reference & Implementation

Spatial composition is CSS-based (grid, flexbox, positioning):

**For CSS/SCSS:**
- [css-scss.md](../../sub-skills/css-scss.md) – Grid, Flexbox, positioning

**For Tailwind (React, Vue, Svelte):**
- [tailwind-spatial.md](../../sub-skills/tailwind-spatial.md) – Grid classes, gap utilities

**For CSS-in-JS:**
- [styled-components-spatial.md](../../sub-skills/styled-components-spatial.md)

## Success Metrics

After implementing spatial strategy:
- Layout feels intentional and modern (not corporate/centered)
- Asymmetry guides attention naturally
- Whitespace creates premium feel
- Overlaps add visual interest and depth
- Grid-breaking creates dynamic rhythm
- Mobile/tablet layouts adapt while preserving hierarchy
- Content remains readable and accessible
- Users feel guided through page by spatial arrangement

---

**Remember:** All spatial choices serve content. Asymmetry and complexity should enhance, not obstruct, the message.
