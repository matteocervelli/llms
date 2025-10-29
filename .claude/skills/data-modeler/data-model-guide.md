# Data Model Design Guide

This guide provides comprehensive principles and patterns for designing robust, maintainable data models.

## Table of Contents

1. [Entity-Relationship Principles](#entity-relationship-principles)
2. [Normalization Guidelines](#normalization-guidelines)
3. [Pydantic Model Structure](#pydantic-model-structure)
4. [Validation Strategies](#validation-strategies)
5. [Type Hints and Annotations](#type-hints-and-annotations)
6. [Field Constraints Catalog](#field-constraints-catalog)

---

## Entity-Relationship Principles

### Identifying Entities

**Entity:** A thing or object in the real world with independent existence

**Questions to identify entities:**
1. Is this a "noun" in the requirements?
2. Does it have attributes that describe it?
3. Does it have relationships with other things?
4. Would users want to create, read, update, or delete it?

**Example:**
```
Requirement: "Users can create posts with comments"

Entities:
- User (has attributes: username, email, created_at)
- Post (has attributes: title, content, author)
- Comment (has attributes: content, author, post)
```

### Entity Relationships

**One-to-One (1:1)**
- One entity instance relates to exactly one instance of another
- Example: User ↔ UserProfile

**One-to-Many (1:N)**
- One entity instance relates to many instances of another
- Example: User → Posts (one user, many posts)

**Many-to-Many (M:N)**
- Many instances of one entity relate to many instances of another
- Example: Posts ↔ Tags (posts have many tags, tags appear in many posts)

### Relationship Implementation

**Embedded (Denormalized):**
```python
class User(BaseModel):
    id: int
    username: str
    profile: UserProfile  # Embedded: profile data stored with user
```

**Referenced (Normalized):**
```python
class Post(BaseModel):
    id: int
    title: str
    author_id: int  # Reference: only store user ID
```

**When to Embed:**
- Small, related data
- Data rarely changes
- Always accessed together
- Performance is critical

**When to Reference:**
- Large related data
- Data changes frequently
- Independent lifecycle
- Avoid duplication

---

## Normalization Guidelines

### First Normal Form (1NF)

**Rule:** Each field contains atomic (indivisible) values

**❌ Violates 1NF:**
```python
class Order(BaseModel):
    id: int
    customer_name: str
    items: str = "apple,banana,orange"  # Multiple values in one field!
```

**✅ Satisfies 1NF:**
```python
class Order(BaseModel):
    id: int
    customer_name: str
    items: List[str] = ["apple", "banana", "orange"]  # Atomic values in list
```

### Second Normal Form (2NF)

**Rule:** All non-key fields depend on the entire primary key

**❌ Violates 2NF:**
```python
class OrderItem(BaseModel):
    order_id: int
    product_id: int
    product_name: str  # Depends only on product_id, not on (order_id, product_id)
    quantity: int
```

**✅ Satisfies 2NF:**
```python
class Product(BaseModel):
    id: int
    name: str  # product_name moved to Product model

class OrderItem(BaseModel):
    order_id: int
    product_id: int  # Reference to Product
    quantity: int  # Depends on both order_id and product_id
```

### Third Normal Form (3NF)

**Rule:** No transitive dependencies (non-key field depends on another non-key field)

**❌ Violates 3NF:**
```python
class Employee(BaseModel):
    id: int
    name: str
    department_id: int
    department_name: str  # Depends on department_id (transitive dependency)
```

**✅ Satisfies 3NF:**
```python
class Department(BaseModel):
    id: int
    name: str

class Employee(BaseModel):
    id: int
    name: str
    department_id: int  # Reference to Department
```

### When to Denormalize

**Reasons to denormalize:**
- Performance optimization (reduce joins)
- Read-heavy workloads
- Data rarely changes
- Acceptable data duplication

**Example: Denormalized for Performance:**
```python
class BlogPost(BaseModel):
    """Denormalized for read performance."""
    id: int
    title: str
    author_id: int
    author_name: str  # Denormalized: duplicated from User
    author_avatar: str  # Denormalized: duplicated from User
    created_at: datetime

    # Denormalization acceptable because:
    # 1. Posts are read far more than written
    # 2. Author name/avatar rarely change
    # 3. Displaying posts without joining User table is faster
```

---

## Pydantic Model Structure

### Basic Structure

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ModelName(BaseModel):
    """Model docstring explaining purpose."""

    # 1. Primary key (optional for new records)
    id: Optional[int] = Field(None, description="Primary key")

    # 2. Required fields
    name: str = Field(..., description="Required field", min_length=1, max_length=100)

    # 3. Optional fields
    description: Optional[str] = Field(None, description="Optional field")

    # 4. Fields with defaults
    is_active: bool = Field(True, description="Active status")

    # 5. Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Example Name",
                "description": "Example description"
            }
        }
```

### Field Ordering Best Practices

1. **Primary Key** (id)
2. **Required Fields** (no defaults)
3. **Optional Fields** (Optional[T])
4. **Fields with Defaults**
5. **Relationships** (foreign keys, nested models)
6. **Audit Fields** (created_at, updated_at, created_by)

### Config Class

```python
class Config:
    """Common Pydantic config options."""

    # Allow ORM models (SQLAlchemy, etc.) to be parsed
    orm_mode = True

    # Use enum values instead of enum objects in JSON
    use_enum_values = True

    # Allow population by field name or alias
    allow_population_by_field_name = True

    # Validate on assignment (not just construction)
    validate_assignment = True

    # Custom JSON encoders
    json_encoders = {
        datetime: lambda v: v.isoformat(),
        date: lambda v: v.isoformat(),
    }

    # Example for documentation
    schema_extra = {
        "example": {
            "field1": "value1",
            "field2": "value2"
        }
    }
```

---

## Validation Strategies

### Field-Level Validation

**Use `@validator` for:**
- Single field validation
- Format checking
- Value transformation
- Business rule enforcement for one field

```python
from pydantic import BaseModel, validator
import re

class User(BaseModel):
    username: str
    email: str
    age: int

    @validator('username')
    def validate_username(cls, v):
        """Username must be alphanumeric."""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v.lower()

    @validator('email')
    def validate_email(cls, v):
        """Email must be valid format."""
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()

    @validator('age')
    def validate_age(cls, v):
        """Age must be positive."""
        if v < 0:
            raise ValueError('Age must be positive')
        if v < 13:
            raise ValueError('Must be 13 or older')
        return v
```

### Model-Level Validation

**Use `@root_validator` for:**
- Cross-field validation
- Complex business rules involving multiple fields
- Conditional requirements

```python
from pydantic import BaseModel, root_validator
from datetime import date

class Event(BaseModel):
    name: str
    start_date: date
    end_date: date
    max_attendees: int
    current_attendees: int

    @root_validator
    def validate_dates_and_capacity(cls, values):
        """Validate date order and capacity."""
        start = values.get('start_date')
        end = values.get('end_date')
        max_att = values.get('max_attendees')
        current_att = values.get('current_attendees')

        # Validate dates
        if start and end and end < start:
            raise ValueError('End date must be after start date')

        # Validate capacity
        if max_att and current_att and current_att > max_att:
            raise ValueError('Current attendees cannot exceed maximum')

        return values
```

### Validation Order

1. **Field validation** (in field definition order)
2. **Custom @validator** (in decorator order)
3. **@root_validator(pre=False)** (after field validation)

```python
class ComplexModel(BaseModel):
    field1: str
    field2: int

    @validator('field1')  # Step 2: After basic type validation
    def validate_field1(cls, v):
        return v.upper()

    @root_validator(pre=True)  # Step 1: Before any field validation
    def preprocess(cls, values):
        # Transform raw input
        return values

    @root_validator  # Step 3: After all field validation
    def final_validation(cls, values):
        # Cross-field validation
        return values
```

---

## Type Hints and Annotations

### Basic Types

```python
from pydantic import BaseModel
from typing import Optional

class Example(BaseModel):
    # Primitive types
    text: str
    number: int
    decimal: float
    flag: bool

    # Optional (nullable)
    optional_text: Optional[str] = None

    # With default
    default_text: str = "default value"
```

### Collection Types

```python
from typing import List, Dict, Set, Tuple

class Collections(BaseModel):
    # List (ordered, allows duplicates)
    tags: List[str] = []

    # Dict (key-value pairs)
    metadata: Dict[str, str] = {}

    # Set (unordered, unique values)
    categories: Set[str] = set()

    # Tuple (fixed-length, immutable)
    coordinates: Tuple[float, float]  # (latitude, longitude)
```

### Advanced Types

```python
from typing import Union, Literal, Any
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Advanced(BaseModel):
    # Union (one of multiple types)
    value: Union[str, int, float]

    # Literal (specific values only)
    mode: Literal["read", "write", "admin"]

    # Enum
    status: Status

    # Any (avoid when possible)
    flexible: Any
```

### Constrained Types

```python
from pydantic import constr, conint, confloat, conlist

class Constrained(BaseModel):
    # Constrained string
    username: constr(min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$')

    # Constrained integer
    age: conint(ge=0, le=120)  # 0 <= age <= 120

    # Constrained float
    price: confloat(gt=0)  # price > 0

    # Constrained list
    items: conlist(str, min_items=1, max_items=10)
```

---

## Field Constraints Catalog

### String Constraints

```python
from pydantic import Field

class StringConstraints(BaseModel):
    # Length constraints
    short: str = Field(..., min_length=1, max_length=50)

    # Regex pattern
    code: str = Field(..., regex=r'^[A-Z]{3}-\d{4}$')

    # Example: ABC-1234
    formatted: str = Field(..., regex=r'^\(\d{3}\) \d{3}-\d{4}$')
    # Example: (555) 123-4567
```

### Numeric Constraints

```python
class NumericConstraints(BaseModel):
    # Integer constraints
    positive: int = Field(..., gt=0)  # > 0
    non_negative: int = Field(..., ge=0)  # >= 0
    bounded: int = Field(..., ge=1, le=100)  # 1 <= bounded <= 100

    # Float constraints
    price: float = Field(..., gt=0.0, le=1000000.0)
    percentage: float = Field(..., ge=0.0, le=100.0)
    precise: float = Field(..., multiple_of=0.01)  # 2 decimal places
```

### Collection Constraints

```python
class CollectionConstraints(BaseModel):
    # List constraints
    non_empty_list: List[str] = Field(..., min_items=1)
    bounded_list: List[int] = Field(..., min_items=1, max_items=10)
    unique_list: Set[str] = Field(...)  # Use Set for uniqueness

    # Dict constraints
    metadata: Dict[str, str] = Field(..., min_items=1)
```

### Date/Time Constraints

```python
from datetime import datetime, date
from pydantic import validator

class DateTimeConstraints(BaseModel):
    birth_date: date
    appointment: datetime

    @validator('birth_date')
    def validate_birth_date(cls, v):
        """Birth date must be in the past."""
        if v >= date.today():
            raise ValueError('Birth date must be in the past')
        return v

    @validator('appointment')
    def validate_appointment(cls, v):
        """Appointment must be in the future."""
        if v <= datetime.now():
            raise ValueError('Appointment must be in the future')
        return v
```

### Custom Constraints

```python
class CustomConstraints(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email_domain(cls, v):
        """Email must be from allowed domains."""
        allowed_domains = ['example.com', 'test.com']
        domain = v.split('@')[1] if '@' in v else ''
        if domain not in allowed_domains:
            raise ValueError(f'Email must be from: {", ".join(allowed_domains)}')
        return v

    @validator('password')
    def validate_password_complexity(cls, v):
        """Password must meet complexity requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
```

---

## Summary

### Entity-Relationship
- Identify entities from requirements (nouns)
- Define relationships (1:1, 1:N, M:N)
- Choose embedded vs referenced based on use case

### Normalization
- Apply 1NF, 2NF, 3NF for data integrity
- Denormalize strategically for performance
- Document denormalization decisions

### Pydantic Structure
- Order fields logically (id → required → optional → defaults → audit)
- Use Config for ORM mode, examples, encoders
- Provide clear descriptions for all fields

### Validation
- Field-level for single-field rules
- Model-level for cross-field rules
- Clear error messages for users

### Type Hints
- Use specific types, avoid Any
- Constrained types for validation
- Collections for multiple values

### Constraints
- String: min_length, max_length, regex
- Numeric: gt, ge, lt, le, multiple_of
- Collections: min_items, max_items
- Custom: @validator for business rules
