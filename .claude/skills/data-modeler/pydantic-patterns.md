# Pydantic Patterns and Examples

This guide provides comprehensive Pydantic-specific patterns, advanced techniques, and complete code examples.

## Table of Contents

1. [BaseModel Advanced Usage](#basemodel-advanced-usage)
2. [Custom Validators](#custom-validators)
3. [Field Validators with Dependencies](#field-validators-with-dependencies)
4. [Root Validators](#root-validators)
5. [Config Options](#config-options)
6. [Nested Models](#nested-models)
7. [Serialization and Deserialization](#serialization-and-deserialization)
8. [ORM Mode](#orm-mode)

---

## BaseModel Advanced Usage

### Basic BaseModel

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    """Basic Pydantic model."""
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Create instance
user = User(username="john", email="john@example.com")

# Access fields
print(user.username)  # "john"
print(user.created_at)  # datetime object

# Convert to dict
data = user.dict()

# Convert to JSON
json_str = user.json()
```

### Model Inheritance

```python
from pydantic import BaseModel, Field
from datetime import datetime

class TimestampedModel(BaseModel):
    """Base model with timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class AuditedModel(TimestampedModel):
    """Base model with audit fields."""
    created_by: Optional[int] = None
    updated_by: Optional[int] = None

class User(AuditedModel):
    """User inherits timestamps and audit fields."""
    id: Optional[int] = None
    username: str
    email: str

# User automatically has: created_at, updated_at, created_by, updated_by
user = User(username="john", email="john@example.com", created_by=1)
```

### Model Copy and Update

```python
user = User(id=1, username="john", email="john@example.com")

# Create copy
user_copy = user.copy()

# Create copy with updates
user_updated = user.copy(update={"email": "newemail@example.com"})

# Deep copy (for nested models)
user_deep_copy = user.copy(deep=True)

# Exclude fields from copy
user_partial = user.copy(exclude={"id"})
```

### Parse Objects

```python
# From dict
data = {"username": "john", "email": "john@example.com"}
user = User(**data)

# From JSON string
json_str = '{"username": "john", "email": "john@example.com"}'
user = User.parse_raw(json_str)

# From file
user = User.parse_file("user.json")
```

---

## Custom Validators

### Basic @validator

```python
from pydantic import BaseModel, validator
import re

class User(BaseModel):
    username: str
    email: str

    @validator('username')
    def validate_username(cls, v):
        """Validate username format."""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v  # Return transformed value

    @validator('email')
    def validate_email(cls, v):
        """Validate email format."""
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()  # Normalize to lowercase
```

### Multiple Field Validator

```python
class User(BaseModel):
    first_name: str
    last_name: str
    email: str

    @validator('first_name', 'last_name')
    def validate_name_fields(cls, v):
        """Apply same validation to multiple fields."""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        if len(v) > 50:
            raise ValueError('Name too long')
        return v.strip().title()  # Normalize to Title Case
```

### Validator with each_item

```python
class Product(BaseModel):
    tags: List[str]

    @validator('tags', each_item=True)
    def validate_tag(cls, v):
        """Validate each tag individually."""
        if not v or not v.strip():
            raise ValueError('Tag cannot be empty')
        return v.lower().strip()

# Usage
product = Product(tags=["Python", " Django ", "Web"])
# tags become: ["python", "django", "web"]
```

### Validator with pre=True

```python
class User(BaseModel):
    age: int

    @validator('age', pre=True)
    def convert_age(cls, v):
        """Pre-validator: Convert before type validation."""
        if isinstance(v, str):
            # Convert string to int before Pydantic validates type
            return int(v)
        return v

# Usage
user = User(age="25")  # String converted to int
```

### Validator with always=True

```python
class User(BaseModel):
    full_name: Optional[str] = None

    @validator('full_name', always=True)
    def set_default_full_name(cls, v):
        """Validator runs even if field not provided."""
        if v is None:
            return "Unknown"
        return v

# Usage
user = User()
print(user.full_name)  # "Unknown"
```

---

## Field Validators with Dependencies

### Accessing Other Fields

```python
class Password(BaseModel):
    password: str
    password_confirm: str

    @validator('password_confirm')
    def passwords_match(cls, v, values):
        """Access previous fields using 'values' parameter."""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
```

### Complex Cross-Field Logic

```python
from datetime import date

class DateRange(BaseModel):
    start_date: date
    end_date: date
    duration_days: Optional[int] = None

    @validator('end_date')
    def validate_end_after_start(cls, v, values):
        """Validate end_date is after start_date."""
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

    @validator('duration_days', always=True)
    def calculate_duration(cls, v, values):
        """Calculate duration if not provided."""
        if v is not None:
            return v  # User provided duration

        # Calculate from dates
        if 'start_date' in values and 'end_date' in values:
            start = values['start_date']
            end = values['end_date']
            return (end - start).days

        return None
```

---

## Root Validators

### Basic Root Validator

```python
from pydantic import BaseModel, root_validator

class Booking(BaseModel):
    check_in: date
    check_out: date
    guests: int
    room_capacity: int

    @root_validator
    def validate_booking(cls, values):
        """Validate multiple fields together."""
        check_in = values.get('check_in')
        check_out = values.get('check_out')
        guests = values.get('guests')
        capacity = values.get('room_capacity')

        # Validate dates
        if check_in and check_out and check_out <= check_in:
            raise ValueError('Check-out must be after check-in')

        # Validate capacity
        if guests and capacity and guests > capacity:
            raise ValueError(f'Guests ({guests}) exceeds capacity ({capacity})')

        return values
```

### Root Validator with pre=True

```python
class User(BaseModel):
    name: str
    email: str

    @root_validator(pre=True)
    def preprocess_data(cls, values):
        """Transform raw input before any validation."""
        # Convert all string values to lowercase
        return {k: v.lower() if isinstance(v, str) else v for k, v in values.items()}

# Usage
user = User(name="JOHN", email="JOHN@EXAMPLE.COM")
print(user.name)  # "john"
print(user.email)  # "john@example.com"
```

### Conditional Field Requirements

```python
class ShippingInfo(BaseModel):
    shipping_method: Literal["standard", "express", "pickup"]
    address: Optional[str] = None
    pickup_location: Optional[str] = None

    @root_validator
    def validate_shipping_requirements(cls, values):
        """Conditionally require fields based on shipping method."""
        method = values.get('shipping_method')

        if method in ['standard', 'express']:
            if not values.get('address'):
                raise ValueError('Address required for delivery')
            values['pickup_location'] = None  # Clear pickup if delivery

        elif method == 'pickup':
            if not values.get('pickup_location'):
                raise ValueError('Pickup location required')
            values['address'] = None  # Clear address if pickup

        return values
```

---

## Config Options

### Common Config Options

```python
from pydantic import BaseModel
from datetime import datetime, date

class User(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        # Allow ORM models (SQLAlchemy, etc.)
        orm_mode = True

        # Use enum values instead of enum objects
        use_enum_values = True

        # Validate on assignment (not just construction)
        validate_assignment = True

        # Allow population by field name or alias
        allow_population_by_field_name = True

        # Custom JSON encoders
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.strftime('%Y-%m-%d'),
        }

        # Example for OpenAPI/docs
        schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "created_at": "2025-10-29T10:00:00"
            }
        }
```

### Field Aliases

```python
class User(BaseModel):
    id: int = Field(..., alias="userId")
    full_name: str = Field(..., alias="fullName")

    class Config:
        allow_population_by_field_name = True

# Parse using alias
data = {"userId": 1, "fullName": "John Doe"}
user = User(**data)

# Access using field name
print(user.id)  # 1
print(user.full_name)  # "John Doe"

# Serialize using alias
json_data = user.json(by_alias=True)
# {"userId": 1, "fullName": "John Doe"}
```

### Private Fields

```python
class User(BaseModel):
    username: str
    _private_data: str = "secret"  # Not included in serialization

    def get_private(self):
        return self._private_data

user = User(username="john")
print(user.dict())  # {"username": "john"}
print(user.get_private())  # "secret"
```

---

## Nested Models

### Basic Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str = "US"

class User(BaseModel):
    username: str
    address: Address  # Nested model

# Create with nested data
user = User(
    username="john",
    address={
        "street": "123 Main St",
        "city": "Springfield"
    }
)

# Access nested fields
print(user.address.street)  # "123 Main St"
```

### Optional Nested Models

```python
class UserProfile(BaseModel):
    bio: Optional[str] = None
    website: Optional[str] = None

class User(BaseModel):
    username: str
    profile: Optional[UserProfile] = None  # Optional nested model

# User without profile
user1 = User(username="john")

# User with profile
user2 = User(
    username="jane",
    profile={"bio": "Software engineer"}
)
```

### Lists of Nested Models

```python
class Comment(BaseModel):
    author: str
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Post(BaseModel):
    title: str
    content: str
    comments: List[Comment] = Field(default_factory=list)

# Create post with comments
post = Post(
    title="Hello World",
    content="First post",
    comments=[
        {"author": "john", "text": "Great post!"},
        {"author": "jane", "text": "Thanks for sharing"}
    ]
)

# Access comment
print(post.comments[0].author)  # "john"
```

### Recursive Models

```python
from __future__ import annotations
from typing import Optional, List

class Category(BaseModel):
    name: str
    subcategories: List[Category] = Field(default_factory=list)

# Enable forward references
Category.update_forward_refs()

# Create hierarchical structure
root = Category(
    name="Electronics",
    subcategories=[
        Category(name="Computers", subcategories=[
            Category(name="Laptops"),
            Category(name="Desktops")
        ]),
        Category(name="Phones")
    ]
)
```

---

## Serialization and Deserialization

### dict() Method

```python
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

user = User(id=1, username="john", email="john@example.com", password="secret")

# Convert to dict
data = user.dict()

# Exclude fields
data = user.dict(exclude={'password'})
# {'id': 1, 'username': 'john', 'email': 'john@example.com'}

# Include only specific fields
data = user.dict(include={'id', 'username'})
# {'id': 1, 'username': 'john'}

# Exclude unset fields
data = user.dict(exclude_unset=True)

# Exclude None values
data = user.dict(exclude_none=True)
```

### json() Method

```python
user = User(id=1, username="john", email="john@example.com", password="secret")

# Convert to JSON string
json_str = user.json()

# With exclusions
json_str = user.json(exclude={'password'})

# Pretty print
json_str = user.json(indent=2)

# Use field aliases
json_str = user.json(by_alias=True)
```

### Custom Serialization

```python
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class Transaction(BaseModel):
    id: int
    amount: Decimal
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S'),
            Decimal: lambda v: float(v),
        }

transaction = Transaction(
    id=1,
    amount=Decimal('99.99'),
    created_at=datetime.now()
)

json_str = transaction.json()
# {"id": 1, "amount": 99.99, "created_at": "2025-10-29 10:00:00"}
```

---

## ORM Mode

### SQLAlchemy Integration

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel

# SQLAlchemy model
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100))

# Pydantic model with ORM mode
class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# Usage with SQLAlchemy
engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(engine)

with Session(engine) as session:
    # Create SQLAlchemy object
    user_db = UserDB(id=1, username="john", email="john@example.com")
    session.add(user_db)
    session.commit()

    # Convert to Pydantic
    user = User.from_orm(user_db)
    print(user.username)  # "john"
```

### Custom ORM Getters

```python
class UserDB:
    """Custom ORM-like class."""

    def __init__(self):
        self._data = {
            'id': 1,
            'username': 'john',
            'email': 'john@example.com'
        }

    def __getattr__(self, name):
        return self._data.get(name)

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# Convert custom ORM to Pydantic
user_db = UserDB()
user = User.from_orm(user_db)
print(user.dict())
```

---

## Complete Example: E-Commerce Order

```python
from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal

class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Address(BaseModel):
    """Shipping/billing address."""
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=2, max_length=2)
    postal_code: str = Field(..., regex=r'^\d{5}(-\d{4})?$')
    country: str = Field(default="US")

    class Config:
        schema_extra = {
            "example": {
                "street": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "postal_code": "62701"
            }
        }

class OrderItem(BaseModel):
    """Individual order item."""
    product_id: int = Field(..., gt=0)
    product_name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0, le=100)
    unit_price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)

    @property
    def subtotal(self) -> Decimal:
        """Calculate item subtotal."""
        return self.quantity * self.unit_price

class Order(BaseModel):
    """Complete order model."""

    # Identity
    id: Optional[int] = None
    order_number: str = Field(..., regex=r'^ORD-\d{8}$')

    # Customer info
    customer_id: int = Field(..., gt=0)
    customer_email: str = Field(...)

    # Items
    items: List[OrderItem] = Field(..., min_items=1)

    # Addresses
    shipping_address: Address
    billing_address: Optional[Address] = None

    # Pricing
    subtotal: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    tax_amount: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    shipping_cost: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    total_amount: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)

    # Status
    status: OrderStatus = OrderStatus.PENDING

    # Audit
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    @validator('customer_email')
    def validate_email(cls, v):
        """Validate email format."""
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()

    @root_validator
    def calculate_totals(cls, values):
        """Calculate order totals."""
        items = values.get('items', [])

        # Calculate subtotal
        subtotal = sum(item.subtotal for item in items)
        values['subtotal'] = subtotal

        # Calculate tax (8% for example)
        tax_rate = Decimal('0.08')
        tax_amount = subtotal * tax_rate
        values['tax_amount'] = tax_amount.quantize(Decimal('0.01'))

        # Calculate total
        shipping = values.get('shipping_cost', Decimal('0'))
        total = subtotal + tax_amount + shipping
        values['total_amount'] = total.quantize(Decimal('0.01'))

        return values

    @root_validator
    def set_billing_address(cls, values):
        """Set billing address to shipping if not provided."""
        if not values.get('billing_address'):
            values['billing_address'] = values.get('shipping_address')
        return values

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            Decimal: lambda v: str(v),
        }
        schema_extra = {
            "example": {
                "order_number": "ORD-12345678",
                "customer_id": 42,
                "customer_email": "customer@example.com",
                "items": [
                    {
                        "product_id": 1,
                        "product_name": "Widget",
                        "quantity": 2,
                        "unit_price": "19.99"
                    }
                ],
                "shipping_address": {
                    "street": "123 Main St",
                    "city": "Springfield",
                    "state": "IL",
                    "postal_code": "62701"
                },
                "shipping_cost": "5.99"
            }
        }

# Usage
order = Order(
    order_number="ORD-12345678",
    customer_id=42,
    customer_email="customer@example.com",
    items=[
        {
            "product_id": 1,
            "product_name": "Widget",
            "quantity": 2,
            "unit_price": "19.99"
        }
    ],
    shipping_address={
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "postal_code": "62701"
    },
    shipping_cost="5.99"
)

print(f"Subtotal: ${order.subtotal}")
print(f"Tax: ${order.tax_amount}")
print(f"Shipping: ${order.shipping_cost}")
print(f"Total: ${order.total_amount}")
```

---

## Summary

### Key Patterns
- Use `@validator` for field-level validation
- Use `@root_validator` for cross-field validation
- Use Config for ORM mode, aliases, custom encoders
- Use nested models for complex structures
- Use `dict()` and `json()` for serialization with exclusions

### Best Practices
- Return transformed values from validators
- Use `pre=True` for input preprocessing
- Use `always=True` for default value computation
- Enable `orm_mode` for database integration
- Provide examples in `schema_extra`
- Use constrained types for validation
- Document validation rules in docstrings
