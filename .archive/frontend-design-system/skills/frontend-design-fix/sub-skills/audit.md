# Design Audit Checklist

Score each dimension 0–5 to identify improvement opportunities.

## Quick Scoring (5 min per dimension)

### Typography (0–5)
- ❌ 1–2: Generic fonts (Inter, Roboto), safe weights (400–600), linear sizing
- ⚠️ 3–4: Secondary typeface present, some weight variation, moderate jumps
- ✅ 5: Distinctive pairing, weight extremes (100–200, 700–900), aggressive 3x+ jumps

**Score:** __/5

---

### Color & Theme (0–5)
- ❌ 1–2: Material trinity (blue/red/green), no CSS variables, neon accents
- ⚠️ 3–4: Custom primary color, some CSS variables, incomplete strategy
- ✅ 5: Dominant + accent, full CSS variable system, emotional intent

**Score:** __/5

---

### Motion & Animation (0–5)
- ❌ 1–2: No animations, linear timing, slow (2s+), no orchestration
- ⚠️ 3–4: Basic hover effects, fade-in, inconsistent easing
- ✅ 5: Orchestrated load, staggered reveals, hover surprises, scroll triggers

**Score:** __/5

---

### Spatial Composition (0–5)
- ❌ 1–2: Everything centered, uniform padding, perfect symmetry only
- ⚠️ 3–4: Some off-center elements, varied spacing, mix of layouts
- ✅ 5: Intentional asymmetry, overlap/layering, diagonal flow, generous spacing

**Score:** __/5

---

### Backgrounds & Details (0–5)
- ❌ 1–2: Flat solid colors, no depth, no micro-patterns
- ⚠️ 3–4: Some gradients, light texture, minor details
- ✅ 5: Layered gradients, geometric patterns, atmospheric depth

**Score:** __/5

---

## Audit Summary

| Dimension | Score | Priority | Next Step |
|-----------|-------|----------|-----------|
| Typography | __/5 | □ High | `./typography-fixes.md` |
| Color | __/5 | □ High | `./color-fixes.md` |
| Motion | __/5 | □ High | `./motion-fixes.md` |
| Spatial | __/5 | □ High | `./spatial-fixes.md` |
| Backgrounds | __/5 | □ High | `./background-fixes.md` |

**Average Score:** __/5

---

## Next Steps

1. Identify lowest-scoring dimension(s)
2. Follow the corresponding fix sub-skill
3. Apply fixes, re-audit, validate

