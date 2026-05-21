---
name: security-checklist
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Security Analysis Checklist

## OWASP Top 10 Assessment

### A01: Broken Access Control
- [ ] Authentication required for protected resources
- [ ] Authorization checks at every access point
- [ ] Role-based access control (RBAC) implemented
- [ ] Least privilege principle applied
- [ ] Session management secure (timeouts, invalidation)
- [ ] Direct object references protected
- [ ] CORS policy properly configured

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A02: Cryptographic Failures
- [ ] Sensitive data identified (PII, credentials, tokens)
- [ ] Data encrypted in transit (TLS 1.2+)
- [ ] Data encrypted at rest (if applicable)
- [ ] Strong encryption algorithms used (AES-256, RSA-2048+)
- [ ] Secrets not hardcoded in source
- [ ] Secure key management (rotation, storage)
- [ ] Password hashing with modern algorithms (Argon2, bcrypt)

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A03: Injection
- [ ] All user inputs validated and sanitized
- [ ] Parameterized queries/prepared statements used
- [ ] ORM used correctly (no raw SQL with user input)
- [ ] Command injection prevented (avoid shell commands with user input)
- [ ] File path injection prevented (sanitize file paths)
- [ ] LDAP injection prevented (if applicable)
- [ ] NoSQL injection prevented (sanitize query operators)

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A04: Insecure Design
- [ ] Threat modeling completed
- [ ] Secure design patterns used (fail-safe defaults, etc.)
- [ ] Defense in depth implemented
- [ ] Security requirements in acceptance criteria
- [ ] Secure development lifecycle followed
- [ ] Separation of concerns maintained
- [ ] Minimal attack surface design

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A05: Security Misconfiguration
- [ ] Default credentials changed
- [ ] Unnecessary features disabled
- [ ] Error messages don't leak sensitive information
- [ ] Security headers configured (CSP, X-Frame-Options, etc.)
- [ ] Debug mode disabled in production
- [ ] Dependency versions pinned and reviewed
- [ ] Security patching process in place

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A06: Vulnerable and Outdated Components
- [ ] All dependencies identified and documented
- [ ] Dependencies up-to-date or vulnerabilities assessed
- [ ] Unused dependencies removed
- [ ] Dependency scanning automated (e.g., Dependabot)
- [ ] License compatibility verified
- [ ] Supply chain risk assessed
- [ ] Vendor security practices reviewed

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A07: Identification and Authentication Failures
- [ ] Multi-factor authentication considered
- [ ] Password complexity requirements enforced
- [ ] Account lockout after failed attempts
- [ ] Session tokens securely generated (cryptographically random)
- [ ] Session fixation prevented
- [ ] Credential stuffing protections in place
- [ ] Secure password recovery flow

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A08: Software and Data Integrity Failures
- [ ] Code integrity verification (signatures, checksums)
- [ ] CI/CD pipeline security reviewed
- [ ] Deserialization of untrusted data prevented
- [ ] Auto-update mechanisms secure
- [ ] Digital signatures verified
- [ ] Integrity checks on critical data
- [ ] Tamper detection implemented

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A09: Security Logging and Monitoring Failures
- [ ] Security events logged (auth failures, access violations)
- [ ] Log data protected from tampering
- [ ] Sensitive data not logged (passwords, tokens, PII)
- [ ] Logs centralized and monitored
- [ ] Alerting configured for security events
- [ ] Incident response procedures documented
- [ ] Audit trail maintained

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

### A10: Server-Side Request Forgery (SSRF)
- [ ] User-supplied URLs validated and sanitized
- [ ] Allow-list for external services used
- [ ] Network segmentation implemented
- [ ] Internal services not directly accessible
- [ ] Response validation implemented
- [ ] DNS rebinding protections in place
- [ ] Cloud metadata endpoints protected

**Risk Level:** ☐ Low ☐ Medium ☐ High
**Mitigation:**

---

## Python-Specific Security Considerations

### Code Execution
- [ ] `eval()`, `exec()`, `compile()` avoided with user input
- [ ] `pickle` deserialization secured or avoided
- [ ] `subprocess` calls sanitized (avoid shell=True with user input)
- [ ] Template injection prevented (Jinja2 autoescape enabled)
- [ ] File inclusion vulnerabilities prevented

### Web Framework Security (Flask/Django/FastAPI)
- [ ] CSRF protection enabled
- [ ] XSS protection configured
- [ ] SQL injection prevention (ORM or parameterized queries)
- [ ] Secure cookie flags set (HttpOnly, Secure, SameSite)
- [ ] Rate limiting implemented
- [ ] Request size limits configured

