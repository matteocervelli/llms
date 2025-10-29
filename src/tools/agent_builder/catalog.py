"""
Catalog management for agent builder.

Manages agents.json catalog with atomic writes, search capabilities,
and proper CRUD operations for tracking created agents.

This module provides persistent catalog management for agent metadata,
including creation tracking, search, and sync operations with filesystem.

Key differences from skill_builder:
- Agents are single .md files (not directories)
- Catalog file: agents.json (not skills.json)
- No scripts directory tracking (agents don't have scripts)
- Model field tracking (agents specify Claude model)

Performance Target:
- All operations < 100ms
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

from src.tools.agent_builder.exceptions import (
    CatalogCorruptedError,
    CatalogError,
    AgentExistsError,
    AgentNotFoundError,
)
from src.tools.agent_builder.models import AgentCatalog, AgentCatalogEntry, ScopeType, ModelType
from src.core.scope_manager import ScopeManager


class CatalogManager:
    """Manages the agents.json catalog with atomic operations."""

    def __init__(self, catalog_path: Optional[Path] = None):
        """
        Initialize catalog manager.

        Args:
            catalog_path: Path to catalog file (default: ./agents.json)

        Examples:
            >>> manager = CatalogManager()  # Uses cwd/agents.json
            >>> manager = CatalogManager(Path("/path/to/agents.json"))
        """
        if catalog_path is None:
            # Default to project root
            catalog_path = Path.cwd() / "agents.json"

        self.catalog_path = catalog_path.resolve()
        self._ensure_catalog()

    def _ensure_catalog(self) -> None:
        """Ensure catalog file exists, creating it if necessary."""
        if not self.catalog_path.exists():
            empty_catalog = AgentCatalog(schema_version="1.0", agents=[])
            self._write_catalog(empty_catalog)

    def _read_catalog(self) -> AgentCatalog:
        """
        Read catalog from file.

        Returns:
            AgentCatalog object

        Raises:
            CatalogCorruptedError: If catalog JSON is invalid
            CatalogError: If catalog cannot be read
        """
        try:
            with open(self.catalog_path, "r") as f:
                data = json.load(f)
            return AgentCatalog(**data)
        except FileNotFoundError:
            # Create empty catalog if not found
            empty_catalog = AgentCatalog(schema_version="1.0", agents=[])
            self._write_catalog(empty_catalog)
            return empty_catalog
        except json.JSONDecodeError as e:
            raise CatalogCorruptedError(f"Invalid JSON in catalog: {e}")
        except Exception as e:
            raise CatalogError(f"Failed to read catalog: {e}")

    def _write_catalog(self, catalog: AgentCatalog) -> None:
        """
        Write catalog to file with atomic operation.

        Uses temporary file + rename for atomicity to prevent corruption.

        Args:
            catalog: AgentCatalog to write

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

    def _parse_agent_frontmatter(self, agent_path: Path) -> Dict[str, Any]:
        """
        Parse YAML frontmatter from agent .md file.

        Args:
            agent_path: Path to agent markdown file

        Returns:
            Dictionary of frontmatter data, empty dict if parsing fails
        """
        if not agent_path.exists() or not agent_path.suffix == ".md":
            return {}

        try:
            content = agent_path.read_text()

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

    def add_agent(self, entry: AgentCatalogEntry) -> None:
        """
        Add agent to catalog.

        Args:
            entry: AgentCatalogEntry to add

        Raises:
            AgentExistsError: If agent with same name and scope already exists
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        # Check for duplicate by name + scope
        existing = catalog.get_by_name(entry.name, entry.scope)
        if existing:
            raise AgentExistsError(
                f"Agent '{entry.name}' already exists in {entry.scope.value} scope"
            )

        # Add to catalog
        catalog.add_agent(entry)
        self._write_catalog(catalog)

    def update_agent(self, agent_id: UUID, **updates: Any) -> bool:
        """
        Update agent entry fields.

        Args:
            agent_id: UUID of agent to update
            **updates: Field names and values to update

        Returns:
            True if agent was found and updated, False otherwise

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        # Update using catalog method
        success = catalog.update_agent(agent_id, **updates)

        if success:
            self._write_catalog(catalog)

        return success

    def remove_agent(self, agent_id: UUID) -> bool:
        """
        Remove agent from catalog.

        Args:
            agent_id: UUID of agent to remove

        Returns:
            True if agent was found and removed, False otherwise

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        # Remove using catalog method
        success = catalog.remove_agent(agent_id)

        if success:
            self._write_catalog(catalog)

        return success

    def get_agent(
        self,
        name: Optional[str] = None,
        agent_id: Optional[UUID] = None,
        scope: Optional[ScopeType] = None,
    ) -> Optional[AgentCatalogEntry]:
        """
        Get agent by name or ID.

        Args:
            name: Agent name (requires scope if provided)
            agent_id: Agent UUID
            scope: Scope to search in (used with name)

        Returns:
            AgentCatalogEntry if found, None otherwise

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        if agent_id:
            return catalog.get_by_id(agent_id)
        elif name:
            return catalog.get_by_name(name, scope)

        return None

    def list_agents(self, scope: Optional[ScopeType] = None) -> List[AgentCatalogEntry]:
        """
        List all agents, optionally filtered by scope.

        Args:
            scope: Optional scope to filter by

        Returns:
            List of AgentCatalogEntry objects

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        if scope:
            return catalog.filter_by_scope(scope)

        return catalog.agents

    def search_agents(
        self,
        query: Optional[str] = None,
        scope: Optional[ScopeType] = None,
        model: Optional[ModelType] = None,
        template: Optional[str] = None,
    ) -> List[AgentCatalogEntry]:
        """
        Search agents by various criteria.

        Args:
            query: Text query to search in name/description
            scope: Filter by scope
            model: Filter by Claude model
            template: Filter by template name

        Returns:
            List of matching AgentCatalogEntry objects

        Raises:
            CatalogError: If catalog operation fails
        """
        catalog = self._read_catalog()

        # Start with all agents or search results
        if query:
            results = catalog.search(query)
        else:
            results = catalog.agents

        # Apply filters
        if scope:
            results = [a for a in results if a.scope == scope]

        if model:
            results = [a for a in results if a.model == model]

        if template:
            results = [a for a in results if a.metadata.get("template") == template]

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
            "total": len(catalog.agents),
            "by_scope": {
                "global": len([a for a in catalog.agents if a.scope == ScopeType.GLOBAL]),
                "project": len([a for a in catalog.agents if a.scope == ScopeType.PROJECT]),
                "local": len([a for a in catalog.agents if a.scope == ScopeType.LOCAL]),
            },
            "by_model": {},
            "by_template": {},
        }

        # Count by model
        for agent in catalog.agents:
            model = agent.model.value if agent.model else "unknown"
            stats["by_model"][model] = stats["by_model"].get(model, 0) + 1

        # Count by template
        for agent in catalog.agents:
            template = agent.metadata.get("template", "unknown")
            stats["by_template"][template] = stats["by_template"].get(template, 0) + 1

        return stats

    def sync_catalog(self, project_root: Optional[Path] = None) -> Dict[str, Any]:
        """
        Sync catalog with filesystem.

        Scans agents directories in global and project scopes, adds missing agents,
        and removes orphaned entries for agents that no longer exist.

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
        report: dict[str, list[str]] = {"added": [], "removed": [], "errors": []}

        # Initialize scope manager
        scope_manager = ScopeManager()

        # Define scopes to scan
        scopes_to_scan = [
            (ScopeType.GLOBAL, scope_manager.get_global_path() / "agents"),
            (ScopeType.PROJECT, project_root / ".claude" / "agents"),
        ]

        # Track found agents (name, scope) tuples
        found_agents = set()

        # Scan each scope
        for scope, agents_dir in scopes_to_scan:
            if not agents_dir.exists():
                continue

            # Iterate over agent .md files
            for agent_file in agents_dir.glob("*.md"):
                if not agent_file.is_file():
                    continue

                try:
                    # Parse frontmatter
                    frontmatter = self._parse_agent_frontmatter(agent_file)
                    agent_name = frontmatter.get("name", agent_file.stem)
                    description = frontmatter.get("description", "")
                    model_str = frontmatter.get("model", ModelType.SONNET.value)

                    # Parse model
                    try:
                        model = ModelType(model_str)
                    except ValueError:
                        model = ModelType.SONNET  # Default fallback

                    # Mark as found
                    found_agents.add((agent_name, scope))

                    # Check if already in catalog
                    existing = catalog.get_by_name(agent_name, scope)
                    if not existing:
                        # Create catalog entry
                        entry = AgentCatalogEntry(
                            id=uuid4(),
                            name=agent_name,
                            description=description,
                            scope=scope,
                            model=model,
                            path=agent_file,
                            metadata={
                                "template": frontmatter.get("template", "unknown"),
                            },
                        )

                        # Add to catalog
                        catalog.add_agent(entry)
                        report["added"].append(agent_name)

                except Exception as e:
                    report["errors"].append(f"Failed to process {agent_file.name}: {e}")

        # Remove orphaned entries (agents in catalog but not on filesystem)
        for agent in list(catalog.agents):
            if not agent.path.exists() or (agent.name, agent.scope) not in found_agents:
                catalog.remove_agent(agent.id)
                report["removed"].append(agent.name)

        # Write updated catalog
        self._write_catalog(catalog)

        return report
