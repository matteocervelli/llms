# Deploy — Overview

Post-merge workflow covering the gap between "PR merged" and "observability running".

## Modes

| Mode       | When to use                                                                      |
| ---------- | -------------------------------------------------------------------------------- |
| `flags`    | Setting up feature flags before or after deploy (LaunchDarkly, Flipt, env-based) |
| `canary`   | Gradual rollout — canary %, blue-green switching, traffic splitting              |
| `verify`   | Post-deploy smoke tests, health checks, SLO gate (error rate + p99)              |
| `rollback` | Trigger conditions and rollback strategies when verify fails                     |

## Suggested Flow

```
/pr-merge complete
  → /deploy flags         (if feature is flag-gated)
  → deploy to production
  → /deploy canary        (if gradual rollout needed)
  → /deploy verify        (always — smoke tests + SLO gate)
  → if verify passes → promote to 100% → /ops (long-term observability)
  → if verify fails  → /deploy rollback
```

## Ask for a Mode

Tell me which area you need:

- `/deploy flags` — feature flag setup
- `/deploy canary` — gradual rollout process
- `/deploy verify` — post-deploy smoke test checklist
- `/deploy rollback` — rollback triggers and strategies
