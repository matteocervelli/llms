# Scoped Testing

After editing source files during implementation, run the narrowest test scope:

- Python: `uv run pytest tests/test_{module}.py -x -q` (not full suite)
- Turborepo: `pnpm turbo run test --filter={package}` (not all packages)
- Monorepo: only the affected package, not root

Don't run the full suite on every edit. Full suite is verified by CI.
