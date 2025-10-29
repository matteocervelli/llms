# API Design Guide

## Overview

This guide provides best practices for designing APIs in this project, covering both external REST APIs (if applicable) and internal Python function APIs.

---

## Python Function API Design

### Function Signatures

**Clear, Type-Hinted Signatures:**
```python
from typing import Optional, List, Dict, Union
from pathlib import Path

def create_skill(
    name: str,
    description: str,
    allowed_tools: Optional[List[str]] = None,
    output_dir: Path = Path(".claude/skills"),
    *,  # Force keyword-only arguments after this
    template: str = "basic",
    dry_run: bool = False
) -> SkillConfig:
    """
    Create a new skill with the given configuration.

    Args:
        name: Skill name (alphanumeric with hyphens)
        description: Brief description of what the skill does
        allowed_tools: List of allowed tool names (default: None)
        output_dir: Directory to write skill files (default: .claude/skills)
        template: Template to use (default: "basic")
        dry_run: If True, validate but don't write files (default: False)

    Returns:
        SkillConfig: Configuration of the created skill

    Raises:
        ValidationError: If name or description is invalid
        FileExistsError: If skill already exists and overwrite=False
        IOError: If unable to write skill files

    Examples:
        >>> create_skill("analysis", "Analyze requirements")
        SkillConfig(name='analysis', ...)

        >>> create_skill(
        ...     name="design",
        ...     description="Design architecture",
        ...     allowed_tools=["Read", "Write"],
        ...     template="advanced"
        ... )
    """
    pass
```

**Best Practices:**
- Use type hints for all parameters and return values
- Provide default values for optional parameters
- Use keyword-only arguments (`*`) for clarity
- Document parameters, returns, raises, and examples
- Keep functions focused (single responsibility)
- Return meaningful values (not just True/False)

### Parameter Design

**Good:**
```python
def search_skills(
    query: str,
    scope: ScopeType = ScopeType.PROJECT,
    limit: int = 10
) -> List[SkillConfig]:
    """Search skills matching query."""
    pass
```

**Avoid:**
```python
def search(q, s=None, l=None):  # Unclear parameters
    pass

def do_thing(params):  # Too generic
    pass

def search_skills(query, scope, limit, sort, order, offset, ...):  # Too many params
    pass
```

**When to Use `**kwargs`:**
- Forwarding arguments to underlying functions
- Plugin/extension points with unknown parameters
- Configuration dictionaries

```python
def build_with_options(name: str, **options: Any) -> Result:
    """
    Build with flexible options.

    Args:
        name: Resource name
        **options: Additional options passed to builder
            - template (str): Template name
            - dry_run (bool): Validate only
            - verbose (bool): Enable verbose output
    """
    pass
```

### Return Values

**Use Pydantic Models for Complex Returns:**
```python
from pydantic import BaseModel

class CreateResult(BaseModel):
    """Result of create operation."""
    success: bool
    resource: SkillConfig
    warnings: List[str] = []
    metadata: Dict[str, Any] = {}

def create_skill(name: str) -> CreateResult:
    """Create skill and return detailed result."""
    # ...
    return CreateResult(
        success=True,
        resource=skill,
        warnings=["Template outdated"]
    )
```

**Use Typed Tuples for Multiple Values:**
```python
from typing import NamedTuple

class ValidationResult(NamedTuple):
    is_valid: bool
    errors: List[str]
    warnings: List[str]

def validate_config(config: Dict) -> ValidationResult:
    """Validate configuration."""
    return ValidationResult(
        is_valid=True,
        errors=[],
        warnings=["Using default value"]
    )
```

**Use Union for Alternative Returns:**
```python
from typing import Union

def get_skill(name: str) -> Union[SkillConfig, None]:
    """Get skill by name or None if not found."""
    pass

# Or with Result pattern
from typing import Result  # Python 3.13+

def get_skill(name: str) -> Result[SkillConfig, NotFoundError]:
    """Get skill by name or error."""
    pass
```

### Error Handling

**Define Specific Exceptions:**
```python
class SkillBuilderError(Exception):
    """Base exception for skill builder."""
    pass

class ValidationError(SkillBuilderError):
    """Validation failed."""

    def __init__(self, message: str, errors: List[str]):
        super().__init__(message)
        self.errors = errors

class SkillNotFoundError(SkillBuilderError):
    """Skill not found."""

    def __init__(self, name: str):
        super().__init__(f"Skill not found: {name}")
        self.skill_name = name
```

