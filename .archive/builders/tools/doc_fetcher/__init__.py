"""
Documentation Fetcher Tool

Automatically fetch, convert, and manage documentation from LLM provider websites.
Supports multiple providers (Anthropic, OpenAI, etc.) with intelligent change detection
and manifest tracking.

Main Components:
    - fetcher: HTTP fetching with rate limiting and robots.txt compliance
    - converter: HTML to Markdown conversion
    - manifest: Manifest management and change detection
    - models: Pydantic data models for validation
    - exceptions: Custom exceptions
    - main: CLI interface

Example Usage:
    >>> from src.tools.doc_fetcher.main import cli
    >>> # Fetch all providers
    >>> cli(['fetch', '--all'])
    >>> # Update changed documents
    >>> cli(['update'])
    >>> # List tracked documents
    >>> cli(['list'])
"""

from .exceptions import (
    ConversionError,
    FetchError,
    ManifestError,
    RateLimitError,
)
from .models import (
    DocumentSource,
    FetchResult,
    ManifestEntry,
    ProviderConfig,
)

__all__ = [
    "ConversionError",
    "FetchError",
    "ManifestError",
    "RateLimitError",
    "DocumentSource",
    "FetchResult",
    "ManifestEntry",
    "ProviderConfig",
]

__version__ = "0.1.0"
