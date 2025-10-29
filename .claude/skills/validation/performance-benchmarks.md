# Performance Benchmarks and Criteria

## Overview

This document defines performance standards and benchmarks for features in the LLM Configuration Management project. Use these criteria during validation to ensure acceptable performance.

---

## Performance Categories

### 1. Response Time (Latency)

**Definition:** Time from request initiation to response completion

**Target Metrics:**
- **p50 (Median):** < 50ms
- **p95:** < 200ms
- **p99:** < 500ms
- **Max:** < 1000ms

**Measurement:**
```python
import time

start = time.time()
result = operation()
duration = time.time() - start

assert duration < 0.2, f"Operation took {duration}s, expected < 0.2s"
```

**Priority:**
- **Critical Operations:** p95 < 100ms (e.g., read operations, queries)
- **Standard Operations:** p95 < 200ms (e.g., create, update)
- **Complex Operations:** p95 < 500ms (e.g., batch operations, complex queries)

---

### 2. Throughput

**Definition:** Number of operations per second

**Target Metrics:**
- **Read Operations:** > 1000 ops/sec
- **Write Operations:** > 500 ops/sec
- **Complex Operations:** > 100 ops/sec

**Measurement:**
```python
import time

operations = 1000
start = time.time()

for _ in range(operations):
    operation()

duration = time.time() - start
throughput = operations / duration

assert throughput > 500, f"Throughput: {throughput} ops/s, expected > 500"
```

---

### 3. Resource Usage

#### Memory Usage

**Target Metrics:**
- **Base Memory:** < 50MB
- **Peak Memory:** < 100MB per operation
- **Memory Growth:** < 10MB per 1000 operations

**Measurement:**
```python
import tracemalloc

tracemalloc.start()
operation()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

peak_mb = peak / 1024 / 1024
assert peak_mb < 100, f"Peak memory: {peak_mb}MB, expected < 100MB"
```

#### CPU Usage

**Target Metrics:**
- **Single Operation:** < 50% of single core
- **Batch Operations:** < 80% of single core
- **Sustained Load:** < 60% average

**Measurement:**
```bash
# Use psutil or time command
/usr/bin/time -l python script.py
```

---

### 4. Database/File System Performance

#### Query Performance

**Target Metrics:**
- **Simple Query:** < 10ms
- **Join Query:** < 50ms
- **Complex Query:** < 200ms
- **Queries per Operation:** < 5

**Best Practices:**
- Use indexes for frequently queried fields
- Batch queries where possible
- Use query profiling to identify slow queries
- Implement query caching for repeated queries

#### File I/O Performance

**Target Metrics:**
- **Small File (<100KB):** < 10ms
- **Medium File (100KB-1MB):** < 50ms
- **Large File (>1MB):** Stream, don't load entirely

**Best Practices:**
- Use `pathlib` for path operations
- Stream large files with generators
- Batch file operations where possible
- Use appropriate buffer sizes

---

## Feature-Specific Benchmarks

### CLI Commands

**Target Metrics:**
- **Startup Time:** < 100ms
- **Simple Command:** < 200ms total
- **Complex Command:** < 1000ms total

**Example:**
```bash
# Measure CLI performance
time python -m src.tools.skill_builder.main create --name test

# Expected: real < 0.2s
```

---

### File Operations

#### Creating Skills/Commands/Agents

**Target Metrics:**
- **Create Single Item:** < 100ms
- **Create with Templates:** < 200ms
- **Batch Create (10 items):** < 1000ms

**Breakdown:**
- Template loading: < 20ms
- Validation: < 30ms
- File writing: < 50ms
- Total: < 100ms

---

### Template Processing

**Target Metrics:**
- **Simple Template:** < 10ms
- **Complex Template:** < 50ms
- **Template with Substitutions:** < 100ms

**Jinja2 Rendering:**
```python
from jinja2 import Template

# Should complete in < 50ms for typical templates
template = Template(template_string)
result = template.render(**context)
```

---

### Validation Operations

**Target Metrics:**
- **Input Validation:** < 5ms
- **File Validation:** < 20ms
- **Security Validation:** < 50ms

**Pydantic Validation:**
```python
from pydantic import BaseModel

# Should complete in < 5ms for typical models
model = ConfigModel(**data)
```

---

## Performance Testing

### Unit Performance Tests

```python
import pytest
import time

def test_operation_performance():
    """Verify operation meets performance requirement."""
    iterations = 100
    start = time.time()

    for _ in range(iterations):
        result = operation()

    duration = time.time() - start
    avg_time = duration / iterations

    assert avg_time < 0.05, f"Average time: {avg_time}s, expected < 0.05s"
```

### Load Testing

```python
import concurrent.futures
import time

def test_concurrent_load():
    """Test performance under concurrent load."""
    workers = 10
    operations_per_worker = 100

    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(run_operations, operations_per_worker)
            for _ in range(workers)
        ]
        concurrent.futures.wait(futures)

    duration = time.time() - start
    total_ops = workers * operations_per_worker
    throughput = total_ops / duration

    assert throughput > 500, f"Throughput: {throughput} ops/s, expected > 500"
```

### Profiling

