"""
Tests for catalog_system Pydantic data models.
"""

from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest
from pydantic import ValidationError


class TestCatalogEntry:
    """Test base CatalogEntry model."""

    def test_catalog_entry_with_valid_data(self):
        """Test creating CatalogEntry with valid data."""
        from src.tools.catalog_system.models import CatalogEntry

        entry = CatalogEntry(
            name="test-skill",
            scope="global",
            description="A test skill",
            file_path=Path("/path/to/skill.md"),
        )
        assert entry.name == "test-skill"
        assert entry.scope == "global"
        assert entry.description == "A test skill"
        assert entry.file_path == Path("/path/to/skill.md")
        assert isinstance(entry.id, UUID)
        assert isinstance(entry.created_at, datetime)
        assert isinstance(entry.updated_at, datetime)

    def test_catalog_entry_with_minimal_data(self):
        """Test creating CatalogEntry with minimal required fields."""
        from src.tools.catalog_system.models import CatalogEntry

        entry = CatalogEntry(name="minimal", scope="project", file_path=Path("/path/to/file.md"))
        assert entry.name == "minimal"
        assert entry.scope == "project"
        assert entry.description == ""  # Default empty string
        assert entry.file_path == Path("/path/to/file.md")

    def test_catalog_entry_name_validation_min_length(self):
        """Test name field has minimum length validation."""
        from src.tools.catalog_system.models import CatalogEntry

        with pytest.raises(ValidationError) as exc_info:
            CatalogEntry(name="", scope="global", file_path=Path("/path/to/file.md"))  # Empty name

        error = exc_info.value.errors()[0]
        assert "name" in str(error["loc"])

    def test_catalog_entry_name_validation_max_length(self):
        """Test name field has maximum length validation."""
        from src.tools.catalog_system.models import CatalogEntry

        with pytest.raises(ValidationError) as exc_info:
            CatalogEntry(
                name="a" * 101,  # Exceeds 100 character limit
                scope="global",
                file_path=Path("/path/to/file.md"),
            )

        error = exc_info.value.errors()[0]
        assert "name" in str(error["loc"])

    def test_catalog_entry_scope_validation(self):
        """Test scope field only accepts valid literals."""
        from src.tools.catalog_system.models import CatalogEntry

        # Valid scopes
        for scope in ["global", "project", "local"]:
            entry = CatalogEntry(name="test", scope=scope, file_path=Path("/path/to/file.md"))
            assert entry.scope == scope

        # Invalid scope
        with pytest.raises(ValidationError) as exc_info:
            CatalogEntry(
                name="test",
                scope="invalid",
                file_path=Path("/path/to/file.md"),
            )

        error = exc_info.value.errors()[0]
        assert "scope" in str(error["loc"])

    def test_catalog_entry_description_max_length(self):
        """Test description field has maximum length validation."""
        from src.tools.catalog_system.models import CatalogEntry

        with pytest.raises(ValidationError) as exc_info:
            CatalogEntry(
                name="test",
                scope="global",
                description="a" * 501,  # Exceeds 500 character limit
                file_path=Path("/path/to/file.md"),
            )

        error = exc_info.value.errors()[0]
        assert "description" in str(error["loc"])

    def test_catalog_entry_timestamps_auto_generated(self):
        """Test created_at and updated_at are auto-generated."""
        from src.tools.catalog_system.models import CatalogEntry

        entry = CatalogEntry(name="test", scope="global", file_path=Path("/path/to/file.md"))
        assert isinstance(entry.created_at, datetime)
        assert isinstance(entry.updated_at, datetime)
        # Both should be approximately the same time
        assert abs((entry.updated_at - entry.created_at).total_seconds()) < 1  # Within 1 second

    def test_catalog_entry_id_auto_generated(self):
        """Test id is auto-generated as UUID."""
        from src.tools.catalog_system.models import CatalogEntry

        entry1 = CatalogEntry(name="test1", scope="global", file_path=Path("/path/to/file1.md"))
        entry2 = CatalogEntry(name="test2", scope="global", file_path=Path("/path/to/file2.md"))
        assert isinstance(entry1.id, UUID)
        assert isinstance(entry2.id, UUID)
        assert entry1.id != entry2.id  # Different UUIDs


class TestSkillCatalogEntry:
    """Test SkillCatalogEntry model."""

    def test_skill_catalog_entry_with_valid_data(self):
        """Test creating SkillCatalogEntry with valid data."""
        from src.tools.catalog_system.models import SkillCatalogEntry

        entry = SkillCatalogEntry(
            name="example-skill",
            scope="global",
            description="An example skill",
            file_path=Path("/path/to/skill.md"),
            template="basic",
            has_scripts=True,
            file_count=3,
            allowed_tools=["Read", "Write", "Bash"],
        )
        assert entry.name == "example-skill"
        assert entry.template == "basic"
        assert entry.has_scripts is True
        assert entry.file_count == 3
        assert entry.allowed_tools == ["Read", "Write", "Bash"]

    def test_skill_catalog_entry_with_defaults(self):
        """Test SkillCatalogEntry default values."""
        from src.tools.catalog_system.models import SkillCatalogEntry

        entry = SkillCatalogEntry(
            name="minimal-skill",
            scope="project",
            file_path=Path("/path/to/skill.md"),
            template="basic",
        )
        assert entry.has_scripts is False  # Default
        assert entry.file_count == 1  # Default
        assert entry.allowed_tools == []  # Default

    def test_skill_catalog_entry_template_required(self):
        """Test template field is required."""
        from src.tools.catalog_system.models import SkillCatalogEntry

        with pytest.raises(ValidationError) as exc_info:
            SkillCatalogEntry(
                name="test",
                scope="global",
                file_path=Path("/path/to/file.md"),
                # Missing template
            )

        error = exc_info.value.errors()[0]
        assert "template" in str(error["loc"])


