# Feature-Implementer v2 Architecture

## Overview

The Feature-Implementer v2 is a comprehensive system for implementing features from GitHub issues using a main agent orchestration pattern with specialized sub-agents. The architecture ensures that the **main Claude Code agent maintains full control** over implementation while delegating analysis, design, and validation to specialized agents.

## Core Principles

### 1. Main Agent Control
- **Main agent does ALL coding, testing, and committing**
- Sub-agents provide analysis, design, and validation
- Main agent maintains visibility and control throughout

### 2. Separation of Concerns
- **Think vs. Do:** Sub-agents think (analyze, design, validate), main agent does (implements)
- Clear phase boundaries with explicit checkpoints
- Recursive communication for validation fixes

### 3. Quality-First
- Security-by-design (OWASP Top 10)
- Test-Driven Development (TDD)
- 80%+ test coverage requirement
- Automated quality gates

### 4. Documentation-Driven
- Every phase produces documentation
- Traceable decision-making
- Comprehensive audit trail

## Architecture Layers

### Layer 1: User Interface
```
/feature-implement <issue-number> [create-branch:true|false]
```

**Slash Command:**
- Entry point for users
- Simple, intuitive syntax
- Optional branch creation flag

### Layer 2: Main Orchestrator
```
@feature-implementer-main (prompt)
```

**Main Agent Prompt:**
- Stored in `.claude/prompts/feature-implementer-main.md`
- Invoked via `@feature-implementer-main`
- Orchestrates entire workflow
- Executes implementation phase
- Controls deployment

### Layer 3: Specialist Agents

#### Phase 1: Analysis
```
@analysis-specialist
```
- **Model:** Haiku (fast, cost-effective)
- **Purpose:** Analyze GitHub issues for requirements, security, feasibility
- **Output:** `/docs/implementation/analysis/feature-{issue-number}-analysis.md`
- **Skills:** requirements-extractor, security-assessor, tech-stack-evaluator

#### Phase 2: Design
```
@design-orchestrator
  ├── @architecture-designer (parallel)
  ├── @documentation-researcher (parallel)
  └── @dependency-manager (parallel)
```

**Design Orchestrator:**
- **Model:** Sonnet (balanced reasoning)
- **Purpose:** Coordinate parallel design activities
- **Output:** `/docs/implementation/prp/feature-{issue-number}-prp.md` (Product Requirements Prompt)
- **Skills:** design-synthesizer, prp-generator

**Sub-Agents (Parallel Execution):**

1. **Architecture Designer**
   - **Model:** Opus (deep reasoning)
   - **MCP:** sequential-thinking (ultrathink mode)
   - **Purpose:** Design component architecture, data models, APIs
   - **Skills:** architecture-planner, data-modeler, api-designer

2. **Documentation Researcher**
   - **Model:** Haiku
   - **MCPs:** context7, fetch
   - **Purpose:** Fetch and analyze library documentation
   - **Skills:** doc-fetcher, doc-analyzer

3. **Dependency Manager**
   - **Model:** Haiku
   - **Purpose:** Analyze dependencies and version compatibility
   - **Skills:** dependency-analyzer, version-checker

#### Phase 3: User Approval Checkpoint
```
⚠️ STOP and WAIT for user approval
```
- Main agent presents PRP to user
- Explicit approval required before implementation
- User can request changes or approve

#### Phase 4: Implementation
```
Main Agent Implements (TDD)
```
- **Executor:** Main Claude Code agent
- **Method:** Test-Driven Development (RED → GREEN → REFACTOR)
- **Skills:** implementation (auto), test-generator (on-demand), code-reviewer (on-demand)
- **Standards:** 500-line limit, type hints, docstrings, single responsibility

#### Phase 5: Validation
```
@validation-orchestrator
  ├── @unit-test-specialist
  ├── @integration-test-specialist
  ├── @test-runner-specialist
  ├── @code-quality-specialist
  ├── @security-specialist
  └── @e2e-accessibility-specialist (if frontend)
```

