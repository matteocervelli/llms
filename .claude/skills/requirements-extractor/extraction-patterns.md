---
name: extraction-patterns
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Requirements Extraction Patterns

This document provides common patterns for identifying and extracting requirements from natural language in GitHub issues.

## Functional Requirement Patterns

### Pattern 1: Modal Verbs
**Keywords**: "must", "shall", "will", "should"

**Examples**:
- "The system **must** authenticate users before granting access"
  - **FR-001**: User Authentication required before access
- "The application **shall** export data in CSV format"
  - **FR-002**: CSV export capability
- "Users **should** be able to filter results by date"
  - **FR-003**: Date-based filtering

### Pattern 2: Actor-Action-Object
**Format**: [Actor] [Action Verb] [Object/Target]

**Examples**:
- "Users **can create** new projects"
  - **FR-004**: Project creation by users
- "Administrators **manage** user permissions"
  - **FR-005**: Permission management by administrators
- "The system **generates** weekly reports"
  - **FR-006**: Automated weekly report generation

### Pattern 3: Conditional Logic
**Keywords**: "if", "when", "whenever", "given", "provided that"

**Examples**:
- "**When** a user logs in, **then** display the dashboard"
  - **FR-007**: Dashboard display upon successful login
- "**If** payment fails, **then** send notification email"
  - **FR-008**: Payment failure notification
- "**Given** valid credentials, **when** user submits, **then** grant access"
  - **FR-009**: Conditional access based on credentials

### Pattern 4: Capability Statements
**Keywords**: "ability to", "capable of", "supports", "enables", "allows"

**Examples**:
- "Provides the **ability to** search by multiple criteria"
  - **FR-010**: Multi-criteria search capability
- "**Supports** real-time data synchronization"
  - **FR-011**: Real-time synchronization
- "**Enables** users to share documents with team members"
  - **FR-012**: Document sharing functionality

### Pattern 5: Process Flow
**Keywords**: Steps, sequences, workflows

**Examples**:
- "1. User selects file, 2. System validates format, 3. File is uploaded"
  - **FR-013**: File upload with validation workflow
- "Registration process: Email → Verification → Profile Creation"
  - **FR-014**: Multi-step registration process

## Non-Functional Requirement Patterns

### Performance Patterns
**Keywords**: "within", "less than", "at least", "concurrent", "throughput"

**Examples**:
- "Response time must be **less than** 200ms"
  - **NFR-P-001**: 200ms response time requirement
- "Support **at least** 1000 concurrent users"
  - **NFR-P-002**: 1000 concurrent user capacity
- "Process **within** 5 seconds"
  - **NFR-P-003**: 5-second processing time limit

### Security Patterns
**Keywords**: "secure", "encrypted", "authenticated", "authorized", "protected"

**Examples**:
- "All data must be **encrypted** at rest and in transit"
  - **NFR-S-001**: Data encryption requirement
- "Require **authentication** for all API endpoints"
  - **NFR-S-002**: API authentication requirement
- "Implement **role-based access control**"
  - **NFR-S-003**: RBAC implementation

### Usability Patterns
**Keywords**: "accessible", "intuitive", "compliant", "responsive", "mobile-friendly"

**Examples**:
- "Must be **WCAG 2.1 Level AA compliant**"
  - **NFR-U-001**: WCAG 2.1 AA accessibility
- "**Responsive** design for mobile devices"
  - **NFR-U-002**: Mobile responsiveness requirement
- "Support **keyboard navigation**"
  - **NFR-U-003**: Keyboard accessibility

### Reliability Patterns
**Keywords**: "uptime", "available", "recovery", "backup", "failover"

**Examples**:
- "99.9% **uptime** SLA"
  - **NFR-R-001**: 99.9% availability target
- "**Backup** daily at midnight"
  - **NFR-R-002**: Daily backup schedule
- "**Recovery time** under 1 hour"
  - **NFR-R-003**: 1-hour RTO

### Scalability Patterns
**Keywords**: "scale", "grow", "handle", "support", "increase"

**Examples**:
- "Must **scale** to 10M records"
  - **NFR-SC-001**: 10M record capacity
