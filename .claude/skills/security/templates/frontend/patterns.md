# Frontend Security — Key Patterns (Don't/Do/Best)

## XSS Prevention — Jinja2

**Don't:** `{% autoescape false %}{{ user_content }}{% endautoescape %}` or `{{ user.bio | safe }}`
**Do:** Let Jinja2 auto-escape (default): `{{ user.name }}`
**Best:** Configure `select_autoescape(default_for_string=True, default=True)` + custom `sanitize_html` filter using bleach with allowed tags whitelist

## HTMX Response Handling

**Don't:** `HTMLResponse(f"<div>Results for: {q}</div>")` (raw user input)
**Best:** Validate HTMX targets per route, check `HX-Request` header, use `templates.TemplateResponse`

## Content Security Policy

**Don't:** `"default-src *; script-src 'unsafe-inline' 'unsafe-eval' *"`
**Best:** Nonce-based CSP: `script-src 'self' 'nonce-{nonce}' trusted-cdns`, `frame-ancestors 'none'`, `form-action 'self'`

## Cookie Configuration

**Don't:** `response.set_cookie("session", session_id, httponly=False)`
**Best:** Session: `__Host-` prefix, httponly=True, samesite="strict", max_age=8h. CSRF: `__Host-`, httponly=False (JS reads), samesite="strict"

## SRI for External Scripts

**Don't:** `<script src="https://cdn.example.com/lib.js"></script>` (no integrity)
**Best:** `<script src="url" integrity="sha384-XXXXX" crossorigin="anonymous"></script>`

## Form CSRF Protection

**Best:** Generate signed token tied to session, inject as `<meta name="csrf-token">`, add HTMX `configRequest` listener that sets `X-CSRF-Token` header on all requests

## Data Exposure Prevention

**Don't:** Expose `user.id` (sequential int) or `tenant.full_config` in templates
**Best:** Use hashids for public identifiers, separate UserPublic model (no email/tenant_id)

## Vite Build Security

**Best:** `sourcemap: false` in prod, `drop_console: true`, `ignore-scripts=true` in .npmrc, `strict-peer-dependencies=true`

## Secure Error Pages

**Best:** Separate HTMX partial vs full-page error templates, include error_id for support, no technical details

**Full SOP**: Ask for complete frontend security SOP with all code examples.
