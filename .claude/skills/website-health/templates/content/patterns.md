# Content — L2 Patterns

## Hugo Content Organization

- Use `content/posts/`, `content/pages/`, `content/projects/` — one section per content type
- Keep each `.md` file focused: one topic, one clear title (maps to H1)
- Use `draft: true` for work-in-progress; avoid publishing thin placeholder pages
- Taxonomy pages (`/tags/`, `/categories/`) are index pages — exclude from thin-content checks

## Last-Modified / Stale Content

Enable `enableGitInfo = true` in `hugo.toml` to auto-populate `.Lastmod` from git commit dates:

```toml
enableGitInfo = true
```

Then in templates use `{{ .Lastmod.Format "2006-01-02" }}` and expose it via HTTP headers using
your hosting platform's `_headers` file (Netlify/Cloudflare Pages) or nginx `add_header`.

Manual override in front matter: `lastmod: 2024-06-01` takes precedence over git date.

## Avoiding Duplicate Content

- Set canonical URLs: `canonifyURLs = false` + `<link rel="canonical">` in `<head>`
- Add `noindex` to auto-generated index/taxonomy pages via robots meta tag in the layout
- Avoid copy-pasting content across multiple pages; use Hugo `{{ partial }}` for reusable blocks
- Translated pages (bilingual site) are separate content — not duplicates

## Image Alt Text in Hugo Markdown

Standard Markdown image syntax:

```markdown
![Descriptive alt text explaining what the image shows](image.jpg)
```

For decorative images use HTML directly with `role="presentation"` or `aria-hidden="true"`:

```html
<img src="divider.svg" alt="" role="presentation" />
```

Hugo shortcode pattern for images with enforced alt:

```go
{{/* layouts/shortcodes/img.html */}}
<img src="{{ .Get "src" }}" alt="{{ .Get "alt" | default (errorf "alt required for img shortcode") }}">
```

## Heading Hierarchy in Hugo

In templates: use `<h1>` only for the page title (`.Title`), never repeat it in partials.
In content `.md` files: start headings at `##` (H2) — Hugo renders the front matter `title` as H1.

Example layout pattern:

```html
<h1>{{ .Title }}</h1>
{{/* page template — single H1 */}} {{ .Content }} {{/* content uses ## H2, ###
H3 ... */}}
```

## Readability Score Interpretation

| Flesch Score | Grade     | Suitable for              |
| ------------ | --------- | ------------------------- |
| 90–100       | Very easy | 5th grade, conversational |
| 70–90        | Easy      | 6th grade, general public |
| 50–70        | Standard  | 7th–8th grade, mainstream |
| 30–50        | Difficult | High school / college     |
| 0–30         | Very hard | Academic / professional   |

Target 50–70 for blog posts. Technical documentation at 30–50 is acceptable.
Use shorter sentences and common words to improve score.

## Language Consistency for Bilingual Hugo Sites

- Set `defaultContentLanguage` and per-language directories: `content/en/`, `content/it/`
- Each page must have `<html lang="en">` or `<html lang="it">` — set via `{{ .Language.Lang }}`
- Navigation labels and UI strings go in `i18n/en.yaml` / `i18n/it.yaml` — never hardcode them
- Don't mix languages in a single page body; link to the translated version via `hreflang` alternate

```html
<link rel="alternate" hreflang="it" href="{{ .Translations.it.Permalink }}" />
<link rel="alternate" hreflang="en" href="{{ .Translations.en.Permalink }}" />
```

## Content Audit Process (Quarterly)

1. Run `content-analyzer.py <url> --max-pages 200 --output json > audit.json`
2. Triage FAIL items first: duplicate pages → redirect or consolidate; thin pages → expand or noindex
3. Fix missing alt text in source `.md` files or Hugo shortcodes
4. Review stale pages: update content or add `expiryDate` to auto-archive
5. Check readability score trend (not a gate, but track over time)
6. Commit fixes, re-run to confirm PASS
