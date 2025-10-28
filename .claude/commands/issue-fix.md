---
description: Fix bugs and resolve problems from GitHub issues with security and performance validation
allowed-tools: [gh, git, sequential-thinking-mcp]
---

# Fix Bug from Issue: $ARGUMENTS

**💡 Tip:** For safer planning, activate Plan Mode (press Shift+Tab twice) before running this command to review the fix strategy before implementation.

## Analysis Phase

```bash
!gh issue view $ARGUMENTS
!git checkout -b fix/issue-$ARGUMENTS
```

Use sequential-thinking-mcp to:

1. Understand the bug and identify root cause
2. Assess security implications (auth, input validation, data exposure)
3. Plan minimal fix with performance considerations
4. Identify testing strategy

## Implementation Phase

Implement fix following:

- **Security**: Validate inputs, secure error handling, no data leaks
- **Performance**: Measure impact, optimize queries if needed
- **Defensive**: Null checks, proper error boundaries

## Testing Phase

```bash
# Quality checks
!npm run lint && npm run typecheck || flake8 . && mypy .
!npm run test || pytest
```

Create tests for:

- Bug reproduction (verify fix works)
- Security edge cases (malicious inputs)
- Performance regression (response times)
- Integration scenarios

## Validation Checkpoint

**Test the fix in development and confirm:**

1. Original bug is resolved
2. No regressions in existing functionality  
3. Performance impact acceptable
4. Security measures working

## Deploy Phase

```bash
!git add . && git commit -m "fix: resolve issue $ARGUMENTS

- Root cause: [brief description]
- Security: [input validation/auth preserved/no data exposure]
- Performance: [within SLA/optimized/no regression]
- Testing: [unit/integration/security tests added]

Fixes #$ARGUMENTS"

!git push origin fix/issue-$ARGUMENTS
!gh pr create --title "fix: issue $ARGUMENTS" --body "Security-validated bug fix with performance testing. Fixes #$ARGUMENTS"
```

## Documentation

Update:

- `docs/implementation/` with fix details
- `docs/developers/TROUBLESHOOTING.md` if needed
- `docs/architecture/` docs if structural changes
- `docs/guides/` docs if user guide changes

## Final Steps

- Update @CHANGELOG.md with bug fix addition and increase versioning accordingly
- Update user documentation and publish if needed
- Monitor bug fix adoption and performance post-deployment
