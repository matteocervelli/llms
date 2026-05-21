---
name: implementation
description: Fast spec-driven implementation from a committed spec. Use after /spec to implement an issue with a phase roadmap, TDD waves, map patching, review, and pre-commit validation.
allowed-tools: Read, Bash, Grep, Glob, Task, TodoWrite, Edit, MultiEdit, Write
---

# /implementation — Spec-Driven Implementation Skill

## Purpose

Fast, spec-driven implementation. Reads the spec produced by `/spec`, skips
codebase exploration (map already exists), builds a GSD-style phase roadmap,
implements TDD per phase. Designed to run after `/spec` — either immediately
or in a separate session while another issue is being specced in parallel.

## Trigger

```
/implementation --issue N [--fast] [--no-branch]
```

- `--issue N` — required. Finds `docs/specs/*-issue-{N}.md` automatically.
- `--fast` — no questions, auto-approve design decisions from spec.
- `--no-branch` — stay on current branch.

---

## Workflow

### Step 0 — Locate spec

```bash
find docs/specs -name "*-issue-{N}.md" | head -1
```

If not found: `STOP — run /spec --issue N first.`

Read the spec. Extract: requirements (GOAL-XX), file manifest, API contract,
schema, design decisions.

### Step 1 — Load codebase map (no exploration)

```bash
ls docs/codebase/INDEX.md
```

If exists: read `INDEX.md`, `architecture.md`, `conventions.md`, and `test.md`.
Skip all exploration agents. The spec + map are the only context needed.

If missing: `STOP — run /map-codebase first, then /spec --issue N.`

### Step 2 — Create feature branch

```bash
git checkout main && git pull origin main
git checkout -b feature/{N}-{slug}
```

Skip if `--no-branch` or already on `feature/*` / `fix/*`.

### Step 3 — Build phase roadmap (GSD-style)

Using the spec requirements (GOAL-XX), produce a phase plan:

```
Phase 1: {Data layer} — migration, model, schema
  Requirements: GOAL-01, GOAL-02, ...
  Success criteria:
  1. [specific, testable — e.g. "alembic upgrade head runs without error"]
  2. [test count: "N integration tests pass"]
  Entry condition: [what must be true before starting]

Phase 2: {Service + API} — service, routes, tests
  Requirements: GOAL-05, ...
  Success criteria: [endpoint-by-endpoint]
  Depends on: Phase 1

Phase 3: {Proxy + commit} — cross-repo DTOs, proxy router, close issue
  Requirements: GOAL-08, ...
  Success criteria: [all repos committed, N respx tests pass]
  Depends on: Phase 2
```

Show roadmap to user before proceeding (brief, not a full plan approval gate).

### Step 4 — Create task list

TaskCreate for each phase + mandatory final tasks:

- "Run fast test suite"
- "Run /review changes (Codex)"
- "Fix critical/high findings"
- "Run /pre-commit"

### Step 5 — Implement phases (TDD + fresh subagents)

**Token budget**: orchestrator keeps ≤15% of context. All heavy work in subagents.

**Task sizing**: break each phase into 2-5 minute chunks before spawning.
No placeholder language in task descriptions — every task includes exact file
path, exact code to write, exact test command to run.

**Per task execution (Superpowers two-stage model)**:

1. Spawn **fresh subagent** with complete task text + relevant spec sections.
   Zero session history — subagent gets only: task description, spec excerpt,
   `conventions.md` excerpt, files to touch. Nothing else.
2. Subagent implements → RED (write failing test) → GREEN (implement) → runs
   `uv run pytest {test_file} -x -q`
3. **Stage A — Spec compliance review**: dedicated reviewer checks:
   - Does output match spec file manifest exactly? (no extra files)
   - Does schema match spec table exactly? (columns, types, constraints)
   - Are all GOAL-XX requirements covered?
     Only if ✅ → proceed to Stage B.
4. **Stage B — Code quality review**: separate reviewer checks:
   - Follows `conventions.md`? (naming, imports, async, test patterns)
   - No placeholder language or TODO left in code?
   - Edge cases covered?
5. Mark task complete only when both stages ✅.
   If either fails: fix in same subagent context, re-run review. Do NOT move on.

**Wave-based dependency grouping**: tasks within a phase with no inter-dependency
run as a wave (parallel subagents). Tasks that depend on prior outputs wait for
their wave to complete before starting.

Naming, patterns, imports: follow `conventions.md` exactly.
Cross-repo work: order per spec phase plan.

### Step 6 — Post-implementation

After all phases green:

**6a. Update codebase map (patch, not rebuild)**

Spawn 2 Haiku agents in parallel:

- Agent 1: update `architecture.md` + `structure.md` for new files/modules added
- Agent 2: update `integrations.md` if new external endpoints added

Do NOT regenerate `conventions.md` or `stack.md` (they do not change per-feature).
Commit: `docs(codebase): update map for issue #{N}`

**6b. Companion review**

Run `/review changes` with this framing for Codex:

```
Review these changes as Matteo Cervelli would.
Context: spec at docs/specs/*-issue-{N}.md
Flag:
1. Any assumption marked "> Assumed:" in the spec that you would have
   decided differently, and why
2. Any design decision that diverges from `conventions.md`
3. Any missing edge cases in the tests
4. Any scope creep beyond the spec's file manifest
```

**6c. Fix critical/high findings**

**6d. Run `/pre-commit`**

**6e. STOP — propose `/ship --issue N`**

Do not push. Present smoke test checklist. Wait for user.

---

## Fast mode (`--fast`)

- Step 3 roadmap: show but don't wait for confirmation, proceed immediately
- Step 6b Codex review: always runs (not optional in fast mode)
- No AskUserQuestion at any point
- If ambiguity arises mid-implementation: pick the approach in the spec,
  document the choice in a `# NOTE:` comment, flag it in the Codex review prompt

---

## Key invariants

- Never start Phase N+1 with failing tests from Phase N
- Never re-explore the codebase (map + spec are the only context)
- Never implement files not in the spec's file manifest (scope creep)
- Always update the codebase map at end — it's the investment for the next run
- Codex review is mandatory, not optional
