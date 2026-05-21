# Metrics — L2 Patterns

## Auto-Instrumentation vs Custom Metrics

| Don't                                                              | Do                                                                        |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------- |
| Manually instrument every HTTP endpoint                            | Use `prometheus-fastapi-instrumentator` to get HTTP metrics for free      |
| Skip business metrics because infra metrics exist                  | Add custom counters for domain events (orders placed, payments processed) |
| Instrument at the framework level AND middleware (double-counting) | Pick one instrumentation layer                                            |

**Python — one-liner auto-instrumentation**:

```python
from prometheus_fastapi_instrumentator import Instrumentator

# After app = FastAPI()
Instrumentator(
    should_group_status_codes=True,   # 2xx, 4xx, 5xx — not individual codes
    excluded_handlers=["/health", "/metrics"],
).instrument(app).expose(app)
```

**TypeScript — minimal custom middleware**:

```typescript
import { Counter, Histogram, register } from "prom-client";

const httpRequestDuration = new Histogram({
  name: "http_request_duration_seconds",
  help: "HTTP request duration in seconds",
  labelNames: ["method", "route", "status_class"],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
});

app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on("finish", () => {
    end({
      method: req.method,
      route: req.route?.path ?? "unknown",
      status_class: `${Math.floor(res.statusCode / 100)}xx`,
    });
  });
  next();
});

app.get("/metrics", async (_req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});
```

---

## Metric Type Selection

| Type          | Use for                                                                | Example                                                       |
| ------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Counter**   | Monotonically increasing counts                                        | `http_requests_total`, `errors_total`, `jobs_processed_total` |
| **Histogram** | Measured durations or sizes (supports percentiles)                     | `http_request_duration_seconds`, `db_query_duration_seconds`  |
| **Gauge**     | Values that go up and down                                             | `active_connections`, `queue_depth`, `cache_hit_ratio`        |
| **Summary**   | Pre-calculated percentiles (avoid — not aggregatable across instances) | —                                                             |

---

## Histogram Bucket Sizing

**Don't** use default Prometheus buckets (wrong for web services). **Do** align buckets with your SLO thresholds:

```python
# For a 500ms SLO:
LATENCY_BUCKETS = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]

from prometheus_client import Histogram
request_duration = Histogram(
    "http_request_duration_seconds",
    "Request latency",
    buckets=LATENCY_BUCKETS,
)
```

The SLO boundary (0.5s here) must be a bucket boundary — otherwise you can't compute SLO compliance from the histogram.

---

## Label Cardinality Rules

| Don't                                                        | Do                                                            |
| ------------------------------------------------------------ | ------------------------------------------------------------- |
| Label by `user_id` (unbounded cardinality, kills Prometheus) | Label by `tenant_tier` (small set: free/pro/enterprise)       |
| Label by raw HTTP path (`/users/123/orders`)                 | Group routes: `/users/{id}/orders` or label by route template |
| Label by full error message                                  | Label by error class: `validation`, `auth`, `internal`        |

**Cardinality rule of thumb**: Each label should have <100 distinct values. A metric with 3 labels at 10 values each = 1,000 time series (fine). At 1,000 values each = 1 billion (catastrophic).

---

## Business Metrics Pattern

Beyond RED, track what the business cares about:

```python
from prometheus_client import Counter, Gauge

# Domain events
orders_placed = Counter("orders_placed_total", "Orders successfully placed", ["payment_method"])
active_subscriptions = Gauge("active_subscriptions", "Current active subscriptions", ["tier"])

# Usage
orders_placed.labels(payment_method="stripe").inc()
active_subscriptions.labels(tier="pro").set(current_count)
```

---

## PromQL Quick Reference

```promql
# Request rate (per second, 5m window)
rate(http_requests_total[5m])

# Error rate percentage
rate(http_requests_total{status_class="5xx"}[5m])
/ rate(http_requests_total[5m]) * 100

# p99 latency
histogram_quantile(0.99,
  rate(http_request_duration_seconds_bucket[5m])
)

# Apdex score (satisfied <100ms, tolerating <500ms)
(
  rate(http_request_duration_seconds_bucket{le="0.1"}[5m])
  + rate(http_request_duration_seconds_bucket{le="0.5"}[5m])
) / 2 / rate(http_request_duration_seconds_count[5m])
```
