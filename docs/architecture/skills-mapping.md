# Skills Mapping - Feature-Implementer v2

## Overview

This document provides a comprehensive catalog of all 36 skills used in the Feature-Implementer v2 architecture, organized by agent and phase.

## Skills Catalog

### Total Skills: 36
- **Main Agent:** 3 skills
- **Analysis Specialist:** 3 skills
- **Design Orchestrator:** 2 skills
- **Architecture Designer:** 3 skills
- **Documentation Researcher:** 2 skills
- **Dependency Manager:** 2 skills
- **Validation Orchestrator:** 2 skills
- **Unit Test Specialist:** 3 skills
- **Integration Test Specialist:** 2 skills
- **Test Runner Specialist:** 2 skills
- **Code Quality Specialist:** 3 skills
- **Security Specialist:** 3 skills
- **E2E & Accessibility Specialist:** 2 skills
- **Deployment Specialist:** 3 skills

## Skills by Agent

### Main Agent (Phase 4: Implementation)

#### 1. implementation (Auto-Activates)
**Location:** `.claude/skills/implementation/`

**Activation:** Automatically when main agent describes coding tasks

**Purpose:** Provide code style, testing patterns, and best practices during implementation

**Resources:**
- `code-style-guide.md` (826 lines): PEP 8, Google style, project conventions
- `testing-checklist.md`: Comprehensive testing requirements
- `scripts/generate_tests.py`: Test scaffolding automation

**Provides:**
- Code style guidance (PEP 8, Google-style docstrings)
- Testing patterns (pytest fixtures, mocking strategies)
- Best practices (dependency injection, error handling)
- File organization (500-line limit enforcement)
- Type hints and documentation standards

**Used During:**
- TDD implementation loop
- Code refactoring
- Documentation writing

#### 2. test-generator (On-Demand)
**Location:** `.claude/skills/test-generator/`

**Activation:** On-demand via `/generate-tests <file-path>`

**Purpose:** Generate test scaffolding for modules

**Tools:** Read, Write, Edit

**Resources:**
- `testing-templates/unit-test.py`: Unit test template
- `testing-templates/integration-test.py`: Integration test template

**Provides:**
- Test file scaffolding with proper structure
- Fixture setup (pytest, Jest)
- Mock configurations
- Coverage analysis helpers

**Used When:**
- Starting tests for new module
- Need test structure quickly
- Adding tests to existing code

#### 3. code-reviewer (On-Demand)
**Location:** `.claude/skills/code-reviewer/`

**Activation:** On-demand via `/review-code <file-path>`

**Purpose:** Review code for quality, security, and performance

**Tools:** Read, Bash, Grep

**Resources:**
- `review-checklist.md`: Comprehensive code review checklist
- `security-patterns.md`: Security best practices

**Provides:**
- Code quality feedback
- Security vulnerability detection
- Performance optimization suggestions
- Refactoring recommendations
- Style guide compliance checks

**Used When:**
- Self-review before committing
- Refactoring existing code
- Security concerns arise

---

### Analysis Specialist (Phase 1)

#### 4. requirements-extractor (Auto-Activates)
**Location:** `.claude/skills/requirements-extractor/`

**Activation:** Automatically when analyzing GitHub issues

**Purpose:** Extract requirements and acceptance criteria from issues

**Tools:** Read, Grep, Bash

**MCPs:** github-mcp

**Resources:**
- `requirements-checklist.md` (210 lines): Comprehensive requirements validation
- `extraction-patterns.md`: Common requirement patterns

**Provides:**
- Structured requirements list
- Acceptance criteria extraction
- User story identification
- Functional vs. non-functional requirements
- Success criteria definition

**Used During:**
- GitHub issue analysis
- Requirements validation
- Scope definition

#### 5. security-assessor (Auto-Activates)
**Location:** `.claude/skills/security-assessor/`

**Activation:** Automatically during requirements analysis

**Purpose:** Assess security risks and OWASP Top 10 considerations

**Tools:** Read, Grep

**Resources:**
- `security-checklist.md` (316 lines): OWASP Top 10 assessment, Python-specific security
- `threat-modeling-guide.md`: Security threat modeling