**Validation Orchestrator:**
- **Model:** Sonnet
- **Purpose:** Coordinate validation specialists with recursive communication
- **Skills:** validation-coordinator, recursive-communicator

**Validation Specialists (Sequential with Recursive Communication):**

1. **Unit Test Specialist**
   - **Model:** Haiku
   - **Purpose:** Write unit tests (`main-file-name.test.py`)
   - **Skills:** unit-test-writer, pytest-generator, jest-generator

2. **Integration Test Specialist**
   - **Model:** Haiku
   - **Purpose:** Write integration tests for APIs and services
   - **Skills:** integration-test-writer, api-test-generator

3. **Test Runner Specialist**
   - **Model:** Haiku
   - **Purpose:** Execute tests, verify coverage ≥ 80%
   - **Output:** `/docs/implementation/tests/feature-{issue-number}-tests.md`
   - **Skills:** test-executor, coverage-analyzer

4. **Code Quality Specialist**
   - **Model:** Haiku
   - **Purpose:** Run language-specific quality checks
   - **Output:** No documentation (automated)
   - **Skills:** python-quality-checker, typescript-quality-checker, rust-quality-checker

5. **Security Specialist**
   - **Model:** Sonnet
   - **Purpose:** Security assessment and OWASP Top 10 verification
   - **Output:** `/docs/implementation/security/feature-{issue-number}-security.md`
   - **Skills:** security-scanner, vulnerability-assessor, owasp-checker

6. **E2E & Accessibility Specialist** (Frontend Only)
   - **Model:** Haiku
   - **MCP:** playwright
   - **Purpose:** E2E testing and accessibility verification
   - **Output:** `/docs/implementation/e2e/feature-{issue-number}-e2e.md`
   - **Skills:** e2e-test-writer, accessibility-checker

#### Phase 6: Deployment
```
@deployment-specialist
```
- **Model:** Haiku
- **Purpose:** Finalize deployment, documentation, PR creation
- **Skills:** documentation-updater, changelog-generator, pr-creator

## Workflow Phases

### Phase 1: Requirements Analysis

```mermaid
graph TD
    A[User: /feature-implement 123] --> B[@feature-implementer-main]
    B --> C[@analysis-specialist]
    C --> D[Fetch GitHub issue]
    D --> E[Extract requirements]
    E --> F[Assess security risks]
    F --> G[Evaluate tech stack]
    G --> H[Output: analysis.md]
    H --> B
```

**Inputs:**
- GitHub issue number

**Outputs:**
- `/docs/implementation/analysis/feature-{issue-number}-analysis.md`

**Content:**
- Requirements and acceptance criteria
- Security considerations (OWASP Top 10)
- Technical stack requirements
- Dependencies needed
- Scope boundaries
- Identified risks

### Phase 2: Design & Planning

```mermaid
graph TD
    A[@feature-implementer-main] --> B[@design-orchestrator]
    B --> C[@architecture-designer]
    B --> D[@documentation-researcher]
    B --> E[@dependency-manager]
    C --> F[Component architecture]
    D --> G[Library documentation]
    E --> H[Dependency analysis]
    F --> I[Synthesize outputs]
    G --> I
    H --> I
    I --> J[Generate PRP]
    J --> K[Output: prp.md]
    K --> A
```

**Parallel Execution:**
- Architecture design with ultrathink
- Documentation research with context7/fetch
- Dependency analysis

**Outputs:**
- `/docs/implementation/prp/feature-{issue-number}-prp.md` (Product Requirements Prompt)

**Content:**
- Component architecture
- Data models (Pydantic schemas)
- API contracts
- Data flow diagrams
- Error handling strategy
- Library documentation and examples
- Dependencies and versions
- Implementation plan
- Testing strategy

### Phase 3: User Approval Checkpoint

```mermaid
graph TD
    A[@feature-implementer-main] --> B[Present PRP to user]
    B --> C{User approves?}
    C -->|Yes| D[Proceed to implementation]
    C -->|No| E[Request changes]
    E --> F[Update design]
    F --> B
```

**Critical Checkpoint:**
- Main agent presents PRP summary
- User explicitly approves or requests changes
- **NO IMPLEMENTATION without approval**

