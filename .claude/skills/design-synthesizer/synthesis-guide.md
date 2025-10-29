# Design Synthesis Guide

**Purpose**: Comprehensive guide for synthesizing outputs from multiple parallel sub-agents (Architecture Designer, Documentation Researcher, Dependency Manager) into cohesive, integrated design.

**Version**: 2.0.0
**Phase**: 2 (Design & Planning)
**Created**: 2025-10-29

---

## Table of Contents

1. [Overview](#overview)
2. [Cross-Referencing Methodology](#cross-referencing-methodology)
3. [Consistency Checking Procedures](#consistency-checking-procedures)
4. [Conflict Resolution Strategies](#conflict-resolution-strategies)
5. [Gap Identification Techniques](#gap-identification-techniques)
6. [Quality Validation Criteria](#quality-validation-criteria)

---

## Overview

Design synthesis is the process of integrating outputs from multiple independent sub-agents into a unified, coherent design document. This requires careful cross-referencing, consistency checking, conflict resolution, and gap identification to ensure the final design is complete, consistent, and actionable.

### Synthesis Goals

1. **Integration**: Combine architecture, library documentation, and dependencies into single coherent design
2. **Consistency**: Ensure all design elements align and use consistent terminology
3. **Completeness**: Verify all components have implementation paths
4. **Actionability**: Provide clear, specific guidance for implementation
5. **Traceability**: Link all design decisions to requirements

### Synthesis Principles

- **Systematic Approach**: Follow structured methodology, don't skip steps
- **Document Everything**: Record all decisions, conflicts, and trade-offs
- **Transparency**: Make reasoning explicit and traceable
- **Quality Focus**: Don't accept "good enough" - aim for excellence
- **Continuous Validation**: Check consistency throughout synthesis, not just at the end

---

## Cross-Referencing Methodology

Cross-referencing connects related elements across different sub-agent outputs to create integrated design.

### Step 1: Create Cross-Reference Index

Build index mapping key elements across outputs:

**Index Structure**:
```markdown
## Cross-Reference Index

### Components
| Component | Architecture Doc | Library Used | Library Version | Dependencies | Docs Section |
|-----------|------------------|--------------|-----------------|--------------|--------------|
| Component A | Section 2.1 | Library X | 1.2.3 | dep-a, dep-b | Libraries 3.2 |
| Component B | Section 2.2 | Library Y | 2.0.0 | dep-c | Libraries 3.4 |

### Data Models
| Model | Architecture Doc | Library Pattern | Library Version | Validation | Docs Section |
|-------|------------------|-----------------|-----------------|------------|--------------|
| UserModel | Section 3.1 | Library X.ValidationMixin | 1.2.3 | Built-in | Libraries 3.2.1 |
| TaskModel | Section 3.2 | Custom | - | Manual | - |

### API Endpoints
| Endpoint | Architecture Doc | Library Method | Library Version | Dependencies | Docs Section |
|----------|------------------|----------------|-----------------|--------------|--------------|
| POST /users | Section 4.1 | Library X.create() | 1.2.3 | dep-a | Libraries 3.2.2 |
| GET /tasks | Section 4.2 | Library Y.list() | 2.0.0 | dep-c | Libraries 3.4.1 |

### Dependencies
| Dependency | Version | Required By | Conflicts | Resolution | Dependency Doc |
|------------|---------|-------------|-----------|------------|----------------|
| dep-a | >=1.0 | Library X | None | 1.5.0 | Dependencies 2.1 |
| dep-b | <3.0 | Library X | dep-c>=3.0 | 2.8.0 | Dependencies 2.2 |
```

### Step 2: Map Architecture → Libraries

For each architectural component, identify which libraries implement it:

**Mapping Template**:
```markdown
### Component: [Component Name]

**From Architecture Document**:
- **Purpose**: [What the component does]
- **Responsibilities**: [List of responsibilities]
- **Interfaces**: [APIs exposed or consumed]
- **Dependencies**: [Other components it depends on]

**Library Implementation**:
- **Primary Library**: [Library Name] v[Version]
- **API/Classes Used**: [Specific APIs from library]
- **Code Pattern**: [How library is used - link to docs]
- **Configuration**: [Any library configuration needed]

**Documentation Reference**:
- **Library Docs**: Libraries doc, section [X.Y]
- **Code Example**: [Link to example in library docs]
- **Best Practices**: [Link to best practices in library docs]

**Dependencies Required**:
- [Dependency 1]: [Purpose]
- [Dependency 2]: [Purpose]
```

**Example**:
```markdown
### Component: UserAuthenticationService

**From Architecture Document**:
- **Purpose**: Authenticate users via email/password
- **Responsibilities**:
  - Validate credentials
  - Generate session tokens
  - Manage login sessions
- **Interfaces**:
  - `authenticate(email, password) -> Token`
  - `validate_token(token) -> User`
- **Dependencies**: UserRepository, TokenService

**Library Implementation**:
- **Primary Library**: PassLib v1.7.4
- **API/Classes Used**: `PassLib.hash.bcrypt`, `PassLib.verify()`
- **Code Pattern**: Use bcrypt with cost factor 12 (documented in libraries-42.md, section 3.1)
- **Configuration**: Set `BCRYPT_ROUNDS=12` in settings

**Documentation Reference**:
- **Library Docs**: libraries-42.md, section 3.1.2
- **Code Example**: libraries-42.md, Example 3.1.2.A
- **Best Practices**: Use salt, validate input, rate-limit attempts

**Dependencies Required**:
- passlib[bcrypt]: Password hashing
- python-jose: JWT token generation
```

### Step 3: Map Libraries → Dependencies

For each library, identify its dependency tree:

**Mapping Template**:
```markdown
### Library: [Library Name] v[Version]

**From Library Documentation**:
- **Purpose**: [What library does]
- **Key APIs**: [Main APIs used in architecture]
- **Integration Pattern**: [How to integrate]

**Dependencies**:
```
[Library Name]==[Version]
├── [dep-1]==[version]  # [Purpose]
│   └── [sub-dep]==[version]
├── [dep-2]==[version]  # [Purpose]
└── [optional-dep] (optional)  # [Purpose]
```

**From Dependency Analysis**:
- **Required Dependencies**: [List with versions]
- **Optional Dependencies**: [List with versions and when to use]
- **Version Constraints**: [Any restrictions]
- **Conflicts Detected**: [Any conflicts with other libraries]
- **Resolution**: [How conflicts were resolved]

**Installation**:
```bash
pip install [library-name]==[version]
# Dependencies auto-installed: [list]
```
```

**Example**:
```markdown
### Library: SQLAlchemy v2.0.0

**From Library Documentation**:
- **Purpose**: Python SQL toolkit and ORM
- **Key APIs**: declarative_base(), sessionmaker(), Query
- **Integration Pattern**: Define models with Base, create session, query

**Dependencies**:
```
sqlalchemy==2.0.0
├── greenlet==2.0.2  # Async support
├── typing-extensions>=4.2  # Type hints
└── asyncpg (optional)  # PostgreSQL async driver
```

**From Dependency Analysis** (dependencies-42.md, section 2.1):
- **Required Dependencies**: greenlet==2.0.2, typing-extensions==4.5.0
- **Optional Dependencies**: asyncpg==0.28.0 (for async PostgreSQL)
- **Version Constraints**: Python 3.9+
- **Conflicts Detected**: greenlet version conflict with gevent (resolved to 2.0.2)
- **Resolution**: Pin greenlet to 2.0.2 (compatible with both)

**Installation**:
```bash
pip install sqlalchemy==2.0.0
# Auto-installs: greenlet==2.0.2, typing-extensions==4.5.0
```
```

### Step 4: Map Data Models → Library Patterns

For each data model in architecture, map to library validation/serialization:

**Mapping Template**:
```markdown
### Data Model: [Model Name]

**From Architecture Document**:
- **Fields**: [List of fields with types]
- **Validation Rules**: [Required validations]
- **Relationships**: [Relations to other models]
- **Business Logic**: [Any model methods]

**Library Pattern**:
- **Base Class**: [Library base class to inherit]
- **Validation**: [How validation is implemented]
- **Serialization**: [How model is serialized]
- **Example Code**:
```python
# From libraries-42.md, Example 4.2.A
[Code example]
```

**Implementation Notes**:
- [Any special considerations]
- [Performance implications]
- [Testing approach]
```

### Step 5: Map API Contracts → Library Methods

For each API endpoint, map to library methods:

**Mapping Template**:
```markdown
### API Endpoint: [Method] [Path]

**From Architecture Document**:
- **Purpose**: [What endpoint does]
- **Request**: [Request format]
- **Response**: [Response format]
- **Error Handling**: [Error codes and messages]

**Library Implementation**:
- **Framework**: [Web framework] v[Version]
- **Handler Pattern**: [Route decorator, class-based view, etc.]
- **Request Parsing**: [Library method for request]
- **Response Formatting**: [Library method for response]
- **Error Handling**: [Library exception handling]

**Code Pattern** (from libraries-42.md, Example 5.3.B):
```python
[Code example showing endpoint implementation]
```

**Validation**:
- **Input**: [How request is validated]
- **Output**: [How response is validated]
```

### Step 6: Create Traceability Matrix

Build complete traceability matrix linking requirements → architecture → libraries → dependencies:

**Traceability Matrix**:
```markdown
| Requirement | Architecture | Component | Library | Version | Dependencies | Tests |
|-------------|--------------|-----------|---------|---------|--------------|-------|
| FR-001: User auth | Section 2.1 | UserAuthService | PassLib | 1.7.4 | bcrypt | test_auth.py |
| FR-002: Data export | Section 2.3 | ExportService | pandas | 2.0.0 | numpy | test_export.py |
| NFR-P-001: API < 200ms | Section 4 | All endpoints | FastAPI | 0.95.0 | uvicorn | test_performance.py |
```

This matrix ensures every requirement has implementation path through architecture → library → code.

---

## Consistency Checking Procedures

Consistency checking validates alignment across all sub-agent outputs.

### Check 1: Terminology Consistency

Verify consistent naming across documents:

**Procedure**:
1. Extract all entity names from each document:
   - Architecture: Component names, model names, API names
   - Libraries: Class names, function names
   - Dependencies: Package names

2. Build terminology map:
```markdown
| Concept | Architecture Doc | Library Doc | Dependency Doc | Standardized Name |
|---------|------------------|-------------|----------------|-------------------|
| User entity | "UserProfile" | "Profile" | "user_model" | **UserProfile** |
| Auth service | "AuthenticationService" | "AuthService" | "auth_svc" | **AuthenticationService** |
```

3. Flag inconsistencies:
```markdown
**Inconsistency Found**:
- Architecture calls it "UserProfile"
- Library docs call it "Profile"
- Dependency analysis calls it "user_model"

**Resolution**: Standardize to "UserProfile" (most descriptive)
**Action**: Update all references to use "UserProfile"
```

4. Create glossary:
```markdown
## Terminology Glossary
- **UserProfile**: User entity with id, name, email (Architecture: Section 3.1, Libraries: Section 4.2)
- **AuthenticationService**: Service handling user authentication (Architecture: Section 2.1, Libraries: Section 3.1)
```

### Check 2: Version Consistency

Verify library versions match across documents:

**Procedure**:
1. Extract all library versions from each document
2. Compare versions:
```markdown
| Library | Architecture Doc | Library Doc | Dependency Doc | Consistent? |
|---------|------------------|-------------|----------------|-------------|
| SQLAlchemy | 2.0.0 | 2.0.0 | 2.0.0 | ✅ Yes |
| Celery | Not mentioned | 5.3.0 | 5.2.0 | ⚠️  Mismatch |
```

3. Resolve mismatches:
```markdown
**Version Mismatch**: Celery
- Library doc says: 5.3.0
- Dependency analysis says: 5.2.0

**Investigation**:
- Check dependency analysis reasoning for 5.2.0
- Check if 5.3.0 breaks anything

**Resolution**: Use 5.3.0 (latest stable, no breaking changes)
**Update**: Dependency document updated to 5.3.0
```

### Check 3: API Alignment

Verify architecture API contracts align with library capabilities:

**Procedure**:
1. For each API endpoint in architecture:
   - Check if library supports the operation
   - Verify request/response formats match library expectations
   - Confirm error handling aligns with library patterns

2. Create alignment matrix:
```markdown
| API Endpoint | Architecture Design | Library Support | Aligned? | Notes |
|--------------|---------------------|-----------------|----------|-------|
| POST /users | Create user with email | ✅ Supported | ✅ Yes | Use Library.create() |
| DELETE /users/:id | Soft delete | ⚠️  Hard delete only | ❌ No | Need to implement soft delete |
```

3. Flag misalignments:
```markdown
**API Misalignment**: DELETE /users/:id
- **Architecture Design**: Soft delete (set deleted_at timestamp)
- **Library Support**: Only hard delete (remove from database)

**Options**:
1. Implement soft delete logic (add deleted_at field, filter queries)
2. Change architecture to use hard delete

**Decision**: Implement soft delete (requirement NFR-S-003 mandates data retention)
**Implementation**: Add deleted_at field, override Library.delete() method
```

### Check 4: Data Model Validation

Verify data models in architecture match library validation patterns:

**Procedure**:
1. For each data model:
   - Check field types match library expectations
   - Verify validations can be implemented with library
   - Confirm relationships align with library ORM patterns

2. Create validation matrix:
```markdown
| Model | Field | Architecture Type | Library Pattern | Validation Method | Aligned? |
|-------|-------|-------------------|-----------------|-------------------|----------|
| User | email | EmailStr | Email validator | Pydantic EmailStr | ✅ Yes |
| User | age | int (18-120) | Integer | Range validator | ✅ Yes (Field(ge=18, le=120)) |
| Task | status | Enum | String | Custom validator | ⚠️  Need enum |
```

3. Resolve validation mismatches:
```markdown
**Validation Mismatch**: Task.status
- **Architecture**: Enum (PENDING, RUNNING, COMPLETED, FAILED)
- **Library**: Stores as string, no built-in enum validation

**Solution**: Create Python Enum and use Pydantic validation
```python
from enum import Enum
from pydantic import BaseModel, validator

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(BaseModel):
    status: TaskStatus
```
```

### Check 5: Dependency Compatibility

Verify all dependencies are compatible:

**Procedure**:
1. Check dependency tree for conflicts
2. Verify version constraints are satisfiable
3. Check for circular dependencies
4. Validate Python version compatibility

**Compatibility Checklist**:
```markdown
## Dependency Compatibility Check

### Version Conflicts
- ✅ No conflicting version constraints
- ⚠️  greenlet: Library A needs >=2.0, Library B needs <2.5 (resolved to 2.0.2)

### Circular Dependencies
- ✅ No circular dependencies detected

### Python Version
- ✅ All libraries support Python 3.9+
- ⚠️  Library C requires Python 3.10+ (need to upgrade or find alternative)

### Operating System
- ✅ All libraries are cross-platform
- ⚠️  Library D has Linux-only dependency (need Windows alternative)
```

---

## Conflict Resolution Strategies

When inconsistencies or conflicts are found, use these strategies to resolve them.

### Strategy 1: Priority-Based Resolution

When multiple options exist, use priority rules:

**Priority Rules**:
1. **Requirements**: Requirements from analysis document always take precedence
2. **Security**: Security considerations override performance/convenience
3. **Stability**: Stable, well-tested libraries preferred over cutting-edge
4. **Standards**: Industry standards and best practices preferred
5. **Performance**: Performance considerations after correctness/security

**Example**:
```markdown
**Conflict**: Library choice for JSON serialization
- **Option A**: orjson (faster, but non-standard API)
- **Option B**: standard json (slower, but standard library)

**Resolution**:
- Priority 4 (Standards) says: Use standard library where possible
- **Decision**: Use standard json module
- **Rationale**: Performance difference minimal for use case, standard library reduces dependencies
- **Exception**: If performance testing shows bottleneck, revisit
```

### Strategy 2: Trade-Off Analysis

Document trade-offs when choosing between conflicting approaches:

**Trade-Off Template**:
```markdown
**Conflict**: [Description]

**Option 1**: [Approach 1]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Cost**: [Implementation time/complexity]
- **Risk**: [Potential issues]

**Option 2**: [Approach 2]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Cost**: [Implementation time/complexity]
- **Risk**: [Potential issues]

**Decision**: [Chosen option]
**Rationale**: [Why this option was chosen]
**Trade-Off**: [What we're giving up]
**Mitigation**: [How to address cons of chosen option]
```

**Example**:
```markdown
**Conflict**: Async vs Sync implementation

**Option 1**: Full async with asyncio
- **Pros**: Better concurrency, modern approach
- **Cons**: More complex, some libraries don't support async
- **Cost**: 2-3 additional days development
- **Risk**: Medium - team less familiar with async patterns

**Option 2**: Sync with threading
- **Pros**: Simpler, all libraries support sync
- **Cons**: Less efficient concurrency
- **Cost**: Baseline
- **Risk**: Low - team familiar with threading

**Decision**: Sync with threading
**Rationale**: Team familiarity, lower risk, faster delivery
**Trade-Off**: Giving up some concurrency efficiency
**Mitigation**: Profile performance, can refactor to async later if needed
```

### Strategy 3: Hybrid Approach

Sometimes best solution is combination of conflicting approaches:

**Hybrid Template**:
```markdown
**Conflict**: [Description]

**Approach A**: [Full commitment to option A]
**Approach B**: [Full commitment to option B]

**Hybrid Solution**: [Combine aspects of both]
- **Use A for**: [Specific use cases]
- **Use B for**: [Different use cases]
- **Integration**: [How they work together]

**Benefits**:
- [Advantages of hybrid approach]

**Drawbacks**:
- [Disadvantages and mitigation]
```

**Example**:
```markdown
**Conflict**: ORM vs Raw SQL

**Approach A**: Full ORM (SQLAlchemy) for everything
**Approach B**: Raw SQL for everything

**Hybrid Solution**:
- **Use ORM for**: CRUD operations, standard queries
- **Use Raw SQL for**: Complex analytical queries, performance-critical operations
- **Integration**: ORM for 80% of queries, raw SQL for specialized needs

**Benefits**:
- Developer productivity for common operations (ORM)
- Performance for complex operations (raw SQL)
- Flexibility to choose best tool per use case

**Drawbacks**:
- Need to maintain both approaches (mitigate with clear guidelines)
- Potential for inconsistent patterns (mitigate with code review)
```

### Strategy 4: Escalation

When conflicts cannot be resolved:

**Escalation Process**:
1. Document the conflict clearly
2. List all options considered
3. Explain why resolution is unclear
4. Flag for Phase 3 (Implementation) to resolve
5. Provide recommendation with uncertainty noted

**Escalation Template**:
```markdown
**Unresolved Conflict**: [Description]

**Context**: [Background and importance]

**Options Considered**:
1. [Option 1] - [Pros/Cons]
2. [Option 2] - [Pros/Cons]

**Why Unresolved**: [What information is missing or ambiguous]

**Recommendation**: [Tentative suggestion]
**Uncertainty**: [What could go wrong]
**Resolution Needed By**: [Phase/milestone]
**Who Decides**: [Implementation Specialist / Stakeholder]
```

---

## Gap Identification Techniques

Identify missing information, unresolved issues, and incomplete specifications.

### Technique 1: Completeness Checklist

Use systematic checklist to find gaps:

**Architecture Completeness**:
- [ ] All components have defined responsibilities
- [ ] All components have defined interfaces
- [ ] All data models have complete field definitions
- [ ] All API endpoints have request/response specs
- [ ] All error conditions have handling strategies
- [ ] All data flows are documented
- [ ] All external integrations are specified

**Library Documentation Completeness**:
- [ ] All libraries have version numbers
- [ ] All libraries have installation instructions
- [ ] All library APIs used have documentation references
- [ ] All libraries have code examples
- [ ] All libraries have known issues documented
- [ ] All library configurations are specified

**Dependency Completeness**:
- [ ] All dependencies have version constraints
- [ ] All version conflicts are resolved
- [ ] All installation order is documented
- [ ] All system dependencies are listed
- [ ] All optional dependencies are noted

### Technique 2: Cross-Reference Gap Analysis

Compare cross-reference index to find gaps:

**Gap Analysis Matrix**:
```markdown
| Component | Has Architecture? | Has Library? | Has Dependencies? | Has Tests? | Complete? |
|-----------|-------------------|--------------|-------------------|------------|-----------|
| Component A | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Complete |
| Component B | ✅ Yes | ⚠️  Partial | ✅ Yes | ❌ No | ❌ Incomplete |
| Component C | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ Incomplete |

**Gaps Identified**:
- Component B: Library integration partially documented, missing code example
- Component C: No library selected, no dependencies identified, no test plan
```

### Technique 3: Question-Based Gap Analysis

Ask probing questions about each design element:

**Question Framework**:
For each component:
- What does it do? (functionality)
- How is it implemented? (library/pattern)
- What does it depend on? (dependencies)
- How is it configured? (settings)
- How is it tested? (test strategy)
- What can go wrong? (error handling)
- How does it perform? (performance)

**Example**:
```markdown
### Component: EmailService

**What does it do?**
✅ Sends transactional emails (password reset, notifications)

**How is it implemented?**
⚠️  Partially defined - uses "email library" but specific library not chosen

**What does it depend on?**
❌ Gap - SMTP server configuration not specified

**How is it configured?**
❌ Gap - Email templates location not defined

**How is it tested?**
❌ Gap - No test strategy for email sending

**What can go wrong?**
✅ Error handling for SMTP failures documented

**How does it perform?**
⚠️  Partial - "should be fast" but no specific requirements

**Gaps to Address**:
1. Choose specific email library (e.g., email-validator, aiosmtplib)
2. Specify SMTP configuration (server, port, authentication)
3. Define email template storage and format
4. Create test strategy (mock SMTP server for tests)
5. Quantify performance requirements (e.g., <2s to send email)
```

### Technique 4: Implementation Path Validation

For each architectural element, verify clear path to implementation:

**Implementation Path Checklist**:
```markdown
### Component: [Component Name]

**Architecture Design**: ✅ Complete
**Library Selected**: ✅ SQLAlchemy 2.0.0
**Library Documented**: ✅ Code examples provided
**Dependencies Resolved**: ✅ All dependencies compatible
**Implementation Pattern**: ✅ declarative_base() pattern documented

**Can Implement?**: ✅ Yes - all information available

---

### Component: [Another Component]

**Architecture Design**: ✅ Complete
**Library Selected**: ⚠️  "Message queue library" (generic)
**Library Documented**: ❌ No specific documentation
**Dependencies Resolved**: ❌ Cannot resolve until library chosen
**Implementation Pattern**: ❌ Pattern unknown

**Can Implement?**: ❌ No - library selection required

**Gaps**:
1. Choose specific message queue library (RabbitMQ vs Redis vs Celery)
2. Fetch documentation for chosen library
3. Resolve dependencies for chosen library
4. Document integration pattern
```

---

## Quality Validation Criteria

Final quality checks before synthesis is complete.

### Criterion 1: Completeness

**Validation Checklist**:
- [ ] All architecture components have library implementations
- [ ] All libraries have complete documentation references
- [ ] All dependencies are resolved with specific versions
- [ ] All data models have validation strategies
- [ ] All API endpoints have implementation patterns
- [ ] All error conditions have handling strategies
- [ ] All gaps are documented (if any)

**Completeness Score**: [X/Y complete] - [% complete]

### Criterion 2: Consistency

**Validation Checklist**:
- [ ] Terminology is consistent across all documents
- [ ] Version numbers match in all references
- [ ] API contracts align with library capabilities
- [ ] Data models align with library patterns
- [ ] Dependencies are compatible with each other
- [ ] Architecture patterns follow library best practices

**Consistency Issues**: [Number] - [List if any]

### Criterion 3: Actionability

**Validation Checklist**:
- [ ] Implementation steps are clear and specific
- [ ] Code patterns are documented with examples
- [ ] Installation instructions are complete
- [ ] Configuration requirements are specified
- [ ] Testing approaches are defined
- [ ] Every design decision has rationale

**Actionability Assessment**: [Clear / Partially Clear / Unclear]

### Criterion 4: Traceability

**Validation Checklist**:
- [ ] All design elements trace to requirements
- [ ] All library choices have justification
- [ ] All design decisions are documented
- [ ] All conflicts show resolution reasoning
- [ ] All trade-offs are explained

**Traceability Matrix**: [Complete / Incomplete]

### Criterion 5: Feasibility

**Validation Checklist**:
- [ ] All libraries are available and maintained
- [ ] All dependencies can be installed
- [ ] No circular dependencies
- [ ] No unresolvable version conflicts
- [ ] Implementation is achievable with available resources

**Feasibility Assessment**: [Feasible / At Risk / Not Feasible]

---

## Summary

Design synthesis requires systematic approach:

1. **Cross-Reference**: Map all elements across sub-agent outputs
2. **Check Consistency**: Validate alignment in terminology, versions, APIs, data models, dependencies
3. **Resolve Conflicts**: Use priority rules, trade-off analysis, hybrid approaches, or escalate
4. **Identify Gaps**: Use checklists, cross-reference analysis, probing questions, implementation path validation
5. **Validate Quality**: Check completeness, consistency, actionability, traceability, feasibility

**Success Indicators**:
- ✅ 100% of components mapped to libraries
- ✅ 100% of dependencies resolved
- ✅ All terminology consistent
- ✅ All conflicts resolved or escalated with recommendation
- ✅ All gaps identified and documented
- ✅ Clear implementation path for every architectural element

---

**Remember**: Synthesis is not about perfection, but about creating the best possible design given available information, while clearly documenting any limitations, uncertainties, or gaps that need resolution during implementation.
