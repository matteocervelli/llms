# Solve Prompt Template

## Variables

- `$PROBLEM_DESCRIPTION` — the technical problem (required)
- `$CONTEXT_BLOCK` — concatenated file/directory contents from `--context` flags (or empty)

## Gathering Context

```bash
CONTEXT_BLOCK=""
for CONTEXT_PATH in "${CONTEXT_PATHS[@]}"; do
  if [[ -f "$CONTEXT_PATH" ]]; then
    FILE_CONTENT=$(cat "$CONTEXT_PATH")
    CONTEXT_BLOCK+="
--- FILE: $CONTEXT_PATH ---
$FILE_CONTENT
"
  elif [[ -d "$CONTEXT_PATH" ]]; then
    DIR_LISTING=$(find "$CONTEXT_PATH" -type f \( -name '*.py' -o -name '*.ts' -o -name '*.js' -o -name '*.go' -o -name '*.rs' -o -name '*.md' \) | head -30)
    CONTEXT_BLOCK+="
--- DIRECTORY: $CONTEXT_PATH ---
Files:
$DIR_LISTING
"
    for F in $(echo "$DIR_LISTING" | head -5); do
      FILE_CONTENT=$(head -500 "$F" 2>/dev/null || true)
      [[ -n "$FILE_CONTENT" ]] && CONTEXT_BLOCK+="
--- FILE: $F ---
$FILE_CONTENT
"
    done
  fi
done
```

## Prompt

```
You are a senior architect providing a second opinion on a technical problem.

## Problem
$PROBLEM_DESCRIPTION

## Context
$CONTEXT_BLOCK

## Analysis Instructions

Analyze this problem thoroughly. Consider the constraints implied by any context files provided.

Be direct. No cheerleading. A one-line response is unacceptable.
Challenge assumptions in the problem statement if they seem flawed.

## Required Output Format

You MUST use this exact structure:

### Problem Restatement
Restate the problem in your own words. Call out any assumptions you're making.

### Approaches

For EACH approach (provide at least 2):

#### Approach N: [Name]
- **Description**: What this approach involves
- **Pros**: Specific advantages
- **Cons**: Specific disadvantages
- **Best When**: Under what conditions this is the right choice

### Recommendation
Which approach you'd choose and why. Be specific about the reasoning.

### Top 3 Risks
1. **Risk** — Mitigation strategy
2. **Risk** — Mitigation strategy
3. **Risk** — Mitigation strategy

### Validation Criteria
How to verify the chosen approach is working. Specific, measurable checks.

### Questions to Resolve
Any open questions that would change the recommendation if answered differently.

If a section has no findings, write 'None.' — do NOT omit the section.
```

## Approach Consensus (`--all` mode)

When multiple companions recommend approaches:

- All same approach → UNANIMOUS — high confidence
- 2 of 3 agree → MAJORITY — strong signal, note dissent
- All different → NO CONSENSUS — present all, highlight trade-offs

## Dispatch

```bash
: "${HOME:=$(eval echo ~)}"
echo "$PROMPT" | bash "$HOME/.claude/shared/companions/runner.sh" "$COMPANION" --model "$MODEL" --capability solve
```