**Provides:**
- OWASP Top 10 risk assessment
- Input validation requirements
- Authentication/authorization needs
- Data security considerations
- Secure communication requirements

**Used During:**
- Initial requirements analysis
- Security risk identification
- Threat modeling

#### 6. tech-stack-evaluator (Auto-Activates)
**Location:** `.claude/skills/tech-stack-evaluator/`

**Activation:** Automatically during requirements analysis

**Purpose:** Evaluate technical stack compatibility and requirements

**Tools:** Read, Bash, Grep

**Resources:**
- `tech-stack-matrix.md`: Technology compatibility matrix
- `language-feature-map.md`: Language-specific features

**Provides:**
- Language/framework compatibility
- Library version requirements
- Technology constraints
- Performance implications
- Migration considerations

**Used During:**
- Requirements analysis
- Technology selection
- Feasibility assessment

---

### Design Orchestrator (Phase 2)

#### 7. design-synthesizer (Auto-Activates)
**Location:** `.claude/skills/design-synthesizer/`

**Activation:** Automatically when synthesizing sub-agent outputs

**Purpose:** Synthesize parallel sub-agent outputs into cohesive design

**Tools:** Read, Write, Edit

**Resources:**
- `synthesis-guide.md`: Guidelines for output synthesis
- `design-patterns.md`: Common design patterns

**Provides:**
- Output integration from multiple sub-agents
- Consistency checking across designs
- Conflict resolution
- Coherent design narrative
- Gap identification

**Used During:**
- After parallel sub-agents complete
- Design synthesis phase
- PRP generation preparation

#### 8. prp-generator (Auto-Activates)
**Location:** `.claude/skills/prp-generator/`

**Activation:** Automatically when generating PRP document

**Purpose:** Generate Product Requirements Prompt (PRP) from synthesized design

**Tools:** Write, Edit

**Resources:**
- `prp-template.md`: PRP document template
- `prp-examples.md`: Example PRPs

**Provides:**
- Structured PRP document
- Implementation plan
- Testing strategy
- Documentation requirements
- Acceptance criteria

**Used During:**
- Final design document generation
- PRP creation
- User approval preparation

---

### Architecture Designer (Phase 2, Sub-Agent)

#### 9. architecture-planner (Auto-Activates)
**Location:** `.claude/skills/architecture-planner/`

**Activation:** Automatically when planning component architecture

**Purpose:** Design component architecture and module structure

**Tools:** Read, Write, Edit

**MCPs:** sequential-thinking-mcp (ultrathink)

**Resources:**
- `architecture-patterns.md`: Common architectural patterns (layered, hexagonal, event-driven)
- `component-design-guide.md`: Component design principles

**Provides:**
- Component architecture (interfaces, core, implementations)
- Module boundaries
- Dependency relationships
- Layer separation (presentation, business, data)
- Extension points

**Used During:**
- Architecture design phase
- Component structure planning
- Module organization

#### 10. data-modeler (Auto-Activates)
**Location:** `.claude/skills/data-modeler/`

**Activation:** Automatically when designing data models

**Purpose:** Design data models with Pydantic schemas

**Tools:** Read, Write, Edit

**Resources:**
- `data-model-guide.md`: Data modeling best practices
- `pydantic-patterns.md`: Pydantic schema patterns

**Provides:**
- Pydantic schema definitions
- Data validation rules
- Type annotations
- Relationship mappings
- Serialization strategies

**Used During:**
- Data model design
- API contract definition
- Database schema planning

#### 11. api-designer (Auto-Activates)
**Location:** `.claude/skills/api-designer/`

**Activation:** Automatically when designing API contracts

**Purpose:** Design REST APIs or function contracts

**Tools:** Read, Write, Edit

**Resources:**
- `api-design-guide.md`: API design best practices (REST, GraphQL)
- `function-design-patterns.md`: Function design patterns

**Provides:**
- API endpoint definitions
- Request/response schemas
- Error handling patterns
- Authentication/authorization
- Rate limiting strategies

**Used During:**
- API contract design
- Function signature definition
- Interface specification

