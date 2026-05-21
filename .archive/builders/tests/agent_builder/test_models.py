"""
Tests for agent_builder models.

Tests the Pydantic models for agent configuration, catalog entries,
and catalog management with comprehensive validation rules.
"""

import pytest
from datetime import datetime
from pathlib import Path
from uuid import UUID

from src.tools.agent_builder.models import (
    AgentConfig,
    AgentCatalogEntry,
    AgentCatalog,
    ScopeType,
    ModelType,
)


class TestModelType:
    """Tests for ModelType enum."""

    def test_model_types_exist(self):
        """Test all model types are defined."""
        assert ModelType.HAIKU == "claude-3-5-haiku-20241022"
        assert ModelType.SONNET == "claude-3-5-sonnet-20241022"
        assert ModelType.OPUS == "claude-opus-4-20250514"

    def test_model_type_values(self):
        """Test model type values are strings."""
        for model in ModelType:
            assert isinstance(model.value, str)
            assert len(model.value) > 0


class TestAgentConfig:
    """Tests for AgentConfig model."""

    def test_valid_agent_config(self):
        """Test creating a valid agent configuration."""
        config = AgentConfig(
            name="test-agent",
            description="Test agent for unit testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
        )

        assert config.name == "test-agent"
        assert config.description == "Test agent for unit testing"
        assert config.scope == ScopeType.PROJECT
        assert config.model == ModelType.SONNET
        assert config.template == "basic"
        assert config.content is None
        assert config.frontmatter == {}

    def test_agent_name_validation_valid(self):
        """Test valid agent names."""
        valid_names = [
            "test",
            "test-agent",
            "agent123",
            "my-cool-agent-v2",
            "a",
            "a" * 64,
        ]

        for name in valid_names:
            config = AgentConfig(
                name=name,
                description="Test agent for validation",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )
            assert config.name == name

    def test_agent_name_validation_invalid_empty(self):
        """Test agent name cannot be empty."""
        with pytest.raises(ValueError, match="Name must be 1-64 characters"):
            AgentConfig(
                name="",
                description="Use for testing",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_agent_name_validation_invalid_too_long(self):
        """Test agent name cannot exceed 64 characters."""
        with pytest.raises(ValueError, match="Name must be 1-64 characters"):
            AgentConfig(
                name="a" * 65,
                description="Test agent",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_agent_name_validation_invalid_uppercase(self):
        """Test agent name must be lowercase."""
        with pytest.raises(ValueError, match="lowercase letters"):
            AgentConfig(
                name="TestAgent",
                description="Test agent",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_agent_name_validation_invalid_spaces(self):
        """Test agent name cannot contain spaces."""
        with pytest.raises(ValueError, match="lowercase letters"):
            AgentConfig(
                name="test agent",
                description="Test agent",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_agent_name_validation_invalid_special_chars(self):
        """Test agent name cannot contain special characters."""
        invalid_names = ["test_agent", "test.agent", "test@agent", "test!"]

        for name in invalid_names:
            with pytest.raises(ValueError, match="lowercase letters"):
                AgentConfig(
                    name=name,
                    description="Test agent",
                    scope=ScopeType.PROJECT,
                    model=ModelType.SONNET,
                )

    def test_agent_name_validation_invalid_leading_hyphen(self):
        """Test agent name cannot start with hyphen."""
        with pytest.raises(ValueError, match="cannot start or end with hyphen"):
            AgentConfig(
                name="-test",
                description="Test agent",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_agent_name_validation_invalid_trailing_hyphen(self):
        """Test agent name cannot end with hyphen."""
        with pytest.raises(ValueError, match="cannot start or end with hyphen"):
            AgentConfig(
                name="test-",
                description="Test agent",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_agent_name_validation_invalid_consecutive_hyphens(self):
        """Test agent name cannot contain consecutive hyphens."""
        with pytest.raises(ValueError, match="consecutive hyphens"):
            AgentConfig(
                name="test--agent",
                description="Test agent",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_description_validation_valid(self):
        """Test valid agent descriptions."""
        valid_descriptions = [
            "Use for testing agents",
            "Agent for processing data",
            "Helper when working with files",
            "Use during development if needed",
        ]

        for desc in valid_descriptions:
            config = AgentConfig(
                name="test-agent",
                description=desc,
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )
            assert config.description == desc

    def test_description_validation_invalid_empty(self):
        """Test description cannot be empty."""
        with pytest.raises(ValueError, match="Description cannot be empty"):
            AgentConfig(
                name="test-agent",
                description="",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_description_validation_invalid_too_long(self):
        """Test description cannot exceed 1024 characters."""
        with pytest.raises(ValueError, match="1024 characters or less"):
            AgentConfig(
                name="test-agent",
                description="a" * 1025,
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_description_validation_invalid_no_usage_context(self):
        """Test description must include usage context."""
        with pytest.raises(ValueError, match="should include when"):
            AgentConfig(
                name="test-agent",
                description="This is a test agent.",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_template_validation_valid(self):
        """Test valid template names."""
        valid_templates = ["basic", "advanced", "my_template", "template-v2"]

        for template in valid_templates:
            config = AgentConfig(
                name="test-agent",
                description="Use for testing",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                template=template,
            )
            assert config.template == template

    def test_template_validation_invalid_path_traversal(self):
        """Test template name cannot contain path traversal."""
        with pytest.raises(ValueError, match="Template name cannot contain path separators"):
            AgentConfig(
                name="test-agent",
                description="Use for testing",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                template="../../../etc/passwd",
            )

    def test_custom_content(self):
        """Test agent with custom content."""
        content = "# Custom Agent\n\nThis is custom content."
        config = AgentConfig(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            content=content,
        )
        assert config.content == content

    def test_custom_frontmatter(self):
        """Test agent with custom frontmatter."""
        frontmatter = {"custom_field": "value", "version": "1.0"}
        config = AgentConfig(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            frontmatter=frontmatter,
        )
        assert config.frontmatter == frontmatter


class TestAgentCatalogEntry:
    """Tests for AgentCatalogEntry model."""

    def test_valid_catalog_entry(self):
        """Test creating a valid catalog entry."""
        entry = AgentCatalogEntry(
            name="test-agent",
            description="Test agent for validation",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path/to/agent"),
        )

        assert entry.name == "test-agent"
        assert entry.description == "Test agent for validation"
        assert entry.scope == ScopeType.PROJECT
        assert entry.model == ModelType.SONNET
        assert entry.path == Path("/absolute/path/to/agent")
        assert isinstance(entry.id, UUID)
        assert isinstance(entry.created_at, datetime)
        assert isinstance(entry.updated_at, datetime)
        assert entry.metadata == {}

    def test_catalog_entry_with_metadata(self):
        """Test catalog entry with metadata."""
        metadata = {"template": "basic", "version": "1.0"}
        entry = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path"),
            metadata=metadata,
        )
        assert entry.metadata == metadata

    def test_catalog_entry_path_must_be_absolute(self):
        """Test catalog entry path must be absolute."""
        with pytest.raises(ValueError, match="Path must be absolute"):
            AgentCatalogEntry(
                name="test-agent",
                description="Use for testing",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                path=Path("relative/path"),
            )


class TestAgentCatalog:
    """Tests for AgentCatalog model."""

    def test_empty_catalog(self):
        """Test creating an empty catalog."""
        catalog = AgentCatalog()
        assert catalog.schema_version == "1.0"
        assert catalog.agents == []

    def test_add_agent(self):
        """Test adding an agent to catalog."""
        catalog = AgentCatalog()
        entry = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path"),
        )

        catalog.add_agent(entry)
        assert len(catalog.agents) == 1
        assert catalog.agents[0] == entry

    def test_add_duplicate_agent_raises_error(self):
        """Test adding duplicate agent raises error."""
        catalog = AgentCatalog()
        entry1 = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path1"),
        )
        entry2 = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path2"),
        )

        catalog.add_agent(entry1)
        with pytest.raises(ValueError, match="already exists"):
            catalog.add_agent(entry2)

    def test_get_by_id(self):
        """Test retrieving agent by ID."""
        catalog = AgentCatalog()
        entry = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path"),
        )
        catalog.add_agent(entry)

        found = catalog.get_by_id(entry.id)
        assert found == entry

        # Test not found
        from uuid import uuid4

        assert catalog.get_by_id(uuid4()) is None

    def test_get_by_name(self):
        """Test retrieving agent by name."""
        catalog = AgentCatalog()
        entry = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path"),
        )
        catalog.add_agent(entry)

        found = catalog.get_by_name("test-agent")
        assert found == entry

        # Test not found
        assert catalog.get_by_name("nonexistent") is None

    def test_get_by_name_with_scope_filter(self):
        """Test retrieving agent by name with scope filter."""
        catalog = AgentCatalog()
        entry1 = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path1"),
        )
        entry2 = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.GLOBAL,
            model=ModelType.SONNET,
            path=Path("/absolute/path2"),
        )
        catalog.add_agent(entry1)

        # Same name, different scope should not conflict
        catalog.agents.append(entry2)  # Bypass duplicate check for testing

        found = catalog.get_by_name("test-agent", scope=ScopeType.PROJECT)
        assert found == entry1

        found = catalog.get_by_name("test-agent", scope=ScopeType.GLOBAL)
        assert found == entry2

    def test_search_by_name(self):
        """Test searching agents by name."""
        catalog = AgentCatalog()
        catalog.add_agent(
            AgentCatalogEntry(
                name="pdf-processor",
                description="Use for PDF processing",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                path=Path("/path1"),
            )
        )
        catalog.add_agent(
            AgentCatalogEntry(
                name="data-analyzer",
                description="Use for data analysis",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                path=Path("/path2"),
            )
        )

        results = catalog.search("pdf")
        assert len(results) == 1
        assert results[0].name == "pdf-processor"

    def test_search_by_description(self):
        """Test searching agents by description."""
        catalog = AgentCatalog()
        catalog.add_agent(
            AgentCatalogEntry(
                name="agent1",
                description="Use for PDF processing",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                path=Path("/path1"),
            )
        )
        catalog.add_agent(
            AgentCatalogEntry(
                name="agent2",
                description="Use for data analysis",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                path=Path("/path2"),
            )
        )

        results = catalog.search("analysis")
        assert len(results) == 1
        assert results[0].name == "agent2"

    def test_search_with_scope_filter(self):
        """Test searching with scope filter."""
        catalog = AgentCatalog()
        catalog.add_agent(
            AgentCatalogEntry(
                name="global-agent",
                description="Use for testing",
                scope=ScopeType.GLOBAL,
                model=ModelType.SONNET,
                path=Path("/path1"),
            )
        )
        catalog.add_agent(
            AgentCatalogEntry(
                name="project-agent",
                description="Use for testing",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                path=Path("/path2"),
            )
        )

        results = catalog.search("agent", scope=ScopeType.PROJECT)
        assert len(results) == 1
        assert results[0].scope == ScopeType.PROJECT

    def test_filter_by_scope(self):
        """Test filtering agents by scope."""
        catalog = AgentCatalog()
        catalog.add_agent(
            AgentCatalogEntry(
                name="agent1",
                description="Use for testing",
                scope=ScopeType.GLOBAL,
                model=ModelType.SONNET,
                path=Path("/path1"),
            )
        )
        catalog.add_agent(
            AgentCatalogEntry(
                name="agent2",
                description="Use for testing",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                path=Path("/path2"),
            )
        )

        global_agents = catalog.filter_by_scope(ScopeType.GLOBAL)
        assert len(global_agents) == 1
        assert global_agents[0].scope == ScopeType.GLOBAL

    def test_remove_agent(self):
        """Test removing an agent from catalog."""
        catalog = AgentCatalog()
        entry = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path"),
        )
        catalog.add_agent(entry)

        assert catalog.remove_agent(entry.id) is True
        assert len(catalog.agents) == 0

        # Test removing nonexistent agent
        from uuid import uuid4

        assert catalog.remove_agent(uuid4()) is False

    def test_update_agent(self):
        """Test updating an agent's fields."""
        catalog = AgentCatalog()
        entry = AgentCatalogEntry(
            name="test-agent",
            description="Use for testing",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=Path("/absolute/path"),
        )
        catalog.add_agent(entry)

        original_updated_at = entry.updated_at

        # Update description
        assert catalog.update_agent(entry.id, description="Updated description") is True

        updated_entry = catalog.get_by_id(entry.id)
        assert updated_entry.description == "Updated description"
        assert updated_entry.updated_at > original_updated_at

        # Test updating nonexistent agent
        from uuid import uuid4

        assert catalog.update_agent(uuid4(), description="test") is False
