# ADR-004: Manifest Schema v1.1 Enhancement

**Status**: Implemented
**Date**: 2025-01-26
**Author**: Matteo Cervelli
**Context**: Issue #5 - Create Documentation Manifest System

## Context

The Documentation Fetcher tool uses a manifest file (`manifests/docs.json`) to track all fetched documentation. The initial implementation (v1.0) provided basic tracking with URL, hash, and metadata fields. As the system grows to support multiple providers and more sophisticated search and management capabilities, we need enhanced schema features:

1. **Unique Identification**: No way to uniquely identify documents beyond URL
2. **Provider/Category Tracking**: No centralized list of tracked providers/categories
3. **Limited Search**: No built-in search functionality across documents
4. **Topic Categorization**: No way to tag documents with topics/keywords
5. **Field-Level Updates**: No way to update specific fields without replacing entire entry

## Decision

We will upgrade the manifest schema from v1.0 to v1.1 with the following enhancements:

### Schema Changes

**Top-Level Structure**:
```json
{
  "version": "1.1",
  "last_updated": "ISO8601",
  "providers": ["anthropic", "openai"],      // NEW
  "categories": ["api", "guides"],            // NEW
  "documents": [...]
}
```

**Document Entry**:
```json
{
  "id": "uuid-v4",                           // NEW
  "provider": "anthropic",
  "url": "https://...",
  "local_path": "docs/...",
  "hash": "sha256",
  "last_fetched": "ISO8601",
  "category": "api",
  "title": "...",
  "description": "...",
  "topics": ["api", "rest", "claude"]        // NEW
}
```

### New Features

1. **Unique IDs**: UUID v4 for each document
   - Auto-generated on creation
   - Enables precise document identification
   - Supports field-level updates

2. **Provider/Category Tracking**: Top-level arrays
   - Auto-populated from documents
   - Sorted alphabetically
   - Enables quick filtering and statistics

3. **Topic Tags**: List of keywords per document
   - Max 20 topics per document
   - Max 50 characters per topic
   - Alphanumeric + hyphens/underscores only
   - Lowercase normalized
   - Supports categorization and search

4. **New Management Functions**:
   - `update_page(page_id, **fields)`: Update specific fields by ID
   - `search_pages(query, fields, filters)`: Full-text search across documents
   - `get_providers()`: Get list of tracked providers
   - `get_categories()`: Get list of tracked categories
   - `migrate_schema(from, to)`: Schema version migration

### Validation Rules

**ID Field**:
- Must be valid UUID v4
- Auto-generated if not provided
- Validated using Python's `uuid.UUID()`

**Topics Field**:
- Maximum 20 topics per document
- Maximum 50 characters per topic
- Only alphanumeric characters, hyphens, and underscores
- Automatically normalized to lowercase
- Empty list if not provided

## Rationale

### Why UUID v4 for IDs?
- Non-sequential (no information leakage)
- Globally unique (no collisions)
- Standard format (128-bit)
- Python's `uuid.uuid4()` is fast and reliable

### Why Limited Topics?
- 20 topics is sufficient for categorization
- Prevents abuse and keeps manifest manageable
- 50 characters per topic prevents verbose descriptions
- Enforces focused, keyword-style tagging

### Why Providers/Categories Arrays?
- O(1) lookup for statistics
- Avoids scanning all documents
- Auto-updated on document changes
- Sorted for consistent output

### Why Full-Text Search?
- Enables quick discovery of relevant docs
- Searches across title, description, and topics
- Case-insensitive for better UX
- Optional provider/category filtering

## Implementation

### Phase 1: Data Models
- Enhanced `ManifestEntry` with `id` and `topics` fields
- Added `ManifestSchema` model for top-level validation
- Pydantic validators for UUID and topics

### Phase 2: ManifestManager
- Updated schema version to "1.1"
- Implemented `update_page()`, `search_pages()`, helpers
- Auto-populate providers/categories on add/update
- Migration support from v1.0 to v1.1

### Phase 3: Migration Strategy
- New manifests: Created with v1.1 schema
- Existing v1.0 manifests: Auto-detected and migrated
- Migration adds:
  - `providers` and `categories` arrays
  - `id` field to all documents (auto-generated)
  - `topics` field to all documents (empty list)

## Consequences

### Positive
- ✅ Enhanced document management with unique IDs
- ✅ Topic-based categorization and search
- ✅ Provider/category tracking for statistics
- ✅ Field-level updates without replacing entire entries
- ✅ Backward compatibility via automatic migration
- ✅ Improved search capabilities across documents
- ✅ Future-proof for additional schema enhancements

### Negative
- ⚠️ Breaking change for external tools reading v1.0 manifests (mitigated by auto-migration)
- ⚠️ Slightly larger manifest files (UUID + topics storage)
- ⚠️ Migration overhead on first load of v1.0 manifests

### Neutral
- Schema version bump requires documentation updates
- Tests updated to expect v1.1 schema
- README updated with new features

## Security Considerations

1. **UUID Validation**: Strict UUID v4 format prevents injection attacks
2. **Topics Sanitization**: Alphanumeric-only prevents XSS and injection
3. **Search Query Sanitization**: Case-insensitive string matching (no regex injection)
4. **Path Traversal**: Existing protection maintained
5. **Input Validation**: Pydantic models enforce all constraints

## Performance Impact

- **update_page()**: <50ms (single document lookup and update)
- **search_pages()**: <100ms for 1000 documents (simple string matching)
- **get_providers/categories()**: <10ms (direct array access)
- **migrate_schema()**: <200ms for 100 documents (one-time cost)

## Testing

- 19 new tests added (100% passing)
- Coverage: 76% for manifest module
- Tests cover:
  - UUID validation and auto-generation
  - Topics validation (count, length, characters)
  - update_page() functionality
  - search_pages() with various queries and filters
  - get_providers/categories() helpers
  - Schema migration v1.0 → v1.1

## Alternatives Considered

### Alternative 1: Use URL as ID
- **Rejected**: URLs can change, breaking references
- **Rejected**: Not suitable for unique identification

### Alternative 2: Sequential Integer IDs
- **Rejected**: Information leakage (document count)
- **Rejected**: Not globally unique
- **Rejected**: Collision risk in distributed systems

### Alternative 3: Unlimited Topics
- **Rejected**: Potential abuse
- **Rejected**: Manifest bloat
- **Rejected**: Harder to manage and validate

### Alternative 4: Full-Text Search with Elasticsearch
- **Rejected**: Over-engineered for current scale
- **Rejected**: External dependency
- **Future**: Consider if scale grows to 10,000+ documents

## Migration Path

**From v1.0 to v1.1**:
1. Detect v1.0 manifest on load
2. Add `providers` and `categories` arrays (empty)
3. Generate UUID v4 for each document's `id` field
4. Add empty `topics` array to each document
5. Populate `providers` and `categories` from documents
6. Update version to "1.1"
7. Save migrated manifest atomically

**No Migration Path Needed**:
- v1.1 is the current version
- Future versions will need migration from v1.1

## References

- [Issue #5: Create Documentation Manifest System](https://github.com/matteocervelli/llms/issues/5)
- [ADR-003: Documentation Fetcher](./ADR-003-documentation-fetcher.md)
- [Python UUID Documentation](https://docs.python.org/3/library/uuid.html)
- [Pydantic Validation](https://docs.pydantic.dev/latest/usage/validators/)

## Changelog

- **2025-01-26**: Initial ADR created and implemented