**Document Exceptions:**
```python
def delete_skill(name: str) -> None:
    """
    Delete skill by name.

    Args:
        name: Skill name to delete

    Raises:
        SkillNotFoundError: If skill doesn't exist
        PermissionError: If lacking write permissions
        IOError: If file deletion fails

    Example:
        >>> delete_skill("old-skill")
        >>> # Raises SkillNotFoundError if not found
    """
    pass
```

---

## REST API Design (If Applicable)

### Resource Naming

**Use Nouns, Not Verbs:**
```
✅ Good:
GET    /skills
GET    /skills/{id}
POST   /skills
PUT    /skills/{id}
DELETE /skills/{id}

❌ Avoid:
GET    /getSkills
POST   /createSkill
POST   /deleteSkill
```

**Use Plural for Collections:**
```
✅ /skills/{id}
❌ /skill/{id}
```

**Nested Resources for Relationships:**
```
/skills/{skill-id}/templates
/skills/{skill-id}/templates/{template-id}
```

### HTTP Methods

| Method | Action | Example | Idempotent |
|--------|--------|---------|------------|
| GET | Retrieve | `GET /skills/{id}` | Yes |
| POST | Create | `POST /skills` | No |
| PUT | Replace | `PUT /skills/{id}` | Yes |
| PATCH | Update | `PATCH /skills/{id}` | No |
| DELETE | Remove | `DELETE /skills/{id}` | Yes |

### Request/Response Format

**Request Body (POST /skills):**
```json
{
  "name": "analysis",
  "description": "Analyze feature requirements",
  "allowed_tools": ["Read", "Grep", "Bash"],
  "template": "basic"
}
```

**Success Response (201 Created):**
```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "analysis",
    "description": "Analyze feature requirements",
    "allowed_tools": ["Read", "Grep", "Bash"],
    "template": "basic",
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  },
  "meta": {
    "version": "1.0",
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "name",
        "issue": "Name must be alphanumeric with hyphens",
        "value": "invalid name!"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

### Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, PATCH, DELETE |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE (no response body) |
| 400 | Bad Request | Validation error, malformed request |
| 401 | Unauthorized | Authentication required/failed |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource already exists, version conflict |
| 422 | Unprocessable Entity | Valid request, business logic error |
| 500 | Internal Server Error | Unexpected server error |

### Pagination

**Query Parameters:**
```
GET /skills?limit=20&offset=0
GET /skills?page=1&per_page=20
GET /skills?cursor=abc123
```

**Response with Pagination:**
```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "has_more": true,
    "next_cursor": "abc123"
  },
  "links": {
    "self": "/skills?limit=20&offset=0",
    "next": "/skills?limit=20&offset=20",
    "prev": null
  }
}
```

### Filtering & Sorting

**Query Parameters:**
```
GET /skills?scope=global&template=advanced
GET /skills?sort=created_at&order=desc
GET /skills?search=analysis
```

### Versioning

**URL Versioning (Recommended for this project):**
```
/api/v1/skills
/api/v2/skills
```

**Header Versioning:**
```
GET /skills
Accept: application/vnd.llms.v1+json
```

---

## Pydantic Models for API Contracts

### Request Models

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class CreateSkillRequest(BaseModel):
    """Request to create a new skill."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        regex=r"^[a-z0-9-]+$",
        description="Skill name (lowercase, alphanumeric, hyphens)"
    )

    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Clear description of what the skill does"
    )

    allowed_tools: Optional[List[str]] = Field(
        default=None,
        description="List of allowed tool names"
    )

    template: str = Field(
        default="basic",
        description="Template to use for skill generation"
    )

    @validator("allowed_tools")
    def validate_tools(cls, v):
        """Validate tool names against whitelist."""
        if v is None:
            return v

        valid_tools = ["Read", "Write", "Edit", "Bash", "Grep"]
        invalid = [tool for tool in v if tool not in valid_tools]

        if invalid:
            raise ValueError(f"Invalid tools: {invalid}")

        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "analysis",
                "description": "Analyze feature requirements",
                "allowed_tools": ["Read", "Grep"],
                "template": "basic"
            }
        }
```

