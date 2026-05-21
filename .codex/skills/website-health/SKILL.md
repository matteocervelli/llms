---
name: website-health
description: Audit a live website across 7 dimensions — SEO, performance, links, privacy, accessibility, security, content — with PASS/WARN/FAIL gates. Use when checking a deployed site's health or quality. Trigger on "audit my website", "site health", "check SEO", "is my site accessible", "website-health <url>".
allowed-tools: Read, Bash, Grep, Glob, Write
---

# /website-health — Website Health Audit

Orchestrates a cross-cutting website audit across 7 dimensions. Designed for periodic invocation against live sites.

**Architecture — hybrid orchestrator:**

- **Native checks** (new lib scripts): `seo`, `performance`, `links`, `privacy`, `content`
- **Pure delegation** (existing sub-skill owns the logic): `a11y` → `/frontend a11y`, `security` → `/security-verify dast`

## Quick Start

```
/website-health <url>                      # quick summary, all 7 dimensions (L1)
/website-health full <url>                 # deep audit, all dimensions (L2+)
/website-health seo <url>                  # single dimension
/website-health performance <url>          # single dimension
/website-health links <url>                # single dimension
/website-health privacy <url>              # single dimension
/website-health a11y <url>                 # delegates to /frontend a11y + pa11y
/website-health security <url>             # delegates to /security-verify dast + extras
/website-health content <url>              # single dimension
/website-health report <url>               # full audit + persistent markdown report
/website-health patterns <dimension>       # show fix recipes (seo, performance, links, privacy, a11y, security, content)
```

---

## Workflow

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for subcommand, URL, and optional flags (`--stack <name>`).

**Stack auto-detection** (when no URL is provided, check in order):

| Stack           | Marker                                                                          | baseURL extraction                               |
| --------------- | ------------------------------------------------------------------------------- | ------------------------------------------------ |
| Astro Starlight | `astro.config.mjs` / `astro.config.ts` + `@astrojs/starlight` in `package.json` | `site:` field in astro config, or `SITE` env var |
| Astro           | `astro.config.mjs` / `astro.config.ts`                                          | `site:` field in astro config, or `SITE` env var |
| Hugo            | `hugo.toml` or `config.toml` with `baseURL`                                     | `baseURL` value                                  |
| Netlify         | `netlify.toml`                                                                  | from underlying framework config                 |
| Next.js         | `next.config.js` or `next.config.ts`                                            | `NEXT_PUBLIC_SITE_URL` env or localhost          |
| Gatsby          | `gatsby-config.js` with `siteMetadata.siteUrl`                                  | `siteUrl` value                                  |
| Generic         | `package.json` with `homepage`                                                  | `homepage` value                                 |

```bash
# Astro config extraction
if [ -f astro.config.mjs ] || [ -f astro.config.ts ]; then
  ASTRO_SITE=$(grep -E "^\s*site:" astro.config.mjs astro.config.ts 2>/dev/null | head -1 | sed "s/.*site:\s*['\"]//;s/['\"].*//" || echo "")
  STARLIGHT=$(grep -l "@astrojs/starlight" package.json 2>/dev/null)
  STACK="astro"
  [ -n "$STARLIGHT" ] && STACK="astro-starlight"
fi
```

**Stack-specific behavior:**

- `astro-starlight`: activates Starlight-specific content checks (see Dimension: Content — Starlight Mode)
- `astro`: standard checks + Astro build output validation
- All other stacks: standard 7-dimension audit

- If no URL and no marker: report error "No URL provided and no website project detected. Run: `/website-health <url>`"
- If no subcommand: read and show `templates/overview.md`
- If `full`: run all 7 dimensions at deep depth
- If `report`: run all 7 dimensions + write report to `docs/website-health/report-YYYY-MM-DD.md`

### Step 2: Check Tool Availability

```bash
bash "$HOME/.claude/skills/website-health/lib/tool-check.sh"
```

Note which tools are available. Each dimension adapts its checks based on available tools.
Always report tool availability at the start of output.

### Step 3: Connectivity Pre-check

```bash
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "$URL" 2>/dev/null || true)
```

If `000`: report unreachable and exit. Otherwise proceed.

### Step 4: Route to Dimension(s)

Run the requested dimension(s). For summary/full modes, run all 7 sequentially.

**Dimension execution order** (for `full` and summary):

1. SEO
2. Performance
3. Links
4. Privacy
5. Accessibility
6. Security
7. Content

### Step 5: Produce Report

Use the uniform output format (see below). For `report` mode, additionally write to disk using `templates/report-template.md` as scaffold.