---

### Documentation Researcher (Phase 2, Sub-Agent)

#### 12. doc-fetcher (Auto-Activates)
**Location:** `.claude/skills/doc-fetcher/`

**Activation:** Automatically when fetching documentation

**Purpose:** Fetch library/framework documentation via context7/fetch

**Tools:** Read

**MCPs:** context7-mcp, fetch-mcp

**Resources:**
- `doc-sources.md`: Curated documentation sources
- `fetching-strategies.md`: Documentation fetching strategies

**Provides:**
- Latest library documentation
- API reference retrieval
- Code examples extraction
- Version-specific docs
- Official vs. community resources

**Used During:**
- Library research
- API exploration
- Example code discovery

#### 13. doc-analyzer (Auto-Activates)
**Location:** `.claude/skills/doc-analyzer/`

**Activation:** Automatically when analyzing fetched documentation

**Purpose:** Analyze and extract relevant patterns from documentation

**Tools:** Read, Grep

**Resources:**
- `pattern-extraction-guide.md`: Pattern extraction techniques
- `best-practices-catalog.md`: Common best practices

**Provides:**
- Relevant code patterns
- Best practice identification
- API usage examples
- Common pitfalls
- Performance considerations

**Used During:**
- Documentation analysis
- Pattern extraction
- Best practice identification

---

### Dependency Manager (Phase 2, Sub-Agent)

#### 14. dependency-analyzer (Auto-Activates)
**Location:** `.claude/skills/dependency-analyzer/`

**Activation:** Automatically when analyzing dependencies

**Purpose:** Analyze project dependencies and compatibility

**Tools:** Read, Bash, Grep

**Resources:**
- `dependency-checker-script.py`: Automated dependency analysis
- `compatibility-matrix.md`: Dependency compatibility

**Provides:**
- Current dependency analysis
- New dependency identification
- Version compatibility checks
- Dependency tree visualization
- Conflict detection

**Used During:**
- Dependency planning
- Version selection
- Compatibility verification

#### 15. version-checker (Auto-Activates)
**Location:** `.claude/skills/version-checker/`

**Activation:** Automatically when checking version compatibility

**Purpose:** Check version compatibility and security vulnerabilities

**Tools:** Read, Bash

**Resources:**
- `version-matrix.md`: Version compatibility matrix
- `security-advisory-db.md`: Security vulnerability database

**Provides:**
- Version compatibility verification
- Breaking change detection
- Security vulnerability scanning
- Upgrade path recommendations
- Deprecation warnings

**Used During:**
- Dependency version selection
- Security assessment
- Upgrade planning

---

### Validation Orchestrator (Phase 5)

#### 16. validation-coordinator (Auto-Activates)
**Location:** `.claude/skills/validation-coordinator/`

**Activation:** Automatically when coordinating validation workflow

**Purpose:** Coordinate sequential validation specialists

**Tools:** Read, Bash

**Resources:**
- `validation-workflow.md`: Validation workflow orchestration
- `validation-checklist.md`: Comprehensive validation checklist

**Provides:**
- Validation sequence management
- Specialist invocation order
- Dependency handling
- Failure tracking
- Overall validation status

**Used During:**
- Validation orchestration
- Specialist coordination
- Workflow management

#### 17. recursive-communicator (Auto-Activates)
**Location:** `.claude/skills/recursive-communicator/`

**Activation:** Automatically when managing agent-to-agent communication

**Purpose:** Manage recursive communication between validation specialists and main agent

**Tools:** Read, Write

**Resources:**
- `communication-protocol.md`: Agent communication patterns
- `message-templates.md`: Communication message templates

**Provides:**
- Failure communication to main agent
- Fix verification
- Re-validation triggers
- Communication logging
- Deadlock prevention

**Used During:**
- Validation failures
- Main agent fixes
- Re-validation cycles

---

### Unit Test Specialist (Phase 5)

#### 18. unit-test-writer (Auto-Activates)
**Location:** `.claude/skills/unit-test-writer/`

**Activation:** Automatically when writing unit tests

**Purpose:** Write unit tests for implementation

