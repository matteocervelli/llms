"""
Documentation crawler using Crawl4AI for LLM-optimized content extraction.

This module provides a DocumentationCrawler class that uses Crawl4AI to fetch
and extract high-quality markdown from documentation websites. It produces
LLM-optimized content by removing noise, preserving structure, and generating
clean markdown suitable for RAG and fine-tuning applications.

Features:
- LLM-optimized markdown extraction with "fit markdown"
- Automatic noise and boilerplate removal
- JavaScript rendering support
- Async crawling for performance
- Content filtering strategies
- Semantic structure preservation

Example:
    >>> import asyncio
    >>> from doc_fetcher.crawler import DocumentationCrawler
    >>>
    >>> async def main():
    ...     crawler = DocumentationCrawler()
    ...     markdown, metadata = await crawler.crawl_url(
    ...         "https://docs.claude.com/en/docs/claude-code/skills"
    ...     )
    ...     print(f"Title: {metadata['title']}")
    ...     print(f"Content length: {len(markdown)}")
    >>>
    >>> asyncio.run(main())
"""

import asyncio
import hashlib
import time
from typing import Optional
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

from .exceptions import CrawlError, RateLimitError


class DocumentationCrawler:
    """
    Crawls documentation sites using Crawl4AI for LLM-optimized extraction.

    This crawler uses Crawl4AI's advanced features to extract high-quality
    markdown from documentation pages. It applies content filtering to remove
    noise and boilerplate, preserving only the semantic content relevant for
    LLM consumption.

    Attributes:
        rate_limit: Maximum requests per second (default: 1.0)
        browser_config: Playwright browser configuration
        last_request_time: Timestamp of last request for rate limiting
    """

    def __init__(self, rate_limit: float = 1.0):
        """
        Initialize documentation crawler.

        Args:
            rate_limit: Maximum requests per second (default: 1.0)
        """
        self.rate_limit = rate_limit
        self.last_request_time: float = 0.0

        # Configure browser for headless crawling
        self.browser_config = BrowserConfig(
            headless=True,
            verbose=False,
        )

    def _enforce_rate_limit(self) -> None:
        """
        Enforce rate limiting by sleeping if necessary.

        Ensures requests don't exceed the configured rate_limit by calculating
        the required wait time based on the last request timestamp.
        """
        if self.rate_limit <= 0:
            return

        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        min_interval = 1.0 / self.rate_limit

        if time_since_last_request < min_interval:
            sleep_time = min_interval - time_since_last_request
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def _compute_hash(self, content: str) -> str:
        """
        Compute SHA-256 hash of content.

        Args:
            content: Content to hash

        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    async def crawl_url(
        self,
        url: str,
        use_fit_markdown: bool = True,
        remove_overlay: bool = True
    ) -> tuple[str, dict, str]:
        """
        Crawl single URL and extract LLM-optimized markdown.

        This method fetches a documentation page and extracts clean markdown
        using Crawl4AI's content filtering strategies. The "fit markdown"
        option removes noise and boilerplate while preserving semantic content.

        Args:
            url: URL to crawl
            use_fit_markdown: Use filtered markdown (removes noise)
            remove_overlay: Remove overlay elements (popups, modals)

        Returns:
            Tuple of (markdown_content, metadata_dict, content_hash)

        Raises:
            CrawlError: If crawling fails
            RateLimitError: If rate limit exceeded (shouldn't happen with enforcement)

        Example:
            >>> crawler = DocumentationCrawler(rate_limit=1.0)
            >>> markdown, meta, hash = await crawler.crawl_url(
            ...     "https://docs.claude.com/en/docs/claude-code/skills"
            ... )
            >>> print(meta["title"])
            'Agent Skills - Claude Docs'
        """
        try:
            # Enforce rate limiting before request
            self._enforce_rate_limit()

            async with AsyncWebCrawler(config=self.browser_config) as crawler:
                # Configure crawl (simplified for Crawl4AI 0.7.x compatibility)
                config = CrawlerRunConfig(
                    exclude_external_links=True,
                    remove_overlay_elements=remove_overlay,
                    word_count_threshold=10,  # Minimum words per section
                    check_robots_txt=False,  # Documentation crawling for personal use
                )

                result = await crawler.arun(url=url, config=config)

                if not result.success:
                    error_msg = result.error_message or "Unknown error"
                    raise CrawlError(f"Crawl failed for {url}: {error_msg}")

                # Extract markdown (use fit_markdown for LLM-optimized content)
                if use_fit_markdown and result.markdown.fit_markdown:
                    markdown = result.markdown.fit_markdown
                else:
                    markdown = result.markdown.raw_markdown or result.markdown.markdown_v2.raw_markdown

                if not markdown:
                    raise CrawlError(f"No markdown content extracted from {url}")

                # Extract metadata
                metadata = {
                    "title": result.metadata.get("title", ""),
                    "description": result.metadata.get("description", ""),
                    "url": url,
                    "success": result.success,
                }

                # Compute content hash
                content_hash = self._compute_hash(markdown)

                return markdown, metadata, content_hash

        except CrawlError:
            raise
        except Exception as e:
            raise CrawlError(f"Unexpected error crawling {url}: {e}")

    async def crawl_urls(
        self,
        urls: list[str],
        max_concurrent: int = 3
    ) -> list[tuple[str, str, dict, str]]:
        """
        Crawl multiple URLs with controlled concurrency.

        Fetches multiple documentation pages concurrently while respecting
        rate limits. Results are returned in the same order as input URLs.

        Args:
            urls: List of URLs to crawl
            max_concurrent: Maximum concurrent requests (default: 3)

        Returns:
            List of (url, markdown, metadata, hash) tuples

        Example:
            >>> urls = [
            ...     "https://docs.claude.com/en/docs/claude-code/skills",
            ...     "https://docs.claude.com/en/docs/claude-code/hooks",
            ... ]
            >>> results = await crawler.crawl_urls(urls, max_concurrent=2)
            >>> for url, markdown, meta, hash in results:
            ...     print(f"{meta['title']}: {len(markdown)} chars")
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def crawl_with_semaphore(url: str) -> tuple[str, str, dict, str]:
            async with semaphore:
                markdown, metadata, content_hash = await self.crawl_url(url)
                return (url, markdown, metadata, content_hash)

        tasks = [crawl_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return successful results
        successful_results = []
        for result in results:
            if isinstance(result, Exception):
                # Log error but continue
                print(f"Error: {result}")
            else:
                successful_results.append(result)

        return successful_results

    def close(self) -> None:
        """
        Close crawler and release resources.

        Note: Crawl4AI's AsyncWebCrawler uses context managers,
        so explicit closing is typically not needed.
        """
        pass
