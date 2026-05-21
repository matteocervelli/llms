---
name: pr-creator
description: Create comprehensive pull requests with detailed descriptions, test plans, and proper git workflow. Use when finalizing features to ensure high-quality PRs.
allowed-tools: Read, Bash, Grep
---

# Pull Request Creator Skill

## Purpose

Systematic guidance for creating high-quality pull requests with comprehensive descriptions and proper commit messages.

## When to Use

- Called by `/ship` after `/pre-commit` passes — standard path
- Directly when you've already committed and pushed manually and need a PR
- Following git workflow best practices

> **Called by `/ship`?** Skip Step 1 (pre-flight). `/pre-commit` already ran. Start at Step 1.5.

## PR Creation Workflow

### 1. Pre-Flight Checks (skip if called by /ship)

```bash
# All changes committed
git status
# Should show: "nothing to commit, working tree clean"

# All tests passing
pytest

# Code quality checks passed
/quality-check

# CHANGELOG updated
head -50 CHANGELOG.md
```

**If any check fails**: Fix before proceeding.

---

### 1.5. Release Artifact Verification

Run `/release verify commits` to check commit↔changelog consistency.

If result is **WARN** or **FAIL**: report the unmatched commits, ask user whether to fix now (run `/release changelog`) or proceed anyway.

Additionally check:

```bash
# Detect version files in the project
for f in pyproject.toml package.json setup.cfg Cargo.toml; do
  [[ -f "$f" ]] && echo "Version file found: $f"
done

# Check for hardcoded version strings in README
grep -n 'v[0-9]\+\.[0-9]\+\.[0-9]\+' README.md 2>/dev/null || echo "No version refs in README"

# Check roadmap
[[ -f ROADMAP.md ]] && echo "ROADMAP.md exists — verify it reflects shipped features"

# Check project-level CLAUDE.md
[[ -f CLAUDE.md ]] && echo "CLAUDE.md exists — verify new features/skills documented"
```

**Checklist (verify each, report missing):**

- [ ] **CHANGELOG.md** — `/release verify commits` PASS or acknowledged WARN
- [ ] **Version files** — if release PR, version bumped in detected files
- [ ] **README.md** — hardcoded version references updated (if any)
- [ ] **ROADMAP.md** — updated if exists and features affect roadmap
- [ ] **Project CLAUDE.md** — reflects new features/skills/rules if applicable

If any item is missing: report clearly, ask user whether to fix now or proceed.

---

### 2. Review Changes

```bash
# Detect base (supports release/* sub-branching)
# Try upstream tracking branch first, then fall back to main
BASE_BRANCH=$(git config "branch.$(git branch --show-current).merge" 2>/dev/null | sed 's|refs/heads/||')
if [[ -z "$BASE_BRANCH" ]]; then
  # No upstream configured — check if branch was created from a release/*
  PARENT=$(git log --oneline --decorate --all --ancestry-path HEAD 2>/dev/null | grep -m1 'origin/release/' | sed 's|.*origin/\(release/[^ ,)]*\).*|\1|')
  BASE_BRANCH="${PARENT:-main}"
fi

# View commits in feature branch
git log --oneline "$BASE_BRANCH"..HEAD

# View files changed
git diff --stat "$BASE_BRANCH"..HEAD
```

---

### 3. Push to Remote

```bash
git push -u origin feature/issue-123-description
```

---

### 4. Create Pull Request

**PR Title Format**: `<type>: <brief description> (#<issue>)`

**Commit Types**: feat, fix, docs, style, refactor, perf, test, chore

**Create PR with gh CLI**:

```bash
gh pr create \
  --title "feat: implement feature (#123)" \
  --body "$(cat <<'EOF'
[PR description from template]
EOF
)"
```

---

## PR Templates

Templates are in `templates/` directory:

- **minimal.md** - Quick fixes, small changes
- **standard.md** - Normal features
- **comprehensive.md** - Major features, complex changes

Choose based on PR scope.

---

### 5. Update Project Tracking

Update TASK.md to mark issue completed with PR link.

---

### 6. Verify PR Quality

```bash
# View PR in browser
gh pr view --web

# Check CI status
gh pr checks
```

**Quality Checklist**:

- [ ] PR title follows conventional commits
- [ ] PR description comprehensive
- [ ] Test coverage details included
- [ ] Breaking changes documented
- [ ] Issue references included (Closes #123)
- [ ] All CI checks passing

---

## Git Workflow

### Branch Naming

`<type>/<issue-number>-<brief-description>`

Examples:

- `feature/123-user-authentication`
- `fix/124-memory-leak`
- `docs/125-api-documentation`

### Keeping Branch Updated

```bash
# Rebase on main
git fetch origin main
git rebase origin/main

# Force push (if already pushed)
git push --force-with-lease
```

---

## Common Issues

### PR too large

Break into smaller PRs, create epic issue for tracking.

### Merge conflicts

```bash
git checkout main && git pull
git checkout feature/123 && git rebase main
# Resolve conflicts
git push --force-with-lease
```

### CI checks failing

```bash
gh pr checks
# Fix issues locally, commit, push
```

---

## Quick Reference

```bash
# Create PR
gh pr create --title "..." --body "..."

# View PR
gh pr view 123

# Edit PR
gh pr edit 123

# Check status
gh pr checks
```

---

## Related Skills

- `/quality-check` - Run before PR
- `/release changelog` - Update CHANGELOG
- `/pre-commit` - Full validation suite
- `/review changes` - Companion review (run before PR)
- `/pr-merge` - Post-PR merge workflow
- `/release plan` - Version planning
