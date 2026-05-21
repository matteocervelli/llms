# Component Scaffold Template

## File Structure

```
src/components/ui/[name]/
  [name].tsx          # Component implementation
  [name].test.tsx     # Tests (all variants, states, keyboard nav)
```

## Component Template

```typescript
import { FC } from 'react';

interface [Name]Props {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  className?: string;
  children?: React.ReactNode;
}

export const [Name]: FC<[Name]Props> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  className,
  children,
}) => {
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

## Required Variants

| Variant     | Purpose                   | Color  |
| ----------- | ------------------------- | ------ |
| `primary`   | Main brand action         | Brand  |
| `secondary` | Less emphasis             | Muted  |
| `success`   | Confirmation actions      | Green  |
| `danger`    | Destructive/error actions | Red    |
| `warning`   | Caution states            | Orange |

## Required Sizes

| Size | Use Case                         |
| ---- | -------------------------------- |
| `sm` | Mobile-optimized, compact spaces |
| `md` | Default, balanced                |
| `lg` | Desktop emphasis, hero sections  |

## Required States

- **disabled** — Inactive, `aria-disabled="true"`
- **hover** — Mouse hover visual feedback
- **focus** — Keyboard focus, `outline: 2px solid; outline-offset: 2px`
- **active** — Pressed/active state
- **loading** — Async operation (if applicable)

## Test Template

```typescript
import { render, screen } from '@testing-library/react';
import { [Name] } from './[Name]';

describe('[Name]', () => {
  it('renders without crashing', () => {
    render(<[Name]>Test</[Name]>);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('renders all variants', () => {
    const variants = ['primary', 'secondary', 'success', 'danger', 'warning'];
    variants.forEach(variant => {
      const { container } = render(<[Name] variant={variant}>Test</[Name]>);
      expect(container.firstChild).toHaveClass(variant);
    });
  });

  it('handles disabled state', () => {
    render(<[Name] disabled>Test</[Name]>);
    expect(screen.getByText('Test')).toHaveAttribute('aria-disabled', 'true');
  });

  it('is keyboard navigable', () => {
    render(<[Name]>Test</[Name]>);
    const el = screen.getByText('Test');
    el.focus();
    expect(el).toHaveFocus();
  });
});
```

## Accessibility Checklist

- [ ] Semantic HTML (no div/span for interactive elements)
- [ ] ARIA attributes (`aria-label`, `aria-disabled`, `aria-describedby`)
- [ ] Keyboard navigation (Tab, Enter/Space, Escape, Arrow keys)
- [ ] Focus indicators (`outline: 2px solid`, `:focus-visible`)
- [ ] WCAG 2.1 AA color contrast (4.5:1 minimum)

## Preview Integration

Add to `src/app/preview/page.tsx`:

```typescript
import { [Name] } from '@/components/ui/[Name]/[Name]';

<section className="preview-section">
  <h2>[Name]</h2>
  <div className="preview-grid">
    <[Name] variant="primary">Primary</[Name]>
    <[Name] variant="secondary">Secondary</[Name]>
    <[Name] variant="success">Success</[Name]>
    <[Name] variant="danger">Danger</[Name]>
    <[Name] variant="warning">Warning</[Name]>
  </div>
  <div className="preview-grid">
    <[Name] size="sm">Small</[Name]>
    <[Name] size="md">Medium</[Name]>
    <[Name] size="lg">Large</[Name]>
  </div>
</section>
```
