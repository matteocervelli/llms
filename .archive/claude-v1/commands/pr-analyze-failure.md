---
description: Fix PR failures from CI/CD bots and automated tests
allowed-tools: gh, git, filesystem
---

# Fix PR Failures: $ARGUMENTS

## Analysis Phase

```bash
# Get PR details and CI status
!gh pr view $ARGUMENTS --json title,body,state,statusCheckRollup
!gh pr checks $ARGUMENTS --watch
```

Analyze CI/CD failures:

- **Build failures**: Compilation errors, dependency issues
- **Test failures**: Unit, integration, security test failures  
- **Linting/Format**: Code quality violations
- **Security scans**: Vulnerability alerts, dependency issues
- **Performance**: Load testing, coverage threshold failures

## Quick Fix Strategy

```bash
# Checkout the PR branch
!gh pr checkout $ARGUMENTS
```

### Common Fix Patterns

**Build/Dependency Issues:**

```bash
# Clean install and rebuild
!rm -rf node_modules package-lock.json || rm -rf __pycache__ .pytest_cache
!npm ci || pip install -r requirements.txt
!npm run build || python -m build
```

**Test Failures:**

```bash
# Run specific failing tests locally
!npm run test -- --verbose || pytest -v --tb=short
!npm run test:integration || pytest tests/integration/
```

**Code Quality Issues:**

```bash
# Auto-fix linting and formatting
!npm run lint -- --fix || black . && isort . && flake8 .
!npm run format || prettier --write .
!npm run typecheck || mypy .
```

**Security Issues:**

```bash
# Fix dependency vulnerabilities
!npm audit fix || safety check && pip-audit --fix
!npx audit-ci --moderate || bandit -r src/
```

## Implementation Phase

Based on CI failure type, implement targeted fixes:

### 1. Test Failures

- **Unit Tests**: Fix broken logic, update mocks, handle edge cases
- **Integration Tests**: Update API contracts, fix database setup
- **Security Tests**: Address input validation, auth issues

### 2. Performance Issues  

- **Coverage**: Add missing test cases to reach threshold
- **Performance**: Optimize slow queries, reduce response times
- **Memory**: Fix memory leaks, optimize resource usage

### 3. Quality Issues

- **TypeScript**: Fix type errors, add missing types
- **Linting**: Address code style violations
- **Documentation**: Update JSDoc, README, API docs

## Validation Phase

```bash
# Verify all checks pass locally
!npm run lint && npm run typecheck && npm run test || flake8 . && mypy . && pytest
!npm run build || python -m build

# Security verification
!npm audit || safety check
```

## Deploy Fix

```bash
!git add .
!git commit -m "fix(ci): resolve PR #$ARGUMENTS CI/CD failures

- Fixed: [specific issue description]
- Tests: [test fixes applied]
- Security: [security issues resolved]  
- Performance: [optimizations made]

CI Status: All checks passing"

!git push
```

## Monitor CI Progress

```bash
# Watch CI/CD pipeline progress
!gh pr checks $ARGUMENTS --watch

# Get final status
!gh pr view $ARGUMENTS --json statusCheckRollup
```

## Auto-Merge if Ready

```bash
# Check if all requirements met and auto-merge if configured
!gh pr merge $ARGUMENTS --auto --squash || echo "Manual merge required"
```

## Common Fixes Quick Reference

### JavaScript/TypeScript

```bash
# Dependencies
!npm audit fix && npm run build

# Tests  
!npm run test -- --updateSnapshot
!npm run test:coverage -- --coverageThreshold='{"global":{"branches":80}}'

# Quality
!npx eslint . --fix && npx prettier --write .
!npx tsc --noEmit
```

### Python

```bash
# Dependencies
!pip install -r requirements.txt && safety check

# Tests
!pytest --cov=src --cov-fail-under=80
!pytest --security

# Quality  
!black . && isort . && flake8 .
!mypy src/
```

### Docker/Infrastructure

```bash
# Container build
!docker build -t test-image .
!docker run --rm test-image npm test

# Infrastructure validation
!terraform validate && terraform plan
!ansible-playbook --check playbook.yml
```

---

**Focus**: Quickly identify and fix CI/CD pipeline failures to get PRs mergeable.