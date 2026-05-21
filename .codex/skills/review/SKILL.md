---
name: review
description: Dispatch reviews to external companion AIs (Codex, Gemini, Claude) for an independent second opinion on code changes, PR readiness, doc completeness, architecture, or implementation status. Use when you want a fresh-eyes review beyond Claude-native. Trigger on "get a second opinion", "companion review", "review my changes", "review the PR". For Claude-only quality checks use /code-review.
allowed-tools: Read, Bash, Grep, Glob
---

# Review — Companion-Dispatched Reviews & Analysis

Unified skill for all companion AI reviews. Dispatches structured prompts to external AIs (Codex, Gemini, Claude) via runner.sh for independent second opinions.

For Claude-native code quality checks (no external AI), use `/code-review`.

## Usage

```
/review                              # Auto-detect: uncommitted changes → changes review
/review changes                      # Full review: code + silent-failures + types + comments
/review changes --quick              # Code review only (skip silent-failures/types/comments)
/review pr [--pr N]                  # PR merge readiness (MERGE/BLOCK verdict)
/review doc <file>                   # PRP/PRD/RFC/Design completeness review
/review solve "problem"              # Architecture/design second opinion
/review status <spec>                # Implementation progress vs spec
/review frontend <url>               # Delegates to /frontend review
/review silent-failures [file|diff]  # Error handling audit
/review types [file]                 # Type design analysis
/review comments [file]              # Comment accuracy check
/review gate                         # Lightweight pre-commit gate (critical bugs + security only)
/review adversarial                  # Adversarial review: challenge design choices (Codex gpt-5.5 xhigh)
```

All subcommands support: `[companion]` (codex/gemini/claude), `--model MODEL`, `--all`, `--exclude-self`

## Workflow

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for subcommand and flags:

- First positional arg → subcommand (changes, pr, doc, solve, status, frontend, silent-failures, types, comments, gate, adversarial)
- If no subcommand: check for uncommitted changes → default to `changes`, else show usage
- Companion name: codex, gemini, or claude (optional, resolved from registry defaults)
- `--model MODEL` → override default model
- `--base BRANCH` → diff against branch (for changes/pr)
- `--pr NUMBER` → GitHub PR mode (for pr subcommand)
- `--context FILE` → attach context files (for solve)
- `--type PRP|PRD|RFC|DESIGN` → doc type override (for doc)
- `--issue NUMBER` → GitHub issue (for status)
- `--timeout SECS` → override default timeout
- `--all` → dispatch to all installed companions in parallel
- `--exclude-self` → exclude claude from `--all` runs
- `--quick` → code review only (for changes: skip silent-failures/types/comments checks)

### Step 2: Resolve Companion

```bash
: "${HOME:=$(eval echo ~)}"
DEFAULT_COMPANION=$(bash "$HOME/.claude/shared/companions/lib/resolve-default.sh" "$CAPABILITY")
COMPANION="${COMPANION:-$DEFAULT_COMPANION}"
```

Where `$CAPABILITY` maps from subcommand:

- changes → `review`
- pr → `pr-review`
- doc → `doc-review`
- solve → `solve`
- status → `implementation-status`
- gate → `review`
- silent-failures, types, comments → `review`

### Step 3: Check Availability

```bash
: "${HOME:=$(eval echo ~)}"
cat "$HOME/.claude/shared/companions/registry.json" | jq -r ".companions.$COMPANION.installed"
```

If not installed, report error with install instructions from registry.

### Step 4: Dispatch by Subcommand

Load the prompt template from `templates/` and dispatch:

| Subcommand        | Template                       | Input                                        | Capability            |
| ----------------- | ------------------------------ | -------------------------------------------- | --------------------- |
| `changes`         | `templates/changes.md`         | `git diff` (uncommitted or branch)           | review                |
| `pr`              | `templates/pr.md`              | `gh pr diff` or `git diff base...HEAD`       | pr-review             |
| `doc`             | `templates/doc.md`             | File content + type-specific criteria        | doc-review            |
| `solve`           | `templates/solve.md`           | Problem description + context files          | solve                 |
| `status`          | `templates/status.md`          | Reference doc/issue + codebase access        | implementation-status |
| `gate`            | `templates/gate.md`            | `git diff HEAD` (lightweight, critical only) | review                |
| `adversarial`     | `templates/adversarial.md`     | `git diff HEAD` (uncommitted)                | review                |
| `silent-failures` | `templates/silent-failures.md` | File content or diff                         | review                |
| `types`           | `templates/types.md`           | File content                                 | review                |
| `comments`        | `templates/comments.md`        | File content                                 | review                |

