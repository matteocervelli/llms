---
name: architecture-patterns
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Architecture Patterns Reference

## Overview

This document provides a reference for common architectural patterns suitable for Python projects, with specific guidance for this LLM configuration management system.

---

## Layered Architecture

### Description
Organizes code into horizontal layers, each with specific responsibilities. Each layer depends only on the layers below it.

### Structure
```
┌─────────────────────────────┐
│   Presentation Layer        │  (CLI, Web UI, API endpoints)
├─────────────────────────────┤
│   Business Logic Layer      │  (Core domain logic, use cases)
├─────────────────────────────┤
│   Data Access Layer         │  (Repositories, database access)
├─────────────────────────────┤
│   Infrastructure Layer      │  (File system, external APIs)
└─────────────────────────────┘
```

### When to Use
- Clear separation of concerns needed
- Multiple interfaces to same business logic
- Team members specialize in different layers
- Standard CRUD applications

### Python Implementation
```python
# Presentation Layer (CLI)
# main.py
import click
from business_logic import FeatureService

@click.command()
def create_feature(name: str):
    service = FeatureService()
    result = service.create(name)
    click.echo(result)

# Business Logic Layer
# service.py
class FeatureService:
    def __init__(self, repository: FeatureRepository):
        self.repository = repository

    def create(self, name: str) -> Feature:
        # Validation and business rules
        feature = Feature(name=name)
        return self.repository.save(feature)

# Data Access Layer
# repository.py
class FeatureRepository:
    def save(self, feature: Feature) -> Feature:
        # Database operations
        pass
```

### Pros
- Clear separation of concerns
- Easy to understand and navigate
- Testable (can mock lower layers)
- Reusable business logic

### Cons
- Can lead to tight coupling between layers
- Changes may ripple across layers
- May be overkill for simple projects

---

## Modular (Package-Based) Architecture

### Description
Organizes code into self-contained modules/packages by feature or domain, each with its own layers internally.

### Structure
```
src/
├── tools/
│   ├── command_builder/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── builder.py
│   │   ├── validator.py
│   │   └── main.py
│   ├── skill_builder/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── builder.py
│   │   └── main.py
├── core/
│   ├── config.py
│   ├── exceptions.py
└── utils/
    ├── file_utils.py
    └── validators.py
```

### When to Use
- Feature-oriented development
- Multiple tools/services that are independent
- Want to limit blast radius of changes
- Teams working on different features

### Python Implementation
```python
# Each module is self-contained
# src/tools/skill_builder/__init__.py
from .models import SkillConfig
from .builder import SkillBuilder
from .main import cli

__all__ = ["SkillConfig", "SkillBuilder", "cli"]

# Other modules import only what they need
from src.tools.skill_builder import SkillBuilder
```

### Pros
- High cohesion within modules
- Low coupling between modules
- Easy to add/remove features
- Clear ownership boundaries

### Cons
- Risk of duplication across modules
- Harder to enforce cross-cutting concerns
- May need shared utilities

**Best for:** This project (LLM config management)

---

## Repository Pattern

### Description
Abstracts data access logic behind an interface, separating domain logic from data persistence details.

### Structure
```python
# Interface (Abstract Base Class)
from abc import ABC, abstractmethod

class FeatureRepository(ABC):
    @abstractmethod
    def get(self, id: int) -> Feature:
        pass

    @abstractmethod
    def save(self, feature: Feature) -> Feature:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

# Implementation
class FileSystemFeatureRepository(FeatureRepository):
    def get(self, id: int) -> Feature:
        # Read from file system
        pass

    def save(self, feature: Feature) -> Feature:
        # Write to file system
        pass

    def delete(self, id: int) -> None:
        # Delete from file system
        pass

# Usage (dependency injection)
class FeatureService:
    def __init__(self, repository: FeatureRepository):
        self.repository = repository  # Can be any implementation
```

### When to Use
- Need to abstract data storage (files, DB, API)
- Want testability (mock repositories)
- May change data source in future
- Multiple data sources possible

### Pros
- Testable (easy to mock)
- Flexible (swap implementations)
- Clean separation of concerns
- Centralized data access logic

### Cons
- Additional abstraction layer
- More files/classes to maintain
- May be overkill for simple CRUD

**Best for:** File system operations in this project

---

## Service Layer Pattern

### Description
Encapsulates business logic in service classes, coordinating between repositories and providing a cohesive API.

### Structure
```python
# Models (domain entities)
from pydantic import BaseModel

class Feature(BaseModel):
    id: Optional[int]
    name: str
    description: str

# Repository (data access)
class FeatureRepository:
    def save(self, feature: Feature) -> Feature:
        pass

# Service (business logic)
class FeatureService:
    def __init__(
        self,
        repository: FeatureRepository,
        validator: FeatureValidator
    ):
        self.repository = repository
        self.validator = validator

    def create_feature(self, name: str, description: str) -> Feature:
        # Business logic: validate, create, save
        self.validator.validate_name(name)
        feature = Feature(name=name, description=description)
        return self.repository.save(feature)

    def update_feature(self, id: int, updates: dict) -> Feature:
        # Business logic: get, validate, update, save
        feature = self.repository.get(id)
        self.validator.validate_updates(updates)
        updated = feature.copy(update=updates)
        return self.repository.save(updated)
```

### When to Use
- Complex business logic
- Multiple repositories needed per operation
- Transactions or orchestration required
- Want to reuse business logic

### Pros
- Centralizes business logic
- Testable
- Reusable across interfaces (CLI, API, etc.)
- Clear entry points