### Phase 4: Implementation

```mermaid
graph TD
    A[@feature-implementer-main] --> B[Create feature branch]
    B --> C[TDD Cycle]
    C --> D[Write failing test RED]
    D --> E[Implement minimal code GREEN]
    E --> F[Refactor REFACTOR]
    F --> G{More components?}
    G -->|Yes| C
    G -->|No| H[Implementation complete]
```

**Executor:** Main Claude Code agent

**Method:** Test-Driven Development
1. **RED:** Write failing test
2. **GREEN:** Implement minimal code to pass
3. **REFACTOR:** Improve code quality

**Skills (Main Agent):**
- **implementation** (auto-activates): Provides style, testing, patterns
- **test-generator** (on-demand): Scaffolds tests
- **code-reviewer** (on-demand): Self-review feedback

**Standards:**
- 500-line file limit
- Type hints for all functions
- Google-style docstrings
- Single responsibility principle
- Dependency injection for testability

### Phase 5: Validation

```mermaid
graph TD
    A[@feature-implementer-main] --> B[@validation-orchestrator]
    B --> C[@unit-test-specialist]
    C --> D{Tests pass?}
    D -->|No| E[Communicate with main agent]
    E --> F[Main agent fixes]
    F --> C
    D -->|Yes| G[@integration-test-specialist]
    G --> H[@test-runner-specialist]
    H --> I{Coverage ≥ 80%?}
    I -->|No| E
    I -->|Yes| J[@code-quality-specialist]
    J --> K{Quality checks pass?}
    K -->|No| E
    K -->|Yes| L[@security-specialist]
    L --> M{Security OK?}
    M -->|No| E
    M -->|Yes| N{Frontend?}
    N -->|Yes| O[@e2e-accessibility-specialist]
    N -->|No| P[Validation complete]
    O --> P
```

**Recursive Communication:**
- Validation specialists communicate failures to main agent
- Main agent fixes issues
- Specialists re-validate
- Loop continues until all validations pass

**Validation Sequence:**
1. Unit tests written and executed
2. Integration tests written and executed
3. Test coverage verified (≥ 80%)
4. Code quality checks (Black, mypy, flake8, ESLint, etc.)
5. Security assessment (OWASP Top 10)
6. E2E and accessibility tests (if frontend)

**Outputs:**
- `/docs/implementation/tests/feature-{issue-number}-tests.md`
- `/docs/implementation/security/feature-{issue-number}-security.md`
- `/docs/implementation/e2e/feature-{issue-number}-e2e.md` (if frontend)

### Phase 6: Deployment

```mermaid
graph TD
    A[@feature-implementer-main] --> B[@deployment-specialist]
    B --> C[Update CHANGELOG.md]
    C --> D[Update documentation]
    D --> E[Update TASK.md]
    E --> F[Pre-commit hook]
    F --> G{Hook passes?}
    G -->|No| H[Fix issues]
    H --> F
    G -->|Yes| I[Commit changes]
    I --> J[Push to remote]
    J --> K[Create PR]
    K --> L[Update GitHub issue]
    L --> M[Deployment complete]
```

**Deployment Steps:**
1. Update CHANGELOG.md with feature details
2. Update documentation (implementation docs, API docs, user guides)
3. Update TASK.md with completion
4. Run pre-commit hook (automated quality checks)
5. Commit: `git commit -m "feat: implement feature from issue #{issue-number}"`
6. Push: `git push origin feature/{issue-number}`
7. Create PR: `gh pr create --title "Feature: {title}" --body "{description}"`
8. Update GitHub issue with PR link

## Directory Structure

