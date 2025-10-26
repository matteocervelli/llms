# ADR-005: Crawl4AI Integration for LLM-Optimized Documentation Fetching

**Status**: Implemented
**Date**: 2025-01-26
**Author**: Matteo Cervelli
**Context**: Issue #6 - Fetch Initial Anthropic/Claude Code Documentation

## Context

The Documentation Fetcher tool initially used BeautifulSoup + Markdownify for converting HTML to Markdown. While functional, this approach had several limitations:

1. **Markdown Quality**: Generic HTML-to-Markdown conversion not optimized for LLM consumption
2. **JavaScript Rendering**: No support for dynamically loaded content
3. **Content Extraction**: Manual CSS selectors required for each site
4. **LLM Optimization**: No specific formatting for AI/LLM use cases
5. **Maintenance Burden**: Site changes break scrapers

When implementing Issue #6 to fetch 22 priority Claude Code documentation pages, we needed to decide between:
- **Option A**: Continue with BeautifulSoup/Markdownify
- **Option B**: Use Tavily (search-focused API)
- **Option C**: Use Crawl4AI (documentation-focused crawler)

## Decision

We will integrate **Crawl4AI** as the primary documentation fetching engine, replacing BeautifulSoup + Markdownify for all documentation crawling tasks.

### Architecture

**New Component**: `src/tools/doc_fetcher/crawler.py`
- `DocumentationCrawler` class for async URL crawling
- Wraps Crawl4AI's `AsyncWebCrawler` with rate limiting
- Token bucket algorithm (1 req/sec default)
- LLM-optimized markdown extraction via `fit_markdown`

**Integration Points**:
- `main.py`: New async methods `fetch_document_crawl4ai()` and `fetch_provider_crawl4ai()`
- `exceptions.py`: New `CrawlError` exception type
- `fetcher.py`: Updated `ALLOWED_DOMAINS` to include `docs.claude.com`
- `requirements.txt`: Added `crawl4ai>=0.7.0` and `playwright>=1.40.0`

### Implementation

```python
# crawler.py
class DocumentationCrawler:
    async def crawl_url(
        self,
        url: str,
        use_fit_markdown: bool = True,
        remove_overlay: bool = True
    ) -> tuple[str, dict, str]:
        """Crawl single URL and extract LLM-optimized markdown."""
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            config = CrawlerRunConfig(
                exclude_external_links=True,
                remove_overlay_elements=remove_overlay,
                word_count_threshold=10,
            )
            result = await crawler.arun(url=url, config=config)
            markdown = result.markdown.fit_markdown or result.markdown.raw_markdown
            metadata = {"title": result.metadata.get("title", ""), ...}
            content_hash = self._compute_hash(markdown)
            return markdown, metadata, content_hash
```

### Configuration

**Crawl4AI Browser Config**:
- Headless mode: Enabled for automation
- Browser: Chromium via Playwright
- Viewport: 1920x1080 (desktop rendering)
- User agent: Custom doc_fetcher identification

**Rate Limiting**:
- Default: 1 request/second
- Token bucket implementation
- Configurable via `rate_limit` parameter
- Respects robots.txt (inherited from existing fetcher)

## Rationale

### Why Crawl4AI Over BeautifulSoup/Markdownify?

1. **LLM-Optimized Markdown**:
   - Crawl4AI's `fit_markdown` generates markdown specifically formatted for LLM consumption
   - Superior content extraction vs generic HTML parsing
   - Preserves semantic structure and hierarchy

2. **JavaScript Rendering**:
   - Uses Playwright for full browser rendering
   - Handles dynamically loaded content (SPAs, lazy-loading)
   - Executes JavaScript before extraction

3. **Automatic Content Extraction**:
   - No manual CSS selectors required
   - Intelligent main content detection
   - Removes navigation, footers, ads automatically

4. **Python-Native**:
   - Pure Python library (async/await support)
   - Integrates seamlessly with existing codebase
   - No external services or API keys required

5. **Purpose-Built for Documentation**:
   - Designed for technical documentation crawling
   - Handles code blocks, tables, nested lists
   - Preserves markdown formatting

### Why Not Tavily?

Tavily is a search-focused API optimized for web search, not documentation crawling:

- **Search vs Crawl**: Tavily finds pages; we need content extraction
- **API Dependency**: Requires external service and API key
- **Cost**: Per-request pricing model
- **Less Control**: Cannot customize extraction logic
- **Not LLM-Optimized**: Generic markdown conversion

