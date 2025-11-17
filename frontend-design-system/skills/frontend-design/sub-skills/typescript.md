# TypeScript for Design Systems Sub-Skill

## Overview
Type-safe patterns for design tokens, component props, animations, and theme configuration. Enables compile-time design system validation.

## Design Token Types

```typescript
// src/tokens/types.ts
export type ColorValue = string & { readonly __brand: 'ColorValue' }
export type SpacingValue = string & { readonly __brand: 'SpacingValue' }
export type MotionValue = string & { readonly __brand: 'MotionValue' }

export interface ColorToken {
  50: ColorValue
  100: ColorValue
  500: ColorValue
  900: ColorValue
}

export interface SpacingScale {
  xs: SpacingValue   // 4px
  sm: SpacingValue   // 8px
  md: SpacingValue   // 16px
  lg: SpacingValue   // 24px
  xl: SpacingValue   // 32px
  '2xl': SpacingValue // 48px
}

export interface DesignTokens {
  colors: Record<'primary' | 'secondary', ColorToken>
  spacing: SpacingScale
  duration: Record<'fast' | 'base' | 'slow', number>
  easing: Record<'easeOut' | 'easeIn', string>
}
```

## Theme Token Factory

```typescript
// src/tokens/design-tokens.ts
import { ColorToken, SpacingScale, DesignTokens } from './types'

const createColorToken = (base: string): ColorToken => ({
  50: `${base}50` as ColorValue,
  100: `${base}100` as ColorValue,
  500: `${base}500` as ColorValue,
  900: `${base}900` as ColorValue,
})

export const designTokens: DesignTokens = {
  colors: {
    primary: createColorToken('--color-primary-'),
    secondary: createColorToken('--color-secondary-'),
  },
  spacing: {
    xs: 'var(--space-xs)' as SpacingValue,
    sm: 'var(--space-sm)' as SpacingValue,
    md: 'var(--space-md)' as SpacingValue,
    lg: 'var(--space-lg)' as SpacingValue,
    xl: 'var(--space-xl)' as SpacingValue,
    '2xl': 'var(--space-2xl)' as SpacingValue,
  },
  duration: {
    fast: 150,
    base: 300,
    slow: 500,
  },
  easing: {
    easeOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    easeIn: 'cubic-bezier(0.4, 0, 0.6, 1)',
  },
}

export type Theme = typeof designTokens
```

## Component Prop Typing for Variants

```typescript
// src/components/Button.tsx
import { FC, ReactNode } from 'react'

type ButtonVariant = 'primary' | 'secondary' | 'danger'
type ButtonSize = 'sm' | 'md' | 'lg'

interface ButtonProps {
  variant?: ButtonVariant
  size?: ButtonSize
  disabled?: boolean
  children: ReactNode
  onClick?: () => void
}

export const Button: FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  children,
  onClick,
}) => {
  return (
    <button
      className={`button button--${variant} button--${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// Ensures only valid combinations
type ValidButtonProps = ButtonProps & {
  variant: Exclude<ButtonVariant, 'invalid'>
  size: ButtonSize
}
```

## Type-Safe Animation Configuration

```typescript
// src/animations/types.ts
import { Variants } from 'framer-motion'

export interface AnimationConfig {
  duration: number
  delay?: number
  ease: 'easeOut' | 'easeIn' | 'easeInOut'
}

export const createMotionVariants = (
  config: AnimationConfig
): Variants => ({
  hidden: {
    opacity: 0,
    y: 20,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: config.duration,
      delay: config.delay ?? 0,
      ease: config.ease,
    },
  },
})

// Usage
const fadeInUp = createMotionVariants({
  duration: 0.6,
  delay: 0.1,
  ease: 'easeOut',
})
```

## Framer Motion Type Integration

```typescript
// src/animations/orchestration.ts
import { Variants, TargetAndTransition } from 'framer-motion'
import { designTokens } from '../tokens/design-tokens'

interface PageLoadSequence {
  staggerChildren: number
  delayChildren: number
}

export const createContainerVariants = (
  sequence: PageLoadSequence
): Variants => ({
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: sequence.staggerChildren,
      delayChildren: sequence.delayChildren,
    },
  },
})

// Type-safe timing from tokens
const timing: TargetAndTransition = {
  duration: designTokens.duration.base / 1000,
  ease: designTokens.easing.easeOut,
}
```

## Design System Utility Types

```typescript
// src/utils/design-types.ts
export type Breakpoint = 'mobile' | 'tablet' | 'desktop' | 'wide'

export interface ResponsiveValue<T> {
  mobile: T
  tablet?: T
  desktop?: T
  wide?: T
}

export const mapResponsive = <T,>(
  values: ResponsiveValue<T>,
  breakpoint: Breakpoint
): T => {
  return values[breakpoint] ?? values.mobile
}

// Usage in components
const padding: ResponsiveValue<string> = {
  mobile: designTokens.spacing.md,
  tablet: designTokens.spacing.lg,
  desktop: designTokens.spacing.xl,
}
```

## Theming with TypeScript

```typescript
// src/theme/theme-provider.tsx
import { createContext, useContext } from 'react'
import { DesignTokens, designTokens } from '../tokens/design-tokens'

export type ThemeMode = 'light' | 'dark'

interface ThemeContextType {
  mode: ThemeMode
  tokens: DesignTokens
  toggle: () => void
}

const ThemeContext = createContext<ThemeContextType | null>(null)

export const useTheme = (): ThemeContextType => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

## Related Documentation
- [React + Vite Implementation](./react-vite.md)
- [CSS/SCSS Implementation](./css-scss.md)
- [Color & Theme Dimension](../../../design-references/color-palettes.md)
- [Motion Patterns Dimension](../../../design-references/motion-patterns.md)
