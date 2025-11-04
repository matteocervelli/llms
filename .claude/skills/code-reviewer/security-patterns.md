---
name: security-patterns
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Security Patterns and Best Practices

This document provides comprehensive security patterns, common vulnerabilities, and best practices for secure coding.

---

## OWASP TOP 10 (2021)

### A01: Broken Access Control

**Description:** Restrictions on what authenticated users can do are not properly enforced.

#### Common Vulnerabilities
- Missing authorization checks
- Horizontal privilege escalation (accessing other users' data)
- Vertical privilege escalation (accessing admin functions)
- CORS misconfiguration
- Insecure direct object references (IDOR)

#### Detection Patterns
```python
# ❌ VULNERABLE: No authorization check
@app.route('/user/<user_id>/data')
def get_user_data(user_id):
    # Anyone can access any user's data
    return User.query.get(user_id).data

# ✅ SECURE: Proper authorization
@app.route('/user/<user_id>/data')
@login_required
def get_user_data(user_id):
    # Check if current user can access this data
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)
    return User.query.get(user_id).data
```

#### Prevention Patterns
```python
# Pattern 1: Decorator for authorization
from functools import wraps

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403, "Insufficient permissions")
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/admin/users')
@require_permission('admin.users.view')
def list_users():
    return User.query.all()

# Pattern 2: Resource ownership check
def check_resource_ownership(resource_type, resource_id):
    resource = resource_type.query.get_or_404(resource_id)
    if resource.owner_id != current_user.id:
        abort(403, "Access denied")
    return resource

# Pattern 3: CORS configuration
from flask_cors import CORS

# Restrictive CORS (whitelist specific origins)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://trusted-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

### A02: Cryptographic Failures

**Description:** Failures related to cryptography which often lead to sensitive data exposure.

#### Common Vulnerabilities
- Weak encryption algorithms (DES, RC4, MD5, SHA1)
- Hardcoded encryption keys
- Insufficient key length
- Not using encryption for sensitive data
- Storing passwords in plaintext
- Weak random number generation

#### Detection Patterns
```python
# ❌ VULNERABLE: Weak hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ❌ VULNERABLE: Weak encryption
from Crypto.Cipher import DES
cipher = DES.new(key)  # DES is weak

# ❌ VULNERABLE: Hardcoded key
SECRET_KEY = "hardcoded_secret_123"

# ✅ SECURE: Strong password hashing
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ✅ SECURE: Strong encryption
from cryptography.fernet import Fernet
key = Fernet.generate_key()  # Properly generated key
cipher = Fernet(key)
encrypted = cipher.encrypt(data)
```

#### Prevention Patterns
```python
# Pattern 1: Password hashing with bcrypt
import bcrypt

def hash_password(password: str) -> bytes:
    """Securely hash password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)  # 12 rounds is current recommendation
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password: str, hashed: bytes) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Pattern 2: Secure encryption with Fernet
from cryptography.fernet import Fernet
import os

def get_encryption_key() -> bytes:
    """Get encryption key from environment."""
    key_base64 = os.environ.get('ENCRYPTION_KEY')
    if not key_base64:
        raise ValueError("ENCRYPTION_KEY not set in environment")
    return key_base64.encode()

def encrypt_data(data: bytes) -> bytes:
    """Encrypt data using Fernet."""
    cipher = Fernet(get_encryption_key())
    return cipher.encrypt(data)

def decrypt_data(encrypted: bytes) -> bytes:
    """Decrypt data using Fernet."""
    cipher = Fernet(get_encryption_key())
    return cipher.decrypt(encrypted)

# Pattern 3: Secure random generation
import secrets

# Generate secure random token
token = secrets.token_urlsafe(32)  # 32 bytes = 256 bits

# Generate secure random password
import string
alphabet = string.ascii_letters + string.digits + string.punctuation
password = ''.join(secrets.choice(alphabet) for _ in range(20))
```

---

### A03: Injection

**Description:** User-supplied data is not validated, filtered, or sanitized by the application.

#### Common Vulnerabilities
- SQL injection
- Command injection
- Code injection
- LDAP injection
- XML injection
- Template injection

#### Detection Patterns
```python
# ❌ VULNERABLE: SQL injection
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)

# ❌ VULNERABLE: Command injection
os.system(f"ping {user_input}")

# ❌ VULNERABLE: Code injection
eval(user_input)
exec(user_code)

# ✅ SECURE: Parameterized query
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))

# ✅ SECURE: Avoid shell commands
import subprocess
subprocess.run(['ping', '-c', '1', validated_host], check=True)
```

#### Prevention Patterns
```python
# Pattern 1: Parameterized SQL queries
from sqlalchemy import text

# Using SQLAlchemy
def get_user_by_username(username: str):
    """Safely query user by username."""
    query = text("SELECT * FROM users WHERE username = :username")
    return db.session.execute(query, {"username": username}).fetchone()

# Using raw SQL with parameters
def get_user_by_id(user_id: int):
    """Safely query user by ID."""
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Pattern 2: Safe command execution
import subprocess
import shlex

def safe_command_execution(command_args: list) -> str:
    """Execute command safely."""
    # Validate input
    if not all(isinstance(arg, str) for arg in command_args):
        raise ValueError("Invalid command arguments")

    # Use list form, not shell
    result = subprocess.run(
        command_args,
        capture_output=True,
        text=True,
        check=True,
        timeout=30
    )
    return result.stdout

# Pattern 3: Input validation and sanitization
import re

def validate_email(email: str) -> str:
    """Validate and sanitize email."""
    # Email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")
    return email.lower().strip()

def validate_alphanumeric(value: str, max_length: int = 50) -> str:
    """Validate alphanumeric input."""
    if not value.isalnum():
        raise ValueError("Value must be alphanumeric")
    if len(value) > max_length:
        raise ValueError(f"Value exceeds max length {max_length}")
    return value
```

---

### A04: Insecure Design

**Description:** Missing or ineffective control design.

#### Prevention Patterns
```python
# Pattern 1: Secure session management
from flask import session
import secrets

def create_session(user_id: int) -> str:
    """Create secure session."""
    session_id = secrets.token_urlsafe(32)
    session['user_id'] = user_id
    session['session_id'] = session_id
    session['created_at'] = time.time()
    session.permanent = True
    return session_id

def validate_session():
    """Validate session security."""
    # Check session age
    if 'created_at' in session:
        age = time.time() - session['created_at']
        if age > 3600:  # 1 hour
            session.clear()
            raise ValueError("Session expired")

    # Check session ID
    if 'session_id' not in session:
        raise ValueError("Invalid session")

# Pattern 2: Rate limiting
from functools import wraps
from time import time

rate_limit_storage = {}

def rate_limit(max_requests: int, window: int):
    """Rate limit decorator."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = f"{f.__name__}:{request.remote_addr}"
            now = time()

            # Clean old entries
            if key in rate_limit_storage:
                rate_limit_storage[key] = [
                    t for t in rate_limit_storage[key]
                    if now - t < window
                ]
            else:
                rate_limit_storage[key] = []

            # Check limit
            if len(rate_limit_storage[key]) >= max_requests:
                abort(429, "Too many requests")

            # Add request
            rate_limit_storage[key].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/api/sensitive')
@rate_limit(max_requests=10, window=60)  # 10 requests per minute
def sensitive_endpoint():
    return {"status": "ok"}
```

---

### A05: Security Misconfiguration

**Description:** Missing appropriate security hardening or improperly configured permissions.

#### Common Issues
- Default credentials still enabled
- Verbose error messages
- Unnecessary features enabled
- Missing security headers
- Outdated software

#### Prevention Patterns
```python
# Pattern 1: Security headers
from flask import Flask

def add_security_headers(app: Flask):
    """Add security headers to Flask app."""
    @app.after_request
    def set_security_headers(response):
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'

        # XSS protection
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline';"
        )

        # HTTPS enforcement
        response.headers['Strict-Transport-Security'] = (
            'max-age=31536000; includeSubDomains'
        )

        return response

