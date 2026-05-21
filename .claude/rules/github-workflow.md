---
paths:
  - ".github/**"
  - "CHANGELOG.md"
  - "CHANGELOG*"
---

# GitHub Workflow Conventions

## Issue Naming

```
[MILESTONE|ORDER] [PRIORITY] #ISSUE Title
```

- `MILESTONE` — sprint name (e.g. `SPRINT-1`) or permanent bucket (`BACKLOG`, `TECH-DEBT`, `BUG`, `DOCUMENTATION`)
- `ORDER` — absolute sequential position across all issues in that milestone
- `PRIORITY` — P0/P1/P2/P3 (see table below)
- `#ISSUE` — GitHub issue number
- `Title` — short imperative title (conventional-commits prefix optional: `feat`, `fix`, `docs`…)

Examples:

- `[BACKLOG|01] [P2] #89 Refactor auth module`
- `[SPRINT-1|13] [P2] #135 File Upload feature`
- `[v3.10|05] [P1] #42 OAuth2 integration`

## Priority Levels

| P0 | Critical — immediate | P1 | High — this week |
| P2 | Medium — this sprint | P3 | Low — when available |

## Labels (Minimal Set)

Only three: `bug` (#d73a4a), `enhancement` (#a2eeef), `documentation` (#0075ca). Priority lives in the title.

## Permanent Milestones

Every repo: `BACKLOG`, `BUG`, `TECH-DEBT`, `DOCUMENTATION`.

Sprint: `SPRINT-{n}` or `SPRINT-{n}-{feature}`. Version: `v{major}.{minor}`.
