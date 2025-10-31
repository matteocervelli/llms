# Language Feature Map

Language-specific features, capabilities, and performance characteristics for Python, TypeScript, and Rust.

## Python Features & Capabilities

### Language Version Features

**Python 3.10+ (Recommended)**:
- ✅ Structural pattern matching (`match`/`case`)
- ✅ Improved error messages
- ✅ Type unions with `|` (e.g., `int | str`)
- ✅ Parameter specification variables

**Python 3.11+ (Current)**:
- ✅ Exception groups and `except*`
- ✅ 10-60% performance improvement
- ✅ Better error locations
- ✅ `Self` type annotation

**Python 3.12+**:
- ✅ Per-interpreter GIL
- ✅ Improved f-string performance
- ✅ Type parameter syntax

### Async/Await Capabilities

**Async I/O**:
```python
# Async function definition
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com")
        return response.json()

# Concurrent execution
results = await asyncio.gather(
    fetch_data(),
    fetch_data(),
    fetch_data()
)
```

**Performance**:
- 10-100x more concurrent connections vs sync
- Best for I/O-bound operations
- Not beneficial for CPU-bound tasks

**Limitations**:
- Requires async-aware libraries
- More complex error handling
- Debugging can be harder

### Type System

**Type Hints** (Python 3.9+):
```python
from typing import Optional, Union, List, Dict

def process_data(
    items: List[Dict[str, any]],
    timeout: Optional[float] = None
) -> Union[str, None]:
    ...
```

**Pydantic for Runtime Validation**:
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    email: str = Field(..., regex=r".+@.+\..+")
    age: int = Field(..., ge=0, le=150)
```

**mypy for Static Type Checking**:
- Catches type errors before runtime
- 80-90% bug reduction in typed code
- CI/CD integration recommended

### Performance Characteristics

**Strengths**:
- Rapid development (2-5x faster than statically typed languages)
- Rich library ecosystem
- Excellent for prototyping

**Weaknesses**:
- Slower than compiled languages (10-100x)
- GIL limits CPU-bound parallelism
- Higher memory usage

**Performance Optimization**:
- Use numpy/pandas for numerical operations (100x speedup)
- Cython for critical paths (10-50x speedup)
- PyPy for long-running services (2-5x speedup)
- Async for I/O-bound operations (10-100x concurrency)

### Concurrency Models

**Async/Await** (I/O-bound):
- Single-threaded event loop
- Best for: API calls, database queries, file I/O
- Handles 10,000+ concurrent connections

**Threading** (I/O-bound with libraries):
- Limited by GIL for Python code
- Works well with C extensions (numpy, requests)
- Best for: blocking I/O with non-Python libraries

**Multiprocessing** (CPU-bound):
- True parallelism (separate Python interpreters)
- Higher memory overhead
- Best for: data processing, computation

**Example Use Cases**:
- **API Server**: Async (FastAPI)
- **Data Processing**: Multiprocessing (pandas parallel)
- **Web Scraping**: Threading or Async
- **ML Training**: Multiprocessing or specialized libraries

---

## TypeScript/JavaScript Features & Capabilities

### Language Features

**Modern JavaScript (ES2020+)**:
- ✅ Optional chaining (`?.`)
- ✅ Nullish coalescing (`??`)
- ✅ Private fields (`#private`)
- ✅ BigInt for large integers
- ✅ Dynamic import (`import()`)

**TypeScript 5.0+**:
- ✅ Decorators (stable)
- ✅ const type parameters
- ✅ Improved module resolution
- ✅ Better inference

### Type System

**TypeScript Types**:
```typescript
// Advanced types
type User = {
  id: number;
  email: string;
  role: 'admin' | 'user';
};

// Generics
function identity<T>(arg: T): T {
  return arg;
}

// Utility types
type Partial<User> = {
  id?: number;
  email?: string;
  role?: 'admin' | 'user';
};
```

**Strengths**:
- Structural typing (duck typing)
- Powerful type inference
- Gradual typing (can adopt incrementally)

### Async/Await

**Promise-based Concurrency**:
```typescript
// Async function
async function fetchData(): Promise<Data> {
  const response = await fetch('https://api.example.com');
  return response.json();
}

// Parallel execution
const [data1, data2, data3] = await Promise.all([
  fetchData(),
  fetchData(),
  fetchData()
]);
```

**Performance**:
- Single-threaded event loop (like Python async)
- Excellent for I/O-bound operations
- Handles 10,000+ concurrent connections

### Performance Characteristics

**Strengths**:
- Fast startup time
- Low memory footprint
- Good runtime performance (V8 JIT)
- Excellent for real-time applications

**Weaknesses**:
- Single-threaded (CPU-bound tasks block event loop)
- No true parallelism (except Worker Threads)
- Memory leaks can be harder to track

**Optimization**:
- Worker Threads for CPU-bound tasks
- Clustering for multi-core utilization
- Caching and memoization
- Stream processing for large data

### Concurrency Models

**Event Loop** (Default):
- Non-blocking I/O
- Callbacks, Promises, Async/Await
- Best for: Web servers, APIs, real-time apps

