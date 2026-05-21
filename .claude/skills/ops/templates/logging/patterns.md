# Logging — L2 Patterns

## Log Levels

| Don't                                                 | Do                                                |
| ----------------------------------------------------- | ------------------------------------------------- |
| `DEBUG` everything in production                      | `DEBUG` only in dev — env-configurable            |
| Use print/console.log in application code             | Use the logger at the right level                 |
| Log at `ERROR` for expected failures (user not found) | `WARNING` for recoverable, `ERROR` for unexpected |

**Level guide**: DEBUG=internals, INFO=business events (user created, order placed), WARNING=degraded state (cache miss, retry), ERROR=unexpected failures, CRITICAL=data loss or security breach.

---

## Structlog Setup (Python)

```python
import structlog
import logging

def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, level.upper()),
    )
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            # Add PIIScrubber() here — see /security operations for implementation
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

logger = structlog.get_logger()
```

---

## Pino Setup (TypeScript)

```typescript
import pino from "pino";

export const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  timestamp: pino.stdTimeFunctions.isoTime,
  // In production: remove prettyPrint, pipe stdout to log aggregator
  ...(process.env.NODE_ENV === "development" && {
    transport: { target: "pino-pretty" },
  }),
});

// Per-request child logger (binds requestId to all child log lines)
export const requestLogger = (requestId: string) => logger.child({ requestId });
```

---

## Correlation IDs

**Python (FastAPI middleware)**:

```python
from contextvars import ContextVar
import uuid
from fastapi import Request

request_id_var: ContextVar[str] = ContextVar("request_id", default="")

async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request_id_var.set(request_id)
    # Bind to structlog context for this request
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    structlog.contextvars.clear_contextvars()
    return response
```

**TypeScript (Express middleware)**:

```typescript
import { randomUUID } from "crypto";

app.use((req, res, next) => {
  const requestId = (req.headers["x-request-id"] as string) ?? randomUUID();
  req.log = logger.child({ requestId });
  res.setHeader("X-Request-ID", requestId);
  next();
});
```

---

## Sink Selection

| Situation                       | Sink                                   |
| ------------------------------- | -------------------------------------- |
| Single server, simple stack     | File + logrotate (daily, keep 14 days) |
| Multiple instances / Kubernetes | stdout → Promtail → Loki → Grafana     |
| AWS-native                      | stdout → CloudWatch Logs agent         |
| Already paying for DataDog      | stdout → DataDog agent                 |

**Rule**: Never block on log writes. Use async sinks or fire-and-forget. Log loss is acceptable; application slowdown is not.

---

## What to Log

| Always log                                     | Never log                                   |
| ---------------------------------------------- | ------------------------------------------- |
| HTTP requests: method, path, status, latency   | Raw passwords or tokens                     |
| Auth events: login, logout, failed attempt     | Full PII (names, emails in body)            |
| Background jobs: start, end, item count, error | Full request/response bodies (use sampling) |
| DB queries exceeding 500ms                     | Health check endpoints (too noisy)          |
| Unhandled exceptions with full stack trace     | —                                           |
