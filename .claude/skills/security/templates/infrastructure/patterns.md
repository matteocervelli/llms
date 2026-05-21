# Infrastructure Security — Key Patterns (Don't/Do/Best)

## Docker Container Hardening

**Don't:** `FROM python:3.12` + run as root, `privileged: true`, `network_mode: host`
**Best:** Multi-stage build (builder → slim runtime), `USER appuser` (uid 1000), HEALTHCHECK, `no-new-privileges:true`, `cap_drop: ALL`, `read_only: true`, resource limits (cpus: 2.0, memory: 1G)

## Docker Compose Security

**Best:** YAML anchor `x-common-security` for shared security config, Docker secrets (file-based), separate networks (dmz, app_net, data_net internal), json-file logging with size limits

## Network Isolation

**Don't:** All services on same network, DB ports exposed to host
**Best:** 3-tier network: DMZ (nginx, ports 80/443) → app_net (app) → data_net (postgres, redis, internal: true). Static IP assignments per subnet.

## Nginx Hardening

**Best:** `server_tokens off`, rate limiting zones (general: 10r/s, login: 1r/s), TLSv1.3 only, Cloudflare IP allowlist with `set_real_ip_from`, security headers (HSTS, X-Frame-Options DENY, nosniff), block dotfiles, reject invalid Host headers (return 444)

## Firewall (UFW)

**Best:** Default deny incoming, allow 22 (rate limited), 80, 443. Block Docker internal subnets from external. Medium logging.

## Garage S3 Security

**Don't:** Admin API exposed to network, no bucket quotas
**Best:** Admin on localhost only, per-app keys with minimal permissions, bucket quotas, tenant-prefixed object keys with path traversal prevention (`replace("..", "").lstrip("/")`)

## Cloudflare Configuration

**Best:** Strict SSL mode, always HTTPS, min TLS 1.2, WAF rules blocking threat_score > 30 and path traversal, rate limiting on /auth/login (5 req/min per IP)

## Ubuntu Host Hardening

**Best:** unattended-upgrades + fail2ban, SSH: key-only, no root login, MaxAuthTries 3, strong ciphers only. Kernel hardening: rp_filter, ignore broadcasts, no source routing, syncookies.

**Full SOP**: Ask for complete infrastructure security SOP with all code examples.
