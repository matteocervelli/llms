# Design Patterns Reference

**Purpose**: Common design patterns and architectural structures for synthesizing cohesive designs from sub-agent outputs.

**Version**: 2.0.0
**Phase**: 2 (Design & Planning)
**Created**: 2025-10-29

---

## Table of Contents

1. [Component Integration Patterns](#component-integration-patterns)
2. [Library Usage Patterns](#library-usage-patterns)
3. [Dependency Management Patterns](#dependency-management-patterns)
4. [Error Handling Patterns](#error-handling-patterns)
5. [Testing Patterns](#testing-patterns)
6. [Data Flow Patterns](#data-flow-patterns)

---

## Component Integration Patterns

Common patterns for connecting architectural components with library implementations.

### Pattern 1: Service Layer Pattern

**Use When**: Components provide business logic that uses multiple libraries.

**Structure**:
```
┌─────────────────────────────────┐
│      Service Layer              │
│  (Business Logic Component)     │
├─────────────────────────────────┤
│  - Uses: Library A, Library B   │
│  - Coordinates operations       │
│  - Implements business rules    │
└─────────────────────────────────┘
           ↓            ↓
    ┌──────────┐  ┌──────────┐
    │Library A │  │Library B │
    │ (Data)   │  │(Async)   │
    └──────────┘  └──────────┘
```

**Example**:
```python
# Component: UserService
# Uses: SQLAlchemy (data), PassLib (password), JWT (tokens)

from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from jose import jwt

class UserService:
    """Service layer component integrating multiple libraries."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user(self, email: str, password: str) -> User:
        """Create user with hashed password (PassLib) and store (SQLAlchemy)."""
        # Hash password using PassLib
        hashed_password = bcrypt.hash(password)

        # Create user model with SQLAlchemy
        user = User(email=email, password=hashed_password)
        self.db.add(user)
        self.db.commit()

        return user

    def authenticate(self, email: str, password: str) -> Optional[str]:
        """Authenticate user and return JWT token."""
        # Query user with SQLAlchemy
        user = self.db.query(User).filter_by(email=email).first()
        if not user:
            return None

        # Verify password with PassLib
        if not bcrypt.verify(password, user.password):
            return None

        # Generate JWT token with jose
        token = jwt.encode({"sub": user.id}, SECRET_KEY, algorithm="HS256")
        return token
```

**Synthesis Notes**:
- Map component responsibilities to library capabilities
- Document which library handles each operation
- Show how libraries are coordinated
- Specify error handling for each library interaction

---

### Pattern 2: Repository Pattern

**Use When**: Components abstract data access with ORM or database libraries.

**Structure**:
```
┌─────────────────────────────────┐
│    Repository Component         │
│  (Data Access Abstraction)      │
├─────────────────────────────────┤
│  - Uses: ORM Library            │
│  - CRUD operations              │
│  - Query building               │
└─────────────────────────────────┘
           ↓
    ┌──────────────┐
    │ ORM Library  │
    │ (SQLAlchemy) │
    └──────────────┘
           ↓
    ┌──────────────┐
    │   Database   │
    └──────────────┘
```

**Example**:
```python
# Component: UserRepository
# Uses: SQLAlchemy ORM

from sqlalchemy.orm import Session
from typing import Optional, List

class UserRepository:
    """Repository pattern using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID using SQLAlchemy query."""
        return self.session.query(User).filter_by(id=user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email using SQLAlchemy query."""
        return self.session.query(User).filter_by(email=email).first()

    def list_all(self, limit: int = 100) -> List[User]:
        """List all users with SQLAlchemy query."""
        return self.session.query(User).limit(limit).all()

    def create(self, user: User) -> User:
        """Create user using SQLAlchemy session."""
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        """Update user using SQLAlchemy session."""
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Delete user using SQLAlchemy session."""
        self.session.delete(user)
        self.session.commit()
```

**Synthesis Notes**:
- Map CRUD operations to ORM methods
- Document query patterns from library documentation
- Show session/transaction management
- Specify error handling for database operations

---

### Pattern 3: Factory Pattern

**Use When**: Components create objects with complex library initialization.

**Structure**:
```
┌─────────────────────────────────┐
│     Factory Component           │
│  (Object Creation)              │
├─────────────────────────────────┤
│  - Uses: Multiple Libraries     │
│  - Creates configured objects   │
│  - Handles initialization       │
└─────────────────────────────────┘
           ↓
    Creates instances of:
    - Library A objects
    - Library B objects
    - Composite objects
```

**Example**:
```python
# Component: DatabaseFactory
# Uses: SQLAlchemy (ORM), alembic (migrations), asyncpg (async driver)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

class DatabaseFactory:
    """Factory for creating database connections with proper configuration."""

    @staticmethod
    def create_sync_engine(database_url: str):
        """Create synchronous SQLAlchemy engine."""
        return create_engine(
            database_url,
            pool_pre_ping=True,  # Verify connections
            pool_size=10,
            max_overflow=20
        )

    @staticmethod
    def create_async_engine(database_url: str):
        """Create asynchronous SQLAlchemy engine with asyncpg."""
        # Convert postgres:// to postgresql+asyncpg://
        async_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
        return create_async_engine(
            async_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )

    @staticmethod
    def create_session_factory(engine) -> sessionmaker:
        """Create SQLAlchemy session factory."""
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
```

**Synthesis Notes**:
- Document library initialization parameters
- Show configuration from library documentation
- Specify which library features are used
- Map factory methods to architecture components

---

## Library Usage Patterns

Common patterns for using libraries in architectural implementations.

### Pattern 1: Dependency Injection

**Use When**: Libraries should be mockable for testing.

**Structure**:
```python
# Component receives library dependencies via __init__

class MyService:
    def __init__(
        self,
        database: Session,        # SQLAlchemy session
        cache: Redis,             # Redis client
        logger: Logger            # Logging client
    ):
        self.db = database
        self.cache = cache
        self.logger = logger

    def do_work(self):
        """Use injected dependencies."""
        self.logger.info("Starting work")
        data = self.db.query(Model).all()
        self.cache.set("key", data)
```

**Benefits**:
- Testable: Can inject mocks
- Flexible: Can swap implementations
- Clear: Dependencies explicit

**Synthesis Notes**:
- List all injected library clients
- Document library versions for each dependency
- Show mock examples for testing

---

### Pattern 2: Configuration Object

**Use When**: Library needs complex configuration.

**Structure**:
```python
# Create configuration object, pass to library

from pydantic import BaseSettings

class DatabaseConfig(BaseSettings):
    """Configuration for SQLAlchemy based on library docs."""
    database_url: str
    pool_size: int = 10
    max_overflow: int = 20
    echo: bool = False

    class Config:
        env_prefix = "DATABASE_"

# Use configuration
config = DatabaseConfig()
engine = create_engine(
    config.database_url,
    pool_size=config.pool_size,
    max_overflow=config.max_overflow,
    echo=config.echo
)
```

**Benefits**:
- Centralized: All config in one place
- Validated: Pydantic validation
- Documented: Types show requirements

**Synthesis Notes**:
- Map configuration fields to library parameters
- Document default values from library documentation
- Show environment variable mapping

---

### Pattern 3: Adapter Pattern

**Use When**: Library API doesn't match architectural interface.

**Structure**:
```python
# Architectural interface
class EmailServiceInterface(ABC):
    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> bool:
        pass

# Library: python-postmark has different API
from postmark import PMMail

class PostmarkAdapter(EmailServiceInterface):
    """Adapt Postmark library to EmailService interface."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def send(self, to: str, subject: str, body: str) -> bool:
        """Adapt architectural interface to Postmark API."""
        try:
            message = PMMail(
                api_key=self.api_key,
                to=to,
                subject=subject,
                text_body=body,
                sender="noreply@example.com"
            )
            message.send()
            return True
        except Exception as e:
            return False
```

**Benefits**:
- Decoupled: Architecture independent of library
- Swappable: Can replace library without changing architecture
- Testable: Can mock interface

**Synthesis Notes**:
- Document architectural interface
- Show how library API maps to interface
- Explain adapter transformation logic

---

## Dependency Management Patterns

Common patterns for managing library dependencies.

### Pattern 1: Pinned Dependencies

**Use When**: Need reproducible builds and stability.

**Structure**:
```txt
# requirements.txt - Exact versions pinned
sqlalchemy==2.0.0
fastapi==0.95.0
pydantic==1.10.7
redis==4.5.1

# All transitive dependencies also pinned
greenlet==2.0.2
typing-extensions==4.5.0
```

**Benefits**:
- Reproducible: Same versions everywhere
- Stable: No surprise updates
- Secure: Known versions, auditable

**Synthesis Notes**:
- Pin all direct dependencies
- Pin critical transitive dependencies
- Document why specific versions chosen

---

### Pattern 2: Constraint Files

**Use When**: Multiple services share common dependencies.

**Structure**:
```txt
# constraints.txt - Shared constraints
sqlalchemy>=2.0.0,<3.0.0
pydantic>=1.10.0,<2.0.0

# service-a/requirements.txt
-c ../constraints.txt
sqlalchemy
pydantic
fastapi==0.95.0

# service-b/requirements.txt
-c ../constraints.txt
sqlalchemy
pydantic
celery==5.3.0
```

**Benefits**:
- Consistency: Same versions across services
- Flexibility: Services can add unique deps
- Maintainability: Update constraints once

**Synthesis Notes**:
- Document constraint rationale
- Show which services share constraints
- Explain version ranges

---

### Pattern 3: Dependency Groups

**Use When**: Different dependency sets for different environments.

**Structure**:
```toml
# pyproject.toml with dependency groups
[project]
dependencies = [
    "sqlalchemy>=2.0.0",
    "fastapi>=0.95.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
]
async = [
    "asyncpg>=0.28.0",
    "aioredis>=2.0.0",
]
```

**Benefits**:
- Organized: Dependencies grouped by purpose
- Minimal: Production doesn't need dev deps
- Flexible: Install only what you need

**Synthesis Notes**:
- Categorize dependencies by usage
- Document when each group is needed
- Show installation commands per group

---

## Error Handling Patterns

Common patterns for handling library errors in architecture.

### Pattern 1: Library Exception Mapping

**Use When**: Library exceptions need to map to architectural error types.

**Structure**:
```python
# Architectural exception hierarchy
class ServiceError(Exception):
    """Base error for service layer."""
    pass

class NotFoundError(ServiceError):
    """Resource not found."""
    pass

class ValidationError(ServiceError):
    """Invalid input data."""
    pass

# Map library exceptions to service exceptions
from sqlalchemy.exc import NoResultFound, IntegrityError

class UserService:
    def get_user(self, user_id: int) -> User:
        try:
            return self.db.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            # Map SQLAlchemy exception to architectural exception
            raise NotFoundError(f"User {user_id} not found")
        except IntegrityError as e:
            # Map SQLAlchemy exception to architectural exception
            raise ValidationError(f"Database integrity error: {e}")
```

**Benefits**:
- Decoupled: Architecture independent of library exceptions
- Consistent: Same error types across components
- Actionable: Error types guide handling

**Synthesis Notes**:
- Document all library exceptions that can occur
- Map each library exception to architectural exception
- Show error message transformations

---

### Pattern 2: Retry Pattern

**Use When**: Library operations may fail transiently.

**Structure**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential
from redis.exceptions import ConnectionError

class CacheService:
    """Service using Redis with retry pattern."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=lambda e: isinstance(e, ConnectionError)
    )
    def get(self, key: str) -> Optional[str]:
        """Get value from Redis with retry on connection errors."""
        try:
            return self.redis.get(key)
        except ConnectionError as e:
            # tenacity will retry this exception
            raise
```

**Benefits**:
- Resilient: Handles transient failures
- Configurable: Retry strategy adjustable
- Clean: Declarative with decorator

**Synthesis Notes**:
- Document which library operations need retry
- Specify retry strategy (attempts, backoff)
- Show which exceptions to retry vs. fail fast

---

## Testing Patterns

Common patterns for testing components that use libraries.

### Pattern 1: Mock Library Pattern

**Use When**: Testing without library dependencies.

**Structure**:
```python
# Component using library
class UserService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter_by(id=user_id).first()

# Test with mocked library
from unittest.mock import Mock

def test_get_user():
    # Mock SQLAlchemy session
    mock_session = Mock()
    mock_query = Mock()
    mock_user = User(id=1, name="Test")

    # Set up mock chain: session.query().filter_by().first()
    mock_session.query.return_value = mock_query
    mock_query.filter_by.return_value = mock_query
    mock_query.first.return_value = mock_user

    # Test with mock
    service = UserService(mock_session)
    user = service.get_user(1)

    assert user.id == 1
    mock_session.query.assert_called_once_with(User)
    mock_query.filter_by.assert_called_once_with(id=1)
```

**Benefits**:
- Fast: No real library/database needed
- Isolated: Tests only component logic
- Controllable: Can simulate errors

**Synthesis Notes**:
- Document mock setup for each library
- Show how to mock library method chains
- Provide examples of mocking success and errors

---

### Pattern 2: Test Container Pattern

**Use When**: Integration testing with real library dependencies.

**Structure**:
```python
# Integration test with real database (using testcontainers)
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine

def test_user_repository_integration():
    # Start real PostgreSQL container
    with PostgresContainer("postgres:15") as postgres:
        # Create engine with real database
        engine = create_engine(postgres.get_connection_url())

        # Create tables
        Base.metadata.create_all(engine)

        # Create session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Test with real database
        repo = UserRepository(session)
        user = repo.create(User(name="Test", email="test@example.com"))

        assert user.id is not None
        retrieved = repo.get_by_id(user.id)
        assert retrieved.name == "Test"
```

**Benefits**:
- Real: Tests actual library behavior
- Isolated: Clean database per test
- Reliable: Container ensures consistency

**Synthesis Notes**:
- Document container images for each library
- Show setup and teardown patterns
- Specify test data initialization

---

## Data Flow Patterns

Common patterns for data flowing through components and libraries.

### Pattern 1: Request-Response Pattern

**Use When**: Synchronous data flow through components.

**Structure**:
```
Client Request
    ↓
┌─────────────────┐
│  API Controller │  (FastAPI)
└─────────────────┘
    ↓ (Pydantic validation)
┌─────────────────┐
│  Service Layer  │  (Business Logic)
└─────────────────┘
    ↓ (SQLAlchemy ORM)
┌─────────────────┐
│   Repository    │  (Data Access)
└─────────────────┘
    ↓
Database
```

**Example**:
```python
# FastAPI endpoint
@app.post("/users", response_model=UserResponse)
def create_user(request: UserCreateRequest):  # Pydantic validation
    # Pass to service
    user = user_service.create_user(request.email, request.password)
    # Service uses repository with SQLAlchemy
    return UserResponse.from_orm(user)
```

**Synthesis Notes**:
- Map each layer to library
- Document data transformations
- Show validation at each layer

---

### Pattern 2: Event-Driven Pattern

**Use When**: Asynchronous data flow with event bus.

**Structure**:
```
Component A
    ↓ (publishes event)
┌──────────────────┐
│   Event Bus      │  (Redis/RabbitMQ)
└──────────────────┘
    ↓ (subscribes)
Component B
```

**Example**:
```python
# Publisher (using Redis)
import redis
import json

class EventPublisher:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def publish(self, channel: str, event: dict):
        self.redis.publish(channel, json.dumps(event))

# Subscriber (using Redis)
class EventSubscriber:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.pubsub = redis_client.pubsub()

    def subscribe(self, channel: str, handler: Callable):
        self.pubsub.subscribe(channel)
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                event = json.loads(message['data'])
                handler(event)
```

**Synthesis Notes**:
- Document event schema (Pydantic models)
- Map publish/subscribe to library methods
- Show error handling for lost messages

---

## Summary

When synthesizing design from sub-agent outputs:

1. **Identify Pattern**: Match architectural component to appropriate pattern
2. **Map Libraries**: Show how libraries implement pattern
3. **Document Integration**: Explain how components and libraries connect
4. **Show Examples**: Provide code examples using library APIs
5. **Specify Dependencies**: List all libraries and versions required

**Common Pattern Sequence**:
```
Architecture Component
    → Choose Pattern (Service, Repository, Factory, etc.)
        → Select Libraries (from Documentation Researcher)
            → Show Integration Code (using library APIs)
                → Specify Dependencies (from Dependency Manager)
                    → Document Testing Approach
```

These patterns provide reusable templates for creating cohesive designs from sub-agent outputs.

---

**Remember**: Patterns are guidelines, not rigid rules. Adapt patterns based on specific requirements, library capabilities, and architectural constraints documented in sub-agent outputs.
