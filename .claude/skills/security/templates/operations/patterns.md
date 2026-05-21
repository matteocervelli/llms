# Operations Security — Key Patterns (Don't/Do/Best)

## Secrets Management

**Don't:** Secrets in .env committed to git, hardcoded in docker-compose.yml, in shell history
**Best:** secrets manager CLI (e.g. `vault kv get`, `aws secretsmanager get-secret-value`) at deploy time → temporary files (chmod 600) → Docker secrets → cleanup on exit (trap). App reads `${VAR}_FILE` paths.

## Secret Rotation

**Best:** Generate new secrets (openssl rand), backup current to secrets manager vault, update database password, update secrets manager entries, redeploy, invalidate all sessions. Quarterly schedule.

## Deployment Security

**Don't:** Manual file transfers, deploy from dirty working directory
**Best:** Git-based: check working dir clean → run tests → SSH deploy → git checkout version → compose up → alembic migrate → health check → rollback on failure. Log every deployment.

## Rollback Procedure

**Best:** List recent deployments from log, `git checkout <version>`, redeploy, health check. Keep deployment log at `/opt/app/deployments.log`.

## Health Checks

**Don't:** Simple 200 OK with no real checks
**Best:** Check each component (postgres, redis) with timeout, return status per component (healthy/degraded/unhealthy) with latency_ms. Return 503 if any unhealthy.

## Logging & Monitoring

**Don't:** `logger.info(f"User login: {email}, password: {password}")`
**Best:** structlog with PIIScrubber processor (redact password/token/email/phone). Dedicated SecurityEventLogger for auth events and access denials.

## Incident Response

**Best:** 4 severity levels: SEV1 (immediate) → SEV4 (next business day). First 5 min: check /health, docker logs, recent deployments. Preserve evidence before fixes. GDPR: 72h notification to authority.

## Data Breach Response

**Best:** Contain (stop app) → preserve evidence (logs, audit, connections) → rotate ALL secrets → invalidate sessions → full audit → document lessons → GDPR notifications.

## Backup Verification

**Best:** Monthly restoration test: download from B2 → decrypt GPG → restore to test database → verify data integrity (tenant counts) → cleanup. Automated script.

**Full SOP**: Ask for complete operations security SOP with all code examples.
