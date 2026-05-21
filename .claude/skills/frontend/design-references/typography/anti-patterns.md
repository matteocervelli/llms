# Typography Anti-Patterns

Avoid these common mistakes that undermine typography hierarchy and brand perception.

## Fonts to Never Use

**These are overused defaults that signal generic or generic-feeling design**:

- **Inter** - The default choice. Fine in isolation, but everywhere.
- **Roboto** - Google Material's ubiquitous option. Lacks personality.
- **Open Sans** - Web-safe fallback masquerading as intentional choice.
- **Lato** - Outdated, feels like 2014 web design.
- **Arial** - System font. Signals lack of design investment.
- **Helvetica/System fonts** - Zero differentiation.

**Better alternatives** exist for every use case. See **font-pairings.json** for 6 intentional, distinctive pairings.

## Weight Mistakes

### Only Using 400/600
```css
/* WRONG */
p { font-weight: 400; }
strong { font-weight: 600; }
```

**Problem**: 200-point difference is subtle. At small sizes, indistinguishable.

### Better approach
```css
/* CORRECT */
p { font-weight: 400; }
em { font-weight: 500; }
strong { font-weight: 700; }
.bold { font-weight: 800; }
```

Use weights spanning 200-800 range. This creates actual visual distinction. Most Google Fonts families support ≥5 weights—use them.

### Weight vs Style Confusion
Don't mix italic for emphasis with different weights:
```css
/* WRONG */
em { font-style: italic; }
strong { font-weight: 700; }

/* CORRECT */
em { font-weight: 500; font-style: italic; }
strong { font-weight: 700; font-style: normal; }
```

## Size Mistakes

### The 1.5x Incremental Trap
```css
/* WRONG */
h1 { font-size: 48px; }  /* 48 */
h2 { font-size: 32px; }  /* 32 = 48 × 0.67 */
h3 { font-size: 21px; }  /* 21 = 32 × 0.66 */
body { font-size: 14px; } /* 14 = 21 × 0.67 */
```

Sizes feel arbitrary. No visual hierarchy clarity. Progression is mathematical, not intentional.

**See size-scales.md** for extreme and aggressive jump patterns that create actual distinction.

## Pairing Mistakes

### Sans + Sans Combinations
```css
/* WRONG */
h1 { font-family: "Poppins", sans-serif; }
p { font-family: "Open Sans", sans-serif; }
```

Two sans-serifs compete. Neither leads. No visual contrast. Feels like indecision.

### Serif + Serif Combinations
```css
/* WRONG */
h1 { font-family: "Crimson Text", serif; }
p { font-family: "Lato", serif; } /* Lato isn't serif */
```

Multiple serifs dilute impact. Confusing hierarchy. Feels cluttered.

### Same Weight Across Levels
```css
/* WRONG */
h1 { font-family: "Playfair Display"; font-weight: 400; }
body { font-family: "Inter"; font-weight: 400; }
```

Display font at light weight reads weak. No hierarchy. Lacks impact.

### Correct Pairing
```css
/* CORRECT */
h1 { font-family: "Playfair Display"; font-weight: 900; }
body { font-family: "Inter"; font-weight: 400; }
```

Display font bold/heavy. Body light/regular. Clear distinction.

## Implementation Checklist

- [ ] Display font ≠ body font (different family, not just weight)
- [ ] Multiple weight levels (≥4 distinct weights across hierarchy)
- [ ] Deliberate size jumps (extreme/aggressive, not 1.5x)
- [ ] No overused defaults (avoid Inter, Roboto, Open Sans, Lato)
- [ ] Weight difference ≥200 points between hierarchy levels
- [ ] Pairing contrast (serif + sans OR different sans subfamilies)

## References

See **font-pairings.json** for 6 proven combinations and their specific use cases.