### Configuration Structure
```
.claude/
├── commands/
│   └── feature-implement.md          # Slash command
│
├── prompts/
│   └── feature-implementer-main.md   # Main orchestrator prompt
│
├── agents/
│   ├── analysis-specialist.md
│   ├── design-orchestrator.md
│   ├── architecture-designer.md
│   ├── documentation-researcher.md
│   ├── dependency-manager.md
│   ├── validation-orchestrator.md
│   ├── unit-test-specialist.md
│   ├── integration-test-specialist.md
│   ├── test-runner-specialist.md
│   ├── code-quality-specialist.md
│   ├── security-specialist.md
│   ├── e2e-accessibility-specialist.md
│   └── deployment-specialist.md
│
├── skills/
│   ├── implementation/                # Main agent
│   ├── test-generator/                # Main agent
│   ├── code-reviewer/                 # Main agent
│   ├── requirements-extractor/        # Analysis specialist
│   ├── security-assessor/             # Analysis specialist
│   ├── tech-stack-evaluator/          # Analysis specialist
│   ├── design-synthesizer/            # Design orchestrator
│   ├── prp-generator/                 # Design orchestrator
│   ├── architecture-planner/          # Architecture designer
│   ├── data-modeler/                  # Architecture designer
│   ├── api-designer/                  # Architecture designer
│   ├── doc-fetcher/                   # Documentation researcher
│   ├── doc-analyzer/                  # Documentation researcher
│   ├── dependency-analyzer/           # Dependency manager
│   ├── version-checker/               # Dependency manager
│   ├── validation-coordinator/        # Validation orchestrator
│   ├── recursive-communicator/        # Validation orchestrator
│   ├── unit-test-writer/              # Unit test specialist
│   ├── pytest-generator/              # Unit test specialist
│   ├── jest-generator/                # Unit test specialist
│   ├── integration-test-writer/       # Integration test specialist
│   ├── api-test-generator/            # Integration test specialist
│   ├── test-executor/                 # Test runner specialist
│   ├── coverage-analyzer/             # Test runner specialist
│   ├── python-quality-checker/        # Code quality specialist
│   ├── typescript-quality-checker/    # Code quality specialist
│   ├── rust-quality-checker/          # Code quality specialist
│   ├── security-scanner/              # Security specialist
│   ├── vulnerability-assessor/        # Security specialist
│   ├── owasp-checker/                 # Security specialist
│   ├── e2e-test-writer/               # E2E specialist
│   ├── accessibility-checker/         # E2E specialist
│   ├── documentation-updater/         # Deployment specialist
│   ├── changelog-generator/           # Deployment specialist
│   └── pr-creator/                    # Deployment specialist
│
└── hooks/
    ├── pre-commit.json                # Quality checks before commit
    └── post-implementation.json       # Validation trigger
```

### Documentation Structure
```
docs/implementation/
├── analysis/
│   └── feature-{issue-number}-analysis.md
├── prp/
│   └── feature-{issue-number}-prp.md
├── tests/
│   └── feature-{issue-number}-tests.md
├── security/
│   └── feature-{issue-number}-security.md
└── e2e/
    └── feature-{issue-number}-e2e.md
```

## Agent Specifications

### Total Agents: 13

1. **Main Orchestrator:** feature-implementer-main (prompt)
2. **Analysis Layer:** analysis-specialist
3. **Design Layer:** design-orchestrator + 3 sub-agents
4. **Validation Layer:** validation-orchestrator + 6 specialists
5. **Deployment Layer:** deployment-specialist

### Model Selection Strategy

| Agent | Model | Rationale |
|-------|-------|-----------|
| Main Orchestrator | Sonnet | Balanced reasoning for orchestration |
| Analysis Specialist | Haiku | Fast analysis, cost-effective |
| Design Orchestrator | Sonnet | Balanced design coordination |
| Architecture Designer | Opus | Deep reasoning for architecture |
| Documentation Researcher | Haiku | Fast documentation fetching |
| Dependency Manager | Haiku | Fast dependency analysis |
| Validation Orchestrator | Sonnet | Balanced validation coordination |
| Unit Test Specialist | Haiku | Fast test generation |
| Integration Test Specialist | Haiku | Fast test generation |
| Test Runner Specialist | Haiku | Fast test execution |
| Code Quality Specialist | Haiku | Fast quality checks |
| Security Specialist | Sonnet | Balanced security assessment |
| E2E & Accessibility | Haiku | Fast E2E testing |
| Deployment Specialist | Haiku | Fast deployment tasks |

