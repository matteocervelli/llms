# Validation Checklist

Comprehensive quality gate checklist for validation workflow. Use this checklist to track validation progress and ensure all quality standards are met before deployment.

## Overall Validation Status

```markdown
**Issue**: #{issue-number}
**Feature**: [Feature Name]
**Technology Stack**: [Python, TypeScript, Swift, etc.]
**Frontend**: [Yes/No]
**Validation Started**: [YYYY-MM-DD HH:MM:SS]
**Validation Completed**: [YYYY-MM-DD HH:MM:SS] or [In Progress]
**Total Time**: [HH:MM:SS]
**Overall Status**: [Pending / In Progress / Passed / Failed]
```

---

## Phase 1: Unit Test Writing

### Checklist

- [ ] **Unit Test Specialist Invoked**: @unit-test-specialist called with correct inputs
- [ ] **PRP Loaded**: Product Requirements Prompt read and parsed
- [ ] **Implementation Files Identified**: All files requiring tests identified
- [ ] **Test Files Created**: Unit test files created in /tests/ directory
- [ ] **Test Naming Convention**: Files named correctly (test_feature_{issue-number}.py)
- [ ] **All Functions Tested**: Every public function has corresponding unit test
- [ ] **All Classes Tested**: Every class has unit tests for public methods
- [ ] **Edge Cases Covered**: Null, empty, boundary values tested
- [ ] **External Dependencies Mocked**: All external calls/services mocked
- [ ] **Test Fixtures Created**: Test data and fixtures defined
- [ ] **Test Documentation**: Tests are well-documented with docstrings

### Quality Standards

- **Minimum Tests**: At least 1 test per public function/method
- **Edge Case Coverage**: Minimum 3 edge cases per function (null, empty, boundary)
- **Mock Usage**: All external dependencies (DB, API, filesystem) mocked
- **Fixture Quality**: Reusable fixtures for common test data

### Specialist Output

```markdown
**Specialist**: @unit-test-specialist
**Status**: [Pending / In Progress / Completed / Failed]
**Iteration**: [Current / Max]
**Tests Created**: [Count]
**Files Created**: [List of test file paths]
**Completion Time**: [MM:SS]
```

---

## Phase 2: Integration Test Writing

### Checklist

- [ ] **Integration Test Specialist Invoked**: @integration-test-specialist called
- [ ] **Unit Tests Available**: Phase 1 complete, unit tests written
- [ ] **Component Interactions Identified**: Components that interact identified
- [ ] **Test Files Created**: Integration test files in /tests/integration/ directory
- [ ] **Test Naming Convention**: Files named correctly (test_feature_{issue-number}_integration.py)
- [ ] **Component Interaction Tests**: Tests for component-to-component calls
- [ ] **Database Integration Tests**: DB operations tested (if applicable)
- [ ] **API Integration Tests**: API calls tested (if applicable)
- [ ] **Service Integration Tests**: External service interactions tested
- [ ] **Workflow Tests**: End-to-end component workflows tested
- [ ] **Test Isolation**: Integration tests don't interfere with each other

### Quality Standards

- **Minimum Tests**: At least 1 integration test per component interaction
- **Database Tests**: All CRUD operations tested (if DB used)
- **API Tests**: All API calls tested with mocked responses
- **Workflow Coverage**: All critical workflows have integration tests

### Specialist Output

```markdown
**Specialist**: @integration-test-specialist
**Status**: [Pending / In Progress / Completed / Failed]
**Iteration**: [Current / Max]
**Tests Created**: [Count]
**Files Created**: [List of integration test file paths]
**Completion Time**: [MM:SS]
```

---

## Phase 3: Test Execution & Coverage

### Checklist

#### Test Execution
- [ ] **Test Runner Specialist Invoked**: @test-runner-specialist called
- [ ] **All Tests Available**: Unit and integration tests written
- [ ] **Test Framework Configured**: pytest, jest, XCTest, etc. set up
- [ ] **Tests Executed**: All tests run successfully
- [ ] **Unit Tests Pass**: 100% pass rate for unit tests
- [ ] **Integration Tests Pass**: 100% pass rate for integration tests
- [ ] **No Test Errors**: Zero errors during test execution
- [ ] **No Test Warnings**: Zero warnings during test execution

