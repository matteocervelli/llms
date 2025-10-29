# Security Advisory Database

## Overview

This document catalogs known security vulnerabilities in common Python dependencies, with CVE references, affected versions, severity ratings, and mitigation strategies.

**Last Updated**: 2025-10-29

## Severity Ratings (CVSS v3.1)

| Rating | CVSS Score | Response Time | Priority |
|--------|------------|---------------|----------|
| Critical | 9.0-10.0 | Immediate (< 24h) | P0 |
| High | 7.0-8.9 | Urgent (< 1 week) | P1 |
| Medium | 4.0-6.9 | Scheduled (< 1 month) | P2 |
| Low | 0.1-3.9 | Normal cycle | P3 |

## Core Dependencies

### requests

#### CVE-2023-32681 (Medium - CVSS 6.5)

**Status**: Fixed in 2.31.0+

**Affected Versions**: requests < 2.31.0

**Vulnerability**: Unintended leak of Proxy-Authorization headers

**Description**:
requests forwarded Proxy-Authorization headers to destination servers when following redirects, even when the destination was not the proxy. This could lead to credential exposure.

**Impact**:
- Exposure of proxy credentials to unintended servers
- Potential credential theft
- Privacy violation

**Mitigation**:
```bash
# Upgrade to fixed version
pip install 'requests>=2.31.0'
```

**Fixed Version**: requests==2.31.0

**References**:
- https://github.com/psf/requests/security/advisories/GHSA-j8r2-6x86-q33q
- https://nvd.nist.gov/vuln/detail/CVE-2023-32681

---

### urllib3

#### CVE-2024-37891 (Medium - CVSS 4.4)

**Status**: Fixed in 2.2.2+

**Affected Versions**: urllib3 < 2.2.2

**Vulnerability**: Proxy-Authorization header leak

**Description**:
Similar to CVE-2023-32681, urllib3 leaked proxy credentials during redirects.

**Impact**:
- Credential exposure
- Privacy violation

**Mitigation**:
```bash
# Upgrade to fixed version
pip install 'urllib3>=2.2.2'
```

**Fixed Version**: urllib3==2.2.2

**References**:
- https://github.com/urllib3/urllib3/security/advisories/GHSA-34jh-p97f-mpxf

---

### pydantic

#### CVE-2024-3772 (High - CVSS 7.5)

**Status**: Fixed in 2.7.0+

**Affected Versions**: pydantic 2.0.0 - 2.6.4

**Vulnerability**: Regular expression DoS in email validation

**Description**:
Inefficient regular expression in email validator could cause catastrophic backtracking, leading to DoS.

**Impact**:
- Denial of Service
- Application hang
- CPU exhaustion

**Mitigation**:
```bash
# Upgrade to fixed version
pip install 'pydantic>=2.7.0'
```

**Fixed Version**: pydantic==2.7.0

**References**:
- https://github.com/pydantic/pydantic/security/advisories/GHSA-mr82-8j83-vxmv
- https://nvd.nist.gov/vuln/detail/CVE-2024-3772

---

### cryptography

#### CVE-2023-50782 (High - CVSS 7.5)

**Status**: Fixed in 42.0.0+

**Affected Versions**: cryptography < 42.0.0

**Vulnerability**: NULL pointer dereference in PKCS#7 parsing

**Description**:
Processing malformed PKCS#7 certificates could cause NULL pointer dereference and crash.

**Impact**:
- Application crash
- Denial of Service

**Mitigation**:
```bash
# Upgrade to fixed version
pip install 'cryptography>=42.0.0'
```

**Fixed Version**: cryptography==42.0.0

**References**:
- https://github.com/pyca/cryptography/security/advisories/GHSA-3ww4-gg4f-jr7f

---

## Development Tools

### pip

#### CVE-2023-5752 (Medium - CVSS 5.9)

**Status**: Fixed in 23.3+

**Affected Versions**: pip < 23.3

