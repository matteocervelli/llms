---
name: pr-fix
description: Triage, fix, and pre-flight a PR before merge. Checks mergeability, CI, reviews, and bot comments — fixes issues, runs /pre-commit before pushing, then hands off to /pr-merge.
---

# PR Fix Skill

## Purpose

Full triage, fix, and pre-flight for a PR. Diagnoses all issues (merge conflicts, CI failures, bot comments, review requests), fixes them, enforces `/pre-commit` before pushing, then hands off to `/pr-merge` for the actual merge and post-merge workflow.

## Usage

```bash
/pr-fix <pr-number>
```

**Relationship with other skills:**

- `/pr-fix` = triage problems + fix them + pre-flight validation (you stay on the PR branch)
- `/pr-merge` = validate readiness + execute merge + post-merge workflow (docs, milestone, release)
- Use `/pr-fix` first when you know there are issues. Use `/pr-merge` when you expect the PR is ready.

## Phase 1: Full Triage

Checkout the PR branch first:

```bash
gh pr checkout <pr-number>
```

Then run ALL four sources in parallel:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
PR=<pr-number>

# 1. PR metadata — mergeability, draft state, review decision
gh pr view $PR --json mergeable,isDraft,state,reviewDecision,additions,deletions

# 2. CI check status
gh pr checks $PR --repo $REPO

# 3. Bot inline comments (Codex, Gemini, etc.)
gh api repos/$REPO/pulls/$PR/comments \
  --jq '.[] | "[\(.path):\(.line // .original_line // "?")]\n\(.body)\n---"'

# 4. Top-level reviews (approval/request-changes state)
gh pr view $PR --repo $REPO --json reviews \
  --jq '.reviews[] | "\(.author.login) [\(.state)]: \(.body)"'

# 5. Forgejo CI status (if dual-remote)
  SHA=$(gh pr view $PR --json headRefOid --jq '.headRefOid')
fi
```

If bot reviews are still `pending`, poll until complete (max 3 attempts, 30s apart):

```bash
for i in 1 2 3; do
  STATE=$(gh pr checks $PR --repo $REPO 2>&1)
  echo "$STATE"
  echo "$STATE" | grep -q "pending" && sleep 30 || break
