---
description: Create a UI Component in /components/ui with variants, tests, and preview
argument-hint: <component-name> <component-summary>
---

# Create UI Component

Create a production-ready UI component with TypeScript, variants, comprehensive tests, and preview integration.

## What it does

1. Parses component name and summary from arguments
2. Creates component file with TypeScript and variants
3. Generates comprehensive test file
4. Adds component to preview page
5. Runs quality checks (linting, type checking, tests)
6. Verifies accessibility compliance

## Usage

```bash
/ui-component Button "Primary action button with variants"
/ui-component Modal "Dialog component for user interactions"
/ui-component Input "Text input field with validation"
```

**💡 Tip:** For safer planning, activate Plan Mode (press Shift+Tab twice) before running this command to review the component structure before creation.

## Context

Parse $ARGUMENTS to extract:
- **[name]**: Component name (converted to PascalCase)
- **[summary]**: Component purpose/description

Example: `/ui-component Card "Display content in a card layout"`
- [name] = Card
- [summary] = Display content in a card layout

## Component Creation

### File Structure

Create in: `src/components/ui/[name]/[name].tsx`

```typescript
import { FC } from 'react';

interface [name]Props {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  className?: string;
  children?: React.ReactNode;
}

/**
 * [name] Component
 *
 * [summary]
 *
 * @example
 * ```tsx
 * <[name] variant="primary" size="md">
 *   Content here
 * </[name]>
 * ```
 */
export const [name]: FC<[name]Props> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  className,
  children,
}) => {
  // Implementation
  return (
    <div
      className={cn(baseStyles, variantStyles[variant], sizeStyles[size], className)}
      aria-disabled={disabled}
    >
      {children}
    </div>
  );
};
```

### Required Variants

Use theme colors from @src/app/globals.css:

1. **primary** - Main brand color (primary action)
2. **secondary** - Secondary brand color (less emphasis)
3. **success** - Success/confirmation actions (green)
4. **danger** - Destructive/error actions (red)
5. **warning** - Caution/warning states (orange)

### Required Sizes

- **sm** - Small (mobile-optimized, compact spaces)
- **md** - Medium (default, balanced)
- **lg** - Large (desktop emphasis, hero sections)

### Required States

- **disabled** - Inactive/non-interactive state
- **hover** - Mouse hover state
- **focus** - Keyboard focus state
- **active** - Pressed/active state
- **loading** (if applicable) - Async operation in progress

## Testing

### Create Test File

Location: `src/components/ui/[name]/[name].test.tsx`

Reference: @src/components/ui/Button/Button.test.tsx

```typescript
import { render, screen } from '@testing-library/react';
import { [name] } from './[name]';

describe('[name]', () => {
  it('renders without crashing', () => {
    render(<[name]>Test</[name]>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('renders all variants correctly', () => {
    const variants = ['primary', 'secondary', 'success', 'danger', 'warning'];
    variants.forEach(variant => {
      const { container } = render(<[name] variant={variant}>Test</[name]>);
      expect(container.firstChild).toHaveClass(variant);
    });
  });

  it('renders all sizes correctly', () => {
    const sizes = ['sm', 'md', 'lg'];
    sizes.forEach(size => {
      const { container } = render(<[name] size={size}>Test</[name]>);
      expect(container.firstChild).toHaveClass(size);
    });
  });

  it('handles disabled state', () => {
    render(<[name] disabled>Test</[name]>);
    expect(screen.getByText('Test')).toHaveAttribute('aria-disabled', 'true');
  });

  it('accepts custom className', () => {
    const { container } = render(<[name] className="custom">Test</[name]>);
    expect(container.firstChild).toHaveClass('custom');
  });
});
```

### Run Tests

```bash
!npm run test -- [name].test.tsx
!npm run test:coverage -- [name]
```

Iterate until all tests pass with >80% coverage.

## Preview Integration

Add to `src/app/preview/page.tsx`:

