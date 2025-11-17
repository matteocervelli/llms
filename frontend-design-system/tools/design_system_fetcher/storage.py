"""
Design token storage and file management.

This module handles saving design tokens and metadata to the design-systems/
directory structure. It manages file I/O, metadata serialization, and directory
organization.

Directory structure:
    design-systems/
    ├── {system-name}/
    │   ├── metadata.json
    │   ├── content.md
    │   └── tokens.json

Example:
    >>> from storage import DesignTokenStorage
    >>>
    >>> storage = DesignTokenStorage(
    ...     output_dir="/path/to/design-systems"
    ... )
    >>> storage.save(
    ...     system_name="Material Design",
    ...     tokens={...},
    ...     content="...",
    ...     metadata={...}
    ... )
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class DesignTokenStorage:
    """
    Manages storage and retrieval of design tokens and metadata.

    Handles file I/O for saving tokens to the design-systems/ directory
    with proper organization and metadata tracking.

    Attributes:
        output_dir: Base directory for design system storage
    """

    def __init__(self, output_dir: str | Path = "design-systems") -> None:
        """
        Initialize the storage manager.

        Args:
            output_dir: Base directory for design system storage (default: design-systems)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        system_name: str,
        tokens: dict,
        content: str,
        metadata: dict,
        overwrite: bool = True,
    ) -> Path:
        """
        Save design tokens and metadata to disk.

        Creates a system-specific directory and saves tokens, content, and metadata.
        Automatically creates necessary directories.

        Args:
            system_name: Name of the design system
            tokens: Dictionary of extracted tokens (colors, typography, etc.)
            content: Original markdown content
            metadata: Metadata dict (title, description, url, fetched_at, etc.)
            overwrite: Whether to overwrite existing files (default: True)

        Returns:
            Path to the system directory

        Raises:
            ValueError: If system_name is empty or contains invalid characters
            IOError: If file operations fail

        Example:
            >>> storage = DesignTokenStorage()
            >>> path = storage.save(
            ...     system_name="Material Design",
            ...     tokens={...},
            ...     content="...",
            ...     metadata={...}
            ... )
            >>> print(path)
            Path('design-systems/material-design')
        """
        # Validate and normalize system name
        system_name_normalized = self._normalize_name(system_name)
        if not system_name_normalized:
            raise ValueError(f"Invalid system_name: {system_name}")

        # Create system directory
        system_dir = self.output_dir / system_name_normalized
        system_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Save metadata
            self._save_metadata(system_dir, system_name, metadata)

            # Save tokens
            self._save_tokens(system_dir, tokens)

            # Save original content
            self._save_content(system_dir, content)

            logger.info(f"Saved design system '{system_name}' to {system_dir}")
            return system_dir

        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error saving design system: {e}")
            raise

    def load(self, system_name: str) -> Optional[dict]:
        """
        Load design tokens and metadata for a system.

        Args:
            system_name: Name of the design system

        Returns:
            Dictionary with keys: tokens, metadata, content
            Returns None if system directory doesn't exist

        Example:
            >>> storage = DesignTokenStorage()
            >>> data = storage.load("Material Design")
            >>> if data:
            ...     print(data['tokens']['colors'])
        """
        system_name_normalized = self._normalize_name(system_name)
        system_dir = self.output_dir / system_name_normalized

        if not system_dir.exists():
            logger.warning(f"System directory not found: {system_dir}")
            return None

        try:
            metadata = self._load_metadata(system_dir)
            tokens = self._load_tokens(system_dir)
            content = self._load_content(system_dir)

            return {
                "metadata": metadata,
                "tokens": tokens,
                "content": content,
            }

        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error loading design system: {e}")
            return None

    def list_systems(self) -> list[str]:
        """
        List all available design systems.

        Returns:
            List of system names (normalized directory names)

        Example:
            >>> storage = DesignTokenStorage()
            >>> systems = storage.list_systems()
            >>> print(systems)
            ['material-design', 'figma-design']
        """
        if not self.output_dir.exists():
            return []

        return [d.name for d in self.output_dir.iterdir() if d.is_dir()]

    def delete(self, system_name: str) -> bool:
        """
        Delete a design system and all its files.

        Args:
            system_name: Name of the design system

        Returns:
            True if deleted, False if system not found

        Example:
            >>> storage = DesignTokenStorage()
            >>> deleted = storage.delete("Material Design")
            >>> print(deleted)
            True
        """
        system_name_normalized = self._normalize_name(system_name)
        system_dir = self.output_dir / system_name_normalized

        if not system_dir.exists():
            logger.warning(f"System directory not found: {system_dir}")
            return False

        try:
            import shutil

            shutil.rmtree(system_dir)
            logger.info(f"Deleted design system: {system_dir}")
            return True

        except Exception as e:
            logger.error(f"Error deleting system: {e}")
            return False

    def _save_metadata(self, system_dir: Path, system_name: str, metadata: dict) -> None:
        """
        Save metadata to metadata.json.

        Args:
            system_dir: System directory path
            system_name: Original system name
            metadata: Metadata dictionary
        """
        metadata_path = system_dir / "metadata.json"

        # Prepare metadata with schema
        full_metadata = {
            "name": system_name,
            "version": metadata.get("version", "1.0"),
            "source_url": metadata.get("url", ""),
            "fetched_at": metadata.get("fetched_at", datetime.utcnow().isoformat()),
            "content_hash": metadata.get("content_hash", ""),
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "system_name": metadata.get("system_name", system_name),
        }

        with open(metadata_path, "w") as f:
            json.dump(full_metadata, f, indent=2)

    def _save_tokens(self, system_dir: Path, tokens: dict) -> None:
        """
        Save tokens to tokens.json.

        Args:
            system_dir: System directory path
            tokens: Tokens dictionary (colors, typography, spacing, shadows)
        """
        tokens_path = system_dir / "tokens.json"

        # Prepare tokens with schema
        full_tokens = {
            "colors": tokens.get("colors", {}),
            "typography": tokens.get("typography", {}),
            "spacing": tokens.get("spacing", []),
            "shadows": tokens.get("shadows", []),
        }

        with open(tokens_path, "w") as f:
            json.dump(full_tokens, f, indent=2)

    def _save_content(self, system_dir: Path, content: str) -> None:
        """
        Save original markdown content.

        Args:
            system_dir: System directory path
            content: Markdown content
        """
        content_path = system_dir / "content.md"

        with open(content_path, "w") as f:
            f.write(content)

    def _load_metadata(self, system_dir: Path) -> dict:
        """
        Load metadata from metadata.json.

        Args:
            system_dir: System directory path

        Returns:
            Metadata dictionary
        """
        metadata_path = system_dir / "metadata.json"

        if not metadata_path.exists():
            return {}

        with open(metadata_path, "r") as f:
            return json.load(f)

    def _load_tokens(self, system_dir: Path) -> dict:
        """
        Load tokens from tokens.json.

        Args:
            system_dir: System directory path

        Returns:
            Tokens dictionary
        """
        tokens_path = system_dir / "tokens.json"

        if not tokens_path.exists():
            return {"colors": {}, "typography": {}, "spacing": [], "shadows": []}

        with open(tokens_path, "r") as f:
            return json.load(f)

    def _load_content(self, system_dir: Path) -> str:
        """
        Load original markdown content.

        Args:
            system_dir: System directory path

        Returns:
            Markdown content string
        """
        content_path = system_dir / "content.md"

        if not content_path.exists():
            return ""

        with open(content_path, "r") as f:
            return f.read()

    @staticmethod
    def _normalize_name(name: str) -> str:
        """
        Normalize system name for use as directory name.

        Converts to lowercase, replaces spaces with hyphens, removes invalid chars.

        Args:
            name: System name

        Returns:
            Normalized name suitable for use as directory name
        """
        import re

        # Convert to lowercase
        normalized = name.lower().strip()

        # Replace spaces and underscores with hyphens
        normalized = re.sub(r"[\s_]+", "-", normalized)

        # Remove invalid characters (keep alphanumeric, hyphens)
        normalized = re.sub(r"[^a-z0-9-]", "", normalized)

        # Remove multiple consecutive hyphens
        normalized = re.sub(r"-+", "-", normalized)

        # Remove leading/trailing hyphens
        normalized = normalized.strip("-")

        return normalized
