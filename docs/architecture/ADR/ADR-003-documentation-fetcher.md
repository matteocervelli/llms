# ADR-003: Documentation Fetcher Tool

**Status**: Accepted
**Date**: 2025-10-26
**Deciders**: Matteo Cervelli
**Issue**: [#4 Build Documentation Fetcher Tool](https://github.com/matteocervelli/llms/issues/4)

## Context

The LLM Configuration Management System needs a way to automatically fetch and maintain up-to-date documentation from multiple LLM providers (Anthropic, OpenAI, etc.). Documentation changes frequently, and manually tracking updates is inefficient and error-prone.

### Requirements

1. **Multi-Provider Support**: Fetch from multiple LLM providers
2. **Change Detection**: Only refetch when content changes
3. **Format Conversion**: Convert HTML to Markdown for consistency
4. **Manifest Tracking**: Maintain metadata about all fetched documents
5. **Rate Limiting**: Respect provider rate limits and robots.txt
6. **Security**: Prevent XSS, path traversal, and other vulnerabilities
7. **CLI Interface**: Simple commands for fetch, update, and list operations
8. **Testability**: 80%+ test coverage with comprehensive tests

### Constraints

- Must integrate with existing scope intelligence system
- Must follow 500-line limit per file
- Must use Python 3.11+ and existing dependencies
- Must respect robots.txt and rate limits
- Must be extensible for future providers

## Decision

We have decided to implement a modular Documentation Fetcher tool with the following architecture:

### Architecture Components

```
src/tools/doc_fetcher/
├── models.py          # Pydantic data models (150 lines)
├── exceptions.py      # Custom exceptions (100 lines)
├── fetcher.py         # HTTP fetching + rate limiting (200 lines)
├── converter.py       # HTML to Markdown conversion (200 lines)
├── manifest.py        # Manifest management (250 lines)
├── main.py            # CLI interface (150 lines)
└── providers/         # Provider configurations (YAML)
    ├── anthropic.yaml
    └── openai.yaml
```

### Key Design Decisions

#### 1. Pydantic for Validation

**Choice**: Use Pydantic for all data models

**Rationale**:
- Strong typing with runtime validation
- Automatic serialization/deserialization
- Clear error messages for invalid data
- Integrates well with Python 3.11+

**Alternatives Considered**:
- Dataclasses: No runtime validation
- Plain dicts: No type safety

#### 2. Token Bucket Rate Limiting

**Choice**: Implement token bucket algorithm

**Rationale**:
- Smooth rate limiting with burst capacity
- Simple to implement and understand
- Configurable rate and capacity
- Prevents provider overload

**Alternatives Considered**:
- Fixed delay: Too rigid, wastes time
- Sliding window: More complex, unnecessary

#### 3. SHA-256 for Change Detection

**Choice**: Use SHA-256 hashing for content comparison

**Rationale**:
- Fast and reliable change detection
- Collision resistance
- Standard library support
- O(1) comparison

**Alternatives Considered**:
- Last-Modified headers: Not always available
- ETag: Provider-dependent
- Content comparison: Too slow for large docs

#### 4. BeautifulSoup4 + Markdownify

**Choice**: Use BeautifulSoup4 for HTML parsing and markdownify for conversion

**Rationale**:
- Robust HTML parsing with error recovery
- Clean Markdown output
- Preserves structure and code blocks
- Mature, well-tested libraries

**Alternatives Considered**:
- html2text: Less control over output
- Custom parser: Reinventing the wheel
- Pandoc: External dependency

#### 5. YAML for Provider Configs

**Choice**: Store provider configurations in YAML files

**Rationale**:
- Human-readable and editable
- Comments support for documentation
- Easy to version control
- Standard format

**Alternatives Considered**:
- JSON: No comments, less readable
- Python files: Security risk (code execution)
- Database: Overkill for static config

#### 6. Manifest as JSON

**Choice**: Store manifest in JSON format

**Rationale**:
- Machine-readable and parsable
- Compact storage
- Standard format
- Easy integration with other tools

**Alternatives Considered**:
- SQLite: Overkill for simple key-value
- CSV: No nested structure support
- YAML: Slower parsing

#### 7. Atomic File Writes

**Choice**: Use temp file + rename for atomic writes

**Rationale**:
- Prevents corruption on failure
- POSIX atomic rename guarantee
- Simple to implement
- No external dependencies

**Alternatives Considered**:
- Direct writes: Risk of corruption
- File locking: Platform-dependent
- Database: Overkill

#### 8. Click for CLI

**Choice**: Use Click framework for CLI

**Rationale**:
- Rich CLI features (colors, progress bars)
- Automatic help generation
- Type validation
- Context management

**Alternatives Considered**:
- argparse: Less features, more boilerplate
- typer: Newer, less mature
- Custom parser: Reinventing the wheel

### Security Measures

1. **URL Validation**:
   - HTTPS only
   - Domain whitelist
   - Protocol enforcement

2. **XSS Prevention**:
   - Strip dangerous HTML attributes (onclick, etc.)
   - Remove script/style tags
   - Sanitize before conversion

3. **Path Traversal Protection**:
   - Validate local_path in ManifestEntry
   - Reject paths with ".." or absolute paths
   - Use Path objects for safety

4. **Rate Limiting**:
   - Prevent provider overload
   - Respect robots.txt
   - Exponential backoff on errors

5. **Size Limits**:
   - 10MB max response size
   - Streaming downloads to prevent memory exhaustion
   - Content-Length header checking

6. **Timeouts**:
   - 30s request timeout
   - Prevents hung connections
   - Configurable per request

### Performance Targets

- **Fetch single page**: < 5s (network dependent)
- **Convert HTML to MD**: < 500ms per page
- **Hash computation**: < 50ms per page
- **Manifest operations**: < 100ms
- **Rate limit**: Configurable, default 1 req/sec

### Testing Strategy

- **Unit tests**: Individual functions and classes
- **Integration tests**: End-to-end workflows
- **Mocking**: HTTP requests, file I/O
- **Coverage**: 80%+ minimum
- **Test categories**:
  - Models validation
  - Exceptions
  - Rate limiting
  - HTTP fetching
  - HTML conversion
  - Manifest CRUD
  - CLI commands

## Consequences

### Positive

- **Automated Documentation**: No manual fetching required
- **Change Detection**: Only refetch when needed
- **Consistent Format**: All docs in Markdown
- **Extensible**: Easy to add new providers
- **Secure**: Multiple security layers
- **Testable**: High test coverage
- **Maintainable**: Modular, well-documented code

### Negative

- **Complexity**: Multiple components to maintain
- **Provider Changes**: HTML structure changes may break conversion
- **Rate Limits**: Slow for large documentation sets
- **Dependencies**: Relies on external libraries (requests, BeautifulSoup, etc.)

### Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Provider blocks requests | Medium | High | robots.txt compliance, rate limiting, User-Agent identification |
| HTML structure changes | High | Medium | Robust parsing with error recovery, version control for configs |
| Rate limit too strict | Low | Low | Configurable rate limit per provider |
| Manifest corruption | Low | High | Atomic writes, schema validation |

## Implementation Notes

### File Size Management

All files kept under 500 lines:
- models.py: 150 lines
- exceptions.py: 100 lines
- fetcher.py: 200 lines
- converter.py: 200 lines
- manifest.py: 250 lines
- main.py: 150 lines

### Integration Points

- **Scope Manager**: Future integration for global/project/local configs
- **LLM Adapter**: Documentation as context for adapter builders
- **Manifest System**: Shared manifest format with other tools

### Future Enhancements

1. **Incremental Updates**: Only fetch changed sections
2. **Parallel Fetching**: Concurrent requests with semaphore
3. **Caching**: HTTP caching with ETag/Last-Modified
4. **Webhooks**: Automatic updates on provider changes
5. **RAG Integration**: Index documents for semantic search
6. **Version Control**: Git integration for doc changes

## References

- [GitHub Issue #4](https://github.com/matteocervelli/llms/issues/4)
- [ADR-001: Scope Intelligence System](ADR-001-scope-intelligence-system.md)
- [ADR-002: LLM Adapter Architecture](ADR-002-llm-adapter-architecture.md)
- [Tool README](../../../src/tools/doc_fetcher/README.md)

## Approval

**Approved by**: Matteo Cervelli
**Date**: 2025-10-26