Tavily is excellent for search tasks but not ideal for systematic documentation fetching.

### Why Not Continue with BeautifulSoup?

BeautifulSoup served us well initially but has limitations:

- **Manual Extraction**: Requires CSS selectors per site
- **No JavaScript**: Cannot render dynamic content
- **Generic Markdown**: Not optimized for LLMs
- **Maintenance**: Site changes break selectors
- **Quality**: Markdownify produces suboptimal markdown

## Implementation Results

### Initial Deployment (Issue #6)

**Fetched**: 22 priority Claude Code documentation pages (100% success rate)

**Categories**:
- Claude Code: 12 pages (overview, quickstart, workflows, skills, commands, subagents, hooks, memory, MCP, output-styles, headless)
- Agent Skills: 5 pages (overview, quickstart, best practices, MCP connector, remote MCP servers)
- Agent SDK: 3 pages (overview, TypeScript, Python references)
- API: 2 pages (messages, models endpoints)

**Performance**:
- Total time: ~50 seconds (22 pages)
- Average per page: ~2.3 seconds (including 1 req/sec rate limiting)
- Crawl time: ~1.5 seconds per page (actual fetch)
- Output: 22 markdown files, ~500KB total

**Quality Metrics**:
- All pages rendered correctly
- Code blocks preserved with syntax highlighting
- Tables converted to markdown format
- Links maintained (relative and absolute)
- Metadata extracted (title, description)

## Consequences

### Positive

- ✅ **Superior Markdown Quality**: LLM-optimized content extraction
- ✅ **JavaScript Support**: Full browser rendering with Playwright
- ✅ **Automatic Extraction**: No manual CSS selectors needed
- ✅ **Python-Native**: Seamless integration with existing codebase
- ✅ **Async Performance**: Concurrent crawling with async/await
- ✅ **Purpose-Built**: Designed for documentation, not generic scraping
- ✅ **No External Dependencies**: No API keys or external services
- ✅ **Cost-Free**: Open-source library, no per-request costs
- ✅ **Maintainable**: Site changes less likely to break extraction

### Negative

- ⚠️ **Dependency Size**: Crawl4AI + Playwright adds ~200MB (browsers)
- ⚠️ **Browser Installation**: Requires `playwright install chromium`
- ⚠️ **Resource Usage**: Headless browser uses more memory than BeautifulSoup
- ⚠️ **Complexity**: More moving parts (browser automation)
- ⚠️ **Startup Time**: Browser initialization adds ~1 second overhead

### Neutral

- Crawl4AI is actively maintained (v0.7.x as of January 2025)
- Playwright is mature and stable (v1.40+)
- Async architecture requires `asyncio.run()` in CLI commands
- Rate limiting maintained at 1 req/sec (same as before)

## Security Considerations

1. **Browser Isolation**: Playwright runs in sandboxed environment
2. **URL Validation**: Existing ALLOWED_DOMAINS whitelist maintained
3. **Content Sanitization**: HTML sanitization still applies
4. **Path Traversal**: Existing protection unchanged
5. **Rate Limiting**: Token bucket prevents abuse
6. **robots.txt Compliance**: Existing checks maintained

**No New Security Risks**: Crawl4AI operates within existing security model.

## Performance Impact

### Comparison: BeautifulSoup vs Crawl4AI

| Metric | BeautifulSoup | Crawl4AI |
|--------|---------------|----------|
| Fetch Time | ~1.0s | ~1.5s |
| Startup Overhead | ~10ms | ~1.0s |
| Memory Usage | ~50MB | ~150MB |
| Markdown Quality | Basic | LLM-Optimized |
| JavaScript Support | No | Yes |
| Maintenance | High | Low |

**Trade-off**: Slightly slower and more resource-intensive, but significantly better output quality and lower maintenance burden.

### Real-World Performance (Issue #6)

- 22 pages fetched in ~50 seconds
- Rate limiting: 1 req/sec (primary time factor)
- Actual crawl: ~1.5s per page
- **Acceptable**: Quality improvement justifies performance cost

## Testing

### Unit Tests

- `DocumentationCrawler` initialization
- Rate limiting enforcement (token bucket)
- Hash computation (SHA-256)
- URL validation and sanitization

### Integration Tests

- Async URL crawling with mock responses
- Metadata extraction from crawled pages
- Error handling (network failures, timeouts)
- Rate limit compliance

### Manual Testing (Issue #6)

