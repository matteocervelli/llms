# Database Security — Key Patterns (Don't/Do/Best)

## Connection Security

**Don't:** `"postgresql://user:pass@localhost/db"` (no SSL, no timeouts)
**Best:** asyncpg with `ssl=require`, `statement_timeout=30000`, `lock_timeout=10000`, `idle_in_transaction_session_timeout=60000`. pg_hba.conf: `hostssl` only, reject all unmatched.

## Redis Security

**Don't:** `Redis(host="redis", port=6379)` (no password, open to network)
**Best:** requirepass + bind localhost/Docker, separate databases per purpose (sessions=0, cache=1, rate_limits=2), `rename-command FLUSHALL ""`, maxmemory with LRU eviction

## Multi-Tenant Data Isolation

**Don't:** `select(Item).where(Item.id == item_id)` (no tenant filter)
**Best:** PostgreSQL Row-Level Security with session variable:

```sql
ALTER TABLE items ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON items USING (tenant_id = current_setting('app.current_tenant_id')::INTEGER);
```

SQLAlchemy `after_begin` event sets `app.current_tenant_id` from ContextVar.

## PII Encryption

**Don't:** `email = Column(String)` (plain text PII)
**Best:** Fernet encryption with `email_hash` index for lookups. Transparent encryption via SQLAlchemy hybrid_property.

## pgvector Embedding Security

**Don't:** Embeddings without tenant_id column
**Best:** Partition by tenant (`PARTITION BY HASH (tenant_id)`), per-partition IVFFlat indexes, RLS enabled

## Database Roles

**Best:** 4 roles with least privilege: app (CRUD only, RLS enforced), readonly (SELECT only), migration (schema changes), backup (pg_read_all_data)

## Backup Security

**Best:** pg_dump → GPG encrypt → sha256 checksum → upload to B2. Encryption key from secrets manager CLI. Monthly restoration tests.

## Audit Trail

**Best:** Generic audit trigger function logging table_name, record_id, tenant_id, action, old_data, new_data, actor_user_id. Applied to sensitive tables via `CREATE TRIGGER`.

**Full SOP**: Ask for complete database security SOP with all code examples.
