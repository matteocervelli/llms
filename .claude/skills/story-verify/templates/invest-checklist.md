# INVEST Validation Checklist

## Scoring Rules (0-100 per criterion)

### Independent (I)

Check `blocked_by` field in story YAML.

| Condition                             | Score |
| ------------------------------------- | ----- |
| Empty blocked_by or 1 dependency      | 100   |
| 2-3 dependencies                      | 50    |
| >3 dependencies or circular reference | 0     |

**Circular check**: If US-A blocks US-B AND US-B blocks US-A → score 0 for both.

### Negotiable (N)

Analyze `i_want` field text.

| Condition                                                            | Score |
| -------------------------------------------------------------------- | ----- |
| Describes behavior/outcome ("view", "receive", "manage")             | 100   |
| Mentions tech but stays flexible ("use a table to display")          | 50    |
| Prescribes implementation ("create a React component with useState") | 0     |

**Red flags**: specific library names, code patterns, exact UI elements.

### Valuable (V)

Analyze `so_that` field.

| Condition                                                      | Score |
| -------------------------------------------------------------- | ----- |
| Clear, measurable benefit ("reduce time from 5 min to 30 sec") | 100   |
| Vague benefit ("improve the experience", "make it better")     | 50    |
| Missing `so_that` or empty string                              | 0     |

**Quality indicators**: numbers, percentages, time savings, cost reduction.

### Estimable (E)

Check `story_points` and `acceptance_criteria` fields.

| Condition                                             | Score |
| ----------------------------------------------------- | ----- |
| Has valid Fibonacci points (1,2,3,5,8) + >=3 criteria | 100   |
| Has points OR >=2 criteria, but not both              | 50    |
| Missing both, or non-Fibonacci points, or <2 criteria | 0     |

### Small (S)

Check `story_points` value.

| Condition            | Score |
| -------------------- | ----- |
| 1-5 points           | 100   |
| 6-8 points           | 50    |
| >8 points or missing | 0     |

**>8 points**: MUST suggest splitting. Common splits:

- By user action (view vs edit vs delete)
- By data scope (single item vs list vs search)
- By persona (admin vs end-user)

### Testable (T)

Check `acceptance_criteria` array.

| Condition                                                      | Score |
| -------------------------------------------------------------- | ----- |
| All criteria have given + when + then (all 3 fields non-empty) | 100   |
| Some criteria missing 1 field                                  | 50    |
| No criteria, or criteria without given/when/then structure     | 0     |

## Pass/Fail Logic

- **Overall score** = (I + N + V + E + S + T) / 6
- **PASS**: overall >= 70 AND every individual criterion >= 50
- **FAIL**: overall < 70 OR any criterion < 50

## Severity Levels

| Score Range | Severity | Action                   |
| ----------- | -------- | ------------------------ |
| 0-49        | Critical | Must fix before sprint   |
| 50-69       | High     | Should fix before sprint |
| 70-84       | Medium   | Optional improvement     |
| 85-100      | Low      | Nice to have polish      |
