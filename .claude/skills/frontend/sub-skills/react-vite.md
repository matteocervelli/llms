# React 18+ with Vite Sub-Skill

## Overview
Production-grade React 18+ setup using Vite bundler, TypeScript, Framer Motion for animations, and CSS/SCSS styling without CSS-in-JS.

## Project Structure

```
src/
├── components/          # React components
├── styles/              # Global SCSS files
├── tokens/              # Design tokens (TypeScript)
├── pages/               # Page components
└── lib/                 # Utilities & helpers
```

## Vite Configuration

```javascript
// vite.config.ts
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import './src/styles/variables.scss';`
      }
    }
  },
  server: {
    port: 5173
  }
})
```

## TypeScript & React Setup

```typescript
// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles/global.scss'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## Component Pattern with Design Tokens

```typescript
// src/components/Button.tsx
import { FC, ReactNode } from 'react'
import { getSpacing, getColor } from '../tokens/design-tokens'
import styles from './Button.module.scss'

interface ButtonProps {
  variant: 'primary' | 'secondary'
  size: 'sm' | 'md' | 'lg'
  children: ReactNode
}

export const Button: FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children
}) => {
  const padding = getSpacing(size)
  const backgroundColor = getColor(variant)

  return (
    <button
      className={`${styles.button} ${styles[variant]} ${styles[size]}`}
      style={{ padding }}
    >
      {children}
    </button>
  )
}
```

## Font Loading in Vite

```html
<!-- index.html -->
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
```

## Color System with CSS Variables

```scss
// src/styles/colors.scss
:root {
  --color-primary: #1e40af;
  --color-secondary: #06b6d4;
  --color-text: #1f2937;
  --color-bg: #ffffff;
  --color-border: #e5e7eb;
}

[data-theme="dark"] {
  --color-primary: #60a5fa;
  --color-secondary: #22d3ee;
  --color-text: #f3f4f6;
  --color-bg: #111827;
  --color-border: #374151;
}
```

## Framer Motion Orchestrated Page Load

```typescript
// src/pages/Home.tsx
import { motion } from 'framer-motion'
import styles from './Home.module.scss'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
      delayChildren: 0.1,
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: 'easeOut' }
  }
}

export default function Home() {
  return (
    <motion.main
      className={styles.container}
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      <motion.h1 variants={itemVariants}>Welcome</motion.h1>
      <motion.p variants={itemVariants}>Explore design excellence</motion.p>
    </motion.main>
  )
}
```

## Implementation Across 5 Dimensions

### Typography (See typography.md)
- Font stack via CSS variables
- Scale via SCSS mixins
- Line height rhythm via spatial scale

### Color (See color-theme.md)
- CSS custom properties for theming
- Dark mode via [data-theme] selector
- Contrast validation via tokens

### Motion (See motion.md)
- Framer Motion orchestration
- Spring physics for natural movement
- Stagger timings tied to rhythm

### Spatial (See spatial.md)
- CSS Grid/Flexbox layouts
- Spacing scale via design tokens
- Responsive via mobile-first SCSS

### Backgrounds (See backgrounds.md)
- CSS gradients with color tokens
- Pattern overlays via CSS
- Layering via z-index tokens

## Related Documentation
- [Typography Dimension](../../../design-references/typography.md)
- [Color & Theme Dimension](../../../design-references/color-palettes.md)
- [Motion Patterns Dimension](../../../design-references/motion-patterns.md)
- [Spatial Composition Dimension](../../../design-references/spatial-compositions.md)
