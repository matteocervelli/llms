# ADR-002: LLM Adapter Architecture

**Status**: Accepted
**Date**: 2025-10-26
**Authors**: Matteo Cervelli
**Related Issues**: [#3](https://github.com/matteocervelli/llms/issues/3)

## Context

The LLM Configuration Management System needs to support multiple LLM providers (Claude Code, Codex, OpenCode, future providers) while maintaining a consistent developer experience. Each LLM provider has different:

- **File formats**: Claude uses Markdown, others might use JSON, YAML, or custom formats
- **Directory structures**: Different providers organize skills/commands/agents differently
- **Configuration requirements**: Each provider may have unique configuration needs
- **Feature sets**: Not all providers support the same features (skills, commands, agents, hooks, plugins)

We needed an architecture that:
1. Provides a uniform interface for creating and managing LLM elements
2. Abstracts provider-specific implementation details
3. Allows easy addition of new LLM providers
4. Integrates seamlessly with the existing Scope Intelligence System
5. Maintains type safety and comprehensive testing

## Decision

We will implement the **Adapter Pattern** with the following architecture:

### Core Components

1. **`LLMAdapter` (Abstract Base Class)**
   - Defines the interface that all adapters must implement
   - Provides common validation and sanitization methods
   - Enforces consistent behavior across adapters

2. **Concrete Adapters** (`ClaudeAdapter`, future `CodexAdapter`, etc.)
   - Implement provider-specific logic
   - Handle file formats and directory structures
   - Provide metadata about capabilities

3. **Data Models** (`CreationResult`, `AdapterMetadata`, `ElementType`)
   - Standardize return values and configuration
   - Enable type-safe interactions
   - Provide clear contracts

4. **Custom Exceptions** (`AdapterError`, `InvalidNameError`, `CreationError`)
   - Provide clear error messaging
   - Enable precise error handling
   - Follow Python exception hierarchy

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Code                               │
│                (Tools, CLI, API)                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              LLMAdapter (Abstract Base Class)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Abstract Methods:                                    │   │
│  │  - create_skill(name, description, content)          │   │
│  │  - create_command(name, description, content)        │   │
│  │  - create_agent(name, description, content)          │   │
│  │  - _get_metadata()                                   │   │
│  │                                                       │   │
│  │ Common Methods:                                      │   │
│  │  - validate_name(name, element_type)                 │   │
│  │  - sanitize_input(text, max_length)                  │   │
│  │  - _ensure_directory_exists(directory)               │   │
│  └──────────────────────────────────────────────────────┘   │
└───┬────────────────────────────────┬────────────────────────┘
    │                                │
    ▼                                ▼
┌─────────────────┐      ┌──────────────────────┐
│ ClaudeAdapter   │      │  Future Adapters:    │
│                 │      │  - CodexAdapter      │
│ - Markdown      │      │  - OpenCodeAdapter   │
│ - .claude/      │      │  - etc.              │
│ - skills/       │      │                      │
│ - commands/     │      │                      │
│ - agents/       │      │                      │
└─────────────────┘      └──────────────────────┘
```

### Key Design Decisions

#### 1. Adapter Pattern over Strategy Pattern
- **Rationale**: Adapters encapsulate complete provider implementations, not just algorithms
- **Benefit**: Clear separation between provider logic and common validation

#### 2. Abstract Base Class over Duck Typing
- **Rationale**: Enforces interface compliance at class definition time
- **Benefit**: Type safety, IDE support, clear contracts

#### 3. Dataclasses for Models
- **Rationale**: Immutable, type-safe data structures with automatic methods
- **Benefit**: Less boilerplate, better type hints, clear documentation

#### 4. Scope Integration
- **Rationale**: Adapters receive `ScopeConfig` from `ScopeManager`
- **Benefit**: Consistent scope handling, no duplication of scope logic

#### 5. Template Rendering in Adapters
- **Rationale**: Each adapter controls its own file format
- **Benefit**: Provider-specific formatting without central template complexity

## Consequences

### Positive

✅ **Extensibility**: Adding new LLM providers requires only implementing a new adapter
✅ **Maintainability**: Provider-specific code is isolated in dedicated adapters
✅ **Type Safety**: Abstract base class ensures all adapters implement required methods
✅ **Testability**: Each adapter can be tested independently with mocks
✅ **Consistency**: Common validation/sanitization logic shared across all adapters
✅ **Integration**: Seamless integration with existing Scope Intelligence System
✅ **Documentation**: Clear interface makes adapter development straightforward

### Negative

⚠️ **Abstraction Overhead**: Simple providers may not need full adapter complexity
⚠️ **Code Duplication**: Some similar logic may exist across adapters
⚠️ **Learning Curve**: Developers must understand adapter pattern to add providers

### Mitigation Strategies

1. **Abstraction Overhead**: Provide base implementation methods that simple adapters can use
2. **Code Duplication**: Extract common patterns into utility modules as they emerge
3. **Learning Curve**: Comprehensive documentation and examples for adding new adapters

## Implementation Details

### File Organization

```
src/core/
├── adapter_exceptions.py    # Custom exception classes
├── adapter_models.py         # Data models (dataclasses)
├── llm_adapter.py           # Abstract base class and ClaudeAdapter
└── scope_manager.py         # Existing scope intelligence

tests/
├── test_llm_adapter.py           # Unit tests
└── test_adapter_integration.py   # Integration tests with ScopeManager
```

### Security Measures

- **Input Validation**: All names validated against regex pattern `^[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?$`
- **Length Limits**: Names ≤ 64 chars, descriptions ≤ 500 chars (configurable)
- **Path Traversal Prevention**: Use `Path.resolve()`, no `../` allowed
- **Sanitization**: Remove control characters (except newlines), null bytes
- **Permission Checks**: Verify write permissions before file operations

### Performance Targets

- Single file creation: < 50ms
- Name validation: < 5ms
- Template rendering: < 10ms

All targets based on local filesystem operations, no network I/O.

## Alternatives Considered

### Alternative 1: Single Monolithic Class with Conditionals

```python
class LLMManager:
    def create_skill(self, provider, name, description, content):
        if provider == "claude":
            # Claude-specific logic
        elif provider == "codex":
            # Codex-specific logic
        # etc.
```

**Rejected because**:
- Violates Open/Closed Principle (must modify class for new providers)
- Poor testability (complex conditional logic)
- Difficult to maintain as providers grow

### Alternative 2: Plugin System with Dynamic Loading

```python
# Load adapters dynamically from plugins/
adapters = load_plugins_from_directory("plugins/")
adapter = adapters["claude"]
```

**Rejected because**:
- Adds complexity without clear benefit for Sprint 1
- Harder to debug and test
- Can be added later if needed without changing current architecture

### Alternative 3: Factory Pattern

```python
class AdapterFactory:
    @staticmethod
    def create_adapter(provider_name):
        if provider_name == "claude":
            return ClaudeAdapter()
        # etc.
```

**Partially adopted**:
- Factory pattern may be added in Sprint 2 for convenience
- Current architecture doesn't preclude factory addition
- Direct instantiation is simpler for Sprint 1

## Future Considerations

### Sprint 2+

1. **Adapter Factory**: Add `AdapterFactory.create(provider, scope)` for convenience
2. **Template System**: Extract common templates for reusable content blocks
3. **Adapter Registry**: Dynamic adapter discovery and registration
4. **Validation Plugins**: Extensible validation rules per provider
5. **Batch Operations**: Support creating multiple elements in single transaction

### Long-term

1. **Async Support**: Add async variants for network-based LLM providers
2. **Versioning**: Support multiple versions of same provider adapter
3. **Migration Tools**: Convert between different provider formats
4. **Adapter Chaining**: Compose adapters for advanced workflows

## References

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns) (Gang of Four)
- [Python ABC Documentation](https://docs.python.org/3/library/abc.html)
- [ADR-001: Scope Intelligence System](./ADR-001-scope-intelligence-system.md)
- [GitHub Issue #3: Build Basic LLM Adapter Architecture](https://github.com/matteocervelli/llms/issues/3)

## Changelog

- **2025-10-26**: Initial version, Sprint 1 implementation