## Skills Catalog

### Total Skills: 36

#### Main Agent Skills (3)
1. **implementation** (auto) - Code style, testing patterns, best practices
2. **test-generator** (on-demand) - Test scaffolding
3. **code-reviewer** (on-demand) - Code review feedback

#### Analysis Specialist Skills (3)
4. **requirements-extractor** (auto) - Extract requirements from issues
5. **security-assessor** (auto) - OWASP Top 10 assessment
6. **tech-stack-evaluator** (auto) - Evaluate tech stack compatibility

#### Design Orchestrator Skills (2)
7. **design-synthesizer** (auto) - Synthesize sub-agent outputs
8. **prp-generator** (auto) - Generate Product Requirements Prompt

#### Architecture Designer Skills (3)
9. **architecture-planner** (auto) - Plan component architecture
10. **data-modeler** (auto) - Design data models (Pydantic)
11. **api-designer** (auto) - Design API contracts

#### Documentation Researcher Skills (2)
12. **doc-fetcher** (auto) - Fetch documentation via context7/fetch
13. **doc-analyzer** (auto) - Analyze and extract patterns

#### Dependency Manager Skills (2)
14. **dependency-analyzer** (auto) - Analyze project dependencies
15. **version-checker** (auto) - Check version compatibility

#### Validation Orchestrator Skills (2)
16. **validation-coordinator** (auto) - Coordinate validation workflow
17. **recursive-communicator** (auto) - Manage agent-to-agent communication

#### Unit Test Specialist Skills (3)
18. **unit-test-writer** (auto) - Write unit tests
19. **pytest-generator** (auto) - Generate pytest tests (Python)
20. **jest-generator** (auto) - Generate Jest tests (TypeScript)

#### Integration Test Specialist Skills (2)
21. **integration-test-writer** (auto) - Write integration tests
22. **api-test-generator** (auto) - Generate API tests

#### Test Runner Specialist Skills (2)
23. **test-executor** (auto) - Execute all tests
24. **coverage-analyzer** (auto) - Analyze test coverage

#### Code Quality Specialist Skills (3)
25. **python-quality-checker** (auto) - Black, mypy, flake8
26. **typescript-quality-checker** (auto) - ESLint, Prettier, tsc
27. **rust-quality-checker** (auto) - rustfmt, clippy

#### Security Specialist Skills (3)
28. **security-scanner** (auto) - Scan for vulnerabilities
29. **vulnerability-assessor** (auto) - Assess vulnerabilities
30. **owasp-checker** (auto) - Check OWASP Top 10

#### E2E & Accessibility Specialist Skills (2)
31. **e2e-test-writer** (auto) - Write E2E tests with Playwright
32. **accessibility-checker** (auto) - Check WCAG compliance

#### Deployment Specialist Skills (3)
33. **documentation-updater** (auto) - Update all documentation
34. **changelog-generator** (auto) - Generate CHANGELOG entries
35. **pr-creator** (auto) - Create GitHub PRs

## MCP Integrations

### Required MCPs

1. **github-mcp**
   - Issue management
   - PR creation
   - Comment management

2. **context7-mcp**
   - Library documentation fetching
   - API reference lookup

3. **sequential-thinking-mcp**
   - Complex reasoning (ultrathink mode)
   - Deep architectural analysis

4. **fetch-mcp**
   - Web documentation fetching
   - External resource retrieval

5. **playwright-mcp** (Frontend only)
   - E2E testing
   - Accessibility verification

## Hooks Configuration

### Pre-Commit Hook
```json
{
  "pre-commit": {
    "command": "python -m pytest tests/ && black --check src/ && mypy src/ && flake8 src/",
    "description": "Run quality checks before committing",
    "blocking": true
  }
}
```

### Post-Implementation Hook
```json
{
  "post-implementation": {
    "command": "python .claude/skills/validation/scripts/run_checks.py",
    "description": "Trigger validation workflow after implementation",
    "blocking": false
  }
}
```

## Quality Standards

