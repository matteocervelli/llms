---
name: validation-workflow
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Validation Workflow Guide

This guide provides detailed procedures for managing the validation workflow, including specialist invocation, dependency resolution, and status tracking.

## Workflow Overview

The validation workflow consists of **5-6 sequential phases**, each coordinated by a specialist agent:

```
Phase 1: Unit Test Writing
  └─→ @unit-test-specialist
       └─→ Output: Unit test files in /tests/

Phase 2: Integration Test Writing
  └─→ @integration-test-specialist
       └─→ Output: Integration test files in /tests/integration/

Phase 3: Test Execution
  └─→ @test-runner-specialist
       └─→ Output: Test results + coverage report
       └─→ Recursive Loop: IF fail → main agent fix → re-run

Phase 4: Code Quality
  └─→ @code-quality-specialist
       └─→ Output: Linting, typing, formatting results
       └─→ Recursive Loop: IF fail → main agent fix → re-check

Phase 5: Security Assessment
  └─→ @security-specialist
       └─→ Output: Security scan + OWASP compliance
       └─→ Recursive Loop: IF fail → main agent fix → re-scan

Phase 6: E2E & Accessibility (Frontend Only)
  └─→ @e2e-accessibility-specialist
       └─→ Output: E2E test results + WCAG compliance
       └─→ Recursive Loop: IF fail → main agent fix → re-test

Result: All validations pass → Ready for Deployment
```

## Phase 1: Unit Test Writing

**Specialist**: @unit-test-specialist
**Model**: Haiku
**Objective**: Write comprehensive unit tests for all public functions and classes

### Invocation

```markdown
**Prerequisites**:
- ✅ PRP document available
- ✅ Implementation files identified
- ✅ Technology stack known (for test framework selection)

**Invocation Command**:
@unit-test-specialist write unit tests for feature #{issue-number}
PRP: /docs/implementation/prp/feature-{issue-number}-prp.md
Implementation files: [list]
Technology stack: [Python/TypeScript/Swift/etc.]

**Expected Inputs**:
- PRP document path
- List of implementation file paths
- Technology stack (determines test framework)

**Expected Outputs**:
- Unit test files in /tests/ directory
- Test naming: test_feature_{issue-number}.py (Python) or test-feature-{issue-number}.test.ts (TypeScript)
- Tests for all public functions/classes
- Edge case coverage
- Mocked external dependencies
- Test fixtures and data

**Success Criteria**:
- ✅ All public functions have unit tests
- ✅ All classes have unit tests
- ✅ Edge cases covered (null, empty, boundary values)
- ✅ External dependencies mocked
- ✅ Test fixtures created for complex data
```

### Status Tracking

```markdown
**Unit Test Specialist Status**:
- Status: In Progress → Completed
- Iteration: 1/1 (typically completes in one iteration)
- Output Files: /tests/test_feature_{issue-number}.py
- Tests Written: [Count]
- Completion Time: ~5-10 minutes
```

### Proceed to Phase 2

```markdown
IF unit tests successfully written:
  ✅ Mark Phase 1 complete
  ✅ Update validation checklist
  ✅ Proceed to Phase 2: Integration Test Writing
ELSE:
  ⚠️ Specialist failed (rare - usually succeeds)
  ⚠️ Trigger recursive communication
  ⚠️ Wait for main agent to address issue
```

---

## Phase 2: Integration Test Writing

**Specialist**: @integration-test-specialist
**Model**: Haiku
**Objective**: Write integration tests for component interactions

### Invocation

```markdown
**Prerequisites**:
- ✅ Phase 1 complete (unit tests written)
- ✅ PRP document available
- ✅ Implementation files identified
- ✅ Unit test files available (for reference)

**Invocation Command**:
@integration-test-specialist write integration tests for feature #{issue-number}
PRP: /docs/implementation/prp/feature-{issue-number}-prp.md
Implementation files: [list]
Unit tests: /tests/test_feature_{issue-number}.py
Technology stack: [Python/TypeScript/Swift/etc.]

**Expected Inputs**:
- PRP document path
- List of implementation file paths
- Unit test file paths (for reference)
- Technology stack

**Expected Outputs**:
- Integration test files in /tests/integration/ directory
- Test naming: test_feature_{issue-number}_integration.py
- Tests for component interactions
- Database integration tests (if applicable)
- API integration tests (if applicable)
- Service interaction tests
- Cross-component workflow tests

**Success Criteria**:
- ✅ All component interactions tested
- ✅ Database operations tested (if applicable)
- ✅ API calls tested (if applicable)
- ✅ Service integrations verified
- ✅ End-to-end workflows covered
```

