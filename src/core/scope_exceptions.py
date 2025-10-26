"""
Scope Manager Exceptions

Custom exceptions for the scope intelligence system.
"""


class ScopeError(Exception):
    """Base exception for scope-related errors."""

    pass


class ScopeNotFoundError(ScopeError):
    """Raised when a requested scope does not exist.

    Examples:
        >>> raise ScopeNotFoundError("Project scope not found in current directory")
    """

    pass


class InvalidScopeError(ScopeError):
    """Raised when an invalid scope type or configuration is specified.

    Examples:
        >>> raise InvalidScopeError("Invalid scope type: 'invalid'")
    """

    pass


class MultipleScopeFlagsError(ScopeError):
    """Raised when multiple mutually exclusive scope flags are provided.

    Examples:
        >>> raise MultipleScopeFlagsError("Cannot specify both --global and --project")
    """

    pass
