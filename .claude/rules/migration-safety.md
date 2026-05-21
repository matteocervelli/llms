---
paths:
  - "alembic.ini"
  - "alembic/**"
  - "migrations/**"
  - "prisma/**"
---

# Migration Safety

Rules for projects with database migrations. Prevents migration conflicts in parallel branches.

## DB Naming Convention

Per-worktree databases use: `{app}_dev_{branch_slug}` where `branch_slug` replaces `/` and `-` with `_`.

Main dev DB is always the default from `.env` / `.env.local` — never clone or reference production.

## Single Head Enforcement

Before creating a PR, verify exactly one migration head:

```bash
HEADS=$(alembic heads 2>/dev/null | wc -l)
[[ "$HEADS" -gt 1 ]] && echo "FAIL: merge heads first" && alembic merge heads -m "merge_$(git branch --show-current)"
```

## Snapshot Protocol

Before starting branch work (if not using worktree isolation):

```bash
pg_dump "$MAIN_DB" > .claude/db-snapshots/main-$(date +%s).sql
```

Restore before verifying migrations in pre-PR (use the most recent snapshot):

```bash
SNAPSHOT=$(ls -t .claude/db-snapshots/main-*.sql 2>/dev/null | head -1)
psql "$MAIN_DB" < "$SNAPSHOT"
alembic upgrade head  # must succeed from clean state
```

## Post-Merge Check

After merging a branch with migrations, check for multiple heads on main:

```bash
git checkout main && git pull
HEADS=$(alembic heads 2>/dev/null | wc -l)
[[ "$HEADS" -gt 1 ]] && echo "Create merge migration: alembic merge heads"
```

## Graceful Degradation

If `pg_dump`, `createdb`, or `alembic` are missing, skip migration protocol and report as SKIPPED.
Do not block the workflow — migration safety is advisory for solo dev.
