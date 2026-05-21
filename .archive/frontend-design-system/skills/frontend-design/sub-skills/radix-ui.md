# Radix UI: Headless Primitives with Custom Styling

Radix UI provides unstyled, accessible component primitives. Pair with Tailwind or CSS to build completely custom designs unbound by framework assumptions.

## Headless Component Architecture

Radix decouples logic from presentation:

```tsx
// Radix provides the accessibility layer, you provide the UI
import * as Dialog from "@radix-ui/react-dialog"

export const Modal = () => (
  <Dialog.Root>
    <Dialog.Trigger asChild>
      <button className="px-4 py-2 bg-primary text-white rounded">
        Open Modal
      </button>
    </Dialog.Trigger>
    <Dialog.Content className="fixed inset-0 bg-black/40 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-md">
        <Dialog.Title className="text-2xl font-serif font-bold">
          Dialog Title
        </Dialog.Title>
        <Dialog.Description className="text-neutral mt-2">
          Custom styled content here.
        </Dialog.Description>
        <Dialog.Close asChild>
          <button className="btn-primary mt-6">Close</button>
        </Dialog.Close>
      </div>
    </Dialog.Content>
  </Dialog.Root>
)
```

## Styling with CSS/SCSS

Radix exposes data attributes for state-based styling:

```scss
// dropdown.scss
.dropdown-trigger[data-state="open"] {
  background-color: var(--primary);
  color: white;
}

.dropdown-content[data-state="open"] {
  animation: slideDown 200ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

## Radix + Tailwind Integration

Combine Radix primitives with Tailwind utilities:

```tsx
import * as Popover from "@radix-ui/react-popover"

export const PopoverComponent = () => (
  <Popover.Root>
    <Popover.Trigger className="px-3 py-2 rounded border border-primary text-primary hover:bg-primary/5">
      Trigger
    </Popover.Trigger>
    <Popover.Content
      className="bg-white rounded-lg shadow-lg p-4 border border-gray-200 z-50"
      sideOffset={8}
    >
      <p className="text-sm text-neutral font-sans">Popover content</p>
    </Popover.Content>
  </Popover.Root>
)
```

## Applying Design Dimensions

**Typography**: Define font hierarchy in Tailwind classes
```tsx
<Dialog.Title className="font-serif text-2xl font-bold leading-tight">
  Headline
</Dialog.Title>
```

**Color**: Use CSS variables aligned with color dimension
```css
.dropdown-trigger[data-state="open"] {
  background: var(--primary);
  color: var(--primary-foreground);
}
```

**Spacing**: Custom gaps and padding per dimension spec
```tsx
<div className="space-y-6 p-8">  <!-- 24px gap, 32px padding -->
```

**Motion**: Smooth animations via CSS keyframes
```scss
animation: slideDown 200ms cubic-bezier(0.16, 1, 0.3, 1);
```

**Composition**: Flexible grid layouts without component assumptions
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
```

## Accessible Animations

Respect user motion preferences:

```scss
@media (prefers-reduced-motion: reduce) {
  .dropdown-content[data-state="open"] {
    animation: none;
  }
}
```

## Theming Strategy

1. **Define color tokens** in CSS variables
2. **Use data attributes** (`data-state`, `data-side`) for state styling
3. **Compose with Tailwind** for rapid styling
4. **Create wrapper components** for consistency
5. **Document component API** (props, slots, events)

## Common Radix Primitives

- **Dialog**: Modal, popover, dropdown
- **Menu**: Accessible menu components
- **Popover**: Floating UI containers
- **Tabs**: Tabbed interfaces
- **Scroll Area**: Custom scrollbars
- **Slider**: Range inputs with custom styling

## Dimension Connections

- [Typography System](../dimension-sub-skills/typography.md)
- [Color & Theme](../dimension-sub-skills/color-theme.md)
- [Motion & Animation](../dimension-sub-skills/motion.md)
- [Spatial Compositions](../dimension-sub-skills/spatial-compositions.md)

## Key Takeaways

- Radix is **unstyled by design**—complete creative freedom
- Data attributes enable state-based styling without JavaScript
- WCAG compliance is built-in; focus on visual hierarchy
- Pair with Tailwind for rapid development or CSS for control
- Perfect for highly branded, custom interfaces

**Strategy**: Use Radix for logic/accessibility, Tailwind for styling speed.
