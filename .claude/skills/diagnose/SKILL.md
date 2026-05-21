---
name: diagnose
description: Investigate bugs with unknown root cause. Spawns fresh-context investigation subagent + parallel /review solve companion, persists hypotheses across iterations, hands off to /fix when root cause found.
allowed-tools: Read, Bash, Grep, Glob, Task, Write
---

# Diagnose Skill

## Purpose

Investigation skill for bugs where the root cause is **unknown**. When you don't know why
something is broken — just that it is — use `/diagnose` before reaching for `/fix`.

Key mechanism: spawns a fresh-context debugger subagent (Task tool) alongside a `/review solve`
companion analysis. The main agent orchestrates, stays clean, and synthesizes results. Debug
sessions persist in `.claude/debug/<slug>.md` so they survive context compaction and can be resumed.

**Not for:** applying a fix you already understand (use `/fix`), or quick one-line patches (use `/quick`).

---

## When to Use

|                    | `/quick` | `/fix` | `/diagnose`                  | `/implementation` |
| ------------------ | -------- | ------ | ---------------------------- | ----------------- |
| Root cause known?  | Yes      | Yes    | **No**                       | Yes               |
| Code changes       | Yes      | Yes    | **No (read-only)**           | Yes               |
| Subagent isolation | No       | No     | **Yes (fresh 200k context)** | No                |
| Companion analysis | No       | No     | **Yes (/review solve)**      | No                |
| Output             | Commit   | Commit | **Root cause report**        | PR                |

---

## Usage

```bash
/diagnose "auth token not working"          # start new session
/diagnose --resume auth-token               # resume session by slug
/diagnose --list                            # show all active sessions
/diagnose --close auth-token               # mark session resolved
/diagnose --issue 42                        # pull symptoms from GitHub issue
/diagnose --issue 42 "login fails on iOS"   # issue + free-form description
```

---

## Workflow

### Step 1: Collect Symptoms

Ask the user for (or pull from `gh issue view <N>` if `--issue` provided):

- **Expected** — what should happen
- **Actual** — what is happening
- **Error** — exact error message or stack trace (if any)
- **Timeline** — when did this start, what changed recently
- **Reproduction** — minimal steps to reproduce

Generate a session slug: slugify the first 3-4 words of the description.
Example: "auth token not working" → `auth-token-not-working`

### Step 2: Triage Relevant Files

Before spawning the subagent, the main agent does a quick triage:

```bash
# Find files related to the error message or function names mentioned
grep -r "<error keyword>" src/ --include="*.py" -l
# Identify entry points, related test files, config
```

Build a file list (max ~20 files) with a one-line reason per file.
This seeds the subagent with a focused starting point — not the whole codebase.

### Step 3: Initialize Session File

Write `.claude/debug/<slug>.md`:

```markdown
# Diagnose Session: <title>

**State:** active
**Created:** YYYY-MM-DD HH:MM
**Iteration:** 1
**Issue:** #N or —

## Symptoms

- Expected: ...
- Actual: ...
- Error: ...
- Timeline: ...
- Reproduction: ...

## Relevant Files

- `path/to/file.py` — reason it's relevant

## Hypotheses

### H1: <description>

- **Test:** <how to verify>
- **Result:** pending
- **Evidence:** —

## Root Cause

<!-- Filled when found -->

## Suggested Fix

<!-- Filled when root cause is confirmed -->
```

### Step 4: Parallel Investigation

Launch **both** simultaneously:

**A. Debugger subagent** (Task tool):

```
type: general-purpose
model: sonnet
prompt: |
  You are a debugger. Your job is to find the root cause of a bug.
  DO NOT modify any source code files — read-only investigation only.

  Read the session file at .claude/debug/<slug>.md for symptoms and file list.
  Then:
  1. Read all listed relevant files
  2. Form 2-3 hypotheses about the root cause
  3. Test each hypothesis: run existing tests, grep for related code, trace execution paths
  4. For each hypothesis: document Test, Result (confirmed/rejected), Evidence
  5. Write your findings back to the session file under ## Hypotheses
  6. If you find the root cause, fill ## Root Cause and ## Suggested Fix

  Model escalation: if sonnet-level investigation exhausts hypotheses after 2 attempts,
  note "Escalate to opus" in the session file.
```

**B. Companion analysis** (`/review solve`):

```bash
/review solve "<symptom description>" --context .claude/debug/<slug>.md
```

The companion gives an architectural second opinion: is this a design smell, a missing
invariant, or a pure implementation bug? Runs concurrently — no need to wait for the subagent.

### Step 5: Synthesize Results

Once both complete, the main agent:

1. Reads the updated session file (subagent findings)
2. Reads the companion analysis output
3. Synthesizes: code-level evidence (subagent) + architectural perspective (companion)
4. Reports a clear summary to the user:
   - What each hypothesis found
   - Whether root cause is confirmed
   - Confidence level (confirmed / suspected / unclear)

### Step 6: Evaluate and Iterate

**Root cause confirmed** → proceed to Step 7.

**All hypotheses rejected:**

- Ask the user for additional context (logs, reproduction details, recent changes)
- Update the session file with new context
- Increment `Iteration` counter
- **Iteration 1–2**: Spawn a new subagent iteration (`model: sonnet`) with updated session state
- **Iteration 3** (all hypotheses exhausted): Automatically escalate — spawn an Opus subagent:
  ```
  type: general-purpose
  model: opus
  prompt: |
    Sonnet-level investigation exhausted all hypotheses after 2 iterations.
    Read the full session file at .claude/debug/<slug>.md including all rejected hypotheses.
    Use deeper reasoning to identify what was missed. Focus on non-obvious causes:
    timing issues, environment differences, subtle state mutations, implicit contracts.
    Document new hypotheses and test them. Update ## Hypotheses, ## Root Cause, ## Suggested Fix.
  ```
  If Opus also cannot find the root cause, ask the user for direct manual investigation input.

### Step 7: Hand Off

Present the root cause to the user:

```
Root cause: <one-sentence summary>
Evidence: <key findings from hypothesis testing>
Confidence: confirmed | suspected

Suggested next step:
  - Small fix (1-3 files): /fix "<root cause summary>"
  - Larger change:         /implementation "<root cause summary>"
```

**Do NOT auto-invoke `/fix`** — the user decides when and how to proceed.

### Step 8: Close Session

Via `--close <slug>` (or automatically triggered after `/fix` confirms resolution):

```markdown
**State:** resolved
**Resolved:** YYYY-MM-DD
**Fix:** <commit SHA or PR #>
```

Session files are kept for future reference. They're gitignored (`.claude/debug/` is in `.gitignore`).

---

## --list and --resume

### --list

```bash
/diagnose --list
```

Glob `.claude/debug/*.md`, parse `State:` and title from each file.
Display as a table: slug | state | created | issue.

### --resume \<slug\>

```bash
/diagnose --resume auth-token-not-working
```

Read the session file, display current state and previous hypotheses.
Spawn a new subagent iteration with the full session context (including rejected hypotheses).
The subagent uses rejected hypotheses to avoid repeating dead ends.

---

## Session File Location

`.claude/debug/<slug>.md` — gitignored, peer to `.claude/plans/` and `.claude/tasks/`.

The directory is already excluded in `.gitignore`. Do not commit debug sessions.

---

## Related Skills

- `/fix` — apply the fix once root cause is known (natural next step after `/diagnose`)
- `/implementation` — larger fixes requiring full TDD and PR workflow
- `/review solve` — companion analysis used internally in Step 4
- `/review changes` — review code changes after `/fix` applies the fix
