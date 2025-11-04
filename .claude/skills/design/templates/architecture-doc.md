---
name: architecture-doc
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Architecture Design: [Feature Name]

> **Status:** Draft | In Review | Approved
> **Author:** [Your Name]
> **Date:** [YYYY-MM-DD]
> **Version:** 1.0

---

## Overview

### Purpose
[Brief description of what this feature does and why it's needed]

### Scope
**In Scope:**
- [Feature component 1]
- [Feature component 2]

**Out of Scope:**
- [Deferred item 1]
- [Deferred item 2]

### Success Criteria
- [Measurable criterion 1]
- [Measurable criterion 2]

---

## Architecture Pattern

**Chosen Pattern:** [Layered | Modular | Service Layer | etc.]

**Rationale:**
[Why this pattern was chosen over alternatives]

**Alignment with Project:**
[How this fits with existing architecture]

---

## Component Design

### Component 1: [Component Name]

**Responsibility:**
[What this component does - single responsibility]

**Dependencies:**
- [External dependency 1]
- [Internal module 1]

**Interface:**
```python
class ComponentName:
    """Component description."""

    def method_name(self, param: str) -> Result:
        """Method description."""
        pass
```

**Implementation Notes:**
- [Note 1]
- [Note 2]

---

### Component 2: [Component Name]

[Repeat structure above for each component]

---

## Data Model

### Entity: [Entity Name]

**Description:** [What this entity represents]

**Schema:**
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EntityModel(BaseModel):
    """Entity model with validation."""

    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., max_length=1000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = []

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        schema_extra = {
            "example": {
                "name": "example",
                "description": "Example entity",
                "tags": ["tag1", "tag2"]
            }
        }
```

**Validation Rules:**
- [Rule 1: e.g., name must be unique]
- [Rule 2: e.g., description required]

**Relationships:**
- [Related entity 1]: [Type of relationship]

---

## API Specification

### Internal API: [Function/Method Name]

```python
def function_name(
    param1: str,
    param2: int = 0,
    *,
    optional_param: Optional[str] = None
) -> ResultType:
    """
    Function description.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)
        optional_param: Description (optional)

    Returns:
        ResultType with outcome

    Raises:
        ValidationError: If validation fails
        ProcessError: If processing fails

    Examples:
        >>> function_name("test", 42)
        ResultType(...)
    """
    pass
```

**Usage Example:**
```python
result = function_name(
    param1="value",
    param2=100,
    optional_param="extra"
)
```

---

### REST API Endpoint (If Applicable)

**Endpoint:** `[METHOD] /api/v1/resources`

**Request:**
```json
{
  "field1": "value",
  "field2": 123
}
```

**Response (200 OK):**
```json
{
  "data": {
    "id": "uuid",
    "field1": "value",
    "field2": 123
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Field validation failed",
    "details": [
      {
        "field": "field1",
        "issue": "Required field missing"
      }
    ]
  }
}
```

---

## Data Flows

### Flow 1: [Primary Workflow Name]

**Sequence:**
```
User Input
    ↓
Validator (validates input)
    ↓
Service (business logic)
    ↓
Repository (data access)
    ↓
Database/File System
    ↓
Response to User
```

**Steps:**
1. User provides input via [CLI | API | UI]
2. Validator checks input against rules
3. Service executes business logic
4. Repository persists data
5. Response returned with result

**Error Paths:**
- **Validation Error** → Return 400 with details
- **Not Found** → Return 404
- **Processing Error** → Return 500, log error

---

### Flow 2: [Secondary Workflow Name]

[Repeat structure for additional flows]

---

## Module Structure

```
src/tools/feature_name/
├── __init__.py              # Public exports
├── models.py                # Pydantic models
├── interfaces.py            # Abstract base classes
├── core.py                  # Core business logic
├── repository.py            # Data access layer
├── validators.py            # Input validation
├── utils.py                 # Helper functions
├── config.py                # Configuration
├── exceptions.py            # Custom exceptions
├── templates/               # Template files
│   └── template.md
├── scripts/                 # Helper scripts
│   └── helper.py
└── tests/
    ├── __init__.py
    ├── test_core.py
    ├── test_validators.py
    ├── test_repository.py
    └── fixtures.py          # Test fixtures
```

**File Size Limit:** Max 500 lines per file (split if exceeded)

---

## Error Handling

### Exception Hierarchy

```python
class FeatureError(Exception):
    """Base exception for feature."""
    pass

class ValidationError(FeatureError):
    """Input validation failed."""

    def __init__(self, message: str, errors: List[str]):
        super().__init__(message)
        self.errors = errors

class NotFoundError(FeatureError):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} not found: {identifier}")
        self.resource = resource
        self.identifier = identifier

class ProcessingError(FeatureError):
    """Processing failed."""
    pass
```

### Error Handling Strategy

**Validation:**
- Validate at boundaries (API entry points)
- Fail fast with clear error messages
- Return ValidationError with field details

**Processing:**
- Catch specific exceptions
- Log errors with context (params, state)
- Return ProcessingError with actionable message

**External Services:**
- Implement retry logic (exponential backoff)
- Circuit breaker for failing services
- Graceful degradation where possible

---

## Configuration

### Configuration Model

```python
from pydantic_settings import BaseSettings

class FeatureConfig(BaseSettings):
    """Feature configuration from environment."""

    # Required settings
    api_key: str

    # Optional with defaults
    timeout: int = 30
    max_retries: int = 3
    debug: bool = False

    # Nested config
    database_url: str = "sqlite:///data.db"

    class Config:
        env_prefix = "FEATURE_"
        case_sensitive = False
        env_file = ".env"
