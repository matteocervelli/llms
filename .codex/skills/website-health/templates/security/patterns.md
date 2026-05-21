# Security — L2 Patterns

## Running the Checks

### Via /security-verify dast (primary)

```
/security-verify dast https://example.com
```

Runs OWASP DAST checks: headers, cookies, CORS, TLS, info disclosure.

### Certificate Expiry Check

```bash
# Check cert expiry date
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null \
  | openssl x509 -noout -dates

# Or via curl
curl -vI https://example.com 2>&1 | grep "expire date"
```

### SRI Check

```bash
# Find CDN scripts without integrity attribute
curl -sL https://example.com | python3 -c "
import sys, re
html = sys.stdin.read()
scripts = re.findall(r'<script[^>]+src=[\"\\x27]([^\"\\x27]+)[\"\\x27][^>]*>', html)
for s in scripts:
    if '://' in s and 'integrity' not in html[html.index(s)-200:html.index(s)]:
        print(f'Missing SRI: {s}')
"
```

### Mixed Content Check

```bash
# Find HTTP resources on HTTPS page
curl -sL https://example.com | python3 -c "
import sys, re
html = sys.stdin.read()
mixed = re.findall(r'(src|href|action)=[\"\\x27](http://[^\"\\x27]+)[\"\\x27]', html)
for attr, url in mixed:
    print(f'Mixed content ({attr}): {url}')
"
```

## Netlify Security Headers

Add to `static/_headers` or `netlify.toml`:

```toml
# netlify.toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
    Content-Security-Policy = "default-src 'self'; script-src 'self' https://cloud.umami.is; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
```

## SRI Generation

```bash
# Generate SRI hash for a CDN resource
curl -sL https://cdn.example.com/lib.js | openssl dgst -sha384 -binary | openssl base64 -A
# Use in HTML:
# <script src="https://cdn.example.com/lib.js"
#   integrity="sha384-<hash>" crossorigin="anonymous"></script>
```

## Hugo SRI Integration

```html
<!-- In baseof.html or head partial -->
{{ $js := resources.Get "js/main.js" | minify | fingerprint "sha384" }}
<script
  src="{{ $js.RelPermalink }}"
  integrity="{{ $js.Data.Integrity }}"
  crossorigin="anonymous"
></script>
```

Hugo's `fingerprint` function automatically generates SRI hashes — use it for all self-hosted assets.

## CSP for Hugo + Umami + Ahrefs

```
Content-Security-Policy: default-src 'self'; script-src 'self' https://cloud.umami.is https://analytics.ahrefs.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://cloud.umami.is https://analytics.ahrefs.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self'
```

## Common Static Site Security Mistakes

| Mistake                 | Fix                                         |
| ----------------------- | ------------------------------------------- |
| No HSTS header          | Add via Netlify `_headers`                  |
| Missing CSP             | Start with report-only, tighten iteratively |
| CDN scripts without SRI | Generate hash, add `integrity` attribute    |
| HTTP images/fonts       | Update to HTTPS or self-host                |
| Server version exposed  | Netlify handles this (no action needed)     |
| No Permissions-Policy   | Deny all unused APIs (camera, mic, geo)     |
