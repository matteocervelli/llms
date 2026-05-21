# Privacy — L2 Patterns

## GDPR-Compliant Cookie Consent (Opt-In)

```html
<!-- Minimum-viable consent banner structure -->
<div id="cookie-banner" role="dialog" aria-label="Cookie consent">
  <p>
    We use cookies to improve your experience.
    <a href="/cookie-policy">Cookie policy</a> |
    <a href="/privacy-policy">Privacy policy</a>
  </p>
  <div class="consent-actions">
    <button id="consent-accept-all">Accept All</button>
    <button id="consent-reject-all">Reject All</button>
    <button id="consent-customize">Customize</button>
  </div>
</div>
```

Rules: no pre-checked boxes, banner must be visible before any scroll/interaction,
"Reject All" must be as easy to reach as "Accept All" (equal prominence, same click depth).

## Cookie Categories (Minimum Granularity)

| Category    | Examples                         | Requires Consent |
| ----------- | -------------------------------- | ---------------- |
| Essential   | session IDs, CSRF tokens, auth   | No               |
| Analytics   | GA4, Umami, Plausible, Matomo    | Yes              |
| Marketing   | Meta Pixel, Google Ads, LinkedIn | Yes              |
| Preferences | language, theme, UI state        | Yes (debated)    |

## Conditional Script Loading (JavaScript)

```js
// Load analytics ONLY after user accepts
const consentKey = "gdpr_consent";

function getConsent() {
  try {
    return JSON.parse(localStorage.getItem(consentKey) || "{}");
  } catch {
    return {};
  }
}

function saveConsent(categories) {
  localStorage.setItem(
    consentKey,
    JSON.stringify({
      ...categories,
      timestamp: new Date().toISOString(),
      version: "1",
    }),
  );
}

function loadAnalytics() {
  if (getConsent().analytics !== true) return;
  const s = document.createElement("script");
  s.src = "https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX";
  s.async = true;
  document.head.appendChild(s);
}

document.getElementById("consent-accept-all").addEventListener("click", () => {
  saveConsent({ analytics: true, marketing: true });
  loadAnalytics();
  hideBanner();
});

document.getElementById("consent-reject-all").addEventListener("click", () => {
  saveConsent({ analytics: false, marketing: false });
  hideBanner();
});

// On page load — restore consent
window.addEventListener("DOMContentLoaded", () => {
  const c = getConsent();
  if (c.timestamp) {
    hideBanner();
    if (c.analytics) loadAnalytics();
  }
});
```

## Hugo Template — Conditional GA/Umami Loading

```html
{{/* layouts/partials/analytics.html */}} {{ if not
.Site.Params.cookieConsent.required }} {{/* Consent not required (e.g., Umami
with no PII) */}}
<script
  defer
  data-website-id="{{ .Site.Params.umamiId }}"
  src="{{ .Site.Params.umamiUrl }}"
></script>
{{ else }} {{/* Loaded by JS consent manager after user accepts */}}
<script>
  window.__analyticsId = "{{ .Site.Params.gaId }}";
</script>
{{ end }}
```

## Set-Cookie Best Practices

```
Set-Cookie: session_id=abc123; Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=86400
Set-Cookie: csrf_token=xyz; Secure; SameSite=Strict; Path=/; Max-Age=3600
```

| Flag       | Value             | Why                                      |
| ---------- | ----------------- | ---------------------------------------- |
| `Secure`   | (flag)            | HTTPS-only transmission                  |
| `HttpOnly` | (flag)            | Block JS access (XSS protection)         |
| `SameSite` | `Lax` or `Strict` | CSRF protection                          |
| `Max-Age`  | seconds           | Explicit expiry; avoid session cookies   |
| `Path`     | `/`               | Scope to application root                |
| `Domain`   | omit if possible  | Over-broad domain = wider attack surface |

## Privacy Policy — GDPR Article 13 Minimum Requirements

A valid privacy notice must state:

1. **Identity** of the data controller (company name, address, contact)
2. **DPO contact** (if applicable)
3. **Purposes and legal basis** for each processing activity
4. **Legitimate interests** (if used as legal basis)
5. **Recipients** or categories of recipients of personal data
6. **Third-country transfers** and safeguards (if any)
7. **Retention periods** for each data category
8. **Data subject rights**: access, rectification, erasure, portability, objection
9. **Right to withdraw consent** (if consent is the legal basis)
10. **Right to lodge a complaint** with supervisory authority

## Cookie Policy Structure

For each cookie, document:

| Cookie Name | Domain               | Category  | Purpose      | Duration | Type       |
| ----------- | -------------------- | --------- | ------------ | -------- | ---------- |
| `_ga`       | google-analytics.com | Analytics | Track visits | 2 years  | Persistent |
| `session`   | yourdomain.com       | Essential | Auth session | Session  | Session    |

## Third-Party Tracker Audit Process

1. Open site in incognito / private window (no existing cookies)
2. Open DevTools → Network tab → filter by "third-party" or check domains
3. DevTools → Application → Cookies: confirm zero non-essential cookies before any click
4. Click "Accept All" → verify analytics scripts load
5. Repeat with "Reject All" → verify no analytics scripts load
6. Export cookie list and update cookie policy table

Tools: `privacy-checker.sh` (automated), browser DevTools, uBlock Origin Logger.
