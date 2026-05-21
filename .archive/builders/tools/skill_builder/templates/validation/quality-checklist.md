# Code Quality Checklist

## Overview

This checklist ensures code meets quality standards before marking features complete. Use this in conjunction with automated tools (Black, mypy, flake8) for comprehensive quality assurance.

---

## Code Style and Formatting

### PEP 8 Compliance

- [ ] Code follows PEP 8 style guide
- [ ] Line length ≤ 88 characters (Black standard)
- [ ] Proper indentation (4 spaces, no tabs)
- [ ] Consistent naming conventions
- [ ] Proper whitespace usage

**Automated Check:**
```bash
black --check src/ tests/
flake8 src/ tests/
```

### Import Organization

- [ ] Imports grouped correctly (standard, third-party, local)
- [ ] Imports sorted alphabetically within groups
- [ ] No unused imports
- [ ] No wildcard imports (`from x import *`)
- [ ] Absolute imports preferred over relative

**Example:**
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import click
from pydantic import BaseModel

# Local
from .models import Feature
```

---

## Type Hints

### Type Hint Coverage

- [ ] All function parameters have type hints
- [ ] All return values have type hints
- [ ] Complex types properly annotated (List, Dict, Optional, Union)
- [ ] Type aliases used for complex types
- [ ] No use of `Any` without justification

**Automated Check:**
```bash
mypy src/
```

### Type Hint Quality

- [ ] Type hints are accurate (not just `Any`)
- [ ] Optional vs required parameters clear
- [ ] Union types used appropriately
- [ ] Generic types parameterized (List[str], not List)

**Example:**
```python
from typing import Optional, List, Dict

def process(
    data: Dict[str, str],
    options: Optional[List[str]] = None
) -> Dict[str, int]:
    pass
```

---

## Documentation

### Docstring Coverage

- [ ] All modules have module docstrings
- [ ] All public classes have docstrings
- [ ] All public functions/methods have docstrings
- [ ] All parameters documented in docstrings
- [ ] Return values documented
- [ ] Exceptions/raises documented

### Docstring Quality

- [ ] Google-style docstrings used consistently
- [ ] Descriptions are clear and complete
- [ ] Examples provided for complex functions
- [ ] Type information matches type hints
- [ ] No outdated/incorrect documentation

**Example:**
```python
def function(param: str, count: int = 0) -> List[str]:
    """
    Short description.

    Longer description if needed.

    Args:
        param: Description of param
        count: Description of count (default: 0)

    Returns:
        List of strings with results

    Raises:
        ValueError: If param is empty

    Examples:
        >>> function("test", 2)
        ['result1', 'result2']
    """
    pass
```

### Inline Comments

- [ ] Complex logic has explanatory comments
- [ ] Comments explain "why," not "what"
- [ ] No commented-out code left in
- [ ] TODO/FIXME comments have context
- [ ] Comments are up-to-date with code

---

## Code Organization

### File Structure

- [ ] No files exceed 500 lines
- [ ] Large files split by responsibility
- [ ] Clear module organization
- [ ] Proper `__init__.py` with exports
- [ ] No circular dependencies

### Function/Method Length

- [ ] Functions ≤ 50 lines (target: 20-30)
- [ ] Complex functions split into smaller ones
- [ ] Single responsibility per function
- [ ] Clear function names (verb-based)

### Class Organization

- [ ] Classes ≤ 300 lines
- [ ] Single responsibility per class
- [ ] Proper method organization:
  1. `__init__` and setup
  2. Public methods
  3. Private methods
  4. Special methods (`__str__`, etc.)

### Complexity

- [ ] Cyclomatic complexity < 10 per function
- [ ] Max nesting depth: 4 levels
- [ ] No "god objects" (classes doing too much)
- [ ] Complex conditionals extracted to functions

---

## Naming Conventions

### Clear and Descriptive

- [ ] Variable names descriptive (not `x`, `tmp`, `data`)
- [ ] Function names verb-based (`create_user`, `validate_input`)
- [ ] Class names noun-based (`UserService`, `FeatureValidator`)
- [ ] Boolean variables prefixed appropriately (`is_`, `has_`, `should_`)

### Consistent Conventions

- [ ] snake_case for functions/variables
- [ ] PascalCase for classes
- [ ] UPPER_SNAKE_CASE for constants
- [ ] Single underscore prefix for internal (`_internal`)
- [ ] Double underscore for private/name mangling (`__private`)

### Avoid Abbreviations

- [ ] No unclear abbreviations (`usr`, `cfg`, `tmp`)
- [ ] Standard abbreviations OK (`id`, `url`, `api`, `http`)
- [ ] Consistency within module/project

---

## Error Handling

### Exception Hierarchy

- [ ] Custom exceptions defined for module
- [ ] Specific exceptions for specific errors
- [ ] Base exception class for module
- [ ] Exceptions inherit appropriately

### Exception Handling

- [ ] Specific exceptions caught (not bare `except:`)
- [ ] Exceptions re-raised appropriately
- [ ] Errors logged before raising
- [ ] Exception messages clear and actionable
- [ ] No silent exception swallowing

**Example:**
```python
class FeatureError(Exception):
    """Base exception."""
    pass

