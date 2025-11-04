---
name: architecture-patterns
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Architecture Patterns Guide

This guide provides comprehensive coverage of architectural patterns for designing clean, maintainable, and scalable systems.

## Table of Contents

1. [Layered Architecture](#layered-architecture)
2. [Hexagonal Architecture (Ports and Adapters)](#hexagonal-architecture)
3. [Clean Architecture](#clean-architecture)
4. [Event-Driven Architecture](#event-driven-architecture)
5. [Microservices Patterns](#microservices-patterns)
6. [Pattern Selection Criteria](#pattern-selection-criteria)

---

## Layered Architecture

### Overview

Layered Architecture organizes code into horizontal layers, each with a specific responsibility. Dependencies flow downward: upper layers depend on lower layers.

### Standard Layers

**Presentation Layer (Top)**
- User interfaces (CLI, Web, API)
- Request/response handling
- Input validation
- Output formatting

**Business Layer (Middle)**
- Business logic and rules
- Workflows and use cases
- Domain models
- Service orchestration

**Data Layer (Bottom)**
- Data access and persistence
- External system integration
- Caching
- File I/O

### Benefits
- ✅ Simple to understand and implement
- ✅ Clear separation of concerns
- ✅ Easy to maintain and test
- ✅ Well-suited for traditional applications

### Drawbacks
- ❌ Can become monolithic
- ❌ Database-centric design
- ❌ Tight coupling between layers
- ❌ Difficult to change data layer

### Python Example

```python
# Directory Structure
# src/
# ├── presentation/    # Layer 1: Presentation
# │   ├── cli.py
# │   └── api.py
# ├── business/        # Layer 2: Business
# │   ├── services.py
# │   └── models.py
# └── data/            # Layer 3: Data
#     ├── repository.py
#     └── database.py

# ==================== PRESENTATION LAYER ====================
# src/presentation/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.business.services import UserService

app = FastAPI()
user_service = UserService()

class UserRequest(BaseModel):
    name: str
    email: str

@app.post("/users")
async def create_user(user: UserRequest):
    """Presentation layer: Handle HTTP requests."""
    try:
        result = await user_service.create_user(user.name, user.email)
        return {"id": result.id, "status": "created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== BUSINESS LAYER ====================
# src/business/services.py
from src.business.models import User
from src.data.repository import UserRepository

class UserService:
    """Business layer: Business logic and orchestration."""

    def __init__(self):
        self.repository = UserRepository()

    async def create_user(self, name: str, email: str) -> User:
        """Create user with business validation."""
        # Business rule: Email must be unique
        existing = await self.repository.find_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")

        # Business rule: Name must be non-empty
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")

        # Create and save user
        user = User(name=name.strip(), email=email.lower())
        return await self.repository.save(user)

# src/business/models.py
from dataclasses import dataclass

@dataclass
class User:
    """Domain model."""
    name: str
    email: str
    id: int = None

# ==================== DATA LAYER ====================
# src/data/repository.py
from typing import Optional
from src.business.models import User
from src.data.database import Database

class UserRepository:
    """Data layer: Data access abstraction."""

    def __init__(self):
        self.db = Database()

    async def save(self, user: User) -> User:
        """Persist user to database."""
        user_id = await self.db.execute(
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
            user.name, user.email
        )
        user.id = user_id
        return user

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        row = await self.db.fetch_one(
            "SELECT id, name, email FROM users WHERE email = $1",
            email
        )
        return User(id=row['id'], name=row['name'], email=row['email']) if row else None
```

### When to Use
- Traditional CRUD applications
- Straightforward business logic
- Database-centric systems
- Rapid prototyping

---

## Hexagonal Architecture

### Overview

Hexagonal Architecture (Ports and Adapters) places business logic at the center, with adapters connecting to external systems through ports (interfaces).

### Core Concepts

**Core Domain (Center)**
- Pure business logic
- No external dependencies
- Framework-independent

**Ports (Interfaces)**
- Input ports: Application services
- Output ports: Repository interfaces

**Adapters (Implementations)**
- Input adapters: REST API, CLI, GraphQL
- Output adapters: Database, External APIs, File System

### Benefits
- ✅ Business logic isolated from infrastructure
- ✅ Easy to test (mock adapters)
- ✅ Flexible: Swap adapters without changing core
- ✅ Framework-independent core

### Drawbacks
- ❌ More complex initial setup
- ❌ Requires discipline to maintain boundaries
- ❌ Can be over-engineering for simple apps

### Python Example

```python
# Directory Structure
# src/
# ├── core/              # Hexagon center
# │   ├── domain/        # Domain models
# │   ├── ports/         # Interfaces (ports)
# │   └── usecases/      # Business logic
# └── adapters/          # Hexagon edges
#     ├── input/         # Input adapters
#     │   ├── api/
#     │   └── cli/
#     └── output/        # Output adapters
#         ├── database/
#         └── external/

# ==================== CORE DOMAIN ====================
# src/core/domain/user.py
from dataclasses import dataclass

@dataclass
class User:
    """Pure domain model (no infrastructure dependencies)."""
    name: str
    email: str
    id: int = None

# ==================== OUTPUT PORTS ====================
# src/core/ports/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from src.core.domain.user import User

class IUserRepository(ABC):
    """Output port: Repository interface."""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save user."""
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        pass

# ==================== USE CASES ====================
# src/core/usecases/create_user.py
from src.core.domain.user import User
from src.core.ports.user_repository import IUserRepository

class CreateUserUseCase:
    """Business logic (core hexagon)."""

    def __init__(self, repository: IUserRepository):
        """Inject repository port."""
        self.repository = repository

    async def execute(self, name: str, email: str) -> User:
        """Execute use case."""
        # Business validation
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")

        existing = await self.repository.find_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")

        # Create and save
        user = User(name=name.strip(), email=email.lower())
        return await self.repository.save(user)

# ==================== INPUT ADAPTERS ====================
# src/adapters/input/api/user_routes.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.usecases.create_user import CreateUserUseCase
from src.adapters.output.database.postgres_user_repository import PostgresUserRepository

app = FastAPI()

# Dependency injection (wire adapters)
user_repository = PostgresUserRepository()
create_user_usecase = CreateUserUseCase(user_repository)

class UserRequest(BaseModel):
    name: str
    email: str

@app.post("/users")
async def create_user(user: UserRequest):
    """Input adapter: REST API."""
    try:
        result = await create_user_usecase.execute(user.name, user.email)
        return {"id": result.id, "status": "created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==================== OUTPUT ADAPTERS ====================
# src/adapters/output/database/postgres_user_repository.py
from typing import Optional
from src.core.domain.user import User
from src.core.ports.user_repository import IUserRepository
import asyncpg

class PostgresUserRepository(IUserRepository):
    """Output adapter: PostgreSQL implementation."""

    def __init__(self):
        self.connection_string = "postgresql://..."

    async def save(self, user: User) -> User:
        """Implement save using PostgreSQL."""
        conn = await asyncpg.connect(self.connection_string)
        try:
            user_id = await conn.fetchval(
                "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
                user.name, user.email
            )
            user.id = user_id
            return user
        finally:
            await conn.close()

    async def find_by_email(self, email: str) -> Optional[User]:
        """Implement find using PostgreSQL."""
        conn = await asyncpg.connect(self.connection_string)
        try:
            row = await conn.fetchrow(
                "SELECT id, name, email FROM users WHERE email = $1",
                email
            )
            return User(id=row['id'], name=row['name'], email=row['email']) if row else None
        finally:
            await conn.close()
```

### When to Use
- Complex business logic
- Multiple input/output channels
- High testability requirements
- Framework independence important

---

## Clean Architecture

### Overview

Clean Architecture (Uncle Bob Martin) organizes code into concentric circles, with business rules at the center and infrastructure at the edges.

### Layers (from center outward)

1. **Entities** (innermost): Core business objects
2. **Use Cases**: Application-specific business rules
3. **Interface Adapters**: Convert data formats
4. **Frameworks & Drivers** (outermost): External tools

### Dependency Rule

**Dependencies point inward only.** Outer layers depend on inner layers, never the reverse.

### Benefits
- ✅ Maximum testability
- ✅ Framework independence
- ✅ Database independence
- ✅ UI independence
- ✅ Highly maintainable

### When to Use
- Large, complex systems
- Long-term maintainability critical
- Multiple platforms (web, mobile, CLI)
- Team wants strict architecture

---

## Event-Driven Architecture

### Overview

Event-Driven Architecture uses events to trigger and communicate between decoupled services.

### Core Concepts

**Events**: Notifications of state changes
**Publishers**: Emit events
**Subscribers**: React to events
**Event Bus**: Routes events

### Python Example

```python
# src/events/event_bus.py
from typing import Callable, List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    """Base event."""
    name: str
    data: dict
    timestamp: datetime = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow()

class EventBus:
    """Event bus for pub/sub."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, handler: Callable):
        """Subscribe to event."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)

    async def publish(self, event: Event):
        """Publish event to subscribers."""
        if event.name in self._subscribers:
            for handler in self._subscribers[event.name]:
                await handler(event)

# Usage
event_bus = EventBus()

# Subscriber 1: Send email notification
async def send_email_notification(event: Event):
    print(f"Sending email for user {event.data['email']}")

# Subscriber 2: Log event
async def log_event(event: Event):
    print(f"Logging event: {event.name} at {event.timestamp}")

# Subscribe
event_bus.subscribe("user.created", send_email_notification)
event_bus.subscribe("user.created", log_event)

# Publisher
async def create_user(name: str, email: str):
    # Create user logic...
    user_id = 123

    # Publish event
    await event_bus.publish(Event(
        name="user.created",
        data={"id": user_id, "name": name, "email": email}
    ))
```

### When to Use
- Microservices communication
- Asynchronous workflows
- Decoupled systems
- Real-time notifications

---

## Pattern Selection Criteria

### Decision Matrix

| Pattern | Complexity | Testability | Flexibility | Learning Curve | Best For |
|---------|-----------|-------------|-------------|----------------|----------|
| Layered | Low | Medium | Low | Low | CRUD apps, prototypes |
| Hexagonal | Medium | High | High | Medium | Complex business logic |
| Clean | High | Very High | Very High | High | Enterprise systems |
| Event-Driven | Medium | Medium | Very High | Medium | Async workflows |

### Selection Guidelines

**Choose Layered Architecture when:**
- Building simple CRUD application
- Rapid prototyping needed
- Team is small or inexperienced
- Database is central to design

**Choose Hexagonal Architecture when:**
- Business logic is complex
- Multiple input channels (API, CLI, UI)
- High testability is critical
- Want framework independence

**Choose Clean Architecture when:**
- Building large enterprise system
- Long-term maintainability is paramount
- Supporting multiple platforms
- Team is experienced with architecture

**Choose Event-Driven Architecture when:**
- Building microservices
- Need asynchronous processing
- Decoupling is critical
- Real-time features required

### Hybrid Approaches

Most real-world systems combine patterns:
- **Layered + Hexagonal**: Use ports/adapters for data layer
- **Hexagonal + Events**: Use event bus for cross-service communication
- **Clean + Events**: Events as outer layer communication

---

## Summary

- **Layered Architecture**: Simple, database-centric, good for CRUD
- **Hexagonal Architecture**: Business logic isolated, highly testable
- **Clean Architecture**: Maximum flexibility, framework-independent
- **Event-Driven**: Decoupled, asynchronous, scalable

Choose patterns based on:
1. System complexity
2. Team experience
3. Maintainability requirements
4. Performance needs
5. Scalability goals

**Remember:** Start simple (Layered), evolve to complex patterns (Hexagonal, Clean) as system grows and requirements become clearer.
