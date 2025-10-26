"""
Custom exceptions for the Documentation Fetcher tool.

Provides specific exception types for different failure scenarios:
- FetchError: HTTP fetching failures
- ConversionError: HTML to Markdown conversion failures
- ManifestError: Manifest file operations failures
- RateLimitError: Rate limiting violations
"""


class DocFetcherError(Exception):
    """Base exception for all doc_fetcher errors."""

    pass


class FetchError(DocFetcherError):
    """
    Raised when fetching a URL fails.

    Common causes:
        - Network connectivity issues
        - HTTP errors (404, 500, etc.)
        - Timeout errors
        - Invalid URL format
        - robots.txt violations
    """

    def __init__(self, url: str, message: str) -> None:
        """
        Initialize FetchError.

        Args:
            url: The URL that failed to fetch
            message: Error description
        """
        self.url = url
        super().__init__(f"Failed to fetch {url}: {message}")


class ConversionError(DocFetcherError):
    """
    Raised when HTML to Markdown conversion fails.

    Common causes:
        - Malformed HTML
        - Unsupported HTML elements
        - Encoding issues
        - Parser failures
    """

    def __init__(self, url: str, message: str) -> None:
        """
        Initialize ConversionError.

        Args:
            url: The URL of the document being converted
            message: Error description
        """
        self.url = url
        super().__init__(f"Failed to convert {url}: {message}")


class ManifestError(DocFetcherError):
    """
    Raised when manifest operations fail.

    Common causes:
        - File I/O errors
        - JSON parsing errors
        - Schema validation failures
        - Permission errors
        - Corrupted manifest file
    """

    def __init__(self, operation: str, message: str) -> None:
        """
        Initialize ManifestError.

        Args:
            operation: The operation that failed (e.g., 'load', 'save', 'update')
            message: Error description
        """
        self.operation = operation
        super().__init__(f"Manifest operation '{operation}' failed: {message}")


class RateLimitError(DocFetcherError):
    """
    Raised when rate limiting is triggered.

    This error indicates that requests are being made too frequently
    and the rate limiter has rejected the request.
    """

    def __init__(self, wait_time: float) -> None:
        """
        Initialize RateLimitError.

        Args:
            wait_time: Seconds to wait before retry
        """
        self.wait_time = wait_time
        super().__init__(f"Rate limit exceeded. Wait {wait_time:.1f} seconds before retry.")