### Cons
- Can become "god objects"
- May mix concerns if not careful
- Extra layer of indirection

**Best for:** Complex tools in this project (command_builder, skill_builder)

---

## Builder Pattern

### Description
Separates construction of complex objects from their representation, allowing step-by-step creation.

### Structure
```python
class SkillBuilder:
    """Builds Skill objects step by step."""

    def __init__(self):
        self.skill = Skill()

    def set_name(self, name: str) -> "SkillBuilder":
        self.skill.name = name
        return self

    def set_description(self, description: str) -> "SkillBuilder":
        self.skill.description = description
        return self

    def add_tool(self, tool: str) -> "SkillBuilder":
        self.skill.allowed_tools.append(tool)
        return self

    def build(self) -> Skill:
        # Validate complete object
        if not self.skill.name:
            raise ValueError("Skill name required")
        return self.skill

# Usage (fluent interface)
skill = (SkillBuilder()
    .set_name("analysis")
    .set_description("Analyze requirements")
    .add_tool("Read")
    .add_tool("Grep")
    .build())
```

### When to Use
- Objects have many optional parameters
- Construction process is complex
- Want to ensure valid final object
- Fluent API desired

### Pros
- Fluent, readable API
- Ensures object validity
- Flexible construction
- Clear intent

### Cons
- More code than simple constructors
- May be overkill for simple objects

**Best for:** command_builder, skill_builder in this project

---

## Factory Pattern

### Description
Creates objects without specifying their exact class, delegating instantiation to factory methods or classes.

### Structure
```python
# Factory Method
class RepositoryFactory:
    @staticmethod
    def create(storage_type: str) -> FeatureRepository:
        if storage_type == "filesystem":
            return FileSystemRepository()
        elif storage_type == "database":
            return DatabaseRepository()
        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

# Usage
repo = RepositoryFactory.create("filesystem")

# Or: Factory with configuration
class ServiceFactory:
    def __init__(self, config: Config):
        self.config = config

    def create_service(self) -> FeatureService:
        repo = self.create_repository()
        validator = self.create_validator()
        return FeatureService(repo, validator)

    def create_repository(self) -> FeatureRepository:
        return FileSystemRepository(self.config.data_dir)

    def create_validator(self) -> FeatureValidator:
        return FeatureValidator(self.config.validation_rules)
```

### When to Use
- Need to decouple object creation from usage
- Object type determined at runtime
- Multiple related objects need creation
- Want centralized creation logic

### Pros
- Decouples creation from usage
- Easy to add new types
- Centralized instantiation logic

### Cons
- Extra abstraction
- More classes to maintain

**Best for:** Creating services/repositories in this project

---

## Command Pattern

### Description
Encapsulates requests as objects, allowing parameterization, queuing, and logging of operations.

### Structure
```python
from abc import ABC, abstractmethod

# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

# Concrete commands
class CreateSkillCommand(Command):
    def __init__(self, builder: SkillBuilder, name: str):
        self.builder = builder
        self.name = name
        self.created_skill = None

    def execute(self) -> None:
        self.created_skill = self.builder.create(self.name)

    def undo(self) -> None:
        if self.created_skill:
            self.builder.delete(self.created_skill.name)

# Invoker
class CommandInvoker:
    def __init__(self):
        self.history = []

    def execute(self, command: Command) -> None:
        command.execute()
        self.history.append(command)

    def undo_last(self) -> None:
        if self.history:
            command = self.history.pop()
            command.undo()
```

### When to Use
- Need undo/redo functionality
- Want to queue/log operations
- Decouple sender from receiver
- Need transaction-like behavior

### Pros
- Decouples sender and receiver
- Easy to add new commands
- Supports undo/redo
- Can queue and log commands

### Cons
- Many small classes
- May be overkill for simple operations

**Use sparingly** in this project

---

## Choosing the Right Pattern

### For This Project (LLM Config Management)

**Primary Architecture:** Modular (Package-Based)
- Each tool is a self-contained module
- Clear feature boundaries
- Independent development

**Within Each Module:**
- **Service Layer**: For complex business logic (command_builder, skill_builder)
- **Repository Pattern**: For file system operations
- **Builder Pattern**: For constructing complex objects (commands, skills, agents)
- **Factory Pattern**: For creating services with dependencies

### Decision Matrix

| Pattern | Complexity | Testability | Flexibility | Best For |
|---------|------------|-------------|-------------|----------|
| Layered | Medium | High | Medium | Standard apps |
| Modular | Low | High | High | **This project** |
| Repository | Medium | Very High | High | Data access |
| Service Layer | Medium | High | Medium | Business logic |
| Builder | Low | High | High | Complex objects |
| Factory | Low | High | High | Object creation |
| Command | High | High | High | Undo/transaction |

---

## Anti-Patterns to Avoid

### 1. God Object
**Problem:** One class/module does everything
**Solution:** Split into focused, single-responsibility modules

### 2. Spaghetti Code
**Problem:** No clear structure, tangled dependencies
**Solution:** Use layered or modular architecture

### 3. Circular Dependencies
**Problem:** Module A imports B, B imports A
**Solution:** Extract shared code to separate module, use dependency injection

### 4. Tight Coupling
**Problem:** Modules directly depend on implementation details
**Solution:** Use interfaces/abstract base classes, dependency injection

### 5. Anemic Domain Model
**Problem:** Models with no behavior, only data
**Solution:** Add business logic methods to models (when appropriate)

---

## References

- [Martin Fowler - Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/)
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Design Patterns](https://python-patterns.guide/)
