---
name: progress
description: On-demand situational awareness — fresh git/PR snapshot plus continuation, distilled into one concrete "next action" suggestion. Use mid-session when you've lost track, after a compaction, or starting a new work block. Trigger on "where was I", "what's next", "progress", "what should I do now", "/progress".
---

# Progress Skill

## Purpose

Fills the routing gap that SessionStart leaves open. SessionStart injects data; `/progress` interprets it and tells you what to do next.

Use mid-session when you've lost track, after a context compaction, or at the start of a new work block.

**What it does NOT do:** Re-fetch GitHub issues, CHANGELOG, or codebase map — those are already in session context from SessionStart. Running `/progress` will not flood your context window.

## Usage

```
/progress              # current repo only (default)
/progress --all        # cross-repo: show recent work from all projects
/progress --no-memory  # skip memory recall entirely (fastest, git-only)
```

No subcommands at v1. One command, one compact output.

## Workflow

### Step 0 — Memory context (skip if `--no-memory`)

Run the memory recall command with a hard 10-second timeout. If the command fails, times out, or returns empty or invalid JSON (`[]`, whitespace, non-JSON output), silently skip this step and proceed to Step 1 — this enrichment must never block the rest of `/progress`.

**Default (`/progress`):** scope to current repo only via `--project`.
**With `--all`:** query all repos (omit `--project`, use `--deep --since`).

```bash
# Detect current repo name (same logic as memory injection hook)
CURRENT_REPO=$(git remote get-url origin 2>/dev/null | sed 's/.*\///' | sed 's/\.git$//')
# Fallback: directory name
CURRENT_REPO=${CURRENT_REPO:-$(basename "$PWD")}

# Compute ISO date for 3 days ago (macOS: date -v-3d, Linux: date -d '3 days ago')
SINCE_DATE=$(date -v-3d +%Y-%m-%d 2>/dev/null || date -d '3 days ago' +%Y-%m-%d 2>/dev/null || echo "")

# Default: scope to current repo
# With --all: cross-repo (drop --project, add --deep --since)
if [[ "$FLAGS" == *"--all"* ]]; then
  RECALL_FLAGS="--deep ${SINCE_DATE:+--since "$SINCE_DATE"}"
else
  RECALL_FLAGS="--project "$CURRENT_REPO""
fi

timeout 10 uv run --project ~/.claude/skills/memory/recall \
  python ~/.claude/skills/memory/recall/scripts/memory_recall.py \
  "recent work" $RECALL_FLAGS --compact --limit 5 2>/dev/null
```

Parse the JSONL output (one JSON object per line). Each line has: `project`, `branch`, `date`, `summary`. Compact mode pre-filters short/empty summaries, so results are already clean.

**Filter out empty results** — discard any entry where `summary` is empty or where `project` is an empty string.

**Group by project** — keep only the most recent session per project (highest `date`). Cap at 3 entries total.

**Extract issue references** from each `summary` — look for bare `#N` and `owner/repo#N` patterns.

**Cross-reference** extracted issues. For each session with a non-empty `branch`, the branch name often encodes the project context. For the repo identity, run `git remote get-url origin` in the current directory and parse `owner/repo` from the URL. Bare `#N` references belong to that repo.

For each unique `owner/repo` identified (at most 3 across all sessions), fetch open issues:

```bash
gh issue view N -R owner/repo --json number,title,state,labels \
  --jq 'select(.state=="OPEN") | {number,title,labels}' 2>/dev/null
```

Use `labels` to extract priority. Priority inference: look for a label matching `P0`, `P1`, `P2`, `P3` (case-insensitive). If the title starts with `[P0]`/`[P1]`/`[P2]`/`[P3]` (following the project's naming convention), extract it from there. If no priority signal found, treat as P3.

Store these results — they feed the "Where you left off" section and the routing engine in Step 4.

### Step 1 — Fresh git snapshot

Run these commands to get current (not session-start) state:

```bash
git status --short
git log --oneline -3
git branch --show-current

# Release awareness
LAST_TAG=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null)
UNRELEASED_COUNT=$(git log --no-merges --oneline "${LAST_TAG:-$(git rev-list --max-parents=0 HEAD)}..HEAD" 2>/dev/null | wc -l)
RELEASE_TAG_AT_HEAD=$(git tag --points-at HEAD | grep '^v' | head -1)
```

### Step 2 — PR check

```bash
gh pr list --state open --json number,title,headRefName 2>/dev/null || echo "Not a GitHub repo or gh not configured"
```

### Step 3 — Continuation check

Read `.claude/memory/local/continuation.md` if it exists. Extract the first meaningful line (skip blank lines and the auto-header). This is fresher than what was auto-loaded at session start.

### Step 4 — Routing engine

Analyze the collected state and output the **Situation Report** (see format below) followed by one `→ Next Action` recommendation.

Apply these rules in priority order:

| State                                                         | Suggestion                                                            |
| ------------------------------------------------------------- | --------------------------------------------------------------------- |
| Staged files in git                                           | `/pre-commit` — staged changes ready for validation                   |
| Unstaged changes on `feature/*` or `fix/*`                    | `/review changes` — review before staging                             |
| On `feature/*`/`fix/*` with commits, no open PR               | `/pr-creator` — branch has unreleased work                            |
| Open PR exists                                                | `/review pr --pr N` then `/pr-merge` when ready                       |
| Continuation mentions specific in-progress task               | Resume that task (name it explicitly)                                 |
| Memory (Step 0) surfaces P0/P1 open issue from recent session | `/implementation --issue N` — resume highest-priority cross-repo work |
| HEAD tagged `v*` (just released)                              | Post-release: `/release verify tags`, close milestone, plan next      |
| On `main`, clean, >10 unreleased commits                      | Release candidate — run `/release plan` to scope a version            |
| On `main` with uncommitted changes                            | Unusual state — clarify before proceeding                             |
| Clean state, no continuation, no open PRs                     | `/story plan` or `/release plan` — what's next on the backlog?        |

If multiple rules match, apply the highest-priority one only.

## Output Format

Keep the total output under 25 lines.

```
## Situation
- Branch: <branch-name> (<N commits ahead of main> | clean)
- Working tree: <staged/unstaged summary, or "clean">
- Release: <last-tag> + <N> unreleased commits
- Open PRs: <"None" or "#N title">

## Last Session
<one-line summary from continuation.md, or "No continuation found">

### Where you left off (last 3 days)
- <project> (<YYYY-MM-DD>): <one-line summary of what was happening>
  → Open issue: <repo>#<N> — <title>
- <project> (<YYYY-MM-DD>): <one-line summary>
  → No open issues referenced

Suggested next: <repo>#<N> (<priority>, last touched N days ago)

## → Next Action
/<skill> — <one-sentence rationale>
```

**"Where you left off" rules:**

- Show at most 3 project entries, most recent first by `started_at`.
- Omit the entire section (including the header) if Step 0 produced no results.
- Each entry is exactly 2 lines: summary line + issue status line.
- Truncate the one-line summary to ~100 characters if needed.
- "Suggested next" picks the highest-priority open issue across all entries. Priority order: P0 > P1 > P2 > P3. Ties broken by recency (most recently active project wins). Omit if no open issues were found.

## Related Skills

- `/memory recall` — underlying retrieval engine powering Step 0
- `/pre-commit` — full validation before commit
- `/review changes` — companion review of uncommitted changes
- `/pr-creator` — create PR from current branch
- `/pr-merge` — merge an open PR
- `/story plan` — plan next sprint from backlog
- `/release plan` — scope next version release