**Vulnerability**: Mercurial configuration injection

**Description**:
When using Mercurial VCS backend, pip could execute arbitrary commands through configuration injection.

**Impact**:
- Arbitrary code execution
- Supply chain attack vector

**Mitigation**:
```bash
# Upgrade pip
python -m pip install --upgrade 'pip>=23.3'
```

**Fixed Version**: pip==23.3

**References**:
- https://github.com/pypa/pip/security/advisories/GHSA-5xp3-jfq3-5q8x

---

### setuptools

#### CVE-2024-6345 (Critical - CVSS 9.8)

**Status**: Fixed in 70.0.0+

**Affected Versions**: setuptools < 70.0.0

**Vulnerability**: Remote code execution via package download

**Description**:
Downloading packages from untrusted sources could lead to arbitrary code execution.

**Impact**:
- Remote code execution
- Complete system compromise
- Supply chain attack

**Mitigation**:
```bash
# Upgrade setuptools immediately
pip install 'setuptools>=70.0.0'
```

**Fixed Version**: setuptools==70.0.0

**Priority**: **CRITICAL - Upgrade immediately**

**References**:
- https://github.com/pypa/setuptools/security/advisories/GHSA-cx63-2mw6-8hw5

---

## HTTP & Networking

### httpx

**Current Status**: No known vulnerabilities in versions >=0.27.0

**Recommended**: httpx>=0.27.0

**Security Best Practices**:
- Always verify SSL certificates
- Use timeouts to prevent hanging connections
- Validate redirect URLs

```python
import httpx

# Secure configuration
async with httpx.AsyncClient(
    verify=True,  # Verify SSL
    timeout=30.0,  # 30 second timeout
    follow_redirects=True,
    max_redirects=5
) as client:
    response = await client.get(url)
```

---

### certifi

**Current Status**: Regular updates for CA certificates

**Recommended**: certifi>=2024.2.2

**Note**: certifi provides Mozilla's CA bundle. Always keep updated for latest trusted certificates.

---

## Data Processing

### jinja2

#### CVE-2024-22195 (Medium - CVSS 6.1)

**Status**: Fixed in 3.1.3+

**Affected Versions**: jinja2 < 3.1.3

**Vulnerability**: XSS in HTML attributes

**Description**:
Improper sanitization in HTML attribute rendering could allow XSS.

**Impact**:
- Cross-site scripting
- User session hijacking
- Data theft

**Mitigation**:
```bash
# Upgrade to fixed version
pip install 'jinja2>=3.1.3'
```

**Fixed Version**: jinja2==3.1.3

**References**:
- https://github.com/pallets/jinja/security/advisories/GHSA-h5c8-rqwp-cp95

---

### pyyaml

#### CVE-2020-14343 (Critical - CVSS 9.8)

**Status**: Fixed in 5.4+

**Affected Versions**: pyyaml < 5.4

**Vulnerability**: Arbitrary code execution via unsafe load

**Description**:
Using yaml.load() with untrusted data could execute arbitrary Python code.

**Impact**:
- Remote code execution
- Complete system compromise

**Mitigation**:
```bash
# Upgrade to fixed version
pip install 'pyyaml>=6.0'

# Use safe_load instead of load
import yaml
data = yaml.safe_load(untrusted_input)  # Safe
# data = yaml.load(untrusted_input)  # UNSAFE
```

**Fixed Version**: pyyaml==5.4 (safe_load available in all versions)

**Best Practice**: **Always use yaml.safe_load() for untrusted input**

**References**:
- https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation

---

## Security Scanning Tools

### Safety CLI

**Tool**: https://github.com/pyupio/safety

**Installation**:
```bash
pip install safety
```

**Usage**:
```bash
# Scan current environment
safety check

# Scan requirements.txt
safety check -r requirements.txt

# JSON output
safety check --json
```

---

### pip-audit

**Tool**: https://github.com/pypa/pip-audit

