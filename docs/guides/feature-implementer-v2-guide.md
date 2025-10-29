# Feature-Implementer v2: Complete User Guide

**Version**: 1.0.0
**Date**: 2025-10-29
**Status**: Production Ready

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [The 6-Phase Workflow](#the-6-phase-workflow)
4. [All 14 Agents](#all-14-agents)
5. [Skills System](#skills-system)
6. [Quality Automation](#quality-automation)
7. [Common Scenarios](#common-scenarios)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Usage](#advanced-usage)

---

## Introduction

The **Feature-Implementer v2 Architecture** is a sophisticated multi-agent system that orchestrates the complete software development lifecycle. It provides:

- **14 specialized agents** for analysis, design, implementation, validation, and deployment
- **37 production skills** with domain expertise
- **Automated quality gates** via hooks
- **Progressive disclosure** for efficient token usage (99.76% reduction vs v1)
- **Recursive validation** ensuring code quality

### When to Use

✅ **Use Feature-Implementer v2 for**:
- Implementing new features from GitHub issues
- Features requiring security considerations
- Complex multi-component implementations
- Projects needing comprehensive documentation
- Teams requiring quality enforcement

❌ **Don't use for**:
- Simple bug fixes (use `/issue-fix` instead)
- Quick prototypes or experiments
- Single-function changes
- Documentation-only updates

---

## Quick Start

### Prerequisites

1. **GitHub Issue**: Feature must be tracked in a GitHub issue
2. **Project Setup**: Git repository with `.claude/` directory
3. **Hooks Configured**: Pre-commit and post-implementation hooks enabled

### Basic Usage

```bash
# Invoke the feature-implementer agent
@feature-implementer implement issue #123

# The agent will guide you through 6 phases:
# Phase 1: Analysis (automatic)
# Phase 2: Design (automatic)
# Phase 3: Approval (requires your input)
# Phase 4: Implementation (automatic)
# Phase 5: Validation (automatic)
# Phase 6: Deployment (automatic)
```

### Your Role

You have **TWO key responsibilities**:

1. **Provide GitHub Issue**: Well-written issue with clear requirements
2. **Approve Design** (Phase 3): Review and approve architecture before implementation

Everything else is automated!

---

## The 6-Phase Workflow

### Phase 1: Requirements Analysis

**Agent**: `@analysis-specialist` (Haiku model)
**Duration**: ~2-3 minutes
**Auto-activated Skills**:
- requirements-extractor
- security-assessor
- tech-stack-evaluator

**What Happens**:
1. Fetches GitHub issue details
2. Extracts functional and non-functional requirements
3. Assesses security implications (OWASP Top 10, data privacy)
4. Evaluates tech stack compatibility
5. Identifies dependencies and constraints

**Output**: `docs/implementation/analysis/analysis.md`

**Example Output**:
```markdown
# Requirements Analysis

## Functional Requirements
1. User can upload profile photo
2. Photo is resized to 300x300px
3. Photo is stored in S3

## Non-Functional Requirements
- Max file size: 5MB
- Supported formats: JPG, PNG, WebP
- Response time: < 2 seconds

## Security Assessment
- Input validation: File type, size checks
- Storage: Secure S3 bucket with encryption
- Access control: User can only upload own photo
- OWASP: A03:2021 - Injection (file upload)

## Tech Stack
- Backend: Python + FastAPI
- Storage: AWS S3
- Image processing: Pillow library
```

**What You Do**: Nothing - this phase is fully automatic

---

### Phase 2: Architecture & Design

**Agent**: `@design-orchestrator` (Sonnet model)
**Duration**: ~5-7 minutes
**Sub-agents** (run in parallel):
- `@architecture-designer` (Opus + ultrathink)
- `@documentation-researcher` (Haiku + context7-mcp)
- `@dependency-manager` (Haiku)

**What Happens**:
1. **Architecture Design**:
   - Component breakdown
   - Data models
   - API contracts
   - System interactions

2. **Documentation Research**:
   - Fetches latest library docs (FastAPI, Pillow, boto3, etc.)
   - Identifies best practices
   - Finds usage examples

3. **Dependency Management**:
   - Analyzes dependency compatibility
   - Checks version constraints
   - Identifies potential conflicts

4. **Design Synthesis**:
   - Combines all sub-agent outputs
   - Creates cohesive architecture plan
   - Generates PRP document

**Output**: `docs/implementation/prp/prp.md` (Problem-Requirements-Plan)

**Example Output**:
```markdown
# Problem-Requirements-Plan (PRP)

## Problem
Users cannot upload profile photos, limiting personalization.

## Requirements
[From Phase 1 analysis]

## Architecture Plan

### Components
1. **UploadEndpoint** (`/api/v1/users/{user_id}/photo`)
   - Method: POST
   - Auth: Bearer token
   - Input: multipart/form-data
   - Output: JSON with photo URL

2. **PhotoProcessor** (`src/services/photo_processor.py`)
   - Validate file type and size
   - Resize to 300x300px
   - Optimize for web

3. **S3StorageService** (`src/services/s3_storage.py`)
   - Upload to S3
   - Generate signed URL
   - Handle errors

### Data Models
```python
class PhotoUpload(BaseModel):
    file: UploadFile
    user_id: str

class PhotoResponse(BaseModel):
    url: str
    uploaded_at: datetime
```

### API Contract
POST /api/v1/users/{user_id}/photo
Request: multipart/form-data with 'file' field
Response: 200 OK with PhotoResponse

### Dependencies
- fastapi >= 0.100.0
- pillow >= 10.0.0
- boto3 >= 1.28.0
```

**What You Do**: Nothing yet - wait for Phase 3

---

### Phase 3: User Approval

**Agent**: `@feature-implementer` (Sonnet model)
**Duration**: Your decision
**Interactive**: YES - requires your input

**What Happens**:
1. Agent presents analysis and design documents
2. Highlights key architectural decisions
3. Asks for your approval

**What You Do**: Review and decide

**Option 1: Approve**:
```
You: "The design looks good, please proceed with implementation."
```
→ Moves to Phase 4 (Implementation)

**Option 2: Request Changes**:
```
You: "Please revise the API to use GraphQL instead of REST."
```
→ Returns to Phase 2 with your feedback

**Option 3: Ask Questions**:
```
You: "Why did you choose Pillow over ImageMagick?"
Agent: [Explains reasoning]
You: "OK, proceed with Pillow."
```
→ Moves to Phase 4 after clarification

**Review Checklist**:
- ✅ Architecture aligns with project standards
- ✅ Security considerations are adequate
- ✅ Dependencies are appropriate
- ✅ API contracts make sense
- ✅ Data models are well-designed
- ✅ No over-engineering or under-engineering

**Pro Tip**: Use Plan Mode (Shift+Tab twice) to explore design in detail before approval

---

### Phase 4: Implementation

**Agent**: `@feature-implementer` (Sonnet model)
**Duration**: ~10-20 minutes (varies by complexity)
**Auto-activated Skills**:
- analysis
- design
- implementation

**What Happens**:
1. **Test-Driven Development**:
   - Writes tests first (unit tests)
   - Implements code to pass tests
   - Refactors for quality

2. **Code Standards**:
   - Follows project conventions
   - Maintains ≤500 lines per file
   - Adds comprehensive docstrings
   - Type hints for all functions

3. **Best Practices**:
   - Single Responsibility Principle
   - Dependency Injection
   - Error handling
   - Logging

4. **Initial Testing**:
   - Runs unit tests
   - Fixes any failures
   - Ensures tests pass before proceeding

**Output**:
- Implementation files (src/)
- Unit test files (tests/)
- Initial test results

**What You Do**: Nothing - implementation is automatic

**What Gets Created**:
```
src/
├── api/
│   └── endpoints/
│       └── photo_upload.py        # API endpoint
├── services/
│   ├── photo_processor.py         # Image processing
│   └── s3_storage.py              # S3 operations
└── models/
    └── photo.py                   # Data models

tests/
├── test_photo_upload.py           # API tests
├── test_photo_processor.py        # Processor tests
└── test_s3_storage.py             # Storage tests
```

---

### Phase 5: Validation

**Agent**: `@validation-orchestrator` (Sonnet model)
**Duration**: ~15-25 minutes
**Specialists** (run sequentially with recursive communication):

1. **Unit Test Specialist** (`@unit-test-specialist`, Haiku)
2. **Integration Test Specialist** (`@integration-test-specialist`, Haiku)
3. **Test Runner Specialist** (`@test-runner-specialist`, Haiku)
4. **Code Quality Specialist** (`@code-quality-specialist`, Haiku)
5. **Security Specialist** (`@security-specialist`, Sonnet)
6. **E2E/Accessibility Specialist** (`@e2e-accessibility-specialist`, Sonnet + playwright) - frontend only

**What Happens**:

**Step 1: Unit Tests** (~3 min)
- Reviews existing unit tests
- Adds missing test cases
- Ensures edge cases covered
- Validates test quality

**Step 2: Integration Tests** (~4 min)
- Creates integration tests
- Tests component interactions
- Tests API endpoints end-to-end
- Validates error handling

**Step 3: Test Execution** (~3 min)
- Runs all tests (unit + integration)
- Generates coverage report
- **Validates ≥80% coverage**
- Reports failures if any

**Step 4: Code Quality** (~4 min)
- Runs Black (formatting)
- Runs Flake8 (linting)
- Runs Mypy (type checking)
- **All must pass**

**Step 5: Security Scan** (~5 min)
- OWASP Top 10 compliance
- Input validation checks
- Authentication/authorization review
- Secret detection
- Vulnerability assessment

**Step 6: E2E & Accessibility** (~6 min, frontend only)
- Playwright E2E tests
- User flow validation
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader compatibility

**Recursive Communication**:
If any validation fails:
1. Validation Orchestrator receives failure report
2. Orchestrator asks implementation agent to fix issues
3. Implementation agent fixes problems
4. Validation repeats from failed step
5. Loop continues until all checks pass

**Output**:
- Test reports (docs/implementation/tests/)
- Coverage reports
- Security scan results (docs/implementation/security/)
- E2E test results (docs/implementation/e2e/, frontend only)

**What You Do**: Nothing - validation is automatic and recursive

**Success Criteria**:
✅ All tests pass
✅ Coverage ≥80%
✅ Black, Flake8, Mypy pass
✅ No security vulnerabilities
✅ E2E tests pass (frontend)
✅ WCAG 2.1 AA compliance (frontend)

---

### Phase 6: Deployment

**Agent**: `@deployment-specialist` (Haiku model)
**Duration**: ~5-8 minutes
**Auto-activated Skills**:
- documentation-updater
- changelog-generator
- pr-creator

**What Happens**:
1. **Documentation Updates**:
   - Updates README.md (if needed)
   - Updates API documentation
   - Creates/updates user guides
   - Updates architecture docs

2. **CHANGELOG Generation**:
   - Creates CHANGELOG entry
   - Follows conventional format
   - Lists all changes
   - Includes breaking changes

3. **Pull Request Creation**:
   - Creates PR with detailed description
   - Links to GitHub issue
   - Includes test plan
   - Adds appropriate labels

**Output**:
- Updated documentation files
- CHANGELOG.md entry
- GitHub Pull Request

**What You Do**: Review the PR and merge when ready

**Example PR Description**:
```markdown
## Summary
Implement user profile photo upload feature with image processing and S3 storage.

## Changes
- Added POST /api/v1/users/{user_id}/photo endpoint
- Implemented PhotoProcessor service for image validation and resizing
- Integrated S3StorageService for secure file storage
- Added comprehensive unit and integration tests (85% coverage)
- Security: Input validation, file type checks, access control

## Test Plan
- [x] Unit tests pass (85% coverage)
- [x] Integration tests pass
- [x] Security scan clean (OWASP Top 10)
- [x] Code quality checks pass (Black, Flake8, Mypy)
- [ ] Manual testing: Upload photo via UI
- [ ] Manual testing: Verify S3 storage

## Breaking Changes
None

## Related Issues
Closes #123

🤖 Generated with Feature-Implementer v2
```

---

## All 14 Agents

### Orchestrators (2)

**1. feature-implementer** (Main)
- **Model**: Sonnet
- **Role**: Orchestrates all 6 phases
- **Skills**: analysis, design, implementation, validation
- **Invocation**: `@feature-implementer implement issue #123`

**2. design-orchestrator** (Phase 2)
- **Model**: Sonnet
- **Role**: Coordinates 3 parallel design sub-agents
- **Skills**: design-synthesizer, prp-generator
- **Invocation**: Automatic (called by main agent)

**3. validation-orchestrator** (Phase 5)
- **Model**: Sonnet
- **Role**: Coordinates 6 sequential validation specialists
- **Skills**: validation-coordinator, recursive-communicator
- **Invocation**: Automatic (called by main agent)

### Analysis (1)

**4. analysis-specialist** (Phase 1)
- **Model**: Haiku
- **Role**: Requirements extraction, security assessment
- **Skills**: requirements-extractor, security-assessor, tech-stack-evaluator
- **Invocation**: Automatic (called by main agent)

### Design Sub-Agents (3)

**5. architecture-designer** (Phase 2)
- **Model**: Opus + sequential-thinking MCP (ultrathink)
- **Role**: Component architecture, data models, API contracts
- **Skills**: architecture-planner, data-modeler, api-designer
- **Invocation**: Automatic (called by design-orchestrator)

**6. documentation-researcher** (Phase 2)
- **Model**: Haiku + context7-mcp, fetch-mcp
- **Role**: Fetch latest library documentation
- **Skills**: doc-fetcher, doc-analyzer
- **Invocation**: Automatic (called by design-orchestrator)

**7. dependency-manager** (Phase 2)
- **Model**: Haiku
- **Role**: Dependency analysis and compatibility
- **Skills**: dependency-analyzer, version-checker
- **Invocation**: Automatic (called by design-orchestrator)

### Validation Specialists (6)

**8. unit-test-specialist** (Phase 5)
- **Model**: Haiku
- **Role**: Write comprehensive unit tests
- **Skills**: unit-test-writer, pytest-generator, jest-generator
- **Invocation**: Automatic (called by validation-orchestrator)

**9. integration-test-specialist** (Phase 5)
- **Model**: Haiku
- **Role**: Write integration tests for component interactions
- **Skills**: integration-test-writer, api-test-generator
- **Invocation**: Automatic (called by validation-orchestrator)

**10. test-runner-specialist** (Phase 5)
- **Model**: Haiku
- **Role**: Execute tests, verify ≥80% coverage
- **Skills**: test-executor, coverage-analyzer
- **Invocation**: Automatic (called by validation-orchestrator)

**11. code-quality-specialist** (Phase 5)
- **Model**: Haiku
- **Role**: Formatting, linting, type checking
- **Skills**: python-quality-checker, typescript-quality-checker, rust-quality-checker
- **Invocation**: Automatic (called by validation-orchestrator)

**12. security-specialist** (Phase 5)
- **Model**: Sonnet
- **Role**: Security scanning, OWASP Top 10 compliance
- **Skills**: security-scanner, vulnerability-assessor, owasp-checker
- **Invocation**: Automatic (called by validation-orchestrator)

**13. e2e-accessibility-specialist** (Phase 5, frontend only)
- **Model**: Sonnet + playwright-mcp
- **Role**: E2E testing, WCAG 2.1 AA compliance
- **Skills**: e2e-test-writer, accessibility-checker
- **Invocation**: Automatic for frontend features

### Deployment (1)

**14. deployment-specialist** (Phase 6)
- **Model**: Haiku
- **Role**: Documentation updates, CHANGELOG, PR creation
- **Skills**: documentation-updater, changelog-generator, pr-creator
- **Invocation**: Automatic (called by main agent)

---

## Skills System

### What are Skills?

Skills are **domain expertise bundles** that agents auto-activate based on task descriptions. They provide:
- Guidance and best practices
- Templates and patterns
- Checklists and workflows
- Tool usage examples

### How Skills Work

**Auto-Activation**:
```
Agent describes task → Claude Code matches to skills → Skills load context
```

**Progressive Disclosure**:
- Only active skills loaded (not all 37 at once)
- Context released after task completes
- Efficient token usage (99.76% reduction vs v1)

### 37 Production Skills

**Core Workflow (4)**:
- `analysis/` - Requirements analysis guidance
- `design/` - Architecture and API design patterns
- `implementation/` - TDD implementation with code style guide
- `validation/` - Quality validation workflow

**Phase 1: Analysis (3)**:
- `requirements-extractor/` - Extract functional & non-functional requirements
- `security-assessor/` - OWASP, data privacy, authentication guidance
- `tech-stack-evaluator/` - Tech stack compatibility assessment

**Phase 2: Design (10)**:
- `design-synthesizer/` - Combine sub-agent outputs into cohesive plan
- `prp-generator/` - Problem-Requirements-Plan document generation
- `architecture-planner/` - Component architecture patterns
- `data-modeler/` - Data model design best practices
- `api-designer/` - API contract design (REST, GraphQL)
- `doc-fetcher/` - Fetch latest library documentation
- `doc-analyzer/` - Analyze docs for best practices
- `dependency-analyzer/` - Dependency compatibility checks
- `version-checker/` - Version constraint management

**Phase 5: Validation (20)**:
- `validation-coordinator/` - Orchestrate sequential validation
- `recursive-communicator/` - Handle validation failures and retries
- `unit-test-writer/` - Unit test patterns and best practices
- `pytest-generator/` - pytest-specific test generation
- `jest-generator/` - Jest-specific test generation
- `integration-test-writer/` - Integration test patterns
- `api-test-generator/` - API endpoint testing
- `test-executor/` - Test execution and reporting
- `coverage-analyzer/` - Coverage analysis and ≥80% validation
- `python-quality-checker/` - Black, Flake8, Mypy for Python
- `typescript-quality-checker/` - ESLint, Prettier, TSC for TypeScript
- `rust-quality-checker/` - Clippy, rustfmt for Rust
- `security-scanner/` - Automated security scanning
- `vulnerability-assessor/` - Vulnerability assessment
- `owasp-checker/` - OWASP Top 10 compliance
- `e2e-test-writer/` - Playwright E2E test patterns
- `accessibility-checker/` - WCAG 2.1 AA compliance checks

**Phase 6: Deployment (3)**:
- `documentation-updater/` - Documentation update patterns
- `changelog-generator/` - CHANGELOG entry generation
- `pr-creator/` - Pull request creation best practices

**On-Demand (2)**:
- `code-reviewer/` - Code review guidelines and checklists
- `test-generator/` - Generic test generation patterns

### Skill Structure

Each skill directory contains:
```
.claude/skills/skill-name/
├── SKILL.md              # Main skill definition
├── examples/             # Usage examples (optional)
├── templates/            # Code templates (optional)
└── resources/            # Additional resources (optional)
```

### Customizing Skills

Edit skill files to customize guidance:

```bash
# Edit a skill
vim .claude/skills/requirements-extractor/SKILL.md

# Add your project-specific patterns
# Add your company standards
# Add language-specific conventions
```

Skills are **project-scoped** - changes apply to this project only.

---

## Quality Automation

### Pre-commit Hook

**Triggers**: On every `git commit` command
**Purpose**: Enforce code quality before commits
**Blocking**: Yes (exit code 2 prevents commit)
**Timeout**: 180 seconds

**Checks Performed** (in order):
1. **Black** (formatting)
   - Checks src/ and tests/
   - Fails if code not formatted
   - Run `black src/ tests/` to fix

2. **Flake8** (linting)
   - Max line length: 100
   - Ignores: E203, W503
   - Fails if linting errors found

3. **Mypy** (type checking)
   - Checks src/
   - Fails if type errors found
   - Add type hints to fix

4. **Pytest** (tests)
   - Runs all tests
   - Fails if any test fails
   - Fix failing tests

**Example Output** (failure):
```
🔍 Running pre-commit quality checks...

  ✓ Checking code formatting (black)...
  ✓ Running linter (flake8)...
  ✓ Type checking (mypy)...

❌ Pre-commit checks FAILED:

1. Mypy (type checking):
src/services/photo_processor.py:42: error: Function is missing a return type annotation

🚫 Commit blocked. Please fix the issues above before committing.
```

**Bypass** (not recommended):
```bash
# Skip pre-commit hook (use sparingly)
git commit --no-verify -m "WIP: in progress"
```

### Post-implementation Hook

**Triggers**: When implementation phase completes
**Purpose**: Auto-launch validation workflow
**Blocking**: No (non-blocking design)
**Timeout**: 60 seconds

**Detection Logic**:
- Monitors conversation transcript
- Detects completion markers:
  - "implementation complete"
  - "implementation phase complete"
  - "all tests pass"
  - "ready for validation"

**What It Does**:
1. Detects implementation completion
2. Extracts design document paths
3. Triggers `@validation-orchestrator`
4. Validation proceeds automatically

**Infinite Loop Prevention**:
- `stop_hook_active` flag prevents re-triggering
- Hook only runs once per implementation
- Non-blocking design allows normal conversation

**Example**:
```
[Implementation completes]

🎯 Implementation complete! Triggering validation workflow...

[Validation-orchestrator automatically invoked]
```

---

## Common Scenarios

### Scenario 1: Simple Backend Feature

**Issue**: "Add GET /api/users endpoint to list users"

**Workflow**:
```bash
@feature-implementer implement issue #456

# Phase 1: Analysis (~2 min)
# - Extract requirements: List users with pagination
# - Security: Authentication required, no sensitive data exposure
# - Tech stack: Python + FastAPI

# Phase 2: Design (~5 min)
# - Architecture: Simple API endpoint
# - Data model: User response model
# - Dependencies: No new dependencies needed

# Phase 3: Approval
You: "Looks good, proceed"

# Phase 4: Implementation (~10 min)
# - Creates src/api/endpoints/users.py
# - Creates tests/test_users.py
# - Implements pagination
# - Adds docstrings and type hints

# Phase 5: Validation (~15 min)
# - Unit tests: 6 tests added, all pass
# - Integration tests: API endpoint tested
# - Test coverage: 92% (exceeds 80% requirement)
# - Code quality: All checks pass
# - Security: No vulnerabilities found

# Phase 6: Deployment (~5 min)
# - Updates API documentation
# - Adds CHANGELOG entry
# - Creates PR #457
```

**Total Time**: ~37 minutes
**Result**: Production-ready feature with tests, docs, and PR

### Scenario 2: Frontend Feature with Accessibility

**Issue**: "Add user profile photo upload UI component"

**Workflow**:
```bash
@feature-implementer implement issue #789

# Phase 1: Analysis (~2 min)
# - Requirements: Upload photo, preview, validation
# - Security: File type checks, size limits
# - Accessibility: Must support keyboard and screen readers

# Phase 2: Design (~6 min)
# - Component architecture: PhotoUpload.tsx
# - State management: React hooks
# - API integration: POST /api/users/{id}/photo
# - Accessibility: ARIA labels, keyboard navigation

# Phase 3: Approval
You: "Design looks good, proceed"

# Phase 4: Implementation (~12 min)
# - Creates src/components/PhotoUpload.tsx
# - Creates tests/PhotoUpload.test.tsx
# - Implements drag-and-drop
# - Adds ARIA labels and keyboard support

# Phase 5: Validation (~25 min)
# - Unit tests: Component rendering, state changes
# - Integration tests: API calls, error handling
# - Test coverage: 88%
# - Code quality: ESLint, Prettier pass
# - Security: No XSS vulnerabilities
# - E2E tests: Playwright tests for upload flow
# - Accessibility: WCAG 2.1 AA compliant (automated check)

# Phase 6: Deployment (~6 min)
# - Updates component documentation
# - Adds Storybook story
# - Updates CHANGELOG
# - Creates PR #790
```

**Total Time**: ~51 minutes
**Result**: Accessible, tested UI component with E2E tests

### Scenario 3: Feature with New Dependencies

**Issue**: "Add PDF export feature using PyPDF2"

**Workflow**:
```bash
@feature-implementer implement issue #234

# Phase 1: Analysis (~2 min)
# - Requirements: Export data to PDF
# - Security: Prevent PDF injection attacks
# - New dependency: PyPDF2

# Phase 2: Design (~7 min)
# - @documentation-researcher fetches PyPDF2 docs via context7-mcp
# - @dependency-manager checks PyPDF2 compatibility
# - Architecture: PDFExportService
# - Latest PyPDF2 best practices incorporated

# Phase 3: Approval
You: "Why PyPDF2 instead of ReportLab?"
Agent: "PyPDF2 is lighter and sufficient for this use case..."
You: "OK, proceed with PyPDF2"

# Phase 4: Implementation (~15 min)
# - Adds PyPDF2 to requirements.txt
# - Creates src/services/pdf_export.py
# - Follows PyPDF2 best practices from fetched docs
# - Creates tests/test_pdf_export.py

# Phase 5: Validation (~16 min)
# - All checks pass
# - Coverage: 84%

# Phase 6: Deployment (~6 min)
# - Documents PDF export feature
# - CHANGELOG mentions new PyPDF2 dependency
# - PR created with dependency update
```

**Key Benefit**: Latest library docs fetched automatically

### Scenario 4: Security-Critical Feature

**Issue**: "Implement password reset via email"

**Workflow**:
```bash
@feature-implementer implement issue #567

# Phase 1: Analysis (~3 min)
# - Requirements: Reset password, email link, expiry
# - Security: CRITICAL
#   - OWASP A07:2021 - Identification and Authentication Failures
#   - Token generation: Cryptographically secure
#   - Token expiry: 15 minutes
#   - Rate limiting: Prevent abuse
#   - Email validation: Prevent email enumeration

# Phase 2: Design (~8 min)
# - Token generation: secrets.token_urlsafe()
# - Database: Store hashed tokens with expiry
# - Rate limiting: 3 requests per IP per hour
# - Email: No user existence confirmation
# - @security-specialist provides OWASP guidance

# Phase 3: Approval
You: "Add 2FA requirement for password reset"
# Returns to Phase 2, adds 2FA to design
You: "Approved with 2FA"

# Phase 4: Implementation (~20 min)
# - Implements secure token generation
# - Adds rate limiting middleware
# - Implements 2FA verification
# - Time-constant comparison for tokens

# Phase 5: Validation (~22 min)
# - Security scan: Focus on auth vulnerabilities
# - Validates token generation is cryptographically secure
# - Tests rate limiting
# - Tests token expiry
# - Tests 2FA flow
# - All OWASP checks pass

# Phase 6: Deployment (~7 min)
# - Security-focused documentation
# - CHANGELOG highlights security feature
# - PR with security review checklist
```

**Total Time**: ~60 minutes
**Key Benefit**: Security validated at every phase

---

## Best Practices

### Writing Good GitHub Issues

The quality of your GitHub issue directly impacts implementation quality.

**Good Issue Example**:
```markdown
## Feature: User Profile Photo Upload

### Summary
Allow users to upload and display profile photos.

### Requirements
- User can upload photo via API
- Supported formats: JPG, PNG, WebP
- Max file size: 5MB
- Photo resized to 300x300px
- Stored in S3 with encryption
- Response time < 2 seconds

### Acceptance Criteria
- [ ] API endpoint accepts photo upload
- [ ] Invalid files rejected with clear error
- [ ] Photo stored securely in S3
- [ ] Photo URL returned in response
- [ ] Test coverage >= 80%
- [ ] Security scan passes

### Security Considerations
- Validate file type (not just extension)
- Check file size before processing
- Only user can upload own photo
- S3 bucket has encryption enabled

### Technical Notes
- Use Pillow for image processing
- Use boto3 for S3 operations
- Integrate with existing auth system
```

**Why This is Good**:
- Clear requirements
- Specific acceptance criteria
- Security considerations included
- Technical constraints specified
- Measurable success criteria

**Bad Issue Example**:
```markdown
## Add photo upload

Users should be able to upload photos.
```

**Why This is Bad**:
- Vague requirements
- No acceptance criteria
- No security considerations
- No technical context

### Reviewing Designs (Phase 3)

**What to Look For**:
1. **Architecture**:
   - Components have single responsibility
   - Dependencies are minimal
   - Extensible for future features

2. **Security**:
   - Input validation planned
   - Authentication/authorization considered
   - OWASP risks addressed

3. **Data Models**:
   - Fields are appropriate
   - Relationships make sense
   - Validations are sufficient

4. **APIs**:
   - Endpoints are RESTful/idiomatic
   - Error handling is clear
   - Response formats are consistent

5. **Dependencies**:
   - New dependencies justified
   - Versions compatible
   - No security vulnerabilities

**When to Request Changes**:
- Architecture violates project standards
- Security considerations insufficient
- Over-engineering or under-engineering
- Better alternative approach exists

**When to Approve**:
- Design aligns with requirements
- Security adequate
- Architecture is sound
- No major red flags

### Managing Validation Failures

If validation fails repeatedly:

**1. Review Validation Reports**:
```bash
# Check what's failing
tail -f logs/validation.log

# Common failures:
# - Test coverage below 80%
# - Type errors
# - Linting errors
# - Security vulnerabilities
```

**2. Understand the Issue**:
```
Agent: "Test coverage is 72%, below the 80% requirement"

# What to do:
# - Ask agent which modules need more tests
# - Review coverage report
# - Identify untested edge cases
```

**3. Let Recursive Validation Work**:
```
# Validation Orchestrator automatically:
# 1. Identifies failure
# 2. Asks implementation agent to fix
# 3. Re-runs validation
# 4. Repeats until pass

# You don't need to intervene unless stuck
```

**4. Manual Intervention (if stuck)**:
```
You: "Let's add tests for the error handling paths"
You: "Add type hints for the process_photo function"

# Agent will implement your suggestions
# Validation will re-run
```

### Optimizing for Speed

**Faster Analysis** (Phase 1):
- Write detailed GitHub issues
- Include security considerations upfront
- Specify tech stack in issue

**Faster Design** (Phase 2):
- Provide architectural preferences in issue
- Link to similar implementations
- Specify which libraries to use

**Faster Approval** (Phase 3):
- Review PRP document while it's being generated
- Use Plan Mode to explore design
- Prepare questions in advance

**Faster Implementation** (Phase 4):
- Cannot speed up (automatic)
- Quality over speed

**Faster Validation** (Phase 5):
- Write high-quality code in Phase 4
- Follow coding standards
- Address security proactively

**Faster Deployment** (Phase 6):
- Cannot speed up (automatic)

**Overall Tips**:
- Start with well-written GitHub issues
- Approve designs quickly if sound
- Let automation run without interruption

---

## Troubleshooting

### Issue: Agent Not Responding

**Symptom**:
```
@feature-implementer implement issue #123
[No response]
```

**Solutions**:
1. Check agent file exists:
   ```bash
   ls .claude/agents/feature-implementer.md
   ```

2. Verify correct syntax:
   ```bash
   @feature-implementer implement issue #123
   # Not: /feature-implementer or @feature-implement
   ```

3. Check for typos in agent name

4. Try alternative invocation:
   ```bash
   Please implement GitHub issue #123 using the feature-implementer agent
   ```

### Issue: Skills Not Activating

**Symptom**:
```
Agent proceeds without expected skills
```

**Solutions**:
1. Describe task clearly to trigger skills:
   ```
   Bad: "Do the thing"
   Good: "Analyze requirements, assess security, evaluate tech stack"
   ```

2. Check skills exist:
   ```bash
   ls .claude/skills/
   find .claude/skills -name "SKILL.md"
   ```

3. Verify skill descriptions match task:
   ```bash
   grep -r "security assessment" .claude/skills/
   ```

### Issue: Hooks Not Running

**Symptom**:
```
git commit -m "test"
[Commits without running quality checks]
```

**Solutions**:
1. Check hooks exist:
   ```bash
   ls .claude/hooks/*.py
   ```

2. Make hooks executable:
   ```bash
   chmod +x .claude/hooks/*.py
   ```

3. Verify settings.json:
   ```bash
   cat .claude/settings.json | jq .hooks
   ```

4. Check Python is available:
   ```bash
   which python3
   python3 --version
   ```

5. Test hook manually:
   ```bash
   echo '{"tool_name": "Bash", "tool_input": {"command": "git commit"}}' | .claude/hooks/pre-commit.py
   ```

### Issue: Design Approval Stuck

**Symptom**:
```
Agent presents design, waits indefinitely for approval
```

**Solutions**:
1. Explicitly approve:
   ```
   You: "The design is approved, please proceed with implementation"
   ```

2. Or request changes:
   ```
   You: "Please revise X, then re-present the design"
   ```

3. Don't be ambiguous:
   ```
   Bad: "Looks interesting"
   Good: "Approved" or "Please change X"
   ```

### Issue: Validation Failing Repeatedly

**Symptom**:
```
Phase 5: Validation keeps failing and retrying
```

**Solutions**:
1. Review failure message:
   ```
   Agent: "Test coverage is 78%, required ≥80%"
   ```

2. Check what's failing:
   ```bash
   # Run tests locally
   pytest --cov=src --cov-report=term-missing

   # Run quality checks
   black --check src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

3. Let agent fix automatically:
   ```
   # Recursive validation will keep trying
   # Agent learns from failures
   # Eventually fixes all issues
   ```

4. Manual intervention if stuck:
   ```
   You: "Add tests for the error handling in photo_processor.py"
   You: "Fix the type error on line 42"
   ```

### Issue: Token Costs Too High

**Symptom**:
```
Using unexpectedly high number of tokens
```

**Solutions**:
1. Check progressive disclosure working:
   ```
   # Only active skills should load
   # Not all 37 skills at once
   ```

2. Avoid loading unnecessary context:
   ```
   Bad: "Read all files, then implement"
   Good: "Implement feature using provided requirements"
   ```

3. Use appropriate models:
   ```
   # Haiku for simple tasks (cheaper)
   # Sonnet for medium tasks (balanced)
   # Opus for complex reasoning (expensive, only architecture phase)
   ```

4. Verify skills release context:
   ```
   # Skills should unload after task completes
   # Check conversation history isn't bloated
   ```

### Issue: E2E Tests Failing (Frontend)

**Symptom**:
```
Phase 5: E2E/Accessibility specialist reports failures
```

**Solutions**:
1. Verify Playwright is installed:
   ```bash
   npx playwright --version
   ```

2. Check browser drivers:
   ```bash
   npx playwright install
   ```

3. Run E2E tests locally:
   ```bash
   npx playwright test
   ```

4. Review E2E test code:
   ```bash
   cat tests/e2e/test-photo-upload.spec.ts
   ```

5. Update selectors if UI changed:
   ```
   You: "The button selector changed to #upload-btn"
   ```

---

## Advanced Usage

### Customizing Workflows

**Modify Agent Prompts**:
```bash
# Edit main orchestrator
vim .claude/agents/feature-implementer.md

# Example: Add extra validation step
# Add after Phase 5: "Run performance benchmarks"
```

**Modify Skills**:
```bash
# Edit implementation skill
vim .claude/skills/implementation/SKILL.md

# Example: Add company-specific coding standards
# Add custom file size limits
# Add language-specific conventions
```

**Modify Hooks**:
```bash
# Edit pre-commit hook
vim .claude/hooks/pre-commit.py

# Example: Add custom check
def check_no_todos(project_dir: str) -> Optional[str]:
    # Fail if code contains TODO comments
    pass
```

### Creating Custom Specialists

**Example: Add Performance Specialist**:

1. **Create Agent**:
```bash
# Create new agent file
vim .claude/agents/performance-specialist.md
```

```markdown
# Performance Specialist

**Model**: haiku
**Role**: Analyze and optimize code performance
**When to Use**: After implementation, before validation

## Auto-Activated Skills
- performance-profiler
- benchmark-runner
- optimization-suggester

## Responsibilities
1. Profile code execution
2. Identify bottlenecks
3. Suggest optimizations
4. Run performance benchmarks
5. Ensure performance targets met
```

2. **Create Skills**:
```bash
mkdir -p .claude/skills/performance-profiler
vim .claude/skills/performance-profiler/SKILL.md
```

3. **Integrate into Workflow**:
```bash
# Edit feature-implementer.md
# Add to Phase 5: "Invoke @performance-specialist"
```

### Multi-Project Configuration

**Global Skills** (shared across projects):
```bash
# Create global skill
mkdir -p ~/.claude/skills/company-standards
vim ~/.claude/skills/company-standards/SKILL.md

# This skill auto-activates for all projects
```

**Project-Specific Skills** (override global):
```bash
# Create project skill with same name
mkdir -p .claude/skills/company-standards
vim .claude/skills/company-standards/SKILL.md

# Project-specific skill takes precedence
```

**Scope Precedence**:
```
Local (.claude/settings.local.json)
  > Project (.claude/)
    > Global (~/.claude/)
```

### Parallel Feature Development

**Scenario**: Multiple features in parallel

**Approach 1: Separate Branches**:
```bash
# Feature A
git checkout -b feature/photo-upload
@feature-implementer implement issue #123

# Feature B (in another terminal/tab)
git checkout -b feature/pdf-export
@feature-implementer implement issue #124

# Both workflows run independently
```

**Approach 2: Sequential**:
```bash
# Complete Feature A
@feature-implementer implement issue #123
# Wait for completion...

# Then Feature B
@feature-implementer implement issue #124
```

**Best Practice**: One feature at a time per workspace for clarity

### Integration with CI/CD

**GitHub Actions Example**:
```yaml
# .github/workflows/feature-implementer.yml
name: Feature Implementation

on:
  issues:
    types: [labeled]

jobs:
  implement:
    if: github.event.label.name == 'auto-implement'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Feature Implementer
        run: |
          # Invoke Claude Code API (if available)
          # Or use this workflow as trigger for manual implementation
```

**Pre-commit in CI**:
```yaml
# .github/workflows/quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Quality Checks
        run: |
          # Same checks as pre-commit hook
          black --check src/ tests/
          flake8 src/ tests/
          mypy src/
          pytest --cov=src --cov-report=term
```

### Metrics and Monitoring

**Track Agent Performance**:
```bash
# Count agent invocations
grep -r "@feature-implementer" .claude/logs/ | wc -l

# Measure average implementation time
# (Extract timestamps from logs)

# Track validation success rate
grep -A 10 "Phase 5: Validation" .claude/logs/ | grep "✅ All checks passed"
```

**Token Usage**:
```bash
# Log token usage per phase
# (Requires custom instrumentation)

# Expected ranges (v2):
# Phase 1: ~500 tokens
# Phase 2: ~2,000 tokens
# Phase 3: ~100 tokens
# Phase 4: ~5,000 tokens
# Phase 5: ~3,000 tokens
# Phase 6: ~1,000 tokens
# Total: ~11,600 tokens (vs 124,000 in v1)
```

---

## Conclusion

The **Feature-Implementer v2 Architecture** provides a production-ready, multi-agent system for implementing features with:

✅ Automated analysis and design
✅ User approval checkpoint
✅ TDD implementation
✅ Comprehensive validation
✅ Automated deployment
✅ 99.76% token efficiency gain
✅ Quality enforcement via hooks

### Next Steps

1. **Try it**: Implement a simple feature
2. **Customize**: Adjust agents/skills for your project
3. **Integrate**: Add to your team's workflow
4. **Share feedback**: Report issues and suggestions

### Resources

- **Architecture**: [feature-implementer-v2.md](../architecture/feature-implementer-v2.md)
- **Migration Guide**: [migration-guide-v1-to-v2.md](../architecture/migration-guide-v1-to-v2.md)
- **Skills Mapping**: [skills-mapping.md](../architecture/skills-mapping.md)
- **GitHub Issues**: https://github.com/matteocervelli/llms/issues

---

**Version**: 1.0.0
**Last Updated**: 2025-10-29
**Status**: Production Ready

**Prepared by**: Feature-Implementer v2 Architecture Team
