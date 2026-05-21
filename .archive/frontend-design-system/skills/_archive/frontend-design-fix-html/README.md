# Frontend Design Fix - HTML/CSS

## Quick Start

This skill helps you transform generic HTML/CSS designs into visually distinctive interfaces using Anthropic's 5 design dimensions.

### What This Skill Does

1. **Analyzes** your current HTML/CSS for generic design patterns
2. **Audits** against anti-patterns (bland typography, purple gradients, centered layouts, etc.)
3. **Applies** aesthetic upgrades across:
   - Typography (distinctive fonts, extreme weights, size jumps)
   - Color & Theme (cohesive palettes, CSS variables, accent colors)
   - Motion (page load animations, staggered reveals, hover interactions)
   - Spatial Composition (asymmetric layouts, broken grids, intentional overlap)
   - Backgrounds (layered gradients, textures, atmospheric depth)

### When to Use

Use this skill when you have:
- Existing HTML/CSS that feels generic or bland
- Designs using default fonts (Inter, Roboto, Arial)
- Solid color backgrounds
- No animations or micro-interactions
- Centered, predictable layouts
- Purple/blue gradients on white

### Basic Workflow

```
1. Provide your HTML/CSS files
2. Skill analyzes and scores against checklist
3. Dimensions are fixed one at a time
4. Before/after comparison generated
5. Accessibility verified
```

## Design Dimensions Explained

### Typography
**Problem**: Generic system fonts in limited weights
**Solution**: Distinctive pairs, extreme weights (100-900), 3x size jumps, high-contrast pairings

### Color & Theme
**Problem**: Purple gradients, no theming, evenly distributed colors
**Solution**: CSS variables, dominant + accent colors, 70-20-10 rule, consistent palette

### Motion
**Problem**: No animations, abrupt transitions
**Solution**: Page load animations, staggered reveals, hover surprises, scroll triggers

### Spatial Composition
**Problem**: Centered, symmetrical, predictable layouts
**Solution**: Asymmetry, intentional overlap, broken grids, generous/controlled spacing

### Backgrounds
**Problem**: Solid colors, no depth
**Solution**: Layered gradients, patterns/textures, atmospheric effects, contextual depth

## Example: Before & After

### Before (Generic)
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: white;
    }
    h1 {
      color: purple;
      font-size: 2rem;
      text-align: center;
    }
    button {
      background: #e0e0e0;
      padding: 10px 20px;
      border: none;
    }
  </style>
</head>
<body>
  <h1>Welcome</h1>
  <button>Click Me</button>
</body>
</html>
```

**Anti-pattern Score**: 5/5 items on checklist

### After (Distinctive)
```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;900&family=Inter:wght@100..900&display=swap" rel="stylesheet">
  <style>
    :root {
      --font-display: 'Playfair Display', serif;
      --font-body: 'Inter', sans-serif;
      --primary: #1a1a1a;
      --accent: #ff6b35;
      --surface: #fafafa;
    }

    body {
      font-family: var(--font-body);
      background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }

    h1 {
      font-family: var(--font-display);
      font-size: 5rem;
      font-weight: 900;
      color: var(--primary);
      margin: 0;
      animation: fadeInUp 0.8s ease-out;
      text-align: left;
      max-width: 600px;
    }

    button {
      font-family: var(--font-body);
      background: var(--accent);
      color: white;
      padding: 1rem 2rem;
      border: none;
      border-radius: 0.25rem;
      font-size: 1.125rem;
      font-weight: 600;
      cursor: pointer;
      margin-top: 2rem;
      transition: all 0.3s ease-out;
      animation: fadeInUp 0.8s ease-out 0.2s both;
    }

    button:hover {
      transform: scale(1.05);
      box-shadow: 0 20px 40px rgba(255, 107, 53, 0.3);
    }

    button:focus {
      outline: 3px solid var(--accent);
      outline-offset: 2px;
    }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
  </style>
</head>
<body>
  <h1>Welcome to Something Remarkable</h1>
  <button>Discover More</button>
</body>
</html>
```

**Anti-pattern Score**: 0/5 items on checklist

### Improvements
- [x] Typography: Playfair Display (display) + Inter (body), weights 100-900, 5rem vs 1rem
- [x] Color: CSS variables, accent color (#ff6b35), layered background gradient
- [x] Motion: fadeInUp animation with staggered timing, hover scale effect
- [x] Spatial: Left-aligned title (asymmetry), 2rem padding (breathing room)
- [x] Background: Linear gradient instead of solid, subtle depth

## Key Concepts

### CSS Custom Properties
```css
:root {
  --primary: #1a1a1a;
  --accent: #ff6b35;
  --transition-fast: 200ms ease-out;
}

button {
  background: var(--accent);
  transition: all var(--transition-fast);
}
```

### Staggered Animations
```css
[data-stagger] {
  animation: fadeInUp 0.4s ease-out forwards;
}

[data-stagger]:nth-child(1) { animation-delay: 100ms; }
[data-stagger]:nth-child(2) { animation-delay: 200ms; }
[data-stagger]:nth-child(3) { animation-delay: 300ms; }
```

### Gradient Backgrounds
```css
background: linear-gradient(
  135deg,
  #1a1a1a 0%,
  #2d2d2d 50%,
  #3a3a3a 100%
);
```

### Accessibility
```css
/* Always provide visible focus states */
button:focus {
  outline: 3px solid var(--accent);
  outline-offset: 2px;
}

/* Maintain minimum 4.5:1 contrast */
color: #1a1a1a;  /* WCAG AA on #fafafa */
```

## Common Patterns

### Typography Stack
```css
/* Display Headlines */
h1, h2, h3 {
  font-family: 'Playfair Display', 'Georgia', serif;
  font-weight: 700;
  letter-spacing: -0.02em;
}

/* Body Text */
body, p {
  font-family: 'Inter', 'Segoe UI', sans-serif;
  font-weight: 400;
  line-height: 1.6;
}

/* Code / Mono */
code, pre {
  font-family: 'IBM Plex Mono', 'Courier New', monospace;
  font-weight: 400;
  font-size: 0.9em;
}
```

### Hover States
```css
a, button {
  transition: all 0.3s ease-out;
}

a:hover {
  text-decoration: underline;
  text-decoration-thickness: 3px;
  text-underline-offset: 6px;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
```

### Responsive Typography
```css
h1 {
  font-size: 2.5rem;
}

@media (min-width: 768px) {
  h1 {
    font-size: 4rem;
  }
}

@media (min-width: 1024px) {
  h1 {
    font-size: 5rem;
  }
}
```

## Tools & Resources

- **Font Pairing**: Google Fonts, Adobe Fonts, Variable Fonts
- **Color Tools**: Coolors.co, Contrast Checker, ColorSpace
- **Animation**: Keyframes, Animate.css, AOS (Animate On Scroll)
- **Accessibility**: WAVE, AXLE DevTools, Lighthouse

## Next Steps

1. **Identify** your current design anti-patterns
2. **Pick a dimension** to start with (typically typography)
3. **Apply fixes** systematically
4. **Verify** accessibility and responsiveness
5. **Iterate** until all dimensions are improved

See `/examples/showcase.md` for complete before/after examples.
