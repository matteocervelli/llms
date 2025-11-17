# Frontend Design Fix - React

## Quick Start

This skill helps you transform generic React component designs into visually distinctive interfaces using Anthropic's 5 design dimensions.

### What This Skill Does

1. **Analyzes** your current React components for generic design patterns
2. **Audits** against anti-patterns (bland typography, purple gradients, centered layouts, etc.)
3. **Applies** aesthetic upgrades across:
   - Typography (distinctive fonts, extreme weights, size jumps, responsive sizing)
   - Color & Theme (cohesive palettes, theme providers, accent colors, dark mode)
   - Motion (Framer Motion orchestration, staggered reveals, hover interactions)
   - Spatial Composition (asymmetric layouts, broken grids, intentional overlap)
   - Backgrounds (layered gradients, textures, atmospheric depth)

### When to Use

Use this skill when you have:
- Existing React components that feel generic or bland
- Components using default fonts (Inter, Roboto, Arial)
- Solid color backgrounds
- No animations or micro-interactions
- Centered, predictable layouts
- Purple/blue gradients on white

### Basic Workflow

```
1. Provide your React component files
2. Skill analyzes and scores against checklist
3. Dimensions are fixed one at a time
4. Theme provider and design tokens added
5. Framer Motion animations integrated
6. Before/after comparison generated
7. Accessibility verified
```

## Design Dimensions Explained

### Typography
**Problem**: Generic system fonts in limited weights, no responsive scaling
**Solution**: Distinctive pairs, extreme weights (100-900), 3x size jumps, responsive sizing with CSS-in-JS

### Color & Theme
**Problem**: Purple gradients, no theming, evenly distributed colors, no dark mode
**Solution**: Theme provider, CSS variables, dominant + accent colors, 70-20-10 rule, light/dark variants

### Motion
**Problem**: No animations, abrupt transitions, no micro-interactions
**Solution**: Framer Motion orchestration, staggered reveals, hover surprises, scroll-triggered animations

### Spatial Composition
**Problem**: Centered, symmetrical, predictable layouts
**Solution**: Asymmetry, intentional overlap, broken grids, generous/controlled spacing

### Backgrounds
**Problem**: Solid colors, no depth
**Solution**: Layered gradients, patterns/textures, atmospheric effects, contextual depth

## Example: Before & After

### Before (Generic React Component)
```jsx
import React from 'react';

export function LandingHero() {
  return (
    <div style={{
      textAlign: 'center',
      padding: '40px 20px',
      background: 'white'
    }}>
      <h1 style={{
        fontSize: '2rem',
        fontFamily: 'Arial, sans-serif',
        color: 'purple'
      }}>
        Welcome
      </h1>
      <button style={{
        padding: '10px 20px',
        background: '#e0e0e0',
        border: 'none'
      }}>
        Click Me
      </button>
    </div>
  );
}
```

**Anti-pattern Score**: 5/5 items on checklist

