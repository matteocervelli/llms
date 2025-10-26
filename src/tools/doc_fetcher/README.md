# Documentation Fetcher Tool

> Automatically fetch, convert, and manage documentation from LLM provider websites

The Documentation Fetcher is a Python CLI tool that downloads documentation from LLM providers (Anthropic, OpenAI, etc.), converts HTML to Markdown, tracks changes with hash-based detection, and maintains a manifest of all documents.

## Features

- **Multi-Provider Support**: Anthropic, OpenAI, and easily extensible
- **Smart Fetching**: SHA-256 hash-based change detection
- **Rate Limiting**: Respectful requests with configurable rate limits
- **robots.txt Compliance**: Automatic robots.txt checking
- **HTML to Markdown**: Clean conversion preserving structure and code blocks
- **Manifest Tracking**: Centralized tracking with metadata
- **Security**: URL validation, XSS prevention, path traversal protection
- **CLI Interface**: Simple commands for fetch, update, and list operations

## Installation

```bash
# Install dependencies (already in requirements.txt)
pip install click requests beautifulsoup4 markdownify pydantic pyyaml

# Or with the project
pip install -e ".[dev]"
```

## Quick Start

```bash
# Fetch all providers
python -m src.tools.doc_fetcher fetch --all

# Fetch specific provider
python -m src.tools.doc_fetcher fetch --provider anthropic

# Update changed documents
python -m src.tools.doc_fetcher update

# List tracked documents
python -m src.tools.doc_fetcher list
```

## Usage

### Fetch Documentation

```bash
# Fetch all configured providers
python -m src.tools.doc_fetcher fetch --all

# Fetch specific provider
python -m src.tools.doc_fetcher fetch --provider anthropic
python -m src.tools.doc_fetcher fetch --provider openai

# Fetch single URL
python -m src.tools.doc_fetcher fetch \
  --provider anthropic \
  --url https://docs.anthropic.com/en/docs/quickstart \
  --category quickstart
```

### Update Documentation

Check all tracked documents for changes and refetch only those that changed:

```bash
python -m src.tools.doc_fetcher update
```

### List Documentation

```bash
# List all documents
python -m src.tools.doc_fetcher list

# Filter by provider
python -m src.tools.doc_fetcher list --provider anthropic

# Filter by category
python -m src.tools.doc_fetcher list --category guides
```

### Verbose Mode

Enable verbose logging for debugging:

```bash
python -m src.tools.doc_fetcher --verbose fetch --all
```

## Provider Configuration

Providers are configured via YAML files in `src/tools/doc_fetcher/providers/`.

### Example: `anthropic.yaml`

```yaml
name: anthropic
base_url: https://docs.anthropic.com
rate_limit: 1.0  # requests per second
robots_txt_url: https://docs.anthropic.com/robots.txt

sources:
  - url: https://docs.anthropic.com/en/docs/quickstart
    provider: anthropic
    category: quickstart

  - url: https://docs.anthropic.com/en/docs/claude-code/overview
    provider: anthropic
    category: claude-code
```

### Adding a New Provider

