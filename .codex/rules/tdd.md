# TDD Rules

Default workflow for all implementation tasks. Only skip if user explicitly requests otherwise.

## Red-Green-Refactor Cycle

1. Write test cases FIRST (happy path, edge cases, error handling)
2. Run tests — confirm they FAIL (red phase)
3. Implement minimum code to make ONE test pass at a time
4. After each change, run fast test suite (`-m "not integration and not e2e"`) — not just new tests; full suite runs on CI
5. If any test fails, fix immediately before proceeding
6. After all tests pass, refactor for clarity without breaking tests
7. Run pre-commit validation

## Non-Negotiable

- Never write implementation before tests exist
- Never skip the red phase (tests must fail first)
- If you catch yourself implementing first, STOP and write tests
- Run fast test suite (`-m "not integration and not e2e"`) after every implementation change, not just new tests; full suite runs on CI
