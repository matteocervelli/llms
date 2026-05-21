# Hugo Static Site Generator Sub-Skill

## Overview
Hugo template patterns for implementing design systems with CSS/SCSS styling, design tokens, and organized component architecture.

## Project Structure

```
content/
├── _index.md           # Homepage
└── posts/              # Blog content

layouts/
├── _default/
│   ├── baseof.html     # Root template
│   ├── list.html       # List pages
│   └── single.html     # Post/page template
├── partials/
│   ├── header.html
│   ├── footer.html
│   ├── components/
│   │   ├── card.html
│   │   ├── button.html
│   │   └── hero.html
│   └── shortcodes/
│       └── component-example.html
└── assets/             # SCSS source files

config.toml            # Site configuration
static/                # CSS output directory
```

## Hugo Configuration

```toml
# config.toml
baseURL = "https://example.com"
languageCode = "en-us"
title = "Design System"

outputs:
  home:
    - HTML
    - JSON

params:
  description = "Design system documentation"
  primaryColor = "#1e40af"
  secondaryColor = "#06b6d4"

[module]
  [[module.imports]]
    path = "github.com/hugo-modules/bootstrap"
```

## SCSS in Hugo Asset Pipeline

```scss
// assets/scss/main.scss
@import 'variables';
@import 'base/reset';
@import 'base/typography';
@import 'mixins/responsive';
@import 'mixins/typography';
@import 'components/button';
@import 'components/card';

// Import Hugo-generated tokens
{{ with resources.Get "tokens/design-tokens.scss" }}
  @import "{{ .RelPermalink }}";
{{ end }}
```

## Base Template Structure

```html
<!-- layouts/_default/baseof.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ .Title }} - {{ .Site.Title }}</title>

  {{ $style := resources.Get "scss/main.scss" | resources.ToCSS }}
  <link rel="stylesheet" href="{{ $style.RelPermalink }}">
</head>
<body>
  {{ partial "header.html" . }}
  <main>
    {{ block "main" . }}{{ end }}
  </main>
  {{ partial "footer.html" . }}
</body>
</html>
```

## Partial Component Templates

```html
<!-- layouts/partials/components/button.html -->
{{ $variant := .variant | default "primary" }}
{{ $size := .size | default "md" }}
{{ $text := .text }}

<button
  class="button button--{{ $variant }} button--{{ $size }}"
  {{ with .href }}href="{{ . }}"{{ end }}
>
  {{ $text }}
</button>

<!-- Usage in content -->
{{ partial "components/button.html" (dict "variant" "primary" "size" "lg" "text" "Learn More") }}
```

## Hero Section with Design Dimensions

```html
<!-- layouts/partials/hero.html -->
<section class="hero" data-theme="{{ .Site.Params.theme | default "light" }}">
  <div class="hero__container">
    <!-- Typography Dimension -->
    <h1 class="hero__title">{{ .title }}</h1>
    <p class="hero__subtitle">{{ .subtitle }}</p>

    <!-- Motion Dimension: Stagger on load -->
    <div class="hero__actions">
      {{ range .buttons }}
        {{ partial "components/button.html" . }}
      {{ end }}
    </div>

    <!-- Spatial Dimension: Responsive grid -->
    <div class="hero__grid">
      {{ range .features }}
        <div class="hero__feature">
          <h3>{{ .title }}</h3>
          <p>{{ .description }}</p>
        </div>
      {{ end }}
    </div>
  </div>

  <!-- Backgrounds Dimension: Gradient overlay -->
  <style>
    .hero {
      background: linear-gradient(135deg,
        var(--color-primary-500),
        var(--color-secondary-500));
    }
  </style>
</section>
```

## Typography Implementation

```html
<!-- layouts/partials/typography-scale.html -->
<h1 class="heading-h1">{{ .title }}</h1>
<h2 class="heading-h2">{{ .subtitle }}</h2>
<p class="text-base">{{ .content }}</p>

<!-- CSS via SCSS mixin in assets/scss/typography.scss -->
```

## Color Theming with Hugo Params

```toml
# config.toml
[params.colors]
  primary-50 = "#f0f9ff"
  primary-500 = "#1e40af"
  primary-900 = "#0c1e3c"
  text = "#1f2937"
  bg = "#ffffff"

[params.colors.dark]
  text = "#f3f4f6"
  bg = "#111827"
```

```html
<!-- Hugo template generates CSS variables -->
<style>
:root {
  {{ range $key, $value := .Site.Params.colors }}
    --color-{{ $key }}: {{ $value }};
  {{ end }}
}
</style>
```

## Spatial Composition in Layouts

```html
<!-- layouts/partials/grid-layout.html -->
<section class="section">
  <div class="container">
    <!-- CSS Grid via SCSS -->
    <div class="grid-3-col">
      {{ range .items }}
        <div class="grid-item">
          {{ partial "components/card.html" . }}
        </div>
      {{ end }}
    </div>
  </div>
</section>

<!-- assets/scss/layouts/_section.scss -->
.section {
  padding: var(--space-xl) var(--space-lg);
}

.grid-3-col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
}
```

## Implementing All 5 Dimensions

**Typography**: Via `heading-h*` and `text-*` classes in SCSS
**Color**: Theme params converted to CSS variables
**Motion**: CSS transitions/animations in component SCSS
**Spatial**: Grid layouts with spacing scale tokens
**Backgrounds**: Gradient overlays, pattern images via CSS

## Related Documentation
- [Typography Dimension](../../../design-references/typography.md)
- [Color & Theme Dimension](../../../design-references/color-palettes.md)
- [Motion Patterns Dimension](../../../design-references/motion-patterns.md)
- [Spatial Composition Dimension](../../../design-references/spatial-compositions.md)
