---
description: Implement production-ready infrastructure with security and performance
allowed-tools: [git, filesystem, sequential-thinking-mcp, context7-mcp]
---

# Infrastructure Setup: $ARGUMENTS

**💡 Tip:** For safer planning, activate Plan Mode (press Shift+Tab twice) before running this command to review the infrastructure strategy before execution.

## Architecture Implementation

```bash
!git checkout -b infrastructure/setup
```

Use sequential-thinking-mcp to plan infrastructure based on @TECH-STACK.md requirements.

Create modular code structure:

```bash
src/
├── interfaces/     # Contracts and types
├── core/          # Business logic  
├── implementations/ # Concrete implementations
├── middleware/    # Security, logging, validation
├── config/        # Environment configuration
└── utils/         # Shared utilities
```

## Database & Persistence

### Schema Design

- Create migration files with proper indexing
- Implement connection pooling and query optimization
- Add database health checks and monitoring

### ORM/Database Layer

**TypeScript + Prisma:**

```bash
!npx prisma init
# Configure schema with security constraints
!npx prisma migrate dev --name init
```

**Python + SQLAlchemy:**

```bash
!alembic init alembic
!alembic revision --autogenerate -m "Initial migration"
```

## API & Security Layer

### Authentication & Authorization

- Implement JWT/session-based auth
- Add role-based access control (RBAC)
- Configure password hashing and validation
- Setup rate limiting and request validation

### Security Middleware

- Input sanitization and validation
- Security headers (CORS, CSP, HSTS)
- API rate limiting and throttling
- Request/response logging for audit

### Input Validation

**TypeScript + Zod:**

```typescript
// Schemas with security validation
export const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(2).max(100).regex(/^[a-zA-Z\s]+$/),
});
```

**Python + Pydantic:**

```python
# Type-safe validation with security
class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
```

## Performance & Caching

### Caching Strategy

- Implement Redis/in-memory caching
- Add query result caching with TTL
- Setup cache invalidation patterns
- Configure cache monitoring

### Performance Optimization

- Database query optimization with proper indexing
- Response compression and minification
- Async/await implementation for I/O operations
- Connection pooling configuration

## Monitoring & Observability

### Structured Logging

```typescript
// JSON logging with correlation IDs
export const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  )
});
```

### Health Checks & Metrics

- Application health endpoints
- Database connectivity checks
- Memory and CPU usage monitoring
- Custom business metrics collection

### Error Tracking

- Structured error logging
- Performance metrics (response times, throughput)
- Security event logging
- Application performance monitoring (APM)

## Testing Infrastructure

### Test Environment Setup

```bash
# Setup test database and environment
!cp .env.example .env.test
# Configure test-specific settings
```

### Testing Framework

- Unit test setup with mocking capabilities
- Integration test framework
- Security testing utilities
- Performance testing tools

## Containerization & Deployment

### Docker Configuration

```dockerfile
# Multi-stage build for optimization
FROM node:18-alpine AS builder
# ... build steps

FROM node:18-alpine AS runtime
# ... runtime configuration
```

### Environment Configuration

- Secure environment variable management
- Configuration validation at startup
- Database connection management
- Service discovery configuration

## Security Hardening

### Security Measures

```bash
# Dependency vulnerability scanning
!npm audit || safety check

# Static security analysis
!npx eslint-plugin-security || bandit -r src/
```

- Input validation at all entry points
- SQL injection prevention (parameterized queries)
- XSS protection with output encoding
- CSRF protection for web applications
- Secure session management

## Build & Deployment Verification

```bash
# Build verification
!npm run build || python -m build

# Integration tests
!npm run test:integration || pytest tests/integration/

# Security verification
!npm run test:security || pytest tests/security/

# Performance baseline
!npm run test:performance || pytest tests/performance/
```

## Documentation Update

Update infrastructure documentation:

- **Architecture diagrams** with security boundaries
- **API documentation** (OpenAPI/Swagger) with auth specs
- **Deployment guide** with security configurations
- **Troubleshooting guide** for common infrastructure issues

## Commit & Validation

```bash
!git add .
!git commit -m "feat(infrastructure): implement production-ready infrastructure

Components implemented:
- Modular architecture (interfaces → core → implementations)
- Database layer with migrations and optimization
- Authentication/authorization with JWT + RBAC
- Security middleware (validation, sanitization, rate limiting)
- Performance optimization (caching, query optimization)
- Monitoring & observability (logging, metrics, health checks)
- Testing infrastructure (unit, integration, security)
- Containerization with multi-stage builds

Security features:
- Input validation and sanitization
- SQL injection prevention
- XSS protection with security headers
- Rate limiting and request throttling
- Audit logging and security monitoring

Performance features:
- Redis caching layer
- Database query optimization
- Connection pooling
- Response compression
- Async I/O operations"

!git push origin infrastructure/setup
!gh pr create --title "Infrastructure: Production-ready setup" --body "Complete infrastructure implementation with security hardening and performance optimization"
```

## Validation Checklist

Test infrastructure components:

- [ ] Database connectivity and migrations working
- [ ] Authentication/authorization flows functional
- [ ] API endpoints responding with proper validation
- [ ] Security headers and rate limiting active
- [ ] Caching layer operational
- [ ] Monitoring and health checks reporting
- [ ] Build and deployment pipeline working
- [ ] All tests passing (unit, integration, security)
