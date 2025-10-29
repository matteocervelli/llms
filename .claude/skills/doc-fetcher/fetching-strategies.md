# Documentation Fetching Strategies

## Overview

This guide provides comprehensive strategies for fetching library and framework documentation using context7-mcp and fetch-mcp. Learn when to use each approach, how to optimize token usage, and best practices for multi-source synthesis.

---

## Strategy 1: Context7-First Approach

**Use when:**
- Library is available in context7
- Need comprehensive API reference
- Require semantic search capabilities
- Want version-specific documentation
- Need structured documentation retrieval

### Workflow

```python
# Step 1: Resolve library ID
resolution = invoke_mcp(
    "context7-mcp",
    tool="resolve-library-id",
    params={"libraryName": "fastapi"}
)

# Step 2: Fetch comprehensive docs
docs = invoke_mcp(
    "context7-mcp",
    tool="get-library-docs",
    params={
        "context7CompatibleLibraryID": resolution["library_id"],
        "topic": "API routing and dependency injection",
        "tokens": 3000
    }
)
```

### Token Optimization

**Start with focused topics:**
- Specific: `"API routing and dependency injection"` ✅
- Generic: `"everything about fastapi"` ❌

**Progressive refinement:**
```python
# First pass: Overview (1500 tokens)
overview = fetch_docs(library_id, "overview and quick start", tokens=1500)

# Second pass: Specific features (2000 tokens each)
routing = fetch_docs(library_id, "API routing patterns", tokens=2000)
validation = fetch_docs(library_id, "Pydantic integration", tokens=2000)

# Combined: 5500 tokens total with focused retrieval
```

**Token guidelines:**
- Quick reference: 1000-1500 tokens
- Single feature: 2000-2500 tokens
- Comprehensive coverage: 3000-4000 tokens
- Multiple features: Split into focused queries

### Advantages

✅ **Semantic Search:** Context-aware documentation retrieval
✅ **Structured Output:** Well-formatted, consistent documentation
✅ **Version Support:** Version-specific documentation available
✅ **Code Examples:** Includes working code snippets
✅ **Quality:** High-quality, authoritative content

### Limitations

⚠️ **Library Coverage:** Not all libraries available
⚠️ **Token Limits:** Maximum tokens per query
⚠️ **Freshness:** May not have bleeding-edge updates
⚠️ **Resolution Required:** Need to resolve library ID first

---

## Strategy 2: Fetch-First Approach

**Use when:**
- Library not available in context7
- Need latest official documentation
- Want specific documentation pages
- Require migration guides or changelogs
- Quick start guides preferred

### Workflow

```python
# Fetch official quick start
quick_start = invoke_mcp(
    "fetch-mcp",
    tool="fetch",
    params={
        "url": "https://fastapi.tiangolo.com/tutorial/first-steps/",
        "prompt": "Extract installation steps, first API example, and running instructions"
    }
)

# Fetch GitHub README
readme = invoke_mcp(
    "fetch-mcp",
    tool="fetch",
    params={
        "url": "https://github.com/tiangolo/fastapi/blob/master/README.md",
        "prompt": "Extract key features, benefits, and basic usage example"
    }
)
```

### Prompt Engineering

**Effective prompts:**
```python
# ✅ Specific and focused
"Extract quick start guide, installation steps, and first API example"

# ✅ Multi-part extraction
"Extract: 1) key features, 2) installation, 3) basic usage example"

# ✅ Contextual
"Extract error handling patterns and exception examples for FastAPI"

# ❌ Too vague
"Get information about FastAPI"

# ❌ Too broad
"Extract everything from this documentation page"
```

**Prompt patterns:**
```python
# Pattern 1: Extraction list
prompt = "Extract: 1) {feature1}, 2) {feature2}, 3) {feature3}"

# Pattern 2: Focused extraction
prompt = "Extract {topic} including code examples and best practices"

# Pattern 3: Comparative extraction
prompt = "Extract differences between {version1} and {version2}"

# Pattern 4: Problem-solution extraction
prompt = "Extract common problems and their solutions for {topic}"
```

