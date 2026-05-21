# Frontend Design Fix - Svelte

## Quick Start

This skill helps you transform generic Svelte component designs into visually distinctive interfaces using Anthropic's 5 design dimensions.

### What This Skill Does

1. **Analyzes** your current Svelte components for generic design patterns
2. **Audits** against anti-patterns (bland typography, purple gradients, centered layouts, etc.)
3. **Applies** aesthetic upgrades across:
   - Typography (distinctive fonts, extreme weights, size jumps, responsive sizing)
   - Color & Theme (cohesive palettes, stores, accent colors, dark mode)
   - Motion (Svelte transitions, animations, scroll-triggered effects)
   - Spatial Composition (asymmetric layouts, broken grids, intentional overlap)
   - Backgrounds (layered gradients, textures, atmospheric depth)

### When to Use

Use this skill when you have:
- Existing Svelte components that feel generic or bland
- Components using default fonts (Inter, Roboto, Arial)
- Solid color backgrounds
- No animations or transitions
- Centered, predictable layouts
- Purple/blue gradients on white

### Basic Workflow

```
1. Provide your Svelte component files (.svelte)
2. Skill analyzes and scores against checklist
3. Dimensions are fixed one at a time
4. Theme store created
5. Svelte transitions integrated
6. Before/after comparison generated
7. Accessibility verified
```

## Design Dimensions Explained

### Typography
**Problem**: Generic system fonts in limited weights, no responsive scaling
**Solution**: Distinctive pairs, extreme weights (100-900), 3x size jumps, responsive sizing with CSS

### Color & Theme
**Problem**: Purple gradients, no theming, evenly distributed colors, no dark mode
**Solution**: Svelte stores, CSS custom properties, dominant + accent colors, light/dark variants

### Motion
**Problem**: No animations, abrupt transitions, no micro-interactions
**Solution**: Svelte transitions, animations, scroll-triggered effects, hover interactions

### Spatial Composition
**Problem**: Centered, symmetrical, predictable layouts
**Solution**: Asymmetry, intentional overlap, broken grids, generous/controlled spacing

### Backgrounds
**Problem**: Solid colors, no depth
**Solution**: Layered gradients, patterns/textures, atmospheric effects, contextual depth

## Example: Before & After

### Before (Generic Svelte Component)
```svelte
<script>
</script>

<div class="hero">
  <h1>Welcome</h1>
  <button>Click Me</button>
</div>

<style>
.hero {
  text-align: center;
  padding: 40px 20px;
  background: white;
}

h1 {
  font-size: 2rem;
  font-family: Arial, sans-serif;
  color: purple;
}

button {
  padding: 10px 20px;
  background: #e0e0e0;
  border: none;
}
</style>
```

**Anti-pattern Score**: 5/5 items on checklist

