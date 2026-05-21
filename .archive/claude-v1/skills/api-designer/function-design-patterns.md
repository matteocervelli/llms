---
name: function-design-patterns
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Function Design Patterns

This guide provides comprehensive patterns for designing clean, maintainable function signatures and contracts.

## Table of Contents

1. [Function Signature Design](#function-signature-design)
2. [Parameter Patterns](#parameter-patterns)
3. [Return Type Patterns](#return-type-patterns)
4. [Error Handling](#error-handling)
5. [Async Function Patterns](#async-function-patterns)
6. [Type Hints](#type-hints)
7. [Docstring Standards](#docstring-standards)

---

## Function Signature Design

### Basic Principles

**1. Clear and Descriptive Names**
```python
# ✅ Good: Clear purpose
def calculate_user_discount(user_id: int, order_total: Decimal) -> Decimal:
    pass

# ❌ Bad: Vague name
def process(data):
    pass
```

**2. Verb-Noun Pattern**
```python
# Actions
get_user(user_id)
create_order(order_data)
update_profile(user_id, profile_data)
delete_comment(comment_id)
validate_email(email)
calculate_total(items)
```

**3. Boolean Functions Start with is/has/can**
```python
def is_active(user: User) -> bool:
    return user.status == "active"

def has_permission(user: User, permission: str) -> bool:
    return permission in user.permissions

def can_edit(user: User, resource: Resource) -> bool:
    return user.id == resource.owner_id or user.is_admin
```

### Function Length

**Keep functions small and focused:**
```python
# ✅ Good: Single responsibility, ~10 lines
def calculate_discount(user: User, order_total: Decimal) -> Decimal:
    """Calculate discount for user's order."""
    if not user.is_premium:
        return Decimal('0')

    discount_rate = Decimal('0.10')
    max_discount = Decimal('100')

    discount = order_total * discount_rate
    return min(discount, max_discount)

# ❌ Bad: Multiple responsibilities, >50 lines
def process_order(order_data: dict):
    # Validate data
    # Calculate totals
    # Apply discounts
    # Process payment
    # Send emails
    # Update inventory
    # Generate invoice
    # ... (50+ lines)
```

---

## Parameter Patterns

### Required Parameters

**Position matters for required params:**
```python
def create_user(
    username: str,
    email: str,
    full_name: str
) -> User:
    """Create user with required fields."""
    pass
```

### Optional Parameters with Defaults

**Optional params come after required:**
```python
def create_user(
    username: str,          # Required
    email: str,             # Required
    full_name: str,         # Required
    is_active: bool = True, # Optional with default
    role: str = "user",     # Optional with default
    tags: List[str] = None  # Optional with default
) -> User:
    """Create user with optional fields."""
    if tags is None:
        tags = []
    pass
```

**⚠️ Avoid mutable defaults:**
```python
# ❌ Bad: Mutable default
def add_item(items: List[str] = []) -> List[str]:
    items.append("new")
    return items

# Same list reused across calls!
result1 = add_item()  # ["new"]
result2 = add_item()  # ["new", "new"] - Oops!

# ✅ Good: None with initialization
def add_item(items: Optional[List[str]] = None) -> List[str]:
    if items is None:
        items = []
    items.append("new")
    return items
```

### Keyword-Only Parameters

**Force keyword arguments for clarity:**
```python
def create_user(
    username: str,
    email: str,
    *,  # Everything after is keyword-only
    is_active: bool = True,
    role: str = "user"
) -> User:
    """Create user with keyword-only optional params."""
    pass

# Usage
user = create_user("john", "john@example.com", is_active=True, role="admin")

# ❌ Error: Must use keywords
user = create_user("john", "john@example.com", True, "admin")
```

### Variable Arguments

***args for variable positional arguments:**
```python
def sum_numbers(*numbers: float) -> float:
    """Sum any number of arguments."""
    return sum(numbers)

result = sum_numbers(1, 2, 3, 4, 5)  # 15
```

****kwargs for variable keyword arguments:**
```python
def create_user(username: str, email: str, **metadata: Any) -> User:
    """Create user with arbitrary metadata."""
    user = User(username=username, email=email)
    user.metadata = metadata
    return user

user = create_user(
    "john",
    "john@example.com",
    department="Engineering",
    location="Remote",
    hire_date="2025-01-01"
)
```

### Parameter Ordering

**Standard order:**
```python
def function(
    required_positional,        # 1. Required positional
    required_positional_2,
    *args,                       # 2. Variable positional
    required_keyword_only,       # 3. Required keyword-only
    optional_keyword_only=None,  # 4. Optional keyword-only
    **kwargs                     # 5. Variable keyword
):
    pass
```

---

## Return Type Patterns

### Single Value Return

```python
def get_user(user_id: int) -> User:
    """Return single user object."""
    pass

def calculate_total(items: List[Item]) -> Decimal:
    """Return single calculated value."""
    pass
```

### Optional Return (None Possible)

```python
def find_user(email: str) -> Optional[User]:
    """Return user if found, None otherwise."""
    pass

def get_first_item(items: List[Item]) -> Optional[Item]:
    """Return first item or None if list empty."""
    return items[0] if items else None
```

### Multiple Values (Tuple)

```python
def get_user_stats(user_id: int) -> Tuple[int, int, float]:
    """Return (post_count, follower_count, avg_rating)."""
    pass

# Usage with unpacking
posts, followers, rating = get_user_stats(123)
```

### Named Tuple for Clarity

```python
from typing import NamedTuple

class UserStats(NamedTuple):
    """Named tuple for user statistics."""
    post_count: int
    follower_count: int
    average_rating: float

def get_user_stats(user_id: int) -> UserStats:
    """Return user statistics."""
    return UserStats(
        post_count=42,
        follower_count=1337,
        average_rating=4.5
    )

# Usage with named access
stats = get_user_stats(123)
print(stats.post_count)        # Clear what this is
print(stats.follower_count)
```

### Result Objects

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

@dataclass
class Result(Generic[T]):
    """Result wrapper for success/failure."""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None

def create_user(username: str, email: str) -> Result[User]:
    """Create user and return result."""
    try:
        user = User(username=username, email=email)
        # ... save user ...
        return Result(success=True, data=user)
    except Exception as e:
        return Result(success=False, error=str(e))

# Usage
result = create_user("john", "john@example.com")
if result.success:
    print(f"Created user: {result.data.username}")
else:
    print(f"Error: {result.error}")
```

---

## Error Handling

### Exceptions vs Return Values

**Use exceptions for exceptional conditions:**
```python
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Use return values for expected failures:**
```python
def find_user(email: str) -> Optional[User]:
    """Find user by email. Returns None if not found."""
    # Not finding a user is expected, not exceptional
    user = db.query(User).filter_by(email=email).first()
    return user
```

### Custom Exceptions

```python
class UserNotFoundError(Exception):
    """Raised when user is not found."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

def get_user(user_id: int) -> User:
    """Get user by ID.

    Raises:
        UserNotFoundError: If user doesn't exist
    """
    user = db.get(User, user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user
```

### Exception Hierarchy

```python
class APIError(Exception):
    """Base exception for API errors."""
    pass

class ValidationError(APIError):
    """Validation failed."""
    pass

class AuthenticationError(APIError):
    """Authentication failed."""
    pass

class AuthorizationError(APIError):
    """Insufficient permissions."""
    pass

class NotFoundError(APIError):
    """Resource not found."""
    pass
```

---

## Async Function Patterns

### Basic Async Function

```python
async def get_user(user_id: int) -> User:
    """Async function to get user."""
    user = await db.get(User, user_id)
    return user
```

### Async with Error Handling

```python
async def fetch_user_data(user_id: int) -> Optional[dict]:
    """Fetch user data from external API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"/users/{user_id}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch user {user_id}: {e}")
        return None
```

### Parallel Async Operations

```python
async def get_user_dashboard(user_id: int) -> Dashboard:
    """Get user dashboard with parallel data fetching."""
    # Run multiple async operations in parallel
    user, posts, notifications = await asyncio.gather(
        get_user(user_id),
        get_user_posts(user_id),
        get_user_notifications(user_id)
    )

    return Dashboard(
        user=user,
        posts=posts,
        notifications=notifications
    )
```

### Async Context Manager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_connection():
    """Async context manager for database connection."""
    conn = await db.connect()
    try:
        yield conn
    finally:
        await conn.close()

# Usage
async with get_db_connection() as conn:
    result = await conn.execute("SELECT * FROM users")
```

---

## Type Hints

### Basic Types

```python
def process_user(
    name: str,
    age: int,
    height: float,
    is_active: bool
) -> dict:
    pass
```

### Collections

```python
from typing import List, Dict, Set, Tuple

def process_items(
    items: List[str],
    metadata: Dict[str, Any],
    tags: Set[str],
    coordinates: Tuple[float, float]
) -> List[dict]:
    pass
```

### Optional and Union

```python
from typing import Optional, Union

def find_user(
    identifier: Union[int, str]  # Can be int or str
) -> Optional[User]:              # Returns User or None
    pass
```

### Generic Functions

```python
from typing import TypeVar, List

T = TypeVar('T')

def first_or_none(items: List[T]) -> Optional[T]:
    """Return first item or None."""
    return items[0] if items else None

# Works with any type
user = first_or_none(users)      # Type: Optional[User]
post = first_or_none(posts)      # Type: Optional[Post]
```

### Callable Types

```python
from typing import Callable

def apply_operation(
    value: int,
    operation: Callable[[int], int]
) -> int:
    """Apply operation function to value."""
    return operation(value)

# Usage
result = apply_operation(5, lambda x: x * 2)  # 10
```

---

## Docstring Standards

### Google Style (Recommended)

```python
def create_user(
    username: str,
    email: str,
    full_name: str,
    is_active: bool = True
) -> User:
    """Create a new user in the system.

    Creates a new user with the provided information and saves it to
    the database. Email must be unique. Username must be alphanumeric.

    Args:
        username: Unique username for the user (3-50 characters)
        email: User's email address (must be valid format)
        full_name: User's full name
        is_active: Whether the user account is active (default: True)

    Returns:
        User: The created user object with generated ID

    Raises:
        ValidationError: If username or email format is invalid
        DuplicateError: If username or email already exists

    Example:
        >>> user = create_user("johndoe", "john@example.com", "John Doe")
        >>> print(user.username)
        johndoe
    """
    pass
```

### Minimal Docstring

```python
def calculate_discount(order_total: Decimal, user: User) -> Decimal:
    """Calculate discount amount for user's order."""
    pass
```

### Complex Function Documentation

```python
async def process_payment(
    user_id: int,
    amount: Decimal,
    payment_method: str,
    metadata: Optional[Dict[str, Any]] = None
) -> PaymentResult:
    """Process payment for user.

    Processes a payment transaction using the specified payment method.
    Validates the user, amount, and payment method before proceeding.
    Creates a payment record and returns the result.

    Args:
        user_id: ID of the user making the payment
        amount: Payment amount (must be positive)
        payment_method: Payment method identifier ("card", "bank", "wallet")
        metadata: Optional additional payment information

    Returns:
        PaymentResult: Object containing:
            - transaction_id: Unique transaction identifier
            - status: Payment status ("success", "pending", "failed")
            - message: Human-readable status message

    Raises:
        UserNotFoundError: If user_id doesn't exist
        InvalidAmountError: If amount is <= 0
        InvalidPaymentMethodError: If payment_method is unsupported
        PaymentProcessingError: If payment processing fails

    Note:
        This function is idempotent. Calling it multiple times with the
        same parameters will not create duplicate charges.

    Example:
        >>> result = await process_payment(
        ...     user_id=123,
        ...     amount=Decimal("99.99"),
        ...     payment_method="card",
        ...     metadata={"card_last4": "4242"}
        ... )
        >>> print(result.status)
        success
    """
    pass
```

---

## Summary

### Function Design Checklist

**Naming:**
- ✅ Descriptive verb-noun pattern
- ✅ Boolean functions: is/has/can
- ✅ Clear purpose from name

**Parameters:**
- ✅ Required before optional
- ✅ No mutable defaults
- ✅ Type hints for all parameters
- ✅ Keyword-only for optional clarity

**Return Values:**
- ✅ Type hint for return
- ✅ Optional[T] for possible None
- ✅ Named tuples for multiple values
- ✅ Result objects for success/failure

**Error Handling:**
- ✅ Exceptions for exceptional cases
- ✅ Return values for expected failures
- ✅ Custom exceptions documented
- ✅ Exception hierarchy

**Async:**
- ✅ async/await for I/O operations
- ✅ Parallel operations with gather
- ✅ Proper error handling
- ✅ Context managers for resources

**Documentation:**
- ✅ Docstring for all public functions
- ✅ Args, Returns, Raises sections
- ✅ Examples for complex functions
- ✅ Notes for important behavior
