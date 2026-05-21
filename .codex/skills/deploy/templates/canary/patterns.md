# Canary / Blue-Green — Key Patterns (Don't/Do/Best)

## Nginx Upstream Weight (Canary)

**Don't:** Restart Nginx for every weight change

```nginx
# BAD — requires reload every time
upstream backend { server app_v2:8000; }
```

**Do:** Use `weight=` with Nginx reload (graceful, no drop)

```nginx
# nginx.conf — 5% canary
upstream backend {
    server app_v1:8000 weight=95;
    server app_v2:8000 weight=5;
}

# Increase weight without full restart:
# nginx -s reload
```

**Best:** Use Nginx Plus or OpenResty for dynamic weight via API (no reload needed)

---

## Docker Compose (Blue-Green)

**Don't:** `docker-compose up` both versions simultaneously without a proxy

```bash
# BAD — port conflicts, undefined behavior
docker-compose up app_blue app_green
```

**Do:** Separate compose profiles, switch at the proxy level

```yaml
# docker-compose.blue.yml
services:
  app:
    image: myapp:v1
    ports: []  # no direct exposure — behind Nginx

# docker-compose.green.yml
services:
  app:
    image: myapp:v2
    ports: []
```

```bash
# Deploy green, then switch Nginx upstream
docker compose -f docker-compose.green.yml up -d
# Update nginx upstream to green, reload
nginx -s reload
# Drain and stop blue
docker compose -f docker-compose.blue.yml down
```

**Best:** Use Traefik labels for zero-downtime routing without Nginx config edits

---

## Kubernetes Rolling + Canary

**Do:** Use Deployment strategy with maxSurge/maxUnavailable

```yaml
# k8s/deployment.yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0 # never reduce capacity during rollout
  replicas: 10
```

**Canary with separate Deployment:**

```yaml
# k8s/deployment-canary.yaml
metadata:
  name: myapp-canary
spec:
  replicas: 1 # 1 canary pod out of 10 total = 10%
  template:
    spec:
      containers:
        - image: myapp:v2
```

**Best:** Use Argo Rollouts or Flagger for automated analysis + promotion

---

## Traffic Shifting Checklist

Before each step increase:

- [ ] `/deploy verify` passes (error rate + p99 within baseline)
- [ ] No new error types in logs (structlog filter: `level=error`)
- [ ] Database connections healthy (pool not exhausted)
- [ ] Dependent services healthy (third-party API timeout rate unchanged)
- [ ] Feature flag kill switch ready if flag-gated feature
