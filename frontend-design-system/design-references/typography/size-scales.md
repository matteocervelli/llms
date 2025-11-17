# Typography Size Scales

Progressive size jumps create visual hierarchy and rhythm. Rather than linear 1.5x increments, use strategic multiplier patterns that establish clear relationships between typographic levels.

## Size Jump Patterns

### Extreme Jump (5.5x progression)
```
88px → 48px → 28px → 16px
```
**Multipliers**: 1.83x, 1.71x, 1.75x average

**Use case**: Premium editorial designs, luxury brands, high-contrast hierarchy
- Hero headlines establish dominance
- Mid-level headlines create secondary emphasis
- Body text remains readable but distinct
- Creates dramatic visual impact

### Aggressive Jump (3x progression)
```
72px → 36px → 18px → 12px
```
**Multipliers**: 2x, 2x, 1.5x

**Use case**: Technology/SaaS products, modern startups, bold brand voices
- Strong distinction between levels
- Limited but powerful emphasis
- Works well with sans-serif families
- Good for UI-heavy interfaces

### Moderate Jump (1.75x progression)
```
56px → 32px → 18px → 12px
```
**Multipliers**: 1.75x, 1.78x, 1.5x

**Use case**: Editorial, content marketing, balanced hierarchy
- Natural reading flow
- Multiple hierarchy levels feel intentional
- Flexible for various content types
- Comfortable for extended reading

## Generic 1.5x Increments: Why They Fail

```
48px → 32px → 21px → 14px (1.5x × 1.52x × 1.5x)
```

**Problems**:
- Differences feel accidental, not intentional
- Sizes cluster too closely
- Lacks visual distinction at each level
- Muddles hierarchy—unclear which level is which
- Works against reading patterns

The 1.5x multiplier creates intermediate sizes that confuse rather than clarify. There's no "big enough" feeling at the headline level.

## When to Use Extreme vs Moderate

| Pattern | Best For | Font Pairing | Example |
|---------|----------|--------------|---------|
| **Extreme (5.5x)** | Luxury, Premium, Editorial | Serif Display + Sans Body | Magazine covers, haute couture sites |
| **Aggressive (3x)** | SaaS, Tech, Modern | Bold Sans + Clean Sans | Startup landing pages, product UIs |
| **Moderate (1.75x)** | Content, Blog, Balanced | Mixed/Flexible | News sites, documentation, blogs |

## Implementation

```css
/* Define CSS custom properties for extreme jump */
:root {
  --h1: clamp(48px, 8vw, 88px);
  --h2: clamp(32px, 5vw, 48px);
  --h3: clamp(20px, 3vw, 28px);
  --body: clamp(14px, 1.5vw, 16px);
}

/* Use throughout design */
h1 { font-size: var(--h1); }
h2 { font-size: var(--h2); }
h3 { font-size: var(--h3); }
body { font-size: var(--body); }
```

Use `clamp()` to maintain proportional scaling across device sizes while respecting min/max bounds.

## References

See **font-pairings.json** for how different typeface combinations interact with these size scales:
- Serif displays pair well with extreme jumps
- Technical fonts benefit from aggressive jumps
- Playful fonts work across moderate ranges
