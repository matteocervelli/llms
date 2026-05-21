"""
Tests for agent_builder exceptions.

Tests the custom exception hierarchy for agent builder operations.
"""

import pytest

from src.tools.agent_builder.exceptions import (
    AgentBuilderError,
    AgentValidationError,
    AgentExistsError,
    AgentNotFoundError,
    AgentSecurityError,
    TemplateError,
    TemplateNotFoundError,
    CatalogError,
    CatalogCorruptedError,
)


class TestExceptionHierarchy:
    """Tests for exception hierarchy."""

    def test_base_exception(self):
        """Test base AgentBuilderError."""
        error = AgentBuilderError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_validation_error(self):
        """Test AgentValidationError inherits from base."""
        error = AgentValidationError("Validation failed")
        assert isinstance(error, AgentBuilderError)
        assert str(error) == "Validation failed"

    def test_agent_exists_error(self):
        """Test AgentExistsError inherits from base."""
        error = AgentExistsError("Agent already exists")
        assert isinstance(error, AgentBuilderError)
        assert str(error) == "Agent already exists"

    def test_agent_not_found_error(self):
        """Test AgentNotFoundError inherits from base."""
        error = AgentNotFoundError("Agent not found")
        assert isinstance(error, AgentBuilderError)
        assert str(error) == "Agent not found"

    def test_agent_security_error(self):
        """Test AgentSecurityError inherits from base."""
        error = AgentSecurityError("Security violation")
        assert isinstance(error, AgentBuilderError)
        assert str(error) == "Security violation"

    def test_template_error(self):
        """Test TemplateError inherits from base."""
        error = TemplateError("Template error")
        assert isinstance(error, AgentBuilderError)
        assert str(error) == "Template error"

    def test_template_not_found_error(self):
        """Test TemplateNotFoundError inherits from TemplateError."""
        error = TemplateNotFoundError("Template not found")
        assert isinstance(error, TemplateError)
        assert isinstance(error, AgentBuilderError)
        assert str(error) == "Template not found"

    def test_catalog_error(self):
        """Test CatalogError inherits from base."""
        error = CatalogError("Catalog error")
        assert isinstance(error, AgentBuilderError)
        assert str(error) == "Catalog error"

    def test_catalog_corrupted_error(self):
        """Test CatalogCorruptedError inherits from CatalogError."""
        error = CatalogCorruptedError("Catalog corrupted")
        assert isinstance(error, CatalogError)
        assert isinstance(error, AgentBuilderError)
        assert str(error) == "Catalog corrupted"

    def test_can_raise_and_catch_base(self):
        """Test can raise and catch base exception."""
        with pytest.raises(AgentBuilderError):
            raise AgentValidationError("test")

    def test_can_raise_and_catch_specific(self):
        """Test can raise and catch specific exception."""
        with pytest.raises(AgentValidationError):
            raise AgentValidationError("test")

    def test_can_distinguish_exceptions(self):
        """Test can distinguish between different exceptions."""
        try:
            raise AgentExistsError("test")
        except AgentNotFoundError:
            pytest.fail("Should not catch AgentNotFoundError")
        except AgentExistsError:
            pass  # Expected
