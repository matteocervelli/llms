# Ops — Observability Overview

No observability context detected. Choose a mode based on where you are in the post-deploy lifecycle:

| Mode        | Command          | When to use                                              |
| ----------- | ---------------- | -------------------------------------------------------- |
| `logging`   | `/ops logging`   | First thing after deploy — structured logs from day one  |
| `metrics`   | `/ops metrics`   | Once logging works — add RED metrics + custom counters   |
| `dashboard` | `/ops dashboard` | Once metrics flow — visualize them in Grafana/DataDog    |
| `alerting`  | `/ops alerting`  | Once dashboards show baselines — define SLO-based alerts |

## Suggested Sequencing

```text
deploy → /ops logging → /ops metrics → /ops dashboard → /ops alerting
```

This order matters: dashboards without metrics are empty, alerts without baselines produce false positives.

## Relationship to `/security operations`

`/security operations` covers secrets management, deployment security, and incident response.
`/ops` covers observability implementation: how to emit, collect, visualize, and act on telemetry.

They complement each other. Run both when setting up a new service.

## Quick Start

Just deployed? Start here:

```text
/ops logging
```