done
```

## Phase 2: Triage Decision

### Hard Stops — Report and Exit

| Condition                | Action                                                                                                                             |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| `mergeable: CONFLICTING` | "Merge conflicts detected. Resolve first: `gh api -X PUT repos/O/R/pulls/N/update-branch` or rebase locally, then re-run /pr-fix." |
| `isDraft: true`          | "PR is a draft. Mark as ready for review first."                                                                                   |
| `state != OPEN`          | "PR is not open (state: X). Nothing to fix."                                                                                       |

### Soft Issues — Proceed to Fix Loop

| Condition                        | Route                                            |
| -------------------------------- | ------------------------------------------------ |
| CI failing                       | → Phase 3 fix loop                               |
| Bot comments (P1/P2)             | → Phase 3 fix loop                               |
| `CHANGES_REQUESTED`              | → Phase 3 fix loop (address review comments)     |
| `REVIEW_REQUIRED` (zero reviews) | Note it — addressed at Phase 6 handoff           |
| All passing, no issues           | Skip Phase 3 → go directly to Phase 4 pre-flight |

## Phase 3: Fix Loop

Fix one category at a time. Verify locally after each fix before moving to the next.

### Common Fix Patterns

**Build/Dependency Issues:**

```bash
rm -rf node_modules package-lock.json || rm -rf __pycache__ .pytest_cache
npm ci || pip install -r requirements.txt
npm run build || python -m build
```

**Test Failures:**

```bash
npm run test -- --verbose || pytest -v --tb=short -m "not integration and not e2e"
npm run test:integration || pytest tests/integration/  # CI runs full suite; run locally only if diagnosing integration failures
```

**Code Quality Issues:**

```bash
npm run lint -- --fix || ruff format . && ruff check --fix .
npm run format || prettier --write .
npm run typecheck || mypy .
```

**Security Issues:**

```bash
npm audit fix || safety check && pip-audit --fix
npx audit-ci --moderate || bandit -r src/
```

### Implementation by Failure Type

**Test Failures:**

- Unit tests: Fix broken logic, update mocks, handle edge cases
- Integration tests: Update API contracts, fix database setup
- Security tests: Address input validation, auth issues

**Quality Issues:**

- TypeScript: Fix type errors, add missing types
- Linting: Address code style violations
- Documentation: Update JSDoc, README, API docs

**Bot Review Comments (Codex P1/P2, Gemini):**

- Address each inline comment with its file:line reference
- Prioritize P1 (blocking) before P2 (advisory)

**Human Review (CHANGES_REQUESTED):**

- Address all requested changes before proceeding
- Reply to review comments after fixing

### Quick Reference by Stack

**JavaScript/TypeScript:**

```bash
npm audit fix && npm run build
npm run test -- --updateSnapshot
npm run test:coverage -- --coverageThreshold='{"global":{"branches":80}}'
npx eslint . --fix && npx prettier --write .
npx tsc --noEmit
```

**Python:**

```bash
pip install -r requirements.txt && safety check
pytest -m "not integration and not e2e"  # coverage threshold enforced on CI, not locally
ruff format . && ruff check --fix . && mypy src/
```

**Docker/Infrastructure:**

```bash
docker build -t test-image .
terraform validate && terraform plan
```

## Phase 4: Pre-flight Before Push (MANDATORY)

**Always run `/pre-commit` before pushing any fix to the PR.** This enforces the same checks CI will run — catching failures locally before they hit the pipeline and breaking the push→CI-fail→fix→repeat cycle.

```
/pre-commit
```

Runs: quality check → tests → coverage → security scan → changelog → companion gate.

**For large diffs (additions + deletions > 200 lines), also run first:**

```
/review changes --quick
```

External AI second opinion on the code changes. Address any BLOCK-level findings before pushing. `--quick` skips the deeper audits (silent-failures, types, comments) for speed.

**Do not proceed to Phase 5 until `/pre-commit` passes.**

## Phase 5: Push + Monitor

```bash
git add .
git commit -m "fix(pr): resolve PR #<pr-number> issues

- Fixed: [specific issue description]
- Tests: [test fixes applied if any]
- Security: [security issues resolved if any]"

git push

# Monitor GitHub CI
gh pr checks <pr-number> --watch

# Monitor Forgejo CI (dual-remote projects)
  SHA=$(git rev-parse HEAD)
  TOKEN=$(cat ~/.config/forgejo/token)
  sleep 60
  for i in 1 2 3; do
    RESULT=$(curl -s \
      -H "Authorization: token $TOKEN")
    STATE=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['state'])" 2>/dev/null)
    echo "Forgejo CI: $STATE (attempt $i)"
    [ "$STATE" = "pending" ] && sleep 30 || break
  done
  echo "$RESULT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Forgejo CI: {d[\"state\"]} ({d[\"total_count\"]} checks)')
for s in (d.get('statuses') or []):
    print(f'  {s[\"context\"]}: {s[\"status\"]}')
"
  # If Forgejo CI failed, loop back to Phase 3
  [ "$STATE" = "failure" ] && echo "FORGEJO CI FAILED — return to Phase 3 fix loop"
fi

# Re-check bot reviews after pushing fixes
gh api repos/$REPO/pulls/<pr-number>/comments \
  --jq '.[] | "[\(.path):\(.line // .original_line // "?")]\n\(.body)\n---"'
```

## Phase 6: Handoff

**If `REVIEW_REQUIRED` (no human reviews on this PR):**

```
PR has no reviews yet. Consider getting a second opinion before requesting merge:

  /review pr <N>   — external AI review (MERGE/BLOCK verdict, ~5 min)

Then run the merge orchestrator:

  /pr-merge <N>
```

**If all checks passing and reviews satisfied:**

```
All issues resolved. Run the merge orchestrator:

  /pr-merge <N>
```

`/pr-merge` owns the merge decision, branch cleanup, milestone check, and release readiness. Do not auto-merge here.

## Tips

- Fix one category at a time (CI, then lint, then security)
- Verify fixes locally before running pre-flight
- `/pre-commit` is mandatory — it prevents the push→CI-fail→fix→repeat cycle
- Use `gh pr checks --watch` to monitor CI progress after push