#### Code Coverage
- [ ] **Coverage Calculated**: Code coverage percentage computed
- [ ] **Coverage ≥80%**: Meets or exceeds 80% coverage target
- [ ] **Coverage Report Generated**: HTML/terminal coverage report available
- [ ] **Uncovered Lines Identified**: Missing coverage lines documented
- [ ] **Critical Paths Covered**: All critical code paths tested
- [ ] **Edge Cases Covered**: Edge cases included in coverage

#### Test Documentation
- [ ] **Test Report Generated**: /docs/implementation/tests/feature-{issue-number}-tests.md
- [ ] **Test Statistics Documented**: Pass/fail counts, coverage %, runtime
- [ ] **Failed Tests Documented**: Failures logged with error messages (if any)
- [ ] **Coverage Gaps Documented**: Uncovered lines identified (if any)

### Quality Standards

- **Pass Rate**: 100% (all tests must pass)
- **Coverage Target**: ≥80% (configurable, default 80%)
- **Test Runtime**: <5 minutes for unit tests, <10 minutes for integration tests
- **Zero Flaky Tests**: All tests deterministic and repeatable

### Specialist Output

```markdown
**Specialist**: @test-runner-specialist
**Status**: [Pending / In Progress / Completed / Failed]
**Iteration**: [Current / Max]
**Total Tests**: [Count]
**Passed**: [Count]
**Failed**: [Count]
**Coverage**: [XX.X%]
**Target**: [≥80%]
**Test Report**: /docs/implementation/tests/feature-{issue-number}-tests.md
**Completion Time**: [MM:SS]
```

### Recursive Communication (If Failures)

```markdown
**Test Failures Detected**:
- [ ] Failure details logged (test names, error messages, file locations)
- [ ] Recursive communication triggered
- [ ] Failure report sent to @feature-implementer-main
- [ ] Awaiting main agent fix
- [ ] Fix completed, re-running tests
- [ ] Iteration count: [Current / Max (5)]
```

---

## Phase 4: Code Quality

### Checklist

#### Linting
- [ ] **Linter Configured**: Tool selected based on tech stack (flake8, ESLint, SwiftLint)
- [ ] **Linter Executed**: Linter run on all implementation files
- [ ] **Zero Linting Errors**: No errors reported
- [ ] **Warnings Reviewed**: Warnings documented (if any)
- [ ] **Linting Report Generated**: Results documented in quality report

#### Type Checking
- [ ] **Type Checker Configured**: Tool selected (mypy, tsc, etc.)
- [ ] **Type Checker Executed**: Type checking run on all files
- [ ] **Zero Type Errors**: No type errors reported
- [ ] **Type Hints Present**: All functions have type hints
- [ ] **Type Checking Report Generated**: Results documented

#### Code Formatting
- [ ] **Formatter Configured**: Tool selected (Black, Prettier, SwiftFormat)
- [ ] **Formatter Executed**: Formatting check run on all files
- [ ] **Zero Formatting Violations**: All files properly formatted
- [ ] **Consistent Style**: Code follows project style guide
- [ ] **Formatting Report Generated**: Results documented

#### Code Quality Report
- [ ] **Quality Report Generated**: /docs/implementation/quality/feature-{issue-number}-quality.md
- [ ] **All Results Documented**: Linting, type checking, formatting results
- [ ] **Quality Score Calculated**: Overall code quality score (if applicable)

### Quality Standards

- **Linting**: Zero errors (warnings acceptable with justification)
- **Type Coverage**: 100% type hints for public functions
- **Formatting**: 100% compliant with project formatter
- **Consistency**: Code follows established patterns in codebase

### Specialist Output

