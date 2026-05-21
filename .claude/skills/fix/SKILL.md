---
name: fix
description: Fix bugs and technical debt with minimal ceremony. Issue GitHub optional — provide one for traceability or work free-form. Replaces /issue-fix.
---

# Fix Skill

## Purpose

Minimal-ceremony fix workflow for bugs and technical debt. GitHub issue is optional — provide one
for traceability, or describe the problem free-form.

Replaces `/issue-fix`. Key differences from the old skill:

- Issue number not required
- No automatic PR (opt-in with `--pr`)
- Cleaner ceremony: branch → fix → security scan → regression test → commit

## When to Use vs Other Skills

|          | `/quick`       | `/fix`            | `/implementation`  |
| -------- | -------------- | ----------------- | ------------------ |
| Ceremony | None           | Minimal           | Full               |
| Size     | Tiny (minutes) | Small-medium      | Medium-large       |
| Type     | Anything       | Bug / tech debt   | Feature / refactor |
| Issue    | Optional       | Optional          | Optional           |
| PR       | No             | Optional (`--pr`) | Yes                |
| Tests    | No             | Regression only   | Full TDD           |

## Usage

```bash
/fix "broken login after password change"
/fix --issue 42 "auth regression on mobile"
/fix --pr "memory leak in worker queue"        # create PR after commit
/fix --issue 15 --pr "null pointer in parser"  # issue + PR
```

## Workflow

### 1. Analysis

If issue provided:

```bash
gh issue view <N>
```

**Complexity check — pick one path:**

**Simple fix** (root cause obvious from description, ≤2 files, no security implications):
→ Reason through root cause directly, proceed to Step 2.

**Complex fix** (scope unclear, multiple files, security implications, or ambiguous cause):
→ Automatically enter Plan Mode:

1. Call `EnterPlanMode`
2. Spawn a Plan agent (`model: sonnet`) with all gathered context to produce:
   - Root cause analysis
   - Minimal change plan (files + rationale)
   - Regression test strategy
   - Security implications (if any)
3. Call `ExitPlanMode` — present plan to user, wait for approval
4. After approval, proceed to Step 2

> **Root cause still unclear after analysis?** Stop and run
> `/diagnose "<symptom description>"` first. Return here once the investigation
> identifies the root cause.

### 2. Branch

```bash
# With issue number
git checkout -b fix/<N>-brief-description

# Without issue (free-form)
git checkout -b fix/brief-description
```

Check for open release branches first:

```bash
git branch -r --list 'origin/release/*' | sed 's|origin/||'
```

If a release branch exists, ask: "Target release branch or main?"

### 3. Implement

Fix following these principles:

- **Minimal**: touch only what's needed — resist refactoring adjacent code
- **Secure**: validate inputs, handle errors cleanly, no data leaks
- **Defensive**: null checks, proper error boundaries

### 4. Test

Write a regression test to verify the fix:

```bash
# Python
ruff check . && mypy .
pytest -k "test_<relevant>"  # Full suite runs on CI; locally run only relevant tests

# JS/TS
npm run lint && npm run typecheck
npm test -- --testPathPattern="<relevant>"
```

Test requirements:

- Bug reproduction test (confirms fix works)
- Security edge cases if the bug has security implications
- Trivial fixes: add a test case to the nearest existing test file (no new test file needed)

### 5. Gate

Run `/security-verify scan` before committing — non-negotiable per `rules/security-gate.md`.

### 6. Commit

```bash
# With issue
git commit -m "$(cat <<'EOF'
fix: <description>

Fixes #<N>
EOF
)"

# Without issue
git commit -m "fix: <description>"
```

### 7. Optional PR

Only if `--pr` flag or explicitly requested:

```bash
gh pr create --title "fix: <description>" --body "$(cat <<'EOF'
## Root Cause
[brief]

## Fix
[what changed and why]

## Testing
- [ ] Regression test added
- [ ] Security edge cases verified
EOF
)"
```

Otherwise: push branch, leave PR for later or skip entirely.

### 8. Update CHANGELOG

Add to `[Unreleased]` section:

```
- fix: <description> (#N if applicable)
```

### 9. Smoke Tests + Review

**Always close with a short manual smoke test checklist** (3–5 items). Infer the interface type:

- **REST endpoint** → `curl` commands covering happy path + error path
- **Frontend** → numbered browser steps (open URL → action → verify state)
- **CLI** → shell commands including `--help` and one error case
- **Library** → one-liner `python -c "..."` or inline snippet

Then suggest (in order, don't skip the first):

```
→ /review changes  ← always before /pre-commit
→ /pre-commit (only if --pr flag or user explicitly asks)
```

**Do NOT jump straight to `/pre-commit`** — `/review changes` should always come first.

---

## Tech Debt Remediation

`/fix` is also the right skill for tech debt when:

- Change is isolated (no interface changes, no API breakage)
- Requires updating existing tests, not writing new suites
- Impact is contained to 1-3 files

For larger tech debt (cross-cutting, interface changes, architectural rework), use `/implementation`.
Tracking: GitHub milestone `TECH-DEBT`.

## Tips

- Keep fixes minimal — resist refactoring unrelated code
- Always document root cause in commit message or PR body for future reference
