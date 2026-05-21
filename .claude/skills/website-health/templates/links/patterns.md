# Links — L2 Patterns

## Common Causes of Broken Internal Links in Hugo

**Draft pages still linked from content:**
Hugo skips draft pages during build (`draft: true` in front matter), but if another page links to a
draft URL, the link is dead in production. Run `hugo list drafts` to see all draft pages.

**Removed content with no redirect:**
Deleting or renaming a content file removes its URL without redirecting old links. Any internal
reference to the old slug becomes a 404. Check `git log --diff-filter=D -- content/` for recently
deleted files.

**Renamed slugs without alias:**
Changing `slug:` or the filename changes the output URL. Add an alias to preserve the old path:

```yaml
# content/posts/new-name.md
aliases:
  - /posts/old-name/
```

**Taxonomy pages with no content:**
Hugo generates taxonomy list pages (e.g. `/tags/foo/`) automatically. If `foo` appears in only one
post that is later removed, the tag URL 404s. Audit with `hugo list all | grep taxonomy`.

---

## Hugo Alias Configuration for Redirects

Aliases generate `<meta http-equiv="refresh">` HTML redirects by default. For clean 301 redirects,
use a Netlify `_redirects` file instead (see below) and disable alias pages:

```toml
# hugo.toml
[outputs]
  home = ["HTML", "RSS"]
  # Do NOT include "ALIAS" here if using Netlify redirects
```

---

## Netlify `_redirects` File Patterns

Place `static/_redirects` in your Hugo project (Hugo copies `static/` to the output root):

```
# Simple slug rename
/posts/old-name/   /posts/new-name/   301

# Section rename
/blog/*            /posts/:splat       301

# Removed page → nearest parent
/about/old-page/   /about/            301

# Temporary redirect (preserves SEO value on original)
/promo/summer      /shop/summer-sale  302

# Force HTTPS (Netlify does this automatically if configured, but explicit is safer)
http://example.com/*   https://example.com/:splat   301!
```

Verify redirects are deployed: `curl -I https://example.com/old-path/` — expect `301` + `Location` header.

---

## Finding Orphan Pages in Hugo

**Pages not in any menu or list:**
An orphan page has front matter `_build: {list: never}` or is excluded from all menus. It exists
in the sitemap but nothing links to it.

Check with:

```bash
# List all output HTML files, then diff against sitemap
hugo --buildDrafts=false 2>/dev/null && \
  find public/ -name "index.html" | sed 's|public||;s|/index.html||' | sort > /tmp/built.txt
curl -s https://example.com/sitemap.xml | grep '<loc>' | sed 's|.*<loc>||;s|</loc>||' | sort > /tmp/sitemap.txt
comm -13 /tmp/built.txt /tmp/sitemap.txt
```

**Common orphan patterns in Hugo:**

- Standalone landing pages with `sitemap: true` but no nav item
- API/JSON output pages accidentally included in sitemap
- Translated pages with no hreflang pointing to them

---

## Sitemap.xml Configuration in Hugo

```toml
# hugo.toml — exclude specific pages
[sitemap]
  changefreq = "weekly"
  priority   = 0.5
  filename   = "sitemap.xml"
```

Per-page exclusion in front matter:

```yaml
sitemap:
  disable: true
```

Override priority per page:

```yaml
sitemap:
  priority: 0.9
  changefreq: daily
```

Exclude entire sections via output format override in `config/_default/`:

```toml
# Do not include /private/ in sitemap
[outputs]
  section = ["HTML"]  # omit "RSS" and sitemap will ignore
```

---

## Reading Crawler Output and Prioritizing Fixes

**Priority order (highest SEO/UX impact first):**

1. **Broken internal links (FAIL)** — Fix immediately. Each 4xx wastes crawl budget and breaks UX.
   - Find the source page from the report, update or remove the link.
   - If the target page moved, add a Netlify redirect.

2. **Redirect chains (WARN/FAIL)** — Collapse multi-hop chains to a single 301.
   - `A -> B -> C` should become `A -> C` directly. Update the `_redirects` entry.
   - Chains lose PageRank at each hop and slow page loads.

3. **Orphan pages (WARN)** — Either link to them from relevant content, or mark `sitemap: false`.
   - If they have organic traffic (check Analytics), add a contextual internal link.
   - If they're stale, delete the file and add a redirect to the nearest parent section.

4. **Broken external links (WARN)** — Lower urgency, but affects credibility.
   - Use the Wayback Machine (`https://web.archive.org/`) to find archived versions.
   - Replace with the archived URL or remove the link.

5. **Link depth > 3 (WARN)** — Restructure navigation or add contextual cross-links from shallower
   pages to deep ones. Hugo taxonomies and `related` content are good tools here.

6. **Nofollow internal (WARN)** — Review whether the `rel="nofollow"` is intentional.
   - CMS plugins sometimes add nofollow to all links. Audit your shortcodes and themes.

---

## Link Audit Automation

Run periodically with:

```bash
python3 ~/.claude/skills/website-health/lib/link-crawler.py https://example.com \
  --depth 4 --timeout 10 --max-pages 500 --output json \
  | tee /tmp/link-audit-$(date +%F).json
```

Pipe JSON output to `jq` to extract just failures:

```bash
cat /tmp/link-audit.json | jq '.checks.broken_internal[] | "\(.source) -> \(.target) [\(.status)]"'
```
