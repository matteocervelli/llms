---
name: ops
description: Post-deploy observability for production services — structured logging, RED metrics + Prometheus, Grafana dashboards, SLO-based alerting. Use when setting up monitoring or instrumenting a live service. Trigger on "add logging", "metrics", "dashboard", "alerting", "observability", "monitor this service".
allowed-tools: Read, Grep, Glob, Bash
---

# Ops — Post-Deploy Observability

Unified observability guidance for production services. Auto-detects context from project files or accepts explicit mode.

## Usage

```
/ops                  # Auto-detect from project signals
/ops logging          # Explicit: structured logging setup
/ops metrics          # Explicit: RED metrics + Prometheus instrumentation
/ops dashboard        # Explicit: Grafana/DataDog/CloudWatch dashboards
/ops alerting         # Explicit: SLO-based alerting policy
/ops overview         # Cross-mode sequencing guide
```

## Workflow

### Step 1: Determine Context

Parse `$ARGUMENTS` for explicit mode. If no arguments, run context detector:

```bash
DETECTED=$(bash "$HOME/.claude/skills/ops/lib/context-detector.sh")
```

### Step 2: Show Relevant Guidance

Based on detected or explicit mode, use progressive disclosure:

**Level 1 — Summary** (default, ~20 lines):
Read and present the summary template for the detected mode. This is the entry point.

**Level 2 — Patterns** (on request, ~60-80 lines):
When the user asks for more detail, "show me patterns", code examples, or "Don't/Do/Best" style guidance, read the patterns template.

**Level 3 — Full SOP** (future):
Not yet available. If the user asks for a complete reference, offer to dive into patterns and answer specific questions.

### Step 3: Handle Multiple Contexts

If context-detector returns multiple modes (e.g., "logging,metrics"):

- Show summary for each detected mode
- Ask: "Which area do you want to dive deeper into?"

### Step 4: No Context Detected

If detection returns "none" and no explicit mode was given:

- Read and show `templates/overview.md`
- Let the user choose which mode to start with

## Template Locations

### Summary Templates (~20 lines each — L1 default)

| Mode        | File                                                  |
| ----------- | ----------------------------------------------------- |
| `logging`   | `~/.claude/skills/ops/templates/logging/summary.md`   |
| `metrics`   | `~/.claude/skills/ops/templates/metrics/summary.md`   |
| `dashboard` | `~/.claude/skills/ops/templates/dashboard/summary.md` |
| `alerting`  | `~/.claude/skills/ops/templates/alerting/summary.md`  |

### Patterns Templates (~60-80 lines each — L2 on request)

| Mode        | File                                                   |
| ----------- | ------------------------------------------------------ |
| `logging`   | `~/.claude/skills/ops/templates/logging/patterns.md`   |
| `metrics`   | `~/.claude/skills/ops/templates/metrics/patterns.md`   |
| `dashboard` | `~/.claude/skills/ops/templates/dashboard/patterns.md` |
| `alerting`  | `~/.claude/skills/ops/templates/alerting/patterns.md`  |

### Reference Templates

| Mode       | File                                         |
| ---------- | -------------------------------------------- |
| `overview` | `~/.claude/skills/ops/templates/overview.md` |

## Progressive Disclosure Rules

1. **Always start at L1** — never dump 300+ lines unprompted
2. **Read templates on demand** — use the Read tool to load templates, don't memorize content
3. **User drives depth** — "show patterns", "show me the code", "how do I set up X" triggers L2
4. **Cross-reference, don't duplicate** — if user asks about PII scrubbing in logging, cite `/security operations` rather than reproducing the PIIScrubber code here

## Relationship to Other Skills

- **`/security operations`**: Covers secrets management, deployment security, incident response. `/ops` covers observability implementation. They complement each other — run both for a new service.
- **`/infrastructure-setup`**: Sets up the base stack (Docker, DB, API layer). `/ops` adds the observability layer on top.
- **`/implementation`**: After implementing a feature, consider `/ops metrics` to add domain-specific counters.

## Examples

**Auto-detected metrics context** (prometheus.yml found):

> → context-detector returns "metrics"
> → Read and show `templates/metrics/summary.md`
> → User: "show me how to add custom counters"
> → Read and show `templates/metrics/patterns.md`

**Explicit logging request**:

> User: `/ops logging`
> → Read and show `templates/logging/summary.md`

**No context, overview**:

> User: `/ops`
> → context-detector returns "none"
> → Read and show `templates/overview.md`

**Cross-reference on PII**:

> User asks about PII in logging patterns
> → Cite `/security operations` for the PIIScrubber implementation
> → Do NOT reproduce the full class here
