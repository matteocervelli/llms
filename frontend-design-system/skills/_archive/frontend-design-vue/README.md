# Frontend Design Vue Skill

Create distinctive, production-grade Vue 3/TypeScript frontends with exceptional design quality.

## Quick Start

This skill enables you to build Vue 3 applications that:
- Avoid generic AI design patterns through intentional choices
- Use Vue 3 Composition API with full TypeScript support
- Implement sophisticated animations with @vueuse/motion
- Manage themes with Provide/Inject pattern
- Build accessible, semantic components
- Deploy production-grade responsive design

## When to Use This Skill

Use this skill when you need to:
- Build a new Vue 3 frontend from scratch
- Create distinctive, non-generic UI components
- Implement sophisticated motion and animation
- Establish a complete design system with Vue
- Build accessible, production-grade frontends
- Apply intentional typography, color, and spacing

## What's Included

The skill contains:

1. **Complete Design Framework** (5 dimensions)
   - Typography with intentional typeface selection
   - Color & theme management with CSS variables
   - Motion & animation with orchestrated timing
   - Spatial composition and layout strategy
   - Background & visual details for personality

2. **Design Thinking Methodology**
   - Pre-coding workflow (Purpose, Tone, Constraints, Differentiation)
   - Design decision framework
   - Anti-patterns to avoid
   - Quality checklists

3. **Vue 3 Implementation Patterns**
   - Composition API with `<script setup>` and TypeScript
   - Single File Components (.vue files)
   - @vueuse/motion for orchestrated animations
   - Scoped styles with CSS variables
   - Reactive design with ref() and reactive()
   - Provide/Inject for theme management
   - Accessibility-first semantic HTML
   - Mobile-first responsive design

4. **Complete Workflow** (8 phases)
   - Phase 1: Design Thinking & Strategy
   - Phase 2: Typography System
   - Phase 3: Color System & Theme
   - Phase 4: Spacing & Layout
   - Phase 5: Motion & Animation
   - Phase 6: Component Architecture
   - Phase 7: Accessibility & Semantics
   - Phase 8: Polish & Performance

5. **Anti-Generic-AI Checklist**
   - Vue 3 specific checks
   - Typography validation
   - Color palette review
   - Motion evaluation
   - Layout assessment
   - Accessibility verification

## Core Principles

### No Generic Defaults

Every design decision should be intentional, never defaulted:
- Reject Inter, Roboto, Open Sans as primary typefaces
- Create custom color palettes with personality
- Use asymmetrical layouts instead of centered grids
- Implement easing functions, never linear timing
- Add motion that serves purpose, not distraction

### Vue 3 First

Always use modern Vue 3 patterns:
- Composition API with `<script setup>`
- TypeScript for full type safety
- Single File Components (.vue files)
- Provide/Inject for theme management
- @vueuse/motion for sophisticated animations

### Design-Code Integration

Design and code are inseparable:
- Define design tokens as CSS variables
- Implement them in Vue composables
- Test across all device sizes
- Validate accessibility
- Document design rationale

## Example Usage

### 1. Start with Design Thinking

Answer the pre-design questions:
```
Purpose: What problem are we solving? Who are we solving it for?
Tone: What emotional response do we want?
Constraints: What are our technical/temporal/business limits?
Differentiation: What one unforgettable element makes this ours?
```

### 2. Build Typography System

```vue
<script setup lang="ts">
// Use CSS variables for all typographic values
// Establish size scale with 3x+ jumps
// Select 2-3 distinctive typefaces
</script>

<style scoped>
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --size-display: 88px;
  --size-heading: 48px;
  --size-subheading: 28px;
  --size-body: 16px;
  --size-caption: 12px;

  --weight-thin: 300;
  --weight-regular: 400;
  --weight-bold: 700;
  --weight-heavy: 900;
}
</style>
```

### 3. Implement Theme Management

```vue
<!-- App.vue -->
<script setup lang="ts">
import { provide } from 'vue'

interface Theme {
  primaryColor: string
  accentColor: string
  backgroundColor: string
}

const theme: Theme = {
  primaryColor: '#004e89',
  accentColor: '#ff6b35',
  backgroundColor: '#fffbf7'
}

provide('theme', theme)
</script>
```

### 4. Build Components with Motion

