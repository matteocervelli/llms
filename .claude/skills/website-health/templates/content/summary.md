# Content — L1 Summary

## Quality Checks

1. **Duplicate content** — SHA-256 hash comparison across all pages
2. **Thin content** — Pages with <300 words (excluding nav/footer)
3. **Missing alt text** — Images without descriptive alt attributes
4. **Heading hierarchy** — Proper H1 -> H2 -> H3 (no level skips)
5. **Language consistency** — Mixed language detection in single-language pages
6. **Stale content** — Pages not updated in >1 year (via Last-Modified header)
7. **Readability** — Flesch-Kincaid score (informational, not gated)

## Bilingual Awareness

For IT/EN sites: checks run per-language, grouped by URL prefix or `<html lang>`.

---

Ask for **patterns** for content quality strategies and Hugo content management tips.
