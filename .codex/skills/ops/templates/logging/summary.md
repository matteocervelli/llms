# Logging — L1 Summary

## Three Non-Negotiables

1. **Structured over text** — Emit JSON from day one. grep-able text logs don't survive scaling.
2. **PII scrubbing** — Strip password, token, email, phone before any log leaves the process. See `/security operations` for the PIIScrubber processor pattern.
3. **Correlation IDs** — Bind a `request_id` to every log line so you can trace a full request across services.

## Stack Defaults

| Stack      | Library                                      | Sink (dev)      | Sink (prod)                |
| ---------- | -------------------------------------------- | --------------- | -------------------------- |
| Python     | `structlog` + JSON renderer                  | stdout (pretty) | stdout → Loki / CloudWatch |
| TypeScript | `pino`                                       | `pino-pretty`   | stdout → Loki / CloudWatch |
| Both       | Avoid `print()` / `console.log` in prod code | —               | —                          |

## Log Levels

`DEBUG` (dev only) → `INFO` (normal events) → `WARNING` (degraded, recoverable) → `ERROR` (failures) → `CRITICAL` (data loss risk)

Set level via environment variable at startup. Never hardcode.

---

Ask for **patterns** to see structlog processor chain, pino setup, correlation ID binding, and sink selection examples.
