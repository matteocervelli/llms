"""
HTML Fetcher with Rate Limiting

Handles HTTP requests with:
- Rate limiting (token bucket algorithm)
- robots.txt compliance
- Request validation and security
- Retry logic with exponential backoff
- Comprehensive error handling
"""

import hashlib
import logging
import time
from typing import Optional
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from pydantic import HttpUrl

from .exceptions import FetchError, RateLimitError
from .models import FetchResult

# Configure logging
logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Token bucket rate limiter.

    Implements a token bucket algorithm to limit request rate.
    Tokens are added at a fixed rate and consumed by requests.
    """

    def __init__(self, rate: float = 1.0, capacity: int = 5) -> None:
        """
        Initialize RateLimiter.

        Args:
            rate: Tokens added per second (requests per second)
            capacity: Maximum tokens in bucket
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = float(capacity)
        self.last_update = time.time()

    def _add_tokens(self) -> None:
        """Add tokens based on elapsed time since last update."""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now

    def acquire(self, tokens: int = 1) -> None:
        """
        Acquire tokens, blocking if necessary.

        Args:
            tokens: Number of tokens to acquire

        Raises:
            RateLimitError: If unable to acquire tokens immediately
        """
        self._add_tokens()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return

        # Calculate wait time
        wait_time = (tokens - self.tokens) / self.rate
        raise RateLimitError(wait_time)

    def try_acquire(self, tokens: int = 1) -> bool:
        """
        Try to acquire tokens without blocking.

        Args:
            tokens: Number of tokens to acquire

        Returns:
            True if tokens acquired, False otherwise
        """
        self._add_tokens()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


