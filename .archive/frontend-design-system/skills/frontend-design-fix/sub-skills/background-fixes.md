# Background & Visual Details Fixes

Replace flat solid colors with layered gradients, geometric patterns, and atmospheric depth.

## Quick Fixes

### Fix 1: Layered Gradients

**Before (Flat):**
```css
body { background: #ffffff; }
```

**After (Layered):**
```css
body {
  background:
    radial-gradient(circle at 20% 50%, rgba(244, 162, 97, 0.1), transparent 50%),
    linear-gradient(135deg, #1a3a52 0%, #2d5a7b 100%);
}
```

**Multi-layer effect:**
```css
.hero {
  background:
    radial-gradient(circle at 80% 20%, rgba(244, 162, 97, 0.15), transparent 40%),
    radial-gradient(circle at 20% 80%, rgba(74, 144, 226, 0.1), transparent 40%),
    linear-gradient(180deg, #1a3a52 0%, #0f1f2e 100%);
}
```

### Fix 2: Geometric Patterns & Textures

**SVG Pattern:**
```jsx
<div style={{
  background: `
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100'%3E%3Ccircle cx='50' cy='50' r='8' fill='%23f4a261' opacity='0.1'/%3E%3C/svg%3E"),
    linear-gradient(135deg, #1a3a52 0%, #2d5a7b 100%)
  `,
  backgroundSize: '100px 100px, cover'
}}>
  Content with subtle pattern
</div>
```

**CSS Grid Pattern:**
```css
.background-grid {
  background:
    linear-gradient(0deg, transparent 24%, rgba(244, 162, 97, 0.1) 25%, rgba(244, 162, 97, 0.1) 26%, transparent 27%),
    linear-gradient(90deg, transparent 24%, rgba(244, 162, 97, 0.1) 25%, rgba(244, 162, 97, 0.1) 26%, transparent 27%);
  background-size: 40px 40px;
  background-color: #1a3a52;
}
```

### Fix 3: Atmospheric Depth

**Layer Strategy:** Background → Midground (elevated) → Foreground (floating accents)

```css
.hero {
  position: relative;
  background: linear-gradient(135deg, #1a3a52, #0f1f2e);
}

.hero::before {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(244, 162, 97, 0.08), transparent 50%);
  pointer-events: none;
}

.hero-content {
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
}
```

### Fix 4: Contextual Visual Elements

**Accent border + faint background icon:**
```css
section {
  border-left: 4px solid var(--accent);
  padding-left: 24px;
  position: relative;
}

section::before {
  position: absolute;
  top: 10%;
  right: 5%;
  font-size: 200px;
  opacity: 0.05;
  color: var(--accent);
  content: '⚡';
  pointer-events: none;
}
```

### Fix 5: Dark Mode Support

```css
:root {
  --bg-gradient-start: #f9f9f9;
  --bg-gradient-end: #ffffff;
  --accent-overlay: rgba(244, 162, 97, 0.05);
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-gradient-start: #1a3a52;
    --bg-gradient-end: #0f1f2e;
    --accent-overlay: rgba(244, 162, 97, 0.1);
  }
}

body {
  background:
    radial-gradient(circle at 20% 50%, var(--accent-overlay), transparent 50%),
    linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
}
```

---

## Checklist

- [ ] No flat solid colors (all use gradients/patterns)
- [ ] Layered gradients create depth
- [ ] Geometric patterns/textures added subtly
- [ ] Foreground/midground/background layers defined
- [ ] Contextual visual details (icons, borders, shapes) present
- [ ] Dark mode gradients defined
- [ ] Performance acceptable (no excessive blur)
- [ ] Accessibility maintained (contrast sufficient)

---

## Performance Tips

- Use CSS gradients, not image files (lighter, faster)
- Limit animated gradients (GPU intensive)
- Use `will-change: background` sparingly
- Blur effects: test on lower-end devices
- Keep SVG patterns simple (fewer paths)

---

See: `/skills/frontend-design/sub-skills/backgrounds.md` for full principles