# Pattern 2: Environment-based configuration
import os

class Config:
    """Secure configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set")

    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL must be set")

    # Debug mode from environment
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

    # Session configuration
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# Pattern 3: Error handling that doesn't leak info
@app.errorhandler(Exception)
def handle_error(error):
    """Handle errors securely."""
    # Log detailed error server-side
    app.logger.error(f"Error: {str(error)}", exc_info=True)

    # Return generic message to client
    if app.debug:
        # In development, show details
        return {"error": str(error)}, 500
    else:
        # In production, hide details
        return {"error": "An error occurred"}, 500
```

---

### A06: Vulnerable and Outdated Components

**Description:** Using components with known vulnerabilities.

#### Prevention Patterns
```python
# Pattern 1: Dependency checking
# In requirements.txt, pin versions
# requests==2.31.0  (instead of requests>=2.0)

# Pattern 2: Regular security audits
# Use tools like:
# - pip-audit
# - safety
# - Snyk

# Run in CI/CD:
# pip-audit --requirement requirements.txt

# Pattern 3: Automated updates
# Use dependabot or renovate bot
# .github/dependabot.yml
```

---

### A07: Identification and Authentication Failures

**Description:** Weak authentication implementation.

#### Prevention Patterns
```python
# Pattern 1: Strong password requirements
import re

def validate_password_strength(password: str) -> bool:
    """Validate password meets strength requirements."""
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")

    if not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain uppercase letter")

    if not re.search(r'[a-z]', password):
        raise ValueError("Password must contain lowercase letter")

    if not re.search(r'[0-9]', password):
        raise ValueError("Password must contain digit")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Password must contain special character")

    return True

# Pattern 2: Account lockout
from datetime import datetime, timedelta

failed_attempts = {}

def check_login_attempts(username: str):
    """Check and enforce login attempt limits."""
    if username in failed_attempts:
        attempts, lockout_until = failed_attempts[username]

        # Check if still locked out
        if lockout_until and datetime.now() < lockout_until:
            raise ValueError("Account temporarily locked. Try again later.")

        # Check attempt count
        if attempts >= 5:
            # Lock for 15 minutes
            failed_attempts[username] = (
                attempts,
                datetime.now() + timedelta(minutes=15)
            )
            raise ValueError("Too many failed attempts. Account locked.")

def record_failed_login(username: str):
    """Record failed login attempt."""
    if username not in failed_attempts:
        failed_attempts[username] = (1, None)
    else:
        attempts, _ = failed_attempts[username]
        failed_attempts[username] = (attempts + 1, None)

def clear_failed_attempts(username: str):
    """Clear failed attempts on successful login."""
    if username in failed_attempts:
        del failed_attempts[username]

# Pattern 3: Multi-factor authentication
import pyotp

def setup_mfa(user):
    """Setup MFA for user."""
    # Generate secret
    secret = pyotp.random_base32()
    user.mfa_secret = secret

    # Generate QR code URI
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name=user.email,
        issuer_name="Your App"
    )
    return uri

def verify_mfa(user, token: str) -> bool:
    """Verify MFA token."""
    if not user.mfa_secret:
        return True  # MFA not enabled

    totp = pyotp.TOTP(user.mfa_secret)
    return totp.verify(token, valid_window=1)
```

---

### A08: Software and Data Integrity Failures

**Description:** Code and infrastructure that does not protect against integrity violations.

#### Prevention Patterns
```python
# Pattern 1: Digital signatures
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

def sign_data(data: bytes, private_key) -> bytes:
    """Sign data with private key."""
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(data: bytes, signature: bytes, public_key) -> bool:
    """Verify signature with public key."""
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

# Pattern 2: File integrity checking
import hashlib

def calculate_file_hash(filepath: str) -> str:
    """Calculate SHA-256 hash of file."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def verify_file_integrity(filepath: str, expected_hash: str) -> bool:
    """Verify file hasn't been tampered with."""
    actual_hash = calculate_file_hash(filepath)
    return actual_hash == expected_hash
