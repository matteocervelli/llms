"""
Custom exceptions for the catalog system.

This module defines the exception hierarchy for catalog-related errors:
- CatalogError: Base exception for all catalog errors
- CatalogNotFoundError: Catalog file not found
- CatalogValidationError: Data validation failed
- ScanError: Filesystem scanning failed
- SyncError: Catalog synchronization failed
"""


class CatalogError(Exception):
    """Base exception for all catalog-related errors."""


class CatalogNotFoundError(CatalogError):
    """Exception raised when a catalog file is not found."""


class CatalogValidationError(CatalogError):
    """Exception raised when catalog data validation fails."""


class ScanError(CatalogError):
    """Exception raised when filesystem scanning fails."""


class SyncError(CatalogError):
    """Exception raised when catalog synchronization fails."""