### Status Tracking

```markdown
**Integration Test Specialist Status**:
- Status: In Progress → Completed
- Iteration: 1/1 (typically completes in one iteration)
- Output Files: /tests/integration/test_feature_{issue-number}_integration.py
- Tests Written: [Count]
- Completion Time: ~5-10 minutes
```

### Proceed to Phase 3

```markdown
IF integration tests successfully written:
  ✅ Mark Phase 2 complete
  ✅ Update validation checklist
  ✅ Proceed to Phase 3: Test Execution
ELSE:
  ⚠️ Specialist failed (rare - usually succeeds)
  ⚠️ Trigger recursive communication
  ⚠️ Wait for main agent to address issue
```

---

## Phase 3: Test Execution (WITH RECURSIVE LOOP)

**Specialist**: @test-runner-specialist
**Model**: Haiku
**Objective**: Execute all tests and verify ≥80% code coverage

### Invocation

```markdown
**Prerequisites**:
- ✅ Phase 1 complete (unit tests written)
- ✅ Phase 2 complete (integration tests written)
- ✅ Implementation files available
- ✅ Test framework installed

**Invocation Command**:
@test-runner-specialist run tests for feature #{issue-number}
Unit tests: /tests/test_feature_{issue-number}.py
Integration tests: /tests/integration/test_feature_{issue-number}_integration.py
Implementation files: [list]
Coverage target: ≥80%
Technology stack: [Python/TypeScript/Swift/etc.]

**Expected Inputs**:
- Unit test file paths
- Integration test file paths
- Implementation file paths (for coverage calculation)
- Coverage target (default: 80%)
- Technology stack (determines test runner: pytest, jest, XCTest, etc.)

**Expected Outputs**:
- Test execution results (pass/fail for each test)
- Code coverage report (percentage, lines covered/total)
- Test documentation at /docs/implementation/tests/feature-{issue-number}-tests.md
- Coverage visualization (if applicable)

**Success Criteria**:
- ✅ All tests pass (100% pass rate)
- ✅ Code coverage ≥80% (or specified target)
- ✅ Test documentation generated
- ✅ No test errors or warnings
```

### Recursive Loop (Critical)

```markdown
**Test Execution Result**:

IF all tests pass AND coverage ≥80%:
  ✅ Mark Phase 3 complete
  ✅ Update validation checklist
  ✅ Log success (iteration count, coverage %)
  ✅ Proceed to Phase 4: Code Quality

ELSE (tests fail OR coverage <80%):
  ⚠️ RECURSIVE LOOP INITIATED

  **Iteration 1**:
  1. Log failure details (which tests failed, coverage %, error messages)
  2. Trigger recursive-communicator skill
  3. Format failure report for main agent:
     - Failed tests with error messages
     - Coverage percentage and missing lines
     - Suggested fixes (from test error analysis)
  4. Send failure report to @feature-implementer-main
  5. Wait for main agent to fix implementation
  6. Main agent signals completion

  **Iteration 2**:
  7. Re-invoke @test-runner-specialist
  8. Re-run tests with updated implementation
  9. Check result:
     - IF pass + coverage ≥80%: Exit loop, proceed to Phase 4
     - IF still fail: Increment iteration, repeat steps 1-6

  **Iteration 3, 4, 5**: Same as Iteration 2

  **Max Iterations**: 5
  IF iteration > 5:
    ⛔ Escalate to main orchestrator with "unresolvable" flag
    ⛔ Require user intervention
    ⛔ Halt validation workflow
```

### Status Tracking (Recursive Loop Example)

```markdown
**Test Runner Specialist Status** (Iteration 2 of 5):
- Status: Failed → Awaiting Fix → Re-running
- Current Iteration: 2/5
- Test Results:
  - Total Tests: 57 (45 unit + 12 integration)
  - Passed: 54
  - Failed: 3
    - test_validation_coordinator.py::test_sequential_invocation - AssertionError
    - test_validation_coordinator.py::test_failure_tracking - KeyError
    - test_validation_coordinator.py::test_workflow_completion - AttributeError
- Coverage: 73.2% (target: ≥80%)
- Missing Coverage: Lines 45-52, 103-110 in validation_coordinator.py
- Action: Recursive communication sent to main agent
- Awaiting: Main agent fix + re-run signal

**Recursive Communication Log**:
- Iteration 1: Test failures detected → Failure report sent to main agent → Awaiting fix
- (Current) Iteration 2: Main agent fixed issues → Re-running tests...
```