**Tools:** Read, Write, Edit

**Resources:**
- `unit-test-templates/`: Language-specific templates
- `testing-best-practices.md`: Unit testing best practices

**Provides:**
- Unit test generation
- Test case identification
- Assertion strategies
- Edge case coverage
- Test naming conventions

**Used During:**
- Unit test creation
- Test coverage expansion
- Regression test writing

#### 19. pytest-generator (Auto-Activates, Python)
**Location:** `.claude/skills/pytest-generator/`

**Activation:** Automatically for Python projects

**Purpose:** Generate pytest tests with fixtures and mocking

**Tools:** Read, Write, Edit

**Resources:**
- `pytest-patterns.md`: Pytest patterns and best practices
- `pytest-fixtures.md`: Common pytest fixtures

**Provides:**
- Pytest test structure
- Fixture definitions
- Mock/patch configurations
- Parametrized tests
- Pytest plugins usage

**Used During:**
- Python unit test generation
- Fixture creation
- Mock setup

#### 20. jest-generator (Auto-Activates, TypeScript)
**Location:** `.claude/skills/jest-generator/`

**Activation:** Automatically for TypeScript/JavaScript projects

**Purpose:** Generate Jest tests with mocking

**Tools:** Read, Write, Edit

**Resources:**
- `jest-patterns.md`: Jest patterns and best practices
- `jest-mocks.md`: Jest mocking strategies

**Provides:**
- Jest test structure
- Mock implementations
- Spy configurations
- Snapshot testing
- Jest matchers usage

**Used During:**
- TypeScript/JavaScript unit test generation
- Mock creation
- Snapshot testing

---

### Integration Test Specialist (Phase 5)

#### 21. integration-test-writer (Auto-Activates)
**Location:** `.claude/skills/integration-test-writer/`

**Activation:** Automatically when writing integration tests

**Purpose:** Write integration tests for APIs and services

**Tools:** Read, Write, Edit

**Resources:**
- `integration-test-templates/`: Integration test templates
- `integration-patterns.md`: Integration testing patterns

**Provides:**
- Integration test generation
- Service interaction tests
- Database integration tests
- External API tests
- End-to-end workflows

**Used During:**
- Integration test creation
- Service testing
- Workflow validation

#### 22. api-test-generator (Auto-Activates)
**Location:** `.claude/skills/api-test-generator/`

**Activation:** Automatically when testing APIs

**Purpose:** Generate API tests (REST, GraphQL)

**Tools:** Read, Write, Edit

**Resources:**
- `api-test-patterns.md`: API testing patterns
- `http-client-examples.md`: HTTP client examples (requests, httpx, fetch)

**Provides:**
- API endpoint tests
- Request/response validation
- Authentication testing
- Error handling tests
- Rate limiting tests

**Used During:**
- API integration testing
- Endpoint validation
- Contract testing

---

### Test Runner Specialist (Phase 5)

#### 23. test-executor (Auto-Activates)
**Location:** `.claude/skills/test-executor/`

**Activation:** Automatically when executing tests

**Purpose:** Execute all tests (unit + integration)

**Tools:** Bash, Read

**Resources:**
- `test-execution-script.py`: Automated test runner
- `test-reporting.md`: Test reporting formats

**Provides:**
- Test execution
- Parallel test running
- Failure reporting
- Test suite management
- Execution time tracking

**Used During:**
- Test execution phase
- CI/CD integration
- Local validation

#### 24. coverage-analyzer (Auto-Activates)
**Location:** `.claude/skills/coverage-analyzer/`

**Activation:** Automatically when analyzing test coverage

**Purpose:** Analyze test coverage and verify ≥ 80% threshold

**Tools:** Bash, Read

**Resources:**
- `coverage-config.md`: Coverage configuration
- `coverage-reporting.md`: Coverage report formats

**Provides:**
- Coverage percentage calculation
- Uncovered line identification
- Coverage report generation
- Threshold verification
- Coverage trends

**Used During:**
- Test coverage analysis
- Quality gate verification
- Coverage improvement

---

### Code Quality Specialist (Phase 5)

