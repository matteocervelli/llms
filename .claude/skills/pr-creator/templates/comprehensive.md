## Feature Summary

[2-3 sentence overview of what was implemented and why it matters]

## Implementation Details

**Architecture**: [Pattern used - e.g., service layer, repository pattern]

**Key Components**:

- **ComponentName**: [Purpose and responsibility]
- **AnotherComponent**: [Purpose and responsibility]

**Dependencies Added**:

- `package-name==version`: [Why it was added]

**Files Modified/Added**:

- `src/module/file.py`: [What changed]
- `tests/test_module.py`: [Tests added]
- `docs/guides/guide.md`: [Documentation]

## Security & Performance

### Security

- ✅ Input validation at all entry points
- ✅ Authentication/authorization implemented
- ✅ Output sanitization (XSS prevention)
- ✅ Parameterized queries (SQL injection prevention)
- ✅ Rate limiting configured
- ✅ Secrets managed securely (no hardcoded credentials)
- ✅ Security tests passing

### Performance

- ✅ Performance targets met
- ✅ Caching strategy implemented
- ✅ Database queries optimized
- ✅ Async operations where appropriate

**Performance Metrics**:

- Response time: [actual vs target]
- Throughput: [requests per second]

## Testing

### Coverage

- **Unit Tests**: [X]% coverage
- **Integration Tests**: [X endpoints/flows covered]
- **Security Tests**: [what's tested]
- **Performance Tests**: [benchmarks met]

### Test Results

```bash
pytest --cov=src --cov-report=term
Coverage: 92%
Tests: 156 passed, 0 failed
```

## Documentation

- ✅ Implementation docs: `docs/implementation/issue-XXX.md`
- ✅ User guide: `docs/guides/guide.md`
- ✅ API documentation: `docs/api/api.md`
- ✅ CHANGELOG updated with v[X.Y.Z] entry

## Breaking Changes

[If yes, list them with migration instructions]
[If no, state: "None"]

**Migration Required**:
[If yes, provide step-by-step migration guide]
[If no, state: "None required"]

## Configuration Changes

**New Environment Variables**:

```bash
FEATURE_VAR=value
```

## Validation Results

### Code Quality

- ✅ Black formatting: Passed
- ✅ mypy type checking: Passed
- ✅ flake8 linting: Passed

### Security Scan

- ✅ Dependency vulnerabilities: None found
- ✅ Secrets detection: No secrets in code

## Test Plan for Reviewers

### Code Review

- [ ] Review code changes for quality and maintainability
- [ ] Check adherence to project coding standards
- [ ] Verify error handling is comprehensive
- [ ] Ensure no security vulnerabilities

### Testing

- [ ] Run test suite: `pytest`
- [ ] Verify all tests pass
- [ ] Check test coverage meets 80%+ threshold

### Manual Testing

- [ ] Test happy path scenarios
- [ ] Test error scenarios
- [ ] Test edge cases

## Acceptance Criteria

From issue #XXX:

- [x] Criterion 1
- [x] Criterion 2
- [x] Criterion 3

All acceptance criteria met ✅

## Related Issues/PRs

- Closes #XXX
- Related to #YYY
- Blocks #ZZZ

## Deployment Notes

**Deploy Requirements**:

- Run database migrations: `alembic upgrade head`
- Update environment variables in production

**Rollback Plan**:

- Revert database migrations: `alembic downgrade -1`
- Restore previous environment variables