### Advantages

✅ **Universal Access:** Any publicly available URL
✅ **Latest Content:** Always current official documentation
✅ **Flexible:** Can fetch any documentation page
✅ **No Library ID:** Direct URL access
✅ **Changelog Access:** Easy to fetch version history

### Limitations

⚠️ **Less Structured:** Output depends on prompt quality
⚠️ **No Semantic Search:** Literal content extraction only
⚠️ **Prompt Dependency:** Quality varies with prompt
⚠️ **Content Filtering:** May include irrelevant sections

---

## Strategy 3: Hybrid Approach (Recommended)

**Use for:**
- Comprehensive documentation research
- Production feature implementations
- Complex library integrations
- Version-sensitive projects

### Multi-Source Workflow

```python
def fetch_comprehensive_docs(library_name: str, topic: str) -> dict:
    """
    Fetch documentation from multiple sources using hybrid approach.
    """
    # Source 1: Context7 (primary API reference)
    try:
        library_id = resolve_library_id(library_name)
        context7_docs = fetch_via_context7(
            library_id=library_id,
            topic=topic,
            tokens=3000
        )
    except LibraryNotFoundError:
        context7_docs = None

    # Source 2: Official documentation (quick start)
    official_url = get_official_docs_url(library_name)
    official_docs = fetch_via_fetch_mcp(
        url=official_url,
        prompt=f"Extract quick start guide and {topic} examples"
    )

    # Source 3: GitHub README (overview and features)
    github_url = get_github_url(library_name)
    github_docs = fetch_via_fetch_mcp(
        url=github_url,
        prompt="Extract key features, installation, and basic usage"
    )

    # Source 4: Changelog (if version upgrade needed)
    if requires_version_migration(library_name):
        changelog_url = get_changelog_url(library_name)
        changelog = fetch_via_fetch_mcp(
            url=changelog_url,
            prompt=f"Extract changes and breaking changes since version {old_version}"
        )
    else:
        changelog = None

    # Synthesize all sources
    return {
        "library": library_name,
        "sources": {
            "context7": context7_docs,
            "official": official_docs,
            "github": github_docs,
            "changelog": changelog
        },
        "synthesized": synthesize_docs(
            context7_docs,
            official_docs,
            github_docs,
            changelog
        )
    }
```

### Source Prioritization

**Priority Order:**
1. **Context7** (if available) - Comprehensive API reference
2. **Official Documentation** - Quick start and tutorials
3. **GitHub Repository** - Latest examples and overview
4. **Changelog** - Version history and migration

**Conflict Resolution:**
If sources disagree:
1. Official documentation takes precedence
2. Context7 for API specifics
3. GitHub for latest examples
4. Document discrepancies for manual review

### Synthesis Strategy

```python
def synthesize_docs(context7, official, github, changelog):
    """
    Synthesize documentation from multiple sources into unified output.
    """
    synthesized = {
        "overview": extract_best_overview(github, official),
        "quick_start": official["quick_start"],
        "api_reference": context7["api_reference"] if context7 else official["api"],
        "code_examples": merge_examples(
            context7.get("examples", []),
            official.get("examples", []),
            github.get("examples", [])
        ),
        "best_practices": extract_best_practices(context7, official),
        "version_info": {
            "current_version": detect_version(context7, official),
            "breaking_changes": changelog.get("breaking_changes") if changelog else [],
            "migration_notes": changelog.get("migration") if changelog else None
        }
    }

    return synthesized
```

---

## Strategy 4: Version-Specific Fetching

**Use when:**
- Specific version required
- Migration from older version
- Compatibility concerns
- Breaking changes expected

### Version Detection

