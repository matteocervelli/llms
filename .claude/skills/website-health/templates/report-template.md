# Website Health Report Template

This template is used by `lib/report-generator.sh` to produce persistent audit reports.

## Report Structure

```
# Website Health Report
**Domain**: <domain>
**Date**: <YYYY-MM-DD>

## Summary
| Dimension     | Status |
|---------------|--------|
| SEO           | PASS/WARN/FAIL |
| Performance   | PASS/WARN/FAIL |
| Links         | PASS/WARN/FAIL |
| Privacy       | PASS/WARN/FAIL |
| Accessibility | PASS/WARN/FAIL |
| Security      | PASS/WARN/FAIL |
| Content       | PASS/WARN/FAIL |

**Overall: PASS/WARN/FAIL**

---

## SEO Audit Results
(output from seo-checker.sh)

## Performance Audit Results
(output from performance-checker.sh)

## Link Health Audit
(output from link-crawler.py)

## Privacy & GDPR Audit
(output from privacy-checker.sh)

## Accessibility
(output from /frontend a11y delegation)

## Security
(output from /security-verify dast delegation)

## Content Quality
(output from content-analyzer.py)
```

## Output Location

Reports are written to: `docs/website-health/report-YYYY-MM-DD.md`

Multiple reports can coexist for historical comparison.

## Usage

```
```

The report command runs all 7 dimensions at full depth, then assembles results via `report-generator.sh`.
