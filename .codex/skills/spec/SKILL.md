---
name: spec
description: >
  Write a durable feature spec before touching code. Reads the codebase map,
  reads related models/migrations to ask technical questions (not generic ones),
  then produces a structured spec doc in docs/specs/. Designed to pipeline with
  /implementation --issue N. Use before any feature implementation.
---

# /spec — Feature Specification

## Trigger

```
/spec --issue N [--fast]
```

- `--issue N` — required. Reads GitHub issue #N.
- `--fast` — skip questions, apply defaults from `reference/defaults.md`, still
  requires user approval of the spec (hard gate).

## Output

`docs/specs/YYYY-MM-DD-{slug}-issue-{N}.md`

YAML frontmatter includes `issue: N` so `/implementation --issue N` finds
this file automatically.

---

## Workflow

### Step 1 — Load codebase map

```bash
ls docs/codebase/INDEX.md 2>/dev/null || echo "missing"
```

If exists and < 7 days old: read `architecture.md` + `conventions.md`.
If missing or stale: run `/map-codebase` first, then proceed.

### Step 2 — Read issue

```bash
gh issue view N --json title,body,labels,state
```

### Step 3 — Brainstorm (9 stages)

See `workflows/brainstorm.md`.

**Key principle**: Stage 1 reads actual related code (models, migrations, FK patterns)
_before_ formulating questions. Questions must demonstrate codebase understanding —
reference specific tables, patterns, or files found in Stage 1.

### Step 4 — Write spec

Use `templates/spec.md`. Every column, every endpoint, every file in manifest.
No placeholders. No TBD. If unknown → make it a deferred decision, explicitly.

### Step 5 — Adversarial review (optional)

Ask explicitly:

> "Do you want an adversarial review of this spec before committing?
> This spawns a Codex/Gemini reviewer that looks for: missing constraints,
> wrong FK assumptions, scope creep, contradictions, and security gaps."

- Yes → run `/review solve "adversarial spec review: find flaws in docs/specs/{filename}"`, present findings, offer to fix before commit
- No → proceed to Step 6

### Step 6 — Commit spec

```bash
git add docs/specs/{filename}
git commit -m "docs(spec): {feature slug} spec — issue #{N}"
```

### Step 7 — Hand off

Print this block verbatim so the user can copy-paste it:

```
Spec committed: docs/specs/{filename}  (on main)

── Option A: implement in current session ──────────────────
  /implementation --issue {N}

── Option B: implement in a parallel worktree ──────────────
  git worktree add -b feature/{N}-{slug} ../{project}-{N} main
  # open new Claude Code session in ../{project}-{N}
  /implementation --issue {N}

── Fast mode (no questions, Codex review at end) ───────────
  /implementation --issue {N} --fast
```

**Spec stays on main.** The branch is created by worktree add or by
/implementation at start. Multiple specs can be committed to main
in parallel — they are docs only, no code conflicts.

Do not start implementing. Do not write any code.

---

## References

- `workflows/brainstorm.md` — 9-stage spec generation with technical question guidelines
- `reference/defaults.md` — fast mode assumptions table
- `templates/spec.md` — required spec document format
