"""
Custom exceptions for command builder.

Provides specific exception types for different error scenarios in command creation,
validation, and catalog management.
"""


class CommandBuilderError(Exception):
    """Base exception for all command builder errors."""

    pass


class ValidationError(CommandBuilderError):
    """Raised when command configuration validation fails."""

    pass


class SecurityError(CommandBuilderError):
    """Raised when security validation fails (path traversal, unsafe commands, etc.)."""

    pass


class TemplateError(CommandBuilderError):
    """Raised when template loading or rendering fails."""

    pass


class CatalogError(CommandBuilderError):
    """Raised when catalog operations fail."""

    pass


class CommandExistsError(CommandBuilderError):
    """Raised when attempting to create a command that already exists."""

    pass


class CommandNotFoundError(CommandBuilderError):
    """Raised when a command cannot be found."""

    pass


class ScopeError(CommandBuilderError):
    """Raised when scope-related operations fail."""

    pass
