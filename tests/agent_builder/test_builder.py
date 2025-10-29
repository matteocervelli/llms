"""
Tests for AgentBuilder class.

Tests cover agent creation, file operations, metadata handling,
and error scenarios following TDD approach.
"""

import json
from pathlib import Path
from datetime import datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from src.tools.agent_builder.builder import AgentBuilder
from src.tools.agent_builder.exceptions import (
    AgentExistsError,
    AgentSecurityError,
    AgentValidationError,
)
from src.tools.agent_builder.models import AgentConfig, AgentCatalogEntry, ModelType, ScopeType


class TestAgentBuilderInit:
    """Tests for AgentBuilder initialization."""

    def test_init_creates_builder(self, temp_agent_dir):
        """Test basic initialization."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        assert builder is not None
        assert builder.base_dir == temp_agent_dir

    def test_init_creates_base_dir_if_not_exists(self, tmp_path):
        """Test base directory creation."""
        base_dir = tmp_path / "nonexistent" / "agents"
        builder = AgentBuilder(base_dir=base_dir)
        assert builder.base_dir.exists()
        assert builder.base_dir.is_dir()

    def test_init_with_existing_directory(self, temp_agent_dir):
        """Test initialization with existing directory."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        assert builder.base_dir.exists()
        assert builder.base_dir == temp_agent_dir


