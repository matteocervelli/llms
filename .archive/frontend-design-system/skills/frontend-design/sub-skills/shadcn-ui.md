# shadcn/ui: Theming Components for Distinctive Design

shadcn/ui provides copy-paste component primitives built on Radix UI and Tailwind. Customize components completely by theming CSS variables and overriding component logic.

## CSS Variables & Theming

Define design tokens in `globals.css`:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 200 14% 8%;
  --primary: 12 76% 61%;      /* Brand color, not default blue */
  --primary-foreground: 0 0% 100%;
  --accent: 0 84% 60%;         /* Brand accent */
  --border: 200 14% 92%;
  --radius: 0.5rem;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: 200 14% 10%;
    --foreground: 0 0% 98%;
    --primary: 12 76% 45%;
  }
}
```

## Extending Component Styles

Copy shadcn components and extend with custom logic:

```tsx
// Button.tsx - Override default shadcn button
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-all",
  {
    variants: {
      variant: {
        primary: "bg-primary text-white hover:shadow-lg active:scale-95",
        outline: "border border-primary text-primary hover:bg-primary/5",
        subtle: "bg-primary/10 text-primary hover:bg-primary/20",
      },
      size: {
        sm: "px-2 py-1 text-sm",
        md: "px-4 py-2 text-base",
        lg: "px-6 py-3 text-lg",
      },
    },
  }
)

export const Button = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement> & VariantProps<typeof buttonVariants>
>(({ className, variant = "primary", size = "md", ...props }, ref) => (
  <button
    ref={ref}
    className={buttonVariants({ variant, size, className })}
    {...props}
  />
))
```

## Applying Design Dimensions

**Typography**: Use custom font families in components
```tsx
<h1 className="font-serif text-3xl">Custom Heading</h1>
<p className="font-sans text-base leading-relaxed">Body text</p>
```

**Color**: Override HSL tokens for brand alignment
```css
--primary: 12 76% 61%;  /* Brand-specific, not default */
--accent: 0 84% 60%;
```

**Spacing**: Customize component padding/gaps via Tailwind
```tsx
<Card className="p-8 gap-6">  <!-- Custom spacing from dimension -->
```

**Motion**: Add animations to interactive states
```tsx
className="transition-all duration-200 hover:shadow-lg active:scale-95"
```

**Composition**: Responsive grid layouts in component layouts
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
```

## Component Theming Strategy

1. **Copy component from registry** to `components/ui/`
2. **Define CSS variables** in `globals.css` aligned with design dimensions
3. **Extend variants** in component file using CVA
4. **Compose with Tailwind** utilities for fine-tuning
5. **Document custom variants** for team consistency

## Dark Mode

```tsx
// Automatic via class strategy
<html className={isDark ? 'dark' : ''}>
  {/* CSS variables automatically switch via @media (prefers-color-scheme) */}
</html>
```

## Dimension Connections

- [Typography System](../dimension-sub-skills/typography.md)
- [Color & Theme](../dimension-sub-skills/color-theme.md)
- [Motion & Animation](../dimension-sub-skills/motion.md)
- [Spatial Compositions](../dimension-sub-skills/spatial-compositions.md)

## Key Takeaways

- shadcn/ui components are **yours to customize**—copy and extend
- CSS variables decouple design tokens from hardcoded values
- CVA (class-variance-authority) enables variant management
- Layer custom components on top of shadcn base
- Always extend, never override package source

**Strategy**: Use shadcn as base primitives; theme aggressively with CSS variables.
