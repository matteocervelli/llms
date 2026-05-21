# Architecture Design — Patterns

## Pattern Selection Guide

| Pattern          | Best For                           | Trade-off                                  |
| ---------------- | ---------------------------------- | ------------------------------------------ |
| **Layered**      | CRUD apps, clear data flow         | Rigid layers, can lead to pass-through     |
| **Hexagonal**    | Complex domains, many integrations | More abstractions, higher initial cost     |
| **Modular**      | Feature-rich apps, team separation | Module boundary discipline required        |
| **Event-Driven** | Async workflows, decoupled systems | Debugging complexity, eventual consistency |

## Layered Architecture (Most Common)

```
Presentation → Business → Data
     ↓              ↓          ↓
  Routes/CLI    Services    Repositories
  Schemas       Models      Adapters
  Validators    Rules       Clients
```

**Rule**: Dependencies flow down only. Business layer never imports from presentation.

## Hexagonal Architecture (Ports & Adapters)

```
              ┌─────────────────┐
  Adapters → │    Ports (IN)    │
              │   ┌───────────┐ │
              │   │   Core    │ │ ← Domain logic
              │   │  Domain   │ │
              │   └───────────┘ │
              │   Ports (OUT)   │ → Adapters
              └─────────────────┘
```

**When**: Multiple input channels (API + CLI + events) or multiple output targets (DB + cache + external).

## Component Design Checklist

- [ ] Each component has ONE primary responsibility
- [ ] Components are independently testable (no global state)
- [ ] Dependencies injected via constructor (not imported directly)
- [ ] Interfaces/Protocols used for cross-layer communication
- [ ] Files < 500 lines (split by responsibility if exceeded)
- [ ] Extension points identified for likely future changes

## Dependency Injection Pattern

```python
class IRepository(Protocol):
    async def save(self, data: dict) -> bool: ...
    async def get(self, id: str) -> dict: ...

class Service:
    def __init__(self, repo: IRepository):
        self.repo = repo  # Injected, mockable, swappable
```

## Design Patterns Quick Reference

- **Repository**: Abstract data access → swap DB implementations
- **Strategy**: Pluggable algorithms → multiple processing modes
- **Factory**: Complex object creation → decouple construction
- **Observer**: Event notification → decouple producers/consumers
- **Adapter**: External system integration → normalize interfaces
