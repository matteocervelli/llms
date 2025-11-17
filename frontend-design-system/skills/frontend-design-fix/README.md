# Frontend Design Fix

Fix generic, template-like designs by applying aesthetic upgrades across five design dimensions.

## When to Use This Skill

✅ Your design feels "AI-generated" or borrowed from a template
✅ Visual hierarchy is weak or unclear
✅ Color palette lacks personality or differentiation
✅ Layout is predictable (everything centered, uniform padding)
✅ Motion is absent or sluggish
✅ You want to upgrade without starting from scratch
✅ Building a stronger design system for existing products

## Quick Fix Workflow

### 1. Diagnose (5 min)
Run the design audit to identify problem areas.

```markdown
→ See `./sub-skills/audit.md`
```

**Output:** Audit report with scores for each dimension

### 2. Prioritize (5 min)
Focus on the 1–2 dimensions with lowest scores first.

### 3. Apply Fixes (15–45 min per dimension)
Follow the targeted sub-skill for each weak dimension.

### 4. Validate (10 min)
Check that improvements don't break accessibility, performance, or brand consistency.

### 5. Measure (5 min)
Compare before/after visuals and document learnings.

---

## Common Problems → Solutions

### "My fonts all look the same"
**Problem:** Using Inter, Roboto, or system fonts across all sizes and weights.
**Fix:** Replace with distinctive pairing (serif + mono, display + sans, etc.).

→ See `./sub-skills/typography-fixes.md`

---

### "Color palette feels corporate/bland"
**Problem:** Oversaturated neon, Material Design trinity, or no strategy.
**Fix:** Introduce dominant color + sharp accent, use CSS variables, create emotional intent.

→ See `./sub-skills/color-fixes.md`

---

### "Everything looks static"
**Problem:** No animations, or linear timing on all transitions.
**Fix:** Add orchestrated page load, staggered reveals, hover surprises, scroll triggers.

→ See `./sub-skills/motion-fixes.md`

---

### "Layout feels predictable"
**Problem:** Everything centered, uniform padding, symmetric grid only.
**Fix:** Break symmetry, add asymmetry/overlap, introduce diagonal flow, adjust spacing.

→ See `./sub-skills/spatial-fixes.md`

---

### "Backgrounds are boring"
**Problem:** Flat solid colors, no depth or visual interest.
**Fix:** Layer gradients, add geometric patterns/noise, create atmospheric effects.

→ See `./sub-skills/background-fixes.md`

---

## Before/After Examples

### Example 1: Typography + Color Fix
**Before:**
```jsx
// Generic
<h1 style={{ fontFamily: 'Inter, sans-serif', fontSize: '32px', color: '#333' }}>
  Welcome
</h1>
```

**After:**
```jsx
// Distinctive
<h1 style={{
  fontFamily: 'Crimson Text, serif',
  fontSize: '72px',
  fontWeight: 900,
  color: '#1a1a1a'
}}>
  Welcome
</h1>
```

→ See `./sub-skills/typography-fixes.md` and `./sub-skills/color-fixes.md`

---

### Example 2: Motion Fix
**Before:**
```css
/* Static */
button {
  background: #0066ff;
  color: white;
}
```

**After:**
```css
/* Interactive */
button {
  background: #0066ff;
  color: white;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 102, 255, 0.3);
}
```

→ See `./sub-skills/motion-fixes.md`

---

### Example 3: Spatial Fix
**Before:**
```jsx
{/* Centered, uniform */}
<div style={{ textAlign: 'center', padding: '64px' }}>
  <h1>Title</h1>
  <p>Content</p>
</div>
```

**After:**
```jsx
{/* Asymmetric, dynamic */}
<div style={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: '48px' }}>
  <div>{/* visual asset */}</div>
  <div style={{ paddingTop: '32px' }}>
    <h1>Title</h1>
    <p>Content</p>
  </div>
</div>
```

→ See `./sub-skills/spatial-fixes.md`

---

## Sub-Skills at a Glance

| Sub-Skill | Problem | Solution |
|-----------|---------|----------|
| `audit.md` | "I don't know what's wrong" | Design audit checklist + scoring |
| `typography-fixes.md` | Generic fonts, weak hierarchy | Distinctive pairings, weight extremes, size jumps |
| `color-fixes.md` | Bland/predictable palette | Dominant + accent, CSS variables, strategy |
| `motion-fixes.md` | Static, no animation | Orchestrated load, staggered reveals, hover |
| `spatial-fixes.md` | Centered, uniform, predictable | Asymmetry, overlap, diagonal flow |
| `background-fixes.md` | Flat, boring, no depth | Gradients, patterns, atmospheric effects |

---

## Implementation Guides

Once you've identified fixes using the principle-based sub-skills above, see framework-specific implementation:

- **React + Vite** → `/skills/frontend-design-fix-react/`
- **Vue** → `/skills/frontend-design-fix-vue/`
- **Svelte** → `/skills/frontend-design-fix-svelte/`
- **HTML/CSS** → `/skills/frontend-design-fix-html/`

Or reference the base dimension skills:

- **Typography** → `/skills/frontend-design/sub-skills/typography.md`
- **Color & Theme** → `/skills/frontend-design/sub-skills/color-theme.md`
- **Motion** → `/skills/frontend-design/sub-skills/motion.md`
- **Spatial** → `/skills/frontend-design/sub-skills/spatial.md`
- **Backgrounds** → `/skills/frontend-design/sub-skills/backgrounds.md`

---

## Success Criteria

After applying fixes:
- [ ] Fonts feel distinctive and intentional
- [ ] Color palette has emotional intent + accent strategy
- [ ] Motion enhances (not distracts from) content
- [ ] Layout shows asymmetry and intentional spacing
- [ ] Backgrounds add depth without clutter
- [ ] WCAG AA+ accessibility maintained
- [ ] Performance acceptable (animations 60fps)
- [ ] Brand personality evident in every element
