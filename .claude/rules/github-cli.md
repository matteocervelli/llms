---
paths:
  - "**/.github/**"
  - "**/CHANGELOG.md"
---

# GitHub CLI Rules

## Milestone Commands

**`gh milestone` does NOT exist.** Always use `gh api` for milestone operations.

```bash
# WRONG - will fail
gh milestone create "Sprint 1"
gh milestone list

# CORRECT - use gh api
gh api repos/:owner/:repo/milestones --method POST \
  -f title="Sprint 1" \
  -f description="Description" \
  -f due_on="YYYY-MM-DDT23:59:59Z"

# List milestones
gh api repos/:owner/:repo/milestones --jq '.[] | "\(.title): \(.open_issues) open"'

# Add issue to milestone (this works with gh issue)
gh issue edit 123 --milestone "Sprint 1"
```

## Valid gh Subcommands

These work: `issue`, `pr`, `repo`, `api`, `auth`, `release`, `workflow`, `run`, `gist`, `ssh-key`, `gpg-key`, `secret`, `variable`, `cache`, `codespace`, `extension`, `search`, `status`, `config`, `alias`, `completion`

These do NOT exist: `milestone`, `label create`, `project board`

## When in Doubt

Before running any `gh` command you're unsure about, check with:

```bash
gh --help | grep <subcommand>
```
