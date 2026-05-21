---
name: pr-merge
description: Safely merge GitHub pull requests using comprehensive pre-merge validation. Use this skill when the user asks to merge a PR, complete a PR workflow, or check if a PR is ready to merge. Validates CI/CD status, reviews, and conflicts before merging with the appropriate strategy.
---

# PR Merge

## Overview

This skill enables safe and comprehensive pull request merging workflows using the `gh` CLI. It automates the complete pre-merge validation process, checks CI/CD status, verifies reviews, and executes merges with the appropriate merge strategy.

## When to Use This Skill

Use this skill when the user requests:

- "Merge PR #123"
- "Can we merge this pull request?"
- "Check if PR is ready to merge"
- "Complete the PR workflow"
- "Merge this feature branch"
- "Is PR #456 ready to be merged?"

## Argument Handling

The skill accepts an optional PR number as argument:

- `/pr-merge 123` — operate on PR #123
- `/pr-merge` — detect PR from current branch

When no PR number is given, detect the current branch's PR:

```bash
gh pr view --json number --jq '.number'
```

If no PR is associated with the current branch, ask the user for the PR number.

## Pre-Merge Validation Workflow

Before merging any PR, execute the complete validation workflow to ensure safety and quality.

### Step 1: Fetch PR Details

```bash
gh pr view <number> --json title,body,state,isDraft,baseRefName,headRefName,author,number,mergeable,additions,deletions,changedFiles,reviewDecision
```

Verify:

- `state` is `OPEN`
- `isDraft` is `false`
- `mergeable` is `MERGEABLE`

**Block merge if** the PR is draft, closed, or has merge conflicts.

### Step 2: Check CI/CD Status

```bash
gh pr checks <number>
```

Or for structured output:

```bash
gh pr checks <number> --json name,state,bucket --jq '.[] | select(.bucket != "pass")'
```

**Block merge if:**

- Any required checks are failing
- Checks are still pending (inform user to wait)

### Step 2b: Check Forgejo CI (dual-remote projects)


```bash
SHA=$(gh pr view <number> --json headRefOid --jq '.headRefOid')
  -H "Authorization: token $TOKEN" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
state=d['state']
print(f'Forgejo CI: {state} ({d[\"total_count\"]} checks)')
for s in (d.get('statuses') or []):
    print(f'  {s[\"context\"]}: {s[\"status\"]}')
if state == 'failure':
    sys.exit(1)
"
```

**Block merge if** Forgejo CI is `failure` — report failing jobs and suggest `/pr-fix`.
If `pending`: warn user, suggest waiting. Do not proceed without explicit user override.

### Step 3: Verify Reviews

```bash
gh api repos/{owner}/{repo}/pulls/{number}/reviews --jq '[.[] | {user: .user.login, state: .state}]'
```

Or check `reviewDecision` from Step 1 JSON output — values are `APPROVED`, `CHANGES_REQUESTED`, `REVIEW_REQUIRED`, or empty.

**Block merge if:**

- `reviewDecision` is `CHANGES_REQUESTED` or `REVIEW_REQUIRED`
- Any reviewer has requested changes

### Step 4: Review Changed Files

Get a summary of changed files and stats:

```bash
# File names and per-file stats (works for any PR size)
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate \
  --jq '.[] | "\(.status)\t+\(.additions) -\(.deletions)\t\(.filename)"'
```

**IMPORTANT:** Do NOT use `gh pr diff --stat` — that flag does not exist. The valid flags for `gh pr diff` are `--color`, `--name-only`, `--patch`, and `--web` only.

For small PRs, you can also use:

```bash
gh pr diff <number> --name-only
```

Note: `gh pr diff` and `--name-only` will fail with HTTP 406 if the diff exceeds 20,000 lines. Always fall back to the API endpoint above for large PRs.

## Merge Execution

Once all validations pass, execute the merge using `gh pr merge`.

### Selecting Merge Method

Choose the appropriate merge method based on project conventions and commit history:

**Squash Merge (`-s`):**

- Use for: Feature branches with messy commit history
- Benefits: Clean, single commit in main branch
- When: Multiple small commits, WIP commits, or iterative development

**Merge Commit (`-m`):**

- Use for: Preserving complete commit history
- Benefits: Full audit trail, maintains original commits
- When: Well-structured commits with meaningful messages

**Rebase Merge (`-r`):**

- Use for: Linear history without merge commits
- Benefits: Clean, linear git history
- When: Small PRs with few commits

