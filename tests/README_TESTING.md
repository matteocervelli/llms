# Skill Builder Testing Guide

Complete testing guide for the skill_builder tool.

## Table of Contents

- [Overview](#overview)
- [Running Tests](#running-tests)
- [Test Organization](#test-organization)
- [Writing Tests](#writing-tests)
- [Fixtures](#fixtures)
- [Coverage](#coverage)
- [Troubleshooting](#troubleshooting)

## Overview

The skill_builder test suite ensures production-quality software through comprehensive testing across multiple dimensions:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete workflows end-to-end
- **Performance Tests**: Verify response time targets (< 50ms, < 100ms, < 10ms)
- **Security Tests**: Validate security measures (path traversal, XSS, injection)
- **CLI Tests**: Test command-line interface and user interactions

### Test Metrics

- **Current Coverage**: 115+ passing tests
- **Target Coverage**: 80%+ code coverage
- **Test Distribution**:
  - Unit Tests: 60+
  - Integration Tests: 20+
  - Performance Tests: 15+
  - Security Tests: 20+

## Running Tests

### Run All Tests

```bash
pytest tests/skill_builder/ -v
```

### Run with Coverage

```bash
pytest tests/skill_builder/ --cov=src/tools/skill_builder --cov-report=html --cov-report=term-missing
```

### Run Specific Test Files

```bash
# Unit tests only
pytest tests/skill_builder/test_models.py -v
pytest tests/skill_builder/test_validator.py -v

# Integration tests
pytest tests/skill_builder/test_skill_builder_integration.py -v

# Performance tests
pytest tests/skill_builder/test_skill_builder_performance.py -v

# Security tests
pytest tests/skill_builder/test_skill_builder_security.py -v

# CLI tests
pytest tests/skill_builder/test_skill_builder_cli.py -v
```

### Run Specific Test Classes or Methods

```bash
# Run specific class
pytest tests/skill_builder/test_validator.py::TestSkillValidator -v

# Run specific test
pytest tests/skill_builder/test_validator.py::TestSkillValidator::test_validate_skill_name_valid -v
```

### Run with Markers

```bash
# Run only parametrized tests
pytest tests/skill_builder/ -v -m parametrize

# Skip slow tests
pytest tests/skill_builder/ -v -m "not slow"
```

## Test Organization

### Directory Structure

```
tests/skill_builder/
├── conftest.py                           # Shared fixtures
├── test_models.py                        # Pydantic model tests
├── test_validator.py                     # Validation logic tests
├── test_templates.py                     # Template rendering tests
├── test_catalog.py                       # Catalog model tests
├── test_catalog_manager.py               # Catalog manager tests
├── test_skill_builder_cli.py             # CLI integration tests
├── test_skill_builder_integration.py     # End-to-end workflow tests
├── test_skill_builder_performance.py     # Performance benchmarks
└── test_skill_builder_security.py        # Security validation tests
```

### Test Categories

#### 1. Unit Tests

Test individual components in isolation:

```python
def test_validate_skill_name_valid():
    """Test valid skill names pass validation."""
    validator = SkillValidator()
    assert validator.validate_skill_name("test-skill")
```

#### 2. Integration Tests

Test complete workflows:

```python
def test_create_list_validate_delete_workflow(tmp_path):
    """Test full skill lifecycle."""
    # Setup
    builder = SkillBuilder(...)

    # Create
    result = builder.build_skill(config)
    assert result.success

    # List
    skills = catalog_manager.list_skills()
    assert len(skills) == 1

    # Validate
    is_valid = validator.validate_skill_directory(result.skill_path)
    assert is_valid

    # Delete
    delete_result = builder.delete_skill(name, scope)
    assert delete_result.success
```

#### 3. Performance Tests

Validate response time targets:

```python
def test_skill_creation_under_50ms(tmp_path):
    """Test skill creation meets performance target."""
    start = time.perf_counter()
    result = builder.build_skill(config)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert result.success
    assert elapsed_ms < 50, f"Creation took {elapsed_ms:.2f}ms (target: < 50ms)"
```

#### 4. Security Tests

Verify security measures:

```python
@pytest.mark.parametrize("malicious_name", [
    "../../../etc/passwd",
    "/absolute/path",
])
def test_path_traversal_blocked(malicious_name):
    """Test path traversal attempts are blocked."""
    with pytest.raises((ValueError, SkillBuilderError)):
        config = SkillConfig(name=malicious_name, ...)
        builder.build_skill(config)
```

#### 5. CLI Tests

Test command-line interface:

```python
def test_list_command(cli_runner):
    """Test skill-builder list command."""
    result = cli_runner.invoke(cli, ["list"])
    assert result.exit_code in [0, 1]
```

## Writing Tests

### Test Structure Pattern

```python
class TestFeatureName:
    """Test suite for specific feature."""

    def test_feature_success_case(self, fixture):
        """Test successful operation."""
        # Setup
        component = Component()

        # Execute
        result = component.method(valid_input)

        # Assert
        assert result.success
        assert result.value == expected

    def test_feature_failure_case(self, fixture):
        """Test error handling."""
        component = Component()

        with pytest.raises(ExpectedError):
            component.method(invalid_input)
```

### Naming Conventions

- **Test files**: `test_<module_name>.py`
- **Test classes**: `Test<FeatureName>`
- **Test methods**: `test_<what_is_being_tested>` (descriptive)

### Docstring Standards

Every test should have a clear docstring:

```python
def test_validate_skill_name_path_traversal():
    """Test path traversal attempts in skill names are rejected.

    Security requirement: Prevent ../../../ style path traversal.
    """
    pass
```

### Using Parametrize

Test multiple inputs efficiently:

```python
@pytest.mark.parametrize("template_name", ["basic", "with_tools", "with_scripts", "advanced"])
def test_all_templates(template_name, tmp_path):
    """Test skill creation with each template."""
    config = SkillConfig(name=f"{template_name}-skill", template=template_name, ...)
    result = builder.build_skill(config)
    assert result.success
```

## Fixtures

### Available Fixtures (conftest.py)

#### Directory Fixtures

```python
def test_example(tmp_path, temp_skill_dir, temp_project_root):
    """
    - tmp_path: pytest built-in, unique temp directory
    - temp_skill_dir: .claude/skills structure
    - temp_project_root: Complete project structure
    """
    pass
```

#### Configuration Fixtures

```python
def test_example(sample_skill_config, sample_skill_config_with_tools):
    """
    - sample_skill_config: Basic skill configuration
    - sample_skill_config_with_tools: Configuration with allowed-tools
    - sample_skill_config_with_scripts: Configuration with scripts/
    """
    pass
```

#### Catalog Fixtures

```python
def test_example(sample_catalog_entry, sample_catalog_with_entries, large_catalog):
    """
    - sample_catalog_entry: Single catalog entry
    - sample_catalog_with_entries: Catalog with 3 skills
    - large_catalog: 100+ skills for performance testing
    """
    pass
```

#### CLI Fixtures

```python
def test_example(cli_runner, mock_questionary):
    """
    - cli_runner: Click CliRunner for testing CLI commands
    - mock_questionary: Mocked questionary for wizard testing
    """
    pass
```

### Creating Custom Fixtures

Add to `conftest.py`:

```python
@pytest.fixture
def custom_fixture(tmp_path):
    """Custom fixture description."""
    # Setup
    resource = setup_resource(tmp_path)

    # Provide to test
    yield resource

    # Teardown (optional)
    cleanup(resource)
```

## Coverage

### Viewing Coverage

After running tests with `--cov`:

```bash
# Terminal summary
pytest tests/skill_builder/ --cov=src/tools/skill_builder --cov-report=term-missing

# HTML report (opens in browser)
pytest tests/skill_builder/ --cov=src/tools/skill_builder --cov-report=html
open htmlcov/index.html
```

### Coverage Targets

| Component | Target | Current |
|-----------|--------|---------|
| Models | 90%+ | ~85% |
| Validator | 90%+ | ~90% |
| Templates | 85%+ | ~85% |
| Builder | 80%+ | ~75% |
| Catalog | 85%+ | ~82% |
| CLI | 70%+ | ~65% |
| **Overall** | **80%+** | **~77%** |

### Improving Coverage

1. **Identify gaps**:
   ```bash
   pytest --cov=src/tools/skill_builder --cov-report=term-missing | grep "MISS"
   ```

2. **Focus on untested lines**:
   - Error handling branches
   - Edge cases
   - Failure recovery paths

3. **Add targeted tests**:
   ```python
   def test_uncovered_branch():
       """Test previously uncovered error branch."""
       # Test the specific uncovered logic
       pass
   ```

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ImportError: No module named 'src'`

**Solution**:
```bash
# Ensure project root is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install in editable mode
pip install -e .
```

#### 2. Fixture Not Found

**Problem**: `fixture 'custom_fixture' not found`

**Solution**:
- Check `conftest.py` exists in correct location
- Verify fixture is defined with `@pytest.fixture` decorator
- Ensure fixture name matches exactly

#### 3. Assertion Failures

**Problem**: `AssertionError: assert False`

**Solution**:
```bash
# Run with verbose output
pytest tests/skill_builder/test_file.py::test_name -vv

# Show local variables
pytest tests/skill_builder/test_file.py::test_name -l

# Drop into debugger
pytest tests/skill_builder/test_file.py::test_name --pdb
```

#### 4. Parametrize Issues

**Problem**: Parametrized test failing for specific values

**Solution**:
```bash
# Run only specific parameter
pytest tests/skill_builder/test_file.py::test_name[param_value] -v
```

#### 5. Slow Tests

**Problem**: Test suite takes too long

**Solution**:
```bash
# Show slowest tests
pytest tests/skill_builder/ --durations=10

# Run tests in parallel
pytest tests/skill_builder/ -n auto  # requires pytest-xdist
```

### Debugging Tips

#### Use pytest Flags

```bash
# Stop on first failure
pytest tests/skill_builder/ -x

# Show print statements
pytest tests/skill_builder/ -s

# Verbose output with locals
pytest tests/skill_builder/ -vv -l

# Full traceback
pytest tests/skill_builder/ --tb=long
```

#### Use Debugger

```python
def test_example():
    """Test with debugger."""
    import pdb; pdb.set_trace()  # Add breakpoint

    result = function_under_test()
    assert result == expected
```

#### Temporary Test Isolation

```python
@pytest.mark.skip(reason="Debugging other tests")
def test_skip_this():
    pass

@pytest.mark.xfail(reason="Known issue #123")
def test_expected_to_fail():
    pass
```

### Performance Issues

If performance tests fail:

1. **Check system load**: Close other applications
2. **Run multiple times**: Ensure consistency
3. **Adjust targets**: If consistently 10-20% over, targets may need adjustment
4. **Profile code**: Use `cProfile` to find bottlenecks

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
result = builder.build_skill(config)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

## Best Practices

### 1. Test Independence

Each test should be independent:

```python
# GOOD: Each test creates its own data
def test_create_skill(tmp_path):
    builder = setup_builder(tmp_path)
    result = builder.build_skill(config)
    assert result.success

# BAD: Tests depend on shared state
global_builder = None

def test_create_skill():
    result = global_builder.build_skill(config)  # Depends on global
```

### 2. Clear Assertions

Use descriptive assertion messages:

```python
# GOOD
assert result.success, f"Skill creation failed: {result.error}"
assert elapsed_ms < 50, f"Operation took {elapsed_ms:.2f}ms (target: < 50ms)"

# BAD
assert result.success
assert elapsed_ms < 50
```

### 3. Test One Thing

Each test should verify one specific behavior:

```python
# GOOD
def test_skill_name_validation():
    """Test skill name validation."""
    validator = SkillValidator()
    assert validator.validate_skill_name("valid-name")

def test_skill_description_validation():
    """Test description validation."""
    validator = SkillValidator()
    assert validator.validate_description("Valid description. Use when needed.")

# BAD
def test_validation():
    """Test all validation."""
    # Tests too many things at once
    validator = SkillValidator()
    assert validator.validate_skill_name("valid-name")
    assert validator.validate_description("Valid description.")
    assert validator.validate_allowed_tools(["Read"])
    # ... etc
```

### 4. Use Fixtures for Setup

Avoid duplication with fixtures:

```python
# GOOD
@pytest.fixture
def configured_builder(tmp_path):
    """Builder with standard configuration."""
    scope_manager = ScopeManager(project_root=tmp_path)
    # ... setup ...
    return SkillBuilder(...)

def test_with_fixture(configured_builder):
    result = configured_builder.build_skill(config)
    assert result.success

# BAD
def test_without_fixture(tmp_path):
    # Repeated setup in every test
    scope_manager = ScopeManager(project_root=tmp_path)
    template_manager = TemplateManager()
    # ... etc
```

## Contributing

When adding new features to skill_builder:

1. **Write tests first** (TDD approach)
2. **Ensure 80%+ coverage** for new code
3. **Add integration tests** for new workflows
4. **Document test patterns** in this guide
5. **Run full test suite** before committing

```bash
# Pre-commit checklist
pytest tests/skill_builder/ --cov=src/tools/skill_builder
black tests/skill_builder/ src/tools/skill_builder/
flake8 tests/skill_builder/ src/tools/skill_builder/
mypy src/tools/skill_builder/
```

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
