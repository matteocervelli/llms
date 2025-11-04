---
description: Review PR before merging to check for best practices and potential issues
argument-hint: <pr-number>
allowed-tools: gh, git, filesystem, security-scan
---

# PR Review Before Merge: $ARGUMENTS

Comprehensive pre-merge review to validate code quality, security, best practices, and readiness for production.

## Phase 1: PR Metadata Analysis

```bash
# Get PR details
!gh pr view $ARGUMENTS --json title,body,author,reviewers,state,isDraft,mergeable,statusCheckRollup,headRefName,baseRefName

# Check review status
!gh pr reviews $ARGUMENTS
```

### Initial Validation Checklist

- [ ] PR is not in draft status
- [ ] PR has proper title and description
- [ ] No merge conflicts
- [ ] CI/CD checks are passing
- [ ] Required approvals are present
- [ ] Target branch is correct (usually main/master)

**BLOCKER**: If any critical items fail, stop and report issues before continuing.

## Phase 2: Changed Files Analysis

```bash
# Get PR diff
!gh pr diff $ARGUMENTS

# List changed files with stats
!gh pr view $ARGUMENTS --json files
```

### File-Level Checks

**Size Validation** (per project 500-line limit):
```bash
# Check for oversized files
!gh pr diff $ARGUMENTS --name-only | while read file; do
    lines=$(git show HEAD:"$file" 2>/dev/null | wc -l)
    if [ "$lines" -gt 500 ]; then
        echo "⚠️  WARNING: $file has $lines lines (limit: 500)"
    fi
done
```

**Modular Design**:
- Each file should have single responsibility
- Check for proper separation of concerns
- Verify clean interfaces between modules

## Phase 3: Code Quality Review

```bash
# Run comprehensive quality checks
!echo "🔍 Running code quality analysis..."
```

### Language-Specific Quality Checks

**Python Projects**:
```bash
# Formatting
!if command -v black &> /dev/null; then echo "→ Formatting (black):" && black --check . 2>&1 | head -20; fi

# Linting
!if command -v flake8 &> /dev/null; then echo "→ Linting (flake8):" && flake8 src/ tests/ 2>&1 | head -20; fi

# Type checking
!if command -v mypy &> /dev/null; then echo "→ Type checking (mypy):" && mypy src/ 2>&1 | head -20; fi

# Test coverage
!if command -v pytest &> /dev/null; then echo "→ Test coverage:" && pytest --cov=src --cov-report=term-missing 2>&1 | tail -10; fi
```

**JavaScript/TypeScript Projects**:
```bash
# Linting
!if [ -f "package.json" ]; then echo "→ Linting (eslint):" && npm run lint 2>&1 | head -20 || echo "No lint script"; fi

# Type checking
!if [ -f "tsconfig.json" ]; then echo "→ Type checking (tsc):" && tsc --noEmit 2>&1 | head -20; fi

# Tests
!if [ -f "package.json" ]; then echo "→ Running tests:" && npm test 2>&1 | tail -20 || echo "No test script"; fi
```

### Quality Assessment Criteria

- **Code Style**: Consistent formatting, proper naming conventions
- **Type Safety**: All functions have type hints/annotations
- **Test Coverage**: Minimum 80% coverage for new/modified code
- **Documentation**: All public functions have docstrings
- **Complexity**: No overly complex functions (cyclomatic complexity < 10)

## Phase 4: Security & Vulnerability Scan

```bash
!echo "🔒 Running security analysis..."
```

**Python Security**:
```bash
# Check for hardcoded secrets
!git diff origin/main..HEAD | grep -iE "(password|secret|key|token|api_key)" || echo "✓ No obvious secrets found"

# Dependency vulnerabilities
!if command -v safety &> /dev/null; then echo "→ Dependency scan (safety):" && safety check; fi
!if command -v bandit &> /dev/null; then echo "→ Security scan (bandit):" && bandit -r src/ -ll; fi
```

**JavaScript/TypeScript Security**:
```bash
# NPM audit
!if [ -f "package.json" ]; then echo "→ Dependency audit:" && npm audit --production; fi

# Check for secrets in diff
!git diff origin/main..HEAD | grep -iE "('|\")?(password|secret|key|token|api[_-]?key)('|\")?\s*[:=]" || echo "✓ No hardcoded secrets detected"
```

**Security Checklist**:
- [ ] No hardcoded credentials or API keys
- [ ] No vulnerable dependencies
- [ ] Proper input validation
- [ ] Secure error handling (no sensitive data in errors)
- [ ] Authentication/authorization properly implemented

## Phase 5: Best Practices Validation

### Commit Message Quality

```bash
# Review commit messages
!gh pr view $ARGUMENTS --json commits --jq '.commits[] | "\(.messageHeadline)"'
```

**Commit Standards**:
- Follow conventional commits format (feat:, fix:, docs:, etc.)
- Clear, descriptive messages
- Reference issues where applicable
- Atomic commits (one logical change per commit)

### Code Organization

**Check for**:
- Single Responsibility Principle
- Dependency Injection (no global imports for services)
- Interface-first design
- Clean Architecture (layer separation)
- Proper error handling

### Documentation Review

```bash
# Check for README or documentation updates
!git diff origin/main..HEAD --name-only | grep -iE "(readme|docs?/)" || echo "ℹ️  No documentation files changed"
```

**Documentation Checklist**:
- [ ] README updated if public API changed
- [ ] API documentation for new public functions
- [ ] Usage examples for complex functionality
- [ ] Migration notes if breaking changes
- [ ] CHANGELOG.md updated