1. Create `src/tools/doc_fetcher/providers/{provider}.yaml`
2. Add provider name to `ALLOWED_DOMAINS` in [fetcher.py](src/tools/doc_fetcher/fetcher.py#L70)
3. Configure sources with URLs, provider name, and categories

```yaml
name: my-provider
base_url: https://docs.myprovider.com
rate_limit: 1.0
robots_txt_url: https://docs.myprovider.com/robots.txt

sources:
  - url: https://docs.myprovider.com/guide
    provider: my-provider
    category: guides
```

## Manifest Format

The manifest is stored at `manifests/docs.json`:

```json
{
  "version": "1.0",
  "last_updated": "2025-10-26T12:00:00Z",
  "documents": [
    {
      "provider": "anthropic",
      "url": "https://docs.anthropic.com/en/docs/quickstart",
      "local_path": "docs/anthropic/quickstart/quickstart.md",
      "hash": "abc123...",
      "last_fetched": "2025-10-26T12:00:00Z",
      "category": "quickstart",
      "title": "Quickstart Guide",
      "description": "Get started with Anthropic API"
    }
  ]
}
```

## Architecture

### Components

- **[models.py](src/tools/doc_fetcher/models.py)**: Pydantic data models with validation
- **[exceptions.py](src/tools/doc_fetcher/exceptions.py)**: Custom exception types
- **[fetcher.py](src/tools/doc_fetcher/fetcher.py)**: HTTP fetching with rate limiting
- **[converter.py](src/tools/doc_fetcher/converter.py)**: HTML to Markdown conversion
- **[manifest.py](src/tools/doc_fetcher/manifest.py)**: Manifest management
- **[main.py](src/tools/doc_fetcher/main.py)**: CLI interface

### Security Features

- **URL Validation**: Only HTTPS, whitelisted domains
- **XSS Prevention**: Strips dangerous HTML attributes
- **Path Traversal Protection**: Validates file paths
- **Rate Limiting**: Token bucket algorithm
- **robots.txt Compliance**: Automatic checking
- **Size Limits**: 10MB max response size
- **Timeouts**: 30s request timeout

### Performance

- **Rate Limiting**: Configurable (default: 1 req/sec)
- **Connection Pooling**: Reused HTTP sessions
- **Retry Logic**: Exponential backoff on failures
- **Hash-based Change Detection**: O(1) lookup
- **Atomic File Writes**: Safe manifest updates

## API Reference

### Models

#### `DocumentSource`
```python
DocumentSource(
    url: HttpUrl,
    provider: str,
    category: str,
    last_fetched: Optional[datetime] = None,
    hash: Optional[str] = None
)
```

#### `ManifestEntry`
```python
ManifestEntry(
    provider: str,
    url: HttpUrl,
    local_path: Path,
    hash: str,
    last_fetched: datetime,
    category: str,
    title: Optional[str] = None,
    description: Optional[str] = None
)
```

### Fetcher

```python
fetcher = DocumentFetcher(rate_limit=1.0, respect_robots=True)
result = fetcher.fetch(url)  # Returns FetchResult
fetcher.close()
```

### Converter

```python
converter = DocumentConverter()
markdown, metadata = converter.convert(html, url)
```

### Manifest Manager

```python
manager = ManifestManager(manifest_path)
data = manager.load()
manager.add_entry(entry)
entry = manager.get_entry(url)
entries = manager.list_entries(provider="anthropic")
changed = manager.detect_changes(url, new_hash)
```

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/test_doc_fetcher.py

# Run with coverage
pytest tests/test_doc_fetcher.py --cov=src.tools.doc_fetcher --cov-report=term-missing

# Run specific test class
pytest tests/test_doc_fetcher.py::TestDocumentFetcher -v
```

Target: 80%+ coverage

## Troubleshooting

### "Domain not in whitelist" Error

Add the domain to `ALLOWED_DOMAINS` in `fetcher.py`:

```python
ALLOWED_DOMAINS = [
    "docs.anthropic.com",
    "platform.openai.com",
    "your-domain.com",  # Add here
]
```

### robots.txt Violations

The tool respects robots.txt by default. If fetching is blocked:

1. Check `{base_url}/robots.txt` manually
2. Disable robots.txt checking (not recommended):
   ```python
   fetcher = DocumentFetcher(respect_robots=False)
   ```

### Rate Limiting

If you hit rate limits:

1. Increase delay in provider config:
   ```yaml
   rate_limit: 0.5  # 1 request every 2 seconds
   ```

2. Wait and retry with exponential backoff (automatic)

### Conversion Errors

If HTML conversion fails:

1. Check HTML structure (must have `<main>` or `<article>`)
2. Enable verbose logging: `--verbose`
3. Inspect HTML manually and adjust `REMOVE_TAGS` in `converter.py`

## Development

### Code Quality

```bash
# Format code
black src/tools/doc_fetcher tests/

# Type checking
mypy src/tools/doc_fetcher

# Linting
flake8 src/tools/doc_fetcher

# All checks
black . && mypy src/tools/doc_fetcher && flake8 src/tools/doc_fetcher && pytest
```

### Adding Features

1. Follow 500-line limit per file
2. Add comprehensive tests (80%+ coverage)
3. Update this README
4. Create ADR if architectural change

## Links

- [Architecture Decision Record](../../../docs/architecture/ADR/ADR-003-documentation-fetcher.md)
- [GitHub Issue #4](https://github.com/matteocervelli/llms/issues/4)
- [Project README](../../../README.md)

## License

MIT License - See [LICENSE](../../../LICENSE)
