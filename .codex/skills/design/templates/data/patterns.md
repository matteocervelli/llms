# Data Modeling — Patterns

## Validation Patterns

### Field-Level Validation

```python
from pydantic import constr, conint, confloat

Username = constr(regex=r'^[a-z0-9_]+$', min_length=3, max_length=50)
PositiveInt = conint(gt=0)
Percentage = confloat(ge=0.0, le=100.0)

class User(BaseModel):
    username: Username
    age: PositiveInt
    score: Percentage
```

### Custom Validators

```python
@validator('email')
def validate_email(cls, v):
    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
        raise ValueError('Invalid email')
    return v.lower()
```

### Cross-Field Validation

```python
@root_validator
def validate_date_range(cls, values):
    start = values.get('start_date')
    end = values.get('end_date')
    if start and end and start >= end:
        raise ValueError('start_date must be before end_date')
    return values
```

## Relationship Patterns

### One-to-One (Embedded)

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    address: Optional[Address] = None  # Embedded
```

### One-to-Many (ID Reference)

```python
class Comment(BaseModel):
    id: int
    post_id: int = Field(..., description="FK to Post")
    content: str

class Post(BaseModel):
    id: int
    comments: List[Comment] = Field(default_factory=list)
```

### Many-to-Many (ID List)

```python
class Article(BaseModel):
    id: int
    tag_ids: List[int] = Field(default_factory=list)
```

## Schema Separation Pattern

```python
# Creation — required fields, no ID
class UserCreate(BaseModel):
    username: str
    email: str

# Response — includes ID + computed fields
class UserResponse(UserCreate):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        orm_mode = True

# Update — all optional
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
```

## Enum Pattern for Choices

```python
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class User(BaseModel):
    status: Status = Status.ACTIVE
```

## Serialization Control

```python
class Config:
    orm_mode = True              # Enable from_orm()
    use_enum_values = True       # Serialize enums as values
    json_encoders = {
        datetime: lambda v: v.isoformat()
    }
    schema_extra = {
        "example": {"username": "johndoe", "email": "john@example.com"}
    }
```

## Best Practices

- **Validate at boundaries** — input from users/APIs, not internal calls
- **Use enums** — never magic strings for constrained choices
- **Field() for everything** — descriptions, constraints, defaults
- **Separate create/response/update** — different schemas for different operations
- **Test edge cases** — empty strings, None vs missing, boundary values
