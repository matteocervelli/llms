# Component Design Guide

This guide provides detailed principles and patterns for designing clean, maintainable components with clear responsibilities and minimal coupling.

## Table of Contents

1. [Single Responsibility Principle](#single-responsibility-principle)
2. [Dependency Injection Patterns](#dependency-injection-patterns)
3. [Interface Design](#interface-design)
4. [Module Boundaries](#module-boundaries)
5. [Extension Points](#extension-points)
6. [Component Interaction Patterns](#component-interaction-patterns)

---

## Single Responsibility Principle

### Definition

**A component should have one, and only one, reason to change.**

Each component should focus on a single aspect of functionality. When requirements change, only components related to that change should need modification.

### Identifying Responsibilities

Ask these questions:
1. **What does this component do?** (Should be a single, clear answer)
2. **Why would this component change?** (Should be ONE reason)
3. **Can I describe this component in one sentence?** (Without using "and" or "or")

### Good vs. Bad Examples

**❌ Bad: Multiple Responsibilities**
```python
class UserManager:
    """Too many responsibilities!"""

    def create_user(self, name: str, email: str):
        """Create user in database."""
        pass

    def send_welcome_email(self, user):
        """Send email to user."""
        pass

    def log_user_creation(self, user):
        """Log to file."""
        pass

    def validate_email_format(self, email: str) -> bool:
        """Validate email."""
        pass

# Problems:
# - Reason to change 1: Database schema changes
# - Reason to change 2: Email service changes
# - Reason to change 3: Logging format changes
# - Reason to change 4: Email validation rules change
```

**✅ Good: Single Responsibilities**
```python
class UserRepository:
    """Single responsibility: User data persistence."""

    async def save(self, user: User) -> User:
        """Save user to database."""
        pass

    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        pass

class EmailService:
    """Single responsibility: Email sending."""

    async def send_welcome_email(self, user: User):
        """Send welcome email."""
        pass

class AuditLogger:
    """Single responsibility: Audit logging."""

    def log_user_created(self, user: User):
        """Log user creation event."""
        pass

class EmailValidator:
    """Single responsibility: Email validation."""

    def is_valid(self, email: str) -> bool:
        """Validate email format."""
        pass

# Each component has ONE reason to change
```

### Guidelines

1. **One Primary Action:** Component should do ONE thing well
2. **Clear Naming:** Name should clearly describe single purpose
3. **Small Size:** 100-300 lines ideal, 500 maximum
4. **Minimal Dependencies:** Few external dependencies
5. **High Cohesion:** Related functionality grouped together

---

## Dependency Injection Patterns

### Why Dependency Injection?

**Benefits:**
- ✅ **Testability**: Easy to inject mocks and test doubles
- ✅ **Flexibility**: Change implementations without modifying client code
- ✅ **Decoupling**: Components depend on abstractions, not implementations
- ✅ **Reusability**: Components can be reused with different dependencies

### Constructor Injection (Recommended)

**When to use:** Required dependencies that component needs to function

```python
from abc import ABC, abstractmethod

class IEmailService(ABC):
    """Abstract email service."""

    @abstractmethod
    async def send(self, to: str, subject: str, body: str):
        pass

class UserService:
    """Inject dependencies via constructor."""

    def __init__(self, email_service: IEmailService, logger: ILogger):
        """Required dependencies injected at construction."""
        self.email_service = email_service
        self.logger = logger

    async def create_user(self, name: str, email: str) -> User:
        """Create user and send welcome email."""
        user = User(name=name, email=email)
        # Use injected dependencies
        await self.email_service.send(email, "Welcome!", "Hello!")
        self.logger.info(f"User created: {email}")
        return user

# Usage: Inject concrete implementations
email_service = SmtpEmailService()
logger = FileLogger()
user_service = UserService(email_service, logger)

# Testing: Inject mocks
mock_email = MockEmailService()
mock_logger = MockLogger()
test_service = UserService(mock_email, mock_logger)
```

### Property Injection

**When to use:** Optional dependencies or circular dependencies

```python
class FeatureProcessor:
    """Optional dependencies via properties."""

    def __init__(self):
        self._cache: Optional[ICache] = None

    @property
    def cache(self) -> Optional[ICache]:
        return self._cache

    @cache.setter
    def cache(self, cache: ICache):
        self._cache = cache

    async def process(self, data: dict) -> dict:
        """Process with optional caching."""
        # Check cache if available
        if self.cache:
            cached = await self.cache.get(data['id'])
            if cached:
                return cached

        # Process data
        result = self._do_processing(data)

        # Cache if available
        if self.cache:
            await self.cache.set(data['id'], result)

        return result
```

### Method Injection

**When to use:** Dependency only needed for single method

```python
class ReportGenerator:
    """Inject per-method dependencies."""

    async def generate_report(self, data: dict, formatter: IFormatter) -> str:
        """Generate report using provided formatter."""
        report_data = self._process_data(data)
        return formatter.format(report_data)

# Usage: Different formatters per call
generator = ReportGenerator()
pdf_report = await generator.generate_report(data, PdfFormatter())
html_report = await generator.generate_report(data, HtmlFormatter())
```

### Dependency Injection Container

**When to use:** Complex dependency graphs

```python
class Container:
    """Simple DI container."""

    def __init__(self):
        self._services = {}

    def register(self, interface: type, implementation: type):
        """Register service."""
        self._services[interface] = implementation

    def resolve(self, interface: type):
        """Resolve service."""
        implementation = self._services.get(interface)
        if not implementation:
            raise ValueError(f"No implementation for {interface}")
        return implementation()

# Setup container
container = Container()
container.register(IEmailService, SmtpEmailService)
container.register(ILogger, FileLogger)
container.register(IUserRepository, PostgresUserRepository)

# Resolve dependencies
user_service = UserService(
    email_service=container.resolve(IEmailService),
    logger=container.resolve(ILogger)
)
```

---

## Interface Design

### Protocol-Based Interfaces (Python 3.8+)

**Recommended approach for Python:**

```python
from typing import Protocol

class IDataRepository(Protocol):
    """Repository interface using Protocol."""

    async def save(self, data: dict) -> bool:
        """Save data."""
        ...

    async def retrieve(self, id: str) -> dict:
        """Retrieve data."""
        ...

# Implementations don't need to explicitly inherit
class PostgresRepository:
    """Implicitly implements IDataRepository."""

    async def save(self, data: dict) -> bool:
        # PostgreSQL implementation
        return True

    async def retrieve(self, id: str) -> dict:
        # PostgreSQL implementation
        return {"id": id}

# Type checker validates protocol compliance
def use_repository(repo: IDataRepository):
    """Accepts any type implementing the protocol."""
    await repo.save({"id": "123"})
```

### ABC-Based Interfaces

**When explicit inheritance needed:**

```python
from abc import ABC, abstractmethod

class IProcessor(ABC):
    """Abstract processor."""

    @abstractmethod
    async def process(self, data: dict) -> dict:
        """Process data."""
        pass

    @abstractmethod
    def validate(self, data: dict) -> bool:
        """Validate data."""
        pass

class ConcreteProcessor(IProcessor):
    """Must implement all abstract methods."""

    async def process(self, data: dict) -> dict:
        return {"result": "processed"}

    def validate(self, data: dict) -> bool:
        return "required_field" in data
```

### Interface Segregation

**Principle:** Many specific interfaces better than one general interface

**❌ Bad: Fat Interface**
```python
class IDataService(ABC):
    """Too many responsibilities in one interface."""

    @abstractmethod
    def save(self, data): pass

    @abstractmethod
    def retrieve(self, id): pass

    @abstractmethod
    def send_email(self, to, subject): pass

    @abstractmethod
    def log(self, message): pass
```

**✅ Good: Segregated Interfaces**
```python
class IDataRepository(Protocol):
    """Focused on data operations."""
    async def save(self, data): ...
    async def retrieve(self, id): ...

class IEmailService(Protocol):
    """Focused on email."""
    async def send(self, to, subject, body): ...

class ILogger(Protocol):
    """Focused on logging."""
    def log(self, message): ...

# Clients depend only on what they need
class UserService:
    def __init__(self, repository: IDataRepository, email: IEmailService):
        self.repository = repository
        self.email = email
        # No logging dependency if not needed
```

---

## Module Boundaries

### Defining Clear Boundaries

**Principles:**
1. **High Cohesion**: Related functionality together
2. **Low Coupling**: Minimal dependencies between modules
3. **Clear Interface**: Well-defined public API
4. **Information Hiding**: Implementation details private

### Module Structure

```python
# src/users/
# ├── __init__.py        # Public API
# ├── models.py          # Public models
# ├── service.py         # Public service
# ├── repository.py      # Public repository
# └── _internal.py       # Private implementation details

# __init__.py - Public API
"""Users module public API."""
from .models import User
from .service import UserService
from .repository import UserRepository

__all__ = ['User', 'UserService', 'UserRepository']

# Other modules should only import from users module:
from users import User, UserService  # ✅ Good
from users._internal import helper   # ❌ Bad (private module)
```

### Cross-Module Dependencies

**Rules:**
1. **Avoid Circular Dependencies**: Module A imports B, B should not import A
2. **Depend on Abstractions**: Import interfaces, not implementations
3. **Minimize Coupling**: Fewer dependencies = easier to change

```python
# ❌ Bad: Circular dependency
# users/service.py
from orders.service import OrderService  # Users depends on Orders

# orders/service.py
from users.service import UserService    # Orders depends on Users

# ✅ Good: Break circular dependency with interface
# users/service.py
from orders.interfaces import IOrderService  # Depend on abstraction

class UserService:
    def __init__(self, order_service: IOrderService):
        self.order_service = order_service

# orders/service.py
# No dependency on users module
```

---

## Extension Points

### Strategy Pattern for Extension

```python
from abc import ABC, abstractmethod
from typing import Dict

class ValidationStrategy(ABC):
    """Extension point for validators."""

    @abstractmethod
    def validate(self, data: dict) -> bool:
        pass

class EmailValidator(ValidationStrategy):
    """Email validation strategy."""

    def validate(self, data: dict) -> bool:
        return '@' in data.get('email', '')

class CustomValidator(ValidationStrategy):
    """User-defined validator (extension)."""

    def validate(self, data: dict) -> bool:
        # Custom validation logic
        return True

# Processor accepts any validator
class DataProcessor:
    def __init__(self, validators: List[ValidationStrategy]):
        self.validators = validators

    def process(self, data: dict):
        """Process with extensible validation."""
        for validator in self.validators:
            if not validator.validate(data):
                raise ValueError("Validation failed")
        # Process data
```

### Plugin Registration

```python
class PluginRegistry:
    """Registry for plugins."""

    _plugins: Dict[str, callable] = {}

    @classmethod
    def register(cls, name: str, plugin: callable):
        """Register plugin."""
        cls._plugins[name] = plugin

    @classmethod
    def get(cls, name: str) -> callable:
        """Get registered plugin."""
        return cls._plugins.get(name)

    @classmethod
    def list_plugins(cls) -> List[str]:
        """List all registered plugins."""
        return list(cls._plugins.keys())

# Users can register custom plugins
def my_custom_processor(data: dict) -> dict:
    return {"processed": True}

PluginRegistry.register("custom", my_custom_processor)

# Use registered plugins
processor = PluginRegistry.get("custom")
result = processor({"input": "data"})
```

---

## Component Interaction Patterns

### Direct Method Calls

**When to use:** Simple, synchronous interactions

```python
class OrderService:
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def place_order(self, order: Order):
        """Direct method call."""
        self.payment_service.process_payment(order.total)
```

### Event-Based Communication

**When to use:** Decoupled, asynchronous interactions

```python
class OrderService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def place_order(self, order: Order):
        """Publish event instead of direct call."""
        await self.event_bus.publish(Event(
            name="order.placed",
            data={"order_id": order.id, "total": order.total}
        ))

# PaymentService subscribes to event
class PaymentService:
    def __init__(self, event_bus: EventBus):
        event_bus.subscribe("order.placed", self.handle_order_placed)

    async def handle_order_placed(self, event: Event):
        """Handle event."""
        await self.process_payment(event.data['total'])
```

### Message Queue

**When to use:** Reliable, asynchronous, distributed

```python
class OrderService:
    def __init__(self, queue: MessageQueue):
        self.queue = queue

    async def place_order(self, order: Order):
        """Send message to queue."""
        await self.queue.send("orders", {
            "order_id": order.id,
            "total": order.total
        })
```

---

## Summary

### Key Principles

1. **Single Responsibility**: One reason to change
2. **Dependency Injection**: Inject dependencies, don't create them
3. **Interface Segregation**: Many specific interfaces
4. **Module Boundaries**: High cohesion, low coupling
5. **Extension Points**: Strategy, plugins, events
6. **Interaction Patterns**: Choose appropriate communication style

### Best Practices

- ✅ Keep components small (< 500 lines)
- ✅ Inject dependencies via constructor
- ✅ Depend on abstractions (interfaces)
- ✅ Design for testability
- ✅ Provide extension points
- ✅ Document public APIs
- ✅ Hide implementation details

### Anti-Patterns to Avoid

- ❌ God objects (too many responsibilities)
- ❌ Circular dependencies
- ❌ Global state
- ❌ Tight coupling
- ❌ Fat interfaces
- ❌ Leaky abstractions
