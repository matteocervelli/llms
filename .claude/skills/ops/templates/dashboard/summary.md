# Dashboard — L1 Summary

## 5 Mandatory Panels for Any Production Service

1. **Request Rate** — RPS over time (time series)
2. **Error Rate** — % of 4xx+5xx responses (stat panel, red when >1%)
3. **Latency p99** — 99th percentile request duration (time series)
4. **Saturation** — CPU% + memory% for the service instance (gauge)
5. **Downstream Health** — DB latency, Redis latency, external API error rate (time series)

Plus one SLO panel: "Are we within error budget?" — single stat, green/red.

## Platform Selection

| Platform       | Best for                       | Notes                    |
| -------------- | ------------------------------ | ------------------------ |
| **Grafana**    | Self-hosted Prometheus stacks  | Free, JSON-configurable  |
| **DataDog**    | If already paying for APM/logs | Better UX, higher cost   |
| **CloudWatch** | AWS-native infrastructure      | Built-in, limited PromQL |

All three support the same conceptual panels — just different JSON/config format.

## Variable Templating (Grafana)

Always add `$datasource` and `$job` template variables so dashboards are portable across environments (dev/staging/prod).

---

Ask for **patterns** to see Grafana panel JSON for FastAPI and Next.js stacks, panel type guide, and DataDog/CloudWatch mapping.