**Worker Threads** (CPU-bound):
- True parallelism
- Message passing between threads
- Best for: Heavy computation, image processing

**Clustering** (Scaling):
- Multiple Node.js processes
- Load balancing across cores
- Best for: Production servers

---

## Rust Features & Capabilities

### Language Features

**Ownership System**:
```rust
// Ownership rules prevent data races at compile time
fn main() {
    let s = String::from("hello");
    takes_ownership(s);
    // s is no longer valid here
}
```

**Pattern Matching**:
```rust
match result {
    Ok(value) => println!("Success: {}", value),
    Err(e) => println!("Error: {}", e),
}
```

**Zero-Cost Abstractions**:
- Abstractions compile to same code as hand-written
- No runtime overhead for safety

### Type System

**Strong Static Typing**:
```rust
// Type inference
let x = 5; // i32 inferred

// Explicit types
let y: u32 = 42;

// Generics
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    &list[0]
}
```

**Trait System**:
- Similar to interfaces/type classes
- Compile-time polymorphism
- No runtime cost

### Async/Await

**Tokio Runtime**:
```rust
#[tokio::main]
async fn main() {
    let response = reqwest::get("https://api.example.com")
        .await
        .unwrap();
    println!("{:?}", response);
}
```

**Performance**:
- Fastest async runtime
- Zero-cost futures
- 100,000+ concurrent tasks on single thread

### Performance Characteristics

**Strengths**:
- C/C++ level performance
- Memory safety without GC
- Fearless concurrency
- Predictable performance

**Weaknesses**:
- Steep learning curve
- Slower compilation
- Smaller ecosystem than Python/JS

**When to Use**:
- Performance-critical code (50-100x faster than Python)
- Low-level systems programming
- Resource-constrained environments
- Safety-critical applications

### Concurrency Models

**Async/Await** (Tokio):
- Best for I/O-bound operations
- Single-threaded or multi-threaded runtime
- Zero-cost abstractions

**Threads**:
- True parallelism
- Ownership prevents data races
- Best for CPU-bound parallel work

**Channels**:
- Message passing between threads
- mpsc (multi-producer, single-consumer)
- Safe concurrent communication

---

## Performance Comparison Matrix

### Startup Time

| Language | Cold Start | Warm Start | Notes |
|----------|------------|------------|-------|
| Python | 50-200ms | 10-50ms | Import time matters |
| Node.js | 20-100ms | 5-20ms | Fast startup |
| Rust | 5-20ms | 1-5ms | Fastest |

### Memory Usage (Idle API Server)

| Language | Memory | Notes |
|----------|--------|-------|
| Python | 30-50MB | Interpreter overhead |
| Node.js | 20-40MB | V8 overhead |
| Rust | 5-15MB | Minimal overhead |

### CPU-Bound Task (Image Processing)

| Language | Time | Relative |
|----------|------|----------|
| Python (pure) | 10.0s | 100x |
| Python (NumPy) | 0.5s | 5x |
| Node.js | 2.0s | 20x |
| Rust | 0.1s | 1x (baseline) |

### I/O-Bound Task (1000 HTTP Requests)

| Language | Time | Concurrent | Notes |
|----------|------|------------|-------|
| Python (sync) | 100s | 1 | Sequential |
| Python (async) | 2s | 1000 | FastAPI/httpx |
| Node.js | 1.5s | 1000 | Native async |
| Rust (tokio) | 1s | 1000 | Fastest async |

---

## Best Practices by Language

### Python Best Practices

**Type Hints**:
```python
# Always use type hints for public APIs
def process_user(user_id: int) -> Optional[User]:
    ...
```

**Async for I/O**:
```python
# Use async for I/O-bound operations
async def fetch_data():
    async with httpx.AsyncClient() as client:
        return await client.get(url)
```

**Error Handling**:
```python
# Specific exceptions, not bare except
try:
    result = process_data()
except ValueError as e:
    logger.error(f"Invalid data: {e}")
except Exception as e:
    logger.exception("Unexpected error")
    raise
```

### TypeScript Best Practices

**Strict Mode**:
```typescript
// Enable strict mode in tsconfig.json
{
  "compilerOptions": {
    "strict": true
  }
}
```

**Avoid `any`**:
```typescript
// Use specific types or unknown
function process(data: unknown): Result {
  if (typeof data === 'string') {
    return parse(data);
  }
  throw new Error('Invalid data');
}
```

**Use Promise Patterns**:
```typescript
// Always handle promise rejections
fetchData()
  .then(data => process(data))
  .catch(error => logger.error(error));

// Or with async/await
try {
  const data = await fetchData();
  process(data);
} catch (error) {
  logger.error(error);
}
```

### Rust Best Practices

**Error Handling**:
```rust
// Use Result for recoverable errors
fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}
```

**Ownership**:
```rust
// Clone only when necessary, prefer borrowing
fn process_string(s: &str) {
    // Read-only access, no ownership transfer
}
```

**Pattern Matching**:
```rust
// Exhaustive pattern matching
match result {
    Ok(value) => process(value),
    Err(e) => handle_error(e),
}
```

---

**Usage**: Reference this map when evaluating language suitability and implementing language-specific optimizations.
