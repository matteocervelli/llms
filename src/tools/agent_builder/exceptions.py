"""
Custom exceptions for the agent_builder tool.

This module defines a hierarchy of exceptions for agent building operations,
providing clear error messages and proper exception handling throughout the tool.
"""


class AgentBuilderError(Exception):
    """Base exception for all agent_builder errors."""

    pass


class AgentValidationError(AgentBuilderError):
    """Raised when agent configuration validation fails."""

    pass


class AgentExistsError(AgentBuilderError):
    """Raised when attempting to create an agent that already exists."""

    pass


class AgentNotFoundError(AgentBuilderError):
    """Raised when a requested agent cannot be found."""

    pass


class AgentSecurityError(AgentBuilderError):
    """Raised when a security validation fails (e.g., path traversal)."""

    pass


class TemplateError(AgentBuilderError):
    """Raised when template operations fail."""

    pass


class TemplateNotFoundError(TemplateError):
    """Raised when a requested template cannot be found."""

    pass


class CatalogError(AgentBuilderError):
    """Raised when catalog operations fail."""

    pass


class CatalogCorruptedError(CatalogError):
    """Raised when the catalog file is corrupted or invalid."""

    pass
