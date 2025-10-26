"""
Pydantic data models for the Documentation Fetcher tool.

Models provide validation, serialization, and type safety for:
- DocumentSource: Configuration for a documentation source
- FetchResult: Result of fetching a URL
- ManifestEntry: Entry in the documentation manifest
- ManifestSchema: Top-level manifest structure
- ProviderConfig: Configuration for an LLM provider
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class DocumentSource(BaseModel):
    """
    Configuration for a documentation source.

    Attributes:
        url: Source URL for the documentation
        provider: Provider name (e.g., 'anthropic', 'openai')
        category: Documentation category (e.g., 'guides', 'api', 'reference')
        last_fetched: Timestamp of last successful fetch
        hash: SHA-256 hash of content for change detection
    """

    url: HttpUrl
    provider: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=100)
    last_fetched: Optional[datetime] = None
    hash: Optional[str] = Field(None, pattern=r"^[a-f0-9]{64}$")

    @field_validator("provider", "category")
    @classmethod
    def validate_alphanumeric(cls, v: str) -> str:
        """Validate that provider and category are alphanumeric with hyphens/underscores."""
        if not all(c.isalnum() or c in "-_" for c in v):
            raise ValueError("Must contain only alphanumeric characters, hyphens, or underscores")
        return v.lower()


class FetchResult(BaseModel):
    """
    Result of fetching a URL.

    Attributes:
        success: Whether the fetch was successful
        url: The URL that was fetched
        content: The fetched content (HTML)
        hash: SHA-256 hash of the content
        error: Error message if fetch failed
        status_code: HTTP status code
        content_type: Content-Type header value
    """

    success: bool
    url: HttpUrl
    content: Optional[str] = None
    hash: Optional[str] = Field(None, pattern=r"^[a-f0-9]{64}$")
    error: Optional[str] = None
    status_code: Optional[int] = Field(None, ge=100, le=599)
    content_type: Optional[str] = None

    @field_validator("status_code")
    @classmethod
    def validate_status_code(cls, v: Optional[int]) -> Optional[int]:
        """Validate HTTP status code is in valid range."""
        if v is not None and not (100 <= v <= 599):
            raise ValueError("Status code must be between 100 and 599")
        return v


class ManifestEntry(BaseModel):
    """
    Entry in the documentation manifest.

    Attributes:
        id: Unique identifier (UUID v4)
        provider: Provider name
        url: Source URL
        local_path: Local file path where content is saved
        hash: SHA-256 hash of the content
        last_fetched: Timestamp of last fetch
        category: Documentation category
        title: Document title (extracted from HTML)
        description: Document description (extracted from HTML)
        topics: List of topics/tags for categorization (max 20, max 50 chars each)
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider: str = Field(..., min_length=1, max_length=100)
    url: HttpUrl
    local_path: Path
    hash: str = Field(..., pattern=r"^[a-f0-9]{64}$")
    last_fetched: datetime
    category: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = Field(None, max_length=1000)
    topics: list[str] = Field(default_factory=list, max_length=20)

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate id is a valid UUID v4."""
        try:
            uuid_obj = uuid.UUID(v, version=4)
            # Ensure it's the same string representation (handles case sensitivity)
            return str(uuid_obj)
        except (ValueError, AttributeError):
            raise ValueError(f"ID must be a valid UUID v4, got: {v}")

    @field_validator("local_path")
    @classmethod
    def validate_local_path(cls, v: Path) -> Path:
        """Validate local_path doesn't contain path traversal attempts."""
        # Convert to string and check for dangerous patterns
        path_str = str(v)
        if ".." in path_str or path_str.startswith("/"):
            raise ValueError("Path must not contain '..' or be absolute")
        return v

    @field_validator("topics")
    @classmethod
    def validate_topics(cls, v: list[str]) -> list[str]:
        """Validate topics list content and format."""
        if len(v) > 20:
            raise ValueError("Maximum 20 topics allowed")

        validated_topics = []
        for topic in v:
            # Check length
            if len(topic) > 50:
                raise ValueError(f"Topic '{topic}' exceeds 50 characters")

            # Check characters (alphanumeric + hyphens/underscores)
            if not all(c.isalnum() or c in "-_" for c in topic):
                raise ValueError(
                    f"Topic '{topic}' must contain only alphanumeric characters, hyphens, or underscores"
                )

            # Normalize to lowercase
            validated_topics.append(topic.lower())

        return validated_topics

    class Config:
        """Pydantic configuration."""

        json_encoders = {
            Path: str,
            datetime: lambda v: v.isoformat(),
        }


class ProviderConfig(BaseModel):
    """
    Configuration for an LLM provider.

    Attributes:
        name: Provider name (e.g., 'anthropic', 'openai')
        base_url: Base URL for the provider's documentation
        rate_limit: Maximum requests per second
        robots_txt_url: URL to the provider's robots.txt
        sources: List of documentation sources to fetch
    """

    name: str = Field(..., min_length=1, max_length=100)
    base_url: HttpUrl
    rate_limit: float = Field(default=1.0, gt=0, le=10)
    robots_txt_url: Optional[HttpUrl] = None
    sources: list[DocumentSource] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate provider name is alphanumeric with hyphens/underscores."""
        if not all(c.isalnum() or c in "-_" for c in v):
            raise ValueError(
                "Name must contain only alphanumeric characters, hyphens, or underscores"
            )
        return v.lower()

    @field_validator("rate_limit")
    @classmethod
    def validate_rate_limit(cls, v: float) -> float:
        """Validate rate limit is reasonable."""
        if v <= 0:
            raise ValueError("Rate limit must be positive")
        if v > 10:
            raise ValueError("Rate limit must not exceed 10 requests/second")
        return v


class ManifestSchema(BaseModel):
    """
    Top-level manifest structure for documentation tracking.

    Attributes:
        version: Schema version (e.g., "1.1")
        last_updated: Timestamp of last manifest update
        providers: List of unique providers tracked
        categories: List of unique categories tracked
        documents: List of document entries
    """

    version: str = Field(..., pattern=r"^\d+\.\d+$")
    last_updated: datetime
    providers: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    documents: list[dict] = Field(default_factory=list)

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate version format (major.minor)."""
        parts = v.split(".")
        if len(parts) != 2:
            raise ValueError("Version must be in format 'major.minor'")
        try:
            int(parts[0])
            int(parts[1])
        except ValueError:
            raise ValueError("Version parts must be integers")
        return v

    class Config:
        """Pydantic configuration."""

        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
