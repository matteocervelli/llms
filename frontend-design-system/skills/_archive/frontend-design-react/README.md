# Frontend Design React Skill

Create distinctive, production-grade React frontends with TypeScript and exceptional design quality.

## Overview

This skill provides a comprehensive framework for building React applications that reject default design patterns and embrace intentional, distinctive aesthetics. It integrates:

- **5-Dimension Design Framework**: Typography, Color, Motion, Spatial Composition, Visual Details
- **React/TypeScript Best Practices**: Functional components, hooks, proper typing
- **Framer Motion Orchestration**: State-driven animations with orchestrated timing
- **Accessibility-First**: WCAG 2.1 AA compliance, semantic HTML, proper ARIA
- **Mobile-First Responsive**: Touch-friendly interactions, responsive layouts
- **Design Thinking Process**: Pre-coding intentional direction and differentiation

## Quick Start

### 1. Design Thinking Phase (Complete First)

Answer these four questions **before** writing any code:

```markdown
**Purpose**: What problem are we solving? Who are we solving it for?
**Tone**: What emotional response do we want?
**Constraints**: What are the real technical, temporal, or business limits?
**Differentiation**: What one unforgettable element makes this distinctly ours?
```

### 2. Stack Requirements

```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "framer-motion": "^10.0.0",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0"
  },
  "optional": {
    "styled-components": "for CSS-in-JS",
    "css-modules": "for scoped CSS"
  }
}
```

### 3. Typography Setup

Choose one high-contrast typeface pairing:

```typescript
// 1. Load fonts from Google Fonts
const fonts = `https://fonts.googleapis.com/css2?family=Playfair+Display:wght@300;400;700&family=IBM+Plex+Sans:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap`

// 2. Create typography tokens
const typography = {
  display: { size: '88px', weight: 700, family: 'Playfair Display' },
  headline: { size: '48px', weight: 700, family: 'Playfair Display' },
  body: { size: '16px', weight: 400, family: 'IBM Plex Sans' },
}

// 3. Apply to components with size jumps (3x+), not incremental scaling
```

### 4. Color System

Define colors with intentionality, not defaults:

```typescript
const colors = {
  // Warm palette example
  primary: '#8B4513',        // Cognac brown
  secondary: '#D4623F',      // Terracotta
  accent: '#E6D52F',         // Sulfur yellow (the surprising element)
  neutral: { 100: '#FAF8F4', 200: '#E8E3DB', 300: '#D4C5B5' },
}
```

### 5. Motion Setup with Framer Motion

```typescript
import { motion } from 'framer-motion';

// Define reusable animation variants
const pageLoad = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
};

// Use in components
<motion.div variants={pageLoad} initial="hidden" animate="visible">
  Content with orchestrated reveals
</motion.div>
```

## Workflow: 8-Phase Process

### Phase 1: Design Thinking (30 min)
Complete pre-design checklist. Define purpose, tone, constraints, differentiation.

### Phase 2: Typography (1-2 hours)
- Select high-contrast typeface pairing
- Create size scale with 3x+ jumps
- Set up CSS-in-JS tokens

### Phase 3: Color & Theme (1-2 hours)
- Define emotional intent
- Create color system with CSS variables
- Plan dark mode if needed

### Phase 4: Motion (1-2 hours)
- Identify animation opportunities
- Plan Framer Motion sequences
- Define easing curves

### Phase 5: Spatial Composition (1-2 hours)
- Design asymmetrical layouts
- Define spacing scale
- Create component structure

### Phase 6: Visual Details (1 hour)
- Design subtle backgrounds
- Add texture/patterns
- Create micro-details

### Phase 7: Implementation (2-4 hours)
- Build React components with TypeScript
- Apply Framer Motion animations
- Implement CSS-in-JS styling
- Optimize performance

### Phase 8: Validation (1 hour)
- Design review
- Accessibility review (WCAG 2.1 AA)
- Performance optimization
- Mobile responsiveness testing

## Key Principles

### ✅ Do This

- **Typography**: Playfair Display + IBM Plex Sans + JetBrains Mono (distinctive pairs)
- **Colors**: Unexpected palettes (burnt orange, cognac, terracotta + sulfur yellow accent)
- **Motion**: Orchestrated reveals with staggered timing and easing
- **Layout**: Asymmetrical, intentional composition
- **Details**: Subtle gradients, texture overlays, micro-illustrations
- **Accessibility**: Semantic HTML, ARIA labels, keyboard support
- **Types**: Full TypeScript with proper interfaces
- **Performance**: React.memo, useCallback, useMemo

### ❌ Avoid This

- **Fonts**: Inter, Roboto, Open Sans (defaults)
- **Colors**: Material Design blues/reds/greens, pure grays
- **Motion**: Linear timing, instant interactions, animation overload
- **Layout**: Centered, symmetrical, "default SaaS dashboard"
- **Details**: Bland backgrounds, obvious gradients, busy patterns
- **Accessibility**: No ARIA, non-semantic markup
- **Motion**: No easing, no orchestration
- **Code**: Untyped props, no memoization

## Component Template

```typescript
import { motion } from 'framer-motion';
import styled from 'styled-components';
import React, { useCallback } from 'react';

interface ComponentProps {
  title: string;
  description: string;
  onAction?: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

const StyledComponent = styled(motion.div)`
  padding: 24px;
  border-radius: 8px;
  background: ${props => props.$variant === 'primary'
    ? '#FAF8F4'
    : '#F0E8DC'};
  border: 1px solid #D4C5B5;
`;

export const Component: React.FC<ComponentProps> = React.memo(({
  title,
  description,
  onAction,
  variant = 'primary',
  disabled = false
}) => {
  const handleClick = useCallback(() => {
    onAction?.();
  }, [onAction]);

  return (
    <StyledComponent
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={!disabled ? { y: -4 } : undefined}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      role="article"
      aria-label={title}
    >
      <h2>{title}</h2>
      <p>{description}</p>
      {onAction && (
        <button
          onClick={handleClick}
          disabled={disabled}
          aria-label={`${title} action`}
        >
          Take Action
        </button>
      )}
    </StyledComponent>
  );
});

Component.displayName = 'Component';
```

## Testing Checklist

- [ ] Does typography use distinctive fonts (3x+ size jumps)?
- [ ] Is color palette custom and intentional?
- [ ] Are animations orchestrated with easing?
- [ ] Is layout asymmetrical and interesting?
- [ ] Do hover states surprise?
- [ ] Is WCAG 2.1 AA compliance met?
- [ ] Does it pass Lighthouse accessibility score?
- [ ] Is responsive design mobile-first?
- [ ] Do animations add value, not distraction?
- [ ] Would you describe this as "intentional" or "generic"?

## Resources

- **SKILL.md**: Full framework, principles, and patterns
- **examples/showcase.md**: Complete React component examples
- **Framer Motion**: https://www.framer.com/motion/
- **Google Fonts**: https://fonts.google.com
- **Easing Functions**: https://easings.net/
- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/

## Examples

See `/examples/showcase.md` for:
1. Distinctive Typography Component
2. Framer Motion Orchestrated Page Load
3. Unexpected Layout with Grid/Flexbox
4. Accessible Interactive Component
5. Mobile-First Responsive Design

---

**Remember**: The difference between generic and intentional design is deciding deliberately instead of defaulting. Every choice should serve the problem you're solving, not the easiest pattern available.