---

## Dimension: SEO

Technical on-page SEO audit. Replaces Ahrefs Site Audit for meta analysis.

**Run:**

```bash
bash "$HOME/.claude/skills/website-health/lib/seo-checker.sh" "$URL" [--depth N] [--sample N]
```

**Checks:**

| Check                     | PASS                         | WARN                 | FAIL                       |
| ------------------------- | ---------------------------- | -------------------- | -------------------------- |
| Title tag                 | 50-60 chars, unique per page | <50 or >60 chars     | Missing                    |
| Meta description          | 150-160 chars, unique        | Length off           | Missing                    |
| H1 tag                    | Exactly 1 per page           | >1 H1                | Missing                    |
| OG + Twitter Cards        | All 4 OG + twitter:card      | Partial (>2)         | <2 present                 |
| robots.txt                | Not blocking critical paths  | Blocks non-sensitive | Missing or blocks sitemap  |
| sitemap.xml               | Valid XML, URLs 200          | Some 3xx/4xx         | Missing or invalid         |
| Canonical URLs            | Self-referencing, present    | Present but wrong    | Missing >50%               |
| Hreflang (bilingual)      | IT/EN cross-refs valid       | Asymmetric           | Missing on bilingual pages |
| Structured data (JSON-LD) | Present on key pages         | Incomplete           | Missing entirely           |
| RSS/Atom feed             | Valid, recent entries        | Stale >90 days       | Missing                    |

**Templates:**

- L1: Read `templates/seo/summary.md`
- L2: Read `templates/seo/patterns.md` (fix examples, Hugo-specific tips)

---

## Dimension: Performance

Core Web Vitals and server-side performance.

**Run:**

```bash
bash "$HOME/.claude/skills/website-health/lib/performance-checker.sh" "$URL"
```

Primary tool: `lighthouse` CLI. Fallback: curl-only header checks.

**Checks:**

| Check                     | PASS                       | WARN               | FAIL            |
| ------------------------- | -------------------------- | ------------------ | --------------- |
| Lighthouse Performance    | >=90                       | >=50               | <50             |
| Lighthouse Best Practices | >=90                       | >=50               | <50             |
| LCP                       | <2.5s                      | <4s                | >=4s            |
| CLS                       | <0.1                       | <0.25              | >=0.25          |
| INP                       | <200ms                     | <500ms             | >=500ms         |
| Page weight               | <1MB                       | <3MB               | >=3MB           |
| Compression               | brotli or gzip             | gzip only          | None            |
| Cache headers             | Cache-Control + ETag       | Cache-Control only | None            |
| Image optimization        | WebP/AVIF, lazy-load       | Partial            | None            |
| Font loading              | font-display:swap, preload | Present            | Render-blocking |

**Templates:**

- L1: Read `templates/performance/summary.md`
- L2: Read `templates/performance/patterns.md`

---

## Dimension: Links

Link health audit — broken links, redirect chains, orphan pages.

**Run:**

```bash
python3 "$HOME/.claude/skills/website-health/lib/link-crawler.py" "$URL" --depth 3 --timeout 5 --output json
```

**Checks:**

| Check                      | PASS | WARN | FAIL |
| -------------------------- | ---- | ---- | ---- |
| Broken internal (4xx)      | 0    | 1-5  | >5   |
| Broken external (4xx/5xx)  | 0    | 1-10 | >10  |
| Redirect chains (>2 hops)  | 0    | 1-3  | >3   |
| Orphan pages               | 0    | 1-3  | >3   |
| Max link depth             | <=3  | 4-5  | >5   |
| Nofollow on internal links | 0    | 1-2  | >2   |

**Templates:**

- L1: Read `templates/links/summary.md`
- L2: Read `templates/links/patterns.md`

---

## Dimension: Privacy

GDPR and privacy compliance audit.

**Run:**

```bash
bash "$HOME/.claude/skills/website-health/lib/privacy-checker.sh" "$URL"
```

Optional: `playwright-cli` for cookie consent interaction testing.

**Checks:**

| Check                 | PASS                       | WARN                | FAIL                    |
| --------------------- | -------------------------- | ------------------- | ----------------------- |
| Cookie consent banner | Present, opt-in, 3 actions | Present but opt-out | Missing                 |
| Pre-consent cookies   | 0 non-essential            | 1-2 tracking        | >2 or analytics         |
| Privacy policy link   | Footer + cookie banner     | Footer only         | Missing                 |
| Cookie policy         | Exists, lists categories   | Incomplete          | Missing                 |
| HTTPS redirect        | HTTP->HTTPS 301            | 302                 | No redirect             |
| Set-Cookie flags      | Secure+HttpOnly+SameSite   | Missing SameSite    | Missing Secure/HttpOnly |
| Third-party trackers  | All declared               | Some undeclared     | Undeclared trackers     |

