# Frontend Design Orchestrator

This is the **entry point** skill for creating distinctive, production-grade frontends using a modular, dimension-based approach.

## What This Is

A **composable design system** that separates:
- **5 universal design dimensions** (typography, color, motion, spatial, backgrounds)
- **Tech-specific implementations** (React, Vue, Svelte, HTML/CSS)
- **Design system integrations** (Tailwind, shadcn/ui, Radix, Material)

Instead of generic AI design, you get intentional, distinctive frontends by applying each dimension strategically.

---

## Quick Start

### Choose Your Technology

```
React + Vite?        → frontend-design-react/SKILL.md
Vue?                 → frontend-design-vue/SKILL.md
Svelte?              → frontend-design-svelte/SKILL.md
Plain HTML/CSS?      → frontend-design-html/SKILL.md

Need to fix existing? → frontend-design-fix-{framework}/SKILL.md
```

### Then Follow the 8-Phase Workflow

1. **Design Thinking** – Answer: purpose, tone, constraints, one unforgettable element
2. **Typography** – Reject defaults, use high-contrast pairs, employ weight extremes
3. **Color & Theme** – Define emotional intent, avoid cliché palettes
4. **Motion** – Plan orchestrated animations with intentional easing
5. **Spatial Composition** – Create asymmetrical layouts with breathing room
6. **Backgrounds & Details** – Add subtle textures and micro-details
7. **Implementation** – Use your tech-specific skill guide
8. **Validation** – Check design, accessibility, performance, mobile

---

## The 5 Dimensions Explained

### 1. Typography (The Primary Carrier of Voice)

**Typefaces to Use:**
- Display: Playfair Display, Crimson Pro, Bricolage Grotesque
- Body: IBM Plex Sans, Space Grotesk, Crimson Pro
- Mono: JetBrains Mono, Fira Code, IBM Plex Mono

**Typefaces to Reject:**
- ❌ Inter, Roboto, Open Sans, Lato, system fonts (these are ubiquitous in AI design)

**Strategy:**
- Create high-contrast pairings: Display + Mono, Serif + Geometric Sans
- Use weight extremes: 300/700/900 (not 400/500/600)
- Apply 3x+ size jumps: Display 88px → Headline 48px → Body 16px
- Never use incremental scaling (48 → 40 → 32)

### 2. Color & Theme (Sets Mood and Coherence)

**Strategy:**
- Define emotional intent (warm, cool, energetic, calm)
- Move beyond default systems (Material trinity, Tailwind defaults)
- Use unexpected but harmonious color relationships
- Reserve one accent color for personality

**To Avoid:**
- ❌ Blue/Red/Green default palette
- ❌ Pure grays without warmth or personality
- ❌ Monochrome soulless gradients
- ❌ Oversaturated neon accents

### 3. Motion (Reveals Personality, Guides Attention)

**Strategy:**
- Orchestrate page loads with staggered timing (100ms, 200ms, 300ms)
- Add scroll triggers for engaged scrolling
- Include delightful hover surprises
- Use easing functions (ease-out, ease-in-out, elastic)

**To Avoid:**
- ❌ Linear timing on everything (robotic)
- ❌ No animation at all (cold, instant)
- ❌ Animation-heavy design that distracts
- ❌ Slow, sluggish transitions (2s+)

### 4. Spatial Composition (Creates Rhythm, Guides the Eye)

**Strategy:**
- Use asymmetrical layouts (more interesting than grid-perfect)
- Create breathing room with generous whitespace
- Build spacing scale: 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Avoid centered, symmetrical, "default SaaS" layouts

**To Avoid:**
- ❌ Everything centered (predictable)
- ❌ Uniform padding everywhere
- ❌ Layouts that could describe "generic SaaS dashboard"

### 5. Backgrounds & Visual Details (The Memorable Foundation)

**Strategy:**
- Support content, don't distract
- Add subtle details that reward observation
- Use subtle gradients (2-3 colors, minimal contrast)
- Create texture via digital patterns or noise (2-5% opacity)

