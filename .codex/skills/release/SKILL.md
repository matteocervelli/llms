---
name: release
description: 'Plan version scope, verify release integrity (commit↔CHANGELOG, tag↔artifacts), generate changelogs, and run full releases. Use when cutting a release or bumping a version. Trigger on "cut a release", "bump the version", "generate changelog", "release plan", "verify the release".'
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Release Skill

Unified entry point for all release operations. Delegates to the right subcommand template based on the first argument.

## Subcommands

| Command                                    | What it does                                                                |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| `/release plan`                            | Scope version, analyze milestones/issues/tags, create GitHub milestone      |
| `/release verify [commits\|tags\|history]` | Integrity checks: commit↔CHANGELOG, tag↔releases↔artifacts, history audit   |
| `/release changelog`                       | Generate CHANGELOG entries + version bump propagation across manifest files |
| `/release full`                            | Full orchestrator: plan → health → fix blockers → docs → tag+ship           |
| `/release`                                 | Auto-detect what's needed (see below)                                       |

## Auto-Detection (no subcommand)

```bash
LAST_TAG=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null)
UNRELEASED=$(git log --no-merges --oneline "${LAST_TAG:-$(git rev-list --max-parents=0 HEAD)}..HEAD" | wc -l)
OPEN_MILESTONE=$(gh api "repos/$(gh repo view --json nameWithOwner --jq '.nameWithOwner')/milestones" \
  --jq '[.[] | select(.state=="open")] | length' 2>/dev/null || echo 0)
CLOSED_ISSUES=$(gh api "repos/$(gh repo view --json nameWithOwner --jq '.nameWithOwner')/milestones" \
  --jq '[.[] | select(.state=="open" and .open_issues==0)] | length' 2>/dev/null || echo 0)
```

Decision tree:

1. Milestone exists with 0 open issues → suggest `/release full`
2. Unreleased commits > 0, no milestone → suggest `/release plan`
3. Clean main, recent tag → suggest `/release verify tags`
4. Default → show the subcommand table above and ask what's needed

## Execution

Load the template matching the subcommand and follow it completely:

- `plan` → `~/.claude/skills/release/templates/plan.md`
- `verify` → `~/.claude/skills/release/templates/verify.md`
- `changelog` → `~/.claude/skills/release/templates/changelog.md`
- `full` → `~/.claude/skills/release/templates/cycle.md`

Pass any additional args through:

- `/release verify commits` → load verify.md, execute the `commits` subcommand
- `/release verify tags` → load verify.md, execute the `tags` subcommand
- `/release verify history` → load verify.md, execute the `history` subcommand

## Gotchas

- Auto-detection commands fail soft (`|| echo 0`) when `gh` is unauthenticated or there's no GitHub remote — a `0` open-milestone count may mean "no GitHub access", not "no milestones"; verify before trusting the decision tree.
- `git describe --tags --match "v*"` only finds tags reachable from HEAD — a tag on a sibling branch is invisible, so "no last tag" can be a false negative.
- `/release changelog` propagates the version bump across manifest files (pyproject.toml, package.json, etc.) — verify all manifests moved together; a partial bump ships mismatched versions.
- `/release full` tags and ships — it is not a dry run. Run `/release plan` first to confirm scope.
