"""
CLI helper functions for Skill Builder.

Provides factory functions for creating manager instances used by the CLI.
"""

from pathlib import Path
from typing import Optional

from src.core.scope_manager import ScopeManager
from .builder import SkillBuilder
from .catalog import CatalogManager
from .templates import TemplateManager


def get_scope_manager() -> ScopeManager:
    """Get ScopeManager instance."""
    return ScopeManager()


def get_template_manager() -> TemplateManager:
    """Get TemplateManager instance."""
    return TemplateManager()


def get_catalog_manager(project_root: Optional[Path] = None) -> CatalogManager:
    """Get CatalogManager instance."""
    if project_root:
        catalog_path = project_root / "skills.json"
        return CatalogManager(catalog_path=catalog_path)
    return CatalogManager()


def get_builder(
    scope_manager: Optional[ScopeManager] = None,
    template_manager: Optional[TemplateManager] = None,
    catalog_manager: Optional[CatalogManager] = None,
) -> SkillBuilder:
    """Get SkillBuilder instance with dependencies."""
    scope_mgr = scope_manager or get_scope_manager()
    template_mgr = template_manager or get_template_manager()
    catalog_mgr = catalog_manager
    return SkillBuilder(
        scope_manager=scope_mgr,
        template_manager=template_mgr,
        catalog_manager=catalog_mgr,
    )
