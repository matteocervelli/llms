---
name: security-checklist
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Security Assessment Checklist

Comprehensive OWASP Top 10 security assessment checklist with Python-specific considerations.

## OWASP Top 10 (2021) Assessment

### 1. Broken Access Control

**Risk Description**: Users can act outside their intended permissions, accessing unauthorized functions or data.

**Assessment Questions**:
- [ ] Are there different user roles or permission levels?
- [ ] Does feature involve accessing resources owned by other users?
- [ ] Can users modify URLs/parameters to access unauthorized data?
- [ ] Are API endpoints protected with proper authorization checks?
- [ ] Is authorization checked on every request (not just on entry)?
- [ ] Are insecure direct object references (IDOR) prevented?
- [ ] Is privilege escalation possible?
- [ ] Are CORS policies properly configured?

**Python-Specific Checks**:
- [ ] Using decorators for permission checks (@requires_permission)?
- [ ] Checking authorization in views/handlers, not just templates?
- [ ] Using Django/Flask permissions frameworks correctly?
- [ ] Implementing resource-level permissions, not just view-level?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Implement RBAC (Role-Based Access Control) or ABAC (Attribute-Based)
- Check permissions on every protected resource access
- Use indirect references (UUIDs instead of sequential IDs)
- Deny by default (whitelist approach)
- Log authorization failures
- Implement resource-level authorization
- Use framework-provided authorization mechanisms

---

### 2. Cryptographic Failures

**Risk Description**: Failure to protect sensitive data through proper encryption, leading to exposure.

**Assessment Questions**:
- [ ] Is sensitive data transmitted over the network?
- [ ] Is sensitive data stored in database?
- [ ] Are passwords handled by the feature?
- [ ] Are API keys, tokens, or secrets used?
- [ ] Is TLS/SSL properly configured (TLS 1.3+)?
- [ ] Are strong encryption algorithms used (AES-256)?
- [ ] Are passwords hashed with secure algorithms (bcrypt, Argon2)?
- [ ] Are cryptographic keys properly managed?
- [ ] Is sensitive data ever logged?

**Python-Specific Checks**:
- [ ] Using bcrypt or Argon2 for password hashing (not MD5/SHA1)?
- [ ] Using secrets module for token generation (not random)?
- [ ] Using cryptography library for encryption (not pycrypto)?
- [ ] Storing secrets in environment variables (not code)?
- [ ] Using Django's password hashers or Werkzeug's security module?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Enforce TLS 1.3+ for all connections
- Use AES-256-GCM for data at rest
- Hash passwords with bcrypt (cost ≥12) or Argon2
- Use secrets module for secure random generation
- Store secrets in environment variables or vaults (never in code)
- Never log passwords, tokens, or PII
- Implement proper key rotation
- Use HTTPS for all API calls

---

### 3. Injection

**Risk Description**: Untrusted data sent to interpreters (SQL, OS, NoSQL, etc.) can execute unintended commands.

**Assessment Questions**:
- [ ] Does feature accept user input?
- [ ] Is input used in SQL queries?
- [ ] Is input used in OS commands?
- [ ] Is input used in LDAP, XPath, or NoSQL queries?
- [ ] Is input used in template rendering?
- [ ] Are parameterized queries used?
- [ ] Is input validated before use?
- [ ] Is ORM used instead of raw SQL?

**Python-Specific Checks**:
- [ ] Using parameterized queries or ORM (SQLAlchemy, Django ORM)?
- [ ] Avoiding subprocess.shell=True or os.system()?
- [ ] Using safe template rendering (Jinja2 autoescaping)?
- [ ] Validating input with Pydantic, marshmallow, or similar?
- [ ] Avoiding eval(), exec(), or compile() with user input?
- [ ] Using SQL placeholders (?, %s) instead of string formatting?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Use parameterized queries (NEVER string concatenation)
- Use ORM/query builders with parameter binding
- Validate all input (whitelist approach)
- Avoid shell commands; use library functions
- Never use eval() or exec() with user input
- Use safe template rendering (auto-escaping enabled)
- Implement input length limits
- Use prepared statements

---

### 4. Insecure Design

**Risk Description**: Missing or ineffective security controls in the design phase.

**Assessment Questions**:
- [ ] Has threat modeling been performed?
- [ ] Are security requirements documented?
- [ ] Are secure design patterns applied?
- [ ] Is defense-in-depth implemented?
- [ ] Are security reviews part of design phase?
- [ ] Is principle of least privilege applied?
- [ ] Are failure scenarios considered?
- [ ] Is rate limiting designed in?

**Python-Specific Checks**:
- [ ] Using type hints for contracts (mypy)?
- [ ] Using Pydantic for request/response validation?
- [ ] Implementing input validation at multiple layers?
- [ ] Using context managers for resource management?
- [ ] Implementing proper exception handling?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Conduct threat modeling early in design
- Document security requirements
- Apply secure design principles (least privilege, fail-safe defaults, complete mediation)
- Implement defense-in-depth
- Use established security patterns
- Plan for failure scenarios
- Design with security in mind from the start

