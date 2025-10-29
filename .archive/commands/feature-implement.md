---
description: LEGACY VERSION - Original 183-line feature-implement command (replaced by 15-line version)
allowed-tools: [gh, git, sequential-thinking-mcp, context7-mcp]
argument-hint: <issue-number> [create-branch:true|false]
---

# LEGACY: Implement Feature from Issue #$1

**⚠️ This is the original 183-line version, preserved for reference and comparison.**
**✅ Current version: `feature-implement.md` (15 lines, delegates to feature-implementer agent)**

---

## Parameter Validation

```bash
# Validate required parameters
if [ -z "$1" ]; then
  echo "Error: Issue number is required"
  echo "Usage: /feature <issue-number> [create-branch:true|false]"
  exit 1
fi

ISSUE_NUMBER="$1"
CREATE_BRANCH="${2:-true}"
```

## Analysis Phase

```bash
!gh issue view $1

# Conditionally create feature branch
if [ "$CREATE_BRANCH" = "true" ]; then
  !git checkout -b feature/$1
else
  echo "Skipping branch creation (CREATE_BRANCH=$CREATE_BRANCH)"
fi
```

Use sequential-thinking-mcp to:

1. Analyze requirements and acceptance criteria
2. Design solution with security considerations (auth, input validation, data protection)
3. Plan performance targets (response times, resource usage)
4. Define layered architecture (interfaces → core → implementations)

When understood the implementation plan, get the tech stack from @docs/TECH-STACK.md.
Then, use context7 to fetch latest documentation for required tools for the specific feature, also considering the tech stack from @docs/TECH-STACK.md

## Design Phase

**⚠️ IMPORTANT: Create a complete design plan before implementation. Do NOT start coding until this plan is reviewed and approved by the user.**

**💡 Tip**: For safer planning, users can activate Plan Mode (press Shift+Tab twice) before running this command.

Use sequential-thinking-mcp with extended thinking to create a comprehensive design:

Create component design following:

- **Security-by-design**: Input validation, authentication flows, data encryption
- **Performance-first**: Caching strategy, query optimization, resource management
- **Modularity**: Keep components under 500 lines, clear separation of concerns

Your design document should include:

1. **Architecture Overview**: Components, layers, and their dependencies
2. **Data Flow**: How data moves through the system
3. **Security Measures**: Authentication, authorization, input validation strategies
4. **Performance Strategy**: Caching mechanisms, optimization approaches, scaling considerations
5. **Testing Approach**: Unit test strategy, integration test coverage, security test scenarios
6. **Implementation Steps**: Ordered list of concrete development tasks

Document architecture decision in `docs/architecture/ADR/` for architectural decisions

### User Confirmation Required

After presenting the complete design, explicitly ask the user: "Should I proceed with implementation based on this design?"

## Model Switch

**Switching to Haiku model for efficient implementation.**

Use the faster Haiku model for the implementation phase to optimize for speed and cost while maintaining quality for code generation tasks.

## Implementation Phase

Implement following layered pattern:

1. Interface layer: Type definitions and contracts
2. Core layer: Business logic with security validation
3. Implementation layer: Data access and external services

**Security measures**:

- Validate all inputs at entry points
- Sanitize outputs to prevent XSS
- Use parameterized queries for database access
- Implement proper authentication/authorization

**Performance optimizations**:

- Add caching where appropriate
- Optimize database queries with proper indexing
- Implement async/await correctly
- Add rate limiting if needed

## Testing Phase

```bash
# Quality checks
!npm run lint && npm run typecheck || flake8 . && mypy .
!npm run test || pytest
!npm run build
```

Create comprehensive tests:

- **Unit tests**: 80%+ coverage, test business logic and edge cases
- **Integration tests**: API endpoints, database interactions
- **Security tests**: Input validation, authentication, authorization
- **Performance tests**: Response times, load testing if needed

## Validation Checkpoint

Test the feature in development and confirm:

1. All acceptance criteria met
2. Security measures working (auth, validation, no data leaks)
3. Performance within targets (response times, resource usage)
4. Integration with existing features smooth

## Documentation Phase

Update documentation:

- API documentation (OpenAPI/Swagger) for new endpoints
- `docs/implementation/` with feature implementation details
- `docs/guides/` with user guide for the feature
- `docs/architecture/sequence-diagrams/` for complex flows

## Deploy Phase

```bash
# Commit and push changes
if [ "$CREATE_BRANCH" = "true" ]; then
  BRANCH_NAME="feature/$1"
else
  BRANCH_NAME=$(git branch --show-current)
fi

!git add . && git commit -m "feat: implement issue #$1

- Implementation: [brief description of solution]
- Security: [auth requirements, input validation, data protection]
- Performance: [caching, optimization, response times]
- Testing: [coverage %, integration tests, security tests]

Features:
- [list key capabilities]

Closes #$1"

!git push origin $BRANCH_NAME

!gh pr create --title "feat: implement issue #$1" --body "
## Feature Summary
[Brief description]

## Security & Performance
- ✅ Security-by-design implemented
- ✅ Performance targets met
- ✅ Comprehensive testing completed

## Testing
- Unit tests: [coverage]%
- Integration tests: All endpoints covered
- Security tests: Auth, validation, no data exposure
- Performance tests: Within SLA

Closes #$1"
```

## Final Steps

- Update @CHANGELOG.md with feature addition and increase versioning accordingly
- Update user documentation and publish if needed
- Monitor feature adoption and performance post-deployment
