---
name: deploy
description: Post-merge deployment workflow covering feature flags, canary/blue-green rollout, smoke-test verification, and rollback triggers. Use after a PR is merged and you need to ship it safely to production. Trigger on "deploy", "roll out", "canary", "feature flag", "rollback".
allowed-tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
---

# Deploy — Post-Merge Deployment Workflow

Structured guidance for everything between `/pr-merge` (code merged) and `/ops` (long-term observability). Covers feature flags, gradual rollout, post-deploy verification, and rollback conditions. Auto-detects context from project signals or accepts explicit subcommand.

## Usage

```
/deploy              # Auto-detect from project signals
/deploy flags        # Explicit: feature flag setup (LaunchDarkly, Flipt, env-based)
/deploy canary       # Explicit: canary / blue-green gradual rollout
/deploy verify       # Explicit: post-deploy smoke tests and SLO gate
/deploy rollback     # Explicit: rollback trigger conditions and strategies
```

## Workflow

### Step 1: Determine Context

Parse `$ARGUMENTS` for explicit mode. If no arguments, run context detector:

```bash
DETECTED=$(bash "$HOME/.claude/skills/deploy/lib/context-detector.sh")
```

### Step 2: Show Relevant Guidance

Based on detected or explicit mode, use progressive disclosure:

**Level 1 — Summary** (default, ~15 lines):
Read and present the summary template. This is the entry point.

**Level 2 — Patterns** (on request, ~60 lines):
When the user asks for more detail, "show me patterns", code examples, or "Don't/Do/Best" style guidance, read the patterns template.

**Level 3 — Full SOP** (future):
Not yet available. Dive into patterns and answer specific questions instead.

### Step 3: Handle Multiple Contexts

If context-detector returns multiple modes (e.g., "verify,rollback"):

- Show summary for each detected mode
- Ask: "Which area do you want to dive deeper into?"

### Step 4: No Context Detected

If detection returns "none" and no explicit mode was given:

- Read and show `templates/overview.md`
- Let the user choose which mode to start with

## Template Locations

### Summary Templates (~15 lines each — L1 default)

| Mode       | File                                                    |
| ---------- | ------------------------------------------------------- |
| `flags`    | `~/.claude/skills/deploy/templates/flags/summary.md`    |
| `canary`   | `~/.claude/skills/deploy/templates/canary/summary.md`   |
| `verify`   | `~/.claude/skills/deploy/templates/verify/summary.md`   |
| `rollback` | `~/.claude/skills/deploy/templates/rollback/summary.md` |

### Patterns Templates (~60 lines each — L2 on request)

| Mode       | File                                                     |
| ---------- | -------------------------------------------------------- |
| `flags`    | `~/.claude/skills/deploy/templates/flags/patterns.md`    |
| `canary`   | `~/.claude/skills/deploy/templates/canary/patterns.md`   |
| `verify`   | `~/.claude/skills/deploy/templates/verify/patterns.md`   |
| `rollback` | `~/.claude/skills/deploy/templates/rollback/patterns.md` |

### Reference Templates

| Mode       | File                                            |
| ---------- | ----------------------------------------------- |
| `overview` | `~/.claude/skills/deploy/templates/overview.md` |

## Progressive Disclosure Rules

1. **Always start at L1** — never dump 300+ lines unprompted
2. **Read templates on demand** — use the Read tool to load templates, don't memorize content
3. **User drives depth** — "show me patterns", "give me code", "how do I set up X" triggers L2
4. **Cross-reference, don't duplicate** — for secrets in flags, cite `/security operations`; for post-deploy metrics, cite `/ops metrics`

## Relationship to Other Skills

- **`/pr-merge`**: Merge is the trigger. `/deploy` is the next step after the PR lands on main.
- **`/ops`**: Covers long-term observability (logging, metrics, dashboards, alerting). `/deploy verify` is the immediate post-deploy gate; `/ops` sets up the sustained monitoring layer.
- **`/security operations`**: Covers secrets management and deployment security. Use before configuring flag SDK credentials.
- **`/implementation`**: After implementing a flagged feature, use `/deploy flags` to wire the flag evaluation into the request path.

## Examples

**Auto-detected flags context** (launchdarkly in deps):

> → context-detector returns "flags"
> → Read and show `templates/flags/summary.md`
> → User: "show me the SDK patterns"
> → Read and show `templates/flags/patterns.md`

**Explicit canary request**:

> User: `/deploy canary`
> → Read and show `templates/canary/summary.md`

**No context, overview**:

> User: `/deploy`
> → context-detector returns "none"
> → Read and show `templates/overview.md`

**Post-merge verification flow**:

> PR merged → `/deploy verify` → smoke tests pass → promote to 100% traffic
> → if any check fails → `/deploy rollback`

## Gotchas

- Never roll back a DB migration without a tested down-migration — data loss risk. Stop traffic and escalate instead.
- Automatic rollback triggers on 5xx > 1% absolute, p99 > baseline × 1.5, or health endpoint non-200 — these fire without manual confirmation; know them before deploying.
- Flag-gated and canary rollbacks are instant (flip flag / drain traffic); only a full-deploy rollback needs `git revert + redeploy` (5–15 min) — pick the fastest path that applies.
- Every automatic rollback in production requires a post-mortem, and the rollback event must be logged (version numbers, trigger, timestamp).
