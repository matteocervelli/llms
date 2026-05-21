---
name: security
description: Stack-specific security implementation guidance (backend, frontend, database, infrastructure, operations) with auto-detection from your changes. Use when implementing a feature securely or hardening code as you write it. Trigger on "how do I secure this", "security best practices", "is this secure", "harden this". For scanning existing code use /security-verify.
allowed-tools: Read, Grep, Glob, Bash
---

# Security — Implementation SOPs

Unified security guidance for your stack. Auto-detects context from edited files or accepts explicit mode.

## Usage

```
/security                     # Auto-detect stack from git changes
/security backend             # Explicit: FastAPI + SQLAlchemy + Redis
/security frontend            # Explicit: Jinja2 + HTMX + TypeScript/Vite
/security database            # Explicit: PostgreSQL + pgvector + Redis
/security infrastructure      # Explicit: Docker + Nginx + Cloudflare
/security operations          # Explicit: Deployment + secrets + monitoring
/security matrix              # Cross-reference matrix (L1/L2/L3)
/security checklist           # L1 essential pre-deployment checklist
```

## Workflow

### Step 1: Determine Context

Parse `$ARGUMENTS` for explicit mode. If no arguments provided, detect context:

```bash
DETECTED=$(bash "$HOME/.claude/skills/security/lib/context-detector.sh")
```

### Step 2: Show Relevant Guidance

Based on detected or explicit mode, use progressive disclosure:

**Level 1 — Summary** (default, ~10 lines):
Show the summary template for the detected stack. This is the entry point.

**Level 2 — Patterns** (on request, ~50 lines):
When user asks for more detail, patterns, or "Don't/Do/Best" examples, show the patterns template.

**Level 3 — Full SOP** (on request, ~500-1100 lines):
When user asks for the complete SOP, read the full source skill file.

### Step 3: Handle Multiple Stacks

If context-detector returns multiple stacks (e.g., "backend,frontend"):

- Show summary for each detected stack
- Let user choose which to dive deeper into

### Step 4: No Context Detected

If detection returns "none" and no explicit mode:

- Show the matrix template as overview
- List available modes for user to choose

## Template Locations

### Summary Templates (~10 lines each)

| Mode           | File                                                            |
| -------------- | --------------------------------------------------------------- |
| backend        | `~/.claude/skills/security/templates/backend/summary.md`        |
| frontend       | `~/.claude/skills/security/templates/frontend/summary.md`       |
| database       | `~/.claude/skills/security/templates/database/summary.md`       |
| infrastructure | `~/.claude/skills/security/templates/infrastructure/summary.md` |
| operations     | `~/.claude/skills/security/templates/operations/summary.md`     |

### Patterns Templates (~50 lines each, Don't/Do/Best)

| Mode           | File                                                             |
| -------------- | ---------------------------------------------------------------- |
| backend        | `~/.claude/skills/security/templates/backend/patterns.md`        |
| frontend       | `~/.claude/skills/security/templates/frontend/patterns.md`       |
| database       | `~/.claude/skills/security/templates/database/patterns.md`       |
| infrastructure | `~/.claude/skills/security/templates/infrastructure/patterns.md` |
| operations     | `~/.claude/skills/security/templates/operations/patterns.md`     |

### Reference Templates

| Mode      | File                                               |
| --------- | -------------------------------------------------- |
| matrix    | `~/.claude/skills/security/templates/matrix.md`    |
| checklist | `~/.claude/skills/security/templates/checklist.md` |

## Progressive Disclosure Rules

1. **Always start with summary** — don't dump 1,100 lines unprompted
2. **Read templates on demand** — use the Read tool to load templates, don't memorize content
3. **User drives depth** — "show patterns", "full SOP", "show me the code" trigger deeper levels
4. **Combine when relevant** — if user edits both .py and Dockerfile, show both backend + infrastructure summaries

## Examples

**Auto-detected backend work:**

> User edited `src/auth.py`
> → context-detector returns "backend"
> → Read and show `templates/backend/summary.md`
> → User: "show me password hashing patterns"
> → Read and show `templates/backend/patterns.md`

**Explicit infrastructure request:**

> User: `/security infrastructure`
> → Read and show `templates/infrastructure/summary.md`

**No context, overview requested:**

> User: `/security`
> → context-detector returns "none"
> → Read and show `templates/matrix.md`

**Pre-deployment check:**

> User: `/security checklist`
> → Read and show `templates/checklist.md`
