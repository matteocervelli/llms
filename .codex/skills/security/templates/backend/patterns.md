# Backend Security — Key Patterns (Don't/Do/Best)

## Password Hashing

**Don't:** `hashlib.sha256(password.encode()).hexdigest()`
**Do:** `CryptContext(schemes=["bcrypt"], deprecated="auto")`
**Best:** Argon2id with memory_cost=65536, time_cost=3, parallelism=4

## Session Storage

**Don't:** Predictable IDs like `f"user_{user_id}_{timestamp}"`
**Do:** `secrets.token_urlsafe(32)` + Redis with TTL
**Best:** Redis sessions with rotation, device tracking, concurrent limits (max 5/user)

## Cookies

**Don't:** `response.set_cookie("session_id", session_id)` (no flags)
**Best:** `__Host-session` prefix, httponly=True, secure=True, samesite="strict"

## Multi-Tenant Authorization

**Don't:** `tenant_id` from request body/query params
**Do:** Extract tenant from session middleware, inject into request.state
**Best:** AuthContext dependency with ContextVar + permission-based access control

## Input Validation

**Don't:** `async def create_user(data: dict)` or `extra = "allow"`
**Do:** Pydantic with `extra = "forbid"`, EmailStr, Field constraints
**Best:** Reusable SafeString/SafeName types + field_validator sanitization (bleach)

## SQL Injection Prevention

**Don't:** `text(f"SELECT * FROM users WHERE email = '{email}'")`
**Do:** ORM queries `select(User).where(User.email == email)` or bound params
**Best:** TenantSafeQuery class with automatic tenant_id filtering on all queries

## Secrets Management

**Don't:** Hardcoded `API_KEY = "sk-1234..."` or .env in git
**Do:** `os.environ["DATABASE_URL"]`
**Best:** pydantic_settings BaseSettings with SecretStr + secrets manager CLI at deploy time

## Error Handling

**Don't:** Return `str(exc)` + `traceback.format_exc()` to client
**Do:** Generic error with `error_id = uuid4()[:8]`, log full trace server-side
**Best:** structlog with PIIFilter (redact password/token/email fields automatically)

## CSRF Protection

**Best:** Signed CSRF tokens: `hmac(session_id:timestamp, secret_key)`, validate age + signature

## Rate Limiting

**Don't:** No rate limiting or in-memory only (doesn't scale)
**Do:** Redis `INCR` with fixed window
**Best:** Sliding window via sorted sets, separate limits for login (10/hr/IP), general (100 RPM)

**Full SOP**: Ask for complete backend security SOP with all code examples.