- ✅ All 22 pages fetched successfully (100% success rate)
- ✅ Markdown quality verified (code blocks, tables, links)
- ✅ Metadata extracted correctly (title, description)
- ✅ Manifest updated with proper hashes and UUIDs
- ✅ Rate limiting respected (1 req/sec)

## Alternatives Considered

### Alternative 1: Continue with BeautifulSoup + Markdownify

**Rejected**:
- Markdown quality not optimal for LLMs
- No JavaScript rendering support
- Requires manual CSS selectors per site
- High maintenance burden

### Alternative 2: Use Tavily API

**Rejected**:
- Search-focused, not documentation-focused
- Requires external API key and service
- Per-request pricing model
- Less control over extraction logic
- Not LLM-optimized

### Alternative 3: Build Custom Headless Browser Solution

**Rejected**:
- Reinventing the wheel
- Significant development time
- Maintenance burden
- Crawl4AI already solves this problem

### Alternative 4: Use Scrapy + Splash

**Rejected**:
- More complex setup (Scrapy framework + Splash service)
- Not LLM-optimized
- Overkill for documentation fetching
- Higher learning curve

## Migration Path

### Phase 1: Crawl4AI Integration (Completed)

- ✅ Install Crawl4AI and Playwright dependencies
- ✅ Create `DocumentationCrawler` class
- ✅ Integrate into `main.py` with async support
- ✅ Update `anthropic.yaml` with 22 priority URLs
- ✅ Fetch initial 22 pages and verify quality
- ✅ Update manifest with all fetched documents

### Phase 2: Gradual Replacement (Future)

- Replace BeautifulSoup calls with Crawl4AI in `fetcher.py`
- Deprecate `DocumentationFetcher.fetch_url()` (BeautifulSoup)
- Use `DocumentationCrawler.crawl_url()` (Crawl4AI) as default
- Remove BeautifulSoup and Markdownify dependencies

### Phase 3: Enhanced Features (Future)

- Implement auto-discovery crawler for full site documentation
- Add sitemap.xml support for efficient crawling
- Implement incremental updates (fetch only changed pages)
- Add parallel crawling for faster batch fetches

## Backward Compatibility

**Existing Code**: BeautifulSoup-based fetcher remains in `fetcher.py`
**New Code**: Crawl4AI-based crawler in `crawler.py`
**CLI**: New methods `fetch_document_crawl4ai()` and `fetch_provider_crawl4ai()`
**Migration**: Gradual replacement, no breaking changes

## Dependencies

**Added**:
- `crawl4ai>=0.7.0`: LLM-optimized web crawler
- `playwright>=1.40.0`: Browser automation for JavaScript rendering

**Installation**:
```bash
uv pip install crawl4ai playwright
.venv/bin/playwright install chromium
```

**Size Impact**:
- Crawl4AI: ~10MB (Python package)
- Playwright: ~200MB (Chromium browser)

## References

- [Issue #6: Fetch Initial Anthropic/Claude Code Documentation](https://github.com/matteocervelli/llms/issues/6)
- [ADR-003: Documentation Fetcher](./ADR-003-documentation-fetcher.md)
- [ADR-004: Manifest Schema v1.1](./ADR-004-manifest-schema-v1.1.md)
- [Crawl4AI Documentation](https://github.com/unclecode/crawl4ai)
- [Playwright Python Documentation](https://playwright.dev/python/)

## Changelog

- **2025-01-26**: Initial ADR created and implemented with Issue #6
- **2025-01-26**: Successfully fetched 22 priority Claude Code documentation pages (100% success rate)

## Future Enhancements

### Potential Features

1. **Auto-Discovery Crawler**: Automatically discover and fetch all pages from a documentation site
2. **Sitemap Support**: Use sitemap.xml for efficient page discovery
3. **Incremental Updates**: Fetch only changed pages based on hash comparison
4. **Parallel Crawling**: Fetch multiple pages concurrently (respecting rate limits)
5. **PDF Support**: Extract content from PDF documentation files
6. **Archive Support**: Snapshot documentation versions over time

### Performance Optimizations

1. **Browser Reuse**: Keep browser instance alive across multiple fetches
2. **Connection Pooling**: Reuse TCP connections for faster requests
3. **Caching**: Cache crawled pages with TTL for repeated fetches
4. **Batch Fetching**: Group related pages for efficient processing

## Conclusion

Crawl4AI integration significantly improves documentation fetching quality while maintaining security, reliability, and ease of use. The LLM-optimized markdown generation justifies the slightly higher resource usage and startup time. This decision sets a strong foundation for future documentation management and enables more sophisticated crawling features in upcoming sprints.
