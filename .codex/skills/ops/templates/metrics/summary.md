# Metrics — L1 Summary

## RED Methodology (the baseline)

| Signal       | What it measures                  | Example metric                            |
| ------------ | --------------------------------- | ----------------------------------------- |
| **Rate**     | Requests per second               | `http_requests_total` counter             |
| **Errors**   | Error rate (4xx/5xx)              | `http_request_errors_total` counter       |
| **Duration** | Latency percentiles (p50/p95/p99) | `http_request_duration_seconds` histogram |

Plus **Saturation** (USE method complement): CPU%, memory%, connection pool usage, queue depth.

## Stack Defaults

| Stack              | Library                             | Auto-instruments?           |
| ------------------ | ----------------------------------- | --------------------------- |
| Python/FastAPI     | `prometheus-fastapi-instrumentator` | Yes — HTTP metrics for free |
| TypeScript/Express | `prom-client` + custom middleware   | Manual (10 lines)           |
| Both               | Scrape target: Prometheus → Grafana | —                           |

## Minimal Setup (Python)

```python
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
# Exposes /metrics endpoint automatically
```

---

Ask for **patterns** to see Counter/Histogram/Gauge selection, histogram bucket sizing, label cardinality rules, and PromQL quick reference.
