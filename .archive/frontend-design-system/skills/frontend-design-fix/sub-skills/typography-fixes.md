# Typography Fixes

Replace generic fonts (Inter, Roboto, Open Sans) with distinctive pairings, establish weight extremes, and use aggressive size jumps.

## Quick Fixes

### Fix 1: Replace Generic Fonts

**Pairing Options:**
- **Serif + Mono**: Crimson Text (headlines) + IBM Plex Mono (body)
- **Sans + Sans**: Playfair Display (h1) + Rubik (body)
- **Display Weight Split**: Playfair thin (100–200) for h1, bold (700–900) for h2

### Fix 2: Use Weight Extremes (Not 400–600)

```css
h1 { font-weight: 900; }      /* Bold, commanding */
h2 { font-weight: 700; }      /* Strong emphasis */
body { font-weight: 300; }    /* Light, readable */
label { font-weight: 600; }   /* Mid-emphasis */
```

### Fix 3: Aggressive Size Jumps (3x+)

```css
/* Before: h1 32px, h2 28px (linear, boring) */
/* After: h1 64px, h2 36px, body 16px (aggressive, clear) */

h1 { font-size: 56px; }       /* 3.5x body */
h2 { font-size: 36px; }       /* 2.25x body */
h3 { font-size: 22px; }       /* 1.4x body */
body { font-size: 16px; }
small { font-size: 12px; }    /* 0.75x body */
```

### Fix 4: Responsive Scale

```css
/* Desktop */
@media (min-width: 1024px) {
  h1 { font-size: 64px; }
  body { font-size: 16px; }
}

/* Mobile */
@media (max-width: 767px) {
  h1 { font-size: 36px; }
  body { font-size: 14px; }
}
```

### Fix 5: Optimize Font Loading

```html
<!-- Load only weights in use -->
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;700&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
```

---

## Checklist

- [ ] Replaced generic fonts (not Inter, Roboto, etc.)
- [ ] Weight extremes in use (100–200, 700–900)
- [ ] Size jumps aggressive (2x–3.5x)
- [ ] Font loading optimized (only needed weights)
- [ ] Responsive typography scales proportionally
- [ ] WCAG AA contrast (4.5:1) maintained

---

See: `/skills/frontend-design/sub-skills/typography.md` for full principles
