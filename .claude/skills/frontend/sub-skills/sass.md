# Sass/SCSS — Design Tokens, Architecture & Patterns

## Core Concept

Sass extends CSS with variables, nesting, mixins, functions, and modules. Use the 7-1 architecture for scalable stylesheets and design tokens for consistent theming.

## 7-1 Architecture

```
scss/
├── abstracts/
│   ├── _tokens.scss       # Design tokens (colors, spacing, typography)
│   ├── _mixins.scss       # Reusable mixins
│   ├── _functions.scss    # Custom functions
│   └── _breakpoints.scss  # Responsive breakpoints
├── base/
│   ├── _reset.scss        # Reset/normalize
│   ├── _typography.scss   # Base typography rules
│   └── _animations.scss   # Keyframe animations
├── components/
│   ├── _buttons.scss      # Button styles
│   ├── _cards.scss        # Card components
│   └── _forms.scss        # Form elements
├── layout/
│   ├── _header.scss       # Header/nav
│   ├── _footer.scss       # Footer
│   ├── _sidebar.scss      # Sidebar
│   └── _grid.scss         # Grid system
├── pages/
│   ├── _home.scss         # Page-specific styles
│   └── _dashboard.scss
├── themes/
│   ├── _light.scss        # Light theme overrides
│   └── _dark.scss         # Dark theme overrides
├── vendors/
│   └── _htmx.scss         # Third-party overrides
└── main.scss              # Single entry point (@use all partials)
```

## Design Tokens

```scss
// abstracts/_tokens.scss

// Colors
$color-primary: #0f766e; // Teal 700
$color-primary-light: #14b8a6; // Teal 500
$color-primary-dark: #0d9488; // Teal 600
$color-secondary: #1e293b; // Slate 800
$color-accent: #f59e0b; // Amber 500
$color-error: #ef4444; // Red 500
$color-success: #22c55e; // Green 500
$color-warning: #f97316; // Orange 500

// Surfaces
$color-bg: #ffffff;
$color-bg-alt: #f8fafc; // Slate 50
$color-surface: #ffffff;
$color-border: #e2e8f0; // Slate 200

// Typography
$font-family-sans:
  "Inter",
  system-ui,
  -apple-system,
  sans-serif;
$font-family-mono: "JetBrains Mono", "Fira Code", monospace;

$font-size-xs: 0.75rem; // 12px
$font-size-sm: 0.875rem; // 14px
$font-size-base: 1rem; // 16px
$font-size-lg: 1.125rem; // 18px
$font-size-xl: 1.25rem; // 20px
$font-size-2xl: 1.5rem; // 24px
$font-size-3xl: 1.875rem; // 30px

$font-weight-normal: 400;
$font-weight-medium: 500;
$font-weight-semibold: 600;
$font-weight-bold: 700;

// Spacing (8px grid)
$space-1: 0.25rem; // 4px
$space-2: 0.5rem; // 8px
$space-3: 0.75rem; // 12px
$space-4: 1rem; // 16px
$space-6: 1.5rem; // 24px
$space-8: 2rem; // 32px
$space-12: 3rem; // 48px
$space-16: 4rem; // 64px

// Borders
$radius-sm: 0.25rem;
$radius-md: 0.375rem;
$radius-lg: 0.5rem;
$radius-full: 9999px;

// Shadows
$shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
$shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
$shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

// Transitions
$transition-fast: 150ms ease;
$transition-normal: 300ms ease;
$transition-slow: 500ms ease;
```

## Mixins

```scss
// abstracts/_mixins.scss

@mixin respond-to($breakpoint) {
  @if $breakpoint == "sm" {
    @media (min-width: 640px) {
      @content;
    }
  }
  @if $breakpoint == "md" {
    @media (min-width: 768px) {
      @content;
    }
  }
  @if $breakpoint == "lg" {
    @media (min-width: 1024px) {
      @content;
    }
  }
  @if $breakpoint == "xl" {
    @media (min-width: 1280px) {
      @content;
    }
  }
}

@mixin flex-center {
  display: flex;
  align-items: center;
  justify-content: center;
}

@mixin truncate($lines: 1) {
  @if $lines == 1 {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  } @else {
    display: -webkit-box;
    -webkit-line-clamp: $lines;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}

@mixin focus-ring($color: $color-primary) {
  &:focus-visible {
    outline: 2px solid $color;
    outline-offset: 2px;
  }
}
```

## Dark Mode with CSS Custom Properties

```scss
// themes/_light.scss
:root {
  --color-bg: #{$color-bg};
  --color-text: #{$color-secondary};
  --color-primary: #{$color-primary};
  --color-surface: #{$color-surface};
  --color-border: #{$color-border};
}

// themes/_dark.scss
[data-theme="dark"] {
  --color-bg: #0f172a;
  --color-text: #e2e8f0;
  --color-primary: #14b8a6;
  --color-surface: #1e293b;
  --color-border: #334155;
}

// Usage in components
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  color: var(--color-text);
}
```

## Design Dimension Integration

- **Typography**: Tokens define font stack, sizes, weights → applied in `base/_typography.scss`
- **Color**: Tokens define palette → CSS custom properties for theming
- **Motion**: Transition tokens + keyframes in `base/_animations.scss`
- **Spatial**: Spacing tokens (8px grid) → consistent margins/padding
- **Backgrounds**: Gradient mixins, texture patterns in components

## Vite Integration

```javascript
// vite.config.ts
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "scss/abstracts" as *;`,
      },
    },
  },
});
```

This auto-imports tokens, mixins, and functions in every SCSS file.

## Best Practices

- **Tokens first**: Define all values as tokens, never hardcode colors/sizes
- **CSS custom properties for runtime**: Tokens → CSS vars for theming
- **Nesting max 3 levels**: Deeper = specificity problems
- **BEM naming**: `.block__element--modifier` for component scoping
- **@use over @import**: Modern Sass modules with namespaces
- **Mobile-first**: Default styles = mobile, `@include respond-to` for larger