### Proceed to Phase 4

```markdown
IF all tests pass AND coverage ≥80% (after recursive loop completes):
  ✅ Mark Phase 3 complete
  ✅ Update validation checklist
  ✅ Log final iteration count (e.g., "3/5 iterations required")
  ✅ Proceed to Phase 4: Code Quality
```

---

## Phase 4: Code Quality (WITH RECURSIVE LOOP)

**Specialist**: @code-quality-specialist
**Model**: Haiku
**Objective**: Run linters, type checkers, and formatters

### Invocation

```markdown
**Prerequisites**:
- ✅ Phase 3 complete (all tests pass, coverage ≥80%)
- ✅ Implementation files available
- ✅ Technology stack known (for tool selection)

**Invocation Command**:
@code-quality-specialist check code quality for feature #{issue-number}
Implementation files: [list]
Technology stack: [Python/TypeScript/Swift/etc.]

**Expected Inputs**:
- Implementation file paths
- Technology stack (determines tools)

**Tool Selection by Stack**:
- **Python**: Black (formatting), mypy (type checking), flake8 (linting)
- **TypeScript**: ESLint (linting), Prettier (formatting), tsc --noEmit (type checking)
- **Swift**: SwiftLint (linting), SwiftFormat (formatting)

**Expected Outputs**:
- Linting results (errors, warnings, file-by-file)
- Type checking results (type errors, file locations)
- Formatting violations (lines needing formatting)
- Code quality score/summary
- Quality report at /docs/implementation/quality/feature-{issue-number}-quality.md

**Success Criteria**:
- ✅ Zero linting errors (warnings acceptable)
- ✅ Zero type errors
- ✅ Code properly formatted (no formatting violations)
- ✅ Quality report generated
```

### Recursive Loop

```markdown
**Code Quality Check Result**:

IF no linting errors AND no type errors AND formatting compliant:
  ✅ Mark Phase 4 complete
  ✅ Update validation checklist
  ✅ Log success
  ✅ Proceed to Phase 5: Security

ELSE (linting errors OR type errors OR formatting violations):
  ⚠️ RECURSIVE LOOP INITIATED

  **Iteration 1**:
  1. Log quality issues (linting errors, type errors, formatting violations)
  2. Trigger recursive-communicator skill
  3. Format quality report for main agent:
     - Linting errors with file locations and line numbers
     - Type errors with explanations
     - Formatting violations (can often auto-fix)
     - Suggested fixes
  4. Send quality report to @feature-implementer-main
  5. Wait for main agent to fix code quality issues
  6. Main agent signals completion

  **Iteration 2+**:
  7. Re-invoke @code-quality-specialist
  8. Re-run quality checks
  9. Check result:
     - IF all pass: Exit loop, proceed to Phase 5
     - IF still fail: Increment iteration, repeat steps 1-6

  **Max Iterations**: 5
  IF iteration > 5:
    ⛔ Escalate to main orchestrator
```

### Proceed to Phase 5

```markdown
IF all quality checks pass (after recursive loop completes):
  ✅ Mark Phase 4 complete
  ✅ Update validation checklist
  ✅ Proceed to Phase 5: Security
```

---

## Phase 5: Security Assessment (WITH RECURSIVE LOOP)

**Specialist**: @security-specialist
**Model**: Haiku (with security knowledge)
**Objective**: Run security scans and verify OWASP Top 10 compliance

### Invocation

```markdown
**Prerequisites**:
- ✅ Phase 4 complete (code quality checks pass)
- ✅ Implementation files available
- ✅ PRP security requirements available

**Invocation Command**:
@security-specialist assess security for feature #{issue-number}
Implementation files: [list]
Security requirements: [from PRP]
OWASP Top 10: https://owasp.org/Top10/

**Expected Inputs**:
- Implementation file paths
- PRP security requirements
- Technology stack (for security tool selection)

**Security Checks**:
1. Input validation (SQL injection, XSS, command injection)
2. Authentication & authorization (access controls)
3. Sensitive data handling (encryption, secure storage, no hardcoded secrets)
4. Error handling (no information leakage)
5. Dependencies (known vulnerabilities, CVEs)
6. OWASP Top 10 compliance

**Expected Outputs**:
- Security scan results
- Vulnerability report (CVEs, severities: Critical, High, Medium, Low)
- OWASP Top 10 compliance checklist
- Recommendations for fixes
- Security report at /docs/implementation/security/feature-{issue-number}-security.md

**Success Criteria**:
- ✅ Zero critical vulnerabilities
- ✅ Zero high vulnerabilities
- ✅ OWASP Top 10 compliant
- ✅ No hardcoded secrets
- ✅ Proper input validation
- ✅ Secure sensitive data handling
```