**Default recommendation:** Use `-s` (squash) unless project conventions dictate otherwise.

### Merge Command

```bash
# Squash merge (default recommendation)
gh pr merge <number> -s -t "feat: description of change" -b "Details here" -d

# Merge commit
gh pr merge <number> -m -d

# Rebase merge
gh pr merge <number> -r -d
```

**Flags reference:**

- `-s` / `--squash` — squash and merge
- `-m` / `--merge` — create merge commit
- `-r` / `--rebase` — rebase and merge
- `-t` / `--subject` — commit title (squash/merge)
- `-b` / `--body` — commit body text
- `-d` / `--delete-branch` — delete branch after merge
- `--auto` — enable auto-merge when requirements aren't yet met

**Always ask user for confirmation before executing `gh pr merge`.**

## Post-Merge Workflow

After successful merge, execute this sequence:

### Step 1: Confirm & Clean Up

```bash
# Confirm merge
gh pr view <number> --json state,mergedAt --jq '"Merged at: \(.mergedAt)"'
```

**Immediately after confirming merge, switch local checkout to the base branch:**

```bash
MERGE_TARGET=$(gh pr view <number> --json baseRefName --jq '.baseRefName')
MERGE_TARGET="${MERGE_TARGET:-main}"
MERGED_BRANCH=$(gh pr view <number> --json headRefName --jq '.headRefName')

# Switch to base branch and pull latest
git checkout "$MERGE_TARGET" && git pull

# Delete local copy of the merged branch if it exists
if git show-ref --verify --quiet "refs/heads/$MERGED_BRANCH"; then
  git branch -d "$MERGED_BRANCH" && echo "Deleted local branch: $MERGED_BRANCH"
fi
```

Do NOT ask for confirmation before deleting the just-merged branch — it was already merged and the user approved the merge. For all other branches, always confirm before deleting.

### Step 1b: Sync Forgejo (dual-remote projects)


```bash
# Check if Forgejo is a push remote

# If yes, extract repo path from remote URL (NOT basename — local dir name may differ)

# Sync to Forgejo
```

Skip if no Forgejo push remote is configured.

### Step 1c: Verify Forgejo CI (post-merge)

After syncing, wait for CI to start then check the result:

```bash
TOKEN=$(cat ~/.config/forgejo/token)
SHA=$(git rev-parse HEAD)

sleep 60
for i in 1 2; do
  RESULT=$(curl -s \
    -H "Authorization: token $TOKEN")
  STATE=$(echo "$RESULT" | python3 -c "import json,sys; print(json.load(sys.stdin)['state'])" 2>/dev/null)
  echo "Post-merge Forgejo CI: $STATE (attempt $i)"
  [ "$STATE" = "pending" ] && sleep 30 || break
done

echo "$RESULT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Post-merge Forgejo CI: {d[\"state\"]} ({d[\"total_count\"]} checks)')
for s in (d.get('statuses') or []):
    print(f'  {s[\"context\"]}: {s[\"status\"]}')
"
```

If `failure`: flag for immediate attention (post-merge, cannot block — document as known issue and check `/ops` if this is a production deploy path).

### Step 2: Analyze Open Branches

```bash
# Fetch and prune stale remote tracking refs
git fetch --prune origin

MERGE_TARGET=$(gh pr view <number> --json baseRefName --jq '.baseRefName')
MERGE_TARGET="${MERGE_TARGET:-main}"

# Remote branches already merged into the target
MERGED_REMOTE=$(git branch -r --merged "origin/$MERGE_TARGET" | grep -v 'HEAD\|main\|release/' | sed 's|origin/||')

# Local branches with no corresponding remote (orphaned — remote was deleted)
ORPHANED_LOCAL=$(git branch | sed 's/^[* ]*//' | while read b; do
  git show-ref --verify --quiet "refs/remotes/origin/$b" || echo "$b"
done | grep -v "^$MERGE_TARGET$\|^main$")

# Stale branches (no commits in 30+ days) — check both remote and local
THIRTY_DAYS_AGO=$(date -v-30d +%s 2>/dev/null || date -d '30 days ago' +%s)
for branch in $(git branch -r | grep -v 'HEAD\|main\|release/' | sed 's|  origin/||'); do
  LAST_EPOCH=$(git log -1 --format='%ct' "origin/$branch" 2>/dev/null)
  LAST_DATE=$(git log -1 --format='%ci' "origin/$branch" 2>/dev/null)
  if [[ -n "$LAST_EPOCH" && "$LAST_EPOCH" -lt "$THIRTY_DAYS_AGO" ]]; then
    DAYS_OLD=$(( ($(date +%s) - LAST_EPOCH) / 86400 ))
    echo "$branch: STALE ($DAYS_OLD days) — last commit $LAST_DATE"
  else
    echo "$branch: active — last commit $LAST_DATE"
  fi
done
```

