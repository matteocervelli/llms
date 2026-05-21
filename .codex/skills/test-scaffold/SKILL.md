---
name: test-scaffold
description: Generate unit test files with structure, fixtures, and mocking patterns for Python (pytest) or JS/TS (Jest), auto-detecting the framework. Use when starting tests for a source file. Trigger on "scaffold tests", "generate test file", "write test boilerplate", "set up tests for".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Test Scaffold Skill

## Purpose

Generate unit test files with proper structure, fixtures, and mocking patterns. Auto-detects framework (pytest vs Jest) based on project configuration.

## Quick Start

```bash
/test-scaffold <source-file>
```

## Framework Detection

1. Check for `pytest.ini`, `pyproject.toml [tool.pytest]` -> pytest
2. Check for `jest.config.*`, `package.json jest` -> Jest
3. File extension: `.py` -> pytest, `.ts/.js` -> Jest

## Test File Naming

| Source                      | Test File                        |
| --------------------------- | -------------------------------- |
| `src/utils/validator.py`    | `tests/test_validator.py`        |
| `src/utils/validator.ts`    | `src/utils/validator.test.ts`    |
| `src/components/Button.tsx` | `src/components/Button.test.tsx` |

## Test Structure (AAA Pattern)

All tests follow Arrange-Act-Assert:

```python
def test_function_condition_expected():
    # Arrange - setup state
    input_data = {"key": "value"}

    # Act - execute behavior
    result = function_under_test(input_data)

    # Assert - verify outcome
    assert result.success is True
```

## Pytest Template

```python
"""Tests for [module_name]."""

import pytest
from unittest.mock import Mock, patch
from src.module import function_to_test, ClassToTest


@pytest.fixture
def sample_data():
    """Sample test data."""
    return {"id": 1, "name": "test"}


@pytest.fixture
def mock_dependency():
    """Mock external dependency."""
    mock = Mock()
    mock.method.return_value = {"status": "ok"}
    return mock


class TestClassName:
    """Tests for ClassName."""

    def test_init_valid_params(self):
        """Test initialization with valid params."""
        instance = ClassToTest(param="value")
        assert instance.param == "value"

    def test_method_returns_expected(self, sample_data):
        """Test method returns expected result."""
        instance = ClassToTest()
        result = instance.method(sample_data)
        assert result["processed"] is True


def test_function_happy_path(sample_data):
    """Test function with valid input."""
    result = function_to_test(sample_data)
    assert result is not None


def test_function_none_raises():
    """Test function raises on None input."""
    with pytest.raises(ValueError, match="cannot be None"):
        function_to_test(None)


@pytest.mark.parametrize("input_val,expected", [
    ("valid", True),
    ("invalid", False),
    ("", False),
])
def test_validation_cases(input_val, expected):
    """Test validation with multiple inputs."""
    assert validate(input_val) == expected


@patch("src.module.external_api")
def test_with_mocked_api(mock_api):
    """Test with mocked external API."""
    mock_api.return_value = {"data": "test"}
    result = function_using_api()
    assert result["data"] == "test"
    mock_api.assert_called_once()
```

## Jest Template

```typescript
/**
 * Tests for [module_name]
 */

import { functionToTest, ClassToTest } from "./module";

jest.mock("./dependency");

describe("ModuleName", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("ClassName", () => {
    let instance: ClassToTest;

    beforeEach(() => {
      instance = new ClassToTest();
    });

    it("should initialize with valid params", () => {
      const instance = new ClassToTest({ param: "value" });
      expect(instance.param).toBe("value");
    });

    it("should throw on invalid params", () => {
      expect(() => new ClassToTest(null)).toThrow("Invalid");
    });
  });

  describe("functionToTest", () => {
    it("should return expected result", () => {
      const result = functionToTest({ key: "value" });
      expect(result).toEqual({ processed: true });
    });

    it("should handle null input", () => {
      expect(() => functionToTest(null)).toThrow();
    });
  });

  describe("validation", () => {
    it.each([
      ["valid@email.com", true],
      ["invalid", false],
      ["", false],
    ])('validates "%s" as %s', (input, expected) => {
      expect(validate(input)).toBe(expected);
    });
  });

  describe("async operations", () => {
    it("should resolve with data", async () => {
      const result = await asyncFunction();
      expect(result.success).toBe(true);
    });

    it("should reject on error", async () => {
      await expect(asyncFunction(null)).rejects.toThrow();
    });
  });
});
```

## What to Test

### Always Test

- Public functions and methods
- Happy path (normal success)
- Error conditions (exceptions, rejections)
- Edge cases (empty, null, boundary values)
- Input validation

### Mock These

- External APIs
- Database calls
- File system (use tmp_path in pytest)
- Time/dates
- Random values

### Don't Test

- Private implementation details
- Framework boilerplate
- Third-party library internals

## Running Tests

### Pytest

```bash
# Run fast suite locally (skip integration/e2e — they run on CI)
pytest -m "not integration and not e2e"

# With coverage (informational; threshold enforced on CI)
pytest -m "not integration and not e2e" --cov=src --cov-report=term-missing

# Full suite with threshold — run on CI, not locally
# pytest --cov=src --cov-fail-under=80

# Specific file
pytest tests/test_module.py -v
```

### Jest

```bash
# Run all
npm test

# With coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

## Coverage Target

**Minimum**: 80% overall
**Critical paths**: 100%

## Integration

Generated tests should pass quality checks from `/quality-check` and be verified by `/pre-commit`.
