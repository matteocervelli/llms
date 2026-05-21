---
paths:
  - "**/skills/**"
  - ".claude/skills/**"
  - ".codex/skills/**"
---

# Skill Architecture — Deterministic vs Latent

When building or improving a skill, decide where logic lives:

## Decision Rule

If a task has a **testable, deterministic algorithm** (same input → same output every time):

- Extract it to `skills/{name}/scripts/{name}.py` or `skills/{name}/lib/{name}.sh`
- SKILL.md invokes the script; it does NOT re-implement the logic in prose
- The script has unit tests in `skills/{name}/tests/`

If a task requires **judgment** (interpretation, synthesis, decision, context-sensitivity):

- Logic lives in SKILL.md as structured instructions
- The model reasons from context; output varies by situation

## Decision Table

| Task type                 | Category      | Lives in |
| ------------------------- | ------------- | -------- |
| Grep / file search        | Deterministic | Script   |
| Timestamp / date math     | Deterministic | Script   |
| URL or link generation    | Deterministic | Script   |
| API call + response parse | Deterministic | Script   |
| Config file read/write    | Deterministic | Script   |
| Code quality check        | Deterministic | Script   |
| Code review / critique    | Latent        | SKILL.md |
| Architecture decision     | Latent        | SKILL.md |
| Bug diagnosis             | Latent        | SKILL.md |
| Synthesis / summarization | Latent        | SKILL.md |

## Why This Matters

LLMs fail silently on mechanical tasks: timezone math produces wrong answers,
link generation drops entries after item 10, grep misses files outside sample.
Scripts are correct or they crash — both are better than silent errors.

The model's intelligence should build the deterministic tool, then be constrained
by it. Latent space builds; deterministic space enforces.

## Anti-Pattern to Avoid

```markdown
# WRONG: SKILL.md doing deterministic work

"Search all JSONL files in ~/.claude/projects/ for sessions
from the last 7 days that contain the word 'error'..."

# RIGHT: SKILL.md calls the script

Run: `uv run python scripts/session-search.py --days 7 --term error`
Then interpret the results.
```
