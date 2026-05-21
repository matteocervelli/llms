# Frontend Design Svelte

Create distinctive, production-grade Svelte/TypeScript frontends with exceptional design quality.

## Overview

This skill provides a complete framework for building Svelte applications that combine:

- **Intentional Design Thinking**: Foundation before code (purpose, tone, constraints, differentiation)
- **Anti-Generic Aesthetics**: Deliberate rejection of default design patterns
- **Svelte-Native Features**: Transitions, reactivity, scoped styles, stores
- **Production-Grade Quality**: Accessibility, performance, responsive design
- **8-Phase Workflow**: From design thinking through polish

## What This Skill Does

### Design Systems Integration

Integrates five proven design frameworks:

1. **Design Thinking** (pre-coding intent definition)
2. **Base Aesthetics** (5-dimensional design framework)
3. **Typography** (distinctive type pairing and scale)
4. **Motion & Animation** (orchestrated, purposeful movement)
5. **Anti-Patterns** (what NOT to do)

### Svelte-Specific Capabilities

- TypeScript component architecture with strict typing
- Svelte transitions and animations (fade, fly, scale, slide, custom)
- Reactive declarations (`$:`) for dynamic styling and computed values
- Scoped styles with CSS variable theming
- Store-based global state and theme management
- Semantic HTML and ARIA accessibility
- Mobile-first responsive design patterns

### Workflow Phases

1. Design Thinking & Intent Definition
2. Design System & Token Definition
3. Component Architecture & TypeScript Contracts
4. Interaction & Motion Design
5. Responsive Design & Layout System
6. Theming & Color Implementation
7. Accessibility & ARIA Implementation
8. Polish & Performance

## Key Features

### Anti-Generic AI Checklist

Before finalizing, verify:

- ✅ High-contrast typography (not Inter/Roboto defaults)
- ✅ Intentional color palette with unexpected accents
- ✅ Asymmetrical, purposeful layouts
- ✅ Orchestrated motion with easing functions
- ✅ Svelte transitions for smooth animations
- ✅ Reactive declarations for dynamic styling
- ✅ Scoped styles with CSS variables
- ✅ Semantic HTML and ARIA attributes

### Component Examples Included

1. **Animated Card with Hover Delight**: Motion-rich card component with orchestrated reveals
2. **Staggered List Animation**: List with cascading entry animations and accessibility
3. **Typography & Color System**: Design token implementation in CSS and Svelte stores

## Usage

### 1. Start with Design Thinking

Answer the 4 critical questions before writing code:
- What problem are we solving? (Purpose)
- What emotional response do we want? (Tone)
- What are our real constraints? (Constraints)
- What makes this distinctly ours? (Differentiation)

### 2. Define Design System

Create design tokens:
- Typography: Display, body, monospace fonts with size scales
- Colors: Primary, accent, semantic colors
- Spacing: 8px incremental scale
- Motion: Easing functions and durations

### 3. Build Components with TypeScript

```svelte
<script lang="ts">
  import { fade } from 'svelte/transition'

  interface Props {
    title: string
    count: number
  }

  let { title, count }: Props = $props()
</script>

<div in:fade={{ duration: 300 }}>
  <h1>{title}</h1>
  <p>Count: {count}</p>
</div>

<style>
  h1 {
    font-family: var(--font-display);
    color: var(--color-accent);
  }
</style>
```

### 4. Implement Svelte Transitions

Use built-in transitions for orchestrated motion:

```svelte
<script lang="ts">
  import { fly, scale } from 'svelte/transition'
  import { cubicOut, elasticOut } from 'svelte/easing'

  let isVisible = $state(true)
</script>

{#if isVisible}
  <div in:fly={{ y: 50, duration: 600, easing: cubicOut }}>
    Content with orchestrated entry
  </div>
{/if}
```

### 5. Manage Theme with Stores

```svelte
<!-- lib/stores/theme.ts -->
import { writable } from 'svelte/store'

export const isDarkMode = writable(false)
export const theme = writable({
  primary: '#8b4513',
  accent: '#d4a574',
  bg: '#faf8f3',
})
```

### 6. Add Accessibility

```svelte
<nav aria-label="Main navigation">
  <button aria-expanded={isOpen} aria-controls="menu">Menu</button>
  <ul id="menu" hidden={!isOpen}>
    {#each items as item}
      <li><a href={item.href}>{item.label}</a></li>
    {/each}
  </ul>
</nav>
```

