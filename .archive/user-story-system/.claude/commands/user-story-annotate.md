---
description: Add technical annotations, implementation hints, and effort estimates to user stories
argument-hint: <story-id|--all>
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Add Technical Context to User Stories

Add technical annotations, implementation hints, and effort estimates to user stories.

## Usage

```
/user-story-annotate <story-id>
/user-story-annotate --all
```

## Examples

```
/user-story-annotate US-0001
/user-story-annotate US-0001 US-0002 US-0003
/user-story-annotate --all
```

## What it does

1. **Analyze Requirements** - Reviews story details and acceptance criteria
2. **Identify Tech Stack** - Determines relevant technologies
3. **Generate Hints** - Provides specific implementation guidance
4. **List Components** - Identifies affected system components
5. **Estimate Effort** - Provides realistic time estimates
6. **Assess Complexity** - Rates complexity (low/medium/high)
7. **Identify Risks** - Highlights technical challenges
8. **Update Story** - Adds annotations to YAML file
9. **Regenerate Docs** - Updates Markdown documentation

## Result

- Technical context added to story YAML
- Implementation hints for developers
- Component impact analysis
- Effort estimation and complexity rating
- Risk identification
- Updated Markdown documentation

---

Activate the **technical-annotator** skill to add technical context to user stories.

Use the `technical-annotator` skill located in `.claude/skills/technical-annotator/SKILL.md`.

## Parameters

- **story-id**: One or more story IDs to annotate (e.g., US-0001)
- **--all**: Annotate all stories in the system

## Technical Annotations Include

### 1. Tech Stack
Technologies needed for implementation:
- Frontend (React, Vue, Angular, TypeScript)
- Backend (FastAPI, Django, Express, Node.js)
- Database (PostgreSQL, MongoDB, Redis)
- Infrastructure (Docker, Kubernetes, AWS)
- Testing (pytest, Jest, Cypress)

### 2. Implementation Hints
Specific guidance like:
- "Use FastAPI dependency injection for database sessions"
- "Implement OAuth2 password flow with JWT tokens"
- "Create React hook for authentication state"
- "Add database migration for new tables"

### 3. Affected Components
List of files that will be:
- **Created**: New files to implement
- **Modified**: Existing files to change
- **Shared**: Common utilities or services

### 4. Effort Estimation
Realistic time estimates:
- Small (1-2 points): 4-8 hours
- Medium (3-5 points): 1-2 days
- Large (8 points): 3-4 days
- Includes implementation, testing, and documentation time

### 5. Complexity Assessment
- **Low**: Simple CRUD, straightforward UI
- **Medium**: Moderate business logic, some integration
- **High**: Complex logic, multiple integrations, performance considerations

### 6. Risk Identification
Potential challenges:
- Performance concerns
- Security requirements
- Third-party dependencies
- Data migration issues
- Testing complexity

## Workflow

The skill will:
1. Load story from `stories/yaml-source/{story-id}.yaml`
2. Analyze story requirements and acceptance criteria
3. Check project context (tech stack, existing patterns)
4. Identify relevant technologies
5. Generate 3-5 specific implementation hints
6. List affected components with create/modify status
7. Estimate effort based on story points and complexity
8. Assess complexity level
9. Identify technical risks and challenges
10. Update story YAML with technical section
11. Regenerate Markdown documentation
12. Present annotation summary

## File References

- Skill: `.claude/skills/technical-annotator/SKILL.md`
- Script: `.claude/skills/user-story-generator/scripts/generate_story_from_yaml.py`
- Stories: `stories/yaml-source/US-*.yaml`
- Config: `.claude/skills/user-story-generator/config/automation-config.yaml`

## Context Sources

The skill checks:
- Project documentation (TECH-STACK.md, README.md)
- Configuration files (package.json, requirements.txt)
- Existing story patterns
- Codebase structure

## Related Commands

- `/user-story-new` - Create new stories (includes auto-annotation)
- `/user-story-refine` - Validate story quality
- `/user-story-deps` - Analyze dependencies
- `/user-story-sprint` - Plan sprint
