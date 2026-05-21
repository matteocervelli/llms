# Post-Deploy Verification — Key Patterns (Don't/Do/Best)

## Health Check Script

**Don't:** Only check HTTP 200 — response body can lie

```bash
# BAD — 200 doesn't mean the service is healthy
curl -s https://service/health && echo "ok"
```

**Do:** Assert key fields in the response body

```bash
#!/usr/bin/env bash
# scripts/smoke-test.sh
set -euo pipefail

BASE_URL="${1:-https://your-service}"

echo "=== Post-Deploy Smoke Test ==="

# 1. Health endpoint
HEALTH=$(curl -sf --max-time 5 "$BASE_URL/health")
echo "$HEALTH" | jq -e '.status == "ok"' > /dev/null || { echo "FAIL: health"; exit 1; }
echo "$HEALTH" | jq -e '.db == "ok"' > /dev/null || { echo "FAIL: db"; exit 1; }
echo "PASS: health"

# 2. Error rate (requires Prometheus — see PromQL below)
# 3. Latency p99 (see PromQL below)

echo "=== All checks passed ==="
```

**Best:** Wrap in a CI job that runs automatically on deploy completion

---

## Prometheus PromQL — Post-Deploy Checks

```promql
# 5xx error rate (last 5 minutes)
sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m]))

# p99 latency (last 5 minutes)
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)

# Compare to pre-deploy baseline (shift window by deploy time offset)
# Replace 30m with time since last deploy
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m] offset 30m)) by (le)
)
```

Run via Prometheus API:

```bash
PROM="http://prometheus:9090"
QUERY='histogram_quantile(0.99,sum(rate(http_request_duration_seconds_bucket[5m]))by(le))'
curl -sG "$PROM/api/v1/query" --data-urlencode "query=$QUERY" | jq '.data.result[0].value[1]'
```

---

## Log Tail Pattern

```bash
# Tail recent errors (structlog / JSON format)
# Adjust container name as needed
docker logs --since 5m myapp 2>&1 | jq 'select(.level == "error")'

# Count errors by type in last 5 minutes
docker logs --since 5m myapp 2>&1 | \
  jq -r 'select(.level == "error") | .event' | \
  sort | uniq -c | sort -rn
```

---

## Synthetic Transaction (key feature smoke test)

```bash
# Example: test auth + protected endpoint
TOKEN=$(curl -sf -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"smoke@test.local","password":"'$SMOKE_PASSWORD'"}' \
  | jq -r '.access_token')

[[ -z "$TOKEN" || "$TOKEN" == "null" ]] && { echo "FAIL: auth"; exit 1; }

STATUS=$(curl -so /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/users/me")

[[ "$STATUS" == "200" ]] || { echo "FAIL: protected endpoint (got $STATUS)"; exit 1; }
echo "PASS: auth + protected endpoint"
```

Store `SMOKE_PASSWORD` in secrets manager, never in code.
