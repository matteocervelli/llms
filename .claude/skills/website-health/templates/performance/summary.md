# Performance — L1 Summary

## Core Web Vitals

| Metric | Good    | Needs Improvement | Poor    |
| ------ | ------- | ----------------- | ------- |
| LCP    | < 2.5s  | 2.5-4.0s          | > 4.0s  |
| CLS    | < 0.1   | 0.1-0.25          | > 0.25  |
| INP    | < 200ms | 200-500ms         | > 500ms |

## Lighthouse Scores (PASS >= 90, WARN >= 50, FAIL < 50)

Performance | SEO | Best Practices | Accessibility

## Quick Wins

1. **Compression** — brotli (best) or gzip
2. **Cache headers** — Cache-Control with max-age + ETag
3. **Image optimization** — WebP/AVIF, width/height attributes, lazy-load
4. **Font loading** — font-display: swap, preload critical fonts
5. **HTTPS** — 301 redirect from HTTP

---

Ask for **patterns** for Lighthouse CLI commands and Netlify optimization configs.
