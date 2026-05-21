# Brainstorm Workflow — 9 Stages

## Stage 1: Codebase Context Read (BEFORE asking any questions)

Read these files in the project to build technical understanding:

1. **Related models/entities** — find existing tables or Pydantic models related to the feature
   ```bash
   grep -r "class.*Model\|class.*Base\|__tablename__" src/ app/ --include="*.py" -l | head -10
   ```
2. **Existing FK patterns** — find how foreign keys are handled in migrations
   ```bash
   ls -t alembic/versions/*.py 2>/dev/null | head -3 | xargs grep -l "ForeignKey\|foreign_keys"
   ```
3. **Existing enum patterns** — find StrEnum / Literal usage
   ```bash
   grep -r "StrEnum\|Literal\[" src/ --include="*.py" -l | head -5
   ```
4. Read the 2-3 most relevant files found above (actual content, not just paths)

**Only after reading**: formulate questions that demonstrate what you already know.

Bad question: "Should owner_agent_role be required or optional?"
Good question: "agent_registry table exists with agent_role as PK — should owner_agent_role FK to it with ON DELETE SET NULL, or remain a loose string for bootstrap flexibility?"

---

## Stage 2: Visual Companion (optional)

Offer: "Would a schema diagram help before I write the spec?" — proceed either way.

---

## Stage 3: Targeted Questions

One `AskUserQuestion` call with 3-5 questions. Rules:
- Every question must reference something found in Stage 1
- No question answerable from the codebase map alone
- Questions reveal you've already read the code; they ask only what the code can't tell you

Example framing: "I see you use `ondelete='RESTRICT'` in work_items — should goals follow the same pattern or use SET NULL for subtree reorganization?"

---

## Stage 4: Approaches

Propose 2-3 concrete alternatives with trade-offs. Reference actual code patterns found.

---

## Stage 5: Design Presentation

Schema, API, data flow, error handling, test strategy — with file paths from the manifest.

---

## Stage 6: Write Spec Doc

See `templates/spec.md` for required format.

---

## Stage 7: Spec Self-Review

Scan for:
- Placeholders (TBD, TODO, `[...]`)
- Contradictions between schema and API sections
- Missing constraints (nullable? default? index?)
- Scope creep beyond the issue
- Missing cross-repo implications

---

## Stage 8: HARD GATE

Present spec to user. **Do NOT proceed without explicit approval.**
Fast mode still requires this gate — questions are skipped, not approval.

---

## Stage 9: Hand Off

Output: `STOP — spec at {path}. Run /implementation --issue N when ready.`
