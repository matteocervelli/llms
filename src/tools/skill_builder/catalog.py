"""
Catalog management for skill builder.

Manages skills.json catalog with atomic writes, search capabilities,
and proper CRUD operations for tracking created skills.
"""

import json
import os
import shutil
import tempfile
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from ..skill_builder.exceptions import (
    CatalogCorruptedError,
    CatalogError,
    SkillExistsError,
    SkillNotFoundError,
)
from ..skill_builder.models import SkillCatalog, SkillCatalogEntry, ScopeType
from ...core.scope_manager import ScopeManager


class CatalogManager:
    """Manages the skills.json catalog with atomic operations."""

    def __init__(self, catalog_path: Optional[Path] = None):
        """
        Initialize catalog manager.

        Args:
            catalog_path: Path to catalog file (default: ./skills.json)
        """
        if catalog_path is None:
            # Default to project root
            catalog_path = Path.cwd() / "skills.json"

        self.catalog_path = catalog_path.resolve()
        self._ensure_catalog()

    def _ensure_catalog(self) -> None:
        """Ensure catalog file exists, creating it if necessary."""
        if not self.catalog_path.exists():
            empty_catalog = SkillCatalog(schema_version="1.0", skills=[])
            self._write_catalog(empty_catalog)

    def _read_catalog(self) -> SkillCatalog:
        """
        Read catalog from file.

        Returns:
            SkillCatalog object

        Raises:
            CatalogCorruptedError: If catalog JSON is invalid
            CatalogError: If catalog cannot be read
        """
        try:
            with open(self.catalog_path, "r") as f:
                data = json.load(f)
            return SkillCatalog(**data)
        except FileNotFoundError:
            # Create empty catalog if not found
            empty_catalog = SkillCatalog(schema_version="1.0", skills=[])
            self._write_catalog(empty_catalog)
            return empty_catalog
        except json.JSONDecodeError as e:
            raise CatalogCorruptedError(f"Invalid JSON in catalog: {e}")
        except Exception as e:
            raise CatalogError(f"Failed to read catalog: {e}")

    def _write_catalog(self, catalog: SkillCatalog) -> None:
        """
        Write catalog to file with atomic operation.

        Uses temporary file + rename for atomicity to prevent corruption.

        Args:
            catalog: SkillCatalog to write

        Raises:
            CatalogError: If catalog cannot be written
        """
        backup_path = None
        try:
            # Create backup if catalog exists
            if self.catalog_path.exists():
                backup_path = self.catalog_path.with_suffix(".json.bak")
                shutil.copy2(self.catalog_path, backup_path)

            # Create parent directory if it doesn't exist
            self.catalog_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to temporary file first
            temp_fd, temp_path = tempfile.mkstemp(
                suffix=".json",
                dir=self.catalog_path.parent,
                text=True,
            )

            try:
                with os.fdopen(temp_fd, "w") as f:
                    # Use model_dump(mode='json') for Pydantic v2
                    catalog_dict = catalog.model_dump(mode="json")
                    json.dump(catalog_dict, f, indent=2)

                # Atomic rename
                Path(temp_path).replace(self.catalog_path)

                # Cleanup backup on success
                if backup_path and backup_path.exists():
                    backup_path.unlink()

            except Exception as e:
                # Cleanup temp file if it still exists
                temp_path_obj = Path(temp_path)
                if temp_path_obj.exists():
                    temp_path_obj.unlink()
                raise

        except Exception as e:
            # Restore from backup on failure
            if backup_path and backup_path.exists():
                if self.catalog_path.exists():
                    self.catalog_path.unlink()
                shutil.copy2(backup_path, self.catalog_path)
                backup_path.unlink()
            raise CatalogError(f"Failed to write catalog: {e}")

    def _parse_skill_frontmatter(self, skill_path: Path) -> Dict[str, Any]:
        """
        Parse YAML frontmatter from SKILL.md.

        Args:
            skill_path: Path to skill directory

        Returns:
            Dictionary of frontmatter data, empty dict if parsing fails
        """
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            return {}

        try:
            content = skill_file.read_text()

            # Extract frontmatter between --- delimiters
            if not content.startswith("---"):
                return {}

            parts = content.split("---", 2)
            if len(parts) < 3:
                return {}

            frontmatter_str = parts[1].strip()
            if not frontmatter_str:
                return {}

            return yaml.safe_load(frontmatter_str) or {}

        except (yaml.YAMLError, OSError):
            return {}

    def add_skill(self, entry: SkillCatalogEntry) -> None:
        """
        Add skill to catalog.

        Args:
            entry: SkillCatalogEntry to add

        Raises:
            SkillExistsError: If skill with same name and scope already exists
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        # Check for duplicate by name + scope
        existing = catalog.get_by_name(entry.name, entry.scope)
        if existing:
            raise SkillExistsError(
                f"Skill '{entry.name}' already exists in {entry.scope.value} scope"
            )

        # Add to catalog
        catalog.add_skill(entry)
        self._write_catalog(catalog)

    def update_skill(self, skill_id: UUID, **updates: Any) -> bool:
        """
        Update skill entry fields.

        Args:
            skill_id: UUID of skill to update
            **updates: Field names and values to update

        Returns:
            True if skill was found and updated, False otherwise

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        # Update using catalog method
        success = catalog.update_skill(skill_id, **updates)

        if success:
            self._write_catalog(catalog)

        return success

    def remove_skill(self, skill_id: UUID) -> bool:
        """
        Remove skill from catalog.

        Args:
            skill_id: UUID of skill to remove

        Returns:
            True if skill was found and removed, False otherwise

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        # Remove using catalog method
        success = catalog.remove_skill(skill_id)

        if success:
            self._write_catalog(catalog)

        return success

    def get_skill(
        self,
        name: Optional[str] = None,
        skill_id: Optional[UUID] = None,
        scope: Optional[ScopeType] = None,
    ) -> Optional[SkillCatalogEntry]:
        """
        Get skill by name or ID.

        Args:
            name: Skill name (requires scope if provided)
            skill_id: Skill UUID
            scope: Scope to search in (used with name)

        Returns:
            SkillCatalogEntry if found, None otherwise

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        if skill_id:
            return catalog.get_by_id(skill_id)
        elif name:
            return catalog.get_by_name(name, scope)

        return None

    def list_skills(
        self, scope: Optional[ScopeType] = None
    ) -> List[SkillCatalogEntry]:
        """
        List all skills, optionally filtered by scope.

        Args:
            scope: Optional scope to filter by

        Returns:
            List of SkillCatalogEntry objects

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        if scope:
            return catalog.filter_by_scope(scope)

        return catalog.skills

    def search_skills(
        self,
        query: Optional[str] = None,
        scope: Optional[ScopeType] = None,
        has_scripts: Optional[bool] = None,
        template: Optional[str] = None,
    ) -> List[SkillCatalogEntry]:
        """
        Search skills by various criteria.

        Args:
            query: Text query to search in name/description
            scope: Filter by scope
            has_scripts: Filter by presence of scripts directory
            template: Filter by template name

        Returns:
            List of matching SkillCatalogEntry objects

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        # Start with all skills or search results
        if query:
            results = catalog.search(query)
        else:
            results = catalog.skills

        # Apply filters
        if scope:
            results = [s for s in results if s.scope == scope]

        if has_scripts is not None:
            results = [
                s for s in results if s.metadata.get("has_scripts") == has_scripts
            ]

        if template:
            results = [s for s in results if s.metadata.get("template") == template]

        return results

    def get_catalog_stats(self) -> Dict[str, Any]:
        """
        Get catalog statistics.

        Returns:
            Dictionary with total count, by-scope breakdown, and feature stats

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        stats = {
            "total": len(catalog.skills),
            "by_scope": {
                "global": len(
                    [s for s in catalog.skills if s.scope == ScopeType.GLOBAL]
                ),
                "project": len(
                    [s for s in catalog.skills if s.scope == ScopeType.PROJECT]
                ),
                "local": len(
                    [s for s in catalog.skills if s.scope == ScopeType.LOCAL]
                ),
            },
            "by_template": {},
            "with_scripts": len(
                [s for s in catalog.skills if s.metadata.get("has_scripts")]
            ),
        }

        # Count by template
        for skill in catalog.skills:
            template = skill.metadata.get("template", "unknown")
            stats["by_template"][template] = stats["by_template"].get(template, 0) + 1

        return stats

    def sync_catalog(self, project_root: Optional[Path] = None) -> Dict[str, Any]:
        """
        Sync catalog with filesystem.

        Scans skills directories in global and project scopes, adds missing skills,
        and removes orphaned entries for skills that no longer exist.

        Args:
            project_root: Project root path (default: current directory)

        Returns:
            Report dictionary with 'added', 'removed', and 'errors' lists

        Raises:
            CatalogError: If catalog operation fails
        """
        if project_root is None:
            project_root = Path.cwd()

        catalog = self._read_catalog()
        report = {"added": [], "removed": [], "errors": []}

        # Initialize scope manager
        scope_manager = ScopeManager()

        # Define scopes to scan
        scopes_to_scan = [
            (ScopeType.GLOBAL, scope_manager.get_global_path() / "skills"),
            (ScopeType.PROJECT, project_root / ".claude" / "skills"),
        ]

        # Track found skills (name, scope) tuples
        found_skills = set()

        # Scan each scope
        for scope, skills_dir in scopes_to_scan:
            if not skills_dir.exists():
                continue

            # Iterate over skill directories
            for skill_dir in skills_dir.iterdir():
                if not skill_dir.is_dir():
                    continue

                # Check for SKILL.md
                skill_file = skill_dir / "SKILL.md"
                if not skill_file.exists():
                    continue

                try:
                    # Parse frontmatter
                    frontmatter = self._parse_skill_frontmatter(skill_dir)
                    skill_name = frontmatter.get("name", skill_dir.name)
                    description = frontmatter.get("description", "")

                    # Mark as found
                    found_skills.add((skill_name, scope))

                    # Check if already in catalog
                    existing = catalog.get_by_name(skill_name, scope)
                    if not existing:
                        # Create catalog entry
                        entry = SkillCatalogEntry(
                            id=uuid4(),
                            name=skill_name,
                            description=description,
                            scope=scope,
                            path=skill_dir,
                            metadata={
                                "template": frontmatter.get("template", "unknown"),
                                "has_scripts": (skill_dir / "scripts").exists(),
                                "file_count": len(list(skill_dir.iterdir())),
                                "allowed_tools": frontmatter.get("allowed-tools", []),
                            },
                        )

                        # Add to catalog
                        catalog.add_skill(entry)
                        report["added"].append(skill_name)

                except Exception as e:
                    report["errors"].append(f"Failed to process {skill_dir.name}: {e}")

        # Remove orphaned entries (skills in catalog but not on filesystem)
        for skill in list(catalog.skills):
            if not skill.path.exists() or (skill.name, skill.scope) not in found_skills:
                catalog.remove_skill(skill.id)
                report["removed"].append(skill.name)

        # Write updated catalog
        self._write_catalog(catalog)

        return report
