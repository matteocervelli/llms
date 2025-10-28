"""
Catalog management for command builder.

Manages commands.json catalog with atomic writes, search capabilities,
and proper CRUD operations for tracking created commands.
"""

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4
from datetime import datetime

from .exceptions import CatalogError
from .models import CommandCatalog, CommandCatalogEntry, ScopeType


class CatalogManager:
    """Manages the commands.json catalog with atomic operations."""

    def __init__(self, catalog_path: Optional[Path] = None):
        """
        Initialize catalog manager.

        Args:
            catalog_path: Path to catalog file (default: ./commands.json)
        """
        if catalog_path is None:
            # Default to project root
            catalog_path = Path.cwd() / "commands.json"

        self.catalog_path = catalog_path
        self._ensure_catalog()

    def _ensure_catalog(self) -> None:
        """Ensure catalog file exists, creating it if necessary."""
        if not self.catalog_path.exists():
            empty_catalog = CommandCatalog()
            self._write_catalog(empty_catalog)

    def _read_catalog(self) -> CommandCatalog:
        """
        Read catalog from file.

        Returns:
            CommandCatalog object

        Raises:
            CatalogError: If catalog cannot be read
        """
        try:
            with open(self.catalog_path, "r") as f:
                data = json.load(f)
            return CommandCatalog(**data)
        except FileNotFoundError:
            # Create empty catalog if not found
            empty_catalog = CommandCatalog()
            self._write_catalog(empty_catalog)
            return empty_catalog
        except json.JSONDecodeError as e:
            raise CatalogError(f"Invalid JSON in catalog: {e}")
        except Exception as e:
            raise CatalogError(f"Failed to read catalog: {e}")

    def _write_catalog(self, catalog: CommandCatalog) -> None:
        """
        Write catalog to file with atomic operation.

        Uses temporary file + rename for atomicity to prevent corruption.

        Args:
            catalog: CommandCatalog to write

        Raises:
            CatalogError: If catalog cannot be written
        """
        try:
            # Create backup if catalog exists
            if self.catalog_path.exists():
                backup_path = self.catalog_path.with_suffix(".json.bak")
                shutil.copy2(self.catalog_path, backup_path)

            # Write to temporary file first
            temp_fd, temp_path = tempfile.mkstemp(
                suffix=".json",
                dir=self.catalog_path.parent,
                text=True,
            )

            try:
                with open(temp_fd, "w") as f:
                    json.dump(
                        catalog.model_dump(),
                        f,
                        indent=2,
                        default=str,
                    )

                # Atomic rename
                Path(temp_path).replace(self.catalog_path)

            except Exception as e:
                # Clean up temp file on error
                Path(temp_path).unlink(missing_ok=True)
                raise e

        except Exception as e:
            raise CatalogError(f"Failed to write catalog: {e}")

    def add_command(self, entry: CommandCatalogEntry) -> None:
        """
        Add a command to the catalog.

        Args:
            entry: Command catalog entry

        Raises:
            CatalogError: If command cannot be added
        """
        catalog = self._read_catalog()

        # Check if command with same name and scope already exists
        existing = catalog.get_by_name(entry.name, entry.scope)
        if existing:
            raise CatalogError(
                f"Command '{entry.name}' already exists in {entry.scope.value} scope"
            )

        catalog.add_command(entry)
        self._write_catalog(catalog)

    def update_command(self, entry: CommandCatalogEntry) -> None:
        """
        Update an existing command in the catalog.

        Args:
            entry: Command catalog entry with updated information

        Raises:
            CatalogError: If command cannot be updated
        """
        catalog = self._read_catalog()

        # Find existing entry
        existing = catalog.get_by_id(entry.id)
        if not existing:
            raise CatalogError(f"Command with ID {entry.id} not found in catalog")

        # Remove old entry and add updated one
        catalog.remove_command(entry.id)
        entry.update_timestamp()
        catalog.add_command(entry)
        self._write_catalog(catalog)

    def remove_command(self, cmd_id: UUID) -> bool:
        """
        Remove a command from the catalog.

        Args:
            cmd_id: Command UUID

        Returns:
            True if removed, False if not found

        Raises:
            CatalogError: If removal fails
        """
        catalog = self._read_catalog()

        if catalog.remove_command(cmd_id):
            self._write_catalog(catalog)
            return True

        return False

    def get_command(
        self,
        name: Optional[str] = None,
        cmd_id: Optional[UUID] = None,
        scope: Optional[ScopeType] = None,
    ) -> Optional[CommandCatalogEntry]:
        """
        Get a command by name or ID.

        Args:
            name: Command name
            cmd_id: Command UUID
            scope: Optional scope filter (only used with name)

        Returns:
            Command catalog entry or None

        Raises:
            CatalogError: If catalog cannot be read
        """
        catalog = self._read_catalog()

        if cmd_id:
            return catalog.get_by_id(cmd_id)
        elif name:
            return catalog.get_by_name(name, scope)
        else:
            return None

    def list_commands(
        self,
        scope: Optional[ScopeType] = None,
    ) -> List[CommandCatalogEntry]:
        """
        List all commands, optionally filtered by scope.

        Args:
            scope: Optional scope filter

        Returns:
            List of command catalog entries

        Raises:
            CatalogError: If catalog cannot be read
        """
        catalog = self._read_catalog()

        if scope:
            return [cmd for cmd in catalog.commands if cmd.scope == scope]

        return catalog.commands

    def search_commands(
        self,
        query: Optional[str] = None,
        scope: Optional[ScopeType] = None,
        has_parameters: Optional[bool] = None,
        has_bash: Optional[bool] = None,
    ) -> List[CommandCatalogEntry]:
        """
        Search commands by various criteria.

        Args:
            query: Text query (searches name and description)
            scope: Filter by scope
            has_parameters: Filter by parameter presence
            has_bash: Filter by bash command presence

        Returns:
            List of matching command catalog entries

        Raises:
            CatalogError: If catalog cannot be read
        """
        catalog = self._read_catalog()
        return catalog.search(
            query=query,
            scope=scope,
            has_parameters=has_parameters,
            has_bash=has_bash,
        )

    def get_catalog_stats(self) -> dict:
        """
        Get statistics about the catalog.

        Returns:
            Dictionary with catalog statistics

        Raises:
            CatalogError: If catalog cannot be read
        """
        catalog = self._read_catalog()

        stats = {
            "total_commands": len(catalog.commands),
            "by_scope": {
                "global": len([c for c in catalog.commands if c.scope == ScopeType.GLOBAL]),
                "project": len([c for c in catalog.commands if c.scope == ScopeType.PROJECT]),
                "local": len([c for c in catalog.commands if c.scope == ScopeType.LOCAL]),
            },
            "with_parameters": len(
                [c for c in catalog.commands if c.metadata.get("has_parameters", False)]
            ),
            "with_bash": len([c for c in catalog.commands if c.metadata.get("has_bash", False)]),
            "with_files": len([c for c in catalog.commands if c.metadata.get("has_files", False)]),
        }

        return stats

    def sync_catalog(self, project_root: Optional[Path] = None) -> Dict[str, Any]:
        """
        Sync catalog with actual command files.

        Scans command directories and syncs catalog:
        - Removes entries for missing files
        - Adds entries for untracked files

        Args:
            project_root: Project root path (default: current directory)

        Returns:
            Dictionary with sync results:
            {
                "removed": List of removed command names,
                "added": List of added command names,
                "unchanged": Count of unchanged commands
            }

        Raises:
            CatalogError: If catalog operations fail
        """
        if project_root is None:
            project_root = Path.cwd()

        catalog = self._read_catalog()

        # Collect all command files from all scopes
        command_files = {}  # path -> file info

        # Global scope
        global_dir = Path.home() / ".claude" / "commands"
        if global_dir.exists():
            for file_path in global_dir.glob("*.md"):
                command_files[str(file_path.resolve())] = {
                    "path": file_path,
                    "scope": ScopeType.GLOBAL,
                }

        # Project scope
        project_dir = project_root / ".claude" / "commands"
        if project_dir.exists():
            for file_path in project_dir.glob("*.md"):
                command_files[str(file_path.resolve())] = {
                    "path": file_path,
                    "scope": ScopeType.PROJECT,
                }

        # Track changes
        removed = []
        added = []
        unchanged = 0

        # Remove catalog entries for missing files
        updated_commands = []
        for entry in catalog.commands:
            if entry.path in command_files:
                updated_commands.append(entry)
                # Mark as found
                command_files[entry.path]["found"] = True
                unchanged += 1
            else:
                removed.append(entry.name)

        # Add catalog entries for untracked files
        for file_info in command_files.values():
            if file_info.get("found"):
                continue  # Already in catalog

            # Read file to get description
            file_path = Path(file_info["path"])  # type: ignore[arg-type]
            try:
                content = file_path.read_text(encoding="utf-8")

                # Extract description from frontmatter
                description = ""
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        # Parse YAML frontmatter (simple extraction)
                        for line in parts[1].split("\n"):
                            if line.startswith("description:"):
                                description = line.split(":", 1)[1].strip()
                                break

                if not description:
                    description = f"Command from {file_path.name}"

                # Create catalog entry
                name = file_path.stem
                entry = CommandCatalogEntry(
                    id=uuid4(),
                    name=name,
                    description=description,
                    scope=ScopeType(file_info["scope"]),  # type: ignore[arg-type]
                    path=str(file_path.resolve()),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    metadata={
                        "template": "unknown",
                        "has_parameters": False,
                        "has_bash": "!" in content,
                        "has_files": "@" in content,
                        "thinking_mode": "thinking: true" in content,
                        "synced": True,
                    },
                )
                updated_commands.append(entry)
                added.append(name)

            except Exception as e:
                # Skip files that can't be read
                continue

        # Update catalog
        catalog.commands = updated_commands
        self._write_catalog(catalog)

        return {
            "removed": removed,
            "added": added,
            "unchanged": unchanged,
        }