### After (Distinctive Svelte Component)
```svelte
<script>
  import { onMount } from 'svelte';
  import { theme } from '$lib/stores/theme.js';

  let isVisible = false;
  let isButtonHovering = false;

  onMount(() => {
    isVisible = true;
  });

  const handleClick = () => {
    console.log('CTA clicked');
  };
</script>

<div class="hero" style="
  --font-display: {$theme.fonts.display};
  --font-body: {$theme.fonts.body};
  --primary: {$theme.colors.primary};
  --accent: {$theme.colors.accent};
  --surface: {$theme.colors.surface};
">
  <!-- Decorative background element -->
  <div class="background-element" />

  <!-- Content with transition -->
  {#if isVisible}
    <div class="content" transition:fadeUp>
      <h1 class="headline">Welcome to Something Remarkable</h1>

      <p class="description">
        Discover what happens when design meets intention.
      </p>

      <button
        class="cta-button"
        on:click={handleClick}
        on:mouseenter={() => isButtonHovering = true}
        on:mouseleave={() => isButtonHovering = false}
      >
        Discover More
      </button>
    </div>
  {/if}

  <!-- Accent line -->
  {#if isVisible}
    <div class="accent-line" transition:scaleX />
  {/if}
</div>

<style>
  :root {
    --font-display: 'Playfair Display', serif;
    --font-body: 'Inter', sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
    --primary: #1a1a1a;
    --accent: #ff6b35;
    --surface: #fafafa;
  }

  .hero {
    background: linear-gradient(135deg, var(--surface) 0%, #e8e8e8 100%);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    padding: 2rem;
    position: relative;
    overflow: hidden;
  }

  .background-element {
    position: absolute;
    top: -10%;
    right: -5%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255, 107, 53, 0.1) 0%, transparent 70%);
    border-radius: 50%;
    z-index: 0;
    animation: float 6s ease-in-out infinite;
  }

  .content {
    position: relative;
    z-index: 1;
    max-width: 600px;
  }

  .headline {
    font-family: var(--font-display);
    font-size: clamp(2.5rem, 8vw, 5rem);
    font-weight: 900;
    color: var(--primary);
    margin: 0 0 1rem 0;
    line-height: 1.1;
    letter-spacing: -0.02em;
  }

  .description {
    font-family: var(--font-body);
    font-size: clamp(1rem, 2vw, 1.25rem);
    color: var(--primary);
    opacity: 0.7;
    line-height: 1.6;
    margin-bottom: 2rem;
  }

  .cta-button {
    font-family: var(--font-body);
    background: var(--accent);
    color: white;
    padding: 1rem 2rem;
    border: none;
    border-radius: 2px;
    font-size: 1.125rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease-out;
    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.2);
  }

  .cta-button:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(255, 107, 53, 0.3);
  }

  .cta-button:focus {
    outline: 3px solid var(--accent);
    outline-offset: 2px;
  }

  .accent-line {
    position: absolute;
    bottom: 2rem;
    right: 2rem;
    width: 120px;
    height: 2px;
    background: var(--accent);
    animation: scaleInLine 0.6s ease-out 0.8s both;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(20px); }
  }

  @keyframes scaleInLine {
    from { transform: scaleX(0); }
    to { transform: scaleX(1); }
  }
</style>

<script context="module">
  export const fadeUp = (node, { duration = 600 } = {}) => {
    return {
      duration,
      css: (t) => {
        const easeOut = 1 - Math.pow(1 - t, 3);
        return `
          opacity: ${t};
          transform: translateY(${(1 - t) * 20}px);
        `;
      },
    };
  };

  export const scaleX = (node, { duration = 600, delay = 800 } = {}) => {
    return {
      duration,
      delay,
      css: (t) => {
        const easeOut = 1 - Math.pow(1 - t, 3);
        return `transform: scaleX(${easeOut});`;
      },
    };
  };
</script>
```

**Anti-pattern Score**: 0/5 items on checklist

