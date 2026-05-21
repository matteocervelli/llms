# Release Plan

## Purpose

Analyze the current project state (milestones, issues, tags, branches) and propose a structured version release plan. Creates milestone + release branch when approved.

## When to Use

- Starting work on a new version
- Organizing backlog into a release
- User asks "what should we ship next?"
- Before `/implementation` when no release branch exists

## Workflow

### Step 1: Discover Current State

```bash
# Detect repo context
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')

# List open milestones with issue counts
gh api "repos/$REPO/milestones" --jq '.[] | select(.state=="open") | "\(.title): \(.open_issues) open, \(.closed_issues) closed — due: \(.due_on // "no deadline")"'

# Count orphaned issues (no milestone)
gh api "repos/$REPO/issues?state=open&per_page=100" --jq '[.[] | select(.milestone == null and .pull_request == null)] | length'

# List orphaned issues with labels
gh api "repos/$REPO/issues?state=open&per_page=100" --jq '.[] | select(.milestone == null and .pull_request == null) | "#\(.number) [\(.labels | map(.name) | join(", "))] \(.title)"'

# Count unreviewed agent signals (ai-suggested label, any milestone)
gh issue list -R "$REPO" --label ai-suggested --state open --json number --jq 'length'

# Check for open release branches
git fetch origin
git branch -r --list 'origin/release/*' | sed 's|origin/||'

# Last 5 tags
git tag --sort=-v:refname | head -5

# Current CHANGELOG state
head -30 CHANGELOG.md 2>/dev/null || echo "No CHANGELOG.md found"

# Check for release.yml workflow (auto-release on tag push)
RELEASE_YML=$([ -f ".forgejo/workflows/release.yml" ] && echo "present" || echo "absent")
echo "release.yml: $RELEASE_YML"

# Check for staging.yml (enforces release-branch flow when present)
HAS_STAGING=$([ -f ".forgejo/workflows/staging.yml" ] && echo "present" || echo "absent")
echo "staging.yml: $HAS_STAGING"
```

### Step 2: Propose Version Scope

Based on discovered state, present one of these scenarios:

**If milestones exist with issues:**

```
VERSION PLANNING — {repo}
==========================
Last release:     v0.3.0 (2026-02-15)
Open milestones:  v0.3.1 (5 open, 2 closed), v0.4.0 (3 open)
Orphaned issues:  7 (not in any milestone)
Agent signals:    3 unreviewed (ai-suggested) ⚠
Release branches: release/v0.3.1

Recommendation: [based on analysis]
```

If agent signals count > 0, prominently note:

```
⚠ Unreviewed signals: N ai-suggested issues need triage before finalizing scope
  → Run `/health agents triage` to review, or include/exclude explicitly
```

Ask user which milestone to target.

**If orphaned issues exist but no milestones:**

Group issues by conventional commit type:

- `bug` label → fix → PATCH
- `enhancement` label → feat → MINOR
- Breaking changes → MAJOR

Propose a version number and ask user to confirm scope.

**If no structure at all:**

Propose initial version (v0.1.0 or based on existing tags) and offer to create milestone + organize issues.

### Step 3: Companion Review (optional)

After assembling the version scope, suggest:

> "Want a second opinion on this release scope? Run `/review solve "release plan for vX.Y.Z with issues #N, #M, #K"` to get Codex/Gemini analysis of prioritization and risk."

### Step 4: Create/Update Milestone

With user confirmation:

```bash
# Create milestone
gh api "repos/$REPO/milestones" --method POST \
  -f title="vX.Y.Z" \
  -f description="[scope description from step 2]" \
  -f due_on="YYYY-MM-DDT23:59:59Z"

# Assign issues to milestone
gh issue edit <number> --milestone "vX.Y.Z"
```

If milestone already exists, just assign missing issues.

### Step 4b: Forgejo Release Auth Check

No secret configuration needed. Forgejo auto-injects `FORGEJO_TOKEN` into every workflow run
with write access to the repository — `release.yml` uses it directly.

```bash
# Verify release.yml does NOT reference secrets.FORGEJO_* (reserved prefix — can never be created)
if [[ -f ".forgejo/workflows/release.yml" ]]; then
  if grep -q 'secrets\.FORGEJO_' .forgejo/workflows/release.yml; then
    echo "WARN: release.yml references a blocked secret (FORGEJO_ prefix reserved by Forgejo)"
    echo "Fix: remove the env block and use \$FORGEJO_TOKEN directly (auto-injected by runner)"
  else
    echo "release.yml: auth OK — uses auto-injected FORGEJO_TOKEN ✓"
  fi
fi
```

### Step 5: Output Next Steps

**If `staging.yml` is present** (staging-gated flow — required, not optional):

```
RELEASE PLAN READY: vX.Y.Z
============================
Milestone:    vX.Y.Z ({N} issues)
Issues:       #{list}
Flow:         release-branch (staging gate enforced — staging.yml present)
Auto-release: [YES — release.yml present] | [NO — manual release required]

Next steps:
1. Pick an issue and run /implementation (branches from main)
2. After each merge: /pr-merge Step 6 shows release progress
3. When milestone complete: /release verify commits → /release changelog
4. Cut release branch: git checkout -b release/vX.Y.Z && git push -u origin release/vX.Y.Z
5. Wait for staging green ✓ (CI clones prod DB + validates migrations)
   └─ If staging fails: fix on release branch → repush → wait for green
6. Open PR: release/vX.Y.Z → main → merge
7. Tag from main: git tag vX.Y.Z && git push --tags
   └─ [if release.yml present] Forgejo + GitHub releases created automatically
   └─ [if release.yml absent]  Create releases manually on Forgejo and GitHub
8. /release verify tags → close milestone
```

**If `staging.yml` is absent** (trunk-based flow):

```
RELEASE PLAN READY: vX.Y.Z
============================
Milestone:    vX.Y.Z ({N} issues)
Issues:       #{list}
Flow:         trunk-based (feature branches → main)
Auto-release: [YES — release.yml present] | [NO — manual release required]

Next steps:
1. Pick an issue and run /implementation (branches from main)
2. After each merge: /pr-merge Step 6 shows release progress
3. When milestone complete: /release verify commits → /release changelog → tag
4. Post-tag: [if release.yml present] Just tag and push — releases created automatically
           | [if release.yml absent]  Create releases manually on Forgejo and GitHub
5. /release verify tags → close milestone
6. Forgejo release secret: verified (release.yml will fire on tag push)
```

> **If release.yml is present**: After tagging, `git push --tags` is all you need. The workflow
> extracts CHANGELOG notes and creates both Forgejo and GitHub releases automatically.
> No Forgejo secret needed — `FORGEJO_TOKEN` is auto-injected by the runner.
> Optional: `GH_PAT` secret for GitHub release mirroring.

## Related Skills

- `/implementation` — implements features (branches from main)
- `/release verify` — verify commit↔changelog and tag↔changelog consistency
- `/review solve` — second opinion on release scope
- `/pr-merge` — Step 6 guides next steps based on milestone progress
