---
issue: { N }
date: { YYYY-MM-DD }
status: draft
codebase_map: docs/codebase/
---

# {Feature Name} — Spec (Issue #{N})

## Context

{Why this is needed. What it unblocks. 2-3 sentences max.}

## Schema — `{table_name}`

| Column | Type | Nullable | Default           | Constraints |
| ------ | ---- | -------- | ----------------- | ----------- |
| `id`   | UUID | NO       | gen_random_uuid() | PK          |
| ...    |      |          |                   |             |

**Relationship strategy:** {adjacency list / closure table / etc.} — {rationale}
**Deferred:** {explicit list of what is NOT in scope}

> Assumed: {any assumption made in fast mode}

## Requirements

- GOAL-01: {atomic, testable requirement}
- GOAL-02: ...

## API Contract

| Method | Path                   | Body             | Response          | Notes             |
| ------ | ---------------------- | ---------------- | ----------------- | ----------------- |
| GET    | `/api/{resource}`      | —                | `list[{Schema}]`  | query params: ... |
| POST   | `/api/{resource}`      | `{CreateSchema}` | `{Schema}` 201    |                   |
| GET    | `/api/{resource}/{id}` | —                | `{Schema}` \| 404 |                   |
| PATCH  | `/api/{resource}/{id}` | `{UpdateSchema}` | `{Schema}` \| 404 | exclude_unset     |
| DELETE | `/api/{resource}/{id}` | —                | 204 \| 404        |                   |

## File Manifest

### {Repo A} ({N} files)

| File                  | Change                |
| --------------------- | --------------------- |
| `path/to/file.py`     | new                   |
| `path/to/existing.py` | edit — {what changes} |

### {Repo B} ({N} files)

| File | Change |
| ---- | ------ |

## Design Decisions

- **{Decision}**: {choice} — {rationale}. Alternatives considered: {alt1}, {alt2}.
  > Assumed: {if fast mode}
