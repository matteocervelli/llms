---
name: threat-modeling-guide
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Threat Modeling Guide

A systematic approach to identifying and prioritizing security threats using STRIDE methodology.

## Overview

Threat modeling is a structured process to identify security threats, understand attack vectors, and prioritize mitigations. This guide uses the STRIDE methodology to systematically evaluate security risks.

## When to Use Threat Modeling

- **Early Design Phase**: Identify risks before implementation
- **New Features**: Assess security impact of new functionality
- **Architecture Changes**: Evaluate security of architectural decisions
- **Third-Party Integrations**: Understand risks of external dependencies
- **Security Reviews**: Comprehensive security assessment

## Threat Modeling Process

### Step 1: Identify Assets

List valuable assets that need protection:

**Data Assets**:
- User credentials (passwords, tokens)
- Personal Identifiable Information (PII)
- Financial information
- Business data
- Intellectual property
- Session tokens
- API keys
- Encryption keys

**System Assets**:
- Application servers
- Databases
- APIs
- File systems
- Network infrastructure
- CI/CD pipelines

**Business Assets**:
- Reputation
- Availability
- Customer trust
- Regulatory compliance

### Step 2: Create Architecture Diagram

Visualize the system to understand:
- Components and their interactions
- Trust boundaries
- Data flows
- External dependencies

**Example**:
```
[User Browser] --HTTPS--> [Load Balancer] ---> [Web Server]
                                                    |
                                    [Application Logic]
                                            |
                                    [Database]
                                            |
                                    [File Storage]
```

**Trust Boundaries**:
- Internet ↔ Web Server (highest risk)
- Web Server ↔ Application
- Application ↔ Database
- Application ↔ External APIs

### Step 3: Identify Threat Actors

Understand who might attack and their motivations:

**External Threat Actors**:
- **Script Kiddies**: Low skill, automated tools, opportunistic
- **Hacktivists**: Ideological motivation, moderate skill
- **Cybercriminals**: Financial motivation, high skill
- **Nation States**: Political/espionage motivation, very high skill
- **Competitors**: Business intelligence, variable skill

**Internal Threat Actors**:
- **Malicious Insiders**: Current/former employees with access
- **Negligent Users**: Unintentional security violations
- **Compromised Accounts**: Legitimate accounts under attacker control

**Automated Threats**:
- **Bots**: Credential stuffing, scraping, DDoS
- **Malware**: Trojans, ransomware, spyware

### Step 4: Enumerate Attack Vectors

Identify how threats could be realized:

**Network-Based**:
- Man-in-the-Middle (MITM) attacks
- Network sniffing
- DDoS attacks
- DNS poisoning

**Application-Based**:
- SQL injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Authentication bypass
- Authorization flaws
- Business logic abuse

**Social Engineering**:
- Phishing
- Pretexting
- Baiting

**Physical**:
- Unauthorized access to infrastructure
- Device theft

### Step 5: STRIDE Analysis

Systematically evaluate threats using STRIDE:

#### S - Spoofing Identity

**Definition**: Pretending to be someone or something else

**Questions**:
- Can attacker impersonate another user?
- Can attacker spoof system components?
- Is authentication properly implemented?
- Are session tokens secure?

**Example Threats**:
- Credential theft and replay
- Session hijacking
- Token forgery
- IP spoofing

**Mitigations**:
- Strong authentication (MFA)
- Secure session management
- Token signing and verification
- Certificate validation

#### T - Tampering with Data

**Definition**: Malicious modification of data

**Questions**:
- Can attacker modify data in transit?
- Can attacker modify data at rest?
- Is data integrity protected?
- Are inputs validated?

**Example Threats**:
- SQL injection
- Parameter tampering
- Cookie modification
- File upload manipulation
- Database tampering

**Mitigations**:
- Input validation
- Parameterized queries
- Integrity checks (HMAC, signatures)
- TLS for data in transit
- Access controls on data stores

#### R - Repudiation

**Definition**: Denying actions without proof