class DocumentFetcher:
    """
    Fetches documentation from URLs with rate limiting and validation.

    Features:
        - Rate limiting with configurable rate
        - robots.txt compliance
        - URL validation and sanitization
        - Retry logic with exponential backoff
        - Content hashing for change detection
    """

    # Security: Only allow HTTPS for documentation
    ALLOWED_PROTOCOLS = ["https"]

    # Security: Whitelist of allowed domains
    ALLOWED_DOMAINS = [
        "docs.anthropic.com",  # Legacy domain
        "docs.claude.com",  # New Claude documentation domain
        "platform.openai.com",
        "docs.openai.com",
        "claude.ai",
    ]

    # Maximum response size (10 MB)
    MAX_RESPONSE_SIZE = 10 * 1024 * 1024

    # Request timeout (30 seconds)
    REQUEST_TIMEOUT = 30

    def __init__(self, rate_limit: float = 1.0, respect_robots: bool = True) -> None:
        """
        Initialize DocumentFetcher.

        Args:
            rate_limit: Maximum requests per second
            respect_robots: Whether to respect robots.txt
        """
        self.rate_limiter = RateLimiter(rate=rate_limit)
        self.respect_robots = respect_robots
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "LLM-Config-Manager/0.1.0 (Documentation Fetcher; +https://github.com/matteocervelli/llms)"
            }
        )
        self.robots_cache: dict[str, RobotFileParser] = {}
        logger.info(f"Initialized DocumentFetcher with rate_limit={rate_limit}")

    def _validate_url(self, url: str) -> None:
        """
        Validate URL for security and correctness.

        Args:
            url: URL to validate

        Raises:
            FetchError: If URL is invalid or not allowed
        """
        parsed = urlparse(url)

        # Check protocol
        if parsed.scheme not in self.ALLOWED_PROTOCOLS:
            raise FetchError(url, f"Protocol '{parsed.scheme}' not allowed. Use HTTPS.")

        # Check domain whitelist
        if parsed.netloc not in self.ALLOWED_DOMAINS:
            raise FetchError(
                url,
                f"Domain '{parsed.netloc}' not in whitelist: {', '.join(self.ALLOWED_DOMAINS)}",
            )

    def _get_robots_parser(self, base_url: str) -> RobotFileParser:
        """
        Get robots.txt parser for base URL.

        Args:
            base_url: Base URL to get robots.txt from

        Returns:
            RobotFileParser instance
        """
        if base_url in self.robots_cache:
            return self.robots_cache[base_url]

        parser = RobotFileParser()
        robots_url = urljoin(base_url, "/robots.txt")

        try:
            parser.set_url(robots_url)
            parser.read()
            self.robots_cache[base_url] = parser
            logger.info(f"Loaded robots.txt from {robots_url}")
        except Exception as e:
            logger.warning(f"Failed to load robots.txt from {robots_url}: {e}")
            # Create permissive parser if robots.txt unavailable
            parser = RobotFileParser()
            self.robots_cache[base_url] = parser

        return parser

    def _check_robots_permission(self, url: str) -> None:
        """
        Check if robots.txt allows fetching the URL.

        Args:
            url: URL to check

        Raises:
            FetchError: If robots.txt disallows the URL
        """
        if not self.respect_robots:
            return

        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        parser = self._get_robots_parser(base_url)

        user_agent = self.session.headers.get("User-Agent", "*")
        if not parser.can_fetch(user_agent, url):
            raise FetchError(url, "Disallowed by robots.txt")

    def _compute_hash(self, content: str) -> str:
        """
        Compute SHA-256 hash of content.

        Args:
            content: Content to hash

        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def fetch(self, url: HttpUrl, retry_count: int = 3) -> FetchResult:
        """
        Fetch URL with rate limiting and validation.

        Args:
            url: URL to fetch
            retry_count: Number of retries on failure

        Returns:
            FetchResult with success status and content

        Raises:
            RateLimitError: If rate limit exceeded
        """
        url_str = str(url)
        logger.info(f"Fetching {url_str}")

        # Validate URL
        try:
            self._validate_url(url_str)
        except FetchError as e:
            logger.error(f"URL validation failed: {e}")
            return FetchResult(success=False, url=url, error=str(e))

        # Check robots.txt
        try:
            self._check_robots_permission(url_str)
        except FetchError as e:
            logger.error(f"robots.txt check failed: {e}")
            return FetchResult(success=False, url=url, error=str(e))

        # Rate limiting
        self.rate_limiter.acquire()

        # Fetch with retry logic
        last_error: Optional[str] = None
        for attempt in range(retry_count):
            try:
                response = self.session.get(
                    url_str,
                    timeout=self.REQUEST_TIMEOUT,
                    stream=True,
                )

                # Check response size
                content_length = response.headers.get("content-length")
                if content_length and int(content_length) > self.MAX_RESPONSE_SIZE:
                    error_msg = f"Response too large: {content_length} bytes"
                    logger.error(error_msg)
                    return FetchResult(
                        success=False,
                        url=url,
                        error=error_msg,
                        status_code=response.status_code,
                    )

                # Read content with size limit
                content = ""
                total_size = 0
                for chunk in response.iter_content(chunk_size=8192, decode_unicode=True):
                    if chunk:
                        total_size += len(chunk)
                        if total_size > self.MAX_RESPONSE_SIZE:
                            error_msg = "Response exceeded size limit during streaming"
                            logger.error(error_msg)
                            return FetchResult(
                                success=False,
                                url=url,
                                error=error_msg,
                                status_code=response.status_code,
                            )
                        content += chunk

                response.raise_for_status()

                # Compute hash
                content_hash = self._compute_hash(content)

                logger.info(
                    f"Successfully fetched {url_str} ({len(content)} bytes, hash: {content_hash[:8]}...)"
                )
                return FetchResult(
                    success=True,
                    url=url,
                    content=content,
                    hash=content_hash,
                    status_code=response.status_code,
                    content_type=response.headers.get("content-type"),
                )

            except requests.exceptions.Timeout:
                last_error = (
                    f"Timeout after {self.REQUEST_TIMEOUT}s (attempt {attempt + 1}/{retry_count})"
                )
                logger.warning(last_error)
                if attempt < retry_count - 1:
                    time.sleep(2**attempt)  # Exponential backoff

            except requests.exceptions.HTTPError as e:
                last_error = f"HTTP error: {e} (attempt {attempt + 1}/{retry_count})"
                logger.warning(last_error)
                if attempt < retry_count - 1 and e.response.status_code >= 500:
                    time.sleep(2**attempt)  # Exponential backoff for server errors
                else:
                    break  # Don't retry on client errors (4xx)

            except requests.exceptions.RequestException as e:
                last_error = f"Request failed: {e} (attempt {attempt + 1}/{retry_count})"
                logger.warning(last_error)
                if attempt < retry_count - 1:
                    time.sleep(2**attempt)  # Exponential backoff

        # All retries failed
        logger.error(f"Failed to fetch {url_str} after {retry_count} attempts: {last_error}")
        return FetchResult(success=False, url=url, error=last_error or "Unknown error")

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()
        logger.info("Closed HTTP session")
