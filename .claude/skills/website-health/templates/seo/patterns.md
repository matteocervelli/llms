# SEO — L2 Patterns (Fix Examples + Hugo Tips)

## Hugo: Title Tag

In `layouts/_default/baseof.html` or `layouts/partials/head.html`:

```html
<title>
  {{- if .IsHome -}} {{ .Site.Title }} {{- else -}} {{ .Title }} | {{
  .Site.Title }} {{- end -}}
</title>
```

Keep `{{ .Title }}` under 50 chars so the combined title stays 50-60 chars total.
Set `title` in front matter: `title: "Short, Keyword-Rich Title"`.

## Hugo: Meta Description

```html
<meta
  name="description"
  content="
  {{- with .Description -}}
    {{ . }}
  {{- else -}}
    {{- with .Summary -}}{{ . | truncate 155 }}{{- end -}}
  {{- end -}}
"
/>
```

Set `description` in front matter. Keep it 150-160 chars. Never let it fall back
to `.Summary` in production — auto-summaries are rarely optimized for search.

## Hugo: Canonical URL

```html
<link rel="canonical" href="{{ .Permalink }}" />
```

Always use `.Permalink` (absolute). Never use `.RelPermalink` for canonical tags.

## Hugo: Open Graph Partial

Create `layouts/partials/opengraph.html`:

```html
<meta property="og:title"       content="{{ .Title }}">
<meta property="og:description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Summary | truncate 155 }}{{ end }}">
<meta property="og:url"         content="{{ .Permalink }}">
<meta property="og:image"       content="{{ with .Params.image }}{{ . | absURL }}{{ else }}{{ "img/og-default.png" | absURL }}{{ end }}">
<meta property="og:type"        content="{{ if .IsHome }}website{{ else }}article{{ end }}">
<meta name="twitter:card"       content="summary_large_image">
<meta name="twitter:title"      content="{{ .Title }}">
<meta name="twitter:description" content="{{ with .Description }}{{ . }}{{ else }}{{ .Summary | truncate 155 }}{{ end }}">
<meta name="twitter:image"      content="{{ with .Params.image }}{{ . | absURL }}{{ else }}{{ "img/og-default.png" | absURL }}{{ end }}">
```

Include in `baseof.html`: `{{ partial "opengraph.html" . }}`

## Hugo: Hreflang (Bilingual IT/EN)

```html
{{ if .IsTranslated }} {{ range .AllTranslations }}
<link rel="alternate" hreflang="{{ .Language.Lang }}" href="{{ .Permalink }}" />
{{ end }}
<link rel="alternate" hreflang="x-default" href="{{ .Permalink }}" />
{{ end }}
```

Both language versions must link to each other — if IT page links to EN, the EN
page must also link back to IT. Asymmetric hreflang causes Google to ignore both.

## JSON-LD: Organization + WebSite

Add to the `<head>` of the homepage:

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "{{ .Site.Title }}",
    "url": "{{ .Site.BaseURL }}",
    "logo": "{{ "img/logo.png" | absURL }}",
    "sameAs": ["https://linkedin.com/company/...", "https://twitter.com/..."]
  }
</script>
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "url": "{{ .Site.BaseURL }}",
    "potentialAction": {
      "@type": "SearchAction",
      "target": "{{ .Site.BaseURL }}search?q={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  }
</script>
```

## JSON-LD: Article (Blog Posts)

In `layouts/_default/single.html`:

```html
{{ if eq .Type "posts" }}
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{{ .Title }}",
    "description": "{{ .Description }}",
    "datePublished": "{{ .Date.Format "2006-01-02T15:04:05Z07:00" }}",
    "dateModified": "{{ .Lastmod.Format "2006-01-02T15:04:05Z07:00" }}",
    "author": {
      "@type": "Person",
      "name": "{{ .Params.author | default .Site.Params.author }}"
    },
    "publisher": {
      "@type": "Organization",
      "name": "{{ .Site.Title }}",
      "logo": { "@type": "ImageObject", "url": "{{ "img/logo.png" | absURL }}" }
    },
    "url": "{{ .Permalink }}",
    "image": "{{ with .Params.image }}{{ . | absURL }}{{ end }}"
  }
</script>
{{ end }}
```

## robots.txt Best Practices

`static/robots.txt`:

```
User-agent: *
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml
```

Never `Disallow: /sitemap.xml`. Never use `Disallow: /` on production.
If blocking crawlers for staging, use HTTP auth, not robots.txt — bots can ignore it.

## Hugo: Sitemap Config

`hugo.toml`:

```toml
[sitemap]
  changefreq = "weekly"
  priority   = 0.5
  filename   = "sitemap.xml"
```

Hugo generates `sitemap.xml` automatically. Submit it to Google Search Console and
Bing Webmaster Tools after each major publish. For large sites (>1000 pages), Hugo
generates a sitemap index (`sitemap.xml` pointing to per-section sitemaps).

## Common SEO Mistakes in Hugo Sites

| Mistake                                    | Fix                                                   |
| ------------------------------------------ | ----------------------------------------------------- |
| `.RelPermalink` in canonical               | Use `.Permalink` (absolute URL required)              |
| `.Summary` in meta description             | Always set `description` in front matter              |
| Missing `x-default` hreflang               | Add `x-default` pointing to default language          |
| No `og:image` fallback                     | Set `Site.Params.ogImage` in config + use as fallback |
| JSON-LD only on homepage                   | Add Article schema to all blog/content pages          |
| `title` in config but not layouts          | Verify layout actually renders `{{ .Title }}`         |
| Duplicate H1 from both page title and hero | Use CSS for visual heading; keep one semantic H1      |