```

---

### A09: Security Logging and Monitoring Failures

**Description:** Without logging and monitoring, breaches cannot be detected.

#### Prevention Patterns
```python
# Pattern 1: Comprehensive security logging
import logging
from datetime import datetime

# Configure security logger
security_logger = logging.getLogger('security')
security_logger.setLevel(logging.INFO)

handler = logging.FileHandler('security.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
security_logger.addHandler(handler)

def log_security_event(event_type: str, user_id: int, details: dict):
    """Log security event."""
    security_logger.info(
        f"Security Event: {event_type} | "
        f"User: {user_id} | "
        f"Details: {details} | "
        f"Timestamp: {datetime.now().isoformat()}"
    )

# Log authentication events
def log_login_attempt(username: str, success: bool, ip: str):
    """Log login attempt."""
    log_security_event(
        'LOGIN_ATTEMPT',
        user_id=username,
        details={
            'success': success,
            'ip_address': ip,
            'timestamp': datetime.now().isoformat()
        }
    )

# Pattern 2: Monitoring sensitive operations
def monitor_sensitive_operation(operation: str):
    """Decorator to monitor sensitive operations."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                duration = time.time() - start_time

                log_security_event(
                    'SENSITIVE_OPERATION',
                    user_id=current_user.id,
                    details={
                        'operation': operation,
                        'duration': duration,
                        'success': True
                    }
                )
                return result
            except Exception as e:
                log_security_event(
                    'SENSITIVE_OPERATION_FAILED',
                    user_id=current_user.id,
                    details={
                        'operation': operation,
                        'error': str(e),
                        'success': False
                    }
                )
                raise
        return wrapped
    return decorator

@app.route('/admin/delete_user/<user_id>')
@monitor_sensitive_operation('DELETE_USER')
def delete_user(user_id):
    # Delete user logic
    pass
```

---

### A10: Server-Side Request Forgery (SSRF)

**Description:** Web application fetches a remote resource without validating the user-supplied URL.

#### Prevention Patterns
```python
# Pattern 1: URL validation
import urllib.parse
import ipaddress

ALLOWED_SCHEMES = ['http', 'https']
BLOCKED_IPS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
]

def validate_url(url: str) -> bool:
    """Validate URL is safe to fetch."""
    parsed = urllib.parse.urlparse(url)

    # Check scheme
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Scheme {parsed.scheme} not allowed")

    # Check for private/local IPs
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        for blocked in BLOCKED_IPS:
            if ip in blocked:
                raise ValueError(f"IP {ip} is not allowed")
    except ValueError:
        # Not an IP address, check hostname
        if parsed.hostname in ['localhost', '0.0.0.0']:
            raise ValueError("Localhost not allowed")

    return True

# Pattern 2: Safe URL fetching
import requests
from requests.exceptions import RequestException

def safe_fetch_url(url: str, timeout: int = 10) -> str:
    """Safely fetch URL content."""
    # Validate URL
    validate_url(url)

    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=False,  # Don't follow redirects
            headers={'User-Agent': 'YourApp/1.0'}
        )
        response.raise_for_status()
        return response.text
    except RequestException as e:
        raise ValueError(f"Failed to fetch URL: {str(e)}")
```

---

## PYTHON-SPECIFIC SECURITY

### Dangerous Functions

#### eval() and exec()
```python
# ❌ NEVER use eval() with user input
user_input = "os.system('rm -rf /')"
eval(user_input)  # DANGEROUS!

# ❌ NEVER use exec() with user input
exec(user_code)  # DANGEROUS!

# ✅ Use ast.literal_eval() for safe evaluation
import ast
data = ast.literal_eval(user_input)  # Only evaluates literals
```

#### pickle Security
```python
# ❌ NEVER unpickle untrusted data
import pickle
data = pickle.loads(untrusted_data)  # DANGEROUS!

# ✅ Use JSON instead
import json
data = json.loads(trusted_data)
```

#### XML Parsing
```python
# ❌ Vulnerable to XXE attacks
import xml.etree.ElementTree as ET
tree = ET.parse(user_file)  # DANGEROUS!

# ✅ Use defusedxml
from defusedxml import ElementTree as ET
tree = ET.parse(user_file)  # Safe
```

### Path Traversal Prevention
```python
import os
from pathlib import Path

def safe_path_join(base_dir: str, user_path: str) -> Path:
    """Safely join paths, preventing traversal."""
    # Convert to Path objects
    base = Path(base_dir).resolve()
    full_path = (base / user_path).resolve()

    # Ensure result is within base directory
    if not str(full_path).startswith(str(base)):
        raise ValueError("Path traversal attempt detected")

    return full_path
```

---

## BEST PRACTICES SUMMARY

### Input Validation
- ✅ Validate all user input
- ✅ Use whitelists, not blacklists
- ✅ Validate type, length, format, range
- ✅ Sanitize before use

### Authentication
- ✅ Use strong password hashing (bcrypt, Argon2)
- ✅ Implement MFA
- ✅ Use secure session management
- ✅ Implement account lockout

### Authorization
- ✅ Check permissions for every action
- ✅ Use principle of least privilege
- ✅ No security through obscurity

### Data Protection
- ✅ Encrypt sensitive data
- ✅ Use HTTPS
- ✅ No secrets in code
- ✅ Proper key management

### Error Handling
- ✅ Don't leak information in errors
- ✅ Log errors server-side
- ✅ Generic messages to users

### Dependencies
- ✅ Keep dependencies updated
- ✅ Regular security audits
- ✅ Use dependency scanning tools

### Logging
- ✅ Log security events
- ✅ Don't log sensitive data
- ✅ Monitor for suspicious activity

---

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org/
- Python Security: https://python.readthedocs.io/en/latest/library/security.html
- CWE Top 25: https://cwe.mitre.org/top25/
