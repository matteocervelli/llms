"""
Custom exceptions for the skill_builder tool.

This module defines a hierarchy of exceptions for skill building operations,
providing clear error messages and proper exception handling throughout the tool.
"""


class SkillBuilderError(Exception):
    """Base exception for all skill_builder errors."""
    pass


class SkillValidationError(SkillBuilderError):
    """Raised when skill configuration validation fails."""
    pass


class SkillExistsError(SkillBuilderError):
    """Raised when attempting to create a skill that already exists."""
    pass


class SkillNotFoundError(SkillBuilderError):
    """Raised when a requested skill cannot be found."""
    pass


class SkillSecurityError(SkillBuilderError):
    """Raised when a security validation fails (e.g., path traversal)."""
    pass


class TemplateError(SkillBuilderError):
    """Raised when template operations fail."""
    pass


class TemplateNotFoundError(TemplateError):
    """Raised when a requested template cannot be found."""
    pass


class CatalogError(SkillBuilderError):
    """Raised when catalog operations fail."""
    pass


class CatalogCorruptedError(CatalogError):
    """Raised when the catalog file is corrupted or invalid."""
    pass
