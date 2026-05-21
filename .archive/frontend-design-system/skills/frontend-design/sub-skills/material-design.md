# Material Design: Customizing Beyond Defaults

Material Design provides opinionated component patterns. Override Material conventions to create distinctive brands while retaining its accessibility and motion principles.

## Customizing Material Theme

Use Material Design's theming system, but define non-default tokens:

```tsx
// theme.ts
import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    primary: {
      main: '#0F172A',      // Brand slate, not blue
      light: '#1E293B',
      dark: '#000000',
    },
    secondary: {
      main: '#DC2626',      // Brand red accent
    },
    background: {
      default: '#FFFFFF',
      paper: '#F8FAFC',
    },
    text: {
      primary: '#0F172A',
      secondary: '#64748B',
    },
  },
  typography: {
    fontFamily: '"Inter", "Helvetica", "Arial", sans-serif',
    h1: {
      fontFamily: '"Crimson Text", serif',
      fontSize: '2.5rem',
      fontWeight: 600,
      lineHeight: 1.2,
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
      letterSpacing: '0.3px',
    },
  },
  shape: {
    borderRadius: 8,  // Override default rounded corners
  },
})

export default theme
```

## Breaking Material Conventions

Material defaults to bold, colorful design. Override for subtlety:

```tsx
// Custom button beyond Material spec
const CustomButton = styled(Button)(({ theme }) => ({
  textTransform: 'none',  // Don't uppercase all caps
  boxShadow: 'none',      // Remove default elevation
  border: '1px solid #E2E8F0',
  padding: '10px 16px',
  '&:hover': {
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    backgroundColor: '#F1F5F9',
  },
}))
```

## Typography Beyond Material

Define custom type scales:

```tsx
typography: {
  h1: { fontSize: '3rem', fontWeight: 700, fontFamily: 'Crimson Text' },
  h2: { fontSize: '2rem', fontWeight: 600 },
  body1: { fontSize: '1rem', lineHeight: 1.6 },
  caption: { fontSize: '0.875rem', color: '#64748B' },
},
```

## Theming with CSS Variables

Layer Material with CSS variable overrides:

```css
/* globals.css */
:root {
  --primary: #0F172A;
  --accent: #DC2626;
  --neutral: #64748B;
  --radius: 8px;
}

/* Override Material inline */
.MuiButton-root {
  border-radius: var(--radius);
  text-transform: none;
}

.MuiCard-root {
  background-color: var(--background);
  border: 1px solid #E2E8F0;
}
```

## Applying Design Dimensions

**Typography**: Custom font scales in typography config
```tsx
typography: {
  h1: { fontFamily: 'Crimson Text', fontSize: '2.5rem' },
  body1: { fontFamily: 'Inter', lineHeight: 1.6 },
}
```

**Color**: Override palette with brand tokens
```tsx
palette: {
  primary: { main: '#0F172A' },
  secondary: { main: '#DC2626' },
}
```

**Spacing**: Custom spacing scale in theme
```tsx
spacing: (factor) => `${0.25 * factor}rem`,
// spacing(4) = 1rem, spacing(8) = 2rem
```

**Motion**: Custom transitions respecting prefers-reduced-motion
```tsx
transitions: {
  easing: { easeInOutCubic: 'cubic-bezier(0.4, 0, 0.2, 1)' },
  duration: { short: 200, standard: 300 },
}
```

**Composition**: Grid system with custom breakpoints
```tsx
breakpoints: {
  xs: 0, sm: 480, md: 768, lg: 1024, xl: 1440,
}
```

## When to Use Material vs Custom

**Choose Material when:**
- Complex data tables required
- Accessibility audits needed out-of-box
- Team familiar with Material patterns
- Admin/enterprise UI

**Choose custom when:**
- Strong brand identity required
- Minimal, elegant aesthetic desired
- Less standard component density
- User-facing consumer product

## Combining Material + Custom Components

```tsx
import { ThemeProvider } from '@mui/material/styles'
import { Button as MaterialButton } from '@mui/material'
import { Button as CustomButton } from './CustomButton'

export const App = () => (
  <ThemeProvider theme={theme}>
    {/* Use Material for complex, data-dense UIs */}
    <MaterialButton variant="contained">Material</MaterialButton>

    {/* Use Custom for hero, brand moments */}
    <CustomButton variant="primary">Custom</CustomButton>
  </ThemeProvider>
)
```

## Dimension Connections

- [Typography System](../dimension-sub-skills/typography.md)
- [Color & Theme](../dimension-sub-skills/color-theme.md)
- [Motion & Animation](../dimension-sub-skills/motion.md)
- [Spatial Compositions](../dimension-sub-skills/spatial-compositions.md)

## Key Takeaways

- Material provides structure; customize tokens aggressively
- Override elevation, radius, and color to match brand
- Use Material's motion system—it's based on easing research
- CSS variables enable runtime theming and dark mode
- Hybrid approach: Material for complex UI, custom for brand

**Strategy**: Extend Material theme, not override components (cleaner upgrades).
