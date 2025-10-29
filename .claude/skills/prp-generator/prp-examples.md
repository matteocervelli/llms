# Product Requirements Prompt (PRP) Examples

**Purpose**: Example PRP documents showing different feature types and complexity levels.

**Version**: 2.0.0
**Phase**: 2 (Design & Planning)
**Created**: 2025-10-29

---

## Table of Contents

1. [Example 1: Simple API Feature](#example-1-simple-api-feature)
2. [Example 2: Medium Complexity Feature](#example-2-medium-complexity-feature)
3. [Example 3: Complex Multi-Component Feature](#example-3-complex-multi-component-feature)

---

## Example 1: Simple API Feature

**Feature**: User Registration API Endpoint
**Complexity**: Low
**Estimated Effort**: 8-12 hours

```markdown
# Product Requirements Prompt: User Registration API (Issue #123)

**Date**: 2025-10-29
**Designer**: Design Orchestrator (Claude Code)
**Issue**: #123 - Add user registration endpoint
**Analysis Document**: /docs/implementation/analysis/feature-123-analysis.md

---

**Status**: Ready for Implementation (Phase 3)
**Complexity**: Low
**Estimated Effort**: 8-12 hours
**Priority**: P0

---

## Executive Summary

This document provides implementation guidance for a user registration API endpoint
that allows new users to create accounts with email and password authentication.

**Architectural Approach**: Single FastAPI endpoint with service layer pattern,
using SQLAlchemy for user persistence, PassLib for password hashing, and Pydantic
for request/response validation.

**Key Libraries**: FastAPI 0.95.0 (API framework), SQLAlchemy 2.0.0 (ORM), PassLib
1.7.4 (password hashing), Pydantic 1.10.7 (validation), email-validator 2.0.0
(email validation).

**Implementation Strategy**: 2-phase approach: (1) User model and repository with
SQLAlchemy, (2) Registration endpoint with FastAPI and validation. Testing includes
unit tests with mocks and integration tests with test database.

**Key Considerations**: OWASP compliance for authentication (bcrypt with cost
factor 12), email validation, unique email constraint, password strength validation.

---

## Requirements Reference

**Source**: /docs/implementation/analysis/feature-123-analysis.md

### Functional Requirements (Summary)
- **FR-001**: System must accept user registration with email and password
- **FR-002**: System must validate email format
- **FR-003**: System must hash passwords before storage
- **FR-004**: System must return user data (excluding password) on successful registration

### Non-Functional Requirements (Summary)

#### Performance
- Registration endpoint response time < 500ms (95th percentile)

#### Security
- Passwords hashed with bcrypt (cost factor 12)
- Emails must be unique
- Password minimum length 8 characters
- HTTPS only for endpoint

#### Usability
- Clear error messages for validation failures
- Standard HTTP status codes

### Acceptance Criteria (Key Points)
- [ ] User can register with valid email and password
- [ ] Duplicate email returns 409 Conflict error
- [ ] Invalid email returns 400 Bad Request error
- [ ] Weak password returns 400 Bad Request error
- [ ] Password is not returned in response

---

## Architecture Design

### Component Overview

```
Client Request
    ↓
┌─────────────────┐
│ POST /register  │  FastAPI Endpoint
└─────────────────┘
    ↓ (Pydantic validation)
┌─────────────────┐
│ UserService     │  Business Logic
└─────────────────┘
    ↓ (PassLib hashing)
┌─────────────────┐
│ UserRepository  │  Data Access
└─────────────────┘
    ↓ (SQLAlchemy ORM)
┌─────────────────┐
│ PostgreSQL      │  Database
└─────────────────┘
```

### Components

#### Component: UserService

**Purpose**: Business logic for user operations

**Responsibilities**:
- Validate user registration data
- Hash passwords using PassLib
- Check for duplicate emails
- Coordinate with repository

**Library Integration**:
- **Primary Library**: PassLib v1.7.4
- **APIs Used**: `passlib.hash.bcrypt.hash()`
- **Pattern**: Service Layer
- **Dependencies**: passlib[bcrypt]

**Implementation Notes**:
- Use bcrypt with cost factor 12 (OWASP recommendation)
- Never log or return passwords
- Validate password strength (min 8 chars, mix of char types)

**Code Example**:
```python
from passlib.hash import bcrypt

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, email: str, password: str) -> User:
        # Check duplicate
        if self.repository.get_by_email(email):
            raise DuplicateEmailError(f"Email {email} already registered")

        # Hash password
        hashed_password = bcrypt.hash(password, rounds=12)

        # Create user
        user = User(email=email, password=hashed_password)
        return self.repository.create(user)
```

#### Component: UserRepository

**Purpose**: Data access layer for user persistence

**Responsibilities**:
- CRUD operations for User model
- Query users by email
- Handle database transactions

**Library Integration**:
- **Primary Library**: SQLAlchemy v2.0.0
- **APIs Used**: `Session.add()`, `Session.commit()`, `Session.query()`
- **Pattern**: Repository
- **Dependencies**: sqlalchemy

**Code Example**:
```python
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter_by(email=email).first()
```

### Data Models

#### Model: User

**Purpose**: Represents registered user in system

**Fields**:
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(255), unique=True, nullable=False, index=True)
    password: str = Column(String(255), nullable=False)  # Hashed
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
```

**Validation Rules**:
- `email`: Required, valid email format (RFC 5322), unique, max 255 chars
- `password`: Required, bcrypt hash (60 chars), never returned in responses
- `created_at`: Auto-generated timestamp

**Relationships**: None

**Library Integration**:
- **Validation**: Pydantic EmailStr validator
- **Serialization**: Pydantic .dict() excluding password
- **Storage**: SQLAlchemy declarative_base() ORM

#### Model: UserRegisterRequest (Pydantic)

```python
from pydantic import BaseModel, EmailStr, Field, validator

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
```

#### Model: UserResponse (Pydantic)

```python
from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True  # Enable from_orm()
```

### API Contracts

#### Endpoint: POST /api/users/register

**Purpose**: Register a new user account

**Request**:
```python
class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str  # Min 8 chars, mix of upper/lower/digit
```
**Example**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response**:
```python
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
```
**Example**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-10-29T10:00:00Z"
}
```

**Status Codes**:
- `201 Created`: User successfully registered
- `400 Bad Request`: Invalid email or weak password
- `409 Conflict`: Email already registered
- `500 Internal Server Error`: Database error

**Implementation Pattern**:
```python
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/api/users/register", response_model=UserResponse, status_code=201)
def register_user(
    request: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    try:
        user_service = UserService(UserRepository(db))
        user = user_service.register_user(request.email, request.password)
        return UserResponse.from_orm(user)
    except DuplicateEmailError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Data Flow

**Flow: User Registration**

1. Client sends POST /api/users/register with email and password
2. FastAPI validates request using Pydantic UserRegisterRequest model
3. Pydantic validators check email format and password strength
4. UserService.register_user() is called
5. UserRepository.get_by_email() checks for duplicate email (SQLAlchemy query)
6. If duplicate, raise DuplicateEmailError → 409 Conflict
7. PassLib.bcrypt.hash() hashes password with cost factor 12
8. User model created with hashed password
9. UserRepository.create() saves user to PostgreSQL (SQLAlchemy)
10. UserResponse model serializes user data (excluding password)
11. 201 Created response returned to client

### Error Handling Strategy

**Exception Hierarchy**:
```python
class AppException(Exception):
    """Base application exception"""
    pass

class DuplicateEmailError(AppException):
    """Email already registered"""
    pass

class ValidationError(AppException):
    """Invalid input data"""
    pass
```

**Library Exception Mapping**:
| Library Exception | App Exception | HTTP Status | User Message |
|-------------------|---------------|-------------|--------------|
| `sqlalchemy.exc.IntegrityError` | `DuplicateEmailError` | 409 | "Email already registered" |
| `pydantic.ValidationError` | `ValidationError` | 400 | "[Field] validation failed: [reason]" |
| `passlib.exc.CryptError` | `AppException` | 500 | "Internal server error" |

---

## Library Documentation

### Library: FastAPI v0.95.0

**Purpose**: Modern web framework for building APIs
**Documentation**: https://fastapi.tiangolo.com/
**Repository**: https://github.com/tiangolo/fastapi

**Installation**:
```bash
pip install fastapi==0.95.0 uvicorn[standard]==0.21.1
```

**Key APIs Used**:
- `@app.post()`: Define POST endpoint
- `response_model`: Automatic response serialization
- `Depends()`: Dependency injection for database session

**Integration Pattern**:
```python
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

@app.post("/endpoint", response_model=ResponseModel, status_code=201)
def endpoint_function(request: RequestModel, db: Session = Depends(get_db)):
    # Implementation
    return ResponseModel(...)
```

**Configuration**:
```python
# main.py
app = FastAPI(
    title="User API",
    description="User registration and authentication",
    version="1.0.0"
)
```

**Best Practices**:
- Use Pydantic models for request/response validation
- Use Depends() for dependency injection (easier testing)
- Return Pydantic models, not ORM models directly
- Use HTTPException for errors

**Testing**:
- **Mocking**: Use TestClient from fastapi.testclient
- **Example**:
```python
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.post("/api/users/register", json={"email": "test@example.com", "password": "Test123"})
assert response.status_code == 201
```

### Library: SQLAlchemy v2.0.0

**Purpose**: Python SQL toolkit and ORM
**Documentation**: https://docs.sqlalchemy.org/
**Repository**: https://github.com/sqlalchemy/sqlalchemy

**Installation**:
```bash
pip install sqlalchemy==2.0.0 psycopg2-binary==2.9.6
```

**Key APIs Used**:
- `declarative_base()`: Create base class for models
- `Session`: Database session for queries
- `Column()`: Define table columns
- `query()`: Query database

**Integration Pattern**:
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)

engine = create_engine("postgresql://user:pass@localhost/db")
SessionLocal = sessionmaker(bind=engine)
```

**Best Practices**:
- Use declarative_base() for ORM models
- Use sessions for transaction management
- Index frequently queried fields (email)
- Use unique constraints in database, not just application

**Testing**:
- **Mocking**: Use in-memory SQLite or testcontainers.postgres
- **Example**:
```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
```

### Library: PassLib v1.7.4

**Purpose**: Password hashing library
**Documentation**: https://passlib.readthedocs.io/
**Repository**: https://github.com/glic3rinu/passlib

**Installation**:
```bash
pip install passlib[bcrypt]==1.7.4
```

**Key APIs Used**:
- `bcrypt.hash()`: Hash password with bcrypt
- `bcrypt.verify()`: Verify password against hash

**Integration Pattern**:
```python
from passlib.hash import bcrypt

# Hash password
hashed = bcrypt.hash("password123", rounds=12)

# Verify password
is_valid = bcrypt.verify("password123", hashed)
```

**Configuration**:
- Use rounds=12 (OWASP recommendation for 2025)

**Best Practices**:
- Never store plaintext passwords
- Use cost factor 12 for bcrypt
- Never log passwords or hashes
- Use constant-time comparison (built into bcrypt.verify)

**Known Issues**: None for this use case

**Testing**:
- **Mocking**: Can test with real bcrypt (fast enough for unit tests)
- Or mock with: `bcrypt.hash = Mock(return_value="hashed")`

---

## Dependencies

### Dependency Tree

```
fastapi==0.95.0
├── pydantic==1.10.7
│   ├── typing-extensions>=4.2.0
│   └── email-validator>=1.1.3
├── starlette==0.26.1
└── uvicorn==0.21.1
    └── click>=7.0

sqlalchemy==2.0.0
├── greenlet==2.0.2
└── typing-extensions>=4.2.0

passlib[bcrypt]==1.7.4
└── bcrypt>=3.1.0
    └── cffi>=1.1

psycopg2-binary==2.9.6
```

### Installation Commands

**Prerequisites**:
```bash
python --version  # Should be >= 3.9
```

**Install Dependencies**:
```bash
pip install -r requirements.txt
```

**requirements.txt**:
```
fastapi==0.95.0
sqlalchemy==2.0.0
passlib[bcrypt]==1.7.4
psycopg2-binary==2.9.6
uvicorn[standard]==0.21.1
pydantic==1.10.7
email-validator==2.0.0
```

### Compatibility

**Python Version**: 3.9+
**Operating System**: Linux, macOS, Windows
**Database**: PostgreSQL 12+

---

## Implementation Plan

### Overview

Implementation follows a 2-phase approach: Foundation (models, repository) and
API endpoint (FastAPI).

**Total Estimated Effort**: 8-12 hours

### Phase 1: Foundation (4-6 hours)

**Goal**: Create User model and repository layer

**Tasks**:
1. **Data Models** (2 hours)
   - [ ] Create SQLAlchemy User model with email, password, created_at
   - [ ] Add unique constraint on email field
   - [ ] Create Pydantic UserRegisterRequest with validation
   - [ ] Create Pydantic UserResponse model
   - [ ] Write unit tests for Pydantic validation

2. **Repository Layer** (2 hours)
   - [ ] Create UserRepository with create() and get_by_email()
   - [ ] Implement SQLAlchemy session management
   - [ ] Write repository unit tests with in-memory SQLite

3. **Database Setup** (1 hour)
   - [ ] Create Alembic migration for users table
   - [ ] Test migration on dev database

**Files Created**:
- `src/models/user.py`: SQLAlchemy and Pydantic models
- `src/repositories/user_repository.py`: Repository implementation
- `tests/unit/test_user_models.py`: Model validation tests
- `tests/unit/test_user_repository.py`: Repository tests
- `alembic/versions/001_create_users_table.py`: Database migration

**Validation Checkpoint**:
- [ ] User model can be saved to database
- [ ] Duplicate email raises IntegrityError
- [ ] Pydantic validation catches invalid emails
- [ ] Pydantic validation catches weak passwords
- [ ] Phase 1 tests pass

### Phase 2: API Endpoint (4-6 hours)

**Goal**: Implement registration endpoint with FastAPI

**Tasks**:
1. **Service Layer** (2 hours)
   - [ ] Create UserService with register_user() method
   - [ ] Integrate PassLib for password hashing
   - [ ] Implement duplicate email check
   - [ ] Add error handling and exceptions
   - [ ] Write service unit tests with mocked repository

2. **API Endpoint** (2 hours)
   - [ ] Create POST /api/users/register endpoint
   - [ ] Add dependency injection for database session
   - [ ] Map exceptions to HTTP status codes
   - [ ] Write API integration tests with TestClient

3. **Documentation** (1 hour)
   - [ ] Add API docs (automatic via FastAPI)
   - [ ] Add code comments
   - [ ] Update README with registration endpoint

**Files Created/Modified**:
- `src/services/user_service.py`: Service layer
- `src/api/endpoints/users.py`: FastAPI endpoint
- `tests/unit/test_user_service.py`: Service tests
- `tests/integration/test_user_api.py`: API integration tests
- `README.md`: Updated with endpoint docs

**Validation Checkpoint**:
- [ ] POST /api/users/register returns 201 with user data
- [ ] Duplicate email returns 409 Conflict
- [ ] Invalid email returns 400 Bad Request
- [ ] Weak password returns 400 Bad Request
- [ ] Password not in response
- [ ] All tests passing

---

## Testing Strategy

### Test Coverage Targets

- **Unit Tests**: 90% coverage
- **Integration Tests**: All critical paths (registration flow)

### Unit Testing

**Framework**: pytest

**Test Files**:
```
tests/unit/
├── test_user_models.py          # Pydantic validation tests
├── test_user_repository.py      # Repository with SQLite in-memory
└── test_user_service.py         # Service with mocked repository
```

**Example Unit Test**:
```python
from unittest.mock import Mock

def test_register_user_success():
    # Arrange
    mock_repo = Mock()
    mock_repo.get_by_email.return_value = None  # No duplicate
    service = UserService(mock_repo)

    # Act
    user = service.register_user("test@example.com", "Test123")

    # Assert
    assert mock_repo.create.called
    assert bcrypt.identify(user.password)  # Password is hashed
```

### Integration Testing

**Framework**: pytest + TestClient

**Test Files**:
```
tests/integration/
└── test_user_api.py             # End-to-end API tests
```

**Example Integration Test**:
```python
from fastapi.testclient import TestClient

def test_register_user_api():
    client = TestClient(app)
    response = client.post(
        "/api/users/register",
        json={"email": "test@example.com", "password": "Test123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "password" not in data

def test_duplicate_email():
    client = TestClient(app)
    # First registration
    client.post("/api/users/register", json={"email": "test@example.com", "password": "Test123"})
    # Duplicate
    response = client.post("/api/users/register", json={"email": "test@example.com", "password": "Test456"})
    assert response.status_code == 409
```

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# With coverage
pytest --cov=src --cov-report=html
```

---

## Success Criteria

### Acceptance Criteria (from Analysis)
- [ ] User can register with valid email and password
- [ ] Duplicate email returns 409 Conflict error
- [ ] Invalid email returns 400 Bad Request error
- [ ] Weak password returns 400 Bad Request error
- [ ] Password is not returned in response

### Implementation Criteria
- [ ] User model created with SQLAlchemy
- [ ] UserRepository implements CRUD operations
- [ ] UserService implements business logic with PassLib
- [ ] POST /api/users/register endpoint functional

### Testing Criteria
- [ ] Unit test coverage ≥ 90%
- [ ] All integration tests passing
- [ ] Password hashing tested

### Quality Criteria
- [ ] Linting passed (black, mypy)
- [ ] No security vulnerabilities
- [ ] Code review approved
- [ ] Documentation complete

---

## Risks & Mitigations

| Risk | Severity | Probability | Impact | Mitigation |
|------|----------|-------------|--------|------------|
| Bcrypt cost factor too low | High | Low | Passwords vulnerable to brute force | Use cost factor 12 (OWASP 2025 rec) |
| Email uniqueness not enforced | High | Medium | Duplicate accounts possible | Add unique constraint at DB level |
| Weak password validation | Medium | Medium | User accounts easily compromised | Implement password strength validator |

---

**PRP Complete**: 2025-10-29 10:00:00
**Ready for Phase 3**: Implementation

---
```

---

## Example 2: Medium Complexity Feature

**Feature**: Caching Layer with Redis
**Complexity**: Medium
**Estimated Effort**: 2-3 days

**Key Differences from Example 1**:
- Multiple components (Cache service, Cache decorator, Cache invalidation)
- External service integration (Redis)
- More complex testing (requires test containers)
- Configuration management
- Monitoring and metrics

**Abbreviated Structure** (full example would be 1000+ lines):
```markdown
# Product Requirements Prompt: Redis Caching Layer (Issue #456)

## Executive Summary
Implements comprehensive caching layer using Redis for performance optimization...

## Architecture Design

### Components
- **CacheService**: Redis client wrapper with get/set/delete operations
- **CacheDecorator**: Python decorator for automatic method caching
- **CacheInvalidator**: Invalidate related caches on data updates
- **CacheMonitor**: Track cache hit/miss rates

### Library Integration
- redis-py 4.5.4 for Redis client
- functools for decorator implementation
- prometheus-client 0.16.0 for metrics

## Implementation Plan

### Phase 1: Core Cache Service (8 hours)
### Phase 2: Cache Decorator (6 hours)
### Phase 3: Cache Invalidation (8 hours)
### Phase 4: Monitoring (4 hours)
### Phase 5: Testing (8 hours)

Total: 2-3 days
```

---

## Example 3: Complex Multi-Component Feature

**Feature**: Real-time Notification System
**Complexity**: High
**Estimated Effort**: 1-2 weeks

**Key Differences from Examples 1 & 2**:
- Many components (WebSocket manager, Queue processor, Notification service, Template engine)
- Multiple external services (Redis pub/sub, Database, Email provider)
- Concurrent/async operations
- Multiple data models and API endpoints
- Complex data flows
- Extensive error handling and retry logic

**Abbreviated Structure** (full example would be 1500+ lines):
```markdown
# Product Requirements Prompt: Real-time Notification System (Issue #789)

## Executive Summary
Implements real-time notification system with WebSocket push, email delivery,
notification history, and template management...

## Architecture Design

### Components (6 total)
- **WebSocketManager**: Manage WebSocket connections for real-time push
- **NotificationService**: Create and send notifications
- **QueueProcessor**: Process notification queue asynchronously
- **TemplateEngine**: Render notification templates
- **NotificationRepository**: Persist notification history
- **EmailService**: Send email notifications

### Library Integration
- fastapi-websocket for WebSocket support
- celery for async queue processing
- jinja2 for template rendering
- sendgrid for email delivery
- redis for pub/sub messaging

## Implementation Plan

### Phase 1: Data Models & Repository (1 day)
### Phase 2: Template Engine (1 day)
### Phase 3: Notification Service (2 days)
### Phase 4: WebSocket Real-time Push (2 days)
### Phase 5: Async Queue Processing (2 days)
### Phase 6: Email Delivery (1 day)
### Phase 7: Testing & Integration (3 days)

Total: 10-12 days
```

---

## Summary

These examples demonstrate PRP structure for features of varying complexity:

1. **Simple (Example 1)**: Single component, straightforward integration, 8-12 hours
2. **Medium (Example 2)**: Multiple components, external service, 2-3 days
3. **Complex (Example 3)**: Many components, async/concurrent, 1-2 weeks

**Key Patterns**:
- Executive summary scales with complexity
- Components section grows with more components
- Implementation plan phases increase with complexity
- Testing strategy becomes more comprehensive
- All examples maintain same overall PRP structure

**Adaptation Guidelines**:
- Adjust detail level based on complexity
- Add more examples for complex integrations
- Expand testing strategy for critical features
- Include more error handling for distributed systems

---

**Examples Version**: 2.0.0
**Last Updated**: 2025-10-29
