"""
Command Builder Tool for Claude Code.

Generates Claude Code slash command .md files with YAML frontmatter, parameter configuration,
bash command integration, file references, and interactive CLI wizard.

Example:
    >>> from command_builder import CommandConfig, CommandBuilder
    >>> config = CommandConfig(name="my-command", description="My custom command")
    >>> builder = CommandBuilder()
    >>> path, content = builder.build_command(config)
"""

from .builder import CommandBuilder
from .catalog import CatalogManager
from .exceptions import (
    CatalogError,
    CommandBuilderError,
    CommandExistsError,
    CommandNotFoundError,
    SecurityError,
    TemplateError,
    ValidationError,
)
from .models import (
    CommandCatalog,
    CommandCatalogEntry,
    CommandConfig,
    CommandParameter,
    ParameterType,
    ScopeType,
)
from .templates import TemplateManager
from .validator import Validator
from .wizard import CommandWizard

__all__ = [
    # Core classes
    "CommandBuilder",
    "CatalogManager",
    "TemplateManager",
    "CommandWizard",
    "Validator",
    # Models
    "CommandConfig",
    "CommandParameter",
    "CommandCatalogEntry",
    "CommandCatalog",
    "ParameterType",
    "ScopeType",
    # Exceptions
    "CommandBuilderError",
    "ValidationError",
    "SecurityError",
    "TemplateError",
    "CatalogError",
    "CommandExistsError",
    "CommandNotFoundError",
]

__version__ = "0.1.0"
