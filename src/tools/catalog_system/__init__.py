"""
Catalog Manifest System - Unified catalog for skills, commands, and agents.

This package provides a unified catalog system to track available skills, commands,
and agents across global, project, and local scopes. It supports auto-discovery,
search/filter capabilities, and CLI commands for element management.

Main Components:
- CatalogManager: Main facade coordinating all catalog operations
- Scanner: Auto-discovers elements by scanning filesystem
- Searcher: Provides search and filter with scoring algorithm
- Syncer: Synchronizes catalogs with filesystem (auto-sync with caching)

Usage:
    from catalog_system import CatalogManager

    manager = CatalogManager()
    skills = manager.list("skills")
    results = manager.search("test", element_type="skills")
"""

from .exceptions import (
    CatalogError,
    CatalogNotFoundError,
    CatalogValidationError,
    ScanError,
    SyncError,
)
from .models import (
    AgentCatalogEntry,
    CatalogEntry,
    CommandCatalogEntry,
    SkillCatalogEntry,
)

__all__ = [
    # Exceptions
    "CatalogError",
    "CatalogNotFoundError",
    "CatalogValidationError",
    "ScanError",
    "SyncError",
    # Models
    "CatalogEntry",
    "SkillCatalogEntry",
    "CommandCatalogEntry",
    "AgentCatalogEntry",
]

__version__ = "0.1.0"