---

### 5. Security Misconfiguration

**Risk Description**: Improperly configured security settings or using insecure defaults.

**Assessment Questions**:
- [ ] Are default configurations changed (passwords, keys)?
- [ ] Are unnecessary features disabled?
- [ ] Are error messages generic (no stack traces)?
- [ ] Are security headers configured (CSP, HSTS, X-Frame-Options)?
- [ ] Is debug mode disabled in production?
- [ ] Are directory listings disabled?
- [ ] Are default accounts removed?
- [ ] Is the application hardened?

**Python-Specific Checks**:
- [ ] DEBUG = False in production (Django/Flask)?
- [ ] SECRET_KEY is strong and not in version control?
- [ ] ALLOWED_HOSTS is properly configured?
- [ ] Using secure session configuration?
- [ ] Using secure cookie settings (HttpOnly, Secure, SameSite)?
- [ ] Disabling unnecessary middleware?
- [ ] Proper CORS configuration?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Use principle of least functionality
- Disable unnecessary features and services
- Configure security headers (CSP, HSTS, X-Frame-Options)
- Generic error messages (no stack traces in production)
- Disable debug mode in production
- Regular security configuration reviews
- Use security scanning tools
- Implement secure defaults

---

### 6. Vulnerable and Outdated Components

**Risk Description**: Using components with known vulnerabilities or that are no longer maintained.

**Assessment Questions**:
- [ ] Are all dependencies up-to-date?
- [ ] Are dependency versions pinned?
- [ ] Is dependency scanning automated?
- [ ] Are security advisories monitored?
- [ ] Are unmaintained packages avoided?
- [ ] Is there a process for updating dependencies?
- [ ] Are transitive dependencies checked?
- [ ] Is Software Composition Analysis (SCA) used?

**Python-Specific Checks**:
- [ ] Using requirements.txt with pinned versions?
- [ ] Running pip-audit or safety regularly?
- [ ] Checking for CVEs in dependencies?
- [ ] Using Dependabot or Snyk?
- [ ] Avoiding packages with no recent updates?
- [ ] Using virtual environments?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Pin dependency versions (requirements.txt, Pipfile.lock)
- Use dependency scanning tools (pip-audit, safety, Snyk, Dependabot)
- Monitor security advisories
- Keep dependencies updated
- Remove unused dependencies
- Use only well-maintained packages
- Automate dependency scanning in CI/CD

---

### 7. Identification and Authentication Failures

**Risk Description**: Weak authentication allowing attackers to compromise accounts.

**Assessment Questions**:
- [ ] Is password strength enforced?
- [ ] Are sessions properly managed (timeout, invalidation)?
- [ ] Is brute-force protection implemented?
- [ ] Is MFA available for sensitive operations?
- [ ] Are password reset flows secure?
- [ ] Are session tokens cryptographically secure?
- [ ] Is credential stuffing prevented?
- [ ] Are authentication attempts logged?

**Python-Specific Checks**:
- [ ] Using Django/Flask authentication frameworks?
- [ ] Implementing password validators?
- [ ] Using secure session configuration?
- [ ] Implementing rate limiting (Flask-Limiter, Django-ratelimit)?
- [ ] Using secure random for session tokens (secrets module)?
- [ ] Implementing CSRF protection?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Enforce strong password policies (min 12 chars, complexity)
- Implement rate limiting for login (5 attempts per 15 min)
- Use secure session management (timeout, HttpOnly cookies)
- Hash passwords with bcrypt (cost ≥12) or Argon2
- Implement account lockout after failed attempts
- Support MFA where appropriate
- Use secure password reset flows (time-limited tokens)
- Log all authentication attempts

---

### 8. Software and Data Integrity Failures

**Risk Description**: Code and infrastructure that does not protect against integrity violations.

**Assessment Questions**:
- [ ] Are dependencies verified (checksums, signatures)?
- [ ] Is CI/CD pipeline secured?
- [ ] Are auto-updates verified?
- [ ] Is deserialization of untrusted data avoided?
- [ ] Is code signing implemented?
- [ ] Are uploads validated?
- [ ] Is input integrity checked?

**Python-Specific Checks**:
- [ ] Avoiding pickle for untrusted data?
- [ ] Using safe serialization (JSON, not pickle)?
- [ ] Verifying package integrity (hash checking)?
- [ ] Securing CI/CD pipeline (secrets management)?
- [ ] Validating file uploads (type, content)?
- [ ] Using safe YAML loading (yaml.safe_load)?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Verify integrity of dependencies (use lock files)
- Secure CI/CD pipeline
- Never deserialize untrusted data with pickle
- Use safe serialization (JSON, protobuf)
- Implement code signing
- Validate file uploads (type, size, content)
- Use hash verification for downloads
- Implement integrity checks