class TestCommandCatalogEntry:
    """Test CommandCatalogEntry model."""

    def test_command_catalog_entry_with_valid_data(self):
        """Test creating CommandCatalogEntry with valid data."""
        from src.tools.catalog_system.models import CommandCatalogEntry

        entry = CommandCatalogEntry(
            name="test-command",
            scope="global",
            description="A test command",
            file_path=Path("/path/to/command.md"),
            aliases=["tc", "testcmd"],
            requires_tools=["gh", "git"],
            tags=["testing", "cli"],
        )
        assert entry.name == "test-command"
        assert entry.aliases == ["tc", "testcmd"]
        assert entry.requires_tools == ["gh", "git"]
        assert entry.tags == ["testing", "cli"]

    def test_command_catalog_entry_with_defaults(self):
        """Test CommandCatalogEntry default values."""
        from src.tools.catalog_system.models import CommandCatalogEntry

        entry = CommandCatalogEntry(
            name="minimal-command",
            scope="project",
            file_path=Path("/path/to/command.md"),
        )
        assert entry.aliases == []  # Default
        assert entry.requires_tools == []  # Default
        assert entry.tags == []  # Default


class TestAgentCatalogEntry:
    """Test AgentCatalogEntry model."""

    def test_agent_catalog_entry_with_valid_data(self):
        """Test creating AgentCatalogEntry with valid data."""
        from src.tools.catalog_system.models import AgentCatalogEntry

        entry = AgentCatalogEntry(
            name="test-agent",
            scope="global",
            description="A test agent",
            file_path=Path("/path/to/agent.md"),
            model="sonnet",
            specialization="Testing specialist",
            requires_skills=["skill1", "skill2"],
        )
        assert entry.name == "test-agent"
        assert entry.model == "sonnet"
        assert entry.specialization == "Testing specialist"
        assert entry.requires_skills == ["skill1", "skill2"]

    def test_agent_catalog_entry_with_defaults(self):
        """Test AgentCatalogEntry default values."""
        from src.tools.catalog_system.models import AgentCatalogEntry

        entry = AgentCatalogEntry(
            name="minimal-agent",
            scope="project",
            file_path=Path("/path/to/agent.md"),
            model="haiku",
        )
        assert entry.specialization == ""  # Default
        assert entry.requires_skills == []  # Default

    def test_agent_catalog_entry_model_required(self):
        """Test model field is required."""
        from src.tools.catalog_system.models import AgentCatalogEntry

        with pytest.raises(ValidationError) as exc_info:
            AgentCatalogEntry(
                name="test",
                scope="global",
                file_path=Path("/path/to/file.md"),
                # Missing model
            )

        error = exc_info.value.errors()[0]
        assert "model" in str(error["loc"])


class TestModelSerialization:
    """Test Pydantic model serialization and deserialization."""

    def test_catalog_entry_to_dict(self):
        """Test CatalogEntry can be serialized to dict."""
        from src.tools.catalog_system.models import CatalogEntry

        entry = CatalogEntry(name="test", scope="global", file_path=Path("/path/to/file.md"))
        data = entry.model_dump()
        assert data["name"] == "test"
        assert data["scope"] == "global"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_catalog_entry_from_dict(self):
        """Test CatalogEntry can be deserialized from dict."""
        from src.tools.catalog_system.models import CatalogEntry

        data = {
            "name": "test",
            "scope": "global",
            "description": "Test entry",
            "file_path": "/path/to/file.md",
        }
        entry = CatalogEntry(**data)
        assert entry.name == "test"
        assert entry.scope == "global"

    def test_skill_catalog_entry_to_json(self):
        """Test SkillCatalogEntry can be serialized to JSON."""
        from src.tools.catalog_system.models import SkillCatalogEntry

        entry = SkillCatalogEntry(
            name="test-skill",
            scope="global",
            file_path=Path("/path/to/skill.md"),
            template="basic",
            allowed_tools=["Read", "Write"],
        )
        json_str = entry.model_dump_json()
        assert "test-skill" in json_str
        assert "basic" in json_str
        assert "Read" in json_str

    def test_skill_catalog_entry_from_json(self):
        """Test SkillCatalogEntry can be deserialized from JSON."""
        from src.tools.catalog_system.models import SkillCatalogEntry

        json_str = """
        {
            "name": "test-skill",
            "scope": "global",
            "file_path": "/path/to/skill.md",
            "template": "basic",
            "allowed_tools": ["Read", "Write"]
        }
        """
        entry = SkillCatalogEntry.model_validate_json(json_str)
        assert entry.name == "test-skill"
        assert entry.template == "basic"
        assert entry.allowed_tools == ["Read", "Write"]