#### 25. python-quality-checker (Auto-Activates, Python)
**Location:** `.claude/skills/python-quality-checker/`

**Activation:** Automatically for Python projects

**Purpose:** Run Black, mypy, flake8 for Python code

**Tools:** Bash, Read

**Resources:**
- `python-quality-config/`: Black, mypy, flake8 configs
- `python-standards.md`: Python coding standards

**Provides:**
- Code formatting (Black)
- Type checking (mypy)
- Linting (flake8)
- Import sorting (isort)
- Complexity checking

**Used During:**
- Python code quality validation
- Pre-commit checks
- CI/CD quality gates

#### 26. typescript-quality-checker (Auto-Activates, TypeScript)
**Location:** `.claude/skills/typescript-quality-checker/`

**Activation:** Automatically for TypeScript/JavaScript projects

**Purpose:** Run ESLint, Prettier, tsc for TypeScript code

**Tools:** Bash, Read

**Resources:**
- `typescript-quality-config/`: ESLint, Prettier, tsc configs
- `typescript-standards.md`: TypeScript coding standards

**Provides:**
- Code formatting (Prettier)
- Type checking (tsc)
- Linting (ESLint)
- Import organization
- Code complexity checking

**Used During:**
- TypeScript code quality validation
- Pre-commit checks
- CI/CD quality gates

#### 27. rust-quality-checker (Auto-Activates, Rust)
**Location:** `.claude/skills/rust-quality-checker/`

**Activation:** Automatically for Rust projects

**Purpose:** Run rustfmt, clippy for Rust code

**Tools:** Bash, Read

**Resources:**
- `rust-quality-config/`: rustfmt, clippy configs
- `rust-standards.md`: Rust coding standards

**Provides:**
- Code formatting (rustfmt)
- Linting (clippy)
- Idiomatic Rust checking
- Performance suggestions
- Safety checks

**Used During:**
- Rust code quality validation
- Pre-commit checks
- CI/CD quality gates

---

### Security Specialist (Phase 5)

#### 28. security-scanner (Auto-Activates)
**Location:** `.claude/skills/security-scanner/`

**Activation:** Automatically when scanning for vulnerabilities

**Purpose:** Scan code for security vulnerabilities

**Tools:** Bash, Read

**Resources:**
- `security-scanner-script.py`: Automated security scanner
- `vulnerability-patterns.md`: Common vulnerability patterns

**Provides:**
- Static code analysis
- Dependency vulnerability scanning
- Secret detection
- SQL injection detection
- XSS vulnerability detection

**Used During:**
- Security assessment
- Vulnerability scanning
- Pre-deployment checks

#### 29. vulnerability-assessor (Auto-Activates)
**Location:** `.claude/skills/vulnerability-assessor/`

**Activation:** Automatically when assessing vulnerabilities

**Purpose:** Assess vulnerability severity and impact

**Tools:** Read, Bash

**Resources:**
- `vulnerability-database.md`: Known vulnerability database
- `cvss-scoring.md`: CVSS scoring guidelines

**Provides:**
- Vulnerability severity assessment
- Impact analysis
- Remediation recommendations
- CVE identification
- Risk prioritization

**Used During:**
- Vulnerability assessment
- Risk analysis
- Remediation planning

#### 30. owasp-checker (Auto-Activates)
**Location:** `.claude/skills/owasp-checker/`

**Activation:** Automatically when checking OWASP Top 10

**Purpose:** Verify OWASP Top 10 compliance

**Tools:** Read, Bash

**Resources:**
- `owasp-checklist.md`: OWASP Top 10 checklist
- `owasp-patterns.md`: OWASP vulnerability patterns

**Provides:**
- OWASP Top 10 verification
- Injection protection
- Authentication/authorization checks
- Sensitive data exposure
- Security misconfiguration detection

**Used During:**
- Security compliance verification
- OWASP Top 10 assessment
- Security audit

---

### E2E & Accessibility Specialist (Phase 5, Frontend)

#### 31. e2e-test-writer (Auto-Activates)
**Location:** `.claude/skills/e2e-test-writer/`

