---
name: best-practices-catalog
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Best Practices Catalog

## Overview

This catalog provides common best practices for popular libraries and frameworks. Use these as a reference when analyzing documentation and extracting implementation guidance.

---

## Python Best Practices

### FastAPI

**General Best Practices:**
```python
# ✅ Use async def for I/O-bound operations
@app.get("/items/")
async def read_items():
    items = await async_db_query("SELECT * FROM items")
    return items

# ❌ Don't use blocking I/O in async functions
@app.get("/items/")
async def read_items():
    items = blocking_db_query("SELECT * FROM items")  # Blocks event loop!
    return items
```

**Dependency Injection:**
```python
# ✅ Use dependency injection for resources
from fastapi import Depends

async def get_db():
    db = Database()
    try:
        yield db
    finally:
        await db.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    return await db.fetch_all("SELECT * FROM items")

# ❌ Don't create resources globally
db = Database()  # Global state, hard to test!

@app.get("/items/")
async def read_items():
    return await db.fetch_all("SELECT * FROM items")
```

**Request Validation:**
```python
# ✅ Use Pydantic models for validation
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)

@app.post("/items/")
async def create_item(item: ItemCreate):
    return item

# ❌ Don't use dict for validation
@app.post("/items/")
async def create_item(item: dict):  # No validation!
    return item
```

### Pydantic

**Model Design:**
```python
# ✅ Use Field for validation and documentation
from pydantic import BaseModel, Field, validator

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="User's username")
    email: str = Field(..., description="User's email address")
    age: int = Field(..., ge=0, le=150, description="User's age")

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

# ❌ Don't skip validation
class User(BaseModel):
    username: str
    email: str
    age: int
```

### Pytest

**Test Organization:**
```python
# ✅ Use fixtures for common setup
import pytest

@pytest.fixture
async def db_session():
    session = await create_test_db()
    yield session
    await session.close()

async def test_user_creation(db_session):
    user = await create_user(db_session, "testuser")
    assert user.username == "testuser"

# ❌ Don't repeat setup in every test
async def test_user_creation():
    session = await create_test_db()  # Repeated!
    user = await create_user(session, "testuser")
    await session.close()
    assert user.username == "testuser"
```

---

## TypeScript/JavaScript Best Practices

### React

**Component Design:**
```typescript
// ✅ Use functional components with hooks
import { useState, useEffect } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  return <div>{user?.name}</div>;
}

// ❌ Don't use class components for new code
class UserProfile extends React.Component {
  // Legacy pattern, prefer functional components
}
```

**State Management:**
```typescript
// ✅ Use context for global state
import { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Click me</button>;
}

// ❌ Don't prop drill through multiple levels
function App() {
  const [theme, setTheme] = useState('light');
  return <Level1 theme={theme} />; // Props passed through many levels
}
```

### Jest

**Test Structure:**
```typescript
// ✅ Use describe blocks for organization
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      const user = await createUser({ name: 'Test' });
      expect(user.name).toBe('Test');
    });

    it('should throw error with invalid data', async () => {
      await expect(createUser({})).rejects.toThrow();
    });
  });
});

// ❌ Don't have flat, unorganized tests
it('test 1', () => { /* ... */ });
it('test 2', () => { /* ... */ });
it('test 3', () => { /* ... */ });
```

---

## Security Best Practices

### Authentication

**JWT Handling:**
```python
# ✅ Use secure token storage and validation
from jose import JWTError, jwt
from datetime import datetime, timedelta

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# ❌ Don't store sensitive data in tokens
def create_access_token(user_data: dict):
    # Don't include passwords, credit cards, etc.!
    return jwt.encode(user_data, SECRET_KEY)
```

### Input Validation

**Sanitization:**
```python
# ✅ Validate and sanitize all input
from pydantic import BaseModel, Field, validator
import re

class UserInput(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v

# ❌ Don't trust user input
def create_user(username: str):  # No validation!
    db.execute(f"INSERT INTO users VALUES ('{username}')")  # SQL injection risk!
```

### Password Security

**Hashing:**
```python
# ✅ Use proper password hashing
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ❌ Don't store plaintext or use weak hashing
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()  # Weak!
```

---

## Performance Best Practices

### Database Operations

**Query Optimization:**
```python
# ✅ Use connection pooling and async operations
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=0
)

async def get_users():
    async with engine.begin() as conn:
        result = await conn.execute("SELECT * FROM users LIMIT 100")
        return result.fetchall()

# ❌ Don't create new connections for each query
def get_users():
    conn = create_connection()  # New connection every time!
    result = conn.execute("SELECT * FROM users")
    conn.close()
    return result
```