### Recursive Loop

```markdown
**Security Scan Result**:

IF no vulnerabilities AND OWASP compliant:
  ✅ Mark Phase 5 complete
  ✅ Update validation checklist
  ✅ Log success
  ✅ IF frontend: Proceed to Phase 6: E2E & Accessibility
  ✅ IF backend: All validations complete

ELSE (vulnerabilities found OR OWASP violations):
  ⚠️ RECURSIVE LOOP INITIATED

  **Iteration 1**:
  1. Log security issues (vulnerabilities, OWASP violations)
  2. Trigger recursive-communicator skill
  3. Format security report for main agent:
     - Vulnerabilities with severity (Critical/High/Medium/Low)
     - OWASP Top 10 violations
     - File locations and line numbers
     - Suggested fixes and remediation steps
  4. Send security report to @feature-implementer-main
  5. Wait for main agent to fix security issues
  6. Main agent signals completion

  **Iteration 2+**:
  7. Re-invoke @security-specialist
  8. Re-run security scan
  9. Check result:
     - IF no vulnerabilities + OWASP compliant: Exit loop, proceed to next phase
     - IF vulnerabilities remain: Increment iteration, repeat steps 1-6

  **Max Iterations**: 5
  IF iteration > 5:
    ⛔ Escalate to main orchestrator (security issues critical)
```

### Proceed to Phase 6 or Complete

```markdown
IF security scan clean AND OWASP compliant (after recursive loop):
  ✅ Mark Phase 5 complete
  ✅ Update validation checklist

  **Determine Next Phase**:
  IF frontend components exist (from PRP):
    ✅ Proceed to Phase 6: E2E & Accessibility
  ELSE (backend only):
    ✅ ALL VALIDATIONS COMPLETE
    ✅ Generate final validation report
    ✅ Return to orchestrator
```

---

## Phase 6: E2E & Accessibility (FRONTEND ONLY, WITH RECURSIVE LOOP)

**Specialist**: @e2e-accessibility-specialist
**Model**: Haiku
**Objective**: Run E2E tests and verify WCAG 2.1 AA compliance

### Invocation

```markdown
**Prerequisites**:
- ✅ Phase 5 complete (security scan clean)
- ✅ Frontend components identified (from PRP)
- ✅ User flows defined (from PRP)

**Invocation Command**:
@e2e-accessibility-specialist test e2e and accessibility for feature #{issue-number}
Frontend files: [list from PRP]
User flows: [from PRP - e.g., "User registration", "Form submission"]
WCAG level: 2.1 AA

**Expected Inputs**:
- Frontend file paths
- User flows to test
- WCAG compliance level (default: 2.1 AA)

**E2E Testing**:
- User flow tests (critical paths)
- Cross-browser compatibility (Chrome, Firefox, Safari)
- Responsive design tests (mobile, tablet, desktop)
- Form submission and validation
- Navigation and routing

**Accessibility Testing** (WCAG 2.1 AA):
- Perceivable: Text alternatives, captions, adaptable content
- Operable: Keyboard accessible, enough time, navigable
- Understandable: Readable, predictable, input assistance
- Robust: Compatible with assistive technologies

**Expected Outputs**:
- E2E test results (pass/fail per user flow)
- Accessibility audit report
- WCAG compliance checklist
- Browser compatibility matrix
- E2E report at /docs/implementation/e2e/feature-{issue-number}-e2e.md

**Success Criteria**:
- ✅ All user flows pass E2E tests
- ✅ Cross-browser compatibility verified
- ✅ Responsive design works on all devices
- ✅ WCAG 2.1 AA compliant (100%)
- ✅ E2E report generated
```

### Recursive Loop