### After (Distinctive React Component)
```jsx
import React, { useState } from 'react';
import { motion } from 'framer-motion';

// Theme configuration
const theme = {
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
  transitions: {
    fast: 200,
    base: 400,
  }
};

// Create motion variants for orchestration
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: 'easeOut' },
  },
};

export function LandingHero() {
  const [isHovering, setIsHovering] = useState(false);

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      style={{
        background: `linear-gradient(135deg, ${theme.colors.surface} 0%, #e8e8e8 100%)`,
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        justifyContent: 'center',
        padding: '2rem',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Decorative background element */}
      <motion.div
        style={{
          position: 'absolute',
          top: '-10%',
          right: '-5%',
          width: '400px',
          height: '400px',
          background: 'radial-gradient(circle, rgba(255, 107, 53, 0.1) 0%, transparent 70%)',
          borderRadius: '50%',
          zIndex: 0,
        }}
        animate={{
          y: [0, 20, 0],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />

      {/* Content container */}
      <motion.div
        style={{
          position: 'relative',
          zIndex: 1,
          maxWidth: '600px',
        }}
        variants={itemVariants}
      >
        <motion.h1
          style={{
            fontFamily: theme.fonts.display,
            fontSize: 'clamp(2.5rem, 8vw, 5rem)',
            fontWeight: 900,
            color: theme.colors.primary,
            margin: 0,
            marginBottom: '1rem',
            lineHeight: 1.1,
            letterSpacing: '-0.02em',
          }}
        >
          Welcome to Something Remarkable
        </motion.h1>

        <motion.p
          style={{
            fontFamily: theme.fonts.body,
            fontSize: 'clamp(1rem, 2vw, 1.25rem)',
            color: theme.colors.primary,
            opacity: 0.7,
            lineHeight: 1.6,
            marginBottom: '2rem',
          }}
          variants={itemVariants}
        >
          Discover what happens when design meets intention.
        </motion.p>

        <motion.button
          style={{
            fontFamily: theme.fonts.body,
            background: theme.colors.accent,
            color: 'white',
            padding: '1rem 2rem',
            border: 'none',
            borderRadius: '2px',
            fontSize: '1.125rem',
            fontWeight: 600,
            cursor: 'pointer',
            transition: `all ${theme.transitions.base}ms ease-out`,
          }}
          variants={itemVariants}
          whileHover={{
            y: -4,
            boxShadow: `0 20px 40px rgba(255, 107, 53, 0.3)`,
          }}
          whileTap={{ scale: 0.95 }}
        >
          Discover More
        </motion.button>
      </motion.div>

      {/* Accent element */}
      <motion.div
        style={{
          position: 'absolute',
          bottom: '2rem',
          right: '2rem',
          width: '120px',
          height: '2px',
          background: theme.colors.accent,
        }}
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ delay: 0.8, duration: 0.6 }}
      />
    </motion.div>
  );
}
```

**Anti-pattern Score**: 0/5 items on checklist

### Improvements
- [x] Typography: Playfair Display (display) + Inter (body), responsive sizing with clamp()
- [x] Color: Theme object, CSS variables via style props, accent color (#ff6b35)
- [x] Motion: Framer Motion orchestration, staggered children, hover effects, floating element
- [x] Spatial: Left-aligned content (asymmetry), layered with absolute positioning
- [x] Background: Linear gradient + floating accent element with radial gradient

## Key React Patterns

### Theme Provider
```jsx
import React, { createContext, useContext } from 'react';

const ThemeContext = createContext({});

export function ThemeProvider({ children }) {
  const theme = {
    colors: {
      primary: '#1a1a1a',
      accent: '#ff6b35',
      surface: '#fafafa',
    },
    fonts: {
      display: "'Playfair Display', serif",
      body: "'Inter', sans-serif",
    },
  };

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
```

### Framer Motion Orchestration
```jsx
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function List({ items }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map(item => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.title}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Responsive Typography with Tailwind
```jsx
export function Heading({ children }) {
  return (
    <h1 className="
      font-['Playfair_Display']
      text-4xl md:text-5xl lg:text-6xl
      font-black
      leading-tight
      text-slate-900
    ">
      {children}
    </h1>
  );
}
```

### Styled Components with Theme
```jsx
import styled from 'styled-components';

const StyledButton = styled.button`
  font-family: ${props => props.theme.fonts.body};
  background: ${props => props.theme.colors.accent};
  color: white;
  padding: 1rem 2rem;
  border: none;
  transition: all 0.3s ease-out;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 20px 40px ${props => props.theme.colors.accent}30;
  }

  &:focus {
    outline: 3px solid ${props => props.theme.colors.accent};
    outline-offset: 2px;
  }
`;
```

## Accessibility

```jsx
// Always use semantic elements
<button>Submit</button>

// Provide focus states
style={{
  outline: '3px solid var(--accent)',
  outlineOffset: '2px',
}}

// Maintain color contrast (4.5:1 minimum for WCAG AA)
color: '#1a1a1a';  /* WCAG AA on #fafafa */

// Use aria-labels when needed
<button aria-label="Close menu">×</button>
```

## Popular React Design Libraries

- **Framer Motion**: Animation library
- **Tailwind CSS**: Utility-first CSS
- **styled-components**: CSS-in-JS
- **Radix UI**: Unstyled accessible components
- **Headless UI**: Tailwind-compatible components

## Tools & Resources

- **Font Pairing**: Google Fonts, Adobe Fonts, Variable Fonts
- **Color Tools**: Coolors.co, Contrast Checker, ColorSpace
- **Animation**: Framer Motion, React Spring, React Use Gesture
- **Accessibility**: WAVE, AXLE DevTools, Lighthouse, React Testing Library

## Next Steps

1. **Wrap your app** in ThemeProvider
2. **Start with typography** dimension
3. **Add Framer Motion** for orchestrated animations
4. **Implement color tokens** as CSS variables or theme object
5. **Test accessibility** with React Testing Library

See `/examples/showcase.md` for complete before/after examples with React.
