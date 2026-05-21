---
name: code-review
description: Claude-native review of code for quality, structure, naming, and maintainability (no external AI). Use when reviewing a file or diff for code quality before committing. Trigger on "review this code", "code review", "is this well-written". For security, use /security-verify; for companion-AI review, use /review.
allowed-tools: Read, Bash, Grep
---

# Code Review Skill

## Purpose

Code review focused on quality, structure, naming, and maintainability. For security reviews, use `/security-verify scan`.

## Quick Start

```bash
/code-review <file-path>
```

## Review Categories

### 1. Code Quality (Critical)

**File Organization**

- [ ] File size <= 500 lines
- [ ] Single responsibility
- [ ] Clear module structure

**Naming**

- [ ] Self-documenting names
- [ ] Verbs for functions, nouns for data
- [ ] Consistent naming style (snake_case/camelCase)
- [ ] No abbreviations

**Type Hints (Python) / Types (TS)**

- [ ] All function parameters typed
- [ ] Return types specified
- [ ] No implicit `Any`

**Docstrings/Comments**

- [ ] Google-style docstrings on public API
- [ ] Comments explain WHY, not WHAT
- [ ] No commented-out code

### 2. Error Handling

- [ ] Specific exception types
- [ ] No bare `except:`
- [ ] Clear error messages
- [ ] Cleanup in finally/with blocks

### 3. Complexity

- [ ] Functions < 50 lines
- [ ] Cyclomatic complexity < 10
- [ ] Nesting depth < 4 levels
- [ ] No deep callback chains

### 4. Testing Readiness

- [ ] Dependencies injectable
- [ ] Side effects isolated
- [ ] Pure functions where possible

### 5. Style

- [ ] Consistent formatting
- [ ] Imports organized
- [ ] No unused imports/variables

## Review Output

```markdown
# Code Review: src/module.py

## Quality Score: 8/10

## Critical Issues (Must Fix)

- Line 45: Function `process_data` is 78 lines. Split into smaller functions.

## Important Issues (Should Fix)

- Line 23: Missing type hint on return value
- Line 67: Bare `except:` - specify exception type

## Suggestions

- Line 12: Consider extracting magic number 86400 to constant

## Strengths

- Clear function naming
- Good separation of concerns
```

## Common Issues Checklist

**Python**

- [ ] No mutable default arguments
- [ ] Using context managers for resources
- [ ] No string concatenation in loops
- [ ] Using generators for large datasets

**TypeScript**

- [ ] Strict mode enabled
- [ ] No `any` types
- [ ] Proper null checks
- [ ] No type assertions without reason

**General**

- [ ] No magic numbers (use constants)
- [ ] DRY - no duplicate code blocks
- [ ] Single return point (when reasonable)
- [ ] Clear control flow

### 6. Security (Stack-Specific)

**FastAPI/Python Backend**:

- [ ] Tenant ID from session middleware, never from request body
- [ ] Pydantic models with `extra = "forbid"`
- [ ] ORM-only queries (no string interpolation)
- [ ] Argon2id for passwords, Redis for sessions

**Jinja2/HTMX Frontend**:

- [ ] No `| safe` on user input (use `| sanitize_html`)
- [ ] CSP nonces on inline scripts
- [ ] CSRF token in forms and HTMX headers
- [ ] No internal IDs exposed (use hashids)

**PostgreSQL Database**:

- [ ] RLS enabled on tenant-scoped tables
- [ ] SSL required in connection string
- [ ] Separate roles (app/migration/readonly)

**For comprehensive security scan**: Run `/security-verify scan`.

## Integration

For comprehensive validation before commit:

1. `/code-review` - This skill (structure, quality)
2. `/security-verify scan` - Security issues
3. `/pre-commit` - Full validation suite