```python
def detect_version_requirements(analysis_doc: dict) -> dict:
    """
    Detect version requirements from analysis document.
    """
    tech_stack = analysis_doc["tech_stack"]

    return {
        "required": {
            library: parse_version_spec(spec)
            for library, spec in tech_stack["primary"].items()
        },
        "current": get_current_project_versions(),
        "migrations_needed": identify_migrations(required, current)
    }
```

### Version-Specific Retrieval

```python
# Context7: Version-specific (if supported)
docs_v2 = fetch_via_context7(
    library_id="/tiangolo/fastapi/v0.100.0",  # Specific version
    topic="API routing",
    tokens=2000
)

# Fetch: Version-specific changelog
changelog = fetch_via_fetch_mcp(
    url="https://github.com/tiangolo/fastapi/blob/master/CHANGELOG.md",
    prompt="""
    Extract all changes between version 0.95.0 and 0.100.0.
    Focus on:
    1. Breaking changes
    2. New features
    3. Deprecations
    4. Migration guidance
    """
)

# Fetch: Version-specific migration guide
migration_guide = fetch_via_fetch_mcp(
    url="https://fastapi.tiangolo.com/migration/",
    prompt="Extract migration steps from 0.95.x to 0.100.x"
)
```

### Migration Documentation

```python
def generate_migration_notes(old_version, new_version, changelog):
    """
    Generate migration notes from changelog.
    """
    return {
        "from_version": old_version,
        "to_version": new_version,
        "breaking_changes": extract_breaking_changes(changelog),
        "deprecations": extract_deprecations(changelog),
        "new_features": extract_new_features(changelog),
        "migration_steps": extract_migration_steps(changelog),
        "code_changes_required": identify_code_changes(changelog),
        "testing_recommendations": suggest_testing_approach(changelog)
    }
```

---

## Strategy 5: Caching Strategy

**Use for:**
- Reduce MCP calls
- Optimize token usage
- Improve performance
- Consistent documentation state

### Caching Implementation

```python
from datetime import datetime, timedelta
from typing import Optional

class DocumentationCache:
    """In-memory documentation cache with TTL."""

    def __init__(self, ttl_hours: int = 24):
        self.cache = {}
        self.ttl = timedelta(hours=ttl_hours)

    def get(self, key: str) -> Optional[dict]:
        """Get cached documentation if not expired."""
        if key not in self.cache:
            return None

        entry = self.cache[key]
        if datetime.utcnow() - entry["cached_at"] > self.ttl:
            # Expired
            del self.cache[key]
            return None

        return entry["data"]

    def set(self, key: str, data: dict):
        """Cache documentation with timestamp."""
        self.cache[key] = {
            "data": data,
            "cached_at": datetime.utcnow()
        }

    def invalidate(self, key: str):
        """Invalidate specific cache entry."""
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        """Clear entire cache."""
        self.cache.clear()

# Global cache instance
doc_cache = DocumentationCache(ttl_hours=24)
```

### Cache Key Strategy

```python
def generate_cache_key(library_name: str, version: str, topic: str) -> str:
    """
    Generate cache key for documentation.
    """
    import hashlib

    # Create deterministic hash from topic
    topic_hash = hashlib.md5(topic.encode()).hexdigest()[:8]

    # Cache key format: library:version:topic_hash
    return f"{library_name}:{version}:{topic_hash}"

# Usage
cache_key = generate_cache_key("fastapi", "0.100.0", "API routing and dependency injection")
# Result: "fastapi:0.100.0:a1b2c3d4"
```

### Cache Usage Pattern

```python
def fetch_with_cache(library_name: str, topic: str) -> dict:
    """
    Fetch documentation with caching.
    """
    # Detect version
    version = detect_library_version(library_name)

    # Check cache
    cache_key = generate_cache_key(library_name, version, topic)
    cached_docs = doc_cache.get(cache_key)

    if cached_docs:
        print(f"Cache HIT: {cache_key}")
        return cached_docs

    # Cache miss - fetch from sources
    print(f"Cache MISS: {cache_key}")
    docs = fetch_comprehensive_docs(library_name, topic)

    # Cache the result
    doc_cache.set(cache_key, docs)

    return docs
```

