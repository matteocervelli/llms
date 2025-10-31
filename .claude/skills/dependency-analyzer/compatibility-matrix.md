# Dependency Compatibility Matrix

## Overview

This document provides compatibility information for common Python dependencies used in the LLM Configuration Management System and Feature-Implementer v2 architecture.

## Python Version Compatibility

### Minimum Python Version: 3.11+

**Rationale:**
- Modern type hints support (PEP 646, 673, 675, 681)
- Performance improvements (faster startup, better memory)
- Security updates and long-term support

### Python Version Matrix

| Package | Python 3.11 | Python 3.12 | Python 3.13 | Notes |
|---------|-------------|-------------|-------------|-------|
| pydantic | ✅ | ✅ | ✅ | 2.0+ recommended |
| requests | ✅ | ✅ | ✅ | Stable across versions |
| httpx | ✅ | ✅ | ✅ | Async support |
| click | ✅ | ✅ | ✅ | CLI framework |
| pytest | ✅ | ✅ | ✅ | Testing framework |
| black | ✅ | ✅ | ✅ | Code formatter |
| mypy | ✅ | ✅ | ✅ | Type checker |

## Common Library Compatibility

### Web & HTTP Libraries

**requests vs. httpx:**
- **Compatible**: Can coexist in the same project
- **Use Case**: requests for sync, httpx for async
- **Recommendation**: Migrate to httpx for new async code

```python
# Compatible usage
import requests  # Sync HTTP
import httpx     # Async HTTP

# Sync request
response = requests.get("https://api.example.com")

# Async request
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")
```

### Data Validation Libraries

**pydantic:**
- **Version**: 2.0+ (breaking changes from 1.x)
- **Compatible with**: Python 3.11+
- **Dependencies**: typing-extensions>=4.6.1, annotated-types>=0.4.0

**pydantic-settings:**
- **Version**: 2.0+ (use with pydantic 2.x)
- **Purpose**: Settings management
- **Compatible with**: pydantic>=2.0

### Testing Libraries

**pytest ecosystem:**
- pytest>=7.4.3
- pytest-cov>=4.1.0 (coverage reporting)
- pytest-asyncio>=0.21.0 (async test support)
- pytest-mock>=3.12.0 (mocking support)

**All compatible** - no known conflicts

### Code Quality Tools

**Formatter + Linter + Type Checker:**
- black>=23.12.0 (code formatter)
- flake8>=6.1.0 (linter)
- mypy>=1.7.1 (type checker)

**All compatible** - designed to work together

## Known Conflicts

### Conflict 1: pydantic 1.x vs. 2.x

**Issue**: Breaking API changes between versions

**Scenario**:
```
Package A requires: pydantic>=1.10,<2.0
Package B requires: pydantic>=2.0
```

**Resolution**:
1. Check if Package A has pydantic 2.x support
2. Upgrade Package A if available
3. If not available, consider:
   - Forking Package A and updating
   - Using compatibility shim (pydantic.v1)
   - Choosing alternative to Package A

**Example**:
```python
# pydantic 2.x with v1 compatibility
from pydantic.v1 import BaseModel  # For legacy code
from pydantic import BaseModel     # For new code
```

### Conflict 2: typing-extensions version conflicts

**Issue**: Many packages depend on typing-extensions with varying version requirements

**Scenario**:
```
pydantic>=2.0 requires: typing-extensions>=4.6.1
some-package requires: typing-extensions>=3.7,<4.0
```

**Resolution**:
1. Upgrade some-package to version supporting typing-extensions>=4.0
2. Use typing-extensions>=4.6.1 (usually backwards compatible)

### Conflict 3: cryptography version conflicts

**Issue**: Security-sensitive package with frequent updates

**Scenario**:
```
requests[security] requires: cryptography>=3.0
another-package requires: cryptography<3.0
```

**Resolution**:
1. Always prefer **latest cryptography** for security
2. Upgrade packages to support latest cryptography
3. Check security advisories for vulnerabilities

## Platform-Specific Dependencies

### Linux-Specific

**None in core dependencies**

### macOS-Specific

**None in core dependencies**

### Windows-Specific

**Potential Issues**:
- colorama (Windows console color support)
- Some packages require Visual C++ build tools

