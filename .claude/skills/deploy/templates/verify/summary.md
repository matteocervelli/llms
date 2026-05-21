# Post-Deploy Verification — L1 Essentials

## Smoke Test Checklist (run immediately after deploy)

| #   | Check                    | Pass condition                           |
| --- | ------------------------ | ---------------------------------------- |
| 1   | Health endpoint          | `GET /health` returns 200 in < 500ms     |
| 2   | Auth flow                | Login returns valid token (no 401/403)   |
| 3   | DB connectivity          | Health check includes `db: ok`           |
| 4   | Key feature (happy path) | Core user action completes without error |
| 5   | Error rate baseline      | 5xx rate ≤ pre-deploy baseline           |
| 6   | Latency p99              | p99 ≤ baseline × 1.5 (warn at ×1.25)     |
| 7   | External integrations    | Third-party API response codes unchanged |
| 8   | Log ingestion            | Logs appearing in sink (no silent drain) |

## SLO Gate

**Hard stop if any of these trigger:**

- 5xx error rate > 1% (absolute) OR > pre-deploy baseline × 2
- p99 latency > pre-deploy baseline × 1.5
- Health endpoint not returning 200

**On gate failure → immediately run `/deploy rollback`.**

## Quick Verify Command

```bash
# Minimal health check — run immediately after deploy
curl -sf https://your-service/health | jq .
```

Expected response:

```json
{ "status": "ok", "db": "ok", "version": "1.2.3" }
```

## Next Steps

- For curl scripts, PromQL queries, and log patterns → ask for **patterns**
- If gate fails → `/deploy rollback`
- If gate passes → `/ops` for long-term observability setup
