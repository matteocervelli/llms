"""
Comprehensive test suite for the Documentation Fetcher tool.

Test Coverage:
- Models validation and serialization
- Exceptions and error handling
- HTTP fetching with mocking
- Rate limiting behavior
- HTML to Markdown conversion
- Manifest CRUD operations
- CLI commands

Target: 80%+ coverage
"""

import json
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests
from click.testing import CliRunner
from pydantic import HttpUrl, ValidationError

from src.tools.doc_fetcher.converter import DocumentConverter
from src.tools.doc_fetcher.exceptions import (
    ConversionError,
    FetchError,
    ManifestError,
    RateLimitError,
)
from src.tools.doc_fetcher.fetcher import DocumentFetcher, RateLimiter
from src.tools.doc_fetcher.main import cli
from src.tools.doc_fetcher.manifest import ManifestManager
from src.tools.doc_fetcher.models import (
    DocumentSource,
    FetchResult,
    ManifestEntry,
    ProviderConfig,
)


# ============================================================================
# Test Models
# ============================================================================


class TestDocumentSource:
    """Tests for DocumentSource model."""

    def test_valid_document_source(self) -> None:
        """Should create valid DocumentSource."""
        source = DocumentSource(
            url=HttpUrl("https://docs.anthropic.com/guide"),
            provider="anthropic",
            category="guides",
        )

        assert str(source.url) == "https://docs.anthropic.com/guide"
        assert source.provider == "anthropic"
        assert source.category == "guides"

    def test_provider_normalization(self) -> None:
        """Should normalize provider to lowercase."""
        source = DocumentSource(
            url=HttpUrl("https://docs.anthropic.com/guide"),
            provider="ANTHROPIC",
            category="GUIDES",
        )

        assert source.provider == "anthropic"
        assert source.category == "guides"

    def test_invalid_provider_characters(self) -> None:
        """Should reject invalid provider characters."""
        with pytest.raises(ValidationError):
            DocumentSource(
                url=HttpUrl("https://docs.anthropic.com/guide"),
                provider="invalid provider!",
                category="guides",
            )

    def test_hash_pattern_validation(self) -> None:
        """Should validate SHA-256 hash pattern."""
        valid_hash = "a" * 64
        source = DocumentSource(
            url=HttpUrl("https://docs.anthropic.com/guide"),
            provider="anthropic",
            category="guides",
            hash=valid_hash,
        )
        assert source.hash == valid_hash

        # Invalid hash
        with pytest.raises(ValidationError):
            DocumentSource(
                url=HttpUrl("https://docs.anthropic.com/guide"),
                provider="anthropic",
                category="guides",
                hash="invalid",
            )


class TestFetchResult:
    """Tests for FetchResult model."""

    def test_successful_fetch_result(self) -> None:
        """Should create successful fetch result."""
        result = FetchResult(
            success=True,
            url=HttpUrl("https://docs.anthropic.com/guide"),
            content="<html>Test</html>",
            hash="a" * 64,
            status_code=200,
        )

        assert result.success is True
        assert result.content == "<html>Test</html>"
        assert result.status_code == 200

    def test_failed_fetch_result(self) -> None:
        """Should create failed fetch result."""
        result = FetchResult(
            success=False,
            url=HttpUrl("https://docs.anthropic.com/guide"),
            error="Connection timeout",
            status_code=408,
        )

        assert result.success is False
        assert result.error == "Connection timeout"