**Installation**:
```bash
pip install pip-audit
```

**Usage**:
```bash
# Scan installed packages
pip-audit

# Scan requirements file
pip-audit -r requirements.txt

# Fix vulnerabilities automatically
pip-audit --fix

# JSON output
pip-audit --format json
```

---

### GitHub Dependabot

**Configuration**: `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
```

**Features**:
- Automatic security updates
- Pull requests for version bumps
- Vulnerability alerts

---

## Security Best Practices

### 1. Regular Updates

**Schedule**:
- **Daily**: Monitor security advisories
- **Weekly**: Run security scans
- **Monthly**: Update dependencies
- **Immediately**: Apply critical patches

### 2. Dependency Pinning

**Production**:
```txt
# Pin exact versions for reproducibility
requests==2.32.3
pydantic==2.10.3
httpx==0.27.2
```

**Development**:
```txt
# Allow security updates
requests~=2.32.0
pydantic~=2.10.0
httpx~=0.27.0
```

### 3. Vulnerability Scanning

**Pre-commit Hook**:
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run security scan
pip-audit --format json > /tmp/audit.json

if [ $? -ne 0 ]; then
    echo "❌ Security vulnerabilities detected!"
    echo "Run: pip-audit --fix"
    exit 1
fi
```

### 4. Supply Chain Security

**Best Practices**:
- Verify package signatures
- Use official PyPI (avoid mirrors)
- Review package source code for critical dependencies
- Monitor package maintainership changes
- Use hash-checking mode in pip

```bash
# Generate hashes
pip freeze > requirements.txt
pip-compile --generate-hashes requirements.in

# Install with hash verification
pip install --require-hashes -r requirements.txt
```

### 5. Secure Coding Practices

**Input Validation**:
```python
# Use pydantic for validation
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    email: str
    age: int

    @validator('email')
    def validate_email(cls, v):
        # Email validation with DoS protection
        if len(v) > 256:  # Prevent long inputs
            raise ValueError('Email too long')
        return v
```

**Avoid Unsafe Functions**:
```python
# UNSAFE
eval(user_input)
exec(user_code)
yaml.load(untrusted_yaml)
pickle.loads(untrusted_data)

# SAFE
ast.literal_eval(user_input)  # Limited eval
yaml.safe_load(untrusted_yaml)  # Safe YAML
json.loads(untrusted_json)  # Use JSON instead of pickle
```

---

## Incident Response

### Critical Vulnerability Detected

1. **Immediate Assessment** (< 1 hour)
   - Verify vulnerability affects your version
   - Assess exploit likelihood
   - Determine impact scope

2. **Rapid Mitigation** (< 4 hours)
   - Test patch in isolated environment
   - Deploy to staging
   - Monitor for issues

3. **Production Deployment** (< 24 hours)
   - Deploy during maintenance window if possible
   - If critical, deploy immediately
   - Monitor production closely

4. **Post-Incident** (< 1 week)
   - Document incident
   - Review detection process
   - Improve monitoring

---

## References

### Official Sources

- [PyPI Security Advisories](https://github.com/advisories?query=type%3Areviewed+ecosystem%3Apip)
- [NIST National Vulnerability Database](https://nvd.nist.gov/)
- [CVE Database](https://cve.mitre.org/)
- [GitHub Security Lab](https://securitylab.github.com/)

### Tools

- [Safety](https://github.com/pyupio/safety)
- [pip-audit](https://github.com/pypa/pip-audit)
- [Bandit](https://github.com/PyCQA/bandit) - Python security linter
- [Snyk](https://snyk.io/) - Comprehensive security platform

### Security Mailing Lists

- [Python Security Announcements](https://mail.python.org/mailman/listinfo/security-announce)
- [PyPI Security](https://status.python.org/)

---

**Version**: 2.0.0
**Last Updated**: 2025-10-29
**Maintained By**: Feature-Implementer v2
**Update Frequency**: Weekly