Report in structured format:

```
POST-MERGE BRANCH ANALYSIS
===========================
Current branch:           v0.14.0-campaigns (switched automatically)
Just merged (deleted):    feature/424-... (local + remote)
Orphaned local:           feature/old-thing (remote gone, local remains)
Remote merged:            feature/another (merged into base, safe to delete)
Stale (30+ days):         feature/abandoned (45 days)
Active:                   feature/in-progress (2 days)
Release branches:         release/v0.3.1 (3 open issues)
```

Suggest cleanup for orphaned local, remote-merged, and stale branches. Always confirm before deleting anything other than the just-merged branch.

### Step 3: Tagging & Release (conditional)

Evaluate whether a tag/release is appropriate:

**Tag if:**

- Merging a `release/*` branch into `main`
- User explicitly requests it
- CHANGELOG has a version section ready (not just [Unreleased])

**Propose tag:**

```bash
# Get proposed version from CHANGELOG
head -20 CHANGELOG.md
echo "Create tag? git tag vX.Y.Z && git push --tags"
```

**Create GitHub release:**

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z" \
  --notes "$(sed -n '/## \[X.Y.Z\]/,/## \[/p' CHANGELOG.md | head -n -1)" \
  --target main
```

### Step 4: Milestone Check

If the merged PR was part of a version milestone:

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
MILESTONE="vX.Y.Z"

# Check remaining issues in milestone
gh api "repos/$REPO/milestones" \
  --jq ".[] | select(.title==\"$MILESTONE\") | \"Open: \(.open_issues), Closed: \(.closed_issues), ID: \(.number)\""
```

- If 0 open issues remain: propose closing the milestone

  ```bash
  gh api "repos/$REPO/milestones/<id>" --method PATCH -f state=closed
  ```

- If issues remain: report which are still open

### Step 5: Documentation Sync

Inspect what the merged PR changed to determine which docs need updating.

**Detect changed files:**

```bash
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate \
  --jq '.[].filename'
```

**Decision tree:**

**A. New or changed skill detected** (any file under `skills/*/` or `commands/*.md`):

- Open `CLAUDE.md` and locate the relevant pipeline section (e.g., "Review Workflow", "Media Pipeline")
- Propose a targeted addition or update — confirm with user before editing
- If the skill has a new invocation trigger or subcommand, update the corresponding CLAUDE.md entry

**B. Skill arguments or workflow steps changed** (`SKILL.md` content changed but no new skill):

- Propose the specific CLAUDE.md diff for the affected entry, confirm before editing
- If no root `README.md` exists: note it as absent, do not create automatically

**C. No skills touched:**

- Skip this step. Do not prompt for unnecessary doc edits.

**CHANGELOG promotion** (evaluate independently of A/B/C above):

```bash
head -30 CHANGELOG.md 2>/dev/null || echo "No CHANGELOG"
```

- `[Unreleased]` section is non-empty **AND** merging a `release/*` branch →
  prompt user to run `/release changelog` to promote `[Unreleased]` → tagged version.
  `/release changelog` Step 6 will also propagate the version bump to `pyproject.toml`,
  `package.json`, `Cargo.toml`, and README badges, then propose a
  `chore: bump version to X.Y.Z` commit. **That commit must land on main before the git tag
  is created** — tag an unversioned state and the release artifacts will be wrong.
  Only after the bump commit is in, verify before tagging:
  ```bash
  git log --oneline main -3           # confirm bump commit is at HEAD
  grep '^version' pyproject.toml 2>/dev/null || grep '"version"' package.json 2>/dev/null || grep '^version' setup.cfg 2>/dev/null || grep '^version' Cargo.toml 2>/dev/null
  ```
  Then: `git tag vX.Y.Z && git push --tags`
- Feature branch merge → skip (promotion happens at release cut, not feature merge time)
- No `CHANGELOG.md` in repo → note it, suggest creating one, do not block the workflow

**Policy violation check** (see `rules/claude-md-branching.md`):

