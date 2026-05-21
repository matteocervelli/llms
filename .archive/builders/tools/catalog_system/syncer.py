"""
Syncer component for catalog system.

Synchronizes catalog files with discovered entries from filesystem.
Uses atomic write pattern for data safety.
"""

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .models import (
    CatalogEntry,
    SkillCatalogEntry,
    CommandCatalogEntry,
    AgentCatalogEntry,
)
from .exceptions import SyncError


class Syncer:
    """
    Synchronizes catalog with filesystem discoveries.

    The Syncer merges discovered entries with existing catalog entries:
    - Adds new entries from discoveries
    - Updates existing entries if they changed
    - Removes orphaned entries (optional)
    - Uses atomic write pattern for safety
    """

    def __init__(self) -> None:
        """Initialize the Syncer."""
        pass

    def sync(
        self,
        catalog_path: Path,
        discovered_entries: List[CatalogEntry],
    ) -> List[CatalogEntry]:
        """
        Synchronize catalog with discovered entries.

        Merges discovered entries with existing catalog entries.
        Filesystem is source of truth - discovered entries override catalog.

        Args:
            catalog_path: Path to catalog JSON file
            discovered_entries: Entries discovered from filesystem

        Returns:
            List of all catalog entries after sync

        Raises:
            SyncError: If sync operation fails

        Example:
            >>> syncer = Syncer()
            >>> from scanner import Scanner
            >>> scanner = Scanner()
            >>> discovered = scanner.scan_skills(
            ...     [Path("~/.claude").expanduser()]
            ... )
            >>> result = syncer.sync(Path("skills.json"), discovered)
        """
        try:
            # Read existing catalog
            existing_entries = self._read_catalog(catalog_path)

            # Merge discovered with existing
            merged_entries = self._merge_entries(existing_entries, discovered_entries)

            # Write updated catalog atomically
            self._write_catalog(catalog_path, merged_entries)

            return merged_entries

        except Exception as e:
            raise SyncError(f"Failed to sync catalog: {e}")

    def _read_catalog(self, catalog_path: Path) -> List[CatalogEntry]:
        """
        Read existing catalog from file.

        Args:
            catalog_path: Path to catalog JSON file

        Returns:
            List of catalog entries

        Raises:
            SyncError: If catalog cannot be read or is corrupted
        """
        if not catalog_path.exists():
            return []

        try:
            data = json.loads(catalog_path.read_text())

            entries = []
            for entry_data in data.get("entries", []):
                # Reconstruct appropriate entry type
                entry = self._deserialize_entry(entry_data)
                if entry:
                    entries.append(entry)

            return entries

        except json.JSONDecodeError as e:
            raise SyncError(f"Catalog file corrupted: {e}")
        except Exception as e:
            raise SyncError(f"Failed to read catalog: {e}")

    def _write_catalog(
        self,
        catalog_path: Path,
        entries: List[CatalogEntry],
    ) -> None:
        """
        Write catalog to file using atomic write pattern.

        Uses temp file + rename for atomicity to prevent corruption.

        Args:
            catalog_path: Path to catalog JSON file
            entries: Catalog entries to write

        Raises:
            SyncError: If write fails
        """
        backup_path = None

        try:
            # Create parent directory if needed
            catalog_path.parent.mkdir(parents=True, exist_ok=True)

            # Create backup if catalog exists
            if catalog_path.exists():
                backup_path = catalog_path.with_suffix(".json.bak")
                shutil.copy2(catalog_path, backup_path)

            # Serialize entries
            entries_data = [entry.model_dump(mode="json") for entry in entries]

            catalog_data = {
                "schema_version": "1.0",
                "entries": entries_data,
                "last_sync": datetime.now().isoformat(),
            }

            # Write to temp file first
            temp_fd, temp_path = tempfile.mkstemp(
                suffix=".json",
                dir=catalog_path.parent,
                text=True,
            )

            try:
                with os.fdopen(temp_fd, "w") as f:
                    json.dump(catalog_data, f, indent=2)

                # Atomic rename
                Path(temp_path).replace(catalog_path)

                # Cleanup backup on success
                if backup_path and backup_path.exists():
                    backup_path.unlink()

            except Exception:
                # Cleanup temp file if it still exists
                temp_path_obj = Path(temp_path)
                if temp_path_obj.exists():
                    temp_path_obj.unlink()
                raise

        except Exception as e:
            # Restore from backup on failure
            if backup_path and backup_path.exists():
                if catalog_path.exists():
                    catalog_path.unlink()
                shutil.copy2(backup_path, catalog_path)
                backup_path.unlink()
            raise SyncError(f"Failed to write catalog: {e}")

    def _merge_entries(
        self,
        existing: List[CatalogEntry],
        discovered: List[CatalogEntry],
    ) -> List[CatalogEntry]:
        """
        Merge discovered entries with existing catalog entries.

        Filesystem (discovered) is source of truth:
        - Keep all discovered entries (they exist on filesystem)
        - Update existing entries with discovered data
        - Remove entries not in discovered (optional - kept for now)

        Args:
            existing: Existing catalog entries
            discovered: Newly discovered entries from filesystem

        Returns:
            Merged list of catalog entries
        """
        # Create lookup of existing entries by (name, scope)
        existing_map: Dict[tuple, CatalogEntry] = {(e.name, e.scope): e for e in existing}

        merged = []

        # Process discovered entries
        for disc_entry in discovered:
            key = (disc_entry.name, disc_entry.scope)

            if key in existing_map:
                # Entry exists - preserve ID and created_at
                existing_entry = existing_map[key]
                disc_entry.id = existing_entry.id
                disc_entry.created_at = existing_entry.created_at
                # updated_at will be set by model

            merged.append(disc_entry)

        # Optionally keep existing entries not in discovered
        # (they might be on filesystem but not scanned yet)
        # For now, we only keep discovered entries

        return merged

    def _deserialize_entry(self, data: Dict[str, Any]) -> CatalogEntry | None:
        """
        Deserialize catalog entry from dict.

        Determines entry type and creates appropriate model instance.

        Args:
            data: Entry data dictionary

        Returns:
            CatalogEntry instance or None if deserialization fails
        """
        try:
            # Determine type by checking for type-specific fields
            if "template" in data:
                return SkillCatalogEntry(**data)
            elif "model" in data:
                return AgentCatalogEntry(**data)
            elif "aliases" in data or "tags" in data:
                return CommandCatalogEntry(**data)
            else:
                # Default to base CatalogEntry (shouldn't happen)
                return None

        except Exception:
            # Skip entries that can't be deserialized
            return None
