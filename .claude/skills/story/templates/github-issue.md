# GitHub Issue Template for Stories

## Issue Title

`US-XXXX: {story_title}`

## Issue Body

```markdown
## User Story

**As a** {persona},
**I want** {i_want},
**So that** {so_that}.

## Acceptance Criteria

{For each criterion:}

- [ ] **Given** {given}, **when** {when}, **then** {then}

## Details

| Field        | Value                  |
| ------------ | ---------------------- |
| Story Points | {story_points}         |
| Priority     | {priority}             |
| Epic         | {epic or "N/A"}        |
| Dependencies | {blocked_by or "None"} |

## Test Traceability

Test file: `tests/unit/test_US_XXXX_{feature_slug}.py`
```

## Labels

```bash
gh issue create \
  --title "US-XXXX: {title}" \
  --body "$(cat stories/generated-docs/US-XXXX.md)" \
  --label "user-story" \
  --label "story-points-{points}" \
  --label "priority-{priority}"
```

## Update Existing Issue

```bash
gh issue edit {issue_number} \
  --body "$(cat stories/generated-docs/US-XXXX.md)"
```
