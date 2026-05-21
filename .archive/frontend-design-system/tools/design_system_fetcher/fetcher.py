"""
Core design system fetching logic.

This module handles fetching design system documentation from URLs using the
DocumentationCrawler. It manages the crawling process, error handling, and
integration with the token extraction and storage modules.

Example:
    >>> import asyncio
    >>> from fetcher import DesignSystemFetcher
    >>> from token_extractor import DesignTokenExtractor
    >>> from storage import DesignTokenStorage
    >>>
    >>> async def main():
    ...     fetcher = DesignSystemFetcher(
    ...         rate_limit=1.0,
    ...         crawler_path="/path/to/crawler.py"
    ...     )
    ...     markdown = await fetcher.fetch(
    ...         url="https://m3.material.io/",
    ...         system_name="Material Design"
    ...     )
    ...     print(f"Fetched {len(markdown)} characters")
    >>>
    >>> asyncio.run(main())
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add src and src/tools/doc_fetcher to path for crawler import
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(src_path / "tools" / "doc_fetcher"))

from tools.doc_fetcher.crawler import DocumentationCrawler
from tools.doc_fetcher.exceptions import CrawlError


class DesignSystemFetcher:
    """
    Fetches design system documentation using DocumentationCrawler.

    This class manages the crawling process for design system URLs,
    handles errors gracefully, and provides metadata about fetched content.

    Attributes:
        crawler: DocumentationCrawler instance for fetching URLs
        rate_limit: Maximum requests per second (default: 1.0)
    """

    def __init__(self, rate_limit: float = 1.0) -> None:
        """
        Initialize the design system fetcher.

        Args:
            rate_limit: Maximum requests per second (default: 1.0)
        """
        self.rate_limit = rate_limit
        self.crawler = DocumentationCrawler(rate_limit=rate_limit)

    async def fetch(
        self, url: str, system_name: str, max_retries: int = 3
    ) -> tuple[str, dict]:
        """
        Fetch design system documentation from a URL.

        Attempts to fetch the URL with retry logic. Returns both the markdown
        content and metadata about the fetch operation.

        Args:
            url: URL of the design system documentation
            system_name: Human-readable name of the design system
            max_retries: Maximum number of retry attempts (default: 3)

        Returns:
            Tuple of (markdown_content, metadata_dict)
            Metadata includes: title, description, url, fetched_at, content_hash

        Raises:
            CrawlError: If fetching fails after all retries

        Example:
            >>> markdown, metadata = await fetcher.fetch(
            ...     url="https://m3.material.io/",
            ...     system_name="Material Design"
            ... )
            >>> print(metadata['fetched_at'])
            '2024-01-15T10:30:00.000000'
        """
        last_error = None
        retry_delay = 2  # Start with 2 second delay

        for attempt in range(max_retries):
            try:
                markdown, metadata, content_hash = await self.crawler.crawl_url(
                    url, use_fit_markdown=True, remove_overlay=True
                )

                # Enrich metadata
                metadata["system_name"] = system_name
                metadata["fetched_at"] = datetime.utcnow().isoformat()
                metadata["content_hash"] = content_hash

                return markdown, metadata

            except CrawlError as e:
                last_error = e
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff

        raise CrawlError(f"Failed to fetch {url} after {max_retries} attempts: {last_error}")

    async def fetch_multiple(
        self, urls: list[tuple[str, str]], max_concurrent: int = 3
    ) -> list[tuple[str, str, dict]]:
        """
        Fetch multiple design system URLs concurrently.

        Args:
            urls: List of (url, system_name) tuples
            max_concurrent: Maximum concurrent requests (default: 3)

        Returns:
            List of (system_name, markdown, metadata) tuples

        Example:
            >>> urls = [
            ...     ("https://m3.material.io/", "Material Design"),
            ...     ("https://design.figma.com/", "Figma Design"),
            ... ]
            >>> results = await fetcher.fetch_multiple(urls, max_concurrent=2)
            >>> for name, markdown, meta in results:
            ...     print(f"{name}: {len(markdown)} chars")
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def fetch_with_semaphore(url: str, name: str) -> tuple[str, str, dict]:
            async with semaphore:
                markdown, metadata = await self.fetch(url, name)
                return (name, markdown, metadata)

        tasks = [fetch_with_semaphore(url, name) for url, name in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return successful results
        successful_results = []
        for result in results:
            if isinstance(result, Exception):
                print(f"Error during fetch: {result}")
            else:
                successful_results.append(result)

        return successful_results
