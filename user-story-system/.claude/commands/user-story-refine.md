---
description: Validate and refine existing user stories against INVEST criteria
argument-hint: <story-id|backlog|--all>
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Refine and Validate User Stories

Validate and refine existing user stories against INVEST criteria.

## Usage

```
/user-story-refine <story-id>
/user-story-refine backlog
/user-story-refine --all
```

## Examples

```
/user-story-refine US-0001
/user-story-refine backlog
/user-story-refine --all
```

## What it does

1. **Load Stories** - Loads specified story or multiple stories
2. **Validate** - Runs INVEST validation on each story
3. **Report Issues** - Presents validation issues with severity
4. **Suggest Fixes** - Provides specific, actionable suggestions
5. **Apply Fixes** - Optionally applies auto-fixes with user approval
6. **Regenerate** - Updates Markdown documentation

## Result

- Validation scores for each story
- List of issues found (critical/warnings)
- Specific fix suggestions
- Updated YAML files (if fixes applied)
- Regenerated Markdown documentation

---

Activate the **story-validator** skill to validate and refine user stories.

Use the `story-validator` skill located in `.claude/skills/story-validator/SKILL.md`.

## Parameters

- **story-id**: Specific story to validate (e.g., US-0001)
- **backlog**: Validate all stories with status "backlog"
- **--all**: Validate all stories regardless of status

## Validation Criteria (INVEST)

- **Independent** - Can be developed separately
- **Negotiable** - Open to discussion
- **Valuable** - Delivers business value
- **Estimable** - Can be estimated
- **Small** - Fits within a sprint (≤8 points)
- **Testable** - Has clear acceptance criteria

## Scoring

- **0-49**: Fail - Requires significant improvement
- **50-69**: Needs work - Has issues to address
- **70-84**: Good - Minor improvements possible
- **85-100**: Excellent - High quality story

## Auto-Fix Capabilities

The skill can automatically fix:
- Missing story points (estimates based on complexity)
- Empty "so that" benefits (generates from context)
- Incomplete acceptance criteria (adds standard scenarios)
- Vague descriptions (suggests clarifications)

## Workflow

The skill will:
1. Load specified story/stories from `stories/yaml-source/`
2. Run INVEST validation on each
3. Calculate overall score (0-100)
4. Identify specific issues by criterion
5. Suggest actionable fixes
6. Ask if you want to apply auto-fixes
7. Update YAML files if fixes applied
8. Regenerate Markdown documentation
9. Present summary report

## File References

- Skill: `.claude/skills/story-validator/SKILL.md`
- Script: `.claude/skills/story-validator/scripts/validate_story_invest.py`
- Stories: `stories/yaml-source/US-*.yaml`
- Config: `.claude/skills/user-story-generator/config/automation-config.yaml`

## Related Commands

- `/user-story-new` - Create new stories
- `/user-story-annotate` - Add technical context
- `/user-story-deps` - Check dependencies
- `/user-story-sprint` - Plan sprint
