# API Design — Patterns

## Schema Design Patterns

### Separate Schemas per Operation

```python
class ResourceCreate(BaseModel):    # POST body — all required fields
    name: str = Field(..., min_length=1, max_length=200)
    category: str

class ResourceUpdate(BaseModel):    # PATCH body — all optional
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = None

class ResourceResponse(BaseModel):  # Response — includes ID + audit
    id: int
    name: str
    category: str
    created_at: datetime
    updated_at: Optional[datetime]

class ResourceList(BaseModel):      # Paginated list response
    items: List[ResourceResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
```

## Error Response Pattern

```python
class ErrorResponse(BaseModel):
    error: str        # "validation_error", "not_found", "unauthorized"
    message: str      # Human-readable
    details: Optional[List[dict]] = None  # Field-level errors
    request_id: Optional[str] = None
```

**Status code mapping**: 400 (bad request), 401 (auth), 403 (forbidden), 404 (not found), 409 (conflict), 422 (validation), 429 (rate limit), 500 (server)

## Authentication Patterns

| Strategy       | Use When                           | Complexity |
| -------------- | ---------------------------------- | ---------- |
| **JWT Bearer** | SPA/mobile apps, stateless         | Medium     |
| **API Key**    | Service-to-service, simple         | Low        |
| **OAuth2**     | Third-party integration            | High       |
| **Session**    | Server-rendered apps (HTMX/Jinja2) | Low        |

### JWT Flow

```
POST /api/v1/auth/login → {access_token, refresh_token, expires_in}
Header: Authorization: Bearer <token>
POST /api/v1/auth/refresh → new access_token
```

### RBAC Permission Matrix

```
Resource    ADMIN       MANAGER     USER        GUEST
CREATE      ✓           ✓           ✗           ✗
READ        all         team        own         public
UPDATE      all         team        own         ✗
DELETE      all         ✗           ✗           ✗
```

## Rate Limiting

```
Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
Tiers: Anonymous (10/h), Auth (100/h), Premium (1000/h), Admin (unlimited)
429 response: {error: "rate_limit_exceeded", retry_after: N}
```

## Pagination & Filtering

```
GET /api/v1/resources?page=1&page_size=20&status=active&sort_by=created_at&sort_order=desc
```

Always paginate lists. Provide total count. Document available filters.

## Function Contract Pattern (Internal APIs)

```python
async def process_feature(
    input_data: InputModel,
    options: Optional[ProcessOptions] = None,
) -> ProcessResult:
    """Process feature. Raises ValidationError, ProcessingError."""
```

- Type-hint everything
- Document raises
- Return typed results, not dicts
- Async by default for I/O operations
