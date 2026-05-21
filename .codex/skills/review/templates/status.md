# Implementation Status Prompt Template

## Variables

- `$REFERENCE` — combined reference content (doc + issue)
- `$FILE_PATH` — reference document path (optional)
- `$ISSUE_NUMBER` — GitHub issue number (optional)
- `$TIMEOUT` — default 600s (deep codebase exploration)

## Gathering Reference Content

```bash
REFERENCE=""

# GitHub issue mode
if [[ -n "$ISSUE_NUMBER" ]]; then
  ISSUE_DATA=$(gh issue view "$ISSUE_NUMBER" --json title,body,comments)
  ISSUE_TITLE=$(echo "$ISSUE_DATA" | jq -r '.title')
  ISSUE_BODY=$(echo "$ISSUE_DATA" | jq -r '.body')
  ISSUE_COMMENTS=$(echo "$ISSUE_DATA" | jq -r '[.comments[].body] | join("\n---\n")')
  REFERENCE+="
## GitHub Issue #$ISSUE_NUMBER: $ISSUE_TITLE

$ISSUE_BODY

### Comments
$ISSUE_COMMENTS
"
fi

# File mode
if [[ -n "$FILE_PATH" ]]; then
  DOC_CONTENT=$(cat "$FILE_PATH")
  REFERENCE+="
## Reference Document: $(basename "$FILE_PATH")

$DOC_CONTENT
"
fi

if [[ -z "$REFERENCE" ]]; then
  echo "Error: No reference source provided. Specify a file path or --issue NUMBER."
  exit 1
fi
```

## Prompt

```
You are a senior engineer assessing implementation status of a codebase against a reference specification.

## Reference Specification
$REFERENCE

## Instructions

Your job is to determine what has been implemented and what hasn't. Follow these steps:

1. Read the reference specification above carefully
2. Extract every requirement, acceptance criterion, feature, and behavioral expectation described
3. Explore the codebase autonomously — read files, search for implementations, trace code paths
4. For EACH extracted item, classify its implementation status

Be thorough. Read actual source files to verify implementation, don't just check for file existence.
Be direct. No cheerleading. A one-line response is unacceptable.

## Status Classifications

- **Done** — Fully implemented and matches the spec
- **Partial** — Some aspects implemented but incomplete
- **Missing** — No implementation found
- **Diverged** — Implemented but differs from the spec in a meaningful way

## Required Output Format

You MUST use this exact structure:

### Implementation Summary
X of Y requirements implemented. N partial, M missing, K diverged.

### Requirements Tracker
| # | Requirement | Status | Evidence | Notes |
|---|-------------|--------|----------|-------|
| 1 | description | Done | file:line | — |
| 2 | description | Partial | file:line | what's missing |
| 3 | description | Missing | — | — |
| 4 | description | Diverged | file:line | how it differs |

### Key Gaps
Most impactful missing/partial items and their dependencies. What would you prioritize fixing first?

### Architecture Observations
Any structural issues noticed during exploration — code organization, patterns, or concerns unrelated to specific requirements but worth flagging.

If a section has no findings, write 'None.' — do NOT omit the section.
```

## Caveat

Codex may hallucinate success — reporting items as Done when they are not. Always cross-reference the evidence paths in the Requirements Tracker. Treat companion output as advisory, not authoritative.

## Dispatch

```bash
: "${HOME:=$(eval echo ~)}"
echo "$PROMPT" | bash "$HOME/.claude/shared/companions/runner.sh" "$COMPANION" --model "$MODEL" --timeout "$TIMEOUT" --capability implementation-status
```