## Anti-Patterns to Reject

### Typography
- Don't use Inter/Roboto/Open Sans as primary (use Playfair, Crimson, Space Grotesk instead)
- Don't use incremental size scaling (use 3x+ jumps)
- Don't use mid-range font weights only (use 300/700 vs 400/600)

### Color
- Don't use Material Design trinity (blue, red, green)
- Don't use default SaaS blue everywhere
- Don't use pure neutral grays without personality

### Layout
- Don't center everything (use asymmetrical composition)
- Don't use uniform padding (use intentional spacing scale)
- Don't use "cookie-cutter" grid layouts

### Motion
- Don't use linear timing (use cubic-bezier easing)
- Don't animate everything simultaneously (use staggered reveals)
- Don't make animations slow/sluggish (300-600ms optimal)

### Svelte-Specific
- Don't skip TypeScript in components
- Don't use global styles when scoped styles work
- Don't hardcode colors/sizes (use CSS variables)

## Files Included

```
frontend-design-svelte/
├── SKILL.md          # Complete skill documentation
├── README.md         # This file
└── examples/
    └── showcase.md   # Real-world Svelte component examples
```

## Documentation Structure

### SKILL.md Sections

1. **Purpose & When to Use**
2. **Core Principles** (4 critical design questions)
3. **Anti-Generic AI Standards** (what to reject)
4. **Svelte-Specific Guidance** (TypeScript, transitions, reactivity, stores, accessibility)
5. **8-Phase Development Workflow**
6. **Anti-Generic-AI Checklist**
7. **Component Examples** (animated card, staggered list)
8. **Best Practices & Resources**

### Examples in showcase.md

Real Svelte component examples demonstrating:
- Orchestrated page load animations
- Mobile-first responsive design
- Theme switching with stores
- Accessibility patterns
- Motion-rich interactions

## Design Framework Integration

This skill integrates directly from the design system:

- **design-thinking.md**: Pre-design intentional questioning
- **aesthetics-base.md**: 5-dimensional design framework
- **typography.md**: Font selection, pairing, scale, weights
- **motion.md**: Animation timing, orchestration, easing
- **anti-patterns.md**: Generic design defaults to reject

## Core Svelte Features Leveraged

1. **Reactivity**: `$state`, `$derived`, `$effect` for dynamic styling
2. **Transitions**: Built-in transitions (fade, fly, scale, slide, custom)
3. **Scoped Styles**: Default scoping with `:global()` for shared styles
4. **CSS Variables**: Theme tokens and dynamic values
5. **Stores**: Global state, theme switching, animation control
6. **TypeScript**: Full type safety in components
7. **Semantic HTML**: ARIA labels, roles, proper heading hierarchy

## Quality Standards

All components should pass:

- **Design**: Intentional, non-generic, distinctive personality
- **Accessibility**: WCAG 2.1 AA compliance, keyboard navigation, screen reader support
- **Performance**: Optimized animations, responsive images, Core Web Vitals
- **TypeScript**: Full type coverage, no `any` types
- **Responsiveness**: Mobile-first, tablet-optimized, desktop-enhanced
- **Theming**: CSS variable support, light/dark mode ready

## When to Use This Skill

✅ Building production Svelte/SvelteKit applications
✅ Creating component libraries with design personality
✅ Designing motion-rich, interactive experiences
✅ Prototyping high-fidelity designs in code
✅ Teaching Svelte design best practices

❌ Quick static HTML pages (use frontend-design-html)
❌ React-heavy applications (use frontend-design-react)
❌ Vue applications (use frontend-design-vue)

## Quick Start

1. **Read SKILL.md** thoroughly to understand the full framework
2. **Review examples/showcase.md** for real Svelte patterns
3. **Answer the 4 Design Questions** before coding
4. **Follow the 8-Phase Workflow** for systematic development
5. **Use the Anti-Generic-AI Checklist** before finalizing

## Philosophy

This skill rejects the homogenized aesthetics of default AI-generated design. Every choice—typography, color, layout, motion, spacing—should be deliberate and purposeful, never defaulted.

**Before you code, design with intention. Before you ship, verify distinctiveness.**

---

For integration with other design frameworks or questions about Svelte-specific patterns, refer to SKILL.md.