```markdown
**Specialist**: @code-quality-specialist
**Status**: [Pending / In Progress / Completed / Failed]
**Iteration**: [Current / Max]

**Linting Results**:
- Errors: [Count]
- Warnings: [Count]
- Tool: [flake8/ESLint/SwiftLint]

**Type Checking Results**:
- Type Errors: [Count]
- Tool: [mypy/tsc]

**Formatting Results**:
- Violations: [Count]
- Tool: [Black/Prettier/SwiftFormat]

**Quality Report**: /docs/implementation/quality/feature-{issue-number}-quality.md
**Completion Time**: [MM:SS]
```

### Recursive Communication (If Failures)

```markdown
**Code Quality Issues Detected**:
- [ ] Issues logged (linting errors, type errors, formatting violations)
- [ ] Recursive communication triggered
- [ ] Quality report sent to @feature-implementer-main
- [ ] Awaiting main agent fix
- [ ] Fix completed, re-running quality checks
- [ ] Iteration count: [Current / Max (5)]
```

---

## Phase 5: Security Assessment

### Checklist

#### Input Validation
- [ ] **SQL Injection Prevention**: All SQL queries parameterized
- [ ] **XSS Prevention**: All user inputs sanitized for display
- [ ] **Command Injection Prevention**: No shell commands with user input
- [ ] **Path Traversal Prevention**: File paths validated
- [ ] **Input Validation**: All inputs validated against expected types/patterns

#### Authentication & Authorization
- [ ] **Authentication Required**: Protected endpoints require authentication
- [ ] **Authorization Checks**: Proper access control on sensitive operations
- [ ] **Session Management**: Secure session handling (if applicable)
- [ ] **Password Security**: Passwords hashed with strong algorithm (if applicable)
- [ ] **Token Security**: Tokens securely generated and validated (if applicable)

#### Sensitive Data Handling
- [ ] **No Hardcoded Secrets**: API keys, passwords not in code
- [ ] **Encryption**: Sensitive data encrypted at rest and in transit
- [ ] **Secure Storage**: Credentials stored in secure vaults/environment variables
- [ ] **Data Minimization**: Only necessary data collected and stored
- [ ] **PII Handling**: Personal data handled according to regulations (GDPR, etc.)

#### Error Handling
- [ ] **No Information Leakage**: Error messages don't reveal system details
- [ ] **Graceful Failures**: Errors handled gracefully without crashes
- [ ] **Logging Security**: Sensitive data not logged
- [ ] **Stack Traces**: Stack traces not exposed to users

#### Dependency Security
- [ ] **Dependency Scan**: All dependencies scanned for vulnerabilities
- [ ] **Known CVEs**: No known Critical or High CVEs in dependencies
- [ ] **Dependency Versions**: Dependencies pinned to secure versions
- [ ] **License Compliance**: Dependency licenses compatible

#### OWASP Top 10 Compliance
- [ ] **A01 Broken Access Control**: Access controls properly implemented
- [ ] **A02 Cryptographic Failures**: Sensitive data encrypted
- [ ] **A03 Injection**: SQL/command/script injection prevented
- [ ] **A04 Insecure Design**: Security designed into architecture
- [ ] **A05 Security Misconfiguration**: Secure defaults, proper configuration
- [ ] **A06 Vulnerable Components**: No vulnerable dependencies
- [ ] **A07 Authentication Failures**: Strong authentication and session management
- [ ] **A08 Data Integrity Failures**: Data integrity verified
- [ ] **A09 Logging Failures**: Security events logged and monitored
- [ ] **A10 SSRF**: Server-side request forgery prevented

#### Security Report
- [ ] **Security Report Generated**: /docs/implementation/security/feature-{issue-number}-security.md
- [ ] **Vulnerabilities Documented**: All findings documented with severity
- [ ] **OWASP Checklist Included**: OWASP Top 10 compliance documented
- [ ] **Recommendations Provided**: Remediation steps for any issues

### Quality Standards

- **Critical Vulnerabilities**: Zero
- **High Vulnerabilities**: Zero
- **Medium Vulnerabilities**: Acceptable with justification and mitigation plan
- **Low Vulnerabilities**: Acceptable, documented
- **OWASP Top 10**: 100% compliant