**Activation:** Automatically when writing E2E tests

**Purpose:** Write E2E tests with Playwright

**Tools:** Read, Write, Bash

**MCPs:** playwright-mcp

**Resources:**
- `e2e-test-templates/`: Playwright test templates
- `e2e-patterns.md`: E2E testing patterns

**Provides:**
- Playwright test generation
- User flow tests
- Page object patterns
- Test data management
- Screenshot/video capture

**Used During:**
- E2E test creation
- User flow validation
- Frontend integration testing

#### 32. accessibility-checker (Auto-Activates)
**Location:** `.claude/skills/accessibility-checker/`

**Activation:** Automatically when checking accessibility

**Purpose:** Verify WCAG compliance and accessibility features

**Tools:** Read, Bash

**MCPs:** playwright-mcp

**Resources:**
- `accessibility-checklist.md`: WCAG compliance checklist
- `aria-patterns.md`: ARIA attribute patterns

**Provides:**
- WCAG compliance verification
- Keyboard navigation testing
- Screen reader support
- Color contrast checking
- Focus management validation

**Used During:**
- Accessibility testing
- WCAG compliance verification
- Frontend validation

---

### Deployment Specialist (Phase 6)

#### 33. documentation-updater (Auto-Activates)
**Location:** `.claude/skills/documentation-updater/`

**Activation:** Automatically when updating documentation

**Purpose:** Update all project documentation

**Tools:** Read, Write, Edit

**Resources:**
- `doc-update-guide.md`: Documentation update guidelines
- `doc-templates/`: Documentation templates

**Provides:**
- Implementation documentation
- API documentation
- User guides
- Architecture documentation
- Migration guides

**Used During:**
- Documentation update phase
- API doc generation
- User guide creation

#### 34. changelog-generator (Auto-Activates)
**Location:** `.claude/skills/changelog-generator/`

**Activation:** Automatically when generating CHANGELOG entries

**Purpose:** Generate CHANGELOG.md entries

**Tools:** Read, Write, Edit

**Resources:**
- `changelog-template.md`: CHANGELOG entry template
- `conventional-commits.md`: Conventional commits guide

**Provides:**
- Conventional commit format
- CHANGELOG entry generation
- Version management
- Breaking change documentation
- Migration notes

**Used During:**
- CHANGELOG update
- Release preparation
- Version documentation

#### 35. pr-creator (Auto-Activates)
**Location:** `.claude/skills/pr-creator/`

**Activation:** Automatically when creating PRs

**Purpose:** Create GitHub pull requests

**Tools:** gh, git

**MCPs:** github-mcp

**Resources:**
- `pr-template.md`: Pull request template
- `pr-best-practices.md`: PR creation best practices

**Provides:**
- PR title generation
- PR description generation
- Reviewer assignment
- Label assignment
- Milestone linking

**Used During:**
- Pull request creation
- Code review initiation
- Deployment preparation

---

## Skills by Phase

### Phase 1: Requirements Analysis
- requirements-extractor (Analysis Specialist)
- security-assessor (Analysis Specialist)
- tech-stack-evaluator (Analysis Specialist)

### Phase 2: Design & Planning
- design-synthesizer (Design Orchestrator)
- prp-generator (Design Orchestrator)
- architecture-planner (Architecture Designer)
- data-modeler (Architecture Designer)
- api-designer (Architecture Designer)
- doc-fetcher (Documentation Researcher)
- doc-analyzer (Documentation Researcher)
- dependency-analyzer (Dependency Manager)
- version-checker (Dependency Manager)

### Phase 3: User Approval
- No skills (user interaction)

### Phase 4: Implementation
- implementation (Main Agent, auto)
- test-generator (Main Agent, on-demand)
- code-reviewer (Main Agent, on-demand)

