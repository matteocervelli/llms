# Color & Theme Fixes

Remove Material Design trinity, build comprehensive CSS variable systems, and apply dominant + accent strategy.

## Quick Fixes

### Fix 1: Replace Material Trinity

**Before (Generic):**
```css
--blue: #0066ff;
--red: #ff0000;
--green: #00cc00;
```

**After (Distinctive):**
```css
--primary: #1a3a52;        /* Deep navy (dominant) */
--accent: #f4a261;         /* Warm coral (accent) */
--success: #27ae60;        /* Muted green */
--error: #c0392b;          /* Dark red */
--warning: #e67e22;        /* Warm orange */
```

### Fix 2: Build CSS Variable System

```css
:root {
  /* Primary & Accent */
  --primary: #1a3a52;
  --accent: #f4a261;

  /* Neutral Scale */
  --bg: #ffffff;
  --bg-secondary: #f9f9f9;
  --border: #e0e0e0;

  /* Text Colors */
  --text: #1a1a1a;
  --text-secondary: #666666;
  --text-inverse: #ffffff;

  /* Semantic */
  --success: #27ae60;
  --error: #c0392b;
  --warning: #e67e22;

  /* Effects */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.1);
}
```

### Fix 3: Use CSS Variables Everywhere

**Before:**
```jsx
<button style={{ backgroundColor: '#0066ff' }}>Click</button>
```

**After:**
```jsx
<button style={{ backgroundColor: 'var(--primary)' }}>Click</button>
```

### Fix 4: Implement Dark Mode

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1a;
    --text: #f0f0f0;
    --primary: #4a90e2;
    --accent: #f4a261;
  }
}
```

### Fix 5: Check Contrast (WCAG AA)

- Text on primary: minimum 4.5:1 contrast
- Text on accent: minimum 4.5:1 contrast
- Tool: WebAIM Contrast Checker

```css
button {
  background: var(--primary);    /* #1a3a52 */
  color: var(--text-inverse);    /* #ffffff = 9.5:1 contrast ✓ */
}
```

---

## Checklist

- [ ] Removed Material Design colors (blue/red/green)
- [ ] Dominant + accent strategy in place
- [ ] All colors in CSS variables
- [ ] No hardcoded color values in components
- [ ] Dark mode support implemented
- [ ] Text contrast WCAG AA (4.5:1+)
- [ ] Palette documented

---

See: `/skills/frontend-design/sub-skills/color-theme.md` for full principles