**Diff collection for `changes`, `adversarial`, and `gate`**: use the shared adaptive collector rather than raw `git diff`:

```bash
: "${HOME:=$(eval echo ~)}"
COLLECT_ARGS="--uncommitted"
[[ -n "$BASE_BRANCH" ]] && COLLECT_ARGS="--base $BASE_BRANCH"
DIFF=$(bash "$HOME/.claude/shared/companions/lib/collect_diff.sh" $COLLECT_ARGS)
```

This applies three-tier sizing automatically (full / per-file-truncated / stat+top10).

Each template contains the full prompt structure. Read the template for the prompt format, then build the prompt in bash using variable expansion. **NEVER use sed for interpolation** — diff content breaks sed delimiters. Instead:

```bash
# Build prompt by assembling sections directly (NOT by sed-replacing template vars)
PROMPT="You are a senior code reviewer...

Scope: $SCOPE
$TRUNCATION_WARNING

[rest of prompt from template]

--- DIFF ---
$DIFF"

# Write to temp file for large prompts (>50K)
echo "$PROMPT" > /tmp/review_prompt.txt
cat /tmp/review_prompt.txt | bash "$HOME/.claude/shared/companions/runner.sh" ...
rm /tmp/review_prompt.txt
```

The template shows the prompt structure and variables. Copy the prompt text from the template's ` ```prompt ` block, substitute variables inline via bash `"$VAR"` expansion, and pipe to runner.sh.

### Step 5: Dispatch via Runner

**Single companion:**

```bash
: "${HOME:=$(eval echo ~)}"
RUNNER_ARGS="$COMPANION --capability $CAPABILITY --timeout $TIMEOUT"
[[ -n "$MODEL" ]] && RUNNER_ARGS+=" --model $MODEL"
echo "$PROMPT" | bash "$HOME/.claude/shared/companions/runner.sh" $RUNNER_ARGS
```

**IMPORTANT**: Do NOT pass `--model default` or `--model ""`. Omit `--model` entirely when no user override is specified — runner.sh resolves from registry automatically.

**Adversarial subcommand**: always add `--structured --model gpt-5.5 --reasoning xhigh` to RUNNER_ARGS. Load the template from `~/.claude/shared/companions/templates/adversarial.md`, substitute `$REVIEWER_CONTEXT` with "second opinion for Claude", and substitute `$DIFF` / `$SCOPE` / `$TRUNCATION_WARNING` as usual.

**Gate subcommand**: use the fast `codex review -` path (no `--structured`). Parse PASS/BLOCK from the text output with grep. Timeout: 120s. Do NOT add `--structured` — `codex exec review --output-schema` has more latency than the native review mode and defeats the purpose of a fast gate.

**Multi-companion (`--all`):**

```bash
MULTI_ARGS="--capability $CAPABILITY --timeout $TIMEOUT"
[[ -n "$MODEL" ]] && MULTI_ARGS+=" --model $MODEL"
$EXCLUDE_SELF && MULTI_ARGS+=" --exclude-self"

: "${HOME:=$(eval echo ~)}"
MULTI_OUTPUT=$(echo "$PROMPT" | bash "$HOME/.claude/shared/companions/multi-runner.sh" $MULTI_ARGS)
```

### Step 6: Present Output

Display companion output directly in the conversation. Never write to files.

**Single companion:**

```
══════════════════════════════════════
REVIEW: [Subcommand] — [Companion] ([model])
Target: [scope description]
══════════════════════════════════════

[companion output]

══════════════════════════════════════
```

**Multi-companion:**

```
══════════════════════════════════════
MULTI-COMPANION REVIEW: [Subcommand]
Target: [scope description]
══════════════════════════════════════

[multi-runner output — each companion labeled]

══════════════════════════════════════
```

### Step 7: Analysis

After presenting companion output, add:

**Extended Analysis** — For each finding:

- Agree/disagree with companion, with reasoning
- Additional codebase context
- Severity assessment

**Action Plan** — Prioritized checklist ordered by severity. Skip false positives.

