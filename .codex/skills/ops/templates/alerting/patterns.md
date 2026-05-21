# Alerting — L2 Patterns

## Burn Rate vs Static Thresholds

| Don't                                  | Do                                                         |
| -------------------------------------- | ---------------------------------------------------------- |
| `error_rate > 1%` with no time context | Multi-window burn rate: fast (1h) + slow (6h)              |
| Alert on every spike                   | Alert when error budget is consumed faster than acceptable |
| Same threshold for all services        | Define SLO per service, derive threshold from it           |

**Multi-window burn rate formula (Prometheus)**:

```promql
# Fast burn: consuming error budget at 14.4× rate over 1h (exhausts monthly budget in ~2 days)
(
  sum(rate(http_requests_total{job="$job",status_class="5xx"}[1h]))
  / sum(rate(http_requests_total{job="$job"}[1h]))
) > (14.4 * (1 - 0.999))

# Slow burn: consuming at 6× rate over 6h (exhausts monthly budget in ~5 days)
(
  sum(rate(http_requests_total{job="$job",status_class="5xx"}[6h]))
  / sum(rate(http_requests_total{job="$job"}[6h]))
) > (6 * (1 - 0.999))
```

Replace `0.999` with your SLO (e.g., `0.995` for 99.5%).

---

## SLO Definition Template

```yaml
# service-slo.yaml
service: api-gateway
slo:
  availability:
    target: 99.9%
    error_budget_minutes_per_month: 43.8
    measurement: "1 - (5xx_requests / total_requests)"
  latency:
    target: 95% of requests < 500ms
    measurement: "histogram_quantile(0.95, http_request_duration_seconds_bucket)"
```

| SLO   | Error budget / month | Fast burn multiplier | Slow burn multiplier |
| ----- | -------------------- | -------------------- | -------------------- |
| 99.9% | 43.8 min             | 14.4×                | 6×                   |
| 99.5% | 3.6 hours            | 14.4×                | 6×                   |
| 99.0% | 7.2 hours            | 14.4×                | 6×                   |

---

## Runbook Structure (Mandatory for Every Alert)

Every Alertmanager rule must include a `runbook_url` annotation. Minimum runbook content:

```markdown
# Alert: HighErrorBurnRate

**Impact**: Users are seeing elevated errors. Error budget is being consumed.

**Trigger condition**: Error rate burn rate > 14.4× for 1h OR > 6× for 6h

**First 3 commands**:

1. `kubectl logs -l app=api-gateway --tail=100 | grep ERROR`
2. `curl https://api.example.com/health`
3. Check recent deploys: `gh run list --limit 5`

**Common causes**:

- Bad deploy in last 30 min → rollback with `./scripts/rollback.sh`
- Downstream dependency down → check status page, enable circuit breaker
- Traffic spike exceeding capacity → scale up replica count

**Escalation**: SEV1 → #incidents channel + page on-call lead
```

---

## Alertmanager Receiver Config

**PagerDuty**:

```yaml
receivers:
  - name: pagerduty-critical
    pagerduty_configs:
      - routing_key: ${PAGERDUTY_ROUTING_KEY}
        severity: critical
        description: "{{ .CommonAnnotations.summary }}"
        details:
          runbook: "{{ .CommonAnnotations.runbook_url }}"

route:
  receiver: pagerduty-critical
  group_by: [alertname, job]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
```

**OpsGenie**:

```yaml
receivers:
  - name: opsgenie-critical
    opsgenie_configs:
      - api_key: ${OPSGENIE_API_KEY}
        priority: P1
        message: "{{ .CommonAnnotations.summary }}"
        description: "{{ .CommonAnnotations.description }}"
        details:
          runbook: "{{ .CommonAnnotations.runbook_url }}"
```

---

## Inhibition Rules (Prevent Alert Storms During Deploy)

```yaml
inhibit_rules:
  # Suppress downstream alerts when the upstream service is already alerting
  - source_match:
      alertname: ServiceDown
    target_match_re:
      alertname: HighErrorRate|HighLatency
    equal: [job]

  # Suppress all non-critical alerts when SEV1 is firing
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: [job]
```

---

## Alert Fatigue Anti-Patterns

| Anti-pattern                        | Why it's bad                    | Fix                                                         |
| ----------------------------------- | ------------------------------- | ----------------------------------------------------------- |
| Every alert pages                   | On-call burnout within weeks    | SEV3/SEV4 go to ticket, not page                            |
| Alerts without runbooks             | On-call wastes time triaging    | Require `runbook_url` in every rule                         |
| Alerts with no clear owner          | Nobody acts, alert gets ignored | Add `team` label to every alert                             |
| Same person on-call forever         | Burnout, knowledge silo         | Rotate weekly, document rotation in runbook                 |
| Alert storms on deploy              | 30 alerts firing simultaneously | Add inhibition rules + deploy window silences               |
| Static thresholds that never update | Alert becomes background noise  | Review thresholds quarterly against actual traffic patterns |
