# Accessibility — L2 Patterns

## Running the Checks

### Via /frontend a11y (primary)

```
/frontend a11y https://example.com
```

Runs full WCAG 2.1 AA audit: axe-core automated scan, keyboard navigation test, screen reader compatibility check.

### Via pa11y (complementary)

```bash
# Single page
pa11y "https://example.com" --standard WCAG2AA --reporter json

# Multiple pages
echo "https://example.com\nhttps://example.com/about" | xargs -I{} pa11y "{}" --standard WCAG2AA
```

## Common Hugo Accessibility Issues

### Missing lang attribute

```html
<!-- BAD -->
<html>
  <!-- GOOD — set in hugo.toml -->
  <html lang="{{ .Site.Language.Lang }}"></html>
</html>
```

### Images without alt text

```html
<!-- BAD -->
{{ $img := resources.Get "hero.jpg" }}
<img src="{{ $img.RelPermalink }}" />

<!-- GOOD -->
<img
  src="{{ $img.RelPermalink }}"
  alt="{{ .Params.hero_alt | default .Title }}"
/>
```

### Skip navigation link

```html
<!-- Add to baseof.html before <nav> -->
<a href="#main-content" class="skip-link">Skip to main content</a>
<!-- ... -->
<main id="main-content"></main>
```

### Form labels

```html
<!-- BAD -->
<input type="email" placeholder="Email" />

<!-- GOOD -->
<label for="email">Email address</label>
<input type="email" id="email" name="email" placeholder="you@example.com" />
```

### Color contrast

```scss
// Minimum contrast ratios (WCAG 2.1 AA)
// Normal text (<18pt): 4.5:1
// Large text (>=18pt or >=14pt bold): 3:1
// UI components and graphics: 3:1

// Check with: https://webaim.org/resources/contrastchecker/
```

### Focus indicators

```scss
// Never remove focus outlines without replacement
a:focus,
button:focus,
input:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

// BAD — never do this
// *:focus { outline: none; }
```

### ARIA landmarks

```html
<header role="banner">
  <nav role="navigation" aria-label="Main">
    <main role="main">
      <footer role="contentinfo">
        <aside role="complementary"></aside>
      </footer>
    </main>
  </nav>
</header>
```

## Axe-Core Rule Categories

| Category | Examples                                                |
| -------- | ------------------------------------------------------- |
| Critical | missing alt, no keyboard access, empty buttons          |
| Serious  | low contrast, missing form labels, no heading structure |
| Moderate | redundant ARIA, missing lang on page sections           |
| Minor    | tabindex > 0, empty table headers                       |