class TestManifestEntry:
    """Tests for ManifestEntry model."""

    def test_valid_manifest_entry(self) -> None:
        """Should create valid ManifestEntry."""
        entry = ManifestEntry(
            provider="anthropic",
            url=HttpUrl("https://docs.anthropic.com/guide"),
            local_path=Path("docs/anthropic/guide.md"),
            hash="a" * 64,
            last_fetched=datetime.now(),
            category="guides",
            title="Test Guide",
        )

        assert entry.provider == "anthropic"
        assert entry.title == "Test Guide"

    def test_path_traversal_prevention(self) -> None:
        """Should prevent path traversal in local_path."""
        with pytest.raises(ValidationError, match="must not contain"):
            ManifestEntry(
                provider="anthropic",
                url=HttpUrl("https://docs.anthropic.com/guide"),
                local_path=Path("../../etc/passwd"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category="guides",
            )

    def test_absolute_path_prevention(self) -> None:
        """Should prevent absolute paths."""
        with pytest.raises(ValidationError, match="must not contain"):
            ManifestEntry(
                provider="anthropic",
                url=HttpUrl("https://docs.anthropic.com/guide"),
                local_path=Path("/etc/passwd"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category="guides",
            )


class TestProviderConfig:
    """Tests for ProviderConfig model."""

    def test_valid_provider_config(self) -> None:
        """Should create valid ProviderConfig."""
        config = ProviderConfig(
            name="anthropic",
            base_url=HttpUrl("https://docs.anthropic.com"),
            rate_limit=1.5,
        )

        assert config.name == "anthropic"
        assert config.rate_limit == 1.5

    def test_rate_limit_validation(self) -> None:
        """Should validate rate limit bounds."""
        # Too low
        with pytest.raises(ValidationError):
            ProviderConfig(
                name="anthropic",
                base_url=HttpUrl("https://docs.anthropic.com"),
                rate_limit=0,
            )

        # Too high
        with pytest.raises(ValidationError):
            ProviderConfig(
                name="anthropic",
                base_url=HttpUrl("https://docs.anthropic.com"),
                rate_limit=11,
            )


# ============================================================================
# Test Exceptions
# ============================================================================


class TestExceptions:
    """Tests for custom exceptions."""

    def test_fetch_error(self) -> None:
        """Should create FetchError with URL."""
        error = FetchError("https://test.com", "Connection failed")
        assert error.url == "https://test.com"
        assert "Connection failed" in str(error)

    def test_conversion_error(self) -> None:
        """Should create ConversionError with URL."""
        error = ConversionError("https://test.com", "Invalid HTML")
        assert error.url == "https://test.com"
        assert "Invalid HTML" in str(error)

    def test_manifest_error(self) -> None:
        """Should create ManifestError with operation."""
        error = ManifestError("save", "Permission denied")
        assert error.operation == "save"
        assert "Permission denied" in str(error)

    def test_rate_limit_error(self) -> None:
        """Should create RateLimitError with wait time."""
        error = RateLimitError(2.5)
        assert error.wait_time == 2.5
        assert "2.5" in str(error)


# ============================================================================
# Test Rate Limiter
# ============================================================================


class TestRateLimiter:
    """Tests for RateLimiter class."""

    def test_initial_tokens(self) -> None:
        """Should start with full token bucket."""
        limiter = RateLimiter(rate=1.0, capacity=5)
        assert limiter.tokens == 5

    def test_acquire_tokens(self) -> None:
        """Should acquire tokens successfully."""
        limiter = RateLimiter(rate=1.0, capacity=5)
        limiter.acquire(1)
        assert limiter.tokens == 4

    def test_rate_limit_exceeded(self) -> None:
        """Should raise error when tokens exhausted."""
        limiter = RateLimiter(rate=1.0, capacity=2)
        limiter.acquire(2)  # Exhaust tokens

        with pytest.raises(RateLimitError):
            limiter.acquire(1)

    def test_token_refill(self) -> None:
        """Should refill tokens over time."""
        limiter = RateLimiter(rate=10.0, capacity=10)  # 10 tokens/sec
        limiter.acquire(10)  # Exhaust tokens

        time.sleep(0.2)  # Wait 200ms (should add ~2 tokens)
        assert limiter.try_acquire(1) is True

    def test_try_acquire_without_blocking(self) -> None:
        """Should try acquiring without blocking."""
        limiter = RateLimiter(rate=1.0, capacity=2)
        assert limiter.try_acquire(1) is True
        assert limiter.try_acquire(1) is True
        assert limiter.try_acquire(1) is False  # Exhausted


# ============================================================================
# Test Document Fetcher
# ============================================================================


class TestDocumentFetcher:
    """Tests for DocumentFetcher class."""

    def test_url_validation_https_only(self) -> None:
        """Should only allow HTTPS URLs."""
        fetcher = DocumentFetcher()
        url = HttpUrl("http://docs.anthropic.com/guide")

        result = fetcher.fetch(url)
        assert result.success is False
        assert "Protocol" in result.error or "not allowed" in result.error

    def test_url_validation_domain_whitelist(self) -> None:
        """Should only allow whitelisted domains."""
        fetcher = DocumentFetcher()
        url = HttpUrl("https://evil.com/malware")

        result = fetcher.fetch(url)
        assert result.success is False
        assert "whitelist" in result.error.lower() or "not in whitelist" in result.error.lower()

    @patch("src.tools.doc_fetcher.fetcher.requests.Session.get")
    def test_successful_fetch(self, mock_get: Mock) -> None:
        """Should successfully fetch valid URL."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "text/html", "content-length": "100"}
        mock_response.iter_content = lambda chunk_size, decode_unicode: [
            "<html>Test content</html>"
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        fetcher = DocumentFetcher()
        url = HttpUrl("https://docs.anthropic.com/guide")
        result = fetcher.fetch(url)

        assert result.success is True
        assert result.content == "<html>Test content</html>"
        assert result.status_code == 200

    @patch("src.tools.doc_fetcher.fetcher.requests.Session.get")
    def test_fetch_timeout(self, mock_get: Mock) -> None:
        """Should handle timeout errors."""
        mock_get.side_effect = requests.exceptions.Timeout("Timeout")

        fetcher = DocumentFetcher()
        url = HttpUrl("https://docs.anthropic.com/guide")
        result = fetcher.fetch(url, retry_count=1)

        assert result.success is False
        assert "timeout" in result.error.lower()

    @patch("src.tools.doc_fetcher.fetcher.requests.Session.get")
    def test_fetch_http_error(self, mock_get: Mock) -> None:
        """Should handle HTTP errors."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404")

        fetcher = DocumentFetcher()
        url = HttpUrl("https://docs.anthropic.com/nonexistent")
        result = fetcher.fetch(url, retry_count=1)

        assert result.success is False


# ============================================================================
# Test Document Converter
# ============================================================================


class TestDocumentConverter:
    """Tests for DocumentConverter class."""

    def test_simple_html_conversion(self) -> None:
        """Should convert simple HTML to Markdown."""
        html = """
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Hello World</h1>
            <p>This is a test.</p>
        </body>
        </html>
        """

        converter = DocumentConverter()
        markdown, metadata = converter.convert(html, "https://test.com")

        assert "Hello World" in markdown
        assert "This is a test" in markdown
        assert metadata["title"] == "Test Page"

    def test_remove_navigation(self) -> None:
        """Should remove navigation elements."""
        html = """
        <html>
        <body>
            <nav>Navigation menu</nav>
            <main><p>Main content</p></main>
        </body>
        </html>
        """

        converter = DocumentConverter()
        markdown, _ = converter.convert(html, "https://test.com")

        assert "Navigation menu" not in markdown
        assert "Main content" in markdown

    def test_remove_dangerous_attributes(self) -> None:
        """Should remove dangerous attributes (XSS prevention)."""
        html = """
        <html>
        <body>
            <p onclick="alert('XSS')">Test</p>
        </body>
        </html>
        """

        converter = DocumentConverter()
        markdown, _ = converter.convert(html, "https://test.com")

        # Should not contain onclick
        assert "onclick" not in markdown.lower()

    def test_metadata_extraction(self) -> None:
        """Should extract metadata from HTML."""
        html = """
        <html>
        <head>
            <title>Test Title</title>
            <meta name="description" content="Test description">
        </head>
        <body><p>Content</p></body>
        </html>
        """

        converter = DocumentConverter()
        _, metadata = converter.convert(html, "https://test.com")

        assert metadata["title"] == "Test Title"
        assert metadata["description"] == "Test description"

    def test_code_block_preservation(self) -> None:
        """Should preserve code blocks."""
        html = """
        <html>
        <body>
            <pre><code class="language-python">print("hello")</code></pre>
        </body>
        </html>
        """

        converter = DocumentConverter()
        markdown, _ = converter.convert(html, "https://test.com")

        assert "print" in markdown
        assert "hello" in markdown


# ============================================================================
# Test Manifest Manager
# ============================================================================


class TestManifestManager:
    """Tests for ManifestManager class."""

    def test_create_new_manifest(self, tmp_path: Path) -> None:
        """Should create new manifest if not exists."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        data = manager.load()

        assert data["version"] == "1.1"
        assert "documents" in data
        assert "providers" in data
        assert "categories" in data
        assert len(data["documents"]) == 0

    def test_add_entry(self, tmp_path: Path) -> None:
        """Should add entry to manifest."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        entry = ManifestEntry(
            provider="anthropic",
            url=HttpUrl("https://docs.anthropic.com/guide"),
            local_path=Path("docs/guide.md"),
            hash="a" * 64,
            last_fetched=datetime.now(),
            category="guides",
        )

        manager.add_entry(entry)

        # Verify entry added
        retrieved = manager.get_entry(str(entry.url))
        assert retrieved is not None
        assert retrieved.provider == "anthropic"
        assert retrieved.hash == "a" * 64

    def test_update_existing_entry(self, tmp_path: Path) -> None:
        """Should update existing entry."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        url = "https://docs.anthropic.com/guide"

        # Add initial entry
        entry1 = ManifestEntry(
            provider="anthropic",
            url=HttpUrl(url),
            local_path=Path("docs/guide.md"),
            hash="a" * 64,
            last_fetched=datetime.now(),
            category="guides",
        )
        manager.add_entry(entry1)

        # Update entry
        entry2 = ManifestEntry(
            provider="anthropic",
            url=HttpUrl(url),
            local_path=Path("docs/guide.md"),
            hash="b" * 64,  # Changed hash
            last_fetched=datetime.now(),
            category="guides",
        )
        manager.add_entry(entry2)

        # Verify updated
        retrieved = manager.get_entry(url)
        assert retrieved is not None
        assert retrieved.hash == "b" * 64

    def test_list_entries_with_filters(self, tmp_path: Path) -> None:
        """Should filter entries by provider and category."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        # Add multiple entries
        for i in range(3):
            entry = ManifestEntry(
                provider="anthropic" if i < 2 else "openai",
                url=HttpUrl(f"https://docs.test.com/guide{i}"),
                local_path=Path(f"docs/guide{i}.md"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category="guides" if i % 2 == 0 else "api",
            )
            manager.add_entry(entry)

        # Test filters
        all_entries = manager.list_entries()
        assert len(all_entries) == 3

        anthropic_entries = manager.list_entries(provider="anthropic")
        assert len(anthropic_entries) == 2

        guides_entries = manager.list_entries(category="guides")
        assert len(guides_entries) == 2

    def test_detect_changes(self, tmp_path: Path) -> None:
        """Should detect content changes via hash."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        url = "https://docs.anthropic.com/guide"
        old_hash = manager.check_hash("old content")

        # Add entry with old hash
        entry = ManifestEntry(
            provider="anthropic",
            url=HttpUrl(url),
            local_path=Path("docs/guide.md"),
            hash=old_hash,
            last_fetched=datetime.now(),
            category="guides",
        )
        manager.add_entry(entry)

        # Check with same hash
        assert manager.detect_changes(url, old_hash) is False

        # Check with different hash
        new_hash = manager.check_hash("new content")
        assert manager.detect_changes(url, new_hash) is True

    def test_manifest_v1_1_schema(self, tmp_path: Path) -> None:
        """Should create manifest with v1.1 schema."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        data = manager.load()

        assert data["version"] == "1.1"
        assert "providers" in data
        assert "categories" in data
        assert isinstance(data["providers"], list)
        assert isinstance(data["categories"], list)

    def test_entry_with_id_and_topics(self, tmp_path: Path) -> None:
        """Should handle entries with id and topics fields."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        entry = ManifestEntry(
            provider="anthropic",
            url=HttpUrl("https://docs.anthropic.com/api"),
            local_path=Path("docs/api.md"),
            hash="a" * 64,
            last_fetched=datetime.now(),
            category="api",
            topics=["api", "rest", "claude"],
        )

        manager.add_entry(entry)

        # Verify entry
        retrieved = manager.get_entry(str(entry.url))
        assert retrieved is not None
        assert retrieved.id  # ID should be auto-generated
        assert retrieved.topics == ["api", "rest", "claude"]

        # Verify providers/categories updated
        data = manager.load()
        assert "anthropic" in data["providers"]
        assert "api" in data["categories"]

    def test_update_page(self, tmp_path: Path) -> None:
        """Should update specific fields of a page."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        # Add initial entry
        entry = ManifestEntry(
            provider="anthropic",
            url=HttpUrl("https://docs.anthropic.com/guide"),
            local_path=Path("docs/guide.md"),
            hash="a" * 64,
            last_fetched=datetime.now(),
            category="guides",
            title="Original Title",
            topics=["guide"],
        )
        manager.add_entry(entry)

        # Get the ID
        retrieved = manager.get_entry(str(entry.url))
        assert retrieved is not None
        page_id = retrieved.id

        # Update specific fields
        manager.update_page(
            page_id,
            title="Updated Title",
            topics=["guide", "tutorial", "getting-started"],
        )

        # Verify updates
        updated = manager.get_entry(str(entry.url))
        assert updated is not None
        assert updated.title == "Updated Title"
        assert updated.topics == ["guide", "tutorial", "getting-started"]
        assert updated.hash == "a" * 64  # Hash should be unchanged

    def test_search_pages(self, tmp_path: Path) -> None:
        """Should search pages by query."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        # Add test entries
        entries_data = [
            {
                "provider": "anthropic",
                "url": "https://docs.anthropic.com/api",
                "title": "API Reference",
                "description": "Complete API documentation for Claude",
                "category": "api",
                "topics": ["api", "rest", "claude"],
            },
            {
                "provider": "anthropic",
                "url": "https://docs.anthropic.com/guide",
                "title": "Getting Started Guide",
                "description": "Learn how to use Claude",
                "category": "guides",
                "topics": ["guide", "tutorial"],
            },
            {
                "provider": "openai",
                "url": "https://platform.openai.com/docs",
                "title": "OpenAI Documentation",
                "description": "GPT-4 and ChatGPT documentation",
                "category": "api",
                "topics": ["api", "gpt"],
            },
        ]

        for data in entries_data:
            entry = ManifestEntry(
                provider=data["provider"],
                url=HttpUrl(data["url"]),
                local_path=Path(f"docs/{data['category']}.md"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category=data["category"],
                title=data.get("title"),
                description=data.get("description"),
                topics=data.get("topics", []),
            )
            manager.add_entry(entry)

        # Search by title
        results = manager.search_pages("API Reference")
        assert len(results) == 1
        assert results[0].title == "API Reference"

        # Search by description
        results = manager.search_pages("Claude")
        assert len(results) == 2  # Both Anthropic docs mention Claude

        # Search by topics
        results = manager.search_pages("tutorial")
        assert len(results) == 1
        assert "tutorial" in results[0].topics

        # Search with provider filter
        results = manager.search_pages("api", provider="anthropic")
        assert len(results) == 1
        assert results[0].provider == "anthropic"

        # Search with category filter
        results = manager.search_pages("documentation", category="api")
        assert len(results) == 2  # Both API category docs

        # Empty query returns nothing
        results = manager.search_pages("")
        assert len(results) == 0

    def test_get_providers(self, tmp_path: Path) -> None:
        """Should return list of providers."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        # Initially empty
        assert manager.get_providers() == []

        # Add entries from different providers
        for provider in ["anthropic", "openai", "anthropic"]:  # Duplicate anthropic
            entry = ManifestEntry(
                provider=provider,
                url=HttpUrl(f"https://docs.{provider}.com/test"),
                local_path=Path(f"docs/{provider}.md"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category="test",
            )
            manager.add_entry(entry)

        # Should have unique, sorted providers
        providers = manager.get_providers()
        assert providers == ["anthropic", "openai"]

    def test_get_categories(self, tmp_path: Path) -> None:
        """Should return list of categories."""
        manifest_path = tmp_path / "manifest.json"
        manager = ManifestManager(manifest_path)

        # Initially empty
        assert manager.get_categories() == []

        # Add entries with different categories
        for category in ["guides", "api", "guides"]:  # Duplicate guides
            entry = ManifestEntry(
                provider="test",
                url=HttpUrl(f"https://docs.test.com/{category}"),
                local_path=Path(f"docs/{category}.md"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category=category,
            )
            manager.add_entry(entry)

        # Should have unique, sorted categories
        categories = manager.get_categories()
        assert categories == ["api", "guides"]

    def test_migrate_schema_v1_0_to_v1_1(self, tmp_path: Path) -> None:
        """Should migrate schema from v1.0 to v1.1."""
        manifest_path = tmp_path / "manifest.json"

        # Create a v1.0 manifest manually
        v1_0_data = {
            "version": "1.0",
            "last_updated": datetime.now().isoformat(),
            "documents": [
                {
                    "provider": "anthropic",
                    "url": "https://docs.anthropic.com/guide",
                    "local_path": "docs/guide.md",
                    "hash": "a" * 64,
                    "last_fetched": datetime.now().isoformat(),
                    "category": "guides",
                    "title": "Test Guide",
                    "description": "Test description",
                }
            ],
        }

        # Write v1.0 manifest
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, "w") as f:
            json.dump(v1_0_data, f)

        # Load and migrate
        manager = ManifestManager(manifest_path)
        manager.migrate_schema("1.0", "1.1")

        # Verify migration
        data = manager.load()
        assert data["version"] == "1.1"
        assert "providers" in data
        assert "categories" in data
        assert data["providers"] == ["anthropic"]
        assert data["categories"] == ["guides"]

        # Verify documents have new fields
        doc = data["documents"][0]
        assert "id" in doc
        assert "topics" in doc
        assert isinstance(doc["id"], str)
        assert isinstance(doc["topics"], list)


# ============================================================================
# Test Models - New Fields
# ============================================================================


class TestManifestEntryNewFields:
    """Tests for new ManifestEntry fields (id, topics)."""

    def test_id_auto_generation(self) -> None:
        """Should auto-generate UUID v4 for id field."""
        entry = ManifestEntry(
            provider="test",
            url=HttpUrl("https://test.com"),
            local_path=Path("test.md"),
            hash="a" * 64,
            last_fetched=datetime.now(),
            category="test",
        )

        assert entry.id
        # Verify it's a valid UUID
        import uuid as uuid_module
        uuid_obj = uuid_module.UUID(entry.id, version=4)
        assert str(uuid_obj) == entry.id

    def test_id_custom_uuid(self) -> None:
        """Should accept custom UUID v4."""
        import uuid as uuid_module
        custom_id = str(uuid_module.uuid4())

        entry = ManifestEntry(
            id=custom_id,
            provider="test",
            url=HttpUrl("https://test.com"),
            local_path=Path("test.md"),
            hash="a" * 64,
            last_fetched=datetime.now(),
            category="test",
        )

        assert entry.id == custom_id

    def test_id_invalid_uuid(self) -> None:
        """Should reject invalid UUID."""
        with pytest.raises(ValidationError):
            ManifestEntry(
                id="not-a-uuid",
                provider="test",
                url=HttpUrl("https://test.com"),
                local_path=Path("test.md"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category="test",
            )

    def test_topics_validation(self) -> None:
        """Should validate topics field."""
        entry = ManifestEntry(
            provider="test",
            url=HttpUrl("https://test.com"),
            local_path=Path("test.md"),
            hash="a" * 64,
            last_fetched=datetime.now(),
            category="test",
            topics=["API", "Rest", "Claude-AI"],
        )

        # Topics should be lowercase normalized
        assert entry.topics == ["api", "rest", "claude-ai"]

    def test_topics_max_count(self) -> None:
        """Should reject more than 20 topics."""
        with pytest.raises(ValidationError):
            ManifestEntry(
                provider="test",
                url=HttpUrl("https://test.com"),
                local_path=Path("test.md"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category="test",
                topics=[f"topic{i}" for i in range(21)],
            )

    def test_topics_max_length(self) -> None:
        """Should reject topics longer than 50 characters."""
        with pytest.raises(ValidationError):
            ManifestEntry(
                provider="test",
                url=HttpUrl("https://test.com"),
                local_path=Path("test.md"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category="test",
                topics=["a" * 51],
            )

    def test_topics_invalid_characters(self) -> None:
        """Should reject topics with invalid characters."""
        with pytest.raises(ValidationError):
            ManifestEntry(
                provider="test",
                url=HttpUrl("https://test.com"),
                local_path=Path("test.md"),
                hash="a" * 64,
                last_fetched=datetime.now(),
                category="test",
                topics=["invalid topic!"],  # Space and ! not allowed
            )


# ============================================================================
# Test CLI
# ============================================================================


class TestCLI:
    """Tests for CLI commands."""

    def test_cli_help(self) -> None:
        """Should display help message."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Documentation Fetcher" in result.output

    def test_fetch_command_help(self) -> None:
        """Should display fetch command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["fetch", "--help"])

        assert result.exit_code == 0
        assert "Fetch documentation" in result.output

    def test_list_command_help(self) -> None:
        """Should display list command help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["list", "--help"])

        assert result.exit_code == 0
        assert "List tracked documents" in result.output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
