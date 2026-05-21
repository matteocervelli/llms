# Accessibility — L1 Summary

**Delegates to**: `/frontend a11y` (full WCAG 2.1 AA audit)

## What Gets Checked

1. **Automated scan** — axe-core (via /frontend a11y) + pa11y (if installed)
2. **Lighthouse a11y score** — Cross-referenced from performance dimension
3. **Color contrast** — 4.5:1 normal text, 3:1 large text (WCAG 1.4.3)
4. **Keyboard navigation** — All interactive elements reachable via Tab
5. **Screen reader** — ARIA roles, labels, landmarks present
6. **Images** — All non-decorative images have descriptive alt text

## Tool Chain

| Tool             | Coverage                             | Install               |
| ---------------- | ------------------------------------ | --------------------- |
| `/frontend a11y` | Full WCAG 2.1 AA (axe-core + manual) | Always available      |
| `pa11y`          | Complementary automated checks       | `npm i -g pa11y`      |
| Lighthouse       | Accessibility score (0-100)          | `npm i -g lighthouse` |

## Gate

- PASS: `/frontend a11y` reports no critical issues
- WARN: Minor issues (missing lang attributes, redundant ARIA)
- FAIL: Critical issues (missing alt text, no keyboard access, contrast failures)

---

Ask for **patterns** to see axe-core rule categories and common Hugo accessibility issues.
