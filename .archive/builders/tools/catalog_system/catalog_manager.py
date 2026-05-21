"""
CatalogManager - Main facade for catalog operations.

Coordinates Scanner, Searcher, and Syncer components to provide
a unified API for catalog management.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any, cast

from .scanner import Scanner
from .searcher import Searcher
from .syncer import Syncer
from .models import (
    CatalogEntry,
    SkillCatalogEntry,
    CommandCatalogEntry,
    AgentCatalogEntry,
)
from src.core.scope_manager import ScopeManager


class CatalogManager:
    """
    Main facade for catalog system operations.

    Provides high-level API for:
    - Listing elements
    - Searching elements
    - Showing element details
    - Syncing catalogs
    - Getting statistics
    """

    def __init__(self, manifests_dir: Optional[Path] = None):
        """
        Initialize CatalogManager.

        Args:
            manifests_dir: Directory containing manifest JSON files
                          (default: project_root/manifests/)
        """
        self.scanner = Scanner()
        self.searcher = Searcher()
        self.syncer = Syncer()
        self.scope_manager = ScopeManager()

        if manifests_dir is None:
            # Default to project root/manifests
            manifests_dir = Path.cwd() / "manifests"

        self.manifests_dir = manifests_dir
        self.manifests_dir.mkdir(parents=True, exist_ok=True)

    def list(
        self,
        element_type: str,
        scope: str = "all",
        auto_sync: bool = True,
    ) -> List[CatalogEntry]:
        """
        List catalog entries with optional auto-sync.

        Args:
            element_type: Type of element
                         ("skills", "commands", "agents", or "all")
            scope: Scope filter
                  ("global", "project", "local", or "all")
            auto_sync: Whether to auto-sync before listing (default: True)

        Returns:
            List of catalog entries

        Example:
            >>> manager = CatalogManager()
            >>> skills = manager.list("skills", scope="global")
        """
        if auto_sync:
            self.sync(element_type)

        # Load from catalog
        entries = self._load_catalog(element_type)

        # Filter by scope
        if scope != "all":
            entries = self.searcher.filter_by_scope(entries, scope)

        return entries

    def search(
        self,
        query: str,
        element_type: str = "all",
        scope: str = "all",
    ) -> List[CatalogEntry]:
        """
        Search catalog entries.

        Args:
            query: Search query string
            element_type: Type filter
                         ("skills", "commands", "agents", or "all")
            scope: Scope filter
                  ("global", "project", "local", or "all")

        Returns:
            List of matching catalog entries sorted by relevance

        Example:
            >>> manager = CatalogManager()
            >>> results = manager.search("python")
        """
        # Load catalogs
        entries = self._load_catalog(element_type)

        # Search
        search_results = self.searcher.search(entries, query)
        entries = [entry for entry, _ in search_results]

        # Filter by scope
        if scope != "all":
            entries = self.searcher.filter_by_scope(entries, scope)

        return entries

    def show(
        self,
        element_type: str,
        name: str,
        scope: Optional[str] = None,
    ) -> Optional[CatalogEntry]:
        """
        Show details for a specific element.

        Args:
            element_type: Type of element ("skill", "command", or "agent")
            name: Name of the element
            scope: Optional scope filter

        Returns:
            Catalog entry if found, None otherwise

        Example:
            >>> manager = CatalogManager()
            >>> skill = manager.show("skill", "python-tester")
        """
        entries = self._load_catalog(self._pluralize_type(element_type))

        # Find matching entry
        for entry in entries:
            if entry.name == name:
                if scope is None or entry.scope == scope:
                    return entry

        return None

    def sync(self, element_type: str = "all") -> None:
        """
        Synchronize catalogs with filesystem.

        Args:
            element_type: Type to sync
                         ("skills", "commands", "agents", or "all")

        Example:
            >>> manager = CatalogManager()
            >>> manager.sync("all")
        """
        types_to_sync = (
            ["skills", "commands", "agents"] if element_type == "all" else [element_type]
        )

        for etype in types_to_sync:
            # Get scope paths
            scope_paths = self._get_scope_paths()

            # Scan filesystem and sync
            catalog_path = self.manifests_dir / f"{etype}.json"
            discovered_entries: List[CatalogEntry]
            if etype == "skills":
                discovered_entries = cast(List[CatalogEntry], self.scanner.scan_skills(scope_paths))
            elif etype == "commands":
                discovered_entries = cast(
                    List[CatalogEntry], self.scanner.scan_commands(scope_paths)
                )
            elif etype == "agents":
                discovered_entries = cast(List[CatalogEntry], self.scanner.scan_agents(scope_paths))
            else:
                continue
            self.syncer.sync(catalog_path, discovered_entries)

    def get_stats(self) -> Dict[str, Any]:
        """
        Get catalog statistics.

        Returns:
            Dictionary with statistics for all catalogs

        Example:
            >>> manager = CatalogManager()
            >>> stats = manager.get_stats()
            >>> print(stats["total"])
        """
        by_type: Dict[str, int] = {}
        by_scope: Dict[str, int] = {
            "global": 0,
            "project": 0,
            "local": 0,
        }
        total = 0

        for element_type in ["skills", "commands", "agents"]:
            entries = self._load_catalog(element_type)
            count = len(entries)

            total += count
            by_type[element_type] = count

            for entry in entries:
                by_scope[entry.scope] = by_scope.get(entry.scope, 0) + 1

        return {
            "total": total,
            "by_type": by_type,
            "by_scope": by_scope,
        }

    def _load_catalog(self, element_type: str) -> List[CatalogEntry]:
        """
        Load entries from catalog file(s).

        Args:
            element_type: Type to load
                         ("skills", "commands", "agents", or "all")

        Returns:
            List of catalog entries
        """
        entries: List[CatalogEntry] = []

        types_to_load = (
            ["skills", "commands", "agents"] if element_type == "all" else [element_type]
        )

        for etype in types_to_load:
            catalog_path = self.manifests_dir / f"{etype}.json"
            if not catalog_path.exists():
                continue

            try:
                import json

                data = json.loads(catalog_path.read_text())

                for entry_data in data.get("entries", []):
                    # Deserialize based on type
                    entry: CatalogEntry
                    if etype == "skills":
                        entry = SkillCatalogEntry(**entry_data)
                    elif etype == "commands":
                        entry = CommandCatalogEntry(**entry_data)
                    elif etype == "agents":
                        entry = AgentCatalogEntry(**entry_data)
                    else:
                        continue

                    entries.append(entry)

            except Exception:
                # Skip corrupted catalogs
                continue

        return entries

    def _get_scope_paths(self) -> List[Path]:
        """Get paths to scan for all scopes."""
        paths = []

        # Global scope
        global_path = self.scope_manager.get_global_path()
        if global_path.exists():
            paths.append(global_path)

        # Project scope
        project_path = self.scope_manager.get_project_path()
        if project_path:
            paths.append(project_path)

        return paths

    def _pluralize_type(self, element_type: str) -> str:
        """Convert singular type to plural."""
        mapping = {
            "skill": "skills",
            "command": "commands",
            "agent": "agents",
        }
        return mapping.get(element_type, element_type)