### Specialist Output

```markdown
**Specialist**: @security-specialist
**Status**: [Pending / In Progress / Completed / Failed]
**Iteration**: [Current / Max]

**Vulnerability Scan Results**:
- Critical: [Count]
- High: [Count]
- Medium: [Count]
- Low: [Count]

**OWASP Top 10 Compliance**:
- Compliant: [X/10]
- Non-Compliant: [List]

**Security Report**: /docs/implementation/security/feature-{issue-number}-security.md
**Completion Time**: [MM:SS]
```

### Recursive Communication (If Vulnerabilities)

```markdown
**Security Vulnerabilities Detected**:
- [ ] Vulnerabilities logged (CVEs, severities, OWASP violations)
- [ ] Recursive communication triggered
- [ ] Security report sent to @feature-implementer-main
- [ ] Awaiting main agent fix
- [ ] Fix completed, re-running security scan
- [ ] Iteration count: [Current / Max (5)]
```

---

## Phase 6: E2E & Accessibility (Frontend Only)

### Checklist

#### E2E Testing
- [ ] **E2E Specialist Invoked**: @e2e-accessibility-specialist called
- [ ] **User Flows Identified**: Critical user flows from PRP
- [ ] **E2E Tests Created**: Playwright/Cypress tests for user flows
- [ ] **All User Flows Pass**: 100% pass rate for E2E tests
- [ ] **Cross-Browser Tested**: Chrome, Firefox, Safari compatibility verified
- [ ] **Mobile Responsive**: Tests pass on mobile viewports
- [ ] **Tablet Responsive**: Tests pass on tablet viewports
- [ ] **Desktop Responsive**: Tests pass on desktop viewports
- [ ] **Form Validation**: All forms submit and validate correctly
- [ ] **Navigation**: All navigation links work correctly
- [ ] **No Console Errors**: No JavaScript errors in browser console

#### Accessibility Testing (WCAG 2.1 AA)
- [ ] **Perceivable - Text Alternatives**: Images have alt text
- [ ] **Perceivable - Captions**: Media has captions (if applicable)
- [ ] **Perceivable - Adaptable**: Content structure is semantic
- [ ] **Perceivable - Distinguishable**: Sufficient color contrast (4.5:1 for text)
- [ ] **Operable - Keyboard**: All functionality keyboard accessible
- [ ] **Operable - Enough Time**: No time limits or adjustable (if applicable)
- [ ] **Operable - Seizures**: No flashing content >3 times/second
- [ ] **Operable - Navigable**: Skip links, headings, focus order correct
- [ ] **Understandable - Readable**: Language identified, text readable
- [ ] **Understandable - Predictable**: Consistent navigation, no unexpected changes
- [ ] **Understandable - Input Assistance**: Labels, error messages, help text
- [ ] **Robust - Compatible**: Valid HTML, works with assistive tech (screen readers)

#### Browser Compatibility Matrix
- [ ] **Chrome (latest)**: Full functionality
- [ ] **Firefox (latest)**: Full functionality
- [ ] **Safari (latest)**: Full functionality
- [ ] **Edge (latest)**: Full functionality (optional)
- [ ] **Mobile Safari**: Full functionality (if mobile app)
- [ ] **Mobile Chrome**: Full functionality (if mobile app)

#### E2E & Accessibility Report
- [ ] **E2E Report Generated**: /docs/implementation/e2e/feature-{issue-number}-e2e.md
- [ ] **User Flow Results**: Pass/fail for each user flow
- [ ] **Accessibility Audit**: WCAG 2.1 AA compliance checklist
- [ ] **Browser Compatibility**: Matrix of browser test results
- [ ] **Screenshots**: Captures of E2E test runs (optional)

### Quality Standards

- **E2E Pass Rate**: 100% (all user flows pass)
- **WCAG 2.1 AA**: 100% compliant
- **Browser Coverage**: Minimum Chrome, Firefox, Safari
- **Responsive Design**: All breakpoints tested (mobile, tablet, desktop)
- **Performance**: Page load <3 seconds, interactions <100ms

