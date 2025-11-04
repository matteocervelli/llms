---
name: tech-stack-matrix
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Technology Stack Matrix

Comprehensive reference for matching requirements to appropriate technologies across Python, TypeScript, and Rust ecosystems.

## Python Technology Stack

### Web Frameworks

| Framework | Use Case | Performance | Learning Curve | Async Support | Recommendation |
|-----------|----------|-------------|----------------|---------------|----------------|
| **FastAPI** | Modern APIs, microservices | Very High | Low-Medium | ✅ Native | ⭐ APIs, real-time |
| **Django** | Full web apps, admin panels | High | Medium-High | ✅ (v3.1+) | ⭐ Full-stack |
| **Flask** | Simple APIs, prototypes | Medium | Low | ⚠️ Extensions | Small projects |
| **Tornado** | WebSockets, real-time | Very High | Medium | ✅ Native | Real-time specific |
| **Starlette** | ASGI apps, lightweight | Very High | Low | ✅ Native | Low-level control |

**Recommendation Matrix**:
- **REST API**: FastAPI (best docs, validation)
- **GraphQL**: FastAPI + Strawberry
- **Full Web App**: Django (batteries included)
- **Microservices**: FastAPI (lightweight, fast)
- **Real-time**: FastAPI or Tornado (WebSocket support)

### Database Libraries

| Library | Database | Type | Async | Performance | Recommendation |
|---------|----------|------|-------|-------------|----------------|
| **SQLAlchemy** | Multi (Postgres, MySQL, SQLite) | ORM | ✅ (v2.0+) | High | ⭐ General purpose |
| **asyncpg** | PostgreSQL | Driver | ✅ | Very High | Performance-critical |
| **psycopg3** | PostgreSQL | Driver | ✅ | High | PostgreSQL native |
| **Django ORM** | Multi | ORM | ✅ (v3.1+) | High | Django projects |
| **Tortoise ORM** | Multi | ORM | ✅ | Medium | FastAPI async |
| **Motor** | MongoDB | Driver | ✅ | High | MongoDB async |
| **redis-py** | Redis | Driver | ✅ | Very High | Caching, sessions |

**Recommendation Matrix**:
- **PostgreSQL + ORM**: SQLAlchemy 2.0+ (async support)
- **PostgreSQL + Raw**: asyncpg (highest performance)
- **MongoDB**: Motor (official async driver)
- **Redis**: redis-py (official, async support)
- **Multi-DB Support**: SQLAlchemy (abstraction layer)

### Validation & Serialization

| Library | Type | Performance | Features | Recommendation |
|---------|------|-------------|----------|----------------|
| **Pydantic** | Type-based | High | Rich, FastAPI integration | ⭐ APIs, data models |
| **marshmallow** | Schema-based | Medium | Flexible, serialization | Complex schemas |
| **cerberus** | Dict-based | High | Simple, lightweight | Simple validation |
| **jsonschema** | JSON Schema | Medium | Standard-compliant | JSON APIs |
| **attrs** | Class-based | Very High | Simple, fast | Performance-critical |

**Recommendation Matrix**:
- **FastAPI Projects**: Pydantic (native integration)
- **Django REST**: Django serializers or marshmallow
- **Complex Nested Data**: marshmallow (serialization helpers)
- **High Performance**: attrs + validators
- **JSON Schema Compliance**: jsonschema

### HTTP Clients

| Library | Async | Features | Performance | Recommendation |
|---------|-------|----------|-------------|----------------|
| **httpx** | ✅ | Modern, timeout, retries | High | ⭐ New projects |
| **requests** | ❌ | Simple, popular | Medium | Legacy, sync code |
| **aiohttp** | ✅ | Client & server | High | Advanced async |
| **urllib3** | ❌ | Low-level, connection pooling | High | Requests backend |

**Recommendation Matrix**:
- **Async Project**: httpx (modern, clean API)
- **Sync Project**: requests (simple, popular)
- **Advanced Control**: aiohttp (low-level access)
- **gRPC**: grpcio (official gRPC support)

### Task Queues & Background Processing

| Library | Broker | Features | Complexity | Performance | Recommendation |
|---------|--------|----------|------------|-------------|----------------|
| **Celery** | Redis/RabbitMQ | Mature, feature-rich | High | High | ⭐ Enterprise |
| **RQ** | Redis | Simple, Redis-only | Low | Medium | ⭐ Simple projects |
| **Dramatiq** | Redis/RabbitMQ | Reliable, simple | Medium | High | Middle ground |
| **Huey** | Redis/SQLite | Lightweight | Low | Medium | Small projects |
| **arq** | Redis | Async, minimal | Low | High | Async-first projects |

**Recommendation Matrix**:
- **Complex Workflows**: Celery (chains, chords, callbacks)
- **Simple Tasks**: RQ (easy setup, Redis-based)
- **Reliability Focus**: Dramatiq (at-least-once delivery)
- **Async Project**: arq (asyncio-native)
- **Embedded**: Huey (SQLite backend option)

### Testing Frameworks

| Library | Type | Features | Ecosystem | Recommendation |
|---------|------|----------|-----------|----------------|
| **pytest** | Unit/Integration | Fixtures, plugins, parametrize | Huge | ⭐ General purpose |
| **unittest** | Unit | Built-in, standard | Standard | Simple projects |
| **hypothesis** | Property-based | Generative testing | Medium | Complex logic |
| **pytest-asyncio** | Async testing | Async fixtures, tests | pytest | Async code |
| **playwright** | E2E | Browser automation | Growing | Web UI testing |

