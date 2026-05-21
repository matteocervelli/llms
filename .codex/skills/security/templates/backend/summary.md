# Backend Security — L1 Essentials

**Stack**: FastAPI + SQLAlchemy + asyncpg + Redis | Multi-tenant SaaS, GDPR

| Control          | Requirement                                           |
| ---------------- | ----------------------------------------------------- |
| Password hashing | Argon2id (not bcrypt, not SHA)                        |
| Sessions         | Redis + `secrets.token_urlsafe(32)`                   |
| Cookies          | `__Host-session`, httponly, secure, samesite=strict   |
| CSRF             | Signed tokens tied to session                         |
| Input validation | Pydantic `extra="forbid"` on all models               |
| SQL safety       | ORM only — no `text(f"...")` or string interpolation  |
| Tenant isolation | tenant_id from session middleware, never from request |
| Secrets          | Pydantic SecretStr, secrets manager CLI at deploy           |
| Error responses  | Generic messages + error_id, no stack traces          |

**Deeper**: Ask for patterns (Don't/Do/Best) or full SOP.
