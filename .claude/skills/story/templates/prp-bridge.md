# Story-to-PRP Bridge

Maps user stories to PRP sections for the `/prp-generator` skill.

## Mapping: Story Fields → PRP Sections

### Stories → Requirements Reference

```
acceptance_criteria → Functional requirements
  - Each Given/When/Then becomes a testable requirement
  - Group by feature area

story_points (sum) → Complexity assessment
  - 1-8 total points: Low complexity
  - 9-20 total points: Medium complexity
  - 21+ total points: High complexity

blocked_by relationships → Architecture constraints
  - Dependencies suggest component boundaries
  - Blocking chains suggest implementation phases
```

### Stories → Architecture Design

```
personas → User context and access patterns
  - Different personas may need different routes/views
  - Role-based access maps to middleware/auth

feature areas (from story titles) → Components
  - Each distinct area maps to a module or service
  - Shared acceptance criteria suggest shared utilities

data entities (from given/then) → Data models
  - "database has X" / "X exists" → model/schema needed
  - "field equals value" → validation rule
```

### Stories → Implementation Plan

```
Story dependencies → Phase ordering
  - Stories with no blocked_by → Phase 1 (Foundation)
  - Stories blocked by Phase 1 → Phase 2 (Core)
  - Integration stories → Phase 3

Story points → Phase effort estimation
  - Phase 1: Foundation stories (data models, config)
  - Phase 2: Core stories (business logic)
  - Phase 3: Integration stories (API, wiring)
  - Phase 4: Testing (from acceptance criteria)
  - Phase 5: Deployment
```

### Stories → Testing Strategy

```
acceptance_criteria → Test cases (1:1 mapping)
  - given → test setup / fixtures
  - when → action under test
  - then → assertion

Story with "API" or "endpoint" in criteria → Integration tests needed
Story with "navigate" or "click" in criteria → E2E tests needed
Story with data validation criteria → Unit tests + parametrize
```

## Invocation

When composing PRP input, pass to `/prp-generator`:

1. **Story list** with IDs, titles, points, and all acceptance criteria
2. **Dependency graph** showing blocking relationships
3. **Personas involved** and their goals
4. **Complexity assessment** (sum of story points)
5. **Feature area groupings** derived from story titles

The PRP generator handles the actual document structure. This bridge just transforms story data into PRP-ready input.
