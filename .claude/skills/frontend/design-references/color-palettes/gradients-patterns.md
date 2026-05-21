# Gradients & Pattern Techniques

Layered gradients, noise textures, and atmospheric backgrounds elevate solid colors into sophisticated visual depth.

## Layered Gradient Techniques

### Two-Layer Gradient (Color + Darkness)
```css
.layered-two {
  background:
    linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)),
    linear-gradient(45deg, #1e293b, #0f172a);
  background-attachment: fixed;
}
```

**Effect**: Accent color fade over dark base. Creates depth without solid colors.

### Three-Layer Gradient (Color + Texture + Dark)
```css
.layered-three {
  background:
    radial-gradient(circle at 20% 80%, rgba(244, 114, 182, 0.15), transparent 50%),
    linear-gradient(135deg, rgba(99, 102, 241, 0.6), rgba(59, 130, 246, 0.6)),
    linear-gradient(45deg, #1e293b, #0f172a);
  background-attachment: fixed;
}
```

**Effect**: Soft accent glow + color layer + dark base = atmospheric depth.

### Gradient Mesh (4-Point)
```css
.gradient-mesh {
  background:
    radial-gradient(circle at 20% 30%, rgba(244, 114, 182, 0.4), transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.3), transparent 40%),
    radial-gradient(circle at 50% 50%, rgba(34, 197, 94, 0.2), transparent 60%),
    linear-gradient(135deg, #0f172a, #1e293b);
}
```

**Effect**: Multiple color nodes blend organically. Complex, sophisticated appearance.

## Radial Gradients for Depth

### Vignette (Dark Edges)
```css
.vignette {
  background:
    radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.7) 100%),
    linear-gradient(135deg, #1e293b, #0f172a);
}
```

**Use case**: Draw focus to center. Emphasize central content.

### Spotlight Effect
```css
.spotlight {
  background:
    radial-gradient(circle at 40% 60%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    linear-gradient(135deg, #1e293b, #0f172a);
}
```

**Use case**: Highlight specific region. Create focal point without text.

## CSS Noise Texture (Canvas-based)

### SVG Noise Filter
```html
<svg style="height: 0; width: 0;">
  <filter id="noise">
    <feTurbulence baseFrequency="0.85" numOctaves="4" result="noise" />
  </filter>
</svg>

<style>
  .noise-background {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    background-filter: url(#noise);
  }
</style>
```

### CSS Filter Approach
```css
.texture-noise {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  position: relative;
}

.texture-noise::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><filter id="n"><feTurbulence baseFrequency=".9" numOctaves="4"/></filter><rect width="100%" height="100%" filter="url(%23n)" opacity=".05"/></svg>');
  pointer-events: none;
  z-index: 1;
}

.texture-noise > * {
  position: relative;
  z-index: 2;
}
```

**Effect**: Subtle grain adds tactile quality. Reduces harsh gradients.

## Atmospheric Backgrounds vs Solid Colors

### Solid Color (Flat, Boring)
```css
body { background: #1e293b; }
```

**Problems**:
- No depth or dimension
- Looks static and flat
- Lacks visual interest
- No layering hierarchy

### Atmospheric Gradient
```css
body {
  background:
    radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.2), transparent 40%),
    radial-gradient(circle at 90% 80%, rgba(244, 114, 182, 0.15), transparent 40%),
    linear-gradient(135deg, #1e293b, #0f172a);
  background-attachment: fixed;
}
```

**Advantages**:
- Subtle depth without distraction
- Visual interest through layering
- Professional, premium appearance
- Maintains text readability
- Fixed attachment scrolls slower (parallax effect)

## Performance-Optimized Patterns

### Minimal Gradient (2 colors, single direction)
```css
.simple {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
}
```

**Performance**: Near-zero cost. GPU-optimized. Smooth on all devices.

### Moderate Complexity (2-3 layers, radial + linear)
```css
.moderate {
  background:
    radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.1), transparent 50%),
    linear-gradient(135deg, #1e293b, #0f172a);
}
```

**Performance**: Minimal impact. Smooth at 60fps on most devices.

### Complex (4+ layers with multiple radial gradients)
```css
.complex {
  background:
    radial-gradient(...),
    radial-gradient(...),
    radial-gradient(...),
    linear-gradient(...);
}
```

**Performance consideration**: Test on mobile. Reduce layer count if 60fps drops.

## Copy-Paste Ready Examples

### Premium Dark Mode
```css
background:
  radial-gradient(circle at 15% 25%, rgba(139, 92, 246, 0.25), transparent 50%),
  linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
background-attachment: fixed;
```

### Ocean Atmosphere
```css
background:
  radial-gradient(ellipse at 50% 0%, rgba(59, 130, 246, 0.3), transparent 60%),
  linear-gradient(180deg, #164e63 0%, #0c2340 100%);
```

### Forest Depth
```css
background:
  radial-gradient(circle at 30% 50%, rgba(34, 197, 94, 0.2), transparent 50%),
  radial-gradient(circle at 70% 30%, rgba(99, 102, 241, 0.15), transparent 50%),
  linear-gradient(135deg, #1e293b, #0f172a);
background-attachment: fixed;
```

## Implementation Tips

- Use `background-attachment: fixed` for parallax effect on scroll
- Limit to 3-4 layers max for performance
- Test on mobile before shipping
- Reduce opacity (0.1-0.3) for subtle effects
- Layer light gradients over dark base for better composition
- Always test text contrast on finished gradient

## References

See **ide-themes.json** for color palette selections that work well in gradient compositions. All examples use colors from curated palettes for visual coherence.
