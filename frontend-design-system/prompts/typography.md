# Typography Guidance

## Overview

Typography is the primary carrier of personality and voice in design. Intentional typeface selection, pairing, and scale immediately distinguish careful design from generic AI output.

## Typefaces to Avoid

These fonts are ubiquitous in default AI outputs and should be rejected as your primary choice:

- **Inter**: Google's modern sans-serif, used everywhere in AI-generated design
- **Roboto**: Android's default, synonymous with generic design
- **Open Sans**: Neutral and safe, but overused
- **Lato**: Round and friendly, but lacks personality
- **System fonts**: Default OS fonts (SF Pro Display, Segoe UI) feel lazy

> If you use any of these, pair them with something unexpected and deliberately break the generic pattern.

## Typefaces to Prefer

These faces bring personality and intention to design:

### Display & Decorative
- **Playfair Display**: Elegant serif, high contrast, sophisticated
- **Bricolage Grotesque**: Modern sans with personality, handcrafted feel
- **Space Grotesk**: Geometric sans with character, works for display or body
- **Crimson Pro**: High-contrast serif, literary and elegant

### Body & Copy
- **IBM Plex Sans**: Humanist sans with warmth, works at all sizes
- **Space Grotesk**: Geometric sans that reads well in small sizes
- **Crimson Pro**: Serif for long-form content, distinctive personality

### Monospace (Technical, Quotes, Code)
- **JetBrains Mono**: Designed for code, readable and stylish
- **Fira Code**: Open source, ligatures for programming
- **IBM Plex Mono**: Humanist monospace, readable at any size

## Pairing Strategy

### High-Contrast Pairings (Recommended)

These pairings create visual interest and immediate personality:

#### Pattern 1: Display + Mono
```
Headline: Playfair Display (elegant serif)
Body: JetBrains Mono (technical monospace)
Result: Sophisticated + Modern
```

#### Pattern 2: Serif + Geometric Sans
```
Headline: Crimson Pro (high-contrast serif)
Body: Space Grotesk (geometric sans)
Result: Elegant + Contemporary
```

#### Pattern 3: Decorative + Humanist
```
Headline: Bricolage Grotesque (handcrafted sans)
Body: IBM Plex Sans (warm humanist sans)
Result: Crafted + Approachable
```

### Avoid Sameness
Don't use two similar typefaces:
- ❌ Roboto Display + Roboto Body (feels flat)
- ❌ Inter + Open Sans (indistinguishable)
- ✅ Playfair Display + JetBrains Mono (creates contrast)

## Font Weights & Extremes

### Weight Strategy

Use weight extremes to create contrast, not mid-range weights:

**Good**:
- Display: 300 (thin) or 700/800 (heavy)
- Body: 400 (regular) or 600 (semi-bold)
- Emphasis: 800/900 for strong hierarchy

**Avoid**:
- Middle weights everywhere (400, 500, 500) feels muddled
- Limited weight range (only 400, 500, 600) lacks contrast
- No visual distinction between hierarchy levels

### Example Weight Combinations

#### High Contrast
```
Headline: 300 weight (very light)
Sub-headline: 700 weight (very heavy)
Body: 400 weight (regular)
Emphasis: 900 weight (extra heavy)
```

#### Balanced Contrast
```
Headline: 400 weight (with letter-spacing)
Bold accent: 800 weight
Body: 400 weight
Fine print: 300 weight (with increased size for readability)
```

## Size Jumps: Extreme Over Incremental

### Size Scale Strategy

Use 3x+ jumps between hierarchy levels, not incremental 1.5x steps:

**Generic (Linear Scaling)**:
```
H1: 48px
H2: 36px (75% of H1)
H3: 28px (78% of H2)
Body: 16px
Small: 14px
```
Result: Feels predictable, every size feels similar distance apart.

**Intentional (3x+ Jumps)**:
```
Display: 96px (3x body)
Headline: 48px (3x body)
Sub-headline: 28px (1.75x body)
Body: 16px
Caption: 12px (0.75x body)
```
Result: Creates clear visual hierarchy, extreme sizes make smaller sizes feel intentional.

### Implementation Rules

1. Start with body size (16px or 18px is standard)
2. Create display size as 4-6x body (64px-96px)
3. Create headline as 2-3x body (32px-48px)
4. All other sizes fall between these extremes
5. Use odd numbers when possible (not round 10px increments)

**Example: 16px Base**
- Display: 88px (5.5x)
- Headline: 48px (3x)
- Sub-headline: 28px (1.75x)
- Body: 16px (1x)
- Small: 13px (0.8x)

**Example: 18px Base**
- Display: 96px (5.3x)
- Headline: 52px (2.9x)
- Sub-headline: 32px (1.8x)
- Body: 18px (1x)
- Small: 14px (0.78x)

## Line Height & Letter Spacing

### Line Height Strategy

- **Display (90px+)**: 1.0-1.1 (tight, confident)
- **Headline (40px+)**: 1.1-1.2 (tight)
- **Sub-headline (24px+)**: 1.2-1.3 (moderate)
- **Body (14px-20px)**: 1.4-1.6 (loose for readability)
- **Small text (<14px)**: 1.5-1.7 (extra loose for clarity)

### Letter Spacing Strategy

- **Display (90px+)**: -0.5 to -1px (negative space tightens)
- **Headline (40px+)**: -0.25px (subtle tightening)
- **Body**: 0px (default)
- **Emphasis/Caps**: +0.5px to +1px (opens up all-caps)

## Practical Implementation

### CSS Font Stack Example

```css
/* Display */
.display {
  font-family: 'Playfair Display', serif;
  font-size: 88px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.5px;
}

/* Headline */
.h1 {
  font-family: 'Playfair Display', serif;
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.25px;
}

/* Body */
.body {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 16px;
  font-weight: 400;
  line-height: 1.6;
  letter-spacing: 0;
}

/* Monospace (Code/Quotes) */
.mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.5px;
}

/* Small Text */
.caption {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 12px;
  font-weight: 400;
  line-height: 1.7;
  letter-spacing: 0px;
}
```

### Font Loading (Google Fonts)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=IBM+Plex+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## Typography Checklist

- [ ] Have you rejected default fonts (Inter, Roboto, Open Sans, Lato)?
- [ ] Do your chosen typefaces create visual contrast?
- [ ] Are font sizes using 3x+ jumps or are they incremental?
- [ ] Do weights span the full range (300-900) or are they mid-range?
- [ ] Is there a clear hierarchy that's immediately visible?
- [ ] Does the pairing feel intentional, not accidental?
- [ ] Would you describe this typography as "generic" or "distinctive"?

## Resources

- **Google Fonts**: https://fonts.google.com (free alternatives)
- **Typefaces**: Playfair Display, Bricolage Grotesque, Space Grotesk, Crimson Pro, IBM Plex, JetBrains Mono
- **Typography Theory**: "Thinking with Type" by Ellen Lupton
