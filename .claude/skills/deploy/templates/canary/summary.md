# Canary / Blue-Green — L1 Essentials

## When to Use Which

| Strategy   | Best for                           | Rollback speed |
| ---------- | ---------------------------------- | -------------- |
| Canary     | Gradual confidence, A/B data       | Fast (shift %) |
| Blue-Green | Zero-downtime with instant cutover | Instant        |
| Rolling    | Stateless services, simple deploys | Slow (drain)   |

## Canary Process (4 Steps)

```
Step 1: 5%  → deploy new version to 5% of traffic
Step 2: monitor → watch error rate + p99 for 10–15 min (use /deploy verify)
Step 3: 50% → if metrics are clean, increase to 50%
Step 4: 100% → full promotion, decommission old version
```

**Abort condition:** If error rate > baseline × 1.5 or p99 > baseline × 1.5 at any step → revert to 0%.

## Blue-Green Prerequisite

- Two identical environments (blue = live, green = new)
- DNS/LB switch is the cutover mechanism
- Both environments must share the same DB schema (no breaking migrations mid-flip)

## Non-Negotiable

- **Never skip step 1 (5%)** — the first canary slice catches most issues
- **Database migrations must run before traffic shift** — not after
- **Health check must pass on new version** before routing any traffic

## Next Steps

- For Nginx / Docker / Kubernetes patterns → ask for **patterns**
