# Rollback — L1 Essentials

## Trigger Conditions

| Condition                         | Type      | Action                     |
| --------------------------------- | --------- | -------------------------- |
| 5xx error rate > 1% absolute      | Automatic | Shift traffic to previous  |
| p99 latency > baseline × 1.5      | Automatic | Shift traffic to previous  |
| Health endpoint returning non-200 | Automatic | Abort deploy immediately   |
| Core feature returning wrong data | Manual    | Flag kill switch OR revert |
| External dependency timeout spike | Manual    | Review before rolling back |
| Data corruption detected          | Manual    | STOP traffic, escalate     |

## 3 Rollback Strategies

| Strategy               | Speed    | When to use                                    |
| ---------------------- | -------- | ---------------------------------------------- |
| Traffic drain (canary) | Instant  | Canary step — shift weight back to old version |
| Feature flag disable   | Instant  | Flag-gated feature — flip to false             |
| Git revert + redeploy  | 5–15 min | Full deploy rollback, no canary available      |

## Decision Flow

```
Verify gate fails?
  → Is it flag-gated? → Disable flag (instant, no redeploy)
  → Is it a canary?   → Drain traffic to previous (nginx weight → 0%)
  → Full deploy?      → git revert + emergency redeploy
  → Data corruption?  → Stop traffic NOW, escalate to on-call
```

## Non-Negotiable

- **Do not rollback DB migrations without a tested down-migration** — data loss risk
- **Log the rollback event** — include version numbers, trigger reason, timestamp
- **Post-mortem required** for any automatic rollback in production

## Next Steps

- For shell scripts, flag disable patterns, k8s rollout undo → ask for **patterns**