**Questions**:
- Are user actions logged?
- Are logs tamper-proof?
- Can users deny their actions?
- Is audit trail comprehensive?

**Example Threats**:
- Log deletion
- Log tampering
- Lack of non-repudiation

**Mitigations**:
- Comprehensive logging
- Append-only logs
- Digital signatures for critical actions
- Centralized log management
- Log integrity monitoring

#### I - Information Disclosure

**Definition**: Exposing information to unauthorized individuals

**Questions**:
- Can sensitive data be accessed by unauthorized users?
- Are error messages revealing too much?
- Is data encrypted at rest and in transit?
- Are secrets properly managed?

**Example Threats**:
- Directory traversal
- Information leakage in errors
- Unencrypted storage
- Exposed secrets in code/logs
- Side-channel attacks

**Mitigations**:
- Encryption (TLS, AES)
- Generic error messages
- Access controls
- Secret management (vaults)
- Data classification
- Secure deletion

#### D - Denial of Service

**Definition**: Making system unavailable

**Questions**:
- Can attacker exhaust resources?
- Are rate limits implemented?
- Is resource allocation bounded?
- Is system resilient to failures?

**Example Threats**:
- Resource exhaustion (CPU, memory, disk)
- Algorithmic complexity attacks
- DDoS attacks
- Database connection exhaustion
- File system filling

**Mitigations**:
- Rate limiting
- Resource quotas
- Input size limits
- Timeouts
- Load balancing
- Auto-scaling
- CAPTCHA

#### E - Elevation of Privilege

**Definition**: Gaining unauthorized capabilities

**Questions**:
- Can attacker gain higher privileges?
- Is privilege escalation possible?
- Are authorization checks complete?
- Is principle of least privilege applied?

**Example Threats**:
- Privilege escalation vulnerabilities
- Insecure direct object references
- Missing authorization checks
- Admin interface exposure
- Default credentials

**Mitigations**:
- Least privilege principle
- Role-based access control
- Authorization checks on every request
- Secure defaults
- Remove/disable default accounts

### Step 6: Assess Risk

For each identified threat, assess:

**Likelihood**: How probable is this threat?
- **High**: Easy to exploit, common attack
- **Medium**: Requires some skill or conditions
- **Low**: Difficult to exploit, rare

**Impact**: What's the damage if exploited?
- **Critical**: Complete system compromise, massive data breach
- **High**: Significant data loss, major functionality loss
- **Medium**: Limited data exposure, service degradation
- **Low**: Minor information disclosure, temporary inconvenience

**Risk Matrix**:

| Impact → | Low | Medium | High | Critical |
|----------|-----|--------|------|----------|
| **Likelihood ↓** |
| **High** | Medium | High | Critical | Critical |
| **Medium** | Low | Medium | High | Critical |
| **Low** | Low | Low | Medium | High |

**Prioritization**:
1. **Critical**: Immediate action required
2. **High**: Fix before release
3. **Medium**: Fix in near-term
4. **Low**: Monitor and fix as time permits

### Step 7: Define Mitigations

For each significant threat, document:

**Mitigation Strategy**:
- **Eliminate**: Remove the feature/vulnerability
- **Reduce**: Implement controls to lower risk
- **Transfer**: Use third-party service
- **Accept**: Document decision to accept risk

**Example Mitigation Documentation**:
```markdown
## Threat: SQL Injection via Search Feature

**STRIDE Category**: Tampering
**Asset**: Customer database
**Attack Vector**: Unsanitized search input
**Likelihood**: High
**Impact**: Critical
**Risk**: Critical

**Mitigation**:
- **Strategy**: Reduce
- **Controls**:
  1. Use parameterized queries (eliminate string concatenation)
  2. Implement input validation (whitelist alphanumeric + spaces)
  3. Limit search query length (max 100 chars)
  4. Use ORM (SQLAlchemy) with parameter binding
  5. Implement Web Application Firewall (WAF)
  6. Monitor for SQL injection patterns in logs
- **Residual Risk**: Low
- **Implementation**: Sprint 1
- **Owner**: Backend team
```