### Phase 5: Validation
- validation-coordinator (Validation Orchestrator)
- recursive-communicator (Validation Orchestrator)
- unit-test-writer (Unit Test Specialist)
- pytest-generator (Unit Test Specialist, Python)
- jest-generator (Unit Test Specialist, TypeScript)
- integration-test-writer (Integration Test Specialist)
- api-test-generator (Integration Test Specialist)
- test-executor (Test Runner Specialist)
- coverage-analyzer (Test Runner Specialist)
- python-quality-checker (Code Quality Specialist, Python)
- typescript-quality-checker (Code Quality Specialist, TypeScript)
- rust-quality-checker (Code Quality Specialist, Rust)
- security-scanner (Security Specialist)
- vulnerability-assessor (Security Specialist)
- owasp-checker (Security Specialist)
- e2e-test-writer (E2E & Accessibility Specialist, Frontend)
- accessibility-checker (E2E & Accessibility Specialist, Frontend)

### Phase 6: Deployment
- documentation-updater (Deployment Specialist)
- changelog-generator (Deployment Specialist)
- pr-creator (Deployment Specialist)

## Skills by Activation Type

### Auto-Activating Skills (33)
All skills except:
- test-generator (on-demand)
- code-reviewer (on-demand)

### On-Demand Skills (2)
- test-generator
- code-reviewer

### Language-Specific Skills (5)
- pytest-generator (Python)
- jest-generator (TypeScript)
- python-quality-checker (Python)
- typescript-quality-checker (TypeScript)
- rust-quality-checker (Rust)

## Skills by Tool Usage

### Read-Only Skills (8)
- security-assessor
- tech-stack-evaluator
- doc-fetcher
- doc-analyzer
- code-reviewer
- vulnerability-assessor
- owasp-checker
- accessibility-checker

### Write-Capable Skills (15)
- implementation
- test-generator
- design-synthesizer
- prp-generator
- architecture-planner
- data-modeler
- api-designer
- recursive-communicator
- unit-test-writer
- pytest-generator
- jest-generator
- integration-test-writer
- api-test-generator
- documentation-updater
- changelog-generator

### Bash-Capable Skills (13)
- requirements-extractor
- tech-stack-evaluator
- dependency-analyzer
- version-checker
- validation-coordinator
- test-executor
- coverage-analyzer
- python-quality-checker
- typescript-quality-checker
- rust-quality-checker
- security-scanner
- vulnerability-assessor
- e2e-test-writer

## Skill Directory Structure