For `--all` mode, perform **consensus analysis** instead:

- UNANIMOUS: All companions agree → high confidence
- MAJORITY: >50% agree → strong signal
- SOLO: Only one flagged → validate manually
- CONFLICTING: Companions disagree → needs human judgment

### Special: `/review frontend`

Delegates to `/frontend review`. Display message:

```
Delegating to /frontend review — visual design review requires Gemini multimodal.
Run: /frontend review [url] [--full-page] [--color-scheme MODE]
```

### Default: `/review changes` (full review)

By default, `/review changes` runs the standard code review prompt PLUS appends checks from:

- `templates/silent-failures.md` (error handling audit)
- `templates/types.md` (type design analysis)
- `templates/comments.md` (comment accuracy)

### Special: `/review changes --quick`

Skips silent-failures, types, and comments checks. Runs only the standard code review prompt from `templates/changes.md`. Use when you want a fast review and don't need the deeper audits.

## Diff Handling (shared by changes, pr, gate)

```bash
# Determine diff
if [[ -n "$BASE_BRANCH" ]]; then
  DIFF=$(git diff "$BASE_BRANCH"...HEAD)
  SCOPE="branch diff: $(git branch --show-current) vs $BASE_BRANCH"
elif [[ -n "$PR_NUMBER" ]]; then
  DIFF=$(gh pr diff "$PR_NUMBER")
  SCOPE="PR #$PR_NUMBER"
else
  DIFF=$(git diff HEAD)
  SCOPE="uncommitted changes"
fi

# Empty check
if [[ -z "$DIFF" ]]; then
  echo "No changes to review."
  exit 0
fi

# Size guard — truncate at 100K chars
DIFF_LEN=${#DIFF}
if [[ $DIFF_LEN -gt 100000 ]]; then
  DIFF="${DIFF:0:100000}"
  TRUNCATION_WARNING="WARNING: Diff truncated from $DIFF_LEN to 100,000 characters."
fi
```

## Default Timeouts

| Subcommand      | Default Timeout | Reason                        |
| --------------- | --------------- | ----------------------------- |
| changes         | 300s            | Standard review               |
| pr              | 300s            | Standard review               |
| doc             | 300s            | Standard review               |
| solve           | 300s            | Standard analysis             |
| status          | 600s            | Deep codebase exploration     |
| gate            | 120s            | Lightweight, pre-commit speed |
| silent-failures | 300s            | Standard analysis             |
| types           | 300s            | Standard analysis             |
| comments        | 300s            | Standard analysis             |

## Critical Rules

0. **Failure policy — one companion, no substitution, no workarounds.**
   - Hard failures (auth error, model-not-found, empty output, non-zero exit): report the exact error and stop. Do NOT retry.
   - Transient failures (timeout, exit 124, rate-limit 429): retry the **same companion once only**. If it fails again, stop and report.
   - Never switch to a different companion after any failure.
   - **Never fall back to Claude's own analysis, `/code-review`, or any other native review path.** The point is an independent second opinion — any Claude-generated review defeats the purpose. Report the failure and let the user decide the next step.
   - This applies to all subcommands and all companions (codex, gemini, claude).

1. **All companions use runner.sh.** No native path for any companion. Codex goes through `codex exec` via runner.sh.

2. **Guard `$HOME` in every bash block**: `: "${HOME:=$(eval echo ~)}"`. Then use `$HOME` (not `~`) in all paths.

3. **Display output directly.** Never write to plan files, markdown files, or any other file.

4. **Codex may hallucinate success** (especially in status assessments). Always cross-reference evidence paths. Treat output as advisory, not authoritative.

## Error Handling

- No changes to review → "No changes to review" and stop
- Missing required input (file path, problem description, reference) → report what's needed and stop
- Companion not installed → report with install instructions from registry
- Companion timeout → report timeout, suggest narrowing scope
- Empty/one-line output → report insufficient output and stop
- `gh` CLI not available (for --pr/--issue) → report GitHub CLI required

## Integration

**Invoked by**: User directly (`/review`), `/pre-commit` step 5 (`/review gate`)
**Infrastructure**: `~/.claude/shared/companions/` (runner.sh, multi-runner.sh, registry.json, lib/)
**Claude-native alternative**: `/code-review` (for fast, local quality checks without external AI)
**Related**: `/frontend review` (visual design review via Gemini multimodal)
