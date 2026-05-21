# Security — L1 Summary

**Delegates to**: `/security-verify dast <url>` (OWASP HTTP checks)

## DAST Coverage (from /security-verify)

- HTTP Security Headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
- Cookie Security (Secure, HttpOnly, SameSite flags)
- CORS configuration
- TLS/SSL (protocol version, certificate)
- Information disclosure (server version, sensitive paths)
- Open redirects

## Additional Checks (this dimension)

| Check              | PASS                 | WARN             | FAIL                    |
| ------------------ | -------------------- | ---------------- | ----------------------- |
| Certificate expiry | >30 days             | 7-30 days        | <7 days or expired      |
| SRI on CDN scripts | All have `integrity` | >50% have SRI    | <50%                    |
| Mixed content      | 0 HTTP on HTTPS      | 1-2 non-critical | Script/iframe over HTTP |

## Gate

- PASS: DAST clean + all additional checks pass
- WARN: DAST has medium findings OR cert <30 days OR partial SRI
- FAIL: DAST has critical/high findings OR cert <7 days OR mixed active content

---

Ask for **patterns** for Netlify security headers, SRI generation, and CSP policies.
