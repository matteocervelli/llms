---
name: pre-commit
description: Full validation gate before committing — quality checks, tests, coverage, security scan, changelog, and companion review. Use right before a commit to verify code is ready. Trigger on "pre-commit", "validate before commit", "ready to commit", "run all checks".
allowed-tools: Read, Bash, Grep, Glob
---

# Pre-Commit Validation Skill

## Purpose

Complete validation gate before committing code. Orchestrates quality checks, test execution, coverage verification, and security scanning.

## Quick Start

```bash
/pre-commit                                # Full pipeline including changelog + companion review
/pre-commit --fast                         # Lite mode: quality + staged security only (no tests/changelog/companion)
/pre-commit --dast http://localhost:8000   # Full pipeline + DAST against running app
/pre-commit --skip-companion               # Skip companion review gate
/pre-commit --skip-changelog               # Skip changelog generation
/pre-commit --skip-companion --skip-changelog  # Quality + tests + security only
```

## Validation Pipeline

```
/pre-commit (full)                         /pre-commit --fast
    |                                           |
    +-> 1. Security Scan (full repo)            +-> 1. Security Scan (staged files only)
    |       - Secret detection                  |       - scanner-runner.sh --staged
    |       - Dependency audit                  |
    |       - Code pattern check                +-> 2. Quality Check (staged files only)
    |                                           |
    +-> 2. Quality Check (full project)         +-> PASS/FAIL Report
    |       - Formatting (ruff format/prettier)
    |       - Linting (ruff check/eslint)
    |       - Type checking (mypy/tsc)
    |
    +-> 3. Test Execution
    |       - Run test suite
    |       - Verify all pass
    |
    +-> 4. Coverage Check
    |       - Measure coverage
    |       - Enforce 80% threshold
    |
    +-> 4b. DAST (only with --dast <url>)
    |       - dast-runner.sh <url>
    |       - HTTP headers, CORS, TLS, info disclosure
    |       - nuclei templates (if installed)
    |       - Requires app running at <url>
    |
    +-> 5. Changelog Update (default, --skip-changelog to bypass)
    |       - Find last version tag
    |       - Gather commits since tag + staged changes
    |       - Diff against existing [Unreleased] section
    |       - Add missing entries to [Unreleased]
    |       - Propose semver bump + tag
    |       - Stage updated CHANGELOG.md
    |
    +-> 6. Companion Review (default, --skip-companion to bypass)
    |       - Lightweight prompt: critical bugs + security only
    |       - multi-runner.sh --capability review --timeout 120
    |       - Gate: BLOCK on unanimous critical, WARN on majority critical
    |
    +-> PASS/FAIL Report
```

### --fast mode

Use when iterating quickly after an already-validated commit:

- Quality check on staged files only (no type-check)
- Security scan on staged files only (`--staged`)
- No tests, no coverage, no changelog, no companion review

Not a substitute for a full pre-commit before the final feature commit.

## Commands by Language

### Python Project

```bash
# 1. Quality
ruff format --check src/ tests/
ruff check src/ tests/
mypy src/

# 2. Tests (fast suite — integration/e2e run on CI)
pytest -v -m "not integration and not e2e"

# 3. Coverage — CI only (not run locally; full suite needed for accurate numbers)
# pytest --cov=src --cov-fail-under=80 --cov-report=term-missing

# 4. Security (full repo scan)
# bandit requires Python ≤3.13 (3.14 removed AST .s/.n attrs used by bandit ≤1.8.x)
# Use: python3.13 -m bandit (pip install bandit under 3.13 first if needed)
python3.13 -m bandit -r src/ -ll
pip-audit
```

### JavaScript/TypeScript Project

```bash
# 1. Quality
npx prettier --check "src/**/*.{ts,tsx}"
npx eslint "src/**/*.{ts,tsx}"
npx tsc --noEmit

# 2. Tests
npm test

# 3. Coverage
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'

# 4. Security
npm audit --production
```

## Step 4c: Migration Health Check (conditional)

Runs only if `alembic.ini` exists in the project:

```bash
if [[ -f alembic.ini ]]; then
  # Check for multiple migration heads (merge conflict indicator)
  HEADS=$(alembic heads 2>/dev/null | wc -l)
  if [[ "$HEADS" -gt 1 ]]; then
    echo "FAIL: $HEADS migration heads detected (expected 1)"
    echo "Fix: alembic merge heads -m 'merge_pre_commit'"
  fi

  # Check for unapplied migrations
  alembic check 2>/dev/null || echo "WARN: pending migrations not applied to dev DB"
fi
```