### Improvements
- [x] Typography: Playfair Display (display) + Inter (body), responsive sizing with clamp()
- [x] Color: CSS custom properties, accent color (#ff6b35), layered gradient background
- [x] Motion: Svelte transitions (fadeUp, scaleX), animations, hover effects
- [x] Spatial: Left-aligned content (asymmetry), layered with absolute positioning
- [x] Background: Linear gradient + floating element with radial gradient

## Key Svelte Patterns

### Theme Store
```javascript
// src/lib/stores/theme.js
import { writable } from 'svelte/store';

export const theme = writable({
  colors: {
    primary: '#1a1a1a',
    accent: '#ff6b35',
    surface: '#fafafa',
    background: '#ffffff',
  },
  fonts: {
    display: "'Playfair Display', serif",
    body: "'Inter', sans-serif",
    mono: "'IBM Plex Mono', monospace",
  },
});

export function toggleDarkMode() {
  theme.update(t => ({
    ...t,
    colors: {
      primary: '#f5f5f5',
      accent: '#ff6b35',
      surface: '#1a1a1a',
      background: '#0a0a0a',
    },
  }));
}
```

### Using Theme in Components
```svelte
<script>
  import { theme } from '$lib/stores/theme.js';
</script>

<div style="
  --primary: {$theme.colors.primary};
  --accent: {$theme.colors.accent};
  --surface: {$theme.colors.surface};
  --font-display: {$theme.fonts.display};
  --font-body: {$theme.fonts.body};
">
  <button style="background: {$theme.colors.accent}">
    Click Me
  </button>
</div>
```

### Staggered List with Animations
```svelte
<script>
  let items = [
    { id: 1, content: 'Item 1' },
    { id: 2, content: 'Item 2' },
    { id: 3, content: 'Item 3' },
  ];

  const staggerAnimation = (node, { index = 0, duration = 400 } = {}) => {
    return {
      delay: index * 100,
      duration,
      css: (t) => {
        return `
          opacity: ${t};
          transform: translateY(${(1 - t) * 20}px);
        `;
      },
    };
  };
</script>

<div class="list-container">
  {#each items as item, i (item.id)}
    <div
      class="list-item"
      transition:staggerAnimation={{ index: i }}
    >
      {item.content}
    </div>
  {/each}
</div>

<style>
  .list-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .list-item {
    padding: 1rem;
    border-radius: 0.5rem;
    background: var(--surface);
    color: var(--primary);
  }
</style>
```

### Scroll-Triggered Animations
```svelte
<script>
  let isVisible = false;

  function handleIntersection(e) {
    const target = e.target;
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        isVisible = true;
        observer.unobserve(target);
      }
    });
    observer.observe(target);
  }
</script>

<div
  use:handleIntersection
  class:visible={isVisible}
  class="scroll-element"
>
  Appears when scrolled into view
</div>

<style>
  .scroll-element {
    opacity: 0;
    transform: translateY(40px);
    transition: all 0.6s ease-out;
  }

  .scroll-element.visible {
    opacity: 1;
    transform: translateY(0);
  }
</style>
```

### Custom Transition Functions
```svelte
<script>
  const fadeSlideIn = (node, { duration = 400 } = {}) => {
    return {
      duration,
      css: (t) => {
        const easeOut = 1 - Math.pow(1 - t, 3);
        return `
          opacity: ${easeOut};
          transform: translateX(${(1 - easeOut) * -20}px);
        `;
      },
    };
  };
</script>

<div transition:fadeSlideIn>
  Content with fade and slide-in animation
</div>
```

## Accessibility

```svelte
<!-- Always use semantic elements -->
<button on:click={handleAction}>Submit</button>

<!-- Provide focus states -->
<style>
  button:focus {
    outline: 3px solid var(--accent);
    outline-offset: 2px;
  }
</style>

<!-- Use aria-labels when needed -->
<button aria-label="Close menu">×</button>

<!-- Maintain color contrast (4.5:1 minimum for WCAG AA) -->
```

## Svelte Animation Directives

```svelte
<!-- Transition in/out -->
<div transition:fade>Content</div>

<!-- Custom duration -->
<div transition:fade={{ duration: 600 }}>Content</div>

<!-- Animate between list changes -->
<div animate:flip={{ duration: 200 }}>Reordered item</div>

<!-- Multiple transitions -->
<div in:fadeIn out:slideOut>Content</div>
```

## Popular Svelte Design Tools

- **Tailwind CSS**: Utility-first CSS
- **Svelte Animate**: Built-in animation utilities
- **Svelte Motion**: Spring and tweened animations
- **Motion One**: Animation library for Svelte
- **svelte-use**: Custom hooks and utilities

## Tools & Resources

- **Font Pairing**: Google Fonts, Adobe Fonts, Variable Fonts
- **Color Tools**: Coolors.co, Contrast Checker, ColorSpace
- **Animation**: Svelte Animate, Motion One, Animate.css
- **Accessibility**: WAVE, AXLE DevTools, Lighthouse, Vitest

## Next Steps

1. **Create theme store** with Svelte stores
2. **Define CSS custom properties** for theme variables
3. **Start with typography** dimension
4. **Add Svelte transitions** for page load and interactions
5. **Implement custom transitions** for sophisticated effects
6. **Test accessibility** with Vitest

See `/examples/showcase.md` for complete before/after examples with Svelte.
