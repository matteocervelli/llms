# Contributing to LLMs Configuration Management System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them get started
- Focus on collaboration and learning
- Follow professional communication standards

---

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/llms.git
   cd llms
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/matteocervelli/llms.git
   ```

---

## Development Setup

### Prerequisites

- Python 3.11 or higher
- uv (Python package installer)
- Git

### Installation

```bash
# Install dependencies with uv
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -e ".[dev]"

# Verify installation
pytest --version
black --version
mypy --version
```

### Environment Configuration

Create a `.env` file if needed for local configuration (not committed to git):

```bash
# Example .env (optional)
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

---

## Development Workflow

### 1. Create a Feature Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow [Code Standards](#code-standards)
- Write tests for new functionality
- Update documentation as needed
- Keep commits focused and atomic

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_your_module.py
```

### 4. Format and Lint

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/
```

### 5. Commit Changes

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```bash
git add .
git commit -m "feat: add skill builder tool"
git commit -m "fix: resolve scope detection issue"
git commit -m "docs: update README with new examples"
git commit -m "test: add tests for doc fetcher"
```

**Commit types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Code style changes (formatting, etc.)
- `chore:` Maintenance tasks

### 6. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
```

---

## Code Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with these specifics:

- **Line length**: 100 characters (configured in pyproject.toml)
- **Indentation**: 4 spaces
- **Quotes**: Prefer double quotes for strings
- **Imports**: Organized in order (stdlib, third-party, local)

### Code Organization

#### File Size
- **Maximum 500 lines per file**
- Split files by logical responsibility when exceeding limit
- Prefer multiple focused files over single large files

#### Naming Conventions
- **Functions/methods**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: Prefix with `_`

#### Type Hints
Always use type hints for function parameters and return values:

```python
def fetch_documentation(url: str, timeout: int = 30) -> dict[str, Any]:
    """Fetch documentation from URL."""
    ...
```

#### Docstrings
Use Google-style docstrings:

```python
def process_markdown(content: str, options: dict[str, Any]) -> str:
    """Process markdown content with specified options.

    Args:
        content: The markdown content to process
        options: Processing options including format and metadata

    Returns:
        Processed markdown content as string

    Raises:
        ValueError: If content is empty or invalid
        ProcessingError: If processing fails
    """
    ...
```

### Architecture Principles

1. **Single Responsibility**: Each module/class has one clear purpose
2. **Dependency Injection**: Pass dependencies as parameters, avoid globals
3. **Interface First**: Define contracts before implementations
4. **Clean Separation**: Maintain strict layer separation

### Project-Specific Patterns

#### Scope Management
Use the scope manager for all tools that create skills/commands/agents:

```python
from src.core.scope_manager import ScopeManager

scope = ScopeManager.detect_scope()  # Auto-detect
# or
scope = ScopeManager.get_scope(scope_type="global")  # Explicit
```

#### LLM Adapter Pattern
Use adapters for LLM-specific operations:

```python
from src.core.llm_adapter import get_adapter

adapter = get_adapter("claude")  # ClaudeAdapter instance
skill = adapter.create_skill(name="my-skill", template="basic")
```

---

## Testing

### Test Organization

```
tests/
├── test_doc_fetcher.py
├── test_scope_manager.py
├── test_skill_builder.py
└── fixtures/
    ├── sample_skill.md
    └── sample_manifest.json
```

### Writing Tests

```python
import pytest
from src.tools.doc_fetcher import DocFetcher

def test_fetch_documentation():
    """Test documentation fetching."""
    fetcher = DocFetcher()
    result = fetcher.fetch("https://example.com/docs")

    assert result is not None
    assert "content" in result
    assert result["status"] == "success"

def test_fetch_with_invalid_url():
    """Test fetching with invalid URL."""
    fetcher = DocFetcher()

    with pytest.raises(ValueError):
        fetcher.fetch("invalid-url")
```

### Test Coverage Requirements

- **Minimum 80% coverage** for all modules
- **100% coverage** for critical paths (authentication, data processing)
- Use `pytest --cov-report=html` to view coverage report

### Mocking External Dependencies

```python
from unittest.mock import Mock, patch

@patch('requests.get')
def test_fetch_with_mock(mock_get):
    """Test fetching with mocked HTTP request."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html>Test content</html>"
    mock_get.return_value = mock_response

    fetcher = DocFetcher()
    result = fetcher.fetch("https://example.com/docs")

    assert result["content"] == "Test content"
```

---

## Documentation

### README Files

Every tool needs a README with:

1. **Overview**: What the tool does
2. **Installation**: How to install/setup
3. **Usage**: Examples and common use cases
4. **API Reference**: Function/class documentation
5. **Examples**: Practical examples

### Code Comments

- Explain **why**, not **what**
- Document complex algorithms
- Add TODO comments for future work
- Use FIXME for known issues

### Updating Documentation

When adding features:

1. Update tool README
2. Update main README if needed
3. Add examples to CLAUDE.md if relevant
4. Update CHANGELOG.md

---

## Pull Request Process

### Before Submitting

- [ ] All tests pass locally
- [ ] Code is formatted with black
- [ ] No linting errors (flake8)
- [ ] Type checking passes (mypy)
- [ ] Coverage meets minimum 80%
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for notable changes)

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Related Issues
Closes #123

## Testing
Description of testing performed

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code formatted and linted
- [ ] Type hints added
- [ ] CHANGELOG.md updated
```

### Review Process

1. **Automated checks**: Tests, linting, type checking must pass
2. **Code review**: At least one approval required
3. **Documentation review**: Ensure docs are clear and complete
4. **Testing review**: Verify tests cover the changes

### After Approval

- Squash commits if needed
- Merge to main branch
- Delete feature branch

---

## Development Tips

### Useful Commands

```bash
# Watch tests (requires pytest-watch)
ptw

# Generate coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html

# Check types for specific file
mypy src/tools/doc_fetcher/main.py

# Format specific file
black src/tools/doc_fetcher/main.py

# Run specific test
pytest tests/test_doc_fetcher.py::test_fetch_documentation -v
```

### IDE Setup

#### VS Code

Recommended extensions:
- Python
- Pylance
- Black Formatter
- autoDocstring

Settings (`.vscode/settings.json`):
```json
{
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true
}
```

---

## Questions?

- Open an issue on GitHub
- Check [CLAUDE.md](CLAUDE.md) for project-specific guidelines
- Review [TASK.md](TASK.md) for current sprint focus

---

**Thank you for contributing! 🎉**
