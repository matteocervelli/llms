# Performance — L2 Patterns

## Lighthouse CLI

```bash
# Full audit, JSON output
lighthouse https://example.com \
  --output json,html \
  --chrome-flags="--headless --no-sandbox" \
  --output-path /tmp/lh-report

# Score summary only (requires jq)
lighthouse https://example.com --output json --quiet \
  --output-path /tmp/lh.json 2>/dev/null && \
  python3 -c "
import json
d = json.load(open('/tmp/lh.json'))
cats = d['categories']
for k,v in cats.items():
    print(f'{k}: {int(v[\"score\"]*100)}')
"

# CI mode — exit 1 if performance < 90
lighthouse https://example.com \
  --budget-path=lighthouse-budget.json \
  --chrome-flags="--headless --no-sandbox"
```

## Netlify `_headers` — Caching and Compression

```
# Static assets — long-lived cache
/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/images/*
  Cache-Control: public, max-age=31536000, immutable

/css/*
  Cache-Control: public, max-age=31536000, immutable

/js/*
  Cache-Control: public, max-age=31536000, immutable

# HTML pages — always revalidate
/*
  Cache-Control: public, max-age=0, must-revalidate
```

Netlify enables brotli automatically. No extra config needed.

## Netlify `netlify.toml` — Asset Optimization

```toml
[build.processing]
  skip_processing = false

[build.processing.css]
  bundle = true
  minify = true

[build.processing.js]
  bundle = true
  minify = true

[build.processing.html]
  pretty_urls = true

[build.processing.images]
  compress = true
```

## Hugo — WebP Image Processing Pipeline

```html
<!-- layouts/partials/responsive-image.html -->
{{ $img := .img }} {{ $alt := .alt }} {{ $widths := slice 480 768 1024 1280 }}
{{ $webp := $img.Process "webp" }}
<picture>
  {{ range $widths }} {{ $resized := $webp.Resize (printf "%dx webp" .) }}
  <source
    srcset="{{ $resized.RelPermalink }}"
    width="{{ . }}"
    media="(max-width: {{ . }}px)"
    type="image/webp"
  />
  {{ end }} {{ $fallback := $img.Resize "1280x" }}
  <img
    src="{{ $fallback.RelPermalink }}"
    width="{{ $fallback.Width }}"
    height="{{ $fallback.Height }}"
    alt="{{ $alt }}"
    loading="lazy"
    decoding="async"
  />
</picture>
```

Hugo config to enable image processing:

```toml
# hugo.toml
[imaging]
  quality = 80
  resampleFilter = "Lanczos"
```

## Font Preloading in Hugo `baseof.html`

```html
<head>
  <!-- Preconnect to font CDN -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />

  <!-- Preload critical font files (adjust URL and format) -->
  <link
    rel="preload"
    href="/fonts/inter-v13-latin-regular.woff2"
    as="font"
    type="font/woff2"
    crossorigin
  />

  <!-- font-display: swap in your CSS -->
  <style>
    @font-face {
      font-family: "Inter";
      src: url("/fonts/inter-v13-latin-regular.woff2") format("woff2");
      font-display: swap;
    }
  </style>
</head>
```

## Resource Hints

```html
<!-- DNS prefetch for third-party origins -->
<link rel="dns-prefetch" href="https://analytics.example.com" />

<!-- Preconnect when you'll fetch a resource soon -->
<link rel="preconnect" href="https://cdn.example.com" crossorigin />

<!-- Prefetch next-page assets (low priority, background) -->
<link rel="prefetch" href="/next-page/index.html" />

<!-- Preload critical above-fold resources (high priority) -->
<link rel="preload" href="/css/critical.css" as="style" />
<link rel="preload" href="/js/main.js" as="script" />
```

## Common Hugo Performance Pitfalls

| Pitfall                                     | Fix                                                       |
| ------------------------------------------- | --------------------------------------------------------- |
| Images not resized at build time            | Use `$img.Resize` or `$img.Fit` in templates              |
| Missing `width`/`height` on `<img>`         | Always set from `$img.Width`/`$img.Height` — prevents CLS |
| Google Fonts loaded via `<link>` at runtime | Self-host or use `font-display: swap` + preload           |
| `loading="lazy"` on above-fold images       | Only lazy-load below-fold; above-fold needs eager         |
| Huge JS bundles from theme                  | Audit `themes/*/assets/js/`, remove unused scripts        |
| No `Cache-Control` on Netlify               | Add `_headers` file; Netlify default is no-cache for HTML |
