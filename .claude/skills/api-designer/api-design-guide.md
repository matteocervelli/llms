---
name: api-design-guide
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# API Design Guide

This guide provides comprehensive principles and best practices for designing RESTful APIs that are intuitive, maintainable, and provide excellent developer experience.

## Table of Contents

1. [REST Principles](#rest-principles)
2. [Resource Design](#resource-design)
3. [HTTP Methods](#http-methods)
4. [URL Structure](#url-structure)
5. [Request/Response Design](#requestresponse-design)
6. [Error Handling](#error-handling)
7. [Authentication and Authorization](#authentication-and-authorization)
8. [Rate Limiting](#rate-limiting)
9. [API Versioning](#api-versioning)
10. [Documentation](#documentation)

---

## REST Principles

### Core Principles

**1. Client-Server Architecture**
- Separation of concerns
- Client and server evolve independently
- Improves portability and scalability

**2. Stateless**
- Each request contains all information needed
- No session state stored on server
- Improves scalability and reliability

**3. Cacheable**
- Responses indicate if they can be cached
- Improves performance and scalability
- Use appropriate cache headers

**4. Uniform Interface**
- Resources identified by URIs
- Manipulation through representations
- Self-descriptive messages
- HATEOAS (optional)

**5. Layered System**
- Client doesn't know if connected directly to end server
- Allows load balancers, caches, proxies

**6. Code on Demand (Optional)**
- Server can send executable code
- Rarely used in modern REST APIs

---

## Resource Design

### Identifying Resources

**Resources are nouns, not verbs:**
- ✅ `/users` (resource)
- ❌ `/getUsers` (verb)

**Common Resources:**
```
/users          Collection of users
/users/{id}     Specific user
/posts          Collection of posts
/posts/{id}     Specific post
/comments       Collection of comments
```

### Resource Relationships

**Nested Resources:**
```
/users/{id}/posts           User's posts
/posts/{id}/comments        Post's comments
/projects/{id}/tasks        Project's tasks
```

**When to Nest:**
- Resource always belongs to parent
- Relationship is clear and strong
- Maximum 2-3 levels deep

**When Not to Nest:**
```
❌ /users/{id}/posts/{id}/comments/{id}/likes
Too deeply nested! Use:
✅ /comments/{id}/likes
```

### Resource Naming Conventions

**Use plural nouns:**
```
✅ /users       (plural)
❌ /user        (singular)
```

**Use kebab-case for multi-word resources:**
```
✅ /user-profiles
✅ /order-items
❌ /userProfiles (camelCase)
❌ /order_items  (snake_case)
```

**Avoid file extensions:**
```
✅ /users/123
❌ /users/123.json
```

---

## HTTP Methods

### Standard Methods

**GET - Retrieve Resource(s)**
```
GET /users           List all users
GET /users/123       Get user with ID 123

Properties:
- Safe (doesn't modify state)
- Idempotent (same result every time)
- Cacheable
```

**POST - Create Resource**
```
POST /users          Create new user

Properties:
- Not safe (modifies state)
- Not idempotent (multiple requests create multiple resources)
- Response: 201 Created with Location header
```

**PUT - Full Replace**
```
PUT /users/123       Replace user 123 entirely

Properties:
- Not safe (modifies state)
- Idempotent (same result if repeated)
- Requires all fields
```

**PATCH - Partial Update**
```
PATCH /users/123     Update specific fields of user 123

Properties:
- Not safe (modifies state)
- Idempotent (should be)
- Requires only changed fields
```

**DELETE - Remove Resource**
```
DELETE /users/123    Delete user 123

Properties:
- Not safe (modifies state)
- Idempotent (deleting twice has same effect)
- Response: 204 No Content or 200 OK
```

### Method Matrix

| Resource | GET | POST | PUT | PATCH | DELETE |
|----------|-----|------|-----|-------|--------|
| `/users` | List all | Create new | Replace all (rare) | Update all (rare) | Delete all (rare) |
| `/users/123` | Get user | - | Replace user | Update user | Delete user |

---

## URL Structure

### URL Components

```
https://api.example.com/v1/users?page=2&sort=name#section

Protocol: https
Domain: api.example.com
Version: v1
Resource: users
Query Params: page=2&sort=name
Fragment: section (client-side, not sent to server)
```

### Path Parameters

**Use for resource identification:**
```
/users/{user_id}
/projects/{project_id}/tasks/{task_id}
```

### Query Parameters

**Use for filtering, sorting, pagination:**
```
# Pagination
/users?page=2&page_size=20

# Filtering
/users?status=active&role=admin

# Sorting
/users?sort_by=created_at&sort_order=desc

# Search
/users?search=john

# Multiple filters
/products?category=electronics&min_price=100&max_price=500
```

### Best Practices

**Keep URLs simple and predictable:**
```
✅ /users/123/posts
❌ /users/123/get-all-posts-for-user
```

**Use hyphens for readability:**
```
✅ /user-profiles
❌ /userprofiles
```

**Lowercase URLs:**
```
✅ /users
❌ /Users
```

---

## Request/Response Design

### Request Body

**Use JSON for complex data:**
```json
POST /users
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe"
}
```

**Use form data for file uploads:**
```
POST /users/123/avatar
Content-Type: multipart/form-data

file: [binary data]
```

### Response Format

**Successful Response:**
```json
{
  "id": 123,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2025-10-29T10:00:00Z"
}
```

**List Response with Pagination:**
```json
{
  "items": [
    {"id": 1, "name": "User 1"},
    {"id": 2, "name": "User 2"}
  ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

**Empty Response:**
```
204 No Content
(no body)
```

### Status Codes

**2xx Success:**
```
200 OK              Successful GET, PUT, PATCH
201 Created         Successful POST (with Location header)
204 No Content      Successful DELETE
```

**4xx Client Errors:**
```
400 Bad Request              Malformed request
401 Unauthorized             Authentication required
403 Forbidden                Insufficient permissions
404 Not Found                Resource not found
409 Conflict                 Resource conflict (duplicate)
422 Unprocessable Entity     Validation error
429 Too Many Requests        Rate limit exceeded
```

**5xx Server Errors:**
```
500 Internal Server Error    Generic server error
502 Bad Gateway              Upstream server error
503 Service Unavailable      Service temporarily down
504 Gateway Timeout          Upstream timeout
```

---

## Error Handling

### Standard Error Format

```json
{
  "error": "validation_error",
  "message": "Request validation failed",
  "details": [
    {
      "field": "email",
      "message": "Invalid email format",
      "code": "invalid_format"
    },
    {
      "field": "age",
      "message": "Must be at least 13",
      "code": "min_value"
    }
  ],
  "request_id": "req_abc123xyz",
  "timestamp": "2025-10-29T10:00:00Z"
}
```

### Error Types

```
validation_error          Validation failed (400, 422)
authentication_error      Authentication failed (401)
authorization_error       Insufficient permissions (403)
not_found_error          Resource not found (404)
conflict_error           Resource conflict (409)
rate_limit_error         Rate limit exceeded (429)
internal_error           Internal server error (500)
```

### Error Response Guidelines

**1. Be Consistent**
- Same format across all endpoints
- Same field names and structure

**2. Be Specific**
- Clear error messages
- Field-level validation errors
- Error codes for programmatic handling

**3. Be Helpful**
- Suggest fixes when possible
- Link to documentation
- Provide context

**4. Be Secure**
- Don't expose implementation details
- Don't leak sensitive information
- Log full details server-side only

---

## Authentication and Authorization

### Authentication Strategies

**1. JWT (JSON Web Token)**
```
POST /api/v1/auth/login
Request:
{
  "username": "johndoe",
  "password": "secret"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer",
  "expires_in": 3600
}

Usage:
Authorization: Bearer eyJhbGciOiJIUzI1...
```

**2. API Key**
```
X-API-Key: your-api-key-here
```

**3. OAuth 2.0**
```
Authorization: Bearer oauth2-access-token
```

### Authorization Patterns

**Role-Based Access Control (RBAC):**
```
Roles: admin, manager, user, guest

Permissions Matrix:
Resource: /users
- admin: create, read, update, delete
- manager: read, update
- user: read (own only)
- guest: none
```

**Attribute-Based Access Control (ABAC):**
```
Rules based on:
- User attributes (role, department, location)
- Resource attributes (owner, visibility, sensitivity)
- Environment (time, IP address, device)

Example:
Allow if:
  user.department == resource.department
  AND current_time within business_hours
  AND user.location == "office"
```

---

## Rate Limiting

### Rate Limit Strategies

**1. Fixed Window**
```
100 requests per hour
Window resets at :00

Problem: Burst at window boundaries
```

**2. Sliding Window**
```
100 requests per rolling 60 minutes
Smoother distribution
```

**3. Token Bucket**
```
Bucket capacity: 100 tokens
Refill rate: 10 tokens/minute
Allows bursts up to capacity
```

### Rate Limit Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1730203200
X-RateLimit-Window: 3600
```

### Rate Limit Exceeded Response

```
429 Too Many Requests

{
  "error": "rate_limit_exceeded",
  "message": "Rate limit of 100 requests per hour exceeded",
  "limit": 100,
  "window": 3600,
  "reset": 1730203200,
  "retry_after": 3456
}
```

---

## API Versioning

### Versioning Strategies

**1. URL Path Versioning (Recommended)**
```
/api/v1/users
/api/v2/users

Pros: Clear, explicit, easy to route
Cons: URLs change between versions
```

**2. Header Versioning**
```
GET /api/users
Accept-Version: v1

Pros: Clean URLs, easy to add new versions
Cons: Less visible, harder to test manually
```

**3. Query Parameter**
```
/api/users?version=1

Pros: Simple, visible
Cons: Pollutes query params, easy to forget
```

### Deprecation Policy

**1. Announce Deprecation**
```
X-API-Deprecated: true
X-API-Sunset-Date: 2026-01-01
X-API-Replacement: /api/v2/users
```

**2. Provide Migration Period**
- Minimum 6-12 months notice
- Clear migration guide
- Support both versions

**3. Gradual Shutdown**
- Increase rate limits warnings
- Final sunset date
- Remove old version

---

## Documentation

### OpenAPI (Swagger) Specification

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
```

### Documentation Best Practices

**1. Provide Examples**
- Request examples
- Response examples
- Error examples

**2. Explain Authentication**
- How to obtain tokens
- How to use tokens
- Token lifecycle

**3. Document Rate Limits**
- Limits per tier
- How to check remaining
- What happens when exceeded

**4. Error Reference**
- All possible errors
- Error codes and meanings
- How to handle each error

**5. Changelog**
- Version history
- Breaking changes
- New features

---

## Summary

### Quick Reference

**Resources:**
- Use plural nouns
- Kebab-case for multi-word
- Nest max 2-3 levels

**Methods:**
- GET: Read (safe, idempotent)
- POST: Create (not idempotent)
- PUT: Full replace (idempotent)
- PATCH: Partial update (idempotent)
- DELETE: Remove (idempotent)

**Status Codes:**
- 2xx: Success
- 4xx: Client error
- 5xx: Server error

**Authentication:**
- JWT recommended
- Bearer token in header
- Secure endpoints appropriately

**Error Handling:**
- Consistent format
- Specific messages
- Field-level details

**Versioning:**
- URL path preferred
- Deprecation policy
- Migration guides

**Documentation:**
- OpenAPI/Swagger spec
- Examples for everything
- Keep updated with changes
