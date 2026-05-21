# Database Security — L1 Essentials

**Stack**: PostgreSQL 18 + pgvector + Redis + asyncpg + SQLAlchemy | Multi-tenant, GDPR

| Control          | Requirement                                     |
| ---------------- | ----------------------------------------------- |
| PostgreSQL SSL   | `ssl=require` on all connections                |
| Auth             | scram-sha-256, not trust or md5                 |
| Redis            | requirepass + bind to localhost/Docker network  |
| Tenant isolation | tenant_id column on all user data tables        |
| RLS              | Enable Row-Level Security on tenant tables (L3) |
| PII encryption   | pgcrypto/Fernet for email, phone (L3)           |
| DB roles         | Separate app, readonly, migration, backup users |
| Timeouts         | statement_timeout=30s, lock_timeout=10s         |
| Backups          | Daily encrypted (GPG) to Backblaze B2           |
| Audit            | Triggers on sensitive tables for audit trail    |

**Deeper**: Ask for patterns (Don't/Do/Best) or full SOP.
