# Architecture Design — Summary

## Core Approach

Design component architecture using established patterns for clean, maintainable systems.

## Key Decisions

1. **Choose architectural pattern**: Layered (UI→Logic→Data), Hexagonal (Ports & Adapters), or Modular
2. **Define component boundaries**: Each component = one responsibility, independently testable
3. **Establish dependency direction**: Outer layers depend on inner; never reverse
4. **Plan dependency injection**: Constructor injection for required deps, protocols for abstractions
5. **Design extension points**: Strategy/Observer/Factory patterns where future flexibility needed

## Standard Structure

```
src/
├── interfaces/     # Presentation layer (CLI, API routes, schemas)
├── core/           # Business layer (models, services, validators, processors)
├── adapters/       # Data layer (DB, external APIs, file storage, cache)
├── config/         # Configuration (settings, env)
└── utils/          # Shared utilities (pure, stateless)
```

## When to Go Deeper

- Ask for **patterns** → architectural pattern comparison and selection guidance
- Ask for **full reference** → complete architecture-patterns.md and component-design-guide.md
