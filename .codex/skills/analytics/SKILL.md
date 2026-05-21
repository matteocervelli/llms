---
name: analytics
description: Run SQL queries against psql, BigQuery, or MySQL from the terminal, including natural-language-to-SQL and schema exploration. Use when analyzing data, inspecting DB state, or debugging tables. Trigger on "query the database", "SQL", "show me data from", "explore table".
user_invocable: true
---

# Analytics Helper

Help write and run database queries from the terminal.

## Usage

```
/analytics "show user signups by month"    # Natural language query
/analytics explore users                    # Explore table schema
/analytics psql                             # Set database context
/analytics connect mydb                     # Connect to named database
```

## Supported Databases

| Type       | CLI       | Connection Source                                    |
| ---------- | --------- | ---------------------------------------------------- |
| PostgreSQL | `psql`    | `$DATABASE_URL` or connection string                 |
| BigQuery   | `bq`      | `gcloud` auth (project from `$GOOGLE_CLOUD_PROJECT`) |
| MySQL      | `mysql`   | `$MYSQL_HOST`, `$MYSQL_USER`, `$MYSQL_PASSWORD`      |
| SQLite     | `sqlite3` | File path                                            |

## Commands

### Natural Language Queries

Describe what you want in plain English:

```
/analytics "count users by country"
/analytics "show orders over $100 from last month"
/analytics "find duplicate emails in customers table"
```

I'll:

1. Generate appropriate SQL
2. Show it for your approval
3. Run via CLI
4. Format output as a table

### Schema Exploration

```
/analytics explore              # List all tables
/analytics explore users        # Describe users table
/analytics explore users.email  # Show column details
```

#### PostgreSQL

```bash
psql -c "\dt"                   # List tables
psql -c "\d+ tablename"         # Describe table with details
psql -c "\di"                   # List indexes
```

#### BigQuery

```bash
bq ls dataset                   # List tables
bq show dataset.table           # Describe table
bq show --schema dataset.table  # Show schema only
```

#### MySQL

```bash
mysql -e "SHOW TABLES"
mysql -e "DESCRIBE tablename"
mysql -e "SHOW INDEX FROM tablename"
```

### Database Context

Set which database you're working with:

```
/analytics psql              # Use PostgreSQL
/analytics bq                # Use BigQuery
/analytics mysql             # Use MySQL
/analytics sqlite mydb.db    # Use SQLite file
```

Context persists for the session.

## Query Templates

### Time Series

```sql
SELECT
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as count
FROM table
GROUP BY 1
ORDER BY 1;
```

### Top N

```sql
SELECT column, COUNT(*) as count
FROM table
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
```

### Duplicates

```sql
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY count DESC;
```

### Recent Records

```sql
SELECT *
FROM table
WHERE created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC
LIMIT 100;
```

### Join Pattern

```sql
SELECT
  u.name,
  COUNT(o.id) as order_count,
  SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name
ORDER BY total_spent DESC;
```

## Safety Rules

1. **Show before run**: Always display the generated SQL before execution
2. **Read-only default**: SELECT queries run immediately after approval
3. **Mutation warning**: UPDATE/DELETE require explicit confirmation
4. **No destructive DDL**: Never run DROP, TRUNCATE without explicit user request
5. **Timeout**: Queries timeout after 30 seconds by default
6. **Row limit**: Add LIMIT 1000 to unbounded SELECTs to prevent memory issues

## Configuration

Create `~/.claude/skills/analytics/config.yaml`:

```yaml
# Named connections
connections:
  prod:
    type: psql
    url: postgres://user:pass@host:5432/dbname
  staging:
    type: psql
    url: postgres://user:pass@staging:5432/dbname
  analytics:
    type: bq
    project: my-gcp-project
    dataset: analytics

# Default connection
default: staging

# Query timeout (seconds)
timeout: 30

# Max rows to return
max_rows: 1000

# Save query history
history: true
history_file: ~/.claude/analytics_history.sql
```

## Output Formatting

Results are formatted as markdown tables:

```
| id | name | created_at |
|----|------|------------|
| 1 | Alice | 2026-01-15 |
| 2 | Bob | 2026-01-16 |

(2 rows, 0.045s)
```

For large results, offer to:

- Export to CSV
- Paginate output
- Summarize with counts

## Error Handling

- Connection failures: Show connection string (redacted) and suggest fixes
- Syntax errors: Show error position and suggest corrections
- Timeout: Offer to increase timeout or add LIMIT
- Permission denied: Suggest checking credentials or role