---

### 9. Security Logging and Monitoring Failures

**Risk Description**: Insufficient logging and monitoring preventing detection of breaches.

**Assessment Questions**:
- [ ] Are authentication events logged?
- [ ] Are authorization failures logged?
- [ ] Are input validation failures logged?
- [ ] Are security exceptions logged?
- [ ] Are logs monitored and alerts configured?
- [ ] Are logs tamper-proof?
- [ ] Is sensitive data excluded from logs?
- [ ] Are logs centralized?

**Python-Specific Checks**:
- [ ] Using Python logging module with proper configuration?
- [ ] Logging security events (auth, authz failures)?
- [ ] Not logging sensitive data (passwords, tokens)?
- [ ] Using structured logging (JSON format)?
- [ ] Sending logs to centralized system (ELK, Splunk)?
- [ ] Implementing log rotation?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Log all security-relevant events
- Implement centralized logging
- Set up alerts for suspicious activity
- Protect logs from tampering (append-only)
- Never log sensitive data (passwords, tokens, PII)
- Regular log review
- Implement log retention policies
- Use structured logging

---

### 10. Server-Side Request Forgery (SSRF)

**Risk Description**: Application fetches remote resources without validating user-supplied URLs.

**Assessment Questions**:
- [ ] Does feature make HTTP requests based on user input?
- [ ] Can users specify URLs or domains?
- [ ] Are webhooks supported?
- [ ] Is URL validation implemented?
- [ ] Are internal network requests blocked?
- [ ] Is URL allowlisting used?
- [ ] Are redirects limited?

**Python-Specific Checks**:
- [ ] Validating URLs before requests.get()?
- [ ] Blocking private IP ranges (127.0.0.1, 192.168.*, 10.*)?
- [ ] Using URL allowlist instead of blocklist?
- [ ] Disabling redirects or limiting them?
- [ ] Using network segmentation?
- [ ] Checking for URL schemes (only http/https)?

**Risk Level**: [None | Low | Medium | High | Critical]

**Mitigations**:
- Validate and sanitize all URLs
- Use allowlist of permitted domains
- Block requests to private IP ranges (RFC1918)
- Disable or limit HTTP redirects
- Use network segmentation
- Validate URL schemes (only allow http/https)
- Implement timeout for external requests
- Use DNS allowlisting

---

## Additional Security Considerations

### API Security
- [ ] Authentication required for all endpoints
- [ ] Rate limiting implemented
- [ ] Content-Type validation
- [ ] CORS properly configured
- [ ] API versioning implemented
- [ ] Input size limits enforced

### Data Protection
- [ ] PII identified and protected
- [ ] Data classification implemented
- [ ] Data retention policies defined
- [ ] Secure data deletion implemented
- [ ] Data minimization applied

### Error Handling
- [ ] Generic error messages for users
- [ ] Detailed errors logged internally
- [ ] No stack traces exposed
- [ ] Graceful degradation implemented

### Testing
- [ ] Security test cases written
- [ ] Penetration testing planned
- [ ] SAST tools integrated in CI/CD
- [ ] DAST tools used for testing
- [ ] Dependency scanning automated

---

## Risk Level Matrix

| Risk Level | Description | Action Required |
|------------|-------------|-----------------|
| **Critical** | Immediate threat, easy to exploit, high impact | Fix immediately before deployment |
| **High** | Significant threat, moderate exploitability | Fix before deployment |
| **Medium** | Moderate threat, requires specific conditions | Fix in near-term sprint |
| **Low** | Minor threat, difficult to exploit | Fix as time permits |
| **None** | No risk identified | Document reasoning |

---

## Python-Specific Security Best Practices

### Password Hashing
```python
# Good: bcrypt
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Good: Argon2
from argon2 import PasswordHasher
ph = PasswordHasher()
hashed = ph.hash(password)

# Bad: MD5/SHA1/SHA256 (not designed for passwords)
```

### Secure Random
```python
# Good: secrets module
import secrets
token = secrets.token_urlsafe(32)

# Bad: random module (predictable)
```

### SQL Injection Prevention
```python
# Good: Parameterized query
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))

# Good: ORM
User.objects.filter(email=email)

# Bad: String formatting
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### Command Injection Prevention
```python
# Good: Use library functions
import shutil
shutil.copy(src, dst)

# Bad: Shell commands
os.system(f"cp {src} {dst}")
```

### Serialization
```python
# Good: JSON
import json
data = json.loads(user_input)

# Bad: Pickle (arbitrary code execution)
import pickle
data = pickle.loads(user_input)
```

---

**Usage**: Use this checklist systematically during security assessment phase to ensure comprehensive OWASP Top 10 coverage.
