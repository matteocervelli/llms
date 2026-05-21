# Links — L1 Summary

## What Gets Checked

1. **Internal broken links** — All `<a href>` within your domain returning 4xx
2. **External broken links** — Outbound links returning 4xx/5xx
3. **Redirect chains** — More than 2 hops (3xx -> 3xx -> target)
4. **Orphan pages** — In sitemap but not linked from any page
5. **Link depth** — Pages requiring >3 clicks from homepage
6. **Nofollow audit** — Internal links accidentally marked nofollow

## Thresholds

| Check             | PASS | WARN | FAIL |
| ----------------- | ---- | ---- | ---- |
| Broken internal   | 0    | 1-5  | >5   |
| Broken external   | 0    | 1-10 | >10  |
| Redirect chains   | 0    | 1-3  | >3   |
| Orphan pages      | 0    | 1-3  | >3   |
| Max link depth    | <=3  | 4-5  | >5   |
| Nofollow internal | 0    | 1-2  | >2   |

---

Ask for **patterns** for crawler config, Hugo broken link sources, and redirect strategies.
