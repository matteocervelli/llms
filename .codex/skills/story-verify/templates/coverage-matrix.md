# Story-to-Test Coverage Matrix

## How to Build the Matrix

### Step 1: Find Test Files

For each story `US-XXXX`, search for matching test files:

```bash
# pytest
find tests/ -name "test_US_XXXX*" -o -name "*US_XXXX*"

# jest
find __tests__/ src/ -name "US_XXXX*.test.*" -o -name "*US_XXXX*"
```

### Step 2: Match Criteria to Tests

For each acceptance criterion in the story:

1. Generate a **criterion slug** from the "then" clause:
   - "I see a health score between 0-100" → `health_score_displayed`
   - "error message is shown" → `error_message_shown`

2. Search test files for matching function:
   - pytest: `def test_*{slug}*` or docstring containing the criterion text
   - jest: `test('*{slug}*'` or `it('*{slug}*'`

3. Mark as covered (found) or gap (not found)

### Step 3: Output Format

```
Story Coverage Report
Generated: {date}
Project: {project_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

US-XXXX: {title}                    [{covered}/{total} criteria]
  {status} {criterion_summary}     → {test_function or "NO TEST"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Summary:
  Stories: {total_stories} ({stories_with_tests} have tests)
  Criteria: {total_criteria} ({covered_criteria} covered)
  Coverage: {percentage}%

  Gaps requiring `/story tests`:
  - US-XXXX: {count} untested criteria
```

### Status Icons

- Covered: checkmark
- Gap: cross mark
- Partial (test exists but doesn't match criterion): warning

## Threshold

- **Green**: >=80% criteria covered
- **Yellow**: 50-79% criteria covered
- **Red**: <50% criteria covered