**Resolution**:
```bash
# Install colorama for Windows color support
pip install colorama
```

## Dependency Resolution Strategies

### Strategy 1: Upgrade All

**When**: Minor version conflicts, all packages actively maintained

**Process**:
1. Update all packages to latest versions
2. Run tests to verify compatibility
3. Fix breaking changes

**Example**:
```bash
pip list --outdated
pip install --upgrade package1 package2 package3
pytest
```

### Strategy 2: Pin Compatible Versions

**When**: Breaking changes in new versions, need stability

**Process**:
1. Identify compatible version range
2. Pin to specific versions in requirements.txt
3. Document reasoning

**Example**:
```
# Pin to compatible versions
pydantic==2.5.0  # Version 2.6+ has breaking changes
httpx==0.27.2    # Stable version
```

### Strategy 3: Use Compatibility Shims

**When**: Mixed pydantic 1.x and 2.x dependencies

**Process**:
1. Use pydantic.v1 for legacy code
2. Migrate incrementally to pydantic 2.x
3. Remove shim when migration complete

**Example**:
```python
# During migration
from pydantic.v1 import BaseModel as BaseModelV1
from pydantic import BaseModel as BaseModelV2

# Legacy code
class OldModel(BaseModelV1):
    pass

# New code
class NewModel(BaseModelV2):
    pass
```

### Strategy 4: Fork and Update

**When**: Unmaintained package with critical conflict

**Process**:
1. Fork the package repository
2. Update dependency requirements
3. Test thoroughly
4. Use forked version temporarily
5. Submit PR to upstream

## Version Specifier Best Practices

### Specifier Types

| Specifier | Meaning | Use Case | Example |
|-----------|---------|----------|---------|
| `==` | Exact version | Production pinning | `requests==2.31.0` |
| `>=` | Minimum version | Flexible lower bound | `pydantic>=2.0.0` |
| `~=` | Compatible release | Minor updates OK | `httpx~=0.27.0` (means >=0.27.0, <0.28.0) |
| `>=,<` | Range | Constrained flexibility | `click>=8.0,<9.0` |
| `!=` | Exclude version | Skip buggy version | `mypy!=1.5.0` |

### Recommendations

**Development**:
```
# requirements-dev.txt
pytest>=7.4.3
black>=23.12.0
mypy>=1.7.1
```

**Production**:
```
# requirements.txt
requests==2.31.0
pydantic==2.5.0
httpx==0.27.2
```

**Library** (if building a library):
```
# pyproject.toml
dependencies = [
    "pydantic>=2.0,<3.0",
    "httpx>=0.27.0",
]
```

## Compatibility Verification

### Manual Testing

```bash
# 1. Create clean virtual environment
python3.11 -m venv test-env
source test-env/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests
pytest

# 4. Check for conflicts
pip check

# 5. List installed versions
pip list
```

### Automated Verification

```python
#!/usr/bin/env python3
"""Verify dependency compatibility."""

import subprocess
import sys

def check_compatibility():
    """Run compatibility checks."""
    # Check for conflicts
    result = subprocess.run(['pip', 'check'], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Dependency conflicts detected:")
        print(result.stdout)
        return False

    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required")
        return False

    print("✅ All compatibility checks passed")
    return True

if __name__ == "__main__":
    sys.exit(0 if check_compatibility() else 1)
```

## Security Considerations

### Known Vulnerabilities

Check for security advisories:

```bash
# Install safety
pip install safety

# Scan dependencies
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

### Secure Version Selection

**Always**:
- Use latest stable versions for security-critical packages (cryptography, requests, urllib3)
- Monitor security advisories (GitHub, PyPI)
- Update promptly when vulnerabilities discovered

**Never**:
- Use deprecated versions with known vulnerabilities
- Ignore security warnings
- Pin to old versions without security updates

## References

- [PyPI Package Index](https://pypi.org/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [PEP 440 - Version Identification](https://peps.python.org/pep-0440/)
- [pydantic Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [GitHub Security Advisories](https://github.com/advisories)

---

**Version**: 2.0.0
**Last Updated**: 2025-10-29
**Maintained By**: Feature-Implementer v2
