# Asymmetry Guide: Breaking Predictable Layouts

Centered, symmetrical layouts feel safe and static. Asymmetry creates visual tension, guides attention, and improves content hierarchy.

## Asymmetric Grid Patterns

### Unequal Column Split (30/70)
```css
.asymmetric-layout {
  display: grid;
  grid-template-columns: 1fr 2.5fr;
  gap: 4rem;
  align-items: center;
}

/* Alternative: mobile-aware */
.asymmetric-layout {
  display: grid;
  grid-template-columns: clamp(200px, 30%, 350px) 1fr;
  gap: 3rem;
}
```

**Visual effect**: Small, focused element + large, dominant element creates hierarchy.

**Use case**:
- Product showcase (text left, image right)
- Team bio (small avatar, large name/bio)
- Feature callout (icon left, description right)

### Offset Column Grid
```css
.offset-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
}

/* First row: offset right */
.item:nth-child(1) {
  grid-column: 1 / 2;
  margin-top: 0;
}

.item:nth-child(2) {
  grid-column: 2 / 3;
  margin-top: 4rem; /* Creates vertical offset */
}

/* Second row: offset left */
.item:nth-child(3) {
  grid-column: 1 / 2;
  margin-top: 4rem;
}

.item:nth-child(4) {
  grid-column: 2 / 3;
  margin-top: 0;
}
```

**Visual effect**: Staggered arrangement prevents predictable alignment.

## Offset Elements with Negative Margins

```css
.container {
  position: relative;
  padding: 3rem;
}

.main-element {
  position: relative;
  z-index: 2;
}

.offset-element {
  position: absolute;
  top: -2rem;
  right: -3rem;
  width: 300px;
  margin: 0; /* Reset, positioning handles placement */
  z-index: 1;
}
```

**CSS margin approach**:
```css
.content-wrapper {
  display: flex;
  gap: 2rem;
}

.sidebar {
  flex: 0 0 200px;
  margin-left: -2rem; /* Negative margin pushes into parent */
  padding-left: 2rem; /* Counteract negative margin for padding */
}

.main {
  flex: 1;
}
```

**Result**: Sidebar appears to break into content without disrupting flow.

## Overlap Techniques with Z-Index

### Card Stack (3D Effect)
```css
.card-stack {
  position: relative;
  height: 500px;
  perspective: 1000px;
}

.card {
  position: absolute;
  width: 320px;
  height: 400px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  background: white;
}

.card:nth-child(1) {
  left: 0;
  top: 0;
  z-index: 3;
  transform: rotate(-2deg);
}

.card:nth-child(2) {
  left: 50px;
  top: 40px;
  z-index: 2;
  transform: rotate(1deg);
}

.card:nth-child(3) {
  left: 100px;
  top: 80px;
  z-index: 1;
  transform: rotate(-1deg);
}
```

### Image + Text Overlap
```css
.overlap-section {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  position: relative;
  align-items: center;
  gap: -2rem; /* Allows overlap */
}

.image {
  grid-column: 1;
  width: 100%;
  z-index: 2;
  margin-right: -2rem; /* Overlap into text */
}

.text {
  grid-column: 2;
  background: white;
  padding: 3rem;
  border-radius: 8px;
  z-index: 1;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

**Result**: Image extends into text container, creating visual depth.

## Diagonal Flow with Transform

### Skewed Container
```css
.diagonal-section {
  position: relative;
  padding: 6rem 4rem;
  background: linear-gradient(135deg, #f5f5f5, #ffffff);
  overflow: hidden;
}

.diagonal-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: var(--accent-color);
  opacity: 0.05;
  transform: skew(-15deg) rotate(-10deg);
  z-index: 0;
}

.diagonal-content {
  position: relative;
  z-index: 1;
}
```

### Rotated Elements
```css
.element {
  transform: rotate(-3deg);
}

.element:nth-child(even) {
  transform: rotate(3deg);
}

/* For stronger effect */
.element-strong {
  transform: rotate(-8deg) skewX(-2deg);
}

.element-strong:nth-child(even) {
  transform: rotate(8deg) skewX(2deg);
}
```

**Timing**: Keep rotation between ±2deg for readability, ±5deg for bold effect.

## Directional Flow Patterns

### Left-Heavy (Content Left, Visual Right)
```css
.left-heavy {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 3rem;
  align-items: center;
}
```

Draws eye left first, then right. Natural reading direction in LTR.

### Right-Heavy (Visual Left, Content Right)
```css
.right-heavy {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 3rem;
  align-items: center;
}
```

Creates emphasis on right side. Works for CTAs and emphasis.

## Implementation Checklist

- [ ] No perfect 50/50 columns (use 30/70, 35/65, 40/60)
- [ ] Vertical stagger on grid rows (offset every other row)
- [ ] Overlap creates depth (z-index + negative margins)
- [ ] Rotation between ±2-5deg (subtle, not disorienting)
- [ ] Color/shadow defines layering hierarchy
- [ ] Asymmetry serves content hierarchy (not just decoration)
- [ ] Mobile resets to single column or symmetric layout

## References

See **layout-patterns.json** for complete pattern library with specific implementation examples and responsive breakpoints.
