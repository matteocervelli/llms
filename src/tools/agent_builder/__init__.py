"""
Claude Code Agent Builder Tool.

A tool for generating and managing Claude Code agents with model selection,
interactive wizards, template management, and catalog tracking.
"""

from .builder import AgentBuilder
from .catalog import CatalogManager
from .exceptions import (
    AgentBuilderError,
    AgentExistsError,
    AgentNotFoundError,
    AgentSecurityError,
    AgentValidationError,
    CatalogCorruptedError,
    CatalogError,
    TemplateError,
    TemplateNotFoundError,
)
from .models import (
    AgentCatalog,
    AgentCatalogEntry,
    AgentConfig,
    ModelType,
    ScopeType,
)
from .templates import TemplateManager
from .validator import AgentValidator

__version__ = "1.0.0"

__all__ = [
    # Core classes
    "AgentBuilder",
    "CatalogManager",
    "TemplateManager",
    "AgentValidator",
    # Models
    "AgentConfig",
    "AgentCatalogEntry",
    "AgentCatalog",
    "ScopeType",
    "ModelType",
    # Exceptions
    "AgentBuilderError",
    "AgentValidationError",
    "AgentExistsError",
    "AgentNotFoundError",
    "AgentSecurityError",
    "TemplateError",
    "TemplateNotFoundError",
    "CatalogError",
    "CatalogCorruptedError",
]
