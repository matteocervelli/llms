---
paths:
  - "CHANGELOG.md"
  - "CHANGELOG*"
  - "pyproject.toml"
  - "package.json"
  - "setup.cfg"
  - "Cargo.toml"
  - ".github/**/*"
---

# Release Workflow

Trunk-based release engineering. Propose steps, never block.

## Trunk-Based Model

Solo dev default: feature branches merge directly to main. No release branches needed.

```
/release plan (milestone) → implementation → review changes → pre-commit → ship → pr-merge
  → when milestone complete: /release verify commits → /release changelog → tag
  → post-tag: /release verify tags → close milestone → /release plan for next
```

## Branch Model

- **Primary (trunk-based):** Feature branches `<type>/<issue>-<description>` branch from and merge to main
- **Required (release branches):** `release/vX.Y.Z` cut from main — **required when `staging.yml` exists in the project** (staging validates migrations against prod DB; skip at your peril)
- **Legacy (release branches without staging):** use only for multi-maintainer stabilization
- Feature branches: `<type>/<issue>-<description>` (cut from main OR release/\* if legacy mode)

> **Rule:** If `.forgejo/workflows/staging.yml` is present and triggers on `release/**`, trunk-based tagging is blocked — use the release-branch flow.

## Transition Suggestions

After plan approval:

- Suggest creating task list (TaskCreate) before writing code

After implementation complete:

- Suggest `/review changes` before `/pre-commit`
- Suggest `/review solve "problem"` if architectural doubts emerged
- Suggest `/frontend verify` if frontend files were modified

After PR creation:

- If CI fails: suggest `/pr-fix <number>`
- If no reviews yet: suggest `/review pr --pr <number>`

After merge (Step 6 of /pr-merge handles this automatically):

- Suggest deleting merged branch (confirm first)
- Suggest analyzing open branches (merged candidates, stale 30+ days)
- If milestone complete: `/release verify commits` → `/release changelog` → tag
- If just tagged: `/release verify tags` → close milestone
- Check milestone: propose closing if 0 open issues remain
- Check migration heads: warn if >1 alembic head detected

## Version Planning Trigger

When user mentions "release", "version", "milestone", "what to ship" → suggest `/release plan`

## Context Management

When approaching context limits during any phase, proactively write `continuation.md` with current task state and pending work. Suggest 1M-token model if task needs finishing in one go.
