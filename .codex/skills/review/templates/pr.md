# PR Review Prompt Template

## Variables

- `$PR_TITLE` — PR title (from gh or branch name)
- `$PR_BODY` — PR description (from gh or commit log)
- `$PR_LABELS` — comma-separated labels (or empty)
- `$SCOPE` — "PR #42: title (head -> base)" or "branch diff: feature vs main"
- `$PR_DIFF` — diff output
- `$TRUNCATION_WARNING` — warning if diff was truncated (or empty)

## Gathering PR Context

### GitHub PR mode (`--pr NUMBER`)

```bash
PR_DIFF=$(gh pr diff "$PR_NUMBER")
PR_META=$(gh pr view "$PR_NUMBER" --json title,body,labels,baseRefName,headRefName,commits)
PR_TITLE=$(echo "$PR_META" | jq -r '.title')
PR_BODY=$(echo "$PR_META" | jq -r '.body')
PR_LABELS=$(echo "$PR_META" | jq -r '[.labels[].name] | join(", ")')
PR_BASE=$(echo "$PR_META" | jq -r '.baseRefName')
PR_HEAD=$(echo "$PR_META" | jq -r '.headRefName')
SCOPE="PR #$PR_NUMBER: $PR_TITLE ($PR_HEAD -> $PR_BASE)"
```

### Branch diff mode (default)

```bash
BASE="${BASE_BRANCH:-main}"
PR_DIFF=$(git diff "$BASE"...HEAD)
COMMITS=$(git log --oneline "$BASE"..HEAD)
BRANCH=$(git branch --show-current)
SCOPE="branch diff: $BRANCH vs $BASE"
PR_TITLE="$BRANCH"
PR_BODY="Commits:\n$COMMITS"
PR_LABELS=""
```

## Prompt

```
You are a senior engineer reviewing a pull request for merge readiness.

## PR Context
Title: $PR_TITLE
Description: $PR_BODY
Labels: $PR_LABELS
Scope: $SCOPE
$TRUNCATION_WARNING

## Review Instructions

Analyze this PR diff for merge readiness. Focus on:

1. **Correctness vs Description** — Does the code do what the PR says it does? Any gaps between intent and implementation?
2. **Backward Compatibility** — Breaking changes to APIs, configs, data formats, or public interfaces? Migration needed?
3. **Architecture Fit** — Does this follow existing patterns? Any unnecessary complexity or abstraction?
4. **Security** — New attack surfaces, credential handling, input validation, OWASP concerns?
5. **Test Coverage** — Are new code paths tested? Edge cases covered? Any untestable code?
6. **Error Handling** — Failure modes, error messages, recovery paths?

Be direct. No cheerleading. A one-line response is unacceptable.

## Required Output Format

You MUST use this exact structure:

### Verdict

One of:
- **MERGE** — Ready to merge, no issues found
- **MERGE WITH NOTES** — Safe to merge, minor items noted below
- **CHANGES REQUESTED** — Issues must be addressed before merge
- **BLOCK** — Critical problems that prevent merge

### Summary
2-3 sentences on what this PR does and the overall assessment.

### Critical (blocks merge)
- `file:line` — description and why it blocks

### Important (should address)
- `file:line` — description

### Suggestions
- `file:line` — description

### Breaking Changes
List any backward-incompatible changes, or 'None.'

### Test Coverage Assessment
Brief assessment of whether new code paths have adequate test coverage.

If a section has no findings, write 'None.' — do NOT omit the section.

--- PR DIFF ---
$PR_DIFF
```

## Verdict Consensus (`--all` mode)

When multiple companions return verdicts:

- All agree MERGE → UNANIMOUS MERGE
- All agree BLOCK → UNANIMOUS BLOCK (flag prominently)
- Mixed → use most conservative verdict as recommendation

## Dispatch

```bash
: "${HOME:=$(eval echo ~)}"
echo "$PROMPT" | bash "$HOME/.claude/shared/companions/runner.sh" "$COMPANION" --model "$MODEL" --capability pr-review
```