**Templates:**

- L1: Read `templates/privacy/summary.md`
- L2: Read `templates/privacy/patterns.md`

---

## Dimension: Accessibility (DELEGATES)

Delegates to existing skills. Do NOT reimplement accessibility checks.

**Delegation chain:**

1. Invoke `/frontend a11y` with the URL — full WCAG 2.1 AA audit
2. If `pa11y` is installed: `pa11y "$URL" --standard WCAG2AA --reporter json`
3. Cross-reference Lighthouse accessibility score if performance was already run

**Templates:**

- L1: Read `templates/a11y/summary.md` (documents delegation)
- L2: Read `templates/a11y/patterns.md`

---

## Dimension: Security (DELEGATES)

Delegates to existing skills plus additional checks.

**Delegation:**

1. Invoke `/security-verify dast "$URL"` — OWASP HTTP headers, CORS, TLS, info disclosure
2. Parse dast output and merge into report

**Additional checks (not in dast-runner.sh):**

| Check              | Tool            | PASS                           | WARN             | FAIL                |
| ------------------ | --------------- | ------------------------------ | ---------------- | ------------------- |
| Cert expiry        | openssl/curl -v | >30 days                       | 7-30 days        | <7 days             |
| SRI on CDN scripts | python3         | All CDN scripts have integrity | >50% have SRI    | <50%                |
| Mixed content      | python3         | 0 HTTP on HTTPS                | 1-2 non-critical | >2 or script/iframe |

**Templates:**

- L1: Read `templates/security/summary.md`
- L2: Read `templates/security/patterns.md`

---

## Dimension: Content

Content quality analysis.

**Run:**

```bash
python3 "$HOME/.claude/skills/website-health/lib/content-analyzer.py" "$URL" --output json
```

**Checks:**

| Check                       | PASS              | WARN           | FAIL                  |
| --------------------------- | ----------------- | -------------- | --------------------- |
| Duplicate content (SHA-256) | 0                 | 1-3 near-dupes | >3                    |
| Thin content (<300 words)   | 0                 | 1-5 thin       | >5                    |
| Missing alt text            | 0                 | 1-5 missing    | >5                    |
| Heading hierarchy           | Proper H1→H2→H3   | Minor skips    | H1 missing/major gaps |
| Language consistency        | <5% foreign words | 5-15%          | >15%                  |
| Stale content (>1yr)        | 0                 | 1-5 pages      | >5                    |
| Readability (Flesch)        | Informational     | Informational  | N/A                   |

**Templates:**

- L1: Read `templates/content/summary.md`
- L2: Read `templates/content/patterns.md`

---

## Dimension: Content — Starlight Mode

Active only when `--stack astro-starlight` is passed (auto-set by stack detection).
Runs IN ADDITION to the standard Content checks.

**Starlight-specific checks:**

| Check                           | PASS                                                 | WARN                           | FAIL                               |
| ------------------------------- | ---------------------------------------------------- | ------------------------------ | ---------------------------------- |
| Sidebar config coverage         | All `src/content/docs/**/*.md` referenced in sidebar | <20% uncovered                 | >20% orphan pages (not in sidebar) |
| Search index                    | Pagefind / built-in search enabled                   | Search present but stale       | No search configured               |
| i18n translation parity (IT↔EN) | IT and EN page counts match ±5%                      | 6-20% gap                      | >20% gap or default lang missing   |
| Frontmatter completeness        | `title`, `description` present on all pages          | <5% missing description        | >5% missing title or description   |
| `prev`/`next` navigation        | Defined or auto-inferred for all doc pages           | Missing on >10% of pages       | Broken prev/next links             |
| Versioned docs (if present)     | All versions have redirect from `/docs/` root        | Missing redirect for 1 version | >1 version unreachable             |
| Draft pages in production       | 0 pages with `draft: true` served                    | —                              | Any `draft: true` page served live |

**Detection of Starlight structure:**

```bash
# Verify expected Starlight directories exist
ls src/content/docs/ 2>/dev/null
grep -r "sidebar" astro.config.mjs astro.config.ts 2>/dev/null | head -5
# Check for i18n
grep -E "locales|defaultLocale" astro.config.mjs astro.config.ts 2>/dev/null
```

---

