# Dashboard — L2 Patterns

## Panel Type Guide

| What you want to show           | Panel type  | Notes                                          |
| ------------------------------- | ----------- | ---------------------------------------------- |
| Trend over time (rate, latency) | Time series | Default for most metrics                       |
| Current state (error rate %)    | Stat        | Add thresholds: green <1%, yellow <5%, red >5% |
| Capacity usage                  | Gauge       | Shows fill level — good for saturation         |
| Top-N slow endpoints            | Table       | Sort by p99 descending                         |
| SLO compliance                  | Stat        | Single number: "99.7% availability this month" |

---

## Grafana Variable Templating

Always add these at the top of every dashboard — makes it portable across dev/staging/prod:

```json
"templating": {
  "list": [
    {
      "name": "datasource",
      "type": "datasource",
      "query": "prometheus"
    },
    {
      "name": "job",
      "type": "query",
      "datasource": "$datasource",
      "query": "label_values(up, job)"
    }
  ]
}
```

Then reference as `{job="$job"}` in all panel queries.

---

## FastAPI Golden Signals — Grafana Panel Definitions

Paste these panel objects into `dashboard.panels[]`. Assumes `$datasource` and `$job` variables.

**Request Rate**:

```json
{
  "title": "Request Rate",
  "type": "timeseries",
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{job=\"$job\"}[5m])) by (status_class)",
      "legendFormat": "{{status_class}}"
    }
  ],
  "fieldConfig": { "defaults": { "unit": "reqps" } }
}
```

**Error Rate %**:

```json
{
  "title": "Error Rate",
  "type": "stat",
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{job=\"$job\",status_class=\"5xx\"}[5m])) / sum(rate(http_requests_total{job=\"$job\"}[5m])) * 100"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "thresholds": {
        "steps": [
          { "color": "green", "value": null },
          { "color": "yellow", "value": 1 },
          { "color": "red", "value": 5 }
        ]
      }
    }
  }
}
```

**p99 Latency**:

```json
{
  "title": "Latency p99",
  "type": "timeseries",
  "targets": [
    {
      "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{job=\"$job\"}[5m])) by (le))",
      "legendFormat": "p99"
    },
    {
      "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{job=\"$job\"}[5m])) by (le))",
      "legendFormat": "p50"
    }
  ],
  "fieldConfig": { "defaults": { "unit": "s" } }
}
```

---

## Next.js / Node.js Adaptations

Replace FastAPI-specific metrics with Node equivalents:

```json
{
  "title": "Event Loop Lag",
  "type": "timeseries",
  "targets": [
    {
      "expr": "nodejs_eventloop_lag_seconds{job=\"$job\"}",
      "legendFormat": "lag"
    }
  ],
  "fieldConfig": { "defaults": { "unit": "s" } }
}
```

```json
{
  "title": "Heap Usage",
  "type": "gauge",
  "targets": [
    {
      "expr": "nodejs_heap_size_used_bytes{job=\"$job\"} / nodejs_heap_size_total_bytes{job=\"$job\"} * 100"
    }
  ],
  "fieldConfig": { "defaults": { "unit": "percent", "max": 100 } }
}
```

---

## DataDog / CloudWatch Conceptual Mapping

| Grafana concept          | DataDog equivalent             | CloudWatch equivalent      |
| ------------------------ | ------------------------------ | -------------------------- |
| Time series panel        | Timeseries widget              | Metric widget (line)       |
| Stat panel               | Query value widget             | Single metric              |
| Gauge panel              | Query value with gauge display | —                          |
| Template variable `$job` | Template variable (tag filter) | Dimension filter           |
| Alerting threshold       | Monitor threshold              | CloudWatch alarm threshold |
| Prometheus `rate()`      | `.rollup("rate")`              | `SampleCount` / period     |

---

## Anti-Patterns

| Anti-pattern                   | Why it's bad                                 | Fix                                           |
| ------------------------------ | -------------------------------------------- | --------------------------------------------- |
| >15 panels on one dashboard    | Cognitive overload — nobody reads it         | One dashboard per service, one row per signal |
| No time range context          | You can't tell if "42 errors" is good or bad | Always show rate vs absolute count            |
| No baseline / no alerts        | Dashboard becomes a passive artifact         | Add thresholds + link to runbook              |
| One dashboard for all services | Can't quickly isolate a specific service     | Use `$job` variable to scope                  |
| Panels without units           | "42" — 42 what?                              | Always set `fieldConfig.defaults.unit`        |