**Gate:**

- Multiple heads → FAIL (must merge before commit)
- Unapplied migrations → WARN (advisory)
- No `alembic.ini` → SKIP (not a migration project)

## Step 4d: Workflow File Audit (conditional)

Runs only if `.forgejo/workflows/` exists in the project:

```bash
if [[ -d .forgejo/workflows ]]; then
  BLOCKED=$(grep -rl 'secrets\.FORGEJO_' .forgejo/workflows/ 2>/dev/null)
  if [[ -n "$BLOCKED" ]]; then
    echo "FAIL: reserved secret prefix in workflow files:"
    echo "$BLOCKED"
    echo "Forgejo blocks secrets starting with FORGEJO_. Use auto-injected \$FORGEJO_TOKEN instead."
    exit 1
  fi
fi
```

**Gate:**

- `secrets.FORGEJO_*` found → FAIL (`FORGEJO_` prefix is reserved — secret can never be created)
- No `.forgejo/workflows/` → SKIP

## Step 5: Changelog Update (`/release changelog`, default)

Runs by default. Skip with `--skip-changelog`. Delegates to `/release changelog`.

**Delegate to `/release changelog`.** It handles:

- Finding last version tag
- Gathering commits since tag + staged changes
- Diffing against existing `[Unreleased]` section
- Adding missing entries per conventional commit type
- Proposing semver bump (proposal only — tagging is a separate decision)
- Staging `CHANGELOG.md`

If no `CHANGELOG.md` exists, `/release changelog` creates one from its template.

**Skip Step 6 (version bump propagation) when called from /pre-commit** — version bumps happen at release time via `/release full`, not at pre-commit time.

## Step 6: Review Gate (`/review gate`, default)

Runs by default. Skip with `--skip-companion`. Uses `/review gate` — a lightweight companion review focused on critical bugs and security only. Cost: ~$0.05/run.

### Dispatch

```bash
LIGHTWEIGHT_PROMPT="You are a pre-commit gate reviewer. Focus ONLY on:
1. Critical bugs — crashes, data loss, security vulnerabilities
2. Security issues — OWASP Top 10, exposed secrets, injection

Ignore style, naming, structure, and suggestions. Only flag issues that would be dangerous to ship.

Scope: uncommitted changes

Output format:
### Critical Findings
- file:line — description (or 'None.')

--- DIFF ---
$DIFF"

: "${HOME:=$(eval echo ~)}"
MULTI_OUTPUT=$(echo "$LIGHTWEIGHT_PROMPT" | bash "$HOME/.claude/shared/companions/multi-runner.sh" \
  --capability review --timeout 120)
```

### Gate Logic

- **BLOCK**: All companions flagged the same critical issue (UNANIMOUS critical) → pipeline FAILS
- **WARN**: >50% of companions flagged a critical issue (MAJORITY critical) → pipeline PASSES with warning
- **PASS**: No critical findings, or only SOLO findings → pipeline PASSES

### Report Line

```
Companion Review
  Gate:       PASS / WARN (1 finding) / FAIL (1 unanimous critical)
  Companions: codex, gemini (34s)
```

## Thresholds

| Check                          | Threshold | Required                                   |
| ------------------------------ | --------- | ------------------------------------------ |
| Format                         | 0 errors  | Yes                                        |
| Lint                           | 0 errors  | Yes                                        |
| Type check                     | 0 errors  | Yes                                        |
| Tests                          | 100% pass | Yes                                        |
| Coverage                       | >= 80%    | CI only (not run locally)                  |
| Security (critical)            | 0 issues  | Yes                                        |
| Security (high)                | 0 issues  | Recommended                                |
| DAST (critical/high)           | 0 issues  | Yes (only with `--dast <url>`)             |
| Changelog (missing entries)    | 0 missed  | Advisory (skip with `--skip-changelog`)    |
| Companion (unanimous critical) | 0 issues  | Yes (skip with `--skip-companion`)         |
| Companion (majority critical)  | 0 issues  | Recommended (skip with `--skip-companion`) |

## Output Format

### PASS

```
=====================================
PRE-COMMIT VALIDATION: PASS
=====================================

Quality
  Format:     PASS
  Lint:       PASS
  Types:      PASS

Testing
  Tests:      PASS (45/45)
  Coverage:   87% (threshold: 80%)

Security
  Secrets:    PASS
  Deps:       PASS
  Patterns:   PASS
  DAST:       PASS (0 critical/high) | SKIP (no --dast flag)

Changelog (skip with --skip-changelog)
  Entries:    3 added (2 new, 1 catch-up)
  Proposed:   v1.3.0 (MINOR — new features detected)
  Tag when ready: git tag v1.3.0 && git push --tags

Companion Review (skip with --skip-companion)
  Gate:       PASS
  Companions: codex, gemini (34s)

Ready to commit!
=====================================
```