**Recommendation Matrix**:
- **General Testing**: pytest (best ecosystem)
- **Async Testing**: pytest + pytest-asyncio
- **Property Testing**: hypothesis (find edge cases)
- **E2E Testing**: playwright or selenium
- **Load Testing**: locust (distributed)

### File Processing

| Library | Purpose | Performance | Features | Recommendation |
|---------|---------|-------------|----------|----------------|
| **PIL/Pillow** | Images | Medium | Comprehensive | ⭐ Image processing |
| **opencv-python** | Computer vision | High | Advanced CV | Image analysis |
| **pandas** | Tabular data | High | Data analysis | ⭐ CSV/Excel |
| **openpyxl** | Excel | Medium | Read/write | Excel files |
| **reportlab** | PDF generation | Medium | Layout control | ⭐ PDF creation |
| **PyPDF2** | PDF manipulation | Medium | Merge/split | PDF editing |
| **python-docx** | Word docs | Medium | Read/write | Word files |

**Recommendation Matrix**:
- **Images**: Pillow (general) or opencv (advanced)
- **CSV/Excel**: pandas (data analysis) or openpyxl (direct)
- **PDF Generation**: reportlab (programmatic) or WeasyPrint (HTML/CSS)
- **PDF Reading**: PyPDF2 or pdfplumber
- **Word**: python-docx (official)

---

## TypeScript/JavaScript Technology Stack

### Web Frameworks

| Framework | Type | Performance | Learning Curve | Recommendation |
|-----------|------|-------------|----------------|----------------|
| **Next.js** | React meta-framework | High | Medium | ⭐ Full-stack React |
| **Remix** | React framework | High | Medium | Modern React |
| **SvelteKit** | Svelte framework | Very High | Low-Medium | Performance-focused |
| **Express** | Node.js backend | High | Low | ⭐ APIs, simple |
| **NestJS** | Node.js enterprise | High | Medium-High | Enterprise apps |
| **Fastify** | Node.js high-perf | Very High | Low-Medium | High-performance APIs |

### React Ecosystem

| Library | Purpose | Size | Popularity | Recommendation |
|---------|---------|------|------------|----------------|
| **React Query** | Data fetching | Small | Very High | ⭐ Server state |
| **Zustand** | State management | Tiny | High | ⭐ Simple state |
| **Redux Toolkit** | State management | Medium | Very High | Complex state |
| **React Hook Form** | Forms | Small | High | ⭐ Form handling |
| **React Router** | Routing | Small | Very High | ⭐ Client routing |

### TypeScript Libraries

| Library | Purpose | Features | Recommendation |
|---------|---------|----------|----------------|
| **Zod** | Validation | Type inference, runtime validation | ⭐ Type safety |
| **class-validator** | Class validation | Decorator-based | NestJS projects |
| **Yup** | Validation | Schema-based | Form validation |
| **TypeORM** | ORM | Decorators, migrations | ⭐ TypeScript ORM |
| **Prisma** | ORM | Type-safe, migrations | ⭐ Modern ORM |

---

## Rust Technology Stack

### Web Frameworks

| Framework | Type | Performance | Maturity | Recommendation |
|-----------|------|-------------|----------|----------------|
| **Axum** | Async, tokio-based | Very High | Medium | ⭐ Modern Rust |
| **Actix-web** | Actor-based | Very High | High | Mature, fast |
| **Rocket** | Ergonomic | High | High | Easy to use |
| **Warp** | Functional, filters | Very High | Medium | Composable |

### Database Libraries

| Library | Purpose | Async | Features | Recommendation |
|---------|---------|-------|----------|----------------|
| **sqlx** | SQL | ✅ | Compile-time checked queries | ⭐ Type-safe SQL |
| **diesel** | ORM | ❌ | Compile-time ORM | Mature ORM |
| **SeaORM** | ORM | ✅ | Async ORM | Async projects |

---

## Performance Comparison

### Request Handling (req/sec)

| Technology | Simple API | With Database | With Auth | Notes |
|------------|------------|---------------|-----------|-------|
| Rust (Axum) | 100,000+ | 50,000+ | 40,000+ | Fastest |
| Python (FastAPI) | 25,000+ | 15,000+ | 12,000+ | Good async |
| Python (Django) | 5,000+ | 3,000+ | 2,500+ | More features |
| Node (Fastify) | 50,000+ | 30,000+ | 25,000+ | Fast |
| Node (Express) | 15,000+ | 10,000+ | 8,000+ | Popular |

### Latency (p95, ms)

| Technology | Database Query | External API | File Upload |
|------------|----------------|--------------|-------------|
| Rust | 1-2ms | 50-100ms | 100-200ms |
| Python (async) | 5-10ms | 50-100ms | 100-200ms |
| Python (sync) | 10-20ms | 100-200ms | 200-400ms |
| Node.js | 2-5ms | 50-100ms | 100-200ms |

---

## Recommendation Decision Tree

### Choose Python When:
- ✅ Data science/ML integration needed
- ✅ Rapid development priority
- ✅ Rich library ecosystem needed
- ✅ Team familiarity with Python
- ✅ Moderate performance requirements (<10K req/s)

### Choose TypeScript/Node When:
- ✅ Full-stack JavaScript team
- ✅ Real-time features (WebSockets)
- ✅ High concurrency needed
- ✅ Fast startup time required
- ✅ NPM ecosystem preference

### Choose Rust When:
- ✅ Maximum performance required
- ✅ Low resource usage critical
- ✅ Memory safety paramount
- ✅ System-level programming needed
- ✅ Can invest in learning curve

---

**Usage**: Reference this matrix when evaluating technologies for feature requirements to match capabilities with needs.
