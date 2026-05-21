"""
Pydantic Schema Examples

Comprehensive examples for data model design patterns.
"""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Set, Union

from pydantic import (
    BaseModel,
    Field,
    constr,
    conint,
    confloat,
    conlist,
    validator,
    root_validator,
)
import re


# =============================================================================
# Enumerations
# =============================================================================


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"


class ProductStatus(str, Enum):
    """Product status enum."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


# =============================================================================
# Custom Constrained Types
# =============================================================================

Username = constr(regex=r"^[a-zA-Z0-9_-]+$", min_length=3, max_length=50)
PositiveInt = conint(gt=0)
Percentage = confloat(ge=0.0, le=100.0)
NonEmptyList = conlist(str, min_items=1)


# =============================================================================
# Nested Models
# =============================================================================


class Address(BaseModel):
    """Nested address model."""

    street: str = Field(..., description="Street address", min_length=1, max_length=200)
    city: str = Field(..., description="City name", min_length=1, max_length=100)
    state: str = Field(
        ..., description="State/province code", min_length=2, max_length=2
    )
    postal_code: str = Field(
        ..., description="Postal/ZIP code", regex=r"^\d{5}(-\d{4})?$"
    )
    country: str = Field(default="US", description="Country code (ISO 3166-1 alpha-2)")

    class Config:
        schema_extra = {
            "example": {
                "street": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "postal_code": "62701",
                "country": "US",
            }
        }


class ProductDimensions(BaseModel):
    """Product dimensions (nested model)."""

    length: confloat(gt=0)
    width: confloat(gt=0)
    height: confloat(gt=0)
    unit: Literal["cm", "in", "m"]

    @property
    def volume(self) -> float:
        """Calculate volume."""
        return self.length * self.width * self.height


# =============================================================================
# Main Entity Models
# =============================================================================


class User(BaseModel):
    """User data model with comprehensive validation."""

    # Identity fields
    id: Optional[int] = Field(None, description="User ID (auto-generated)")
    username: str = Field(
        ..., description="Unique username", min_length=3, max_length=50
    )
    email: str = Field(..., description="Email address (validated)")

    # Profile fields
    full_name: str = Field(
        ..., description="User's full name", min_length=1, max_length=200
    )
    role: UserRole = Field(default=UserRole.USER, description="User role")
    is_active: bool = Field(default=True, description="Account active status")

    # Nested model
    address: Optional[Address] = Field(None, description="Mailing address")

    # Lists
    tags: List[str] = Field(default_factory=list, description="User tags")

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    @validator("email")
    def validate_email(cls, v):
        """Validate email format."""
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v.lower()

    @validator("username")
    def validate_username(cls, v):
        """Validate username format."""
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username must contain only letters, numbers, hyphens, and underscores"
            )
        reserved = ["admin", "root", "system"]
        if v.lower() in reserved:
            raise ValueError(f'Username "{v}" is reserved')
        return v.lower()

    class Config:
        orm_mode = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "role": "user",
                "address": {
                    "street": "123 Main St",
                    "city": "Springfield",
                    "state": "IL",
                    "postal_code": "62701",
                },
                "tags": ["verified", "premium"],
            }
        }


# =============================================================================
# Registration with Cross-Field Validation
# =============================================================================


class UserRegistration(BaseModel):
    """User registration with comprehensive validation."""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(...)
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(..., min_length=8)
    age: int = Field(..., ge=13, le=120)
    phone: Optional[str] = Field(None)

    @validator("password")
    def validate_password_strength(cls, v):
        """Validate password strength."""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        """Validate phone number format."""
        if v is None:
            return v
        digits = re.sub(r"\D", "", v)
        if len(digits) != 10:
            raise ValueError("Phone number must be 10 digits")
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

    @root_validator
    def validate_passwords_match(cls, values):
        """Validate that passwords match (cross-field validation)."""
        password = values.get("password")
        password_confirm = values.get("password_confirm")
        if password != password_confirm:
            raise ValueError("Passwords do not match")
        return values


# =============================================================================
# Complex Business Logic Validation
# =============================================================================


class EventBooking(BaseModel):
    """Event booking with complex validation."""

    event_name: str = Field(...)
    start_date: date = Field(...)
    end_date: date = Field(...)
    attendees: int = Field(..., ge=1, le=1000)
    room_capacity: int = Field(..., ge=1)
    is_catering: bool = Field(default=False)
    catering_headcount: Optional[int] = Field(None, ge=1)

    @root_validator(pre=True)
    def convert_date_strings(cls, values):
        """Pre-validation: Convert date strings to date objects."""
        for field in ["start_date", "end_date"]:
            if field in values and isinstance(values[field], str):
                values[field] = datetime.strptime(values[field], "%Y-%m-%d").date()
        return values

    @root_validator
    def validate_dates(cls, values):
        """Validate date logic."""
        start = values.get("start_date")
        end = values.get("end_date")

        if start and end:
            if end < start:
                raise ValueError("End date must be after start date")
            if (end - start).days > 30:
                raise ValueError("Event duration cannot exceed 30 days")
            if start < date.today():
                raise ValueError("Event cannot be in the past")
        return values

    @root_validator
    def validate_capacity(cls, values):
        """Validate room capacity vs attendees."""
        attendees = values.get("attendees")
        capacity = values.get("room_capacity")
        if attendees and capacity and attendees > capacity:
            raise ValueError(
                f"Attendees ({attendees}) exceeds room capacity ({capacity})"
            )
        return values

    @root_validator
    def validate_catering(cls, values):
        """Validate catering requirements."""
        is_catering = values.get("is_catering")
        catering_headcount = values.get("catering_headcount")
        attendees = values.get("attendees")

        if is_catering:
            if not catering_headcount:
                raise ValueError("Catering headcount required when catering is enabled")
            if catering_headcount > attendees:
                raise ValueError("Catering headcount cannot exceed number of attendees")
        elif catering_headcount:
            raise ValueError("Catering headcount specified but catering is disabled")
        return values


# =============================================================================
# Product with Advanced Types
# =============================================================================


class Product(BaseModel):
    """Product model with advanced type annotations."""

    id: Optional[int] = None
    name: constr(min_length=1, max_length=200)
    sku: constr(regex=r"^[A-Z]{3}-\d{6}$")  # Format: ABC-123456

    price: confloat(gt=0.0, le=1000000.0)
    discount_percentage: Percentage = 0.0
    stock_quantity: PositiveInt

    status: ProductStatus = ProductStatus.DRAFT

    tags: List[str] = Field(default_factory=list)
    categories: Set[str] = Field(default_factory=set)
    attributes: Dict[str, Any] = Field(default_factory=dict)

    metadata: Union[Dict[str, str], None] = None
    measurement_unit: Literal["kg", "lb", "oz", "g"]

    dimensions: Optional[ProductDimensions] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


# =============================================================================
# Relationship Patterns
# =============================================================================


# One-to-One
class UserProfile(BaseModel):
    """User profile (one-to-one with User)."""

    user_id: int = Field(..., description="Foreign key to User")
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None

    @validator("avatar_url")
    def validate_avatar_url(cls, v):
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("Avatar URL must be HTTP/HTTPS")
        return v


# One-to-Many
class Comment(BaseModel):
    """Comment (many comments per post)."""

    id: int
    post_id: int = Field(..., description="Foreign key to Post")
    content: str
    created_at: datetime


class Post(BaseModel):
    """Post with many comments."""

    id: int
    title: str
    content: str
    comments: List[Comment] = Field(default_factory=list)


# Many-to-Many
class Tag(BaseModel):
    """Tag entity."""

    id: int
    name: str


class Article(BaseModel):
    """Article with many tags."""

    id: int
    title: str
    tag_ids: List[int] = Field(default_factory=list)  # Reference by ID
    tags: List[Tag] = Field(default_factory=list)  # Embedded tags


# =============================================================================
# Serialization Control
# =============================================================================


class ApiResponse(BaseModel):
    """API response with serialization control."""

    id: int
    name: str
    internal_code: str = Field(..., alias="code")
    created_at: datetime
    secret_key: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


# Usage examples:
# response = ApiResponse(id=1, name="Test", code="ABC123", created_at=datetime.utcnow())
# data = response.dict(exclude={'secret_key'})
# json_str = response.json(by_alias=True, exclude={'secret_key'})
