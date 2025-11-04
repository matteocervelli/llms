---
name: requirements-checklist
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Requirements Validation Checklist

This checklist ensures that all extracted requirements meet quality standards for clarity, completeness, consistency, and testability.

## General Quality Criteria

### Completeness
- [ ] All functional requirements identified
- [ ] All non-functional requirements identified
- [ ] All acceptance criteria specified
- [ ] All user stories documented
- [ ] All business rules captured
- [ ] All constraints documented
- [ ] All assumptions stated
- [ ] All dependencies listed

### Clarity
- [ ] Requirements use clear, unambiguous language
- [ ] Technical jargon is defined
- [ ] Acronyms are spelled out on first use
- [ ] Pronouns have clear antecedents
- [ ] Avoid subjective terms (fast, easy, user-friendly)
- [ ] Use quantifiable metrics where possible
- [ ] One requirement per statement
- [ ] Requirements are understandable by stakeholders

### Consistency
- [ ] No conflicting requirements
- [ ] Terminology used consistently
- [ ] Priority levels are consistent
- [ ] Requirements don't duplicate each other
- [ ] Requirements align with project goals
- [ ] Cross-references are valid

### Testability
- [ ] Each requirement is verifiable
- [ ] Success criteria are measurable
- [ ] Test scenarios can be written
- [ ] Acceptance criteria are objective
- [ ] Performance metrics are quantified

### Feasibility
- [ ] Requirements are technically achievable
- [ ] Resources are available or obtainable
- [ ] Timeline is realistic
- [ ] No unrealistic expectations
- [ ] Third-party dependencies are verified

### Traceability
- [ ] Each requirement has unique ID
- [ ] Requirements link to business goals
- [ ] Requirements link to user stories
- [ ] Acceptance criteria link to requirements
- [ ] Source (issue, stakeholder) is documented

## Functional Requirements Checklist

- [ ] **Action**: What action does the system perform?
- [ ] **Actor**: Who/what initiates the action?
- [ ] **Input**: What input is required?
- [ ] **Output**: What output is produced?
- [ ] **Conditions**: Under what conditions does this happen?
- [ ] **Error Handling**: What happens if it fails?
- [ ] **Dependencies**: What else must be in place?
- [ ] **Priority**: Is this must-have, should-have, or could-have?

## Non-Functional Requirements Checklist

### Performance
- [ ] Response time requirements specified
- [ ] Throughput requirements specified
- [ ] Concurrent user limits defined
- [ ] Data volume limits defined
- [ ] Resource utilization targets set

### Security
- [ ] Authentication requirements defined
- [ ] Authorization requirements defined
- [ ] Data encryption requirements specified
- [ ] Input validation requirements listed
- [ ] Audit logging requirements specified
- [ ] OWASP Top 10 risks assessed

### Usability
- [ ] User interface standards defined
- [ ] Accessibility requirements specified (WCAG level)
- [ ] Localization/internationalization needs stated
- [ ] Help and documentation requirements listed
- [ ] Error message guidelines provided

### Reliability
- [ ] Uptime/availability target defined (e.g., 99.9%)
- [ ] Recovery time objective (RTO) specified
- [ ] Recovery point objective (RPO) specified
- [ ] Backup frequency defined
- [ ] Failover requirements specified

### Scalability
- [ ] Growth projections provided
- [ ] Horizontal scaling support required?
- [ ] Vertical scaling limits defined
- [ ] Load balancing requirements specified
- [ ] Data partitioning strategy needed?

### Maintainability
- [ ] Code quality standards specified
- [ ] Documentation requirements defined
- [ ] Logging and monitoring requirements listed
- [ ] Deployment frequency target set
- [ ] Technical debt tolerance defined

### Compatibility
- [ ] Browser compatibility specified (if web)
- [ ] OS compatibility specified
- [ ] Mobile device support defined
- [ ] API version compatibility stated
- [ ] Backward compatibility requirements listed

### Compliance
- [ ] Regulatory requirements identified (GDPR, HIPAA, etc.)
- [ ] Industry standards compliance specified
- [ ] Legal requirements documented
- [ ] Privacy requirements defined
- [ ] Data retention policies stated

## Acceptance Criteria Checklist

