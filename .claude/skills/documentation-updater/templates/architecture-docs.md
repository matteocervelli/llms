# Architecture Documentation Template

**Location**: `docs/architecture/<feature-name>-architecture.md`

Use for complex features with multiple components or significant design decisions.

```markdown
# Architecture: <Feature Name>

## Context

Why was this architecture needed?

## Architecture Overview

### System Diagram
```

┌─────────────┐
│ Client │
└──────┬──────┘
│
┌──────▼──────────┐
│ API Layer │
└──────┬──────────┘
│
┌──────▼──────────┐
│ Service Layer │
└──────┬──────────┘
│
┌──────▼──────────┐
│ Repository │
└──────┬──────────┘
│
┌──────▼──────────┐
│ Data Store │
└─────────────────┘

```

### Components

#### API Layer
- **Responsibility**: Handle HTTP requests/responses
- **Technology**: FastAPI/Flask
- **Key Files**: `api/endpoints.py`

#### Service Layer
- **Responsibility**: Business logic
- **Technology**: Pure Python
- **Key Files**: `core.py`

#### Repository Layer
- **Responsibility**: Data access
- **Technology**: SQLAlchemy/File System
- **Key Files**: `repository.py`

## Design Decisions

### Decision 1: <Decision>
**Context**: [Why this decision was needed]
**Options Considered**:
1. Option A: [Description] - Rejected because [reason]
2. Option B: [Description] - **Selected** because [reason]

**Consequences**:
- Positive: [benefit]
- Negative: [trade-off]

### Decision 2: <Decision>
[Same format]

## Data Flow

### Create Flow
```

1. Client sends POST request with data
2. API layer validates request format
3. Service layer validates business rules
4. Repository persists data
5. Response returned to client

```

### Read Flow
[Describe]

## Security Architecture
- Authentication: [mechanism]
- Authorization: [RBAC, ABAC, etc.]
- Data Protection: [encryption, etc.]

## Performance Considerations
- Caching: [strategy]
- Scaling: [horizontal/vertical]
- Bottlenecks: [identified and mitigated]

## Integration Points
- System A: [how it integrates]
- System B: [how it integrates]

## Future Considerations
- Scalability: [how to scale]
- Evolution: [how to extend]
```