```vue
<script setup lang="ts">
import { useMotion } from '@vueuse/motion'
import { ref } from 'vue'

const card = ref()

useMotion(card, {
  initial: { opacity: 0, y: 20 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 100,
      delay: 100
    }
  }
})
</script>

<template>
  <div ref="card" class="card">
    <!-- Component content -->
  </div>
</template>

<style scoped>
.card {
  will-change: opacity, transform;
}
</style>
```

### 5. Ensure Accessibility

```vue
<template>
  <nav role="navigation" aria-label="Main navigation">
    <button
      type="button"
      aria-label="Toggle menu"
      :aria-expanded="menuOpen"
      @click="menuOpen = !menuOpen"
    >
      ☰
    </button>
  </nav>

  <main id="main-content" role="main">
    <h1>Page Title</h1>

    <form @submit.prevent="handleSubmit">
      <label for="email">Email Address</label>
      <input
        id="email"
        v-model="email"
        type="email"
        aria-required="true"
        aria-describedby="email-help"
      >
      <p id="email-help" class="help-text">
        We'll never share your email.
      </p>
    </form>
  </main>
</template>
```

## Key Technologies

- **Vue 3**: Modern reactive framework
- **TypeScript**: Full type safety
- **@vueuse/motion**: Orchestrated animations
- **Vite**: Lightning-fast dev server
- **CSS Variables**: Theme management
- **Intersection Observer**: Scroll triggers
- **ARIA/Semantics**: Accessibility

## Design Dimensions

### 1. Typography
- High-contrast typeface pairings
- Weight extremes (300/700/900, not 400/500/600)
- Size jumps of 3x+, not incremental scaling
- Intentional selection, never defaulted

### 2. Color
- Custom palettes with psychological intent
- Saturation and tone variations
- One unexpected accent color
- Intentional light/dark mode (not inversion)

### 3. Motion
- Orchestrated timing (staggered, not simultaneous)
- Easing functions (not linear)
- Purpose-driven animation
- Hover surprises that delight

### 4. Spatial Composition
- Asymmetrical, non-centered layouts
- Generous whitespace
- Consistent spacing scale
- Visual rhythm through intentional spacing

### 5. Visual Details
- Subtle gradients (2-3 colors, 40-60°)
- Illustrated patterns and texture
- Micro-interactions
- Details that reward observation

## Workflow

Follow the 8-phase implementation workflow for consistent results:

1. **Design Thinking & Strategy**: Answer pre-design questions
2. **Typography System**: Define fonts and scales
3. **Color System & Theme**: Create intentional palette
4. **Spacing & Layout**: Build responsive grid
5. **Motion & Animation**: Add orchestrated interaction
6. **Component Architecture**: Build reusable parts
7. **Accessibility & Semantics**: Ensure WCAG compliance
8. **Polish & Performance**: Optimize and verify

## Anti-Patterns to Avoid

**Typography**: Inter, Roboto, Open Sans as primary; incremental size scaling; mid-range weights only

**Color**: Material Design trinity; pure grays; monochrome everything; oversaturated accents

**Layout**: Centered everything; uniform padding; card+image patterns; stacked boxes

**Motion**: Linear timing; no animation; animation-heavy; slow sluggish transitions

**Details**: Bland white backgrounds; obvious gradients; busy patterns; generic illustrations

## Validation Checklist

Before shipping, verify:

- [ ] Typography is distinctive, not generic
- [ ] Color palette has personality and unexpected accents
- [ ] Layout is asymmetrical with breathing room
- [ ] Motion uses easing functions and serves purpose
- [ ] All components are fully accessible (WCAG AA+)
- [ ] Responsive design tested on mobile, tablet, desktop
- [ ] Performance metrics pass (Lighthouse 90+)
- [ ] Would you describe this as "intentional" or "generic"?

## Resources

- [SKILL.md](./SKILL.md) - Complete technical reference
- [examples/](./examples/) - Working component examples
- [Vue 3 Docs](https://vuejs.org)
- [@vueuse/motion](https://motion.vueuse.org)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## Next Steps

1. Read [SKILL.md](./SKILL.md) for complete technical guidance
2. Review [examples/](./examples/) for working components
3. Follow the 8-phase workflow for your project
4. Use the anti-generic-AI checklist before shipping
5. Reference design dimensions when making decisions
