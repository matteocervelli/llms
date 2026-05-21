# WCAG 2.1 Level AA Accessibility Report Template

Use this template for generating accessibility compliance reports.

---

````markdown
# WCAG 2.1 Level AA Accessibility Report

**Date**: [YYYY-MM-DD]
**Application**: [name]
**Pages Tested**: [count]
**Testing Method**: Automated + Manual

## Executive Summary

**Overall Compliance**: [XX]% compliant

- **Critical Issues**: [count] (must fix)
- **Serious Issues**: [count] (should fix)
- **Moderate Issues**: [count] (nice to fix)
- **Minor Issues**: [count] (best practice)

## WCAG 2.1 Compliance Status

| Principle      | Level A         | Level AA        | Notes     |
| -------------- | --------------- | --------------- | --------- |
| Perceivable    | ✅/❌ ([X]/[Y]) | ✅/❌ ([X]/[Y]) | [summary] |
| Operable       | ✅/❌ ([X]/[Y]) | ✅/❌ ([X]/[Y]) | [summary] |
| Understandable | ✅/❌ ([X]/[Y]) | ✅/❌ ([X]/[Y]) | [summary] |
| Robust         | ✅/❌ ([X]/[Y]) | ✅/❌ ([X]/[Y]) | [summary] |

## Detailed Findings

### Critical: [Issue Title]

**WCAG Criterion**: [X.X.X Title]
**Level**: A/AA
**Impact**: [who is affected]
**Pages**: [list of pages]

**Issue**: [description]

**User Impact**: [how it affects users]

**How to Fix**:

```html
<!-- Before -->
<img src="logo.png" />

<!-- After -->
<img src="logo.png" alt="Company Logo" />
```
````

**WCAG Reference**: [link]

---

## Testing Summary

### Automated Testing (Axe-core)

- Pages scanned: [count]
- Violations found: [count]
- Rules checked: [count]

### Manual Testing

- Keyboard navigation: ✅/❌
- Screen reader (NVDA): ✅/❌
- Screen reader (VoiceOver): ✅/❌
- Zoom to 200%: ✅/❌
- Mobile accessibility: ✅/❌

### Browser Testing

- Chrome: ✅/❌
- Firefox: ✅/❌
- Safari: ✅/❌
- Edge: ✅/❌

## Recommendations

### Immediate (Critical)

1. [Fix 1]
2. [Fix 2]

### Short-term (Serious)

1. [Fix 1]

### Long-term (Moderate)

1. [Fix 1]

## Resources

- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- WebAIM: https://webaim.org/
- A11y Project: https://www.a11yproject.com/

## Certification

This application [IS / IS NOT] compliant with WCAG 2.1 Level AA.

**Assessor**: [name]
**Date**: [YYYY-MM-DD]
**Next Review**: [YYYY-MM-DD]

````

---

## Issue Severity Levels

| Severity | Impact | Response |
|----------|--------|----------|
| Critical | Blocks users | Fix immediately |
| Serious | Significant barrier | Fix before release |
| Moderate | Some difficulty | Fix in next iteration |
| Minor | Best practice | Improve when possible |

---

## Common Issue Templates

### Missing Alt Text

**Issue**: Images missing alternative text
**Criterion**: 1.1.1 Non-text Content (Level A)
**Fix**:
```html
<!-- Before -->
<img src="product.jpg">

<!-- After -->
<img src="product.jpg" alt="Blue running shoes, side view">
````

### Insufficient Contrast

**Issue**: Text does not meet contrast ratio
**Criterion**: 1.4.3 Contrast (Minimum) (Level AA)
**Fix**:

```css
/* Before: contrast 2.5:1 */
color: #888;

/* After: contrast 4.5:1 */
color: #595959;
```

### Missing Form Labels

**Issue**: Form inputs without labels
**Criterion**: 1.3.1 Info and Relationships (Level A)
**Fix**:

```html
<!-- Before -->
<input type="email" placeholder="Email" />

<!-- After -->
<label for="email">Email Address</label>
<input type="email" id="email" />
```

### Missing Skip Link

**Issue**: No way to bypass navigation
**Criterion**: 2.4.1 Bypass Blocks (Level A)
**Fix**:

```html
<a href="#main" class="skip-link">Skip to main content</a>
<nav>...</nav>
<main id="main">...</main>
```
