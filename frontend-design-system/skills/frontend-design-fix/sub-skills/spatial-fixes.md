# Spatial Composition Fixes

Break centered layouts, introduce asymmetry, overlap, and diagonal flow for distinctive visual direction.

## Quick Fixes

### Fix 1: Break Centered Layouts

**Before (Centered):**
```jsx
<section style={{ textAlign: 'center', padding: '80px' }}>
  <h1>Title</h1>
  <p>Content</p>
</section>
```

**After (Asymmetric):**
```jsx
<section style={{
  display: 'grid',
  gridTemplateColumns: '1fr 1.5fr',  /* 60/40 split, not 50/50 */
  gap: '80px',
  alignItems: 'center'
}}>
  <img src="visual.svg" />
  <div>
    <h1>Title</h1>
    <p>Content</p>
  </div>
</section>
```

### Fix 2: Introduce Asymmetry & Overlap

**Column Split (not 50/50):**
```jsx
gridTemplateColumns: '1.5fr 1fr'  /* 60/40 */
gridTemplateColumns: '1.75fr 1fr' /* 64/36 */
```

**Negative Margin Overlap:**
```jsx
<div>
  <section style={{ padding: '80px' }}>Section 1</section>
  <section style={{
    padding: '80px',
    marginTop: '-40px',  /* Overlap */
    zIndex: 1
  }}>Section 2</section>
</div>
```

### Fix 3: Diagonal/Staggered Flow

**Stagger Grid Items:**
```jsx
{items.map((item, i) => (
  <div key={i} style={{
    transform: i % 2 === 0 ? 'translateY(0)' : 'translateY(30px)'
  }}>
    <Card item={item} />
  </div>
))}
```

### Fix 4: Intentional Spacing Scale

**Before (Uniform):**
```css
section { padding: 64px; }
.card { margin: 32px; }
```

**After (Intentional):**
```css
.hero { padding: 120px; }           /* Generous */
.content { padding: 64px; }         /* Moderate */
.table { padding: 24px; }           /* Tight */
.card-grid { gap: 24px; }
.button-group { gap: 12px; }
```

### Fix 5: Hierarchical Spacing

**Use Spacing to Guide Eye:**
```jsx
<h1 style={{ marginBottom: '16px' }}>Title</h1>
<p style={{ marginBottom: '48px' }}>Subtitle</p>
<button>Action</button>
```

---

## Responsive Spacing

```css
/* Desktop */
@media (min-width: 1024px) {
  .hero { padding: 120px 80px; }
  gridTemplateColumns: '1.5fr 1fr';
}

/* Mobile */
@media (max-width: 767px) {
  .hero { padding: 48px 24px; }
  gridTemplateColumns: '1fr';
}
```

---

## Checklist

- [ ] No sections perfectly centered
- [ ] Column splits asymmetric (60/40, not 50/50)
- [ ] Overlapping sections present
- [ ] Spacing intentional (varies by context)
- [ ] Diagonal or staggered flow introduced
- [ ] Negative space guides eye direction
- [ ] Grid layouts have variation
- [ ] Layout feels distinctive

---

See: `/skills/frontend-design/sub-skills/spatial.md` for full principles
