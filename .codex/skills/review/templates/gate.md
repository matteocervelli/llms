# Pre-Commit Gate Prompt Template

Lightweight review for `/pre-commit` step 5. Focuses ONLY on critical bugs and security — not quality, naming, or style.

## Variables

- `$DIFF` — `git diff HEAD` (uncommitted changes)
- `$TIMEOUT` — 120s (fast gate)

## Prompt

```
You are a pre-commit gate reviewer. Focus ONLY on:
1. Critical bugs — crashes, data loss, security vulnerabilities
2. Security issues — OWASP Top 10, exposed secrets, injection

Ignore style, naming, structure, and suggestions. Only flag issues that would be dangerous to ship.

Scope: uncommitted changes

Output format:
### Critical Findings
- file:line — description (or 'None.')

--- DIFF ---
$DIFF
```

## Gate Logic

After receiving output from all companions:

- **BLOCK**: Companion flagged a critical bug or security issue → pipeline FAILS
- **PASS**: No critical findings → pipeline PASSES

## Report Line

```
Companion Review
  Gate:       PASS / WARN (1 finding) / FAIL (1 critical)
  Companions: codex (34s)
```

## Dispatch

Always uses multi-runner for consensus:

```bash
: "${HOME:=$(eval echo ~)}"
MULTI_OUTPUT=$(echo "$PROMPT" | bash "$HOME/.claude/shared/companions/multi-runner.sh" \
  --capability review --timeout 120)
```
