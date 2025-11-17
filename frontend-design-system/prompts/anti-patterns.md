# Anti-Patterns: What to Avoid

## Overview

These are the predictable defaults that appear in generic AI-generated design. Actively rejecting these patterns is the first step toward intentional design.

## Typography Anti-Patterns

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

## Color & Theme Anti-Patterns

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

## Layout & Spatial Anti-Patterns

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

## Motion & Animation Anti-Patterns

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

## Background & Visual Details Anti-Patterns

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

## Copy & Content Anti-Patterns

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

## Visual Hierarchy Anti-Patterns

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

## Structural Anti-Patterns

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

## Interactive Anti-Patterns

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

## When You Break These Rules

It's okay to use a "forbidden" pattern if you do it intentionally:

**✓ Good**: "I used Inter because I paired it with Playfair Display and added custom color system"
**✓ Good**: "I used a blue accent because it's unexpected in this context"
**✓ Good**: "I centered the layout because the content demands symmetry"

**✗ Bad**: Justifying generic choices by saying "that's what the default is"

## The Real Rule

**Don't make decisions because they're default. Make decisions because they're right for your design.**

If you're choosing a typeface, color, layout, or animation because it's the easiest option, you're designing like an AI. Choose deliberately instead.
