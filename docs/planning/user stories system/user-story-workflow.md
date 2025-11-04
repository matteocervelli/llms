# User Story Writing Workflow

## Phase 1: Project Assessment Input
**Before writing stories, capture:**
- Target users/personas
- Core business objectives
- Key features/capabilities needed
- Success metrics

## Phase 2: Story Generation

### For Each Story:

**Step 1: Identify the User**
- Who specifically will use this?
- What's their role/context?

**Step 2: Define the Action**
- What capability do they need?
- What job are they trying to do?

**Step 3: Clarify the Value**
- Why does this matter to them?
- What outcome/benefit results?

**Step 4: Write Acceptance Criteria**
- What's the precondition? (Given...)
- What action triggers it? (When...)
- What's the expected result? (Then...)
- Any edge cases?

**Step 5: Validate with INVEST**
- Independent? Negotiable? Valuable? Estimable? Small? Testable?
- If no, split or refine

## Workflow Variations

### New Stories (Parallel)
1. Map all major features from assessment
2. Prioritize by user value
3. Write stories for top priority features
4. Review batch for dependencies/gaps

### Iteration/New Features
1. Reference existing stories for context
2. Identify what's different/additional
3. Write new story following Steps 1-5
4. Check integration with existing features

## Key Questions Template

**Before writing:**
- What user problem does this solve?
- What's the minimum viable version?
- How will we know it's working?

**While writing:**
- Is this one job-to-be-done or multiple?
- Am I describing solution or need?
- Can I test this clearly?

## Standard User Story Template

```
As a [user type],
I want to [action/capability],
So that [benefit/value].

Acceptance Criteria:
- Given [context/precondition]
- When [action]
- Then [expected outcome]
```

## INVEST Quality Checklist

- **I**ndependent - Can be built separately
- **N**egotiable - Details can be discussed
- **V**aluable - Delivers clear user benefit
- **E**stimable - Team can size the effort
- **S**mall - Completable in one sprint
- **T**estable - Clear pass/fail criteria