**To Avoid:**
- ❌ Bland white backgrounds
- ❌ Obvious rainbow gradients
- ❌ Busy patterns competing with content
- ❌ Decorative elements serving no purpose

---

## Example Workflows

### Scenario: Building a SaaS Dashboard in React

1. **Design Thinking** – Purpose: Help busy professionals. Tone: calm confidence. Differentiation: warm serif typography.
2. **Typography** – Playfair Display (headings) + IBM Plex Sans (body) + JetBrains Mono (data)
3. **Color** – Warm palette: burnt orange, sage green, warm neutrals
4. **Motion** – Staggered card reveals on load, smooth hover elevations
5. **Spatial** – Asymmetrical dashboard grid, 24px/32px spacing
6. **Backgrounds** – Soft cream background with subtle diagonal gradient
7. **Implementation** – Follow `frontend-design-react/SKILL.md`
8. **Validation** – Accessibility check, mobile responsiveness, performance review

### Scenario: Static Marketing Site in HTML/CSS

1. **Design Thinking** – Purpose: Attract creative professionals. Tone: bold, unconventional. Differentiation: unexpected color accent (sulfur yellow).
2. **Typography** – Bricolage Grotesque (display) + Space Grotesk (body)
3. **Color** – Deep indigo base + sulfur yellow accent
4. **Motion** – Scroll-triggered reveals, smooth hover states via CSS transitions
5. **Spatial** – Asymmetrical hero section, offset image layouts
6. **Backgrounds** – Subtle texture overlay, geometric SVG patterns
7. **Implementation** – Follow `frontend-design-html/SKILL.md`
8. **Validation** – Cross-browser testing, mobile optimization

---

## Key Principles

1. **Composition Over Decoration** – Every design choice serves the user
2. **Intentionality Over Defaults** – Reject auto-generated patterns
3. **Contrast Over Harmony** – Typography, colors, and layouts should surprise
4. **Movement Over Static** – Animation serves purpose, not distraction
5. **Personality Over Professionalism** – Distinctive > Safe

---

## Architecture

```
frontend-design/
├── SKILL.md                  ← You are here (orchestrator)
├── README.md                 ← This file (quick start)
└── sub-skills/
    ├── typography.md         ← Full typography guidance
    ├── color-theme.md        ← Color systems & psychology
    ├── motion.md             ← Animation & easing patterns
    ├── spatial.md            ← Layout & composition
    ├── backgrounds.md        ← Gradients & textures
    └── design-thinking.md    ← Pre-design checklist

framework-specific:
├── frontend-design-react/    ← React + Vite + TypeScript
├── frontend-design-vue/      ← Vue 3 + Composition API
├── frontend-design-svelte/   ← Svelte + custom animations
├── frontend-design-html/     ← HTML + CSS/SCSS
├── frontend-design-fix-react/    ← Fix existing React
├── frontend-design-fix-vue/      ← Fix existing Vue
├── frontend-design-fix-svelte/   ← Fix existing Svelte
└── frontend-design-fix-html/     ← Fix existing HTML
```

---

## When to Use This Skill

✅ Building a distinctive frontend that doesn't look AI-generated
✅ Need guidance on design dimensions and composition
✅ Creating a consistent design language across pages
✅ Want to avoid generic SaaS design patterns
✅ Implementing intentional motion and micro-interactions

---

## Next Steps

1. **Open `SKILL.md`** for the complete framework
2. **Pick your tech** (React/Vue/Svelte/HTML)
3. **Complete the design thinking checklist** (before coding)
4. **Follow the 8-phase workflow**
5. **Reference each dimension's sub-skill** as you build

---

## Resources

- **Typography Theory**: "Thinking with Type" by Ellen Lupton
- **Color Psychology**: Emotional associations and cultural meanings
- **Motion Design**: Orchestration, choreography, easing principles
- **Spacing Systems**: Modular scale calculators, golden ratio
- **Accessibility**: WCAG 2.1 Level AA compliance guidelines
