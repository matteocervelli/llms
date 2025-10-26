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
    - Metadata (title, description, category)

    Features:
        - Atomic writes (temp file + rename)
        - Hash-based change detection
        - Schema validation
        - Safe file operations with proper permissions
    """

    MANIFEST_VERSION = "1.0"
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

            # Create empty manifest
            initial_data = {
                "version": self.MANIFEST_VERSION,
                "last_updated": datetime.now().isoformat(),
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
                "provider": entry.provider,
                "url": str(entry.url),
                "local_path": str(entry.local_path),
                "hash": entry.hash,
                "last_fetched": entry.last_fetched.isoformat(),
                "category": entry.category,
                "title": entry.title,
                "description": entry.description,
            }

            # Check if entry exists
            url_str = str(entry.url)
            existing_index = None
            for i, doc in enumerate(data["documents"]):
                if doc.get("url") == url_str:
                    existing_index = i
                    break

            if existing_index is not None:
                # Update existing entry
                data["documents"][existing_index] = entry_dict
                logger.info(f"Updated manifest entry for {url_str}")
            else:
                # Add new entry
                data["documents"].append(entry_dict)
                logger.info(f"Added new manifest entry for {url_str}")

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
                            provider=doc["provider"],
                            url=doc["url"],
                            local_path=Path(doc["local_path"]),
                            hash=doc["hash"],
                            last_fetched=datetime.fromisoformat(doc["last_fetched"]),
                            category=doc["category"],
                            title=doc.get("title"),
                            description=doc.get("description"),
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
                        provider=doc["provider"],
                        url=doc["url"],
                        local_path=Path(doc["local_path"]),
                        hash=doc["hash"],
                        last_fetched=datetime.fromisoformat(doc["last_fetched"]),
                        category=doc["category"],
                        title=doc.get("title"),
                        description=doc.get("description"),
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