- "**Handle** 10x traffic increase"
  - **NFR-SC-002**: 10x traffic scalability
- "Support **horizontal scaling**"
  - **NFR-SC-003**: Horizontal scaling capability

## Acceptance Criteria Patterns

### Pattern 1: Checklist Format
**Format**: `- [ ] Statement`

**Example**:
```
- [ ] User can log in with email and password
- [ ] Invalid credentials show error message
- [ ] Session expires after 30 minutes
```

**Extraction**:
- **AC-001**: User login with email/password
- **AC-002**: Error message for invalid credentials
- **AC-003**: 30-minute session expiration

### Pattern 2: BDD Format (Given-When-Then)
**Format**: Given [context], When [action], Then [outcome]

**Example**:
```
Given a valid user account
When user enters correct credentials
Then user is redirected to dashboard
And session token is created
```

**Extraction**:
- **AC-004**: Valid credentials redirect to dashboard
- **AC-005**: Session token creation on successful login

### Pattern 3: Scenario Format
**Format**: Scenario description with steps

**Example**:
```
Scenario: Successful Password Reset
1. User clicks "Forgot Password"
2. User enters email address
3. System sends reset link
4. User clicks link and enters new password
5. User can log in with new password
```

**Extraction**:
- **AC-006**: Forgot password workflow
- **AC-007**: Reset link email sent
- **AC-008**: Password update via link
- **AC-009**: Login with new password

### Pattern 4: Definition of Done
**Keywords**: "Done when...", "Complete when...", "Success criteria:"

**Example**:
```
Done when:
- Feature is implemented
- Unit tests pass (80%+ coverage)
- Documentation updated
- Code reviewed and merged
```

**Extraction**:
- **AC-010**: Feature implementation complete
- **AC-011**: 80%+ test coverage achieved
- **AC-012**: Documentation updated
- **AC-013**: Code review approved and merged

## User Story Patterns

### Pattern 1: Standard Format
**Format**: As a [role], I want [feature], so that [benefit]

**Example**:
```
As a registered user, I want to export my data to CSV, so that I can analyze it offline.
```

**Extraction**:
- **Role**: Registered user
- **Feature**: Data export to CSV
- **Benefit**: Offline analysis
- **Priority**: (Determine from context)

### Pattern 2: Job Story Format
**Format**: When [situation], I want to [motivation], so I can [expected outcome]

**Example**:
```
When I receive a notification, I want to click to view details, so I can respond quickly.
```

**Extraction**:
- **Situation**: Notification received
- **Motivation**: View details
- **Outcome**: Quick response
- **Priority**: (Determine from context)

### Pattern 3: Feature Request Format
**Keywords**: "I would like...", "It would be great if...", "Please add..."

**Example**:
```
It would be great if users could schedule posts for future publication.
```

**Extraction**:
- **Role**: Content creator/user
- **Feature**: Scheduled post publication
- **Benefit**: Time management, automation
- **Priority**: Could Have (unless stated otherwise)

## Issue Body Structure Patterns

### Pattern 1: Templated Issues
**Common Sections**:
- Description/Overview
- Expected Behavior
- Current Behavior
- Steps to Reproduce
- Acceptance Criteria
- Additional Context

**Extraction Strategy**:
- Description → Business requirement
- Expected Behavior → Functional requirements
- Acceptance Criteria → Test criteria
- Additional Context → Constraints, dependencies

### Pattern 2: Epic Issues
**Structure**: Multiple related features under one umbrella

**Example**:
```
Epic: User Management System

Features:
- User registration
- User authentication
- Password reset
- Profile management
- Role-based access control
```

**Extraction**:
- Break into individual features
- Each feature becomes user story
- Epic provides overall context

### Pattern 3: Bug Reports
**Structure**: Issue describes problem to fix

**Example**:
```
Bug: Login fails with valid credentials

Steps: 1. Enter valid email, 2. Enter correct password, 3. Click login
Expected: User logged in
Actual: "Invalid credentials" error shown
```

**Extraction**:
- Expected behavior → Functional requirement
- Current behavior → Defect to fix
- Fix acceptance criteria → Test cases

