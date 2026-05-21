# Implementation Documentation Template

**Location**: `docs/implementation/issue-<number>-<feature-name>.md`

```markdown
# Implementation: Issue #<number> - <Feature Name>

## Overview

Brief description of what was implemented and why.

## Solution Approach

Detailed explanation of the implementation approach:

- Architecture pattern used (e.g., repository pattern, service layer)
- Key design decisions and rationale
- Trade-offs considered
- Alternative approaches rejected and why

## Architecture

### Component Structure
```

src/tools/feature/
├── **init**.py # Public API exports
├── models.py # Data models (Pydantic)
├── interfaces.py # Abstract interfaces
├── core.py # Business logic
├── repository.py # Data access layer
├── validators.py # Input validation
└── exceptions.py # Custom exceptions

````

### Data Flow
[Describe how data flows through the system]

### Key Components

#### ComponentName
- **Purpose**: [What it does]
- **Responsibilities**: [What it's responsible for]
- **Dependencies**: [What it depends on]

## Implementation Details

### Models
[Document Pydantic models and their fields]

### Business Logic
[Document core algorithms and workflows]

### Data Access
[Document repository methods and database interactions]

### Validation
[Document validation rules and error handling]

## Security Measures
- **Authentication**: [How auth is handled]
- **Authorization**: [Permission checks implemented]
- **Input Validation**: [Validation at entry points]
- **Output Sanitization**: [XSS prevention measures]
- **Data Protection**: [Encryption, secure storage]
- **Secrets Management**: [How secrets are handled]

## Performance Optimizations
- **Caching**: [Caching strategy if applicable]
- **Database**: [Query optimization, indexing]
- **Async Operations**: [Use of async/await]
- **Resource Management**: [Memory, connections]
- **Response Times**: [Measured response times]

## Testing
- **Unit Test Coverage**: [percentage]%
- **Integration Tests**: [what's covered]
- **Security Tests**: [auth, validation, etc.]
- **Performance Tests**: [benchmarks met]
- **Edge Cases**: [scenarios tested]

## Configuration
Environment variables required:
```bash
FEATURE_API_KEY=your_api_key
FEATURE_TIMEOUT=30
FEATURE_DEBUG=false
````

## Dependencies

New dependencies added:

- `package-name==version`: [reason for dependency]

## Breaking Changes

[List any breaking changes or "None"]

## Migration Notes

[Steps needed to migrate or "None required"]

## Known Issues

- [Issue 1]: [Description and workaround]

## Future Enhancements

- [Enhancement 1]: [Description]

## References

- Original Issue: #<number>
- Pull Request: #<pr-number>
- Related Issues: #<related-issues>
- Design Document: docs/architecture/<design-doc>.md

```

```
