# Base Aesthetics Framework

## Overview

This is the core 5-dimension framework for creating intentional, non-generic design that avoids the homogenized aesthetic of default AI outputs. Each dimension works together to create designs with personality and deliberation.

## The Five Dimensions

### 1. Typography Dimension

**Purpose**: Typography is the primary carrier of voice and personality in digital design.

**Core Principles**:
- Typeface selection creates immediate emotional context
- Font pairings establish visual hierarchy and rhythm
- Weight and size extremes create contrast and emphasis
- Avoid: Inter, Roboto, Open Sans, Lato, system fonts (these are default AI outputs)
- Prefer: JetBrains Mono, Fira Code, Space Grotesk, Playfair Display, Crimson Pro, IBM Plex, Bricolage Grotesque

**Implementation**:
- Use high-contrast pairings: Display + Mono, Serif + Geometric Sans
- Employ weight extremes: 100/200 vs 800/900 (not mid-range weights)
- Apply size jumps of 3x or more, not incremental 1.5x steps
- Create visual hierarchy through deliberate typographic choices

**Example Pattern**:
- Display: Playfair Display (300, 400, 700)
- Body: IBM Plex Sans (400, 600)
- Mono: JetBrains Mono (400, 500)

### 2. Color & Theme Dimension

**Purpose**: Color sets mood and creates visual coherence while avoiding cliché palettes.

**Core Principles**:
- Move beyond default color systems (Material Design, Tailwind defaults)
- Use unexpected but harmonious color relationships
- Consider context: what emotional response do you want?
- Saturation and tone matter as much as hue

**Anti-Patterns to Avoid**:
- Primaries: Blue, Red, Green (default AI trinity)
- Neutrals: Pure grays (#999999, #CCCCCC) without personality
- Monochrome gradients that feel soulless
- Color palettes that match "flat design" clichés

**Implementation**:
- Define color intent: Is this a warm, cool, energetic, or calm system?
- Use color psychology intentionally
- Create contrast through saturation, not just hue
- Reserve one unexpected accent color for personality

**Example Approach**:
- Warm palette: Cognac browns, terracotta, warm neutrals with olive undertones
- Cool palette: Deep indigos, soft teals, cool grays with blue undertones
- Accent: Single unexpected color for UI elements (e.g., sulfur yellow, coral pink)

### 3. Motion Dimension

**Purpose**: Motion reveals personality and guides user attention with intentionality.

**Core Principles**:
- Motion should feel deliberate, not random
- Orchestrate page loads with staggered timing
- Use scroll triggers for engaged scrolling experiences
- Hover states should surprise, not just respond

**Implementation**:
- **HTML/CSS**: CSS-only animations with easing functions (ease-in-out, cubic-bezier)
- **React**: Motion library (Framer Motion, Popmotion) for state-driven animation
- Page load: Stagger reveals with animation-delay (100ms, 200ms, 300ms)
- Scroll triggers: Elements animate in when viewport enters
- Hover: Add transforms, color shifts, or subtle scale changes

**Anti-Patterns**:
- Linear timing on everything (feels robotic)
- Instantaneous interactions (feels cold)
- Animation-heavy design that distracts from content

### 4. Spatial Composition Dimension

**Purpose**: Space and layout create rhythm and guide the eye through intentional composition.

**Core Principles**:
- Use asymmetrical layouts when possible (more interesting than grid-perfect)
- Create breathing room with generous whitespace
- Build visual rhythm through consistent spacing systems
- Avoid centered, symmetrical layouts unless purposeful

**Implementation**:
- Define a spacing scale: 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Use odd-numbered layouts: 3-column, 5-item, 7-section
- Create focal points through compositional weight
- Consider micro-interactions within spatial relationships

**Anti-Patterns**:
- Everything centered (feels safe but predictable)
- Uniform padding everywhere
- Layouts that could describe "generic SaaS dashboard"

### 5. Backgrounds & Visual Details Dimension

**Purpose**: The foundation layer that can transform a generic design into something memorable.

**Core Principles**:
- Background should support, not distract
- Add subtle details that reward close observation
- Use gradients intentionally, not as default effects
- Create texture through digital or illustrated means

**Implementation**:
- Subtle gradients: Use 2-3 colors with minimal contrast (40-60° angles)
- Illustrated patterns: Geometric, organic, or custom SVG elements
- Texture overlays: Subtle noise or grain (2-5% opacity)
- Micro-illustrations: Small graphics that reinforce brand voice

**Anti-Patterns**:
- Bland white backgrounds (consider soft colors instead)
- Obvious gradients (rainbow, neon contrasts)
- Busy patterns that compete with content
- Decorative elements that serve no purpose

## Anti-Generic-AI Guardrails

Use these checks to ensure your design doesn't default to generic AI output:

**Typography Check**:
- [ ] Does the typeface choice feel intentional or like a default?
- [ ] Are size jumps extreme (3x+) or incremental?
- [ ] Do font pairings create surprise and interest?

**Color Check**:
- [ ] Could this palette exist in a Material Design system?
- [ ] Do the colors feel chosen or randomly selected?
- [ ] Is there one unexpected accent color that creates personality?

**Motion Check**:
- [ ] Does animation feel orchestrated or reactive?
- [ ] Are timing curves deliberate or linear?
- [ ] Do hover states surprise or just respond?

**Spatial Check**:
- [ ] Is the layout asymmetrical or cookie-cutter centered?
- [ ] Does whitespace feel generous or cramped?
- [ ] Could the layout be described as "standard SaaS"?

**Background Check**:
- [ ] Is the background supporting or distracting?
- [ ] Are gradients subtle or obvious?
- [ ] Do visual details reward close observation?

## Implementation Order

1. **Define Purpose**: What problem are you solving? Who are your users?
2. **Choose Typography**: Select 2-3 typefaces that reflect your tone
3. **Create Color System**: Define palette around emotional intent
4. **Plan Motion**: Identify opportunities for orchestrated animation
5. **Design Spacing**: Create layout with intentional asymmetry
6. **Add Details**: Layer in backgrounds, patterns, and micro-interactions

## References

- Anthropic research on non-generic AI design
- Typography principles: Advanced concepts in type design
- Color theory: Emotional context and psychological associations
- Motion design: Orchestration and choreography principles
