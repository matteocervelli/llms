# Frontend Security — L1 Essentials

**Stack**: Jinja2 + HTMX + Chart.js + TypeScript/Vite + pnpm | SSR-first, Multi-tenant

| Control          | Requirement                                           |
| ---------------- | ----------------------------------------------------- | ------------------- |
| Auto-escaping    | Jinja2 `default_for_string=True`, `default=True`      |
| User HTML        | Sanitize with bleach, never `                         | safe` on user input |
| HTMX config      | `selfRequestsOnly: true`, `allowScriptTags: false`    |
| CSP              | Nonce-based for inline scripts, whitelist CDNs        |
| Cookies          | `__Host-` prefix, httponly (session), samesite=strict |
| CSRF             | Meta tag + HTMX configRequest header injection        |
| External scripts | SRI hashes + `crossorigin="anonymous"`                |
| Data exposure    | Public hashids, not sequential internal IDs           |
| Error pages      | Generic with error_id, no stack traces or paths       |

**Deeper**: Ask for patterns (Don't/Do/Best) or full SOP.
