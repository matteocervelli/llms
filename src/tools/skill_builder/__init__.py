"""
Claude Code Skill Builder Tool.

A tool for generating and managing Claude Code skills with YAML frontmatter,
interactive wizards, template management, and catalog tracking.
"""

from .exceptions import (
    CatalogCorruptedError,
    CatalogError,
    SkillBuilderError,
    SkillExistsError,
    SkillNotFoundError,
    SkillSecurityError,
    SkillValidationError,
    TemplateError,
    TemplateNotFoundError,
)
from .models import (
    ScopeType,
    SkillCatalog,
    SkillCatalogEntry,
    SkillConfig,
)

__version__ = "1.0.0"

__all__ = [
    # Models
    "SkillConfig",
    "SkillCatalogEntry",
    "SkillCatalog",
    "ScopeType",
    # Exceptions
    "SkillBuilderError",
    "SkillValidationError",
    "SkillExistsError",
    "SkillNotFoundError",
    "SkillSecurityError",
    "TemplateError",
    "TemplateNotFoundError",
    "CatalogError",
    "CatalogCorruptedError",
]
