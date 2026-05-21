# Security Checklist — L1 Essential Controls

Use before ANY production deployment. All items are **Critical** priority.

## Backend Security

### Authentication

- [ ] Password hashing: Argon2id (not bcrypt, not SHA)
- [ ] Session storage: Redis with `secrets.token_urlsafe(32)` IDs
- [ ] Cookie name: `__Host-session` prefix
- [ ] Cookie flags: `httponly=True, secure=True, samesite="strict"`

### Multi-Tenant

- [ ] Tenant context: From session middleware, NEVER from request body/query
- [ ] Every query: Includes `tenant_id` filter
- [ ] AuthContext dependency: Used on all protected endpoints

### Input Validation

- [ ] Pydantic models: `extra = "forbid"` on all models
- [ ] User HTML: Sanitized with bleach
- [ ] File uploads: Content-type verified via magic bytes

### SQL Safety

- [ ] No string interpolation: All queries use ORM or bound parameters
- [ ] No raw SQL: `text(f"...")` patterns eliminated

### Secrets

- [ ] SecretStr: All credentials use Pydantic SecretStr
- [ ] No .env in git: `.env` in `.gitignore`
- [ ] secrets manager CLI: Secrets loaded at deploy time

### CSRF

- [ ] CSRF tokens: Signed, tied to session
- [ ] HTMX header: X-CSRF-Token on all requests

## Frontend Security

### XSS Prevention

- [ ] Auto-escape: Jinja2 `default_for_string=True`
- [ ] No `| safe`: On user input
- [ ] sanitize_html filter: For user HTML content
- [ ] safe_json filter: For script tag data

### CSRF

- [ ] Meta tag: `<meta name="csrf-token">`
- [ ] HTMX injection: configRequest listener adds header

### Cookies

- [ ] Session: `__Host-` prefix, httponly, secure, strict
- [ ] CSRF: `__Host-` prefix, secure, strict

### External Scripts

- [ ] SRI hashes: All CDN scripts have integrity attribute
- [ ] crossorigin: Set to "anonymous"

### Data Exposure

- [ ] No internal IDs: Use hashids for public identifiers
- [ ] Public models: Separate from internal models

## Database Security

### Connections

- [ ] SSL required: `ssl=require` in connection string
- [ ] Timeouts: `statement_timeout=30000`

### Multi-Tenant

- [ ] tenant_id column: On all user data tables
- [ ] Foreign key: To tenants table

### Users

- [ ] App user: Not superuser
- [ ] Separate roles: app, readonly, migration, backup

### Redis

- [ ] Password: requirepass configured
- [ ] Bind: Localhost or Docker network only

## Infrastructure Security

### Docker

- [ ] Non-root user: USER directive in Dockerfile
- [ ] no-new-privileges: In compose security_opt

### Network

- [ ] Internal network: For postgres, redis
- [ ] No exposed ports: DB ports not on host

### Host

- [ ] SSH key-only: PasswordAuthentication no
- [ ] UFW enabled: Default deny incoming
- [ ] Fail2ban: Running for SSH

### Cloudflare

- [ ] Strict SSL: Full (strict) mode
- [ ] Always HTTPS: Enabled

## Operations Security

### Deployment

- [ ] Git-based: No manual file transfers
- [ ] Health check: Before marking deploy complete
- [ ] Rollback documented: Procedure exists

### Secrets

- [ ] secrets manager CLI: All secrets from your secrets manager
- [ ] No hardcoded secrets: In code or compose files

### Backups

- [ ] Daily backups: Automated
- [ ] Encrypted: GPG before upload
- [ ] Off-site: Backblaze B2 or similar

### Monitoring

- [ ] Health endpoint: /health returns component status
- [ ] Error IDs: Generic errors with correlation ID

## Quick Verification Commands

```bash
docker compose exec app whoami                              # Expected: appuser (NOT root)
docker compose exec redis redis-cli ping                    # Expected: NOAUTH (needs password)
docker network inspect app_backend --format '{{.Internal}}' # Expected: true
sudo ufw status                                             # Expected: active with default deny
grep PasswordAuthentication /etc/ssh/sshd_config            # Expected: no
```

**If ANY item fails, DO NOT DEPLOY.**
