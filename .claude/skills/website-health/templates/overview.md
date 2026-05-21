# Website Health — Overview

Periodic website audit across 7 dimensions. Delegates to existing skills where possible.

| #   | Dimension     | Command                             | What it checks                                         |
| --- | ------------- | ----------------------------------- | ------------------------------------------------------ |
| 1   | SEO           | `/website-health seo <url>`         | Meta tags, sitemap, robots, hreflang, structured data  |
| 2   | Performance   | `/website-health performance <url>` | Core Web Vitals, Lighthouse, caching, compression      |
| 3   | Links         | `/website-health links <url>`       | Broken links, redirect chains, orphan pages            |
| 4   | Privacy       | `/website-health privacy <url>`     | GDPR consent, cookies, trackers, privacy policy        |
| 5   | Accessibility | `/website-health a11y <url>`        | WCAG 2.1 AA (delegates to /frontend a11y)              |
| 6   | Security      | `/website-health security <url>`    | OWASP DAST + TLS + SRI (delegates to /security-verify) |
| 7   | Content       | `/website-health content <url>`     | Duplicates, thin content, headings, readability        |

## Quick Start

```
/website-health https://example.com          # Summary of all 7 dimensions
/website-health full https://example.com     # Deep audit (all pages)
/website-health report https://example.com   # Deep audit + persistent report
/website-health seo https://example.com      # Single dimension
```

## Tool Dependencies

| Tool             | Required?      | Install                | Used by                       |
| ---------------- | -------------- | ---------------------- | ----------------------------- |
| `curl`           | Yes (built-in) | —                      | All dimensions                |
| `python3`        | Yes (built-in) | —                      | SEO, Links, Content           |
| `lighthouse`     | Recommended    | `npm i -g lighthouse`  | Performance (CWV)             |
| `pa11y`          | Optional       | `npm i -g pa11y`       | Accessibility                 |
| `xmllint`        | Optional       | `brew install libxml2` | SEO (sitemap validation)      |
| `playwright-cli` | Optional       | via `/frontend` skill  | Privacy (consent interaction) |

Without optional tools, checks gracefully degrade — never fail.

## What We Cannot Check (Ahrefs Proprietary)

- Historical backlink index (third-party links pointing TO you)
- Organic traffic estimates per page
- Domain Rating / URL Rating
- Keyword rankings and search volume

Use Ahrefs CSV exports for these. This skill covers everything else.
