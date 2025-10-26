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

        assert data["version"] == "1.0"
        assert "documents" in data
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
