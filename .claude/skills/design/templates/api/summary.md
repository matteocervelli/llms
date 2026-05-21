# API Design — Summary

## Core Approach

Design REST APIs and function contracts with clear specifications, consistent error handling, and proper authentication.

## Key Decisions

1. **Resource identification**: Nouns (plural), not verbs — `/users` not `/getUsers`
2. **HTTP methods**: GET (read), POST (create), PUT (full update), PATCH (partial), DELETE (remove)
3. **Schema design**: Separate Create/Update/Response schemas (Pydantic)
4. **Error format**: Consistent `{error, message, details, request_id}` structure
5. **Auth strategy**: JWT Bearer tokens with RBAC permission matrix
6. **Versioning**: URL path versioning (`/api/v1/`) — explicit and easy to route

## Standard Endpoint Pattern

```
POST   /api/v1/{resources}          → 201 Created
GET    /api/v1/{resources}          → 200 OK (paginated)
GET    /api/v1/{resources}/{id}     → 200 OK
PATCH  /api/v1/{resources}/{id}     → 200 OK
DELETE /api/v1/{resources}/{id}     → 204 No Content
```

## When to Go Deeper

- Ask for **patterns** → schema design patterns, auth strategies, rate limiting
- Ask for **full reference** → complete api-design-guide.md and function-design-patterns.md
