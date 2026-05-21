# Rollback — Key Patterns (Don't/Do/Best)

## Error Rate Detection Script

**Don't:** Poll manually — automate the check

```bash
# BAD — human watching a dashboard is too slow
watch -n 5 curl -s prometheus/api/v1/query?...
```

**Do:** Script that checks rate and exits with code 1 on breach

```bash
#!/usr/bin/env bash
# scripts/check-slo.sh — run after deploy, exit 1 if SLO breached
set -euo pipefail

PROM="${PROM_URL:-http://prometheus:9090}"
THRESHOLD="${ERROR_RATE_THRESHOLD:-0.01}"  # 1%

RATE=$(curl -sG "$PROM/api/v1/query" \
  --data-urlencode 'query=sum(rate(http_requests_total{status=~"5.."}[5m]))/sum(rate(http_requests_total[5m]))' \
  | jq -r '.data.result[0].value[1] // "0"')

echo "Current 5xx rate: $RATE"

# Use awk for float comparison (bash can't)
if awk -v rate="$RATE" -v threshold="$THRESHOLD" 'BEGIN{exit !(rate > threshold)}'; then
  echo "BREACH: error rate $RATE > threshold $THRESHOLD — trigger rollback"
  exit 1
fi

echo "OK: error rate within SLO"
```

**Best:** Integrate with alertmanager webhook → auto-trigger rollback pipeline on alert

---

## Feature Flag Emergency Disable

**LaunchDarkly:**

```bash
# via CLI or API — instant, no redeploy
curl -X PATCH "https://app.launchdarkly.com/api/v2/flags/production/new-feature" \
  -H "Authorization: $LD_API_TOKEN" \
  -H "Content-Type: application/json; domain-model=launchdarkly.semanticpatch" \
  -d '{"instructions":[{"kind":"turnFlagOff"}]}'
```

**Flipt:**

```bash
curl -X PUT "http://flipt:8080/api/v1/flags/new-feature" \
  -H "Content-Type: application/json" \
  -d '{"key":"new-feature","enabled":false,"name":"New Feature"}'
```

**Env-based:**

```bash
# Update env var → restart service (fastest if using Docker)
docker service update --env-add ENABLE_NEW_FEATURE=false myapp
```

---

## Docker Compose Rollback

```bash
#!/usr/bin/env bash
# rollback.sh — revert to previous image tag
set -euo pipefail

PREVIOUS_TAG="${1:?Usage: rollback.sh <previous-image-tag>}"
SERVICE="${2:-app}"

echo "Rolling back $SERVICE to $PREVIOUS_TAG"

# Pull previous image first (fail fast if not available)
docker pull "myapp:$PREVIOUS_TAG"

# Update compose override with previous tag
cat > docker-compose.override.yml <<EOF
services:
  $SERVICE:
    image: myapp:$PREVIOUS_TAG
EOF

docker compose up -d "$SERVICE"
echo "Rollback complete. Verify with /deploy verify"
```

---

## Kubernetes Rollout Undo

```bash
# Undo last deployment (instant — k8s keeps rollout history)
kubectl rollout undo deployment/myapp -n production

# Verify rollback status
kubectl rollout status deployment/myapp -n production

# Roll back to specific revision
kubectl rollout undo deployment/myapp --to-revision=3 -n production

# Check rollout history
kubectl rollout history deployment/myapp -n production
```

---

## Post-Rollback Checklist

- [ ] `/deploy verify` passes on previous version
- [ ] Rollback logged: timestamp, version from/to, trigger reason
- [ ] Feature flag disabled if applicable (prevent re-exposure)
- [ ] On-call notified if automatic rollback triggered in production
- [ ] Post-mortem created within 24h of production rollback
