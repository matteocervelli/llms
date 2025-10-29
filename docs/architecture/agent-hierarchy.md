# Agent Hierarchy - Feature-Implementer v2

## Overview

This document defines the complete agent hierarchy for the Feature-Implementer v2 architecture, including agent relationships, responsibilities, and communication patterns.

## Agent Tree Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  /feature-implement <issue-number> [create-branch:true|false]  │
│  (Slash Command)                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  @feature-implementer-main                                      │
│  (Main Orchestrator Prompt)                                     │
│  Model: Sonnet                                                  │
│  Location: .claude/prompts/feature-implementer-main.md          │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
    PHASE 1               PHASE 2               PHASE 3
    Analysis              Design             User Approval
        │                     │                     │
        ▼                     ▼                     ▼
        │                     │                 PHASE 4
        │                     │             Implementation
        │                     │                     │
        │                     │                     ▼
        │                     │                 PHASE 5
        │                     │                Validation
        │                     │                     │
        │                     │                     ▼
        │                     │                 PHASE 6
        │                     │                Deployment
        │                     │
        ▼                     ▼
```

## Phase 1: Analysis Hierarchy

```
@feature-implementer-main
    │
    └── @analysis-specialist
            │
            ├── Skill: requirements-extractor (auto)
            ├── Skill: security-assessor (auto)
            └── Skill: tech-stack-evaluator (auto)
            │
            └── Output: /docs/implementation/analysis/feature-{n}-analysis.md
```

### @analysis-specialist

**Agent Type:** Specialist
**Model:** Haiku
**Parent:** @feature-implementer-main
**Children:** None (uses skills)

**Tools:**
- Read
- Grep
- Glob
- Bash

**MCPs:**
- github-mcp
- sequential-thinking-mcp

**Skills:**
- requirements-extractor (auto-activates)
- security-assessor (auto-activates)
- tech-stack-evaluator (auto-activates)

**Responsibilities:**
1. Fetch GitHub issue
2. Extract requirements and acceptance criteria
3. Assess security risks (OWASP Top 10)
4. Evaluate tech stack compatibility
5. Identify dependencies
6. Define scope boundaries
7. Document analysis

**Communication Pattern:**
- Receives: Issue number from main agent
- Returns: Analysis document path
- Errors: Reports to main agent

## Phase 2: Design Hierarchy

```
@feature-implementer-main
    │
    └── @design-orchestrator
            │
            ├── @architecture-designer (parallel)
            │       ├── Skill: architecture-planner (auto)
            │       ├── Skill: data-modeler (auto)
            │       └── Skill: api-designer (auto)
            │
            ├── @documentation-researcher (parallel)
            │       ├── Skill: doc-fetcher (auto)
            │       └── Skill: doc-analyzer (auto)
            │
            └── @dependency-manager (parallel)
                    ├── Skill: dependency-analyzer (auto)
                    └── Skill: version-checker (auto)
            │
            ├── Skill: design-synthesizer (auto)
            └── Skill: prp-generator (auto)
            │
            └── Output: /docs/implementation/prp/feature-{n}-prp.md