- [ ] Criteria are written in testable format
- [ ] Each criterion is binary (pass/fail)
- [ ] Criteria cover happy path scenarios
- [ ] Criteria cover error scenarios
- [ ] Criteria cover edge cases
- [ ] Criteria specify expected outcomes
- [ ] Criteria include performance expectations
- [ ] Criteria reference specific data or values
- [ ] BDD format used where appropriate (Given/When/Then)

## User Story Checklist (INVEST Criteria)

- [ ] **Independent**: Can be developed independently
- [ ] **Negotiable**: Details can be discussed
- [ ] **Valuable**: Provides value to users/business
- [ ] **Estimable**: Can estimate effort
- [ ] **Small**: Can be completed in one sprint
- [ ] **Testable**: Acceptance criteria are clear

## Common Requirement Issues

### Ambiguous Language to Avoid
- [ ] "Fast", "quick", "responsive" without metrics
- [ ] "User-friendly", "intuitive", "easy" without criteria
- [ ] "Robust", "reliable", "stable" without measures
- [ ] "Secure" without specific security requirements
- [ ] "Scalable" without growth metrics
- [ ] "Flexible", "extensible" without specifics
- [ ] "As soon as possible", "eventually" without timelines
- [ ] "Maximize", "minimize", "optimize" without targets

### Missing Information Flags
- [ ] No error handling specified
- [ ] No validation rules defined
- [ ] No performance targets set
- [ ] No security considerations mentioned
- [ ] No data migration plan
- [ ] No backward compatibility strategy
- [ ] No rollback procedure
- [ ] No monitoring/alerting requirements

### Conflicting Requirements Patterns
- [ ] Real-time updates vs. batch processing
- [ ] High availability vs. low infrastructure cost
- [ ] Feature richness vs. simplicity
- [ ] Strict security vs. ease of use
- [ ] Performance vs. comprehensive logging
- [ ] Flexibility vs. standardization

## Validation Questions

### For Each Requirement, Ask:
1. **What**: What exactly needs to be built?
2. **Why**: Why is this needed? What problem does it solve?
3. **Who**: Who will use this? Who benefits?
4. **When**: When is this needed? What's the deadline?
5. **Where**: Where does this fit in the system?
6. **How**: How will we know it's done? How will we test it?

### Red Flags
- [ ] Requirement starts with "The system should be able to..."
- [ ] Multiple "and"s in single requirement (decompose it)
- [ ] Contains "etc.", "and so on", "similar" (incomplete)
- [ ] Uses "always", "never", "all" (absolutist)
- [ ] Mixes functional and non-functional aspects
- [ ] Implementation details instead of requirements
- [ ] Solution-focused instead of problem-focused

## Prioritization Validation

### MoSCoW Criteria
- **Must Have (P0)**:
  - [ ] Critical for MVP
  - [ ] System unusable without it
  - [ ] Legal/regulatory requirement
  - [ ] High business value + high urgency

- **Should Have (P1)**:
  - [ ] Important but not critical
  - [ ] Has workarounds
  - [ ] High business value + lower urgency
  - [ ] Included if time/budget allows

- **Could Have (P2)**:
  - [ ] Desirable but optional
  - [ ] Nice-to-have features
  - [ ] Low effort + medium value
  - [ ] Can be deferred without impact

- **Won't Have (P3)**:
  - [ ] Out of scope for this release
  - [ ] Future enhancement
  - [ ] Low priority + high effort
  - [ ] Explicitly excluded

## Documentation Standards

- [ ] Each requirement has unique identifier (FR-XXX, NFR-XXX)
- [ ] Requirements are numbered sequentially
- [ ] Requirements are grouped by category
- [ ] Cross-references use requirement IDs
- [ ] Change history is tracked
- [ ] Source/rationale is documented
- [ ] Owner/stakeholder is identified
- [ ] Creation date is recorded

## Final Validation

Before finalizing requirements:
- [ ] All checkboxes above are completed
- [ ] Stakeholders have reviewed
- [ ] Ambiguities have been resolved
- [ ] Conflicts have been resolved
- [ ] Priorities have been agreed upon
- [ ] Scope is clearly defined
- [ ] Risks have been identified
- [ ] Dependencies have been confirmed
- [ ] Timeline is realistic
- [ ] Team capacity is adequate

---

**Usage**: Use this checklist systematically for each requirement extracted from GitHub issues to ensure high-quality analysis output.

**Completion Threshold**: Aim for 95%+ checklist completion before finalizing requirements documentation.
