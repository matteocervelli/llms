---
name: quick
description: "Zero-ceremony atomic task execution. Use for tiny fixes or enhancements (minutes, not hours) that don't warrant SDLC ceremony. Flags: --discuss (disambiguate first), --full (delegate to /pre-commit after execution), --issue N (link commit to GitHub issue)."
---

# Quick Skill

## Purpose

Atomic task execution without SDLC ceremony. Fills the gap between "raw Claude" and `/fix`/`/implementation`:

- No opusplan model switch
- No task list creation
- No TDD by default
- No PR creation
- Issue GitHub optional

Use when a change takes minutes, not hours.

## When to Use vs Other Skills

|                | `/quick`       | `/fix`            | `/implementation`    |
| -------------- | -------------- | ----------------- | -------------------- |
| Ceremony       | None           | Minimal           | Full (TDD, opusplan) |
| Size           | Tiny (minutes) | Small-medium      | Medium-large         |
| Type           | Anything       | Bug / tech debt   | Feature / refactor   |
| Issue required | No             | No                | No                   |
| PR created     | No             | Optional (`--pr`) | Yes                  |
| Tests required | No             | Regression only   | Full TDD             |

## Usage

```bash
/quick fix the failing auth test
/quick --discuss add rate limiting to the API   # disambiguate before executing
/quick --full refactor the user service         # run /pre-commit after execution
/quick --issue 42 update error message          # link to GitHub issue in commit
```

## Workflow

### Bare mode (default)

1. **Snapshot** — Run `git status` and `git branch --show-current` to establish context
2. **Execute** — Implement the minimal change
   - Trivial edit (1-2 files): work on current branch
   - Slightly larger: `git checkout -b <type>/brief-description`
3. **Smoke tests** — After executing, always output a short checklist (3–5 items) the user can run manually before committing. Infer from modified files:
   - REST endpoint → `curl` commands (happy path + one error case)
   - Frontend → numbered browser steps
   - CLI → shell commands
   - Library/module → `python -c "..."` one-liner
4. **Gate** — Run `/security-verify scan` before committing (non-negotiable per `rules/security-gate.md`)
5. **Commit** — Atomic commit with conventional-commits message:
   - With issue: `fix: <description>` + `Fixes #42` in commit body
   - Without issue: `fix: <description>` or `feat: <description>`
6. **Review suggestion** — After committing, always suggest:
   > "Run `/review changes` to get a companion second opinion before moving on."
7. **Track** — Append entry to `.claude/memory/local/quick-tasks.md`

### --discuss mode

Before executing:

1. Ask 2-3 targeted disambiguation questions (scope, approach, edge cases)
2. Save decisions to `.claude/memory/local/CONTEXT.md`
3. Proceed with bare mode

### --full mode

After executing:

1. Delegate to `/pre-commit` (quality + tests + security + changelog)
2. Use this when the change touches logic where regression is a real risk

## Constraints

- Stay on current model — no `/model opus` suggestion
- No `TaskCreate` calls
- No TDD unless `--full` flag
- No `gh pr create` — use `/fix` or `/implementation` if a PR is needed
- Security scan always mandatory before commit

## Tracking: quick-tasks.md

After each execution, append to `.claude/memory/local/quick-tasks.md`:

```markdown
### YYYY-MM-DD HH:MM — <task description>

- Branch: <branch-name> or "current branch (no new branch)"
- Commit: <sha> "<message>"
- Mode: bare | discuss | full
- Issue: #N or —
```

File is session-scoped and gitignored (`memory/local/` is never committed).

## Tips

- If the change grows beyond ~30 minutes of work, switch to `/fix` or `/implementation`
- `--discuss` is especially useful when the task is ambiguous or touches multiple areas
- `--full` is for logic changes (not just config/text) where test coverage matters