> If the merged PR came from a `feature/*` or `fix/*` branch and it modified
> `CLAUDE.md` or root `README.md`, flag this as a branching policy violation.
> Propose opening a new PR against main with a targeted revert of the CLAUDE.md/README change,
> and a follow-up note to apply it properly on the next release branch.
> Do not commit directly to main — always go through a PR to respect branch protection.

### Step 5b: Docsite Sync (conditional)

Evaluate whether user-facing or internal docs need updating based on what the PR changed.

**Skip this step entirely if ANY of the following is true:**

- No `docs-registry.yaml` exists anywhere in the repo (project has no docs pipeline)
- The PR touched only non-code files (markdown, YAML, config, skills, hooks)
- The PR merged a `docs/*` branch (already docs work)

**Trigger check:**

```bash
# Check docs-registry.yaml exists
find . -name "docs-registry.yaml" -not -path "*/.git/*" | head -1

# Get code files changed by the PR
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate \
  --jq '[.[] | .filename | select(test("^(backend|app|src|frontend)/"))] | length'
```

If registry exists AND code file count > 0, proceed. Otherwise skip silently.

**Steps:**

1. Run `/docs audit` — read-only staleness + registry delta check
2. Cross-reference PR changed files against registry entries:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/files --paginate \
     --jq '[.[] | .filename]'
   ```
   Match changed paths to `file:` entries in `docs-registry.yaml`.
3. Check CHANGELOG for new `### Added` entries since last tag (signals new features):
   ```bash
   sed -n '/## \[Unreleased\]/,/## \[/p' CHANGELOG.md | grep '^- ' | head -10
   ```

**Output format:**

```
## Docsite Check
Mode: internal | Registry: 8 pages (5 published, 2 draft, 1 stale)
PR touched: backend/app/api/campaigns.py (+2 routes)
Affected registered docs: features/campaigns.md (published)

Suggestions:
→ /docs update features/campaigns.md   (stale: code newer than docs)
→ /docs create feature-guide           (new feature in [Unreleased]: "Campaign scheduling")
```

**If nothing is affected:**

```
## Docsite Check
No registered doc pages map to files changed in this PR. Skipping.
```

**Rules:**

- Never auto-execute `/docs update` or `/docs create` — always propose only
- Never block the merge workflow — this is advisory
- If `/docs audit` is slow, fall back to registry staleness check only

### Step 6: Release Readiness & Next Steps

After every merge, analyze the current release state and output guided next steps.

**Gather state:**

```bash
LAST_TAG=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null)
UNRELEASED=$(git log --no-merges --oneline "${LAST_TAG:-$(git rev-list --max-parents=0 HEAD)}..HEAD" | wc -l)
MILESTONE=$(cat .claude/current-milestone 2>/dev/null)
RELEASE_TAG_AT_HEAD=$(git tag --points-at HEAD | grep '^v' | head -1)

# Milestone progress (if milestone set)
if [[ -n "$MILESTONE" ]]; then
  REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)
  gh api "repos/$REPO/milestones" \
    --jq ".[] | select(.title==\"$MILESTONE\") | \"Open: \(.open_issues), Closed: \(.closed_issues)\"" 2>/dev/null
fi

# Check [Unreleased] section
grep -c '^\- ' <(sed -n '/## \[Unreleased\]/,/## \[/p' CHANGELOG.md 2>/dev/null) 2>/dev/null || echo "0"

# Migration heads (if Alembic project)
if [[ -f alembic.ini ]]; then
  HEADS=$(alembic heads 2>/dev/null | wc -l)
fi
```

**Routing table** (first match wins, top = highest priority):

| Priority | State                                 | Guidance                                                                          |
| -------- | ------------------------------------- | --------------------------------------------------------------------------------- |
| 1        | Multiple alembic heads detected       | "Run `alembic merge heads` before next release"                                   |
| 2        | Just tagged (HEAD has v\* tag)        | "Post-release: `/release verify tags`, close milestone, `/release plan` for next" |
| 3        | Milestone complete (0 open issues)    | "Run `/release verify commits` → `/release changelog` → tag"                      |
| 4        | Milestone in progress                 | "Next: pick issue #N, run `/implementation`"                                      |
| 5        | No milestone, >10 unreleased commits  | "Consider `/release plan` to scope a version"                                     |
| 6        | No milestone, 1-10 unreleased commits | "Continue working or `/release verify commits` when ready"                        |

**Output format** (appended to existing post-merge output):