## Priority Indicators

### Must Have Indicators
**Keywords**: "critical", "required", "must", "blocking", "essential", "mandatory"

**Labels**: `priority:critical`, `P0`, `blocker`

### Should Have Indicators
**Keywords**: "important", "should", "needed", "significant"

**Labels**: `priority:high`, `P1`

### Could Have Indicators
**Keywords**: "nice to have", "could", "optional", "desirable", "enhancement"

**Labels**: `priority:medium`, `P2`, `enhancement`

### Won't Have Indicators
**Keywords**: "future", "later", "out of scope", "won't", "deferred"

**Labels**: `wontfix`, `future`, `backlog`

## Constraint Patterns

### Time Constraints
- "Must be completed by [date]"
- "Deadline: [date]"
- "Time-sensitive"

### Resource Constraints
- "Using only existing libraries"
- "Without adding dependencies"
- "Within current infrastructure"

### Technical Constraints
- "Must work on [platform/browser]"
- "Compatible with [technology]"
- "Using [specific technology/framework]"

### Business Constraints
- "Within budget of [amount]"
- "Compliant with [regulation]"
- "Aligned with [business goal]"

## Dependency Patterns

### Explicit Dependencies
- "Depends on #[issue-number]"
- "Blocked by [feature/issue]"
- "Requires [component/library]"

### Implicit Dependencies
- "After user authentication is implemented..."
- "Once the database is migrated..."
- "When the API is available..."

## Extraction Workflow

### Step 1: Identify Pattern
- Scan issue for keywords
- Recognize structure (template, user story, bug report)
- Note sections and headings

### Step 2: Extract Content
- Apply relevant patterns
- Capture exact wording
- Note context and relationships

### Step 3: Categorize
- Functional vs. Non-functional
- Priority level
- Category (performance, security, usability, etc.)

### Step 4: Structure
- Assign unique IDs
- Format consistently
- Link related requirements

### Step 5: Validate
- Check against requirements-checklist.md
- Ensure completeness
- Verify testability

## Common Pitfalls

### Avoid These Extractions
- **Implementation details as requirements**
  - Bad: "Use React hooks for state management"
  - Good: "Maintain application state across components"

- **Solution instead of problem**
  - Bad: "Add a caching layer"
  - Good: "Reduce API response time to <200ms"

- **Vague statements**
  - Bad: "System should be fast"
  - Good: "95th percentile response time <500ms"

## Example: Complete Extraction

### Input (GitHub Issue)
```
Title: Implement user notification system

Description:
We need a notification system so users stay informed about important events.

Requirements:
- Users must receive email notifications for critical events
- In-app notifications should appear in real-time
- Users can customize notification preferences
- Notification history should be accessible for 30 days
- System must handle 10,000 notifications per hour

Acceptance Criteria:
- [ ] Email sent within 5 minutes of event
- [ ] In-app notification appears immediately
- [ ] Preference settings page is functional
- [ ] History shows last 30 days of notifications
```

### Output (Extracted Requirements)
```markdown
## Functional Requirements
- **FR-001**: Email notification delivery for critical events
- **FR-002**: Real-time in-app notification display
- **FR-003**: User-customizable notification preferences
- **FR-004**: 30-day notification history access
- **FR-005**: Notification preference settings interface

## Non-Functional Requirements
- **NFR-P-001**: Email delivery within 5 minutes of event
- **NFR-P-002**: In-app notifications appear immediately (<1 second)
- **NFR-P-003**: System capacity of 10,000 notifications/hour
- **NFR-R-001**: Notification history retained for 30 days

## Acceptance Criteria
- **AC-001**: Email notification sent within 5 minutes
- **AC-002**: In-app notification displays in real-time
- **AC-003**: User can access and modify preferences
- **AC-004**: History page shows 30 days of notifications

## User Story
- **As a** platform user
- **I want to** receive notifications about important events
- **So that** I stay informed and can respond promptly
- **Priority**: Must Have (P0)
```

---

**Usage**: Reference these patterns when analyzing GitHub issues to systematically extract and structure all requirements.
