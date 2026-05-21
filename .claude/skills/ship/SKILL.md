---
name: ship
description: "Final-mile orchestrator - commit + push + PR creation. Run after /pre-commit passes. Chains: commit -> push -> /pr-creator (artifact check + PR). Use --issue N to auto-close a GitHub issue on merge. Use --main to ship directly to main with no PR (closes issue + deletes branch)."
---

# Ship Skill

## Purpose

Zero-ceremony last mile: takes validated code (post `/pre-commit`) and ships it as a pull request in one shot.

**Chain:** commit → push → `/pr-creator` (artifact verification + PR creation)

Does NOT run quality checks or tests — that's `/pre-commit`'s job.

## Usage

```bash
/ship "feat: add search feature"               # commit message provided
/ship --issue 42 "feat: add search feature"    # links issue — PR body gets "Closes #42"
/ship --issue 42                               # derive commit message from diff + branch name
/ship --issue 42 --main                        # direct-to-main: no PR, close issue, delete branch
```

`--main` is the "no review needed" fast-path: commit → push to main → close issue → delete branch.
Only use when the change is tiny, fully validated, and genuinely needs no review.

## Workflow

### 1. Pre-Ship Sanity Check

```bash
git status
git diff --stat
```

- If working tree is already clean (nothing to commit): skip to Step 3 (push).
- If `/pre-commit` hasn't been mentioned this session, warn:

  > "⚠ Did you run `/pre-commit`? `/ship` assumes all checks passed. Proceed? [y/N]"

### 2. Commit

Derive commit type from changes if not explicit in message:

| Change type       | Prefix      |
| ----------------- | ----------- |
| New functionality | `feat:`     |
| Bug fix           | `fix:`      |
| Docs only         | `docs:`     |
| Refactor          | `refactor:` |
| Chore / tooling   | `chore:`    |

If message not provided, generate from `git diff --staged --stat` + branch name.

```bash
git add -u   # stage tracked changes (not untracked)
git commit -m "$(cat <<'EOF'
<type>: <description>

Closes #<N>
EOF
)"
```

Omit `Closes #N` line if no `--issue` flag.

### 3. Push

```bash
git push -u origin HEAD
```

If push fails (upstream diverged):

```bash
git pull --rebase origin <base-branch>
git push -u origin HEAD
```



```bash
SHA=$(git rev-parse HEAD)
TOKEN=$(cat ~/.config/forgejo/token)

# Wait for CI to start, then poll (max 3 attempts)
sleep 60
for i in 1 2 3; do
  RESULT=$(curl -s \
    -H "Authorization: token $TOKEN")
  STATE=$(echo "$RESULT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['state'])" 2>/dev/null)
  [ "$STATE" = "pending" ] && sleep 30 || break
done

# Print per-job breakdown
echo "$RESULT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
for s in (d.get('statuses') or []):
    print(f'  {s[\"context\"]}: {s[\"status\"]}')
"
```

If `state` is `failure`: warn user. Do NOT block PR creation — `/pr-merge` is the hard gate.
If `state` is `pending` after 3 retries: report current state and continue.

### 4a. PR Creation (delegated to /pr-creator) — default path

Hand off to `/pr-creator` starting at **Step 1.5** (artifact verification). Skip Step 1 entirely — `/pre-commit` already covered it.

Pass `--issue N` through: `/pr-creator` injects `Closes #N` in the PR body and selects the right template.

### 4b. Direct-to-main (`--main` flag) — no PR path

**Trigger:** `--main` flag is present. Requires `--issue N` (closing an issue is mandatory to justify skipping review).

**Guard:** Confirm current branch is NOT already `main`. If already on `main`, skip the branch steps below.

```bash
CURRENT_BRANCH=$(git branch --show-current)

# If on a feature branch, merge/push logic differs:
if [ "$CURRENT_BRANCH" != "main" ]; then
  # Push current branch, then fast-forward main
  git push -u origin HEAD
  git checkout main
  git pull origin main
  git merge --ff-only "$CURRENT_BRANCH"
  git push origin main
else
  # Already on main — just push
  git push origin main
fi
```

If `--ff-only` fails (non-linear history), abort and tell the user to rebase first.

**Close the issue:**

```bash
gh issue close <N> --comment "Shipped directly to main in $(git rev-parse --short HEAD)."
```

**Delete the branch (only if we were NOT on main):**

```bash
if [ "$CURRENT_BRANCH" != "main" ]; then
  git branch -d "$CURRENT_BRANCH"
  git push origin --delete "$CURRENT_BRANCH" 2>/dev/null || true
fi
```

Silently ignore remote-delete errors (branch may not exist on remote or dual-remote may already be gone).

## When NOT to Use /ship

- Change hasn't been validated → run `/pre-commit` first, then `/ship`
- Multiple commits need squashing → squash manually before shipping
- PR already exists → `gh pr edit` + `git push`
- No PR needed (direct to main) → use `/ship --issue N --main`

## Gotchas

- Forgejo push-to-create is DISABLED — the repo must already exist (created via API or web UI) before the first push, or the push fails.
- `--main` requires `--issue N` and `--ff-only`; if history is non-linear the fast-forward merge aborts — rebase first, do not force.

## Related Skills

- `/pre-commit` — run before `/ship` (quality + tests + security + changelog)
- `/pr-creator` — PR creation engine, called by `/ship` at Step 1.5
- `/pr-merge` — after PR is reviewed and ready to merge
- `/fix --pr` — minimal path for small fixes (bypass `/ship` for tiny changes)