class TestAgentCreation:
    """Tests for agent creation functionality."""

    def test_create_basic_agent(self, temp_agent_dir, sample_agent_config):
        """Test creating a basic agent."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Create agent
        result = builder.create_agent(sample_agent_config)

        # Verify result
        assert result is not None
        assert isinstance(result, AgentCatalogEntry)
        assert result.name == "plan-agent"
        assert result.description == sample_agent_config.description
        assert result.scope == ScopeType.PROJECT
        assert result.model == ModelType.SONNET

    def test_create_agent_generates_file(self, temp_agent_dir, sample_agent_config):
        """Test that agent file is created on disk."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config)

        # Verify file exists
        agent_file = result.path
        assert agent_file.exists()
        assert agent_file.is_file()
        assert agent_file.suffix == ".md"

    def test_create_agent_with_custom_content(self, temp_agent_dir, sample_agent_config_with_content):
        """Test creating agent with custom content."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config_with_content)

        # Read file and verify custom content
        content = result.path.read_text()
        assert "# Custom Agent" in content
        assert "This is custom content." in content

    def test_create_agent_with_frontmatter(self, temp_agent_dir, sample_agent_config_with_frontmatter):
        """Test creating agent with custom frontmatter."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config_with_frontmatter)

        # Read file and verify frontmatter
        content = result.path.read_text()
        assert "version: '1.0'" in content or 'version: "1.0"' in content
        assert "- planning" in content
        assert "- architecture" in content

    def test_create_agent_returns_catalog_entry(self, temp_agent_dir, sample_agent_config):
        """Test that create_agent returns proper catalog entry."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config)

        # Verify catalog entry fields
        assert isinstance(result.id, UUID)
        assert result.created_at is not None
        assert result.updated_at is not None
        assert result.path.is_absolute()
        assert "template" in result.metadata

    def test_create_agent_with_invalid_name(self, temp_agent_dir):
        """Test that invalid agent names are rejected."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Pydantic validates the config before it reaches the builder
        with pytest.raises(ValidationError):
            config = AgentConfig(
                name="Invalid Name!",  # Invalid: spaces and special chars
                description="Test agent. Use when testing.",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_create_duplicate_agent_raises_error(self, temp_agent_dir, sample_agent_config):
        """Test that creating duplicate agent raises error."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Create first agent
        builder.create_agent(sample_agent_config)

        # Try to create duplicate
        with pytest.raises(AgentExistsError):
            builder.create_agent(sample_agent_config)


class TestAgentFileContent:
    """Tests for agent file content generation."""

    def test_agent_file_has_frontmatter(self, temp_agent_dir, sample_agent_config):
        """Test that generated file has proper frontmatter."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config)

        content = result.path.read_text()
        assert content.startswith("---\n")
        assert "name: plan-agent" in content
        assert "model: claude-3-5-sonnet-20241022" in content

    def test_agent_file_has_description(self, temp_agent_dir, sample_agent_config):
        """Test that generated file includes description."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config)

        content = result.path.read_text()
        assert sample_agent_config.description in content

    def test_agent_file_well_formatted(self, temp_agent_dir, sample_agent_config):
        """Test that generated file is well-formatted markdown."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config)

        content = result.path.read_text()

        # Check for markdown headers
        assert "# " in content

        # Check frontmatter is closed
        lines = content.split("\n")
        frontmatter_closes = [i for i, line in enumerate(lines) if line.strip() == "---"]
        assert len(frontmatter_closes) >= 2  # Opening and closing ---


class TestAgentMetadata:
    """Tests for agent metadata handling."""

    def test_agent_metadata_includes_template(self, temp_agent_dir, sample_agent_config):
        """Test that metadata includes template name."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config)

        assert "template" in result.metadata
        assert result.metadata["template"] == "basic"

    def test_agent_metadata_includes_timestamps(self, temp_agent_dir, sample_agent_config):
        """Test that metadata includes creation/update timestamps."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config)

        assert result.created_at is not None
        assert result.updated_at is not None
        assert isinstance(result.created_at, datetime)
        assert isinstance(result.updated_at, datetime)

    def test_agent_metadata_preserves_custom_fields(
        self, temp_agent_dir, sample_agent_config_with_frontmatter
    ):
        """Test that custom frontmatter is preserved in metadata."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config_with_frontmatter)

        # Custom frontmatter should be in metadata
        assert result.metadata.get("version") == "1.0" or "version" in result.metadata


class TestSecurityValidation:
    """Tests for security validation."""

    def test_rejects_path_traversal_in_name(self, temp_agent_dir):
        """Test that path traversal in name is rejected."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Pydantic validates the config before it reaches the builder
        with pytest.raises(ValidationError):
            config = AgentConfig(
                name="../../../etc/passwd",
                description="Malicious agent. Use for testing security.",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )

    def test_agent_file_created_in_base_dir(self, temp_agent_dir, sample_agent_config):
        """Test that agent file is created within base directory."""
        builder = AgentBuilder(base_dir=temp_agent_dir)
        result = builder.create_agent(sample_agent_config)

        # Verify path is within base_dir
        assert result.path.resolve().is_relative_to(temp_agent_dir.resolve())

    def test_sanitizes_agent_content(self, temp_agent_dir):
        """Test that agent content is sanitized."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        config = AgentConfig(
            name="test-agent",
            description="Test agent with control chars. Use when testing.",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            content="Test\x00content\x01with\x02control\x03chars",
        )

        result = builder.create_agent(config)
        content = result.path.read_text()

        # Control characters should be removed
        assert "\x00" not in content
        assert "\x01" not in content
        assert "\x02" not in content


class TestAgentDeletion:
    """Tests for agent deletion functionality."""

    def test_delete_existing_agent(self, temp_agent_dir, sample_agent_config):
        """Test deleting an existing agent."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Create agent
        result = builder.create_agent(sample_agent_config)
        agent_file = result.path
        assert agent_file.exists()

        # Delete agent
        success = builder.delete_agent(result.id)
        assert success is True
        assert not agent_file.exists()

    def test_delete_nonexistent_agent_returns_false(self, temp_agent_dir):
        """Test deleting non-existent agent returns False."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        from uuid import uuid4
        fake_id = uuid4()

        success = builder.delete_agent(fake_id)
        assert success is False


class TestAgentRetrieval:
    """Tests for agent retrieval functionality."""

    def test_get_agent_by_name(self, temp_agent_dir, sample_agent_config):
        """Test retrieving agent by name."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Create agent
        created = builder.create_agent(sample_agent_config)

        # Retrieve by name
        retrieved = builder.get_agent(name="plan-agent")
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "plan-agent"

    def test_get_agent_by_id(self, temp_agent_dir, sample_agent_config):
        """Test retrieving agent by ID."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Create agent
        created = builder.create_agent(sample_agent_config)

        # Retrieve by ID
        retrieved = builder.get_agent(agent_id=created.id)
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.name == "plan-agent"

    def test_get_nonexistent_agent_returns_none(self, temp_agent_dir):
        """Test that getting non-existent agent returns None."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        result = builder.get_agent(name="nonexistent")
        assert result is None


class TestAgentListing:
    """Tests for agent listing functionality."""

    def test_list_all_agents(self, temp_agent_dir):
        """Test listing all agents."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Create multiple agents
        for i in range(3):
            config = AgentConfig(
                name=f"agent-{i}",
                description=f"Test agent {i}. Use when testing.",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )
            builder.create_agent(config)

        # List all agents
        agents = builder.list_agents()
        assert len(agents) == 3

    def test_list_agents_by_scope(self, temp_agent_dir):
        """Test listing agents filtered by scope."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        # Create agents with different scopes
        builder.create_agent(
            AgentConfig(
                name="global-agent",
                description="Global agent. Use globally.",
                scope=ScopeType.GLOBAL,
                model=ModelType.SONNET,
            )
        )
        builder.create_agent(
            AgentConfig(
                name="project-agent",
                description="Project agent. Use in projects.",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
            )
        )

        # List by scope
        global_agents = builder.list_agents(scope=ScopeType.GLOBAL)
        assert len(global_agents) == 1
        assert global_agents[0].name == "global-agent"

    def test_list_empty_returns_empty_list(self, temp_agent_dir):
        """Test that listing with no agents returns empty list."""
        builder = AgentBuilder(base_dir=temp_agent_dir)

        agents = builder.list_agents()
        assert agents == []