## Output Format

All dimensions use this uniform structure:

```
## Website Health — <domain> — <date>

### <Dimension> [PASS|WARN|FAIL]
- ✓ <passing finding>
- ⚠ <warning finding>
- ✗ <failing finding>
- [SKIP] <skipped check> — <tool> not installed

### ...

Overall: [PASS|WARN|FAIL]
```

**Gate logic:** FAIL if any dimension FAIL. WARN if any WARN. PASS only if all pass.
Skipped checks do not affect the gate.

---

## Post-Audit: Recommendations

After presenting dimension results, ALWAYS generate a Recommendations section by triaging findings.

### Triage Rules

**Quick Wins** (suggest fixing immediately — <5 min each):

- Missing meta tags (title, description, OG) → one-line template edit
- Missing HTTP headers (Cache-Control, ETag, SameSite) → config file edit
- Missing `alt` text on small number of images → content edit
- HTTPS redirect issues → server/CDN config
- Single broken internal links → content fix
- Missing canonical URLs → template one-liner

**Tech Debt** (suggest GitHub issue via `/health issues`):

- Structural SEO gaps (missing JSON-LD, incomplete hreflang across all pages)
- Multiple broken external links (needs manual review of replacements)
- Content quality issues (thin content, stale pages — needs writing)
- Missing cookie consent categories (needs legal review)
- Performance optimization requiring code changes (image format migration, font subsetting)
- Accessibility issues requiring template refactoring

**Install to Unlock** (informational):

- Any [SKIP] findings from missing tools → show install command

### Output Format

After the dimension results and Overall gate, generate:

```
## Recommendations

### Quick Wins (fix now)
- [Dimension] <what to fix> — <where/how, 1 line>

### Tech Debt (create issues)
- [Dimension] <what to fix> — <why it's bigger>

### Install to Unlock
- `<install command>` — <what it enables>
```

If no quick wins: "No quick wins — all findings require deeper investigation."
If no tech debt: "No tech debt items — all findings are quick wins or informational."

### Next Steps

After Recommendations, show actionable next steps:

```
## Next Steps

- **Quick Wins**: Fix the items listed above — small config/template edits
- **Fix Recipes**: `/website-health patterns <dimension>` for code examples
- **Create Issues**: `/health issues` to open GitHub BACKLOG issues for tech debt
- **Full Project Audit**: `/health full` to add code health dimensions
```

The "Full Project Audit" line only shows when running standalone `/website-health`.
When invoked from within `/health full`, omit it (already running everything).

---

## Subcommand: patterns

Show L2 fix recipes for a specific dimension.

```
/website-health patterns seo
/website-health patterns performance
/website-health patterns links
/website-health patterns privacy
/website-health patterns a11y
/website-health patterns security
/website-health patterns content
```

**Steps:**

1. Read `templates/<dimension>/patterns.md`
2. Present content to user

Use after an audit to get detailed fix examples for a specific dimension.

---

## Graceful Degradation

The `lib/tool-check.sh` script runs at the start. Each dimension adapts:

| Tool Missing     | Fallback                                            |
| ---------------- | --------------------------------------------------- |
| `lighthouse`     | curl-only: compression, cache, page weight (no CWV) |
| `pa11y`          | `/frontend a11y` alone                              |
| `xmllint`        | Python lxml or skip sitemap validation              |
| `playwright-cli` | curl-only cookie/banner analysis                    |
| `beautifulsoup4` | Python html.parser (stdlib)                         |
| `openssl`        | curl -v for cert info                               |

**Minimum viable**: `curl` + `python3` only. All 7 dimensions produce output.

---

## What We Cannot Check (Ahrefs Proprietary)

These require Ahrefs' proprietary crawl index — no free tool replicates them:

- Historical backlink index (third-party links pointing TO you)
- Organic traffic estimates per page
- Domain Rating / URL Rating
- Keyword rankings and search volume

Use Ahrefs CSV exports for baseline comparison when available.

---

## Integration

**Two entry points, same outcome (quick wins + tech debt issues):**

- **`/health full`** (recommended for website projects) — runs all project dimensions including website, then offers `/health issues` for everything. Context from `/website-health` is preserved because it runs in the same conversation.
- **`/website-health` standalone** — runs 7 website dimensions, shows recommendations, points to `/health issues` for issue creation. Context is already in the conversation.

**Key**: `/health issues` doesn't re-run checks. It reads findings already in the conversation and proposes `gh issue create` commands. Works after either entry point.

- Skill is stateless — designed for periodic invocation via `/loop` or future headless cron