```markdown
**E2E & Accessibility Result**:

IF all E2E tests pass AND WCAG 2.1 AA compliant:
  ✅ Mark Phase 6 complete
  ✅ Update validation checklist
  ✅ Log success
  ✅ ALL VALIDATIONS COMPLETE

ELSE (E2E failures OR accessibility violations):
  ⚠️ RECURSIVE LOOP INITIATED

  **Iteration 1**:
  1. Log E2E failures and accessibility violations
  2. Trigger recursive-communicator skill
  3. Format E2E/accessibility report for main agent:
     - Failed user flows with error details
     - Accessibility violations with WCAG criteria references
     - File locations and line numbers
     - Suggested fixes
  4. Send report to @feature-implementer-main
  5. Wait for main agent to fix issues
  6. Main agent signals completion

  **Iteration 2+**:
  7. Re-invoke @e2e-accessibility-specialist
  8. Re-run E2E tests and accessibility scan
  9. Check result:
     - IF all pass + WCAG compliant: Exit loop, complete validation
     - IF still fail: Increment iteration, repeat steps 1-6

  **Max Iterations**: 5
  IF iteration > 5:
    ⛔ Escalate to main orchestrator
```

### Complete Validation

```markdown
IF all E2E tests pass AND WCAG 2.1 AA compliant (after recursive loop):
  ✅ Mark Phase 6 complete
  ✅ Update validation checklist
  ✅ ALL VALIDATIONS COMPLETE
  ✅ Generate final validation report
  ✅ Return to orchestrator
```

---

## Workflow Completion

After all phases complete successfully:

```markdown
### Final Validation Status

**All Phases Complete**:
- ✅ Phase 1: Unit tests written (45 tests)
- ✅ Phase 2: Integration tests written (12 tests)
- ✅ Phase 3: All tests pass, coverage 87.3% (3 iterations)
- ✅ Phase 4: Code quality checks pass (1 iteration)
- ✅ Phase 5: Security scan clean, OWASP compliant (2 iterations)
- ✅ Phase 6: E2E tests pass, WCAG 2.1 AA compliant (1 iteration) [or N/A if backend]

**Total Validation Statistics**:
- Total Specialists: 5 (or 6 with E2E)
- Total Iterations: 7 (across all specialists)
- Total Time: 00:42:15
- Recursive Fix Cycles: 3

**Quality Gates Achieved**:
- ✅ Unit tests: 45 tests, 100% pass
- ✅ Integration tests: 12 tests, 100% pass
- ✅ Coverage: 87.3% (target: ≥80%)
- ✅ Linting: Zero errors
- ✅ Type checking: Zero errors
- ✅ Formatting: Compliant
- ✅ Security: Zero vulnerabilities
- ✅ OWASP Top 10: Compliant
- ✅ E2E tests: All pass [if applicable]
- ✅ WCAG 2.1 AA: Compliant [if applicable]

**Validation Documentation**:
- /docs/implementation/tests/feature-{issue-number}-tests.md
- /docs/implementation/quality/feature-{issue-number}-quality.md
- /docs/implementation/security/feature-{issue-number}-security.md
- /docs/implementation/e2e/feature-{issue-number}-e2e.md [if applicable]

**Final Status**: ✅ ALL VALIDATIONS PASSED
**Deployment Readiness**: ✅ READY FOR PHASE 6 (Deployment)

**Action**: Generate final validation report and return to main orchestrator
```

---

## Workflow Error Handling

### Specialist Failure

```markdown
IF specialist fails unexpectedly (not validation failure, but specialist itself errors):
  1. Log specialist error with full context
  2. Attempt re-invocation (1 retry)
  3. IF retry fails:
     a. Trigger recursive-communicator
     b. Report specialist failure to main orchestrator
     c. Include: specialist name, error message, context
     d. Await main orchestrator decision (debug, skip, abort)
```

### Deadlock Detection

```markdown
IF specialist takes > 30 minutes without response:
  1. Log timeout event
  2. Attempt graceful specialist termination
  3. Trigger recursive-communicator
  4. Report timeout to main orchestrator
  5. Await main orchestrator decision (retry, skip, abort)
```

### Max Iterations Exceeded

```markdown
IF any specialist exceeds max iterations (5):
  1. Log max iterations exceeded
  2. Trigger recursive-communicator
  3. Report to main orchestrator with "unresolvable" flag
  4. Include:
     - Specialist name
     - Total iterations attempted
     - Persistent failures across iterations
     - Suggested escalation (user intervention, skip validation, abort)
  5. Await main orchestrator decision
```

---

## Version Control Integration

### Pre-Validation State

```markdown
Before starting validation:
1. Capture current git state
2. Log current commit SHA
3. Note which files will be validated
```

### Post-Validation State

```markdown
After validation completes:
1. Validation tests added to repository
2. Validation reports committed
3. Implementation fixes (from recursive loops) committed
4. Git state clean and ready for deployment
```

---

**Version**: 2.0.0
**Created**: 2025-10-29
**Updated**: 2025-10-29
