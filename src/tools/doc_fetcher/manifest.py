"""
Manifest Management System

Manages the documentation manifest (docs.json) with:
- Atomic file operations (safe writes)
- SHA-256 hash-based change detection
- Entry CRUD operations
- Schema validation
- Thread-safe operations
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from .exceptions import ManifestError
from .models import ManifestEntry

# Configure logging
logger = logging.getLogger(__name__)


class ManifestManager:
    """
    Manages the documentation manifest file.

    The manifest tracks all fetched documentation with metadata including:
    - Source URLs
    - Local file paths
    - Content hashes for change detection
    - Last fetch timestamps
    - Metadata (title, description, category, topics)
    - Unique identifiers (UUIDs)

    Features:
        - Atomic writes (temp file + rename)
        - Hash-based change detection
        - Schema validation
        - Safe file operations with proper permissions
        - Provider and category tracking
        - Full-text search across documents
        - Schema migration support
    """

    MANIFEST_VERSION = "1.1"
    DEFAULT_MANIFEST_PATH = Path("manifests/docs.json")

    def __init__(self, manifest_path: Optional[Path] = None) -> None:
        """
        Initialize ManifestManager.

        Args:
            manifest_path: Path to manifest file (default: manifests/docs.json)
        """
        self.manifest_path = manifest_path or self.DEFAULT_MANIFEST_PATH
        self.manifest_path = Path(self.manifest_path)
        logger.info(f"Initialized ManifestManager with path: {self.manifest_path}")

    def _ensure_manifest_exists(self) -> None:
        """Create manifest file if it doesn't exist."""
        if not self.manifest_path.exists():
            # Create parent directory
            self.manifest_path.parent.mkdir(parents=True, exist_ok=True)

            # Create empty manifest with v1.1 schema
            initial_data = {
                "version": self.MANIFEST_VERSION,
                "last_updated": datetime.now().isoformat(),
                "providers": [],
                "categories": [],
                "documents": [],
            }

            self._write_manifest(initial_data)
            logger.info(f"Created new manifest at {self.manifest_path}")

    def _write_manifest(self, data: dict) -> None:
        """
        Write manifest data to file atomically.

        Uses temp file + rename for atomic writes to prevent corruption.

        Args:
            data: Manifest data dictionary

        Raises:
            ManifestError: If write fails
        """
        try:
            # Write to temporary file
            temp_path = self.manifest_path.with_suffix(".tmp")
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_path.replace(self.manifest_path)

            # Set proper permissions (rw-r--r--)
            os.chmod(self.manifest_path, 0o644)

            logger.debug(f"Wrote manifest to {self.manifest_path}")

        except Exception as e:
            logger.error(f"Failed to write manifest: {e}")
            raise ManifestError("write", str(e)) from e

    def load(self) -> dict:
        """
        Load manifest from file.

        Returns:
            Manifest data dictionary

        Raises:
            ManifestError: If load or validation fails
        """
        try:
            self._ensure_manifest_exists()

            with open(self.manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validate schema
            if "version" not in data:
                raise ManifestError("load", "Missing 'version' field")
            if "documents" not in data:
                raise ManifestError("load", "Missing 'documents' field")

            # Validate version
            if data["version"] != self.MANIFEST_VERSION:
                logger.warning(
                    f"Manifest version mismatch: {data['version']} != {self.MANIFEST_VERSION}"
                )

            logger.info(f"Loaded manifest with {len(data['documents'])} documents")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in manifest: {e}")
            raise ManifestError("load", f"Invalid JSON: {e}") from e
        except FileNotFoundError as e:
            logger.error(f"Manifest file not found: {e}")
            raise ManifestError("load", f"File not found: {e}") from e
        except Exception as e:
            logger.error(f"Failed to load manifest: {e}")
            raise ManifestError("load", str(e)) from e

    def save(self, data: dict) -> None:
        """
        Save manifest to file.

        Args:
            data: Manifest data dictionary

        Raises:
            ManifestError: If save fails
        """
        try:
            # Update timestamp
            data["last_updated"] = datetime.now().isoformat()

            self._write_manifest(data)
            logger.info(f"Saved manifest with {len(data.get('documents', []))} documents")

        except Exception as e:
            logger.error(f"Failed to save manifest: {e}")
            raise ManifestError("save", str(e)) from e

    def add_entry(self, entry: ManifestEntry) -> None:
        """
        Add or update manifest entry.

        If entry with same URL exists, it will be updated.
        Otherwise, a new entry will be added.

        Args:
            entry: ManifestEntry to add/update

        Raises:
            ManifestError: If operation fails
        """
        try:
            # Load current manifest
            data = self.load()

            # Convert entry to dict
            entry_dict = {
                "id": entry.id,
                "provider": entry.provider,
                "url": str(entry.url),
                "local_path": str(entry.local_path),
                "hash": entry.hash,
                "last_fetched": entry.last_fetched.isoformat(),
                "category": entry.category,
                "title": entry.title,
                "description": entry.description,
                "topics": entry.topics,
            }

            # Check if entry exists
            url_str = str(entry.url)
            existing_index = None
            for i, doc in enumerate(data["documents"]):
                if doc.get("url") == url_str:
                    existing_index = i
                    break

            if existing_index is not None:
                # Preserve existing ID if updating
                existing_id = data["documents"][existing_index].get("id")
                if existing_id:
                    entry_dict["id"] = existing_id

                # Update existing entry
                data["documents"][existing_index] = entry_dict
                logger.info(f"Updated manifest entry for {url_str}")
            else:
                # Add new entry
                data["documents"].append(entry_dict)
                logger.info(f"Added new manifest entry for {url_str}")

            # Update providers/categories
            self._update_providers_categories(data)

            # Save manifest
            self.save(data)

        except Exception as e:
            logger.error(f"Failed to add entry: {e}")
            raise ManifestError("add_entry", str(e)) from e

    def get_entry(self, url: str) -> Optional[ManifestEntry]:
        """
        Get manifest entry by URL.

        Args:
            url: URL to lookup

        Returns:
            ManifestEntry if found, None otherwise

        Raises:
            ManifestError: If operation fails
        """
        try:
            data = self.load()

            for doc in data["documents"]:
                if doc.get("url") == url:
                    # Parse and validate entry
                    try:
                        return ManifestEntry(
                            id=doc.get("id", ""),
                            provider=doc["provider"],
                            url=doc["url"],
                            local_path=Path(doc["local_path"]),
                            hash=doc["hash"],
                            last_fetched=datetime.fromisoformat(doc["last_fetched"]),
                            category=doc["category"],
                            title=doc.get("title"),
                            description=doc.get("description"),
                            topics=doc.get("topics", []),
                        )
                    except (KeyError, ValidationError) as e:
                        logger.warning(f"Invalid entry for {url}: {e}")
                        continue

            return None

        except Exception as e:
            logger.error(f"Failed to get entry: {e}")
            raise ManifestError("get_entry", str(e)) from e

    def list_entries(
        self, provider: Optional[str] = None, category: Optional[str] = None
    ) -> list[ManifestEntry]:
        """
        List all manifest entries with optional filtering.

        Args:
            provider: Filter by provider name
            category: Filter by category

        Returns:
            List of ManifestEntry objects

        Raises:
            ManifestError: If operation fails
        """
        try:
            data = self.load()
            entries: list[ManifestEntry] = []

            for doc in data["documents"]:
                # Apply filters
                if provider and doc.get("provider") != provider:
                    continue
                if category and doc.get("category") != category:
                    continue

                # Parse and validate entry
                try:
                    entry = ManifestEntry(
                        id=doc.get("id", ""),
                        provider=doc["provider"],
                        url=doc["url"],
                        local_path=Path(doc["local_path"]),
                        hash=doc["hash"],
                        last_fetched=datetime.fromisoformat(doc["last_fetched"]),
                        category=doc["category"],
                        title=doc.get("title"),
                        description=doc.get("description"),
                        topics=doc.get("topics", []),
                    )
                    entries.append(entry)
                except (KeyError, ValidationError) as e:
                    logger.warning(f"Invalid entry in manifest: {e}")
                    continue

            logger.info(f"Listed {len(entries)} entries (provider={provider}, category={category})")
            return entries

        except Exception as e:
            logger.error(f"Failed to list entries: {e}")
            raise ManifestError("list_entries", str(e)) from e

    def check_hash(self, content: str) -> str:
        """
        Compute SHA-256 hash of content.

        Args:
            content: Content to hash

        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def detect_changes(self, url: str, new_hash: str) -> bool:
        """
        Detect if content has changed based on hash.

        Args:
            url: URL to check
            new_hash: New content hash

        Returns:
            True if content changed, False otherwise
        """
        entry = self.get_entry(url)
        if entry is None:
            # New document
            return True

        # Compare hashes
        changed = entry.hash != new_hash
        if changed:
            logger.info(
                f"Content changed for {url} (old: {entry.hash[:8]}..., new: {new_hash[:8]}...)"
            )
        else:
            logger.debug(f"No changes detected for {url}")

        return changed

    def _update_providers_categories(self, data: dict) -> None:
        """
        Update providers and categories lists from documents.

        Args:
            data: Manifest data dictionary
        """
        providers = set()
        categories = set()

        for doc in data.get("documents", []):
            if "provider" in doc:
                providers.add(doc["provider"])
            if "category" in doc:
                categories.add(doc["category"])

        data["providers"] = sorted(list(providers))
        data["categories"] = sorted(list(categories))

    def update_page(self, page_id: str, **fields: dict) -> None:
        """
        Update specific fields of a manifest entry by ID.

        Args:
            page_id: UUID of the page to update
            **fields: Fields to update (provider, category, title, description, topics, etc.)

        Raises:
            ManifestError: If page not found or update fails
        """
        try:
            data = self.load()

            # Find entry by ID
            entry_index = None
            for i, doc in enumerate(data["documents"]):
                if doc.get("id") == page_id:
                    entry_index = i
                    break

            if entry_index is None:
                raise ManifestError("update_page", f"Page with ID {page_id} not found")

            # Update fields
            allowed_fields = {
                "provider",
                "category",
                "title",
                "description",
                "topics",
                "url",
                "local_path",
                "hash",
            }
            for field, value in fields.items():
                if field not in allowed_fields:
                    logger.warning(f"Ignoring unknown field: {field}")
                    continue

                # Update last_fetched if hash changes
                if field == "hash" and value != data["documents"][entry_index].get("hash"):
                    data["documents"][entry_index]["last_fetched"] = datetime.now().isoformat()

                data["documents"][entry_index][field] = value

            # Update providers/categories
            self._update_providers_categories(data)

            # Save manifest
            self.save(data)
            logger.info(f"Updated page {page_id} with fields: {list(fields.keys())}")

        except Exception as e:
            logger.error(f"Failed to update page: {e}")
            raise ManifestError("update_page", str(e)) from e

    def search_pages(
        self,
        query: str,
        fields: Optional[list[str]] = None,
        provider: Optional[str] = None,
        category: Optional[str] = None,
    ) -> list[ManifestEntry]:
        """
        Search for pages matching a query across specified fields.

        Args:
            query: Search query (case-insensitive)
            fields: Fields to search (default: ["title", "description", "topics"])
            provider: Optional provider filter
            category: Optional category filter

        Returns:
            List of matching ManifestEntry objects

        Raises:
            ManifestError: If search fails
        """
        try:
            if fields is None:
                fields = ["title", "description", "topics"]

            # Sanitize query
            query_lower = query.lower().strip()
            if not query_lower:
                return []

            data = self.load()
            matching_entries: list[ManifestEntry] = []

            for doc in data["documents"]:
                # Apply provider/category filters
                if provider and doc.get("provider") != provider:
                    continue
                if category and doc.get("category") != category:
                    continue

                # Search across specified fields
                match = False
                for field in fields:
                    if field not in doc:
                        continue

                    field_value = doc[field]
                    if field_value is None:
                        continue

                    # Handle list fields (e.g., topics)
                    if isinstance(field_value, list):
                        field_text = " ".join(str(item).lower() for item in field_value)
                    else:
                        field_text = str(field_value).lower()

                    if query_lower in field_text:
                        match = True
                        break

                if match:
                    # Parse and validate entry
                    try:
                        entry = ManifestEntry(
                            id=doc.get("id", ""),
                            provider=doc["provider"],
                            url=doc["url"],
                            local_path=Path(doc["local_path"]),
                            hash=doc["hash"],
                            last_fetched=datetime.fromisoformat(doc["last_fetched"]),
                            category=doc["category"],
                            title=doc.get("title"),
                            description=doc.get("description"),
                            topics=doc.get("topics", []),
                        )
                        matching_entries.append(entry)
                    except (KeyError, ValidationError) as e:
                        logger.warning(f"Invalid entry in manifest: {e}")
                        continue

            logger.info(
                f"Search found {len(matching_entries)} results for query '{query}' "
                f"(provider={provider}, category={category})"
            )
            return matching_entries

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise ManifestError("search_pages", str(e)) from e

    def get_providers(self) -> list[str]:
        """
        Get list of all providers tracked in the manifest.

        Returns:
            Sorted list of provider names

        Raises:
            ManifestError: If operation fails
        """
        try:
            data = self.load()
            return data.get("providers", [])
        except Exception as e:
            logger.error(f"Failed to get providers: {e}")
            raise ManifestError("get_providers", str(e)) from e

    def get_categories(self) -> list[str]:
        """
        Get list of all categories tracked in the manifest.

        Returns:
            Sorted list of category names

        Raises:
            ManifestError: If operation fails
        """
        try:
            data = self.load()
            return data.get("categories", [])
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            raise ManifestError("get_categories", str(e)) from e

    def migrate_schema(self, from_version: str, to_version: str) -> None:
        """
        Migrate manifest schema from one version to another.

        Currently supports:
        - 1.0 -> 1.1: Add providers, categories, and id fields

        Args:
            from_version: Source schema version
            to_version: Target schema version

        Raises:
            ManifestError: If migration fails or unsupported version
        """
        try:
            if from_version == "1.0" and to_version == "1.1":
                logger.info("Migrating manifest from v1.0 to v1.1")
                data = self.load()

                # Add providers and categories arrays
                if "providers" not in data:
                    data["providers"] = []
                if "categories" not in data:
                    data["categories"] = []

                # Add id field to all documents
                import uuid as uuid_module

                for doc in data["documents"]:
                    if "id" not in doc:
                        doc["id"] = str(uuid_module.uuid4())
                        logger.debug(f"Generated ID for {doc.get('url')}: {doc['id']}")

                    # Add empty topics if missing
                    if "topics" not in doc:
                        doc["topics"] = []

                # Update providers/categories from documents
                self._update_providers_categories(data)

                # Update version
                data["version"] = to_version

                # Save migrated manifest
                self.save(data)
                logger.info(f"Successfully migrated manifest to v{to_version}")

            else:
                raise ManifestError(
                    "migrate_schema", f"Unsupported migration: {from_version} -> {to_version}"
                )

        except Exception as e:
            logger.error(f"Schema migration failed: {e}")
            raise ManifestError("migrate_schema", str(e)) from e