**N+1 Query Problem:**
```python
# ✅ Use eager loading
from sqlalchemy.orm import selectinload

users = session.query(User).options(selectinload(User.posts)).all()

# ❌ Don't lazy load in loops
users = session.query(User).all()
for user in users:
    posts = user.posts  # N+1 queries!
```

### Caching

**Cache Strategy:**
```python
# ✅ Use caching for expensive operations
from functools import lru_cache
from datetime import timedelta

@lru_cache(maxsize=128)
def get_expensive_data(key: str):
    # Expensive computation
    return compute_result(key)

# ❌ Don't recompute on every request
def get_expensive_data(key: str):
    return compute_result(key)  # No caching!
```

---

## Testing Best Practices

### Test Organization

**AAA Pattern:**
```python
# ✅ Follow Arrange-Act-Assert pattern
def test_user_creation():
    # Arrange
    user_data = {"username": "test", "email": "test@example.com"}

    # Act
    user = create_user(user_data)

    # Assert
    assert user.username == "test"
    assert user.email == "test@example.com"

# ❌ Don't mix concerns
def test_user_creation():
    user = create_user({"username": "test"})  # Unclear structure
    assert user.username == "test"
    user2 = create_user({"username": "test2"})  # Multiple tests in one!
    assert user2.username == "test2"
```

### Mocking

**Dependency Injection for Tests:**
```python
# ✅ Use dependency injection for testability
from unittest.mock import Mock

async def test_user_service():
    # Mock database
    mock_db = Mock()
    mock_db.fetch_user.return_value = {"id": 1, "name": "Test"}

    # Inject mock
    service = UserService(db=mock_db)
    user = await service.get_user(1)

    assert user["name"] == "Test"
    mock_db.fetch_user.assert_called_once_with(1)

# ❌ Don't use global state
db = Database()  # Global, hard to mock!

async def test_user_service():
    service = UserService()  # Uses global db
    user = await service.get_user(1)  # Can't control db behavior!
```

---

## Error Handling Best Practices

### Exception Hierarchy

**Custom Exceptions:**
```python
# ✅ Create exception hierarchy
class APIException(Exception):
    """Base exception for API errors."""
    pass

class ValidationError(APIException):
    """Validation failed."""
    pass

class NotFoundError(APIException):
    """Resource not found."""
    pass

class AuthenticationError(APIException):
    """Authentication failed."""
    pass

# ❌ Don't use generic exceptions
raise Exception("Something went wrong")  # Too generic!
```

### Error Recovery

**Retry Logic:**
```python
# ✅ Implement retry with exponential backoff
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def fetch_external_api():
    response = await httpx.get("https://api.example.com/data")
    return response.json()

# ❌ Don't fail immediately on transient errors
async def fetch_external_api():
    response = await httpx.get("https://api.example.com/data")  # No retry!
    return response.json()
```

---

## Code Organization Best Practices

### File Structure

**Modular Organization:**
```
# ✅ Organize by feature
src/
├── users/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   └── schemas.py
├── posts/
│   ├── __init__.py
│   ├── models.py
│   └── ...
└── core/
    ├── config.py
    └── database.py

# ❌ Don't organize by type only
src/
├── models/
│   ├── user.py
│   ├── post.py
├── routes/
│   ├── user.py
│   ├── post.py
└── services/
    ├── user.py
    ├── post.py
```

### Dependency Management

**Clean Dependencies:**
```python
# ✅ Use dependency injection
class UserService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache

    async def get_user(self, user_id: int):
        # Service logic
        pass

# ❌ Don't import globals
from app.database import db  # Global dependency!

class UserService:
    async def get_user(self, user_id: int):
        return await db.fetch_user(user_id)
```

---

## Documentation Best Practices

### Code Documentation

**Docstrings:**
```python
# ✅ Use comprehensive docstrings
def create_user(username: str, email: str) -> User:
    """
    Create a new user with the given username and email.

    Args:
        username: Unique username (3-50 characters)
        email: Valid email address

    Returns:
        User: Created user object

    Raises:
        ValidationError: If username or email is invalid
        DuplicateError: If username already exists

    Example:
        >>> user = create_user("john", "john@example.com")
        >>> print(user.username)
        'john'
    """
    pass

# ❌ Don't skip documentation
def create_user(username, email):
    pass  # What does this do?
```

---

**Version:** 2.0.0
**Last Updated:** 2025-10-29
**Maintainer:** Documentation Researcher Agent
