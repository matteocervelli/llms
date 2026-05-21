# Security Matrix — Cross-Reference: Layers x Components

**Stack**: FastAPI + HTMX/Jinja2 + PostgreSQL/Redis + Docker/Nginx + Cloudflare

## Quick Reference: When to Implement

| Priority         | When                          | Controls                                                                        |
| ---------------- | ----------------------------- | ------------------------------------------------------------------------------- |
| **L1 Essential** | Before any production traffic | Auth, input validation, SQL safety, tenant isolation, HTTPS, secrets management |
| **L2 Standard**  | Within first month            | Rate limiting, CSP, audit logging, backup encryption, monitoring                |
| **L3 Hardened**  | At scale / compliance         | RLS policies, encrypted PII, container hardening, penetration testing           |

## Matrix: Security Controls by Layer

### Authentication & Sessions

| Control          | Backend                       | Frontend                    | Database | Infrastructure |
| ---------------- | ----------------------------- | --------------------------- | -------- | -------------- |
| Password hashing | Argon2id (L1)                 | -                           | -        | -              |
| Session storage  | Redis with rotation (L1)      | -                           | -        | -              |
| Session cookies  | \_\_Host- prefix, Strict (L1) | HttpOnly, Secure (L1)       | -        | -              |
| CSRF protection  | Signed tokens (L1)            | Meta tag + HTMX header (L1) | -        | -              |
| Session limits   | Max per user (L2)             | -                           | -        | -              |

### Multi-Tenant Isolation

| Control           | Backend                       | Frontend             | Database                | Infrastructure           |
| ----------------- | ----------------------------- | -------------------- | ----------------------- | ------------------------ |
| Tenant context    | Middleware injection (L1)     | -                    | Session variable (L1)   | -                        |
| Query filtering   | Always include tenant_id (L1) | -                    | RLS policies (L3)       | -                        |
| Data exposure     | Public vs private models (L2) | No internal IDs (L2) | -                       | -                        |
| Storage isolation | Tenant-prefixed keys (L1)     | -                    | Partitioned tables (L3) | Garage tenant paths (L1) |

### Input Validation

| Control            | Backend                    | Frontend              | Database                   | Infrastructure             |
| ------------------ | -------------------------- | --------------------- | -------------------------- | -------------------------- |
| Schema validation  | Pydantic models (L1)       | HTML5 validation (L2) | CHECK constraints (L2)     | -                          |
| Input sanitization | bleach for HTML (L1)       | -                     | -                          | -                          |
| File validation    | Magic bytes check (L2)     | -                     | -                          | -                          |
| Size limits        | Pydantic Field limits (L1) | maxlength attrs (L1)  | Column limits (L1)         | Nginx client_max_body (L1) |
| SQL injection      | ORM only (L1)              | -                     | Parameterized queries (L1) | -                          |

### XSS & Content Security

| Control          | Backend                | Frontend               | Database | Infrastructure    |
| ---------------- | ---------------------- | ---------------------- | -------- | ----------------- |
| Auto-escaping    | -                      | Jinja2 default on (L1) | -        | -                 |
| CSP header       | -                      | Nonce-based (L2)       | -        | Nginx header (L2) |
| SRI hashes       | -                      | External scripts (L2)  | -        | -                 |
| Security headers | Middleware (L1)        | -                      | -        | Nginx (L1)        |
| HTMX hardening   | Target validation (L2) | selfRequestsOnly (L2)  | -        | -                 |

### Encryption

| Control           | Backend              | Frontend | Database             | Infrastructure         |
| ----------------- | -------------------- | -------- | -------------------- | ---------------------- |
| TLS in transit    | SSL connections (L1) | -        | ssl=require (L1)     | Cloudflare strict (L1) |
| PII at rest       | -                    | -        | pgcrypto/Fernet (L3) | -                      |
| Backup encryption | -                    | -        | -                    | GPG to B2 (L1)         |
| Secrets storage   | SecretStr (L1)       | -        | -                    | secrets manager CLI (L1)     |

### Rate Limiting

| Control           | Backend                   | Frontend | Database               | Infrastructure   |
| ----------------- | ------------------------- | -------- | ---------------------- | ---------------- |
| API rate limit    | Redis sliding window (L2) | -        | -                      | Nginx zones (L2) |
| Login rate limit  | Per IP + email (L1)       | -        | -                      | Nginx /auth (L1) |
| Connection limits | Pool settings (L2)        | -        | max_connections (L2)   | limit_conn (L2)  |
| Query timeouts    | statement_timeout (L2)    | -        | PostgreSQL config (L2) | -                |

### Container & Host Security

| Control             | Backend | Frontend | Database | Infrastructure          |
| ------------------- | ------- | -------- | -------- | ----------------------- |
| Non-root user       | -       | -        | -        | USER directive (L1)     |
| Read-only FS        | -       | -        | -        | read_only: true (L2)    |
| Capability dropping | -       | -        | -        | cap_drop: ALL (L2)      |
| Resource limits     | -       | -        | -        | deploy.resources (L2)   |
| Network isolation   | -       | -        | -        | Internal networks (L1)  |
| Host hardening      | -       | -        | -        | SSH, UFW, fail2ban (L1) |

## Implementation Checklist by Priority

### L1 Essential (Before Production)

**Backend**: Argon2, Redis sessions, \_\_Host- cookies, CSRF tokens, Pydantic validation, ORM-only queries, tenant middleware, SecretStr, generic errors
**Frontend**: Jinja2 auto-escape, CSRF meta+header, no internal IDs, secure cookies
**Database**: SSL required, non-superuser app role, tenant_id columns, statement timeouts
**Infrastructure**: Non-root containers, internal DB networks, Cloudflare strict SSL, UFW, SSH keys
**Operations**: secrets manager CLI, git-based deploy, rollback procedure, daily encrypted backups, health endpoint

### L2 Standard (First Month)

**Backend**: Sliding window rate limiting, session rotation, structured logging, file upload validation
**Frontend**: CSP with nonces, SRI hashes, HTMX target validation
**Database**: Connection pool tuning, read-only user
**Infrastructure**: Read-only FS, capability dropping, resource limits, Nginx rate limiting, WAF
**Operations**: Uptime monitoring, incident playbook, backup verification, secret rotation

### L3 Hardened (At Scale)

**Backend**: Permission-based access control, comprehensive audit logging
**Database**: RLS policies, FORCE RLS, PII encryption, partitioned vectors, audit triggers
**Infrastructure**: Bot management, container scanning, penetration testing
**Operations**: Data breach response plan, GDPR procedures, third-party audit
