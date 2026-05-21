---
description: Create user stories from a feature description following INVEST criteria
argument-hint: "[feature-description]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, AskUserQuestion
---

# Create New User Stories from Feature

Create user stories from a feature description following INVEST criteria.

## Usage

```
/user-story-new [feature-description]
```

## Examples

```
/user-story-new "Dashboard analytics for CEO"
/user-story-new "User authentication with OAuth"
/user-story-new
```

## What it does

1. **Feature Extraction** - Asks questions to extract feature details
2. **Story Generation** - Decomposes feature into 2-8 user stories
3. **Validation** - Validates stories against INVEST criteria
4. **Technical Annotation** - Adds tech context and implementation hints
5. **File Creation** - Creates YAML files and Markdown documentation
6. **GitHub Sync** - Creates GitHub issues (if enabled)

## Result

- YAML story files in `stories/yaml-source/`
- Markdown documentation in `stories/generated-docs/`
- GitHub issues (if enabled)
- Validation scores and technical annotations

---

Activate the **user-story-generator** skill to create user stories from the provided feature description.

Use the `user-story-generator` skill located in `.claude/skills/user-story-generator/SKILL.md`.

## Parameters

- **feature-description** (optional): Brief description of the feature. If omitted, the skill will ask for it interactively.

## Workflow

The skill will:
1. Accept or ask for feature description
2. Extract feature details through Q&A (persona, requirements, priority)
3. Show extracted JSON and ask for confirmation
4. Generate 2-8 user stories following INVEST criteria
5. Validate each story (silent qa-validator-agent)
6. Add technical annotations (silent technical-annotator-agent)
7. Create YAML source files
8. Generate Markdown documentation
9. Create GitHub issues if enabled
10. Present comprehensive summary

## File References

- Skill: `.claude/skills/user-story-generator/SKILL.md`
- Scripts: `.claude/skills/story-validator/scripts/validate_story_invest.py`, `.claude/skills/user-story-generator/scripts/generate_story_from_yaml.py`, `.claude/skills/user-story-generator/scripts/github_sync.py`
- Templates: `.claude/skills/user-story-generator/templates/story-template.yaml`, `.claude/skills/user-story-generator/templates/story-template.md`
- Config: `.claude/skills/user-story-generator/config/automation-config.yaml`, `.claude/skills/user-story-generator/config/personas.yaml`

## Related Commands

- `/user-story-refine` - Refine existing stories
- `/user-story-validate` - Validate story quality
- `/user-story-sprint` - Plan a sprint
- `/user-story-deps` - Analyze dependencies