### Response Models

```python
from datetime import datetime
from uuid import UUID

class SkillResponse(BaseModel):
    """Response with skill details."""

    id: UUID
    name: str
    description: str
    allowed_tools: List[str]
    template: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # For SQLAlchemy compatibility
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "analysis",
                "description": "Analyze feature requirements",
                "allowed_tools": ["Read", "Grep", "Bash"],
                "template": "basic",
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T10:30:00Z"
            }
        }
```

### Error Models

```python
class ErrorDetail(BaseModel):
    """Error detail for a specific field."""
    field: str
    issue: str
    value: Optional[Any] = None

class ErrorResponse(BaseModel):
    """Standard error response."""
    code: str
    message: str
    details: Optional[List[ErrorDetail]] = None
```

---

## API Documentation

### Docstring Standards

Use **Google-style docstrings** consistently:

```python
def function_name(param1: str, param2: int = 0) -> bool:
    """
    Short description (one line).

    Longer description if needed. Explain the purpose, behavior,
    and any important details.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when this is raised
        IOError: Description of when this is raised

    Examples:
        >>> function_name("test", 42)
        True

        >>> function_name("invalid")
        False

    Note:
        Additional notes or warnings

    See Also:
        related_function: Related functionality
    """
    pass
```

### OpenAPI/Swagger (For REST APIs)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="LLM Config Management API",
    description="API for managing skills, commands, and agents",
    version="1.0.0"
)

@app.post(
    "/skills",
    response_model=SkillResponse,
    status_code=201,
    summary="Create a new skill",
    description="Create a new skill with the provided configuration",
    tags=["Skills"]
)
async def create_skill(request: CreateSkillRequest) -> SkillResponse:
    """
    Create a new skill.

    - **name**: Unique skill identifier
    - **description**: What the skill does
    - **allowed_tools**: Tools the skill can use
    - **template**: Template to use for generation
    """
    # Implementation
    pass
```

---

## Best Practices Summary

### For Python Functions

1. **Type Everything**: Use type hints for all parameters and returns
2. **Document Everything**: Docstrings with Args, Returns, Raises, Examples
3. **Validate Early**: Check inputs at function boundaries
4. **Return Meaningfully**: Use Pydantic models or NamedTuples for complex returns
5. **Handle Errors**: Define specific exceptions, document what's raised
6. **Keep It Simple**: One function = one responsibility
7. **Use Defaults**: Sensible defaults for optional parameters
8. **Keyword-Only**: Use `*` for clarity in complex signatures

### For REST APIs

1. **RESTful Resources**: Use nouns, standard HTTP methods
2. **Consistent Responses**: Standard format for success/error
3. **Status Codes**: Use correct HTTP status codes
4. **Version APIs**: From day one (v1, v2, etc.)
5. **Validate Inputs**: Use Pydantic models
6. **Paginate Collections**: Always paginate list endpoints
7. **Document APIs**: OpenAPI/Swagger documentation
8. **Security First**: Authentication, authorization, rate limiting

---

## Anti-Patterns to Avoid

### ❌ Boolean Trap
```python
# Bad: What does True mean?
create_skill("analysis", True, False, True)

# Good: Clear keyword arguments
create_skill(
    name="analysis",
    overwrite=True,
    dry_run=False,
    verbose=True
)
```

### ❌ Returning None for Errors
```python
# Bad: Caller must check for None
result = get_skill("unknown")  # Returns None
if result is None:
    # Error handling

# Good: Raise exception
try:
    result = get_skill("unknown")
except SkillNotFoundError:
    # Error handling
```

### ❌ Mutable Default Arguments
```python
# Bad: Default list is shared across calls!
def create_skill(allowed_tools=[]):
    allowed_tools.append("Read")

# Good: Use None and create new list
def create_skill(allowed_tools: Optional[List[str]] = None):
    if allowed_tools is None:
        allowed_tools = []
    allowed_tools.append("Read")
```

### ❌ Inconsistent Naming
```python
# Bad: Inconsistent verb usage
def get_skill()
def retrieve_command()
def fetch_agent()

# Good: Consistent vocabulary
def get_skill()
def get_command()
def get_agent()
```

---

## References

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [REST API Design Best Practices](https://restfulapi.net/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
