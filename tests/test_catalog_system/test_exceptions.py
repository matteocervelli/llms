"""
Tests for catalog_system exception hierarchy.
"""


class TestExceptionHierarchy:
    """Test custom exception classes and inheritance."""

    def test_catalog_error_is_base_exception(self):
        """Test that CatalogError is the base exception."""
        from src.tools.catalog_system.exceptions import CatalogError

        error = CatalogError("test message")
        assert isinstance(error, Exception)
        assert str(error) == "test message"

    def test_catalog_not_found_error_inherits_from_catalog_error(self):
        """Test that CatalogNotFoundError inherits from CatalogError."""
        from src.tools.catalog_system.exceptions import CatalogError, CatalogNotFoundError

        error = CatalogNotFoundError("catalog not found")
        assert isinstance(error, CatalogError)
        assert isinstance(error, Exception)
        assert str(error) == "catalog not found"

    def test_catalog_validation_error_inherits_from_catalog_error(self):
        """Test that CatalogValidationError inherits from CatalogError."""
        from src.tools.catalog_system.exceptions import CatalogError, CatalogValidationError

        error = CatalogValidationError("validation failed")
        assert isinstance(error, CatalogError)
        assert isinstance(error, Exception)
        assert str(error) == "validation failed"

    def test_scan_error_inherits_from_catalog_error(self):
        """Test that ScanError inherits from CatalogError."""
        from src.tools.catalog_system.exceptions import CatalogError, ScanError

        error = ScanError("scan failed")
        assert isinstance(error, CatalogError)
        assert isinstance(error, Exception)
        assert str(error) == "scan failed"

    def test_sync_error_inherits_from_catalog_error(self):
        """Test that SyncError inherits from CatalogError."""
        from src.tools.catalog_system.exceptions import CatalogError, SyncError

        error = SyncError("sync failed")
        assert isinstance(error, CatalogError)
        assert isinstance(error, Exception)
        assert str(error) == "sync failed"


class TestExceptionMessages:
    """Test exception messages and formatting."""

    def test_exception_with_empty_message(self):
        """Test exceptions can be created with empty message."""
        from src.tools.catalog_system.exceptions import CatalogError

        error = CatalogError("")
        assert str(error) == ""

    def test_exception_with_formatted_message(self):
        """Test exceptions support formatted messages."""
        from src.tools.catalog_system.exceptions import CatalogNotFoundError

        error = CatalogNotFoundError(f"Catalog 'skills.json' not found in {'/path/to/dir'}")
        assert "skills.json" in str(error)
        assert "/path/to/dir" in str(error)

    def test_exception_with_multiline_message(self):
        """Test exceptions support multiline messages."""
        from src.tools.catalog_system.exceptions import CatalogValidationError

        message = """Validation failed:
        - Field 'name' is required
        - Field 'scope' must be one of: global, project, local"""
        error = CatalogValidationError(message)
        assert "Validation failed" in str(error)
        assert "Field 'name' is required" in str(error)