```

### @design-orchestrator

**Agent Type:** Orchestrator
**Model:** Sonnet
**Parent:** @feature-implementer-main
**Children:** 3 sub-agents (parallel execution)

**Tools:**
- Read
- Write
- Edit
- Grep
- Glob

**MCPs:**
- sequential-thinking-mcp

**Skills:**
- design-synthesizer (auto-activates) - Synthesizes sub-agent outputs
- prp-generator (auto-activates) - Generates PRP document

**Responsibilities:**
1. Read analysis document
2. Invoke parallel sub-agents
3. Wait for all sub-agents to complete
4. Synthesize outputs into cohesive design
5. Generate Product Requirements Prompt (PRP)
6. Return PRP document

**Communication Pattern:**
- Receives: Analysis document path from main agent
- Sends: Parallel invocations to 3 sub-agents
- Receives: Outputs from 3 sub-agents
- Returns: PRP document path to main agent
- Errors: Reports to main agent

### @architecture-designer

**Agent Type:** Sub-Agent (Design Layer)
**Model:** Opus
**Parent:** @design-orchestrator
**Children:** None (uses skills + MCP)

**Tools:**
- Read
- Write
- Edit

**MCPs:**
- sequential-thinking-mcp (ultrathink mode)

**Skills:**
- architecture-planner (auto-activates)
- data-modeler (auto-activates)
- api-designer (auto-activates)

**Responsibilities:**
1. Use ultrathink for deep architectural reasoning
2. Design component architecture (interfaces, core, implementations)
3. Define data models (Pydantic schemas)
4. Specify API contracts
5. Plan data flow and interactions
6. Design error handling strategy
7. Return architecture section for PRP

**Communication Pattern:**
- Receives: Analysis document from orchestrator
- Returns: Architecture design to orchestrator
- Errors: Reports to orchestrator

### @documentation-researcher

**Agent Type:** Sub-Agent (Design Layer)
**Model:** Haiku
**Parent:** @design-orchestrator
**Children:** None (uses skills + MCPs)

**Tools:**
- Read
- Grep

**MCPs:**
- context7-mcp
- fetch-mcp

**Skills:**
- doc-fetcher (auto-activates)
- doc-analyzer (auto-activates)

**Responsibilities:**
1. Identify libraries/frameworks from analysis
2. Use context7-mcp to fetch latest documentation
3. Use fetch-mcp for additional resources
4. Extract relevant patterns and examples
5. Document API usage and best practices
6. Return documentation section for PRP

**Communication Pattern:**
- Receives: Analysis document from orchestrator
- Returns: Documentation research to orchestrator
- Errors: Reports to orchestrator

### @dependency-manager

**Agent Type:** Sub-Agent (Design Layer)
**Model:** Haiku
**Parent:** @design-orchestrator
**Children:** None (uses skills)

**Tools:**
- Read
- Bash
- Grep

**Skills:**
- dependency-analyzer (auto-activates)
- version-checker (auto-activates)

**Responsibilities:**
1. Analyze current dependencies (requirements.txt, package.json, etc.)
2. Identify new dependencies needed
3. Check version compatibility
4. Assess security vulnerabilities
5. Plan dependency installation strategy
6. Return dependencies section for PRP

**Communication Pattern:**
- Receives: Analysis document from orchestrator
- Returns: Dependency analysis to orchestrator
- Errors: Reports to orchestrator

## Phase 3: User Approval

```
@feature-implementer-main
    │
    ├── Read PRP document
    ├── Present summary to user
    └── Wait for approval
            │
            ├─► User approves → Continue to Phase 4
            └─► User requests changes → Return to Phase 2
```

**Communication Pattern:**
- Main agent presents PRP to user
- User provides approval or requests changes
- **BLOCKING:** Main agent waits for explicit approval

## Phase 4: Implementation

```
@feature-implementer-main
    │
    ├── Create feature branch
    ├── TDD Implementation Loop
    │       ├── Write failing test (RED)
    │       ├── Implement code (GREEN)
    │       └── Refactor (REFACTOR)
    │
    ├── Skill: implementation (auto)
    ├── Skill: test-generator (on-demand)
    └── Skill: code-reviewer (on-demand)
