# Tailwind CSS: Building Distinctive Design Systems

Tailwind CSS is a utility-first framework that excels at creating custom, branded design systems. Move beyond the default palette to build visually distinctive interfaces aligned with your design dimensions.

## Custom Configuration (tailwind.config.js)

Override defaults completely:

```js
export default {
  theme: {
    fontFamily: {
      serif: ['Crimson Text', 'serif'],
      sans: ['Inter', 'sans-serif'],
      mono: ['Roboto Mono', 'monospace'],
    },
    colors: {
      primary: '#0F172A',    // Slate-900 replacement
      accent: '#DC2626',     // Brand red
      success: '#059669',    // Emerald
      neutral: '#6B7280',
    },
    spacing: {
      0: '0',
      1: '0.25rem',    // 4px
      2: '0.5rem',     // 8px
      4: '1rem',       // 16px
      6: '1.5rem',     // 24px
      8: '2rem',       // 32px
      12: '3rem',      // 48px
    },
    animation: {
      fade: 'fadeInOut 300ms ease-in-out',
      slide: 'slideIn 250ms cubic-bezier(0.25, 0.46, 0.45, 0.94)',
      pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
    },
  },
};
```

## @layer for Component Abstraction

Create reusable component classes using `@layer`:

```css
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-primary text-white rounded-lg
           font-medium transition-all duration-200
           hover:shadow-lg active:scale-95;
  }

  .card {
    @apply bg-white rounded-xl shadow-sm border border-gray-200 p-6;
  }

  .input-field {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md
           focus:outline-none focus:ring-2 focus:ring-accent
           transition-shadow duration-150;
  }
}
```

## Applying Design Dimensions

**Typography Dimension**: Use custom font utilities
```html
<h1 class="font-serif text-3xl leading-tight tracking-tight">Headline</h1>
<p class="font-sans text-base leading-relaxed text-neutral">Body</p>
```

**Color Dimension**: Extend color palette with semantic tokens
```js
colors: {
  primary: '#0F172A',
  'primary-light': '#1E293B',
  'primary-dark': '#000000',
}
```

**Spacing Dimension**: Custom spacing scale for layouts
```html
<div class="grid gap-6 p-8"><!-- 24px gap, 32px padding --></div>
```

**Motion Dimension**: Custom animations with cubic-bezier curves
```html
<div class="animate-slide">Slides in smoothly</div>
```

**Composition Dimension**: Responsive grid utilities
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

## Dark Mode & Variants

```js
darkMode: 'class',
extend: {
  colors: {
    'dark-bg': '#1a1a1a',
  },
}
```

```html
<div class="bg-white dark:bg-dark-bg transition-colors">
```

## Dimension Connections

- [Typography System](../dimension-sub-skills/typography.md)
- [Color & Theme](../dimension-sub-skills/color-theme.md)
- [Motion & Animation](../dimension-sub-skills/motion.md)
- [Spacing & Layout](../dimension-sub-skills/spatial-compositions.md)

## Key Takeaways

- Tailwind is most powerful when **customized aggressively**
- Use `@layer` to create component abstractions without CSS overhead
- CSS variables enable dynamic theming aligned with color dimension
- Compose dimensions through utility combinations
- Extend config for brand-specific scales (fonts, colors, animations)

**Avoid**: Relying on default Tailwind palette—define your own at config time.
