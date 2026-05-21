# CSS/SCSS Implementation Sub-Skill

## Overview
Pure CSS and SCSS implementation strategy without CSS-in-JS. Leverages CSS custom properties, SCSS mixins, and organized file structure for design system coherence.

## File Organization

```
src/styles/
├── base/
│   ├── reset.scss          # Normalize + custom resets
│   ├── typography.scss     # Font definitions
│   └── variables.scss      # CSS custom properties
├── mixins/
│   ├── responsive.scss     # Media query helpers
│   ├── typography.scss     # Font mixins
│   └── spacing.scss        # Layout utilities
├── utilities/
│   ├── flexbox.scss        # Flex helpers
│   └── grid.scss           # Grid utilities
├── themes/
│   ├── light.scss
│   └── dark.scss
└── global.scss             # Import orchestration
```

## CSS Custom Properties (Theme Variables)

```scss
// src/styles/base/variables.scss
:root {
  // Colors
  --color-primary-50: #f0f9ff;
  --color-primary-500: #1e40af;
  --color-primary-900: #0c1e3c;

  --color-text: #1f2937;
  --color-text-light: #6b7280;
  --color-border: #e5e7eb;

  // Spacing Scale (8px base)
  --space-xs: 0.25rem;    // 4px
  --space-sm: 0.5rem;     // 8px
  --space-md: 1rem;       // 16px
  --space-lg: 1.5rem;     // 24px
  --space-xl: 2rem;       // 32px
  --space-2xl: 3rem;      // 48px

  // Typography
  --font-sans: 'Inter', -apple-system, sans-serif;
  --font-size-base: 1rem;
  --line-height-tight: 1.2;
  --line-height-normal: 1.6;

  // Motion
  --duration-fast: 150ms;
  --duration-base: 300ms;
  --duration-slow: 500ms;
  --easing-ease-out: cubic-bezier(0.4, 0, 0.2, 1);
}

[data-theme="dark"] {
  --color-text: #f3f4f6;
  --color-text-light: #d1d5db;
  --color-border: #374151;
}
```

## SCSS Mixins for Typography Scale

```scss
// src/styles/mixins/typography.scss
@mixin text-xs {
  font-size: 0.75rem;
  line-height: 1rem;
  font-weight: 400;
}

@mixin text-sm {
  font-size: 0.875rem;
  line-height: 1.25rem;
  font-weight: 400;
}

@mixin text-base {
  font-size: 1rem;
  line-height: 1.5rem;
  font-weight: 400;
}

@mixin heading-h1 {
  font-size: clamp(1.875rem, 5vw, 3.75rem);
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: -0.02em;
}

@mixin heading-h2 {
  font-size: clamp(1.5rem, 4vw, 2.25rem);
  line-height: 1.3;
  font-weight: 700;
}

// Usage
.heading { @include heading-h1; }
.body { @include text-base; }
```

## SCSS Functions for Color Manipulation

```scss
// src/styles/functions/_colors.scss
@function lighten-color($color, $amount) {
  @return adjust-color($color, $lightness: $amount);
}

@function darken-color($color, $amount) {
  @return adjust-color($color, $lightness: -$amount);
}

@function alpha($color, $opacity) {
  @return rgba($color, $opacity);
}

// Usage
.button {
  background-color: var(--color-primary-500);
  border-color: darken-color(var(--color-primary-500), 10%);

  &:hover {
    background-color: darken-color(var(--color-primary-500), 5%);
  }
}
```

## CSS Grid & Flexbox Layouts

```scss
// src/styles/mixins/layout.scss
@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

@mixin grid-auto-fit($min-width: 250px) {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax($min-width, 1fr));
  gap: var(--space-lg);
}

// Implementation
.grid-cards {
  @include grid-auto-fit(300px);
}

.button-group {
  @include flex-center;
  gap: var(--space-md);
}
```

## CSS Animations & Transitions

```scss
// src/styles/animations.scss
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.card {
  animation: slideInUp var(--duration-base) var(--easing-ease-out);
  transition: transform var(--duration-fast),
              box-shadow var(--duration-fast);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }
}
```

## Implementing the 5 Dimensions

### Typography
- Font scale via `@mixin heading-h*` and `@mixin text-*`
- Line height rhythm baked into each mixin
- `--font-sans` CSS variable for consistent stack

### Color
- Primary palette: `--color-primary-50` through `--color-primary-900`
- Theme switching: `[data-theme="dark"]` selector
- Semantic colors: `--color-text`, `--color-border`

### Motion
- Duration tokens: `--duration-fast|base|slow`
- Easing curve: `--easing-ease-out`
- Animations with consistent timing

### Spatial
- 8px spacing scale: `--space-xs` to `--space-2xl`
- Grid & flex utilities
- Responsive gap sizing

### Backgrounds
- Gradient overlays via `background: linear-gradient(...)`
- Pattern support via CSS `background-image`
- Z-index layering via CSS variables

## Related Documentation
- [Typography Dimension](../../../design-references/typography.md)
- [Color & Theme Dimension](../../../design-references/color-palettes.md)
- [Motion Patterns Dimension](../../../design-references/motion-patterns.md)
- [Spatial Composition Dimension](../../../design-references/spatial-compositions.md)
