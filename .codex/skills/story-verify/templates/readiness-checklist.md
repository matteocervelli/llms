# Development Readiness Checklist

## Checks (all must pass for READY verdict)

### 1. INVEST Validation

Run `/story-verify invest {id}`.

- **Required**: Overall score >= 70, all criteria >= 50
- **If fails**: Fix story definition first

### 2. Dependency Resolution

Check `blocked_by` in story YAML.

- **Required**: All blocked_by stories have status `done`
- **If fails**: Complete blocking stories first, or remove dependency if it's no longer needed

### 3. Test Stubs Exist

Search for test file matching `test_US_XXXX*` or `US_XXXX*.test.*`.

- **Required**: At least one test file exists with stubs for each acceptance criterion
- **If fails**: Run `/story tests {id}` to generate stubs

### 4. PRP Coverage

Search PRP directory for files referencing this story ID.

- **Required**: At least one PRP references this story
- **If fails**: Run `/story prp {id}` to generate PRP

### 5. Technical Context

Check if story has enough detail for implementation:

- Are the acceptance criteria specific enough to code against?
- Is the data model clear from the criteria?
- Are external dependencies identified?

This is a judgment call — flag concerns but don't auto-fail.

## Verdicts

| Result       | Meaning                                                          |
| ------------ | ---------------------------------------------------------------- |
| READY        | All 4 required checks pass. Start implementing.                  |
| ALMOST READY | 1 check fails with easy fix (usually missing test stubs)         |
| NOT READY    | 2+ checks fail. Address issues before starting.                  |
| BLOCKED      | Dependencies not resolved. Cannot start until blockers complete. |

## Output Format

```
US-XXXX: {title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  {status} INVEST validation: {PASS|FAIL} (score: {score})
  {status} Dependencies: {list of blocked_by with their status}
  {status} Test stubs: {FOUND|NOT FOUND}
  {status} PRP coverage: {PRP-XXX covers this | NOT FOUND}
  {status} Technical context: {assessment}

  Verdict: {READY|ALMOST READY|NOT READY|BLOCKED}
  {Next action suggestion if not READY}
```