### FAIL

```
=====================================
PRE-COMMIT VALIDATION: FAIL
=====================================

Quality
  Format:     PASS
  Lint:       FAIL (3 errors)
  Types:      PASS

Testing
  Tests:      FAIL (2/45 failed)
  Coverage:   N/A (tests failed)

Security
  Secrets:    PASS
  Deps:       WARN (1 medium CVE)
  Patterns:   PASS

Changelog (skip with --skip-changelog)
  Entries:    1 added (0 new, 1 catch-up)
  Catch-up:   fix: multi-runner default_exclude (ae89a50)
  Proposed:   v1.2.4 (PATCH — fixes only)

Companion Review (skip with --skip-companion)
  Gate:       FAIL (1 unanimous critical)
  Companions: codex, gemini (28s)
  Finding:    NPE in auth.js:42 (unanimous critical)

Issues to fix:
1. Lint errors in src/utils.py:23, 45, 67
2. Test failures in tests/test_api.py
3. Consider updating 'requests' package
4. [Companion] NPE in auth.js:42 — unanimous critical from all companions

Run individual tools for details:
  ruff check src/
  pytest tests/test_api.py -v
=====================================
```

## Quick Fix Commands

When validation fails, run these to auto-fix what's possible:

### Python

```bash
# Auto-format (replaces black + isort)
ruff format src/ tests/

# Auto-fix linting
ruff check --fix src/ tests/

# Update vulnerable deps
pip install --upgrade <package>
```

### JavaScript/TypeScript

```bash
# Auto-format
npx prettier --write "src/**/*.{ts,tsx}"

# Auto-fix linting
npx eslint --fix "src/**/*.{ts,tsx}"

# Fix vulnerabilities
npm audit fix
```

## Integration with Git

### Pre-commit Hook (Optional)

If you want automatic validation before every commit:

```bash
# .git/hooks/pre-commit
#!/bin/bash
claude /pre-commit
if [ $? -ne 0 ]; then
    echo "Pre-commit validation failed. Fix issues before committing."
    exit 1
fi
```

### Manual Workflow (Recommended)

Run `/pre-commit` manually before committing:

```bash
# Make changes
claude "implement feature X"

# Validate before commit
claude /pre-commit

# If PASS, commit
git add -A && git commit -m "feat: implement feature X"
```

## Skipping Checks (Not Recommended)

If you must skip validation (emergency hotfix):

```bash
# Skip pre-commit hook
git commit --no-verify -m "hotfix: emergency fix"

# Document technical debt
# TODO: Run /pre-commit and fix issues in follow-up PR
```

## Gotchas

- Bandit requires Python ≤3.13 — Python 3.14 removed `.s`/`.n` AST attributes; bandit ≤1.8.x crashes and silently reports 0 findings. Use `python3.13 -m bandit` (path: `python3.13 -m bandit`).
- JS audit gates on CRITICAL only, not HIGH — HIGH vulns in transitive/dev deps are noise, not actionable; gating on them erodes trust in the gate.
- Config-only repos (markdown/YAML/text only, no executable code or secrets) qualify for scan skip — note "config-only repo, scan skipped" explicitly before committing.
- `--staged` security scan needs bash 4+ (macOS ships 3.2) — on macOS use full-repo scan instead.
- Coverage is a CI-only gate — `/pre-commit` does not run it locally; the fast test suite (`-m "not integration and not e2e"`) runs locally, full suite on CI.

## Troubleshooting

### Tests Fail

```bash
# Run specific failing test with verbose output
pytest tests/test_module.py::test_name -v -s

# Run with debug
pytest --pdb tests/test_module.py
```

### Coverage Below Threshold

```bash
# See what's not covered
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Type Errors

```bash
# See full error details
mypy src/ --show-error-codes --pretty
```

## Success Criteria

All checks must pass before commit:

- [ ] `ruff format --check` passes
- [ ] `ruff check` has 0 errors
- [ ] `mypy` has 0 errors
- [ ] All tests pass
- [ ] Coverage >= 80% (CI gate)
- [ ] No critical/high security issues
- [ ] No hardcoded secrets
- [ ] CHANGELOG.md [Unreleased] section up to date (no missed commits)
