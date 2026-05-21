# Alerting — L1 Summary

## Core Principle

**Alert on symptoms, not causes.** Page on "users are seeing errors", not on "disk is at 80%". Low-level causes are for dashboards; SLO violations are for pages.

## Error Budget Burn Rate over Static Thresholds

| Approach               | Problem                                            |
| ---------------------- | -------------------------------------------------- |
| `error_rate > 1%`      | Too noisy, wrong time window, arbitrary            |
| Burn rate multi-window | Alerts when budget depletes at a rate that matters |

**Fast burn** (1h window, 14.4× budget burn) → page immediately (SEV1/SEV2)
**Slow burn** (6h window, 6× budget burn) → create ticket (SEV3)

## Severity Levels

| Severity | Condition                             | Response time     |
| -------- | ------------------------------------- | ----------------- |
| **SEV1** | Complete outage or >5% error rate     | Immediate         |
| **SEV2** | Degraded + trend worsening            | 15 minutes        |
| **SEV3** | Elevated errors, within error budget  | 1 hour            |
| **SEV4** | Informational, no action required yet | Next business day |

## 3 Alerts Every Service Needs

1. **Error budget burn rate** (fast + slow windows)
2. **Saturation approaching limit** (predictive — fires before you're at 100%)
3. **Health endpoint failing** (last line of defense)

---

Ask for **patterns** to see burn rate PromQL formulas, SLO definition template, runbook structure, and Alertmanager receiver config.