```

**Agent:** Main agent (self-execution)
**No sub-agents:** Main agent does ALL coding

**Skills:**
- implementation (auto-activates during coding)
- test-generator (on-demand: `/generate-tests <file>`)
- code-reviewer (on-demand: `/review-code <file>`)

**Responsibilities:**
1. Create feature branch
2. Execute TDD cycle for each component
3. Follow coding standards (500-line limit, type hints, docstrings)
4. Use skills for guidance
5. Complete implementation

**Communication Pattern:**
- Self-directed (main agent)
- Skills provide guidance, not execution

## Phase 5: Validation Hierarchy

```
@feature-implementer-main
    │
    └── @validation-orchestrator
            │
            ├── @unit-test-specialist
            │       ├── Skill: unit-test-writer (auto)
            │       ├── Skill: pytest-generator (auto)
            │       └── Skill: jest-generator (auto)
            │       └── Output: tests/*.test.py
            │
            ├── @integration-test-specialist
            │       ├── Skill: integration-test-writer (auto)
            │       └── Skill: api-test-generator (auto)
            │       └── Output: tests/integration/*.py
            │
            ├── @test-runner-specialist
            │       ├── Skill: test-executor (auto)
            │       └── Skill: coverage-analyzer (auto)
            │       └── Output: /docs/implementation/tests/feature-{n}-tests.md
            │
            ├── @code-quality-specialist
            │       ├── Skill: python-quality-checker (auto)
            │       ├── Skill: typescript-quality-checker (auto)
            │       └── Skill: rust-quality-checker (auto)
            │       └── No documentation output
            │
            ├── @security-specialist
            │       ├── Skill: security-scanner (auto)
            │       ├── Skill: vulnerability-assessor (auto)
            │       └── Skill: owasp-checker (auto)
            │       └── Output: /docs/implementation/security/feature-{n}-security.md
            │
            └── @e2e-accessibility-specialist (if frontend)
                    ├── Skill: e2e-test-writer (auto)
                    └── Skill: accessibility-checker (auto)
                    └── Output: /docs/implementation/e2e/feature-{n}-e2e.md
            │
            ├── Skill: validation-coordinator (auto)
            └── Skill: recursive-communicator (auto)
```

### @validation-orchestrator

**Agent Type:** Orchestrator
**Model:** Sonnet
**Parent:** @feature-implementer-main
**Children:** 5-6 specialists (sequential with recursive communication)

**Tools:**
- Read
- Bash
- Grep
- Glob

**MCPs:**
- github-mcp
- sequential-thinking-mcp

**Skills:**
- validation-coordinator (auto-activates)
- recursive-communicator (auto-activates)

**Responsibilities:**
1. Invoke validation specialists in sequence
2. Manage recursive communication between specialists and main agent
3. Coordinate validation workflow
4. Ensure all validations pass
5. Report final validation status

**Communication Pattern:**
- Receives: Implementation completion from main agent
- Sends: Sequential invocations to specialists
- Receives: Validation results from specialists
- Communicates: Failures back to main agent for fixes
- Returns: Validation completion to main agent
- Errors: Reports to main agent

### @unit-test-specialist

**Agent Type:** Specialist (Validation Layer)
**Model:** Haiku
**Parent:** @validation-orchestrator
**Children:** None (uses skills)

**Tools:**
- Read
- Write
- Edit

**Skills:**
- unit-test-writer (auto-activates)
- pytest-generator (auto-activates, Python)
- jest-generator (auto-activates, TypeScript)

**Responsibilities:**
1. Read implementation files
2. Generate unit tests: `main-file-name.test.py`
3. Use pytest fixtures, mocking (Python) or Jest patterns (TypeScript)
4. Communicate with main agent if clarification needed
5. Return test files

**Communication Pattern:**
- Receives: Implementation files from orchestrator
- Communicates: Clarification requests to main agent (via orchestrator)
- Returns: Unit test files to orchestrator
- Errors: Reports to orchestrator

### @integration-test-specialist

**Agent Type:** Specialist (Validation Layer)
**Model:** Haiku
**Parent:** @validation-orchestrator
**Children:** None (uses skills)

**Tools:**
- Read
- Write
- Edit

**Skills:**
- integration-test-writer (auto-activates)
- api-test-generator (auto-activates)

**Responsibilities:**
1. Read architecture from PRP
2. Generate integration tests for APIs, service interactions
3. Use test fixtures for databases, external services
4. Communicate with main agent for test scenarios
5. Return integration test files

**Communication Pattern:**
- Receives: PRP and implementation from orchestrator
- Communicates: Test scenario requests to main agent (via orchestrator)
- Returns: Integration test files to orchestrator
- Errors: Reports to orchestrator

### @test-runner-specialist

**Agent Type:** Specialist (Validation Layer)
**Model:** Haiku
**Parent:** @validation-orchestrator
**Children:** None (uses skills)

**Tools:**
- Read
- Bash

**Skills:**
- test-executor (auto-activates)
- coverage-analyzer (auto-activates)

**Responsibilities:**
1. Run all tests (unit + integration)
2. Verify coverage ≥ 80%
3. Document test results
4. Communicate failures to main agent (via orchestrator)
5. Re-run tests after fixes (recursive)
6. Return test results document

**Communication Pattern:**
- Receives: Test completion from orchestrator
- Communicates: Test failures to main agent (via orchestrator)
- Returns: Test results document to orchestrator
- Recursive: Re-runs tests after main agent fixes
- Errors: Reports to orchestrator

### @code-quality-specialist

**Agent Type:** Specialist (Validation Layer)
**Model:** Haiku
**Parent:** @validation-orchestrator
**Children:** None (uses language-specific skills)

**Tools:**
- Read
- Bash

**Skills (Language-Specific):**
- python-quality-checker (auto-activates for Python)
- typescript-quality-checker (auto-activates for TypeScript)
- rust-quality-checker (auto-activates for Rust)

**Responsibilities:**
1. Detect language from project
2. Run appropriate quality checks
3. Communicate issues to main agent (via orchestrator)
4. Re-run checks after fixes (recursive)
5. No documentation output

**Communication Pattern:**
- Receives: Implementation completion from orchestrator
- Communicates: Quality issues to main agent (via orchestrator)
- Returns: Quality check status to orchestrator
- Recursive: Re-runs checks after main agent fixes
- Errors: Reports to orchestrator

### @security-specialist

**Agent Type:** Specialist (Validation Layer)
**Model:** Sonnet
**Parent:** @validation-orchestrator
**Children:** None (uses skills)

**Tools:**
- Read
- Bash

**Skills:**
- security-scanner (auto-activates)
- vulnerability-assessor (auto-activates)
- owasp-checker (auto-activates)

**Responsibilities:**
1. Scan for security vulnerabilities
2. Check OWASP Top 10 compliance
3. Verify input validation, output sanitization
4. Check authentication/authorization
5. Scan dependencies for vulnerabilities
6. Document findings
7. Communicate vulnerabilities to main agent (via orchestrator)
8. Re-scan after fixes (recursive)
9. Return security assessment document

**Communication Pattern:**
- Receives: Implementation completion from orchestrator
- Communicates: Vulnerabilities to main agent (via orchestrator)
- Returns: Security assessment document to orchestrator
- Recursive: Re-scans after main agent fixes
- Errors: Reports to orchestrator

### @e2e-accessibility-specialist

**Agent Type:** Specialist (Validation Layer, Frontend Only)
**Model:** Haiku
**Parent:** @validation-orchestrator
**Children:** None (uses skills + MCP)

**Tools:**
- Read
- Bash

**MCPs:**
- playwright-mcp

**Skills:**
- e2e-test-writer (auto-activates)
- accessibility-checker (auto-activates)

**Responsibilities:**
1. Identify frontend components from PRP
2. Generate E2E tests with Playwright
3. Test accessibility features (WCAG compliance)
4. Document test scenarios
5. Communicate issues to main agent (via orchestrator)
6. Re-run tests after fixes (recursive)
7. Return E2E & accessibility document

**Communication Pattern:**
- Receives: Frontend implementation from orchestrator
- Communicates: E2E/accessibility issues to main agent (via orchestrator)
- Returns: E2E & accessibility document to orchestrator
- Recursive: Re-runs tests after main agent fixes
- Errors: Reports to orchestrator

## Phase 6: Deployment Hierarchy

```
@feature-implementer-main
    │
    └── @deployment-specialist
            │
            ├── Skill: documentation-updater (auto)
            ├── Skill: changelog-generator (auto)
            └── Skill: pr-creator (auto)
            │
            └── Outputs: CHANGELOG.md, docs/, PR
```

### @deployment-specialist

**Agent Type:** Specialist
**Model:** Haiku
**Parent:** @feature-implementer-main
**Children:** None (uses skills)

**Tools:**
- Read
- Write
- Edit
- Bash
- gh
- git

**MCPs:**
- github-mcp

**Skills:**
- documentation-updater (auto-activates)
- changelog-generator (auto-activates)
- pr-creator (auto-activates)

**Responsibilities:**
1. Update CHANGELOG.md
2. Update documentation (implementation docs, API docs, user guides)
3. Update TASK.md
4. Pre-commit hook execution (automatic)
5. Commit changes
6. Push to remote
7. Create PR
8. Update GitHub issue with PR link

**Communication Pattern:**
- Receives: Validation completion from main agent
- Returns: Deployment completion to main agent
- Errors: Reports to main agent

## Agent Communication Patterns

### Pattern 1: Sequential Delegation
```
Main Agent → Sub-Agent → Return to Main Agent
```
**Used in:** Phase 1 (Analysis), Phase 6 (Deployment)

**Flow:**
1. Main agent invokes sub-agent
2. Sub-agent executes task
3. Sub-agent returns result
4. Main agent continues

### Pattern 2: Parallel Delegation
```
Main Agent → Orchestrator → Sub-Agent 1 (parallel)
                          → Sub-Agent 2 (parallel)
                          → Sub-Agent 3 (parallel)
             ← Orchestrator ← All complete
```
**Used in:** Phase 2 (Design)

**Flow:**
1. Main agent invokes orchestrator
2. Orchestrator invokes 3 sub-agents in parallel
3. Orchestrator waits for all to complete
4. Orchestrator synthesizes results
5. Orchestrator returns to main agent

### Pattern 3: Recursive Communication
```
Main Agent → Orchestrator → Specialist 1 → Check
                                          → Fail → Communicate to Main Agent
                                          → Main Agent Fixes
                                          → Specialist 1 Re-checks
                                          → Pass → Continue
                          → Specialist 2 → ...
```
**Used in:** Phase 5 (Validation)

**Flow:**
1. Main agent invokes orchestrator
2. Orchestrator invokes specialists sequentially
3. Specialist checks and reports failures
4. Orchestrator communicates failures to main agent
5. Main agent fixes issues
6. Specialist re-checks
7. Loop continues until pass
8. Orchestrator moves to next specialist
9. All specialists complete
10. Orchestrator returns to main agent

### Pattern 4: User Interaction
```
Main Agent → Present to User → User Responds → Main Agent Continues
```
**Used in:** Phase 3 (User Approval)

**Flow:**
1. Main agent presents PRP summary
2. Main agent waits (BLOCKING)
3. User approves or requests changes
4. Main agent continues or returns to Phase 2

## Agent Responsibilities Matrix

| Agent | Analysis | Design | Approval | Implementation | Validation | Deployment |
|-------|----------|--------|----------|----------------|------------|------------|
| Main Orchestrator | Delegate | Delegate | Present | **Execute** | Delegate | Delegate |
| Analysis Specialist | **Execute** | - | - | - | - | - |
| Design Orchestrator | - | **Coordinate** | - | - | - | - |
| Architecture Designer | - | **Execute** | - | - | - | - |
| Documentation Researcher | - | **Execute** | - | - | - | - |
| Dependency Manager | - | **Execute** | - | - | - | - |
| Validation Orchestrator | - | - | - | - | **Coordinate** | - |
| Unit Test Specialist | - | - | - | - | **Execute** | - |
| Integration Test Specialist | - | - | - | - | **Execute** | - |
| Test Runner Specialist | - | - | - | - | **Execute** | - |
| Code Quality Specialist | - | - | - | - | **Execute** | - |
| Security Specialist | - | - | - | - | **Execute** | - |
| E2E & Accessibility | - | - | - | - | **Execute** | - |
| Deployment Specialist | - | - | - | - | - | **Execute** |

**Legend:**
- **Execute:** Agent performs the work
- **Coordinate:** Agent orchestrates sub-agents
- **Delegate:** Agent invokes sub-agents
- **Present:** Agent interacts with user

## Agent Count Summary

### By Layer
- **Entry:** 1 (slash command)
- **Orchestration:** 1 (main orchestrator)
- **Analysis:** 1 (analysis specialist)
- **Design:** 4 (1 orchestrator + 3 sub-agents)
- **Validation:** 7 (1 orchestrator + 6 specialists)
- **Deployment:** 1 (deployment specialist)

### Total: 15 Components
- 1 slash command
- 1 main orchestrator (prompt)
- 13 agents

## Agent File Locations

```
.claude/
├── commands/
│   └── feature-implement.md                  # Slash command
│
├── prompts/
│   └── feature-implementer-main.md           # Main orchestrator
│
└── agents/
    ├── analysis-specialist.md                # Phase 1
    ├── design-orchestrator.md                # Phase 2 orchestrator
    ├── architecture-designer.md              # Phase 2 sub-agent
    ├── documentation-researcher.md           # Phase 2 sub-agent
    ├── dependency-manager.md                 # Phase 2 sub-agent
    ├── validation-orchestrator.md            # Phase 5 orchestrator
    ├── unit-test-specialist.md               # Phase 5 specialist
    ├── integration-test-specialist.md        # Phase 5 specialist
    ├── test-runner-specialist.md             # Phase 5 specialist
    ├── code-quality-specialist.md            # Phase 5 specialist
    ├── security-specialist.md                # Phase 5 specialist
    ├── e2e-accessibility-specialist.md       # Phase 5 specialist
    └── deployment-specialist.md              # Phase 6
```

## Conclusion

The agent hierarchy is designed for:
- **Clear responsibilities:** Each agent has a specific role
- **Efficient communication:** Patterns for sequential, parallel, and recursive workflows
- **Main agent control:** Main agent orchestrates and implements
- **Specialized expertise:** Sub-agents provide domain knowledge
- **Scalability:** Easy to add new specialists or orchestrators

This hierarchy ensures that the main Claude Code agent maintains full control over implementation while leveraging specialized sub-agents for analysis, design, and validation.

---

**Version:** 2.0.0
**Status:** Design Complete
**Next Steps:** Agent implementation via GitHub issues
**Branch:** feature/implementer-v2
