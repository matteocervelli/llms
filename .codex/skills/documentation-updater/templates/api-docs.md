# API Documentation Template

**Location**: `docs/api/<feature-name>-api.md`

## REST API Template

```markdown
# <Feature Name> API

## Base URL
```

https://api.example.com/v1

````

## Authentication
```bash
Authorization: Bearer <token>
````

## Endpoints

### GET /feature/resource

Get a resource.

**Request**:

```http
GET /feature/resource?param=value
Authorization: Bearer <token>
```

**Response** (200 OK):

```json
{
  "id": 1,
  "name": "example",
  "value": 123
}
```

**Error Responses**:

- `401 Unauthorized`: Missing or invalid token
- `404 Not Found`: Resource not found

### POST /feature/resource

Create a resource.

**Request**:

```http
POST /feature/resource
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "example",
  "value": 123
}
```

**Response** (201 Created):

```json
{
  "id": 1,
  "name": "example",
  "value": 123,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Rate Limiting

- Rate limit: 100 requests per minute
- Header: `X-RateLimit-Remaining`

## Error Codes

| Code | Meaning                                 |
| ---- | --------------------------------------- |
| 400  | Bad Request - Invalid input             |
| 401  | Unauthorized - Missing/invalid auth     |
| 403  | Forbidden - Insufficient permissions    |
| 404  | Not Found - Resource doesn't exist      |
| 429  | Too Many Requests - Rate limit exceeded |
| 500  | Internal Server Error                   |

````

## Python API Docstring Template

```python
def create_feature(
    name: str,
    value: int,
    options: Optional[Dict[str, Any]] = None
) -> Feature:
    """
    Create a new feature resource.

    This function creates a feature with the given name and value,
    applying optional configuration if provided.

    Args:
        name: The feature name (1-100 characters, alphanumeric)
        value: The feature value (must be non-negative)
        options: Optional configuration dict with keys:
            - timeout (int): Request timeout in seconds (default: 30)
            - retry (bool): Whether to retry on failure (default: True)

    Returns:
        Feature: Created feature instance with:
            - id: Auto-generated unique identifier
            - name: The provided name
            - value: The provided value
            - created_at: Timestamp of creation

    Raises:
        ValueError: If name is empty or value is negative
        ValidationError: If options are invalid
        APIError: If API request fails

    Examples:
        Basic usage:
        >>> feature = create_feature("example", 123)
        >>> print(feature.id)
        1

        With options:
        >>> feature = create_feature(
        ...     "example",
        ...     123,
        ...     options={"timeout": 60, "retry": False}
        ... )

    Note:
        Feature names must be unique within the system.

    See Also:
        - get_feature(): Retrieve existing feature
        - update_feature(): Modify existing feature
    """
    pass
````
