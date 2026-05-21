# Dependency Rules

## Principle: Prefer Zero

- Can you build it in <100 lines? Build it
- Standard library first, always
- External deps = external failure modes
- Every import is technical debt

## When You Must Depend

- Justify in code: `# Using X because [specific reason]`
- Pin exact versions
- Have a fallback plan
- Mock in tests, integrate in staging

## Anti-Patterns

- Don't add library to save 10 lines
- Don't use frameworks for simple scripts
- Don't assume "popular" = right for you

For framework/tool adoption (LangChain, ORMs, auth libs, infra components): `docs/tool-evaluation.md`
