# Safety Rules

Non-negotiable.

## Testing

- Never skip tests to close session
- Never mock tests to fake passing
- All new code needs tests before commit
- Run fast test suite locally after each feature; full suite verified by CI before merge

## Attribution

- Never add "Co-Authored-By" lines to commits, PRs, or issues
- Never add "Generated with Claude" watermarks
- No AI attribution in any form

## Destructive Changes

- Never make destructive changes (database drops, file deletions, config overwrites) without asking user first
- Suggest a backup step before any destructive operation
- When encountering unfamiliar state (files, branches, configs), investigate before overwriting