### Cache Invalidation

**When to invalidate:**
- Version change detected
- Manual refresh requested
- Cache entry expired (24 hours)
- Error in cached data

```python
# Invalidate on version change
if current_version != cached_version:
    doc_cache.invalidate(cache_key)
    docs = fetch_with_cache(library_name, topic)

# Manual refresh
if force_refresh:
    doc_cache.clear()
    docs = fetch_comprehensive_docs(library_name, topic)
```

---

## Error Handling

### Context7 Errors

```python
try:
    library_id = resolve_library_id("some-library")
    docs = fetch_via_context7(library_id, topic, tokens=3000)
except LibraryNotFoundError:
    # Fallback to fetch-mcp
    print(f"Library not found in context7, trying fetch-mcp...")
    docs = fetch_via_fetch_mcp(official_url, prompt)
except TokenLimitExceeded:
    # Reduce token count
    print(f"Token limit exceeded, reducing to 2000...")
    docs = fetch_via_context7(library_id, topic, tokens=2000)
```

### Fetch-MCP Errors

```python
try:
    docs = fetch_via_fetch_mcp(url, prompt)
except URLNotFoundError:
    # Try alternative URL
    print(f"URL not found, trying GitHub...")
    docs = fetch_via_fetch_mcp(github_url, prompt)
except NetworkError:
    # Retry with exponential backoff
    docs = retry_with_backoff(fetch_via_fetch_mcp, url, prompt)
```

### Graceful Degradation

```python
def fetch_with_fallback(library_name: str, topic: str) -> dict:
    """
    Fetch documentation with multiple fallback strategies.
    """
    strategies = [
        ("context7", lambda: fetch_via_context7(library_name, topic)),
        ("official", lambda: fetch_via_fetch_mcp(official_url, prompt)),
        ("github", lambda: fetch_via_fetch_mcp(github_url, prompt)),
        ("cache", lambda: get_stale_cache(library_name, topic))  # Last resort
    ]

    for strategy_name, fetch_func in strategies:
        try:
            docs = fetch_func()
            if docs:
                print(f"Success with strategy: {strategy_name}")
                return docs
        except Exception as e:
            print(f"Strategy {strategy_name} failed: {e}")
            continue

    # All strategies failed
    raise DocumentationUnavailableError(
        f"Unable to fetch documentation for {library_name}"
    )
```

---

## Performance Optimization

### Parallel Fetching

```python
import asyncio

async def fetch_all_sources_parallel(library_name: str, topic: str) -> dict:
    """
    Fetch from multiple sources in parallel.
    """
    # Create fetch tasks
    tasks = [
        fetch_context7_async(library_name, topic),
        fetch_official_async(library_name, topic),
        fetch_github_async(library_name),
    ]

    # Execute in parallel
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    context7_docs, official_docs, github_docs = results

    return {
        "context7": context7_docs if not isinstance(context7_docs, Exception) else None,
        "official": official_docs if not isinstance(official_docs, Exception) else None,
        "github": github_docs if not isinstance(github_docs, Exception) else None
    }
```

### Token Budget Management

```python
def allocate_token_budget(libraries: list, total_budget: int = 10000) -> dict:
    """
    Allocate token budget across multiple libraries.
    """
    priority_weights = {
        "primary": 0.5,      # 50% of budget
        "dependencies": 0.3,  # 30% of budget
        "testing": 0.2       # 20% of budget
    }

    allocation = {}
    for category, weight in priority_weights.items():
        category_libs = [lib for lib in libraries if lib["category"] == category]
        tokens_per_lib = int((total_budget * weight) / len(category_libs))

        for lib in category_libs:
            allocation[lib["name"]] = tokens_per_lib

    return allocation
```

---

**Version:** 2.0.0
**Last Updated:** 2025-10-29
**Maintainer:** Documentation Researcher Agent