## Threat Modeling Template

```markdown
# Threat Model: [Feature Name]

## 1. Assets
- **Data**: [List data assets]
- **Systems**: [List system assets]
- **Business**: [List business assets]

## 2. Architecture
[Diagram or description of components and data flows]

**Trust Boundaries**:
- [Boundary 1]: [Description]
- [Boundary 2]: [Description]

## 3. Threat Actors
- **External**: [List external threats]
- **Internal**: [List internal threats]
- **Automated**: [List automated threats]

## 4. STRIDE Analysis

### Spoofing
| Threat | Likelihood | Impact | Risk | Mitigation |
|--------|------------|--------|------|------------|
| [Threat 1] | [L/M/H] | [L/M/H/C] | [L/M/H/C] | [Strategy] |

### Tampering
| Threat | Likelihood | Impact | Risk | Mitigation |
|--------|------------|--------|------|------------|
| [Threat 1] | [L/M/H] | [L/M/H/C] | [L/M/H/C] | [Strategy] |

### Repudiation
| Threat | Likelihood | Impact | Risk | Mitigation |
|--------|------------|--------|------|------------|
| [Threat 1] | [L/M/H] | [L/M/H/C] | [L/M/H/C] | [Strategy] |

### Information Disclosure
| Threat | Likelihood | Impact | Risk | Mitigation |
|--------|------------|--------|------|------------|
| [Threat 1] | [L/M/H] | [L/M/H/C] | [L/M/H/C] | [Strategy] |

### Denial of Service
| Threat | Likelihood | Impact | Risk | Mitigation |
|--------|------------|--------|------|------------|
| [Threat 1] | [L/M/H] | [L/M/H/C] | [L/M/H/C] | [Strategy] |

### Elevation of Privilege
| Threat | Likelihood | Impact | Risk | Mitigation |
|--------|------------|--------|------|------------|
| [Threat 1] | [L/M/H] | [L/M/H/C] | [L/M/H/C] | [Strategy] |

## 5. Risk Summary
| Risk Level | Count | % of Total |
|------------|-------|------------|
| Critical | [N] | [%] |
| High | [N] | [%] |
| Medium | [N] | [%] |
| Low | [N] | [%] |

## 6. Top Risks
1. **[Threat]**: [Risk level] - [Brief description]
2. **[Threat]**: [Risk level] - [Brief description]
3. **[Threat]**: [Risk level] - [Brief description]

## 7. Mitigation Plan
| Priority | Threat | Mitigation | Owner | Timeline |
|----------|--------|------------|-------|----------|
| 1 | [Threat] | [Strategy] | [Team] | [Sprint] |
| 2 | [Threat] | [Strategy] | [Team] | [Sprint] |

## 8. Residual Risks
[Document risks that remain after mitigations]

## 9. Assumptions
[List assumptions made during threat modeling]

## 10. Review
- **Date**: [Date]
- **Participants**: [Names]
- **Next Review**: [Date]
```

## Best Practices

1. **Start Early**: Threat model during design, not after implementation
2. **Iterate**: Revisit threat model as design evolves
3. **Collaborate**: Include developers, security, and business stakeholders
4. **Be Specific**: Document concrete threats, not generic concerns
5. **Prioritize**: Focus on high-risk threats first
6. **Track**: Monitor mitigation implementation
7. **Update**: Revise threat model when system changes
8. **Document Decisions**: Record why risks are accepted or mitigated

## Common Mistakes to Avoid

- **Too Generic**: "System could be hacked" (not specific enough)
- **Implementation-Focused**: Jumping to solutions before understanding threats
- **Incomplete STRIDE**: Skipping categories
- **No Prioritization**: Treating all threats equally
- **One-Time Activity**: Not updating threat model
- **No Follow-Up**: Identifying threats but not implementing mitigations

---

**Usage**: Use this guide to conduct systematic threat modeling during the security assessment phase of feature analysis.