```

### Configuration Sources

1. Environment variables (highest priority)
2. `.env` file
3. Configuration files (JSON/YAML)
4. Default values (lowest priority)

### Required Configuration

| Setting | Type | Required | Default | Description |
|---------|------|----------|---------|-------------|
| `FEATURE_API_KEY` | str | Yes | - | API key for external service |
| `FEATURE_TIMEOUT` | int | No | 30 | Request timeout in seconds |
| `FEATURE_DEBUG` | bool | No | False | Enable debug logging |

---

## Testing Strategy

### Unit Tests

**Target Coverage:** 80%+

**Components to Test:**
- [ ] Validators: All validation rules
- [ ] Core logic: All business logic branches
- [ ] Utilities: All helper functions

**Mocking Strategy:**
- Mock external dependencies (API calls, file I/O)
- Mock repositories in service tests
- Use fixtures for test data

**Example Test:**
```python
import pytest
from feature import create_resource

def test_create_resource_success(mock_repository):
    """Test successful resource creation."""
    # Arrange
    data = {"name": "test", "value": 123}

    # Act
    result = create_resource(data)

    # Assert
    assert result.name == "test"
    assert result.value == 123
    mock_repository.save.assert_called_once()
```

---

### Integration Tests

**Scenarios to Test:**
- [ ] End-to-end workflow (input → output)
- [ ] Database interactions (create, read, update, delete)
- [ ] External service integration
- [ ] Error handling paths

**Test Environment:**
- Use test database (isolated from production)
- Mock external APIs or use sandbox
- Clean up test data after each test

---

### Performance Tests

**Performance Requirements:**
- Response time: < [N] ms (p95)
- Throughput: [N] requests/second
- Memory usage: < [N] MB
- CPU usage: < [N]%

**Tests to Implement:**
- [ ] Load test: Sustained load at target throughput
- [ ] Stress test: Identify breaking point
- [ ] Spike test: Handle sudden traffic increase

---

## Security Considerations

**From Security Checklist (Analysis Phase):**

### Input Validation
- [ ] All user inputs validated and sanitized
- [ ] SQL injection prevented (parameterized queries)
- [ ] Command injection prevented (avoid shell=True)
- [ ] Path traversal prevented (validate file paths)

### Authentication & Authorization
- [ ] Authentication required for protected endpoints
- [ ] Authorization checks at every access point
- [ ] Session management secure (timeouts, invalidation)

### Data Protection
- [ ] Sensitive data encrypted in transit (TLS)
- [ ] Sensitive data encrypted at rest (if applicable)
- [ ] PII handling compliant with regulations
- [ ] Secrets not hardcoded (environment variables)

### Error Handling
- [ ] Error messages don't leak sensitive information
- [ ] Stack traces not exposed to users
- [ ] Security events logged (auth failures, access violations)

---

## Performance Considerations

### Optimization Strategies

**Caching:**
- Cache frequently accessed data (TTL: [N] seconds)
- Use Redis/in-memory cache for hot data
- Invalidate cache on updates

**Database:**
- Index frequently queried fields
- Use connection pooling
- Batch operations where possible

**Resource Management:**
- Limit concurrent operations ([N] max)
- Use pagination for large datasets
- Stream large files (don't load in memory)

### Performance Budgets

| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| Response Time | < 100ms | < 500ms | > 1000ms |
| Memory Usage | < 50MB | < 100MB | > 200MB |
| Database Queries | 1-2 per request | 3-5 | > 10 |

---

## Dependencies

### External Dependencies

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| pydantic | ^2.0.0 | Data validation | MIT |
| click | ^8.0.0 | CLI framework | BSD |
| pytest | ^7.0.0 | Testing | MIT |

### Internal Dependencies

| Module | Purpose | Coupling |
|--------|---------|----------|
| src.core.config | Configuration management | Low |
| src.utils.validators | Input validation | Low |
| src.utils.file_utils | File operations | Low |

---

## Implementation Notes

### Development Steps

1. **Phase 1: Core Models**
   - Implement Pydantic models
   - Add validation rules
   - Write model tests

2. **Phase 2: Repository Layer**
   - Implement repository interface
   - Add file system/database implementation
   - Write repository tests

3. **Phase 3: Business Logic**
   - Implement core service
   - Add business rules
   - Write service tests (with mocked repository)

4. **Phase 4: API Layer**
   - Implement CLI/REST endpoints
   - Add request/response handling
   - Write integration tests

5. **Phase 5: Documentation**
   - Write user documentation
   - Add API examples
   - Update changelog

### Code Style

- Follow PEP 8 style guide
- Use Black for formatting
- Use mypy for type checking
- Google-style docstrings

### Git Workflow

- Create feature branch: `feature/feature-name`
- Commit frequently with clear messages
- Run tests before pushing
- Create PR for review

---

## Open Questions

- [ ] Question 1: [Description and why it needs answering]
- [ ] Question 2: [Description and who should answer it]
- [ ] Question 3: [Description and deadline for decision]

---

## Review Checklist

**Before Implementation:**
- [ ] Architecture reviewed by team
- [ ] Security considerations addressed
- [ ] Performance requirements feasible
- [ ] Dependencies identified and approved
- [ ] Testing strategy defined
- [ ] Open questions resolved

**Ready for Implementation:** ☐ Yes ☐ No (explain:_________________)

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial design |
| 1.1 | YYYY-MM-DD | [Name] | Updated after review |

---

## References

- Requirements Analysis: `docs/implementation/[feature]-analysis.md`
- Related Issues: GitHub #[issue-number]
- Architecture Patterns: `architecture-patterns.md`
- API Design Guide: `api-design-guide.md`