### Security
- **OWASP Top 10** compliance
- Input validation at all entry points
- Output sanitization
- Parameterized queries
- Secure authentication/authorization
- No secrets in code/logs

### Performance
- Caching strategy implemented
- Optimized database queries
- Async/await for I/O operations
- Rate limiting
- Response time targets met

### Code Quality
- **500-line file size limit**
- Type hints for all functions
- Google-style docstrings
- Single responsibility principle
- Dependency injection
- Clean interfaces

### Testing
- **80%+ test coverage** minimum
- Unit tests for business logic
- Integration tests for APIs
- Security tests
- Performance tests

### Documentation
- Google-style docstrings
- Type hints for all functions
- README updates
- API documentation
- Architecture documentation
- User guides

## Success Criteria

A feature implementation is complete when:

1. ✅ **Acceptance Criteria:** All criteria from GitHub issue met
2. ✅ **Quality Gates:** All validation checks passed
3. ✅ **Documentation:** Complete implementation docs, guides, API docs
4. ✅ **Testing:** 80%+ coverage, all tests green
5. ✅ **Security:** No critical vulnerabilities, OWASP Top 10 compliant
6. ✅ **Performance:** Response times within targets
7. ✅ **Pull Request:** Created with comprehensive description
8. ✅ **Changelog:** Updated with feature addition
9. ✅ **Task Tracking:** TASK.md updated

## Benefits of v2 Architecture

### For Main Agent
✅ **Full control** over implementation
✅ **Complete visibility** into all code changes
✅ **Direct execution** of coding tasks
✅ **Better debugging** (all actions visible)
✅ **Skills provide guidance** (not execution)

### For Sub-Agents
✅ **Specialized expertise** in analysis, design, validation
✅ **Parallel execution** where possible (Phase 2)
✅ **Recursive communication** for validation fixes
✅ **Clear boundaries** (think, not do)

### For Users
✅ **Watch main agent code** in real-time
✅ **Better transparency** (see what's happening)
✅ **Clear approval checkpoints** (control over implementation)
✅ **Comprehensive documentation** at each phase
✅ **Traceable decisions** (audit trail)

### For Development Process
✅ **Clear separation of concerns** (think vs. do)
✅ **Language-agnostic quality checks** (Python, TypeScript, Rust)
✅ **Flexible validation** (add/remove specialists as needed)
✅ **Comprehensive audit trail** (all phases documented)

## Migration from v1

### Key Differences

| Aspect | v1 | v2 |
|--------|----|----|
| Implementation | Sub-agents code | Main agent codes |
| Design | Single agent | Parallel sub-agents |
| Validation | Single agent | Multiple specialists |
| Communication | One-way | Recursive |
| Documentation | Single doc | Phase-specific docs |
| Approval | Implicit | Explicit checkpoint |

### Migration Path

1. **Phase 1:** Implement v2 agents and skills
2. **Phase 2:** Test v2 with non-critical features
3. **Phase 3:** Migrate existing workflows to v2
4. **Phase 4:** Deprecate v1 agents and skills

## Future Enhancements

### Potential Additions

1. **Performance Profiling Agent**
   - Profile code for performance bottlenecks
   - Suggest optimizations

2. **Documentation Quality Agent**
   - Verify documentation completeness
   - Check for broken links

3. **API Versioning Agent**
   - Manage API versioning
   - Track breaking changes

4. **Rollback Agent**
   - Automated rollback on deployment failure
   - Revert changes safely

5. **Monitoring Integration**
   - Post-deployment monitoring
   - Alert on issues

## Conclusion

The Feature-Implementer v2 architecture provides a robust, scalable, and maintainable system for implementing features from GitHub issues. By maintaining main agent control while leveraging specialized sub-agents, we achieve the best of both worlds: expert guidance with full visibility and control.

The architecture is designed to scale as project complexity grows, with clear extension points for additional specialists and validation steps. The comprehensive documentation at each phase ensures traceability and enables continuous improvement of the development process.

---

**Version:** 2.0.0
**Status:** Design Complete
**Next Steps:** Implementation via GitHub milestone and issues
**Branch:** feature/implementer-v2