```
.claude/skills/
├── implementation/
│   ├── SKILL.md
│   ├── code-style-guide.md
│   ├── testing-checklist.md
│   └── scripts/generate_tests.py
├── test-generator/
│   ├── SKILL.md
│   └── testing-templates/
│       ├── unit-test.py
│       └── integration-test.py
├── code-reviewer/
│   ├── SKILL.md
│   ├── review-checklist.md
│   └── security-patterns.md
├── requirements-extractor/
│   ├── SKILL.md
│   ├── requirements-checklist.md
│   └── extraction-patterns.md
├── security-assessor/
│   ├── SKILL.md
│   ├── security-checklist.md
│   └── threat-modeling-guide.md
├── tech-stack-evaluator/
│   ├── SKILL.md
│   ├── tech-stack-matrix.md
│   └── language-feature-map.md
├── design-synthesizer/
│   ├── SKILL.md
│   ├── synthesis-guide.md
│   └── design-patterns.md
├── prp-generator/
│   ├── SKILL.md
│   ├── prp-template.md
│   └── prp-examples.md
├── architecture-planner/
│   ├── SKILL.md
│   ├── architecture-patterns.md
│   └── component-design-guide.md
├── data-modeler/
│   ├── SKILL.md
│   ├── data-model-guide.md
│   └── pydantic-patterns.md
├── api-designer/
│   ├── SKILL.md
│   ├── api-design-guide.md
│   └── function-design-patterns.md
├── doc-fetcher/
│   ├── SKILL.md
│   ├── doc-sources.md
│   └── fetching-strategies.md
├── doc-analyzer/
│   ├── SKILL.md
│   ├── pattern-extraction-guide.md
│   └── best-practices-catalog.md
├── dependency-analyzer/
│   ├── SKILL.md
│   ├── dependency-checker-script.py
│   └── compatibility-matrix.md
├── version-checker/
│   ├── SKILL.md
│   ├── version-matrix.md
│   └── security-advisory-db.md
├── validation-coordinator/
│   ├── SKILL.md
│   ├── validation-workflow.md
│   └── validation-checklist.md
├── recursive-communicator/
│   ├── SKILL.md
│   ├── communication-protocol.md
│   └── message-templates.md
├── unit-test-writer/
│   ├── SKILL.md
│   ├── unit-test-templates/
│   └── testing-best-practices.md
├── pytest-generator/
│   ├── SKILL.md
│   ├── pytest-patterns.md
│   └── pytest-fixtures.md
├── jest-generator/
│   ├── SKILL.md
│   ├── jest-patterns.md
│   └── jest-mocks.md
├── integration-test-writer/
│   ├── SKILL.md
│   ├── integration-test-templates/
│   └── integration-patterns.md
├── api-test-generator/
│   ├── SKILL.md
│   ├── api-test-patterns.md
│   └── http-client-examples.md
├── test-executor/
│   ├── SKILL.md
│   ├── test-execution-script.py
│   └── test-reporting.md
├── coverage-analyzer/
│   ├── SKILL.md
│   ├── coverage-config.md
│   └── coverage-reporting.md
├── python-quality-checker/
│   ├── SKILL.md
│   ├── python-quality-config/
│   └── python-standards.md
├── typescript-quality-checker/
│   ├── SKILL.md
│   ├── typescript-quality-config/
│   └── typescript-standards.md
├── rust-quality-checker/
│   ├── SKILL.md
│   ├── rust-quality-config/
│   └── rust-standards.md
├── security-scanner/
│   ├── SKILL.md
│   ├── security-scanner-script.py
│   └── vulnerability-patterns.md
├── vulnerability-assessor/
│   ├── SKILL.md
│   ├── vulnerability-database.md
│   └── cvss-scoring.md
├── owasp-checker/
│   ├── SKILL.md
│   ├── owasp-checklist.md
│   └── owasp-patterns.md
├── e2e-test-writer/
│   ├── SKILL.md
│   ├── e2e-test-templates/
│   └── e2e-patterns.md
├── accessibility-checker/
│   ├── SKILL.md
│   ├── accessibility-checklist.md
│   └── aria-patterns.md
├── documentation-updater/
│   ├── SKILL.md
│   ├── doc-update-guide.md
│   └── doc-templates/
├── changelog-generator/
│   ├── SKILL.md
│   ├── changelog-template.md
│   └── conventional-commits.md
└── pr-creator/
    ├── SKILL.md
    ├── pr-template.md
    └── pr-best-practices.md
```

## Skill Development Guidelines

### Creating New Skills

1. **Skill Definition (SKILL.md)**
   - Clear purpose statement
   - Activation criteria
   - Tool requirements
   - MCP requirements
   - Resource list

2. **Supporting Resources**
   - Checklists for validation
   - Templates for generation
   - Scripts for automation
   - Guides for best practices

3. **Testing**
   - Skill activation tests
   - Resource availability tests
   - Integration with agent tests

### Skill Naming Conventions

- Use descriptive, action-oriented names
- Suffix specialist skills with their domain (e.g., `-writer`, `-checker`, `-generator`)
- Use consistent terminology across related skills

### Skill Documentation

Each skill must include:
- Purpose and activation criteria
- Required tools and MCPs
- Supporting resource list
- Usage examples
- Integration with agents

## Conclusion

The 36 skills in the Feature-Implementer v2 architecture provide comprehensive coverage across all phases of feature implementation, from requirements analysis to deployment. Skills are designed to:

- **Auto-activate** based on task descriptions (33 skills)
- **Provide guidance** rather than execute (except when explicitly creating artifacts)
- **Support multiple languages** (Python, TypeScript, Rust)
- **Enable recursive workflows** (validation fixes)
- **Maintain quality standards** (security, testing, documentation)

This skill catalog ensures that the main agent and all sub-agents have the domain expertise needed to deliver high-quality feature implementations.

---

**Version:** 2.0.0
**Status:** Design Complete
**Next Steps:** Skill implementation via GitHub issues
**Branch:** feature/implementer-v2