### Specialist Output

```markdown
**Specialist**: @e2e-accessibility-specialist
**Status**: [Pending / In Progress / Completed / Failed]
**Iteration**: [Current / Max]

**E2E Test Results**:
- Total User Flows: [Count]
- Passed: [Count]
- Failed: [Count]

**Accessibility Results**:
- WCAG 2.1 AA Violations: [Count]
- Compliant: [Yes/No]

**Browser Compatibility**:
- Chrome: [Pass/Fail]
- Firefox: [Pass/Fail]
- Safari: [Pass/Fail]

**E2E Report**: /docs/implementation/e2e/feature-{issue-number}-e2e.md
**Completion Time**: [MM:SS]
```

### Recursive Communication (If Failures)

```markdown
**E2E or Accessibility Issues Detected**:
- [ ] Issues logged (failed flows, WCAG violations)
- [ ] Recursive communication triggered
- [ ] E2E/accessibility report sent to @feature-implementer-main
- [ ] Awaiting main agent fix
- [ ] Fix completed, re-running E2E tests
- [ ] Iteration count: [Current / Max (5)]
```

### Frontend Determination

```markdown
**Is Frontend Feature?**
- [ ] Yes: Proceed with Phase 6
- [ ] No: Skip Phase 6, mark as N/A

**Frontend Detection**:
- UI components in implementation files
- HTML/CSS/JavaScript/TypeScript files
- React/Vue/Angular components
- SwiftUI/UIKit (iOS)
- User-facing interfaces
```

---

## Validation Summary

### Overall Quality Gates

| Quality Gate | Status | Details |
|--------------|--------|---------|
| Unit Tests Written | [ ] | [Count] tests created |
| Integration Tests Written | [ ] | [Count] tests created |
| All Tests Pass | [ ] | [Passed/Total] |
| Code Coverage ≥80% | [ ] | [XX.X%] |
| Linting | [ ] | [Errors: X, Warnings: X] |
| Type Checking | [ ] | [Errors: X] |
| Code Formatting | [ ] | [Violations: X] |
| Security Scan | [ ] | [Critical: X, High: X, Medium: X, Low: X] |
| OWASP Compliance | [ ] | [X/10 compliant] |
| E2E Tests | [ ] | [Passed/Total] or N/A |
| WCAG 2.1 AA | [ ] | [Violations: X] or N/A |

### Validation Statistics

```markdown
**Total Specialists Invoked**: [5 or 6]
**Total Iterations**: [Count across all specialists]
**Recursive Fix Cycles**: [Count]
**Total Validation Time**: [HH:MM:SS]
**Overall Status**: [Pending / In Progress / Passed / Failed]
```

### Documentation Generated

- [ ] Test Report: `/docs/implementation/tests/feature-{issue-number}-tests.md`
- [ ] Quality Report: `/docs/implementation/quality/feature-{issue-number}-quality.md`
- [ ] Security Report: `/docs/implementation/security/feature-{issue-number}-security.md`
- [ ] E2E Report: `/docs/implementation/e2e/feature-{issue-number}-e2e.md` (frontend only)
- [ ] Validation Report: `/docs/implementation/validation/feature-{issue-number}-validation.md`

### Deployment Readiness

```markdown
**Ready for Deployment?**
- [ ] All quality gates passed
- [ ] All documentation generated
- [ ] Zero critical/high vulnerabilities
- [ ] All tests passing with ≥80% coverage
- [ ] Code quality checks passed
- [ ] OWASP Top 10 compliant
- [ ] E2E and accessibility verified (if frontend)

**Result**: [✅ READY / ⚠️ NOT READY]
```

---

## Version History

- **v2.0.0** (2025-10-29): Initial validation checklist for Feature-Implementer v2 architecture
- Comprehensive quality gates across 6 validation phases
- OWASP Top 10 and WCAG 2.1 AA compliance tracking
- Recursive communication support for failure handling

---

**Version**: 2.0.0
**Created**: 2025-10-29
**Updated**: 2025-10-29