```python
import cProfile
import pstats

# Profile operation
profiler = cProfile.Profile()
profiler.enable()

operation()

profiler.disable()

# Analyze results
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

---

## Performance Optimization Strategies

### 1. Caching

**When to Cache:**
- Frequently accessed data
- Expensive computations
- Static or rarely-changing data

**Caching Strategies:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(param):
    """Cached expensive operation."""
    pass

# Or use instance-level caching
class Service:
    def __init__(self):
        self._cache = {}

    def get_data(self, key):
        if key not in self._cache:
            self._cache[key] = fetch_data(key)
        return self._cache[key]
```

---

### 2. Lazy Loading

**Delay Loading Until Needed:**
```python
class Resource:
    def __init__(self):
        self._data = None

    @property
    def data(self):
        """Lazy load data."""
        if self._data is None:
            self._data = load_expensive_data()
        return self._data
```

---

### 3. Batching

**Batch Operations:**
```python
# Bad: Individual operations
for item in items:
    save(item)  # N database calls

# Good: Batch operation
save_batch(items)  # 1 database call
```

---

### 4. Streaming

**Stream Large Data:**
```python
# Bad: Load entire file
data = file.read()  # Loads entire file into memory

# Good: Stream file
for line in file:
    process(line)  # Processes one line at a time
```

---

### 5. Indexing

**Database Indexes:**
```sql
-- Create index for frequently queried field
CREATE INDEX idx_name ON table(name);

-- Composite index for multi-field queries
CREATE INDEX idx_name_created ON table(name, created_at);
```

---

### 6. Connection Pooling

**Reuse Connections:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Connection pool
engine = create_engine(
    'postgresql://...',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

## Performance Monitoring

### Metrics to Track

1. **Response Time:** p50, p95, p99
2. **Throughput:** ops/sec
3. **Error Rate:** errors/sec
4. **Resource Usage:** CPU %, memory MB
5. **Queue Depth:** pending operations
6. **Database Metrics:** query time, connection pool usage

### Monitoring Tools

```python
import logging
import time

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor operation performance."""

    @staticmethod
    def monitor(operation_name):
        """Decorator to monitor operation performance."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start
                    logger.info(
                        f"{operation_name} completed in {duration:.3f}s"
                    )
                    return result
                except Exception as e:
                    duration = time.time() - start
                    logger.error(
                        f"{operation_name} failed after {duration:.3f}s: {e}"
                    )
                    raise
            return wrapper
        return decorator

# Usage
@PerformanceMonitor.monitor("create_skill")
def create_skill(name):
    pass
```

---

## Performance Regression Testing

### Baseline Establishment

```python
import pytest

# Store baseline performance
BASELINE_PERFORMANCE = {
    "create_skill": 0.1,  # seconds
    "validate_input": 0.01,
    "render_template": 0.05,
}

def test_performance_regression():
    """Ensure performance hasn't regressed."""
    operation_time = measure_operation()
    baseline = BASELINE_PERFORMANCE["operation"]

    # Allow 10% variance
    assert operation_time < baseline * 1.1, \
        f"Performance regression: {operation_time}s > {baseline}s"
```

---

## Performance Troubleshooting

### Slow Operations Checklist

- [ ] Profile with cProfile to identify hotspots
- [ ] Check for N+1 query problems
- [ ] Verify indexes on database tables
- [ ] Check for unnecessary data loading
- [ ] Review algorithm complexity (O(n²) vs O(n))
- [ ] Check for blocking I/O operations
- [ ] Verify connection pooling configured
- [ ] Check for memory leaks
- [ ] Review logging overhead (debug logging in prod?)
- [ ] Check for inefficient serialization/deserialization

### Memory Issues Checklist

- [ ] Profile with tracemalloc or memory_profiler
- [ ] Check for large data structures in memory
- [ ] Verify generators used for large datasets
- [ ] Check for circular references
- [ ] Review caching strategy (LRU limits?)
- [ ] Check for file handles not closed
- [ ] Verify cleanup in destructors/context managers
- [ ] Review object lifetimes and references

---

## Performance Acceptance Criteria

### Minimum Standards

**For Feature to Pass Validation:**
- [ ] Response time meets targets (p95)
- [ ] Throughput meets minimums
- [ ] Memory usage within bounds
- [ ] No memory leaks detected
- [ ] CPU usage reasonable
- [ ] Database queries optimized
- [ ] No obvious performance issues

### Performance Testing Required

- [ ] Unit performance tests written
- [ ] Load tests run (if applicable)
- [ ] Profiling completed
- [ ] Bottlenecks identified and addressed
- [ ] Performance benchmarks documented
- [ ] Regression tests in place

---

## Performance Report Template

```markdown
# Performance Report: [Feature Name]

## Summary
**Status:** ✅ Pass / ⚠️ Warning / ❌ Fail

## Metrics

### Response Time
- p50: XXms (target: < 50ms)
- p95: XXms (target: < 200ms)
- p99: XXms (target: < 500ms)

### Throughput
- Operations/sec: XXX (target: > 500)

### Resource Usage
- Peak Memory: XXmb (target: < 100MB)
- CPU Usage: XX% (target: < 50%)

### Database
- Avg Query Time: XXms (target: < 50ms)
- Queries per Operation: X (target: < 5)

## Bottlenecks Identified
1. [Description]: [Impact] - [Resolution]

## Optimizations Applied
1. [Optimization]: [Before] → [After]

## Recommendations
- [Recommendation 1]
- [Recommendation 2]
```

---

## References

- [Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)
- [Profiling Python Code](https://docs.python.org/3/library/profile.html)
- [SQLAlchemy Performance](https://docs.sqlalchemy.org/en/14/faq/performance.html)
- [High Performance Python](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
