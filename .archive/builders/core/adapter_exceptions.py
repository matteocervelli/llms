"""
Custom exceptions for LLM adapter operations.

This module provides specialized exception classes for handling errors that occur
during LLM adapter operations such as skill/command/agent creation, validation,
and scope management.

Exception Hierarchy:
    AdapterError (base)
    ├── InvalidNameError (validation errors)
    ├── CreationError (file creation/write errors)
    └── UnsupportedScopeError (scope compatibility errors)

Example Usage:
    >>> from src.core.adapter_exceptions import InvalidNameError
    >>>
    >>> def validate_skill_name(name: str) -> None:
    ...     if not name.replace("-", "").replace("_", "").isalnum():
    ...         raise InvalidNameError(f"Invalid skill name: '{name}'")
"""


class AdapterError(Exception):
    """Base exception for all LLM adapter errors.

    All adapter-specific exceptions inherit from this class, allowing
    for convenient error handling with a single catch block.

    Example:
        >>> try:
        ...     adapter.create_skill("my-skill")
        ... except AdapterError as e:
        ...     print(f"Adapter error: {e}")
    """

    pass


class InvalidNameError(AdapterError):
    """Raised when a skill/command/agent name fails validation.

    This exception is raised when the provided name contains invalid characters,
    exceeds length limits, or violates naming conventions.

    Valid names must:
    - Contain only alphanumeric characters, hyphens, and underscores
    - Be between 1 and 64 characters long
    - Not start or end with hyphens or underscores

    Example:
        >>> raise InvalidNameError("Name contains invalid characters: 'my skill!'")
    """

    pass


class CreationError(AdapterError):
    """Raised when file or directory creation fails.

    This exception is raised when the adapter cannot create a skill, command,
    or agent due to filesystem errors, permission issues, or other I/O problems.

    Common causes:
    - Insufficient write permissions
    - File already exists (when overwrite is disabled)
    - Parent directory doesn't exist
    - Disk space issues

    Example:
        >>> raise CreationError("Failed to create skill file: Permission denied")
    """

    pass


class UnsupportedScopeError(AdapterError):
    """Raised when an operation is attempted on an unsupported scope.

    This exception is raised when an adapter doesn't support a particular
    scope type (global, project, or local) or when the scope configuration
    is incompatible with the adapter's requirements.

    Example:
        >>> raise UnsupportedScopeError(
        ...     "CodexAdapter does not support local scope"
        ... )
    """

    pass


# Public API for easy imports
__all__ = [
    "AdapterError",
    "InvalidNameError",
    "CreationError",
    "UnsupportedScopeError",
]
