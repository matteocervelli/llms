# General Prompt for Implementing Feature-Implementer v2 Issues

## Overview

This prompt should be used when implementing any issue from the Feature-Implementer v2 milestone (#40-53). It provides a consistent approach to implementation with quality standards and best practices.

---

## General Implementation Prompt

```
I need you to implement GitHub issue #{issue-number} for the Feature-Implementer v2 architecture.

## Context

**Branch:** feature/implementer-v2
**Milestone:** Feature-Implementer v2 Architecture
**Issue URL:** https://github.com/matteocervelli/llms/issues/{issue-number}

## Reference Documentation

Before starting, review the following architecture documentation:
- docs/architecture/feature-implementer-v2.md (complete architecture)
- docs/architecture/agent-hierarchy.md (agent structure and relationships)
- docs/architecture/skills-mapping.md (36 skills catalog)
- docs/architecture/implementation-plan.md (implementation strategy)

## Implementation Requirements

1. **Read the Issue**
   - Use: gh issue view {issue-number}
   - Understand all tasks and acceptance criteria
   - Check dependencies on other issues

2. **Create/Update Files**
   - Follow the exact file paths specified in the issue
   - Use templates from architecture documentation
   - Maintain consistent structure and formatting

3. **Follow Standards**
   - **File Size:** Maximum 500 lines per file
   - **Type Hints:** All function parameters and returns
   - **Docstrings:** Google-style for all public functions
   - **Testing:** Skip tests for now (focus on implementation)
   - **Comments:** Explain complex logic, not obvious code

4. **Agent Configuration Structure**
   For agent files (.claude/agents/*.md):
   ```markdown
   # agent-name

   **Description:** Clear description of agent purpose

   **Model:** [haiku|sonnet|opus]

   **Tools:** List of tools (Read, Write, Edit, Bash, Grep, Glob, gh, git)

   **MCPs:** List of MCPs (github-mcp, context7-mcp, etc.)

   **Skills:**
   - skill-name-1 (auto-activates)
   - skill-name-2 (auto-activates)

   **Workflow:**
   1. Step 1
   2. Step 2
   ...

   **Output:** Output location or format

   **Success Criteria:**
   - Criterion 1
   - Criterion 2
   ```

5. **Skill Configuration Structure**
   For skill files (.claude/skills/*/SKILL.md):
   ```markdown
   # skill-name

   **Description:** Clear description of skill purpose

   **Activation:** [Automatically when...|On-demand via...]

   **Tools:** List of tools

   **MCPs:** List of MCPs (if any)

   **Resources:**
   - resource-file-1.md: Description
   - resource-file-2.py: Description

   **Provides:**
   - Capability 1
   - Capability 2
   - Capability 3

   **Used During:**
   - Context 1
   - Context 2
   ```

6. **Supporting Resources**
   Create supporting resource files as needed:
   - Checklists (*.md)
   - Templates (templates/*.md)
   - Scripts (scripts/*.py)
   - Guides (*-guide.md)

7. **Commit Standards**
   - Use conventional commits: `feat: implement issue #{issue-number} - {brief description}`
   - Reference the issue in commit message
   - Keep commits atomic (one issue = one commit)

## Implementation Steps

1. **Checkout branch** (if not already on it)
   ```bash
   git checkout feature/implementer-v2
   ```

2. **Read the issue**
   ```bash
   gh issue view {issue-number}
   ```

3. **Create all required files**
   - Agent configurations
   - Skill configurations
   - Supporting resources
   - Output directories

4. **Verify implementation**
   - All tasks checked off
   - All acceptance criteria met
   - Files follow standards
   - No syntax errors

5. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: implement issue #{issue-number} - {brief description}

   - Task 1
   - Task 2
   - Task 3

   Closes #{issue-number}"
   ```

6. **Push changes** (optional, save for final integration)
   ```bash
   git push origin feature/implementer-v2
   ```

## Quality Checklist

Before marking the issue complete, verify:

- [ ] All files created in correct locations
- [ ] All agent/skill configurations follow structure
- [ ] All supporting resources created
- [ ] File size ≤ 500 lines
- [ ] Type hints for all functions
- [ ] Google-style docstrings
- [ ] No syntax errors
- [ ] Consistent formatting
- [ ] References to architecture docs included
- [ ] Output directories created (if applicable)
- [ ] Commit message follows conventions
- [ ] Issue referenced in commit

## Deliverables

For each issue, provide:

1. **Implementation Summary**
   - Files created
   - Skills/agents configured
   - Resources added
   - Any deviations from plan (with justification)

2. **Commit Message**
   - Conventional commit format
   - Issue reference
   - Brief task list

3. **Next Steps**
   - Dependencies resolved (if any)
   - Next issue to implement
   - Any blockers or concerns

## Common Patterns by Issue Type

### Agent Configuration Issues (#41, #42, #47, #51, etc.)
1. Create `.claude/agents/{agent-name}.md`
2. Follow agent configuration structure
3. List all tools, MCPs, skills
4. Define workflow and success criteria
5. Create output directories if specified

### Skill Configuration Issues (#46, #48-50, etc.)
1. Create `.claude/skills/{skill-name}/SKILL.md`
2. Follow skill configuration structure
3. Create supporting resources (checklists, templates, scripts)
4. Define activation, tools, provides, used during
5. Include usage examples

### Infrastructure Issues (#40, #52, etc.)
1. Create core configuration files
2. Define invocation patterns
3. Test integration points
4. Document usage

### Integration Issues (#53)
1. Verify all previous issues complete
2. Test end-to-end workflow
3. Update documentation
4. Create migration guide

## Example Usage

### For Issue #40 (Core Prompt Infrastructure):
```
I need you to implement GitHub issue #40 for the Feature-Implementer v2 architecture.

[Include full prompt from above]

Issue #40 involves:
- Creating .claude/prompts/feature-implementer-main.md
- Updating /feature-implement slash command
- Testing invocation

Please proceed with implementation following the steps above.
```

### For Issue #41 (Analysis Specialist Agent):
```
I need you to implement GitHub issue #41 for the Feature-Implementer v2 architecture.

[Include full prompt from above]

Issue #41 involves:
- Creating analysis-specialist agent
- Creating 3 skills (requirements-extractor, security-assessor, tech-stack-evaluator)
- Creating output directory /docs/implementation/analysis/

Please proceed with implementation following the steps above.
```

## Notes

- **No Testing:** Skip test implementation for now (focus on feature code only)
- **Single Branch:** All work on `feature/implementer-v2`
- **Atomic Commits:** One issue = one commit
- **Reference Architecture:** Always refer to architecture docs for structure and standards
- **Ask for Clarification:** If anything is unclear, ask before implementing

---

**Usage:** Copy this entire prompt and customize the issue number when implementing each issue from the Feature-Implementer v2 milestone.