```
## Release Status
- Last tag: v1.2.0 (15 commits since)
- Milestone: SPRINT-1 (3/5 closed, 2 remaining)
- Migration heads: 1 (clean)
- [Unreleased]: 8 entries

→ Next: pick issue #26, run /implementation
```

---

## Safety Guidelines

Always follow these safety rules:

1. **Never force merge** — All checks must pass (never use `--admin`)
2. **Never bypass reviews** — Required approvals must exist
3. **Never merge with conflicts** — Conflicts must be resolved first
4. **Never merge draft PRs** — Must be marked as ready for review
5. **Always confirm with user** — Ask before executing the merge

## Validation Failure Responses

When pre-merge validation fails, provide clear, actionable feedback:

**CI/CD Failures:**

- List which checks are failing
- Suggest viewing logs: `gh run view <run-id> --log-failed`
- **Suggest:** "Run `/pr-fix <number>` to triage and fix CI failures, review issues, and bot comments"
- Recommend reviewing workflow files

**Review Issues:**

- List missing required reviews
- Identify reviewers who requested changes
- **Suggest:** "Run `/review pr --pr <number>` for companion-dispatched PR review"
- Suggest addressing review comments first

**Architectural Concerns:**

- If review comments raise design questions
- **Suggest:** "Run `/review solve "concern description"` for a second opinion"

**Merge Conflicts:**

- Report `mergeable` status from PR details
- Recommend updating branch: `gh api -X PUT repos/{owner}/{repo}/pulls/{number}/update-branch`
- Suggest resolving conflicts locally if needed

**Branch Protection:**

- List unmet protection rules
- Explain which requirements are blocking
- Suggest how to satisfy requirements

## Advanced Features

### Update Branch Before Merge

If the base branch has advanced:

```bash
gh api -X PUT repos/{owner}/{repo}/pulls/{number}/update-branch
```

### Enable Auto-Merge

If checks are still pending but everything else is ready:

```bash
gh pr merge <number> -s --auto
```

### Check Multiple PRs

```bash
gh pr list --json number,title,reviewDecision,statusCheckRollup --jq '.[] | select(.reviewDecision == "APPROVED")'
```

## Complete Workflow Example

**User request:** "Merge PR #42"

**Execution sequence:**

1. `gh pr view 42 --json ...` → Confirm open, not draft, mergeable
2. `gh pr checks 42` → All checks passing
3. Check `reviewDecision` → APPROVED
4. `gh api .../pulls/42/files --paginate` → Review changed files
5. Ask user to confirm merge method → squash
6. `gh pr merge 42 -s -d` → Execute merge
7. Confirm success → "PR #42 merged via squash into main"

## Error Handling

Handle common errors gracefully:

- **exit code 1 + "not found":** PR doesn't exist, verify PR number
- **"already been merged":** PR already merged
- **"not mergeable":** Merge conflict exists, need resolution
- **"required status check":** Branch protection rules not met
- **HTTP 406 on diff:** Diff too large (>20k lines), use API files endpoint instead

## gh CLI Quick Reference

```
gh pr view <n> --json <fields>     # Fetch PR metadata
gh pr checks <n>                    # CI/CD status
gh pr diff <n> --name-only          # Changed filenames (small PRs only)
gh pr merge <n> -s|-m|-r            # Merge with strategy
gh pr merge <n> --auto              # Auto-merge when ready
gh api repos/O/R/pulls/N/files      # Per-file diff stats (any size)
gh api repos/O/R/pulls/N/reviews    # Review details
gh run view <id> --log-failed       # Failed CI logs
```

**Invalid flags to avoid:**

- `gh pr diff --stat` — does NOT exist
- `gh pr view --stat` — does NOT exist

## Gotchas

- `gh pr diff --stat` does NOT exist — use `gh api repos/{O}/{R}/pulls/{N}/files --paginate` for file stats instead
- `gh pr diff` and `--name-only` return HTTP 406 if the diff exceeds 20,000 lines — always fall back to the API files endpoint for large PRs
- Forgejo remote path must be extracted from `git remote -v`, NOT from `basename` of the local directory — local dir names often differ from the repo path
- `--ff-only` merge in `--main` mode fails on non-linear history — user must rebase first; never force-merge
- `reviewDecision: REVIEW_REQUIRED` means no review has been submitted yet (distinct from `CHANGES_REQUESTED`) — both block merge
- Branch analysis after merge: `git fetch --prune` is required before checking merged/stale branches or remote-gone branches won't appear correctly