```typescript
import { [name] } from '@/components/ui/[name]/[name]';

// In preview page component
<section className="preview-section">
  <h2>[name] Component</h2>

  {/* Variants */}
  <div className="preview-grid">
    <[name] variant="primary">Primary</[name]>
    <[name] variant="secondary">Secondary</[name]>
    <[name] variant="success">Success</[name]>
    <[name] variant="danger">Danger</[name]>
    <[name] variant="warning">Warning</[name]>
  </div>

  {/* Sizes */}
  <div className="preview-grid">
    <[name] size="sm">Small</[name]>
    <[name] size="md">Medium</[name]>
    <[name] size="lg">Large</[name]>
  </div>

  {/* States */}
  <div className="preview-grid">
    <[name] disabled>Disabled</[name]>
  </div>
</section>
```

⚠️ **Important**: Do NOT add the component to any other page.

## Quality Checks

Run before completion:

```bash
# Linting
!npm run lint
!npm run lint -- --fix

# Type checking
!npm run typecheck
!tsc --noEmit

# Testing
!npm run test -- [name]
!npm run test:coverage

# Build verification
!npm run build
```

## Accessibility Requirements

### Semantic HTML
- Use appropriate HTML elements (`<button>`, `<input>`, etc.)
- Avoid `<div>`/`<span>` for interactive elements

### ARIA Attributes
```typescript
aria-label="[Descriptive label]"
aria-disabled={disabled}
aria-describedby="[description-id]"
role="[appropriate-role]"
```

### Keyboard Navigation
- **Tab**: Move focus to/from component
- **Enter/Space**: Activate component (if interactive)
- **Escape**: Close/cancel (if modal/dialog)
- **Arrow keys**: Navigate options (if applicable)

### Focus Management
```css
&:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 2px;
}
```

### Screen Reader Support
- Meaningful text alternatives
- Announce state changes
- Logical reading order

### Accessibility Checklist
- [ ] WCAG 2.1 AA compliant
- [ ] Keyboard navigable
- [ ] Screen reader compatible
- [ ] Sufficient color contrast (4.5:1 minimum)
- [ ] Focus indicators visible
- [ ] ARIA attributes present

## Examples

### Example 1: Button Component

```bash
/ui-component Button "Primary action button"
```

**Creates:**
- Component with click handling
- All 5 variants (primary, secondary, success, danger, warning)
- 3 sizes (sm, md, lg)
- Disabled state
- Loading state (optional)

### Example 2: Modal Component

```bash
/ui-component Modal "Dialog for user interactions"
```

**Creates:**
- Modal with overlay
- Close button with keyboard support
- Focus trap when open
- Escape key to close
- Scroll lock when open

### Example 3: Input Component

```bash
/ui-component Input "Text input with validation"
```

**Creates:**
- Input with label
- Error state and message
- Helper text support
- Required indicator
- Validation feedback

### Example 4: Card Component

```bash
/ui-component Card "Content container with shadow"
```

**Creates:**
- Card with padding and shadow
- Header, body, footer sections
- Hover state
- Clickable variant (if needed)

## Tips

### Component Design
- ✅ **Keep it simple**: Single responsibility per component
- ✅ **Composable**: Build complex UIs from simple components
- ✅ **Flexible**: Accept className for custom styling
- ✅ **Typed**: Use TypeScript for prop validation
- ✅ **Documented**: Add JSDoc comments

### Styling Best Practices
- Use CSS modules or Tailwind for styling
- Follow project naming conventions
- Use CSS custom properties for theming
- Avoid inline styles (use className)
- Support dark mode if applicable

### Testing Strategy
- Test all variants and sizes
- Test interactive states (hover, focus, disabled)
- Test keyboard navigation
- Test with screen readers
- Test edge cases (empty, long content, etc.)

### Accessibility
- Always include ARIA labels
- Support keyboard navigation
- Ensure sufficient color contrast (4.5:1 minimum)
- Test with screen reader
- Use semantic HTML

### Performance
- Keep components pure (no side effects)
- Memoize expensive computations
- Lazy load large components
- Optimize re-renders with React.memo

## Related Commands

- `/code-quality` - Run linting, type checking, tests before commit
- `/pr-creation` - Create PR after component complete
- `/feature` - Implement larger feature with component