class ValidationError(FeatureError):
    """Validation failed."""
    pass

try:
    validate_data(input)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    raise
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise ProcessingError("Unexpected error") from e
```

---

## Code Smells and Anti-Patterns

### Common Code Smells

- [ ] No duplicated code (DRY violated)
- [ ] No magic numbers (use named constants)
- [ ] No long parameter lists (> 5 parameters)
- [ ] No deeply nested code (> 4 levels)
- [ ] No boolean traps (`func(True, False, True)`)
- [ ] No mutable default arguments
- [ ] No global state/variables

### Design Issues

- [ ] No "god objects" (classes doing everything)
- [ ] No circular dependencies between modules
- [ ] No tight coupling (use dependency injection)
- [ ] No premature optimization
- [ ] No reinventing the wheel (use stdlib/libraries)

---

## Best Practices

### Python Idioms

- [ ] Context managers for resources (`with` statements)
- [ ] Comprehensions for simple transformations
- [ ] Generators for large datasets
- [ ] `pathlib.Path` instead of `os.path`
- [ ] f-strings for formatting
- [ ] `enumerate()` instead of manual counters
- [ ] `zip()` for parallel iteration

### Immutability

- [ ] Tuples for immutable sequences
- [ ] No mutable default arguments
- [ ] Dataclasses with `frozen=True` (if immutable)
- [ ] Pydantic models for validation

### Resource Management

- [ ] Files opened with context managers
- [ ] Database connections properly closed
- [ ] No resource leaks
- [ ] Cleanup in `finally` blocks or context managers

---

## Security

### Input Validation

- [ ] All external input validated
- [ ] SQL injection prevented (parameterized queries)
- [ ] Command injection prevented (no `shell=True` with input)
- [ ] Path traversal prevented (sanitized paths)

### Secrets Management

- [ ] No hardcoded credentials
- [ ] Secrets in environment variables
- [ ] No secrets in logs
- [ ] No secrets in error messages

### Data Handling

- [ ] PII handled appropriately
- [ ] Sensitive data not logged
- [ ] Data sanitized before output
- [ ] Proper encoding/decoding

---

## Testing Considerations

### Testability

- [ ] Functions are pure (where possible)
- [ ] Dependencies injected (not global)
- [ ] Side effects minimized and isolated
- [ ] Test-friendly interfaces

### Test Coverage

- [ ] Unit tests exist for all public functions
- [ ] Critical paths fully tested
- [ ] Edge cases tested
- [ ] Error conditions tested

---

## Performance

### Efficiency

- [ ] No unnecessary loops
- [ ] No premature optimization (but no obvious waste)
- [ ] Appropriate data structures used
- [ ] No quadratic algorithms where linear possible
- [ ] Large files processed in chunks/streams

### Memory Management

- [ ] No memory leaks
- [ ] Large datasets processed with generators
- [ ] Files not loaded entirely into memory
- [ ] Proper cleanup of resources

---

## Maintainability

### Readability

- [ ] Code reads like prose
- [ ] Intent is clear without comments
- [ ] Consistent style throughout
- [ ] Logical organization

### Modularity

- [ ] High cohesion within modules
- [ ] Low coupling between modules
- [ ] Clear interfaces
- [ ] Minimal dependencies

### Extensibility

- [ ] Easy to add new features
- [ ] Open/Closed principle followed
- [ ] Pluggable architecture (where appropriate)
- [ ] Clear extension points

---

## Version Control

### Git Hygiene

- [ ] No large files committed
- [ ] No sensitive data committed
- [ ] `.gitignore` properly configured
- [ ] No generated files committed
- [ ] Meaningful commit messages

---

## Automated Tools

### Run All Checks

```bash
# Format code
black src/ tests/

# Type check
mypy src/

# Lint
flake8 src/ tests/

# Security check
pip-audit

# Complexity check (if radon installed)
radon cc src/ -a

# All together
make lint  # If Makefile configured
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

---

## Quality Metrics Summary

### Target Metrics

| Metric | Target | Tool |
|--------|--------|------|
| Code coverage | ≥ 80% | pytest --cov |
| Type hint coverage | 100% | mypy --strict |
| Docstring coverage | ≥ 90% | interrogate |
| Complexity | < 10 | radon cc |
| Maintainability | A or B | radon mi |
| Lint errors | 0 | flake8 |

### Scoring

- **A Grade:** All targets met, no violations
- **B Grade:** Minor violations, coverage > 75%
- **C Grade:** Some violations, coverage > 60%
- **F Grade:** Major violations, coverage < 60%

---

## Sign-off

**Code Quality Review:**

- [ ] All automated checks passing
- [ ] Manual review complete
- [ ] No critical issues identified
- [ ] Code meets project standards

**Reviewed By:** _________________
**Date:** _________________
**Status:** ☐ Approved ☐ Needs Revision

**Notes:**

---

## References

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Clean Code Principles](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Refactoring: Improving the Design of Existing Code](https://martinfowler.com/books/refactoring.html)