## Phase 6: Test Coverage Analysis

```bash
# Check if tests were added for new functionality
!echo "📊 Analyzing test coverage..."
!git diff origin/main..HEAD --name-only | grep -E "^(src/|lib/)" | wc -l
!git diff origin/main..HEAD --name-only | grep -E "^tests?/" | wc -l
```

**Test Requirements**:
- [ ] Unit tests for new functions
- [ ] Integration tests for new features
- [ ] Tests cover edge cases and error conditions
- [ ] No skipped or disabled tests without justification
- [ ] Test naming follows conventions

### Test Quality Checks

```bash
# Run tests if available
!if command -v pytest &> /dev/null; then pytest -v --tb=short 2>&1 | tail -30; fi
!if [ -f "package.json" ] && npm run test &>/dev/null; then npm test 2>&1 | tail -30; fi
```

## Phase 7: Performance & Impact Assessment

### Code Performance

**Check for**:
- N+1 query problems
- Inefficient algorithms (O(n²) or worse)
- Memory leaks or resource leaks
- Proper use of caching
- Database query optimization

### Breaking Changes

```bash
# Check for potential breaking changes
!git diff origin/main..HEAD | grep -E "^-.*def |^-.*function |^-.*class " || echo "ℹ️  No obvious function/class removals"
```

**Breaking Change Checklist**:
- [ ] No removed public APIs without deprecation
- [ ] Backward compatibility maintained
- [ ] Migration path provided if breaking
- [ ] Version bump appropriate (semver)

## Phase 8: Final Review Summary

### Generate Comprehensive Report

Copy this template and fill in based on findings:

```markdown
# PR Review Summary: #$ARGUMENTS

## 🎯 Overview
- **PR Title**: [title]
- **Author**: [author]
- **Target Branch**: [base] ← [head]
- **Changed Files**: [count]
- **Lines Added/Removed**: +[added] -[removed]

## ✅ Passing Checks
- [list all passing criteria]

## 🚫 Blockers (MUST FIX)
- [ ] [Critical issue 1]
- [ ] [Critical issue 2]

**Cannot merge until these are resolved.**

## ⚠️ Warnings (SHOULD FIX)
- [ ] [Important issue 1]
- [ ] [Important issue 2]

**Strongly recommended to address before merging.**

## 💡 Suggestions (NICE TO HAVE)
- [Improvement 1]
- [Improvement 2]

**Optional enhancements for consideration.**

## 📊 Metrics
- **Code Quality Score**: [X/10]
- **Test Coverage**: [X%]
- **Security Score**: [Pass/Fail]
- **Documentation**: [Complete/Incomplete]

## 🎯 Recommendation

[Choose one]:
✅ **APPROVE**: Ready to merge
⚠️ **APPROVE WITH NOTES**: Can merge, but address warnings
❌ **REQUEST CHANGES**: Blockers must be fixed

## 📝 Reviewer Notes
[Additional context, concerns, or praise]
```

## Quick Reference: Common Issues

### Anti-Patterns to Flag

**Code Smells**:
- Functions > 50 lines
- Files > 500 lines
- Deeply nested code (> 3 levels)
- Duplicate code
- God objects/classes
- Magic numbers without explanation

**Security Issues**:
- Hardcoded secrets
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insufficient input validation
- Improper error handling revealing sensitive info

**Test Issues**:
- No tests for new functionality
- Tests that don't actually test anything
- Overly complex test setup
- Tests depending on external services without mocks

**Documentation Issues**:
- Missing docstrings for public APIs
- Outdated comments
- No usage examples
- Breaking changes not documented

## Advanced Checks (Optional)

### Dependency Analysis

```bash
# Check for new dependencies
!git diff origin/main..HEAD requirements.txt package.json 2>/dev/null | grep "^+" | grep -v "^+++" || echo "ℹ️  No dependency changes"
```

### Performance Profiling

```bash
# If performance tests exist
!if [ -f "tests/performance" ]; then echo "Running performance tests..." && pytest tests/performance/ -v; fi
```

### Accessibility (for UI changes)

```bash
# Check for UI component changes
!git diff origin/main..HEAD --name-only | grep -iE "(component|ui|view)" && echo "⚠️  UI changes detected - verify accessibility"
```

---

## Usage Examples

### Basic usage
```bash
/pr-review-merge 42
```

### With specific focus
```bash
# Focus on security
/pr-review-merge 42  # Then ask: "Focus security analysis on authentication changes"

# Focus on performance
/pr-review-merge 42  # Then ask: "Deep dive into performance implications"
```

## Best Practices for Reviewers

1. **Be Thorough but Efficient**: Use automated checks first, then manual review
2. **Focus on Architecture**: Code style can be auto-fixed; design decisions matter more
3. **Ask Questions**: If something is unclear, ask rather than assume
4. **Praise Good Work**: Acknowledge well-written code, not just problems
5. **Provide Context**: Explain *why* something should change
6. **Be Constructive**: Suggest improvements, don't just criticize
7. **Check Tests**: Good tests are as important as good code
8. **Verify Documentation**: Future maintainers will thank you

## Integration with Other Commands

- **Before review**: `/code-analyze-quality` for quick quality check
- **If issues found**: `/pr-analyze-failure` to fix CI/CD problems
- **After approval**: Standard merge process via GitHub UI or gh CLI

---

**Remember**: The goal is to maintain code quality and prevent issues in production, not to be pedantic. Use judgment on what's truly important vs. what's personal preference.