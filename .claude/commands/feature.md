---
description: Develop new feature with security-by-design and performance optimization
allowed-tools: [gh, git, sequential-thinking-mcp, context7-mcp]
---

# Develop Feature: $ARGUMENTS

## Analysis Phase

```bash
!gh issue view $ARGUMENTS
!git checkout -b feature/$ARGUMENTS
```

Use sequential-thinking-mcp to:

1. Analyze requirements and acceptance criteria
2. Design solution with security considerations (auth, input validation, data protection)
3. Plan performance targets (response times, resource usage)
4. Define layered architecture (interfaces → core → implementations)

When understood the implementation plan, get the tech stack from @docs/TECH-STACK.md.
Then, use context7-mcp to fetch latest documentation for required tools for the specific feature, also considering the tech stack from @docs/TECH-STACK.md

## Design Phase

Create component design following:

- **Security-by-design**: Input validation, authentication flows, data encryption
- **Performance-first**: Caching strategy, query optimization, resource management
- **Modularity**: Keep components under 500 lines, clear separation of concerns

Document architecture decision in `docs/architecture/ADR/` for architectural decisions

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
!git add . && git commit -m "feat: implement $ARGUMENTS && git push origin feature/$ARGUMENTS

- Implementation: [brief description of solution]
- Security: [auth requirements, input validation, data protection]
- Performance: [caching, optimization, response times]
- Testing: [coverage %, integration tests, security tests]

Features:
- [list key capabilities]

Closes #$ARGUMENTS"

!gh pr create --title "feat: $ARGUMENTS" --body "
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

Closes #$ARGUMENTS"
```

## Final Steps

- Update @CHANGELOG.md with feature addition and increase versioning accordingly
- Update user documentation and publish if needed
- Monitor feature adoption and performance post-deployment