### Dependencies
- [ ] Virtual environment used (isolation)
- [ ] `requirements.txt` with pinned versions
- [ ] `pip-audit` or `safety` run for vulnerability scanning
- [ ] No use of `pip install` with `--trusted-host`
- [ ] Package integrity verified (checksum/hash)

---

## Data Protection

### Personal Identifiable Information (PII)
- [ ] PII identified and classified
- [ ] Data minimization principle applied
- [ ] Consent mechanisms implemented (if required)
- [ ] Right to erasure supported (GDPR Article 17)
- [ ] Data portability supported (GDPR Article 20)
- [ ] Data breach notification process defined
- [ ] Privacy policy updated

### Data Storage
- [ ] Database credentials secured (not in code)
- [ ] Database connections encrypted (SSL/TLS)
- [ ] Backups encrypted
- [ ] Data retention policies enforced
- [ ] Secure deletion procedures defined
- [ ] Access logs maintained

### Data Transmission
- [ ] HTTPS enforced (no plain HTTP)
- [ ] Certificate validation enabled
- [ ] TLS 1.2+ used (no SSLv3, TLS 1.0/1.1)
- [ ] Perfect forward secrecy (PFS) configured
- [ ] HSTS header configured
- [ ] Sensitive data not in URLs/query params

---

## API Security

### Authentication & Authorization
- [ ] API keys/tokens secured (not in URLs)
- [ ] OAuth2/JWT properly implemented
- [ ] Token expiration configured
- [ ] Token refresh mechanism secure
- [ ] API versioning implemented
- [ ] Deprecated endpoints disabled

### Input Validation
- [ ] Request body size limited
- [ ] Content-Type validation enforced
- [ ] Schema validation implemented (OpenAPI/JSON Schema)
- [ ] Array/list size limits enforced
- [ ] String length limits enforced
- [ ] Numeric range validation applied

### Rate Limiting & DoS Protection
- [ ] Rate limiting per user/IP implemented
- [ ] Request throttling configured
- [ ] Timeout configured for long operations
- [ ] Circuit breaker pattern for external services
- [ ] Resource exhaustion attacks mitigated
- [ ] Backpressure handling implemented

---

## Infrastructure Security

### Environment
- [ ] Environment variables for secrets (no hardcoding)
- [ ] `.env` files in `.gitignore`
- [ ] Secrets manager used (AWS Secrets Manager, Vault, etc.)
- [ ] Principle of least privilege for service accounts
- [ ] Network segmentation implemented
- [ ] Firewall rules configured

### Containers & Orchestration (if applicable)
- [ ] Base images from trusted sources
- [ ] Images scanned for vulnerabilities
- [ ] Non-root user in containers
- [ ] Read-only file systems where possible
- [ ] Resource limits configured (CPU, memory)
- [ ] Secrets not baked into images

### CI/CD Pipeline
- [ ] Secure credential handling in pipelines
- [ ] Code scanning automated (SAST)
- [ ] Dependency scanning automated
- [ ] Container image scanning automated
- [ ] Secrets scanning enabled (pre-commit hooks)
- [ ] Deployment requires approval

---

## Testing & Validation

### Security Testing
- [ ] Unit tests for authorization checks
- [ ] Integration tests for authentication flows
- [ ] Negative testing (malicious inputs)
- [ ] Fuzz testing planned (if applicable)
- [ ] Penetration testing scheduled (for critical features)
- [ ] Security code review completed

### Test Data
- [ ] Production data not used in testing
- [ ] Test data anonymized/pseudonymized
- [ ] Test credentials different from production
- [ ] Test environment isolated from production

---

## Compliance & Regulatory

### Privacy Regulations
- [ ] GDPR compliance assessed (if EU users)
- [ ] CCPA compliance assessed (if CA users)
- [ ] HIPAA compliance assessed (if health data)
- [ ] Data residency requirements understood
- [ ] Cross-border data transfer rules followed

### Industry Standards
- [ ] PCI DSS compliance (if handling payment cards)
- [ ] SOC 2 requirements understood (if B2B SaaS)
- [ ] ISO 27001 alignment considered
- [ ] Industry-specific regulations reviewed

---

## Risk Summary

### Critical Risks (Address Immediately)
1.
2.
3.

### High Risks (Address Before Release)
1.
2.
3.

### Medium Risks (Monitor & Plan Mitigation)
1.
2.
3.

### Low Risks (Accept or Monitor)
1.
2.
3.

---

## Security Sign-off

**Overall Risk Assessment:** ☐ Low ☐ Medium ☐ High ☐ Critical

**Recommendation:** ☐ Proceed ☐ Proceed with Mitigations ☐ Pause for Review

**Notes:**

**Reviewed By:** _________________
**Date:** _________________

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [CWE Top 25](https://cwe.mitre.org/top25/)
