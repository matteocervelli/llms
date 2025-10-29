---
description: Implement new feature from GitHub issue with security-by-design and performance optimization
allowed-tools: [gh, git, sequential-thinking-mcp, context7-mcp]
argument-hint: <issue-number> [create-branch:true|false]
---

# Implement Feature from Issue #$1

**💡 Tip**: For safer planning, activate Plan Mode (press Shift+Tab twice) before running this command. This will let you review the complete design before implementation starts.

## Parameter Validation

```bash
# Validate required parameters
if [ -z "$1" ]; then
  echo "Error: Issue number is required"
  echo "Usage: /feature-implement <issue-number> [create-branch:true|false]"
  exit 1
fi

ISSUE_NUMBER="$1"
CREATE_BRANCH="${2:-true}"
```

## Invoke Feature-Implementer Agent

The **feature-implementer** agent will orchestrate the complete feature development workflow through five phases:

1. **Requirements Analysis**: Extract requirements, evaluate tech stack, analyze dependencies, assess security
2. **Architecture Design**: Design system architecture, data models, API contracts with user approval checkpoint
3. **Implementation**: TDD workflow with comprehensive testing (80%+ coverage target)
4. **Validation**: Quality gates, performance benchmarks, security validation
5. **Deployment**: Documentation updates, commit, PR creation, changelog

The agent delegates detailed expertise to specialized skills:
- **analysis** skill: Requirements extraction, tech stack evaluation, dependency analysis
- **design** skill: Architecture patterns, API design, data modeling
- **implementation** skill: TDD workflow, coding standards, testing patterns
- **validation** skill: Quality checks, performance validation, security scanning

**Security & Performance**: Security-by-design and performance-first principles applied throughout all phases.

**Quality Standards**: 80%+ test coverage, 500-line file limit, comprehensive documentation.

---

Use the **feature-implementer** agent to implement issue #$ISSUE_NUMBER (branch creation: $CREATE_BRANCH).
