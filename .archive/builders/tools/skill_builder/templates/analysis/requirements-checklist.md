# Requirements Analysis Checklist

## Functional Requirements

### User Stories & Use Cases
- [ ] All user stories clearly defined with "As a..., I want..., So that..."
- [ ] Use cases documented with actors, preconditions, main flow, alternatives
- [ ] Happy path scenarios identified
- [ ] Edge cases and error scenarios documented
- [ ] User interactions and workflows mapped

### Feature Specifications
- [ ] Feature scope clearly bounded (what's included/excluded)
- [ ] Input/output specifications defined
- [ ] Data models and structures specified
- [ ] Business logic and rules documented
- [ ] Validation rules defined
- [ ] Error handling requirements specified

### Integration Points
- [ ] External APIs identified with endpoints and auth
- [ ] Internal services/modules dependencies listed
- [ ] Database interactions specified
- [ ] File system requirements documented
- [ ] Third-party services integration needs
- [ ] Event/messaging requirements (if applicable)

## Non-Functional Requirements

### Performance
- [ ] Response time requirements defined (e.g., < 200ms)
- [ ] Throughput requirements specified (e.g., 1000 req/s)
- [ ] Concurrent users/sessions estimated
- [ ] Data volume expectations documented
- [ ] Resource limits defined (memory, CPU, storage)

### Scalability
- [ ] Growth projections documented
- [ ] Horizontal/vertical scaling strategy considered
- [ ] Load balancing requirements identified
- [ ] Caching strategy planned
- [ ] Database scaling approach defined

### Reliability & Availability
- [ ] Uptime requirements specified (e.g., 99.9%)
- [ ] Failure recovery procedures defined
- [ ] Backup and disaster recovery planned
- [ ] Health check endpoints required
- [ ] Monitoring and alerting needs identified

### Security
- [ ] Authentication requirements defined
- [ ] Authorization and access control specified
- [ ] Data encryption needs (at rest, in transit)
- [ ] PII handling requirements documented
- [ ] Audit logging requirements specified
- [ ] Security testing requirements defined

### Maintainability
- [ ] Code documentation standards specified
- [ ] Logging requirements defined
- [ ] Error reporting mechanism planned
- [ ] Configuration management approach
- [ ] Deployment process documented

### Testability
- [ ] Unit test coverage target (recommend 80%+)
- [ ] Integration test requirements
- [ ] End-to-end test scenarios
- [ ] Performance test requirements
- [ ] Security test requirements

## Acceptance Criteria

### Validation
- [ ] All acceptance criteria are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
- [ ] Acceptance criteria can be verified objectively
- [ ] Success metrics defined (e.g., "User can complete X in < 3 clicks")
- [ ] Failure conditions explicitly stated

### Completeness
- [ ] All user stories have acceptance criteria
- [ ] Edge cases covered in acceptance criteria
- [ ] Performance criteria included
- [ ] Security criteria included
- [ ] Accessibility criteria included (if applicable)

## Dependencies & Constraints

### Technical Dependencies
- [ ] Required libraries/frameworks identified
- [ ] Version compatibility verified
- [ ] License compatibility checked
- [ ] Installation requirements documented
- [ ] Configuration requirements listed

### External Dependencies
- [ ] Third-party services availability confirmed
- [ ] API rate limits understood
- [ ] SLA agreements reviewed
- [ ] Fallback strategies planned
- [ ] Vendor lock-in risks assessed

### Constraints
- [ ] Technology stack constraints documented
- [ ] Budget constraints identified
- [ ] Time constraints realistic
- [ ] Resource constraints (team, infrastructure) noted
- [ ] Regulatory/compliance constraints documented

## Data Requirements

### Data Model
- [ ] Entities and relationships defined
- [ ] Data types and constraints specified
- [ ] Validation rules documented
- [ ] Data lifecycle defined (CRUD operations)
- [ ] Data retention policies specified

### Data Migration
- [ ] Existing data migration needs identified
- [ ] Migration strategy planned
- [ ] Data transformation rules defined
- [ ] Rollback procedures documented
- [ ] Data validation post-migration planned

### Data Privacy
- [ ] PII data identified
- [ ] Data classification completed (public, internal, confidential, restricted)
- [ ] GDPR/privacy compliance requirements understood
- [ ] Data anonymization needs identified
- [ ] Data retention and deletion policies defined

## Documentation Requirements

### Technical Documentation
- [ ] Architecture diagrams needed
- [ ] API documentation required
- [ ] Data model documentation required
- [ ] Configuration documentation required
- [ ] Deployment documentation required

### User Documentation
- [ ] User guide needed
- [ ] API usage examples required
- [ ] Troubleshooting guide needed
- [ ] FAQ required
- [ ] Release notes template prepared

## Risk Assessment

### Technical Risks
- [ ] Technical complexity assessed
- [ ] Technology maturity evaluated
- [ ] Integration complexity identified
- [ ] Performance risks noted
- [ ] Security risks documented

### Project Risks
- [ ] Scope creep risks identified
- [ ] Timeline risks assessed
- [ ] Resource availability risks noted
- [ ] Dependency risks documented
- [ ] Mitigation strategies planned for high risks

## Stakeholder Alignment

### Communication
- [ ] Stakeholders identified and roles documented
- [ ] Communication plan established
- [ ] Review and approval process defined
- [ ] Feedback mechanisms established
- [ ] Change request process documented

### Sign-off
- [ ] Requirements reviewed with stakeholders
- [ ] Ambiguities clarified
- [ ] Priorities agreed upon
- [ ] Timeline expectations aligned
- [ ] Success criteria agreed upon

---

## Completion Criteria

✅ **Requirements are complete when:**
- All sections above are checked
- No major ambiguities remain
- Stakeholders have signed off
- Technical feasibility confirmed
- Risks documented with mitigations
- Ready to proceed to design phase

## Notes

**Instructions for use:**
1. Work through each section systematically
2. Check items as you validate them
3. Document any items that are "N/A" with rationale
4. Flag blockers or high-risk items
5. Summarize findings in the analysis report

**Red Flags:**
- More than 20% of items unchecked or ambiguous
- Critical security/performance requirements undefined
- Stakeholder alignment missing
- Technical feasibility in question
- Multiple high-risk items without mitigation

➡️ **If you see red flags, pause and resolve them before proceeding to design phase.**
