"""
Unit tests for LLM adapter architecture.

This test suite provides comprehensive coverage for the LLM adapter system,
including abstract base class constraints, ClaudeAdapter implementation,
input validation, file creation, and error handling.

Test Coverage:
    - Abstract base class instantiation prevention
    - ClaudeAdapter initialization and metadata
    - Input validation (names, descriptions)
    - File creation for skills, commands, agents
    - Error handling (invalid names, permissions, overwrites)
    - Integration with ScopeManager

Run tests:
    pytest tests/test_llm_adapter.py -v
    pytest tests/test_llm_adapter.py --cov=src/core/llm_adapter
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from datetime import datetime

from src.core.llm_adapter import LLMAdapter, ClaudeAdapter
from src.core.adapter_exceptions import (
    InvalidNameError,
    CreationError,
    UnsupportedScopeError,
)
from src.core.adapter_models import ElementType, AdapterMetadata
from src.core.scope_manager import ScopeConfig, ScopeType


class TestLLMAdapterAbstract:
    """Test suite for LLMAdapter abstract base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Test that LLMAdapter cannot be instantiated directly."""
        scope_config = ScopeConfig(
            path=Path("/test/.claude"),
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            LLMAdapter(scope_config)

    def test_abstract_methods_required(self):
        """Test that subclasses must implement all abstract methods."""

        class IncompleteAdapter(LLMAdapter):
            """Incomplete adapter missing abstract methods."""

            def _get_metadata(self):
                return AdapterMetadata(
                    name="incomplete",
                    version="1.0.0",
                    supported_scopes=["global"],
                    supported_elements=[ElementType.SKILL],
                )

        scope_config = ScopeConfig(
            path=Path("/test/.claude"),
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAdapter(scope_config)


class TestClaudeAdapterInitialization:
    """Test suite for ClaudeAdapter initialization."""

    def test_initialization_with_global_scope(self):
        """Test ClaudeAdapter initializes correctly with global scope."""
        scope_config = ScopeConfig(
            path=Path("/home/user/.claude"),
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )

        adapter = ClaudeAdapter(scope_config)

        assert adapter.scope_config == scope_config
        assert adapter.metadata.name == "claude"
        assert adapter.metadata.version == "1.0.0"
        assert "global" in adapter.metadata.supported_scopes

    def test_initialization_with_project_scope(self):
        """Test ClaudeAdapter initializes correctly with project scope."""
        scope_config = ScopeConfig(
            path=Path("/home/user/project/.claude"),
            type=ScopeType.PROJECT,
            precedence=2,
            exists=True,
        )

        adapter = ClaudeAdapter(scope_config)

        assert adapter.scope_config.type == ScopeType.PROJECT
        assert "project" in adapter.metadata.supported_scopes

    def test_initialization_with_local_scope(self):
        """Test ClaudeAdapter initializes correctly with local scope."""
        scope_config = ScopeConfig(
            path=Path("/home/user/project/.claude/settings.local.json"),
            type=ScopeType.LOCAL,
            precedence=1,
            exists=True,
        )

        adapter = ClaudeAdapter(scope_config)

        assert adapter.scope_config.type == ScopeType.LOCAL
        assert "local" in adapter.metadata.supported_scopes

    def test_metadata_structure(self):
        """Test that adapter metadata has correct structure."""
        scope_config = ScopeConfig(
            path=Path("/test/.claude"),
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )

        adapter = ClaudeAdapter(scope_config)
        metadata = adapter.metadata

        assert metadata.name == "claude"
        assert metadata.version == "1.0.0"
        assert set(metadata.supported_scopes) == {"global", "project", "local"}
        assert set(metadata.supported_elements) == {
            ElementType.SKILL,
            ElementType.COMMAND,
            ElementType.AGENT,
        }
        assert metadata.requires_config is False


class TestInputValidation:
    """Test suite for input validation methods."""

    @pytest.fixture
    def adapter(self):
        """Fixture providing a ClaudeAdapter instance."""
        scope_config = ScopeConfig(
            path=Path("/test/.claude"),
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )
        return ClaudeAdapter(scope_config)

    def test_validate_name_valid_alphanumeric(self, adapter):
        """Test validation accepts valid alphanumeric names."""
        adapter.validate_name("myskill", ElementType.SKILL)  # Should not raise

    def test_validate_name_valid_with_hyphens(self, adapter):
        """Test validation accepts names with hyphens."""
        adapter.validate_name("my-skill", ElementType.SKILL)  # Should not raise

    def test_validate_name_valid_with_underscores(self, adapter):
        """Test validation accepts names with underscores."""
        adapter.validate_name("my_skill", ElementType.SKILL)  # Should not raise

    def test_validate_name_valid_mixed(self, adapter):
        """Test validation accepts mixed valid characters."""
        adapter.validate_name("my-skill_v2", ElementType.SKILL)  # Should not raise

    def test_validate_name_empty_fails(self, adapter):
        """Test validation rejects empty names."""
        with pytest.raises(InvalidNameError, match="cannot be empty"):
            adapter.validate_name("", ElementType.SKILL)

    def test_validate_name_spaces_fail(self, adapter):
        """Test validation rejects names with spaces."""
        with pytest.raises(InvalidNameError, match="Invalid"):
            adapter.validate_name("my skill", ElementType.SKILL)

    def test_validate_name_special_chars_fail(self, adapter):
        """Test validation rejects names with special characters."""
        with pytest.raises(InvalidNameError, match="Invalid"):
            adapter.validate_name("my-skill!", ElementType.SKILL)

    def test_validate_name_starts_with_hyphen_fails(self, adapter):
        """Test validation rejects names starting with hyphen."""
        with pytest.raises(InvalidNameError, match="Invalid"):
            adapter.validate_name("-myskill", ElementType.SKILL)

    def test_validate_name_ends_with_hyphen_fails(self, adapter):
        """Test validation rejects names ending with hyphen."""
        with pytest.raises(InvalidNameError, match="Invalid"):
            adapter.validate_name("myskill-", ElementType.SKILL)

    def test_validate_name_too_long_fails(self, adapter):
        """Test validation rejects names exceeding max length."""
        long_name = "a" * 65  # MAX_NAME_LENGTH is 64
        with pytest.raises(InvalidNameError, match="too long"):
            adapter.validate_name(long_name, ElementType.SKILL)

    def test_sanitize_input_removes_null_bytes(self, adapter):
        """Test sanitization removes null bytes."""
        result = adapter.sanitize_input("Hello\x00World")
        assert result == "HelloWorld"

    def test_sanitize_input_removes_control_chars(self, adapter):
        """Test sanitization removes control characters."""
        result = adapter.sanitize_input("Hello\x01\x02World")
        assert result == "HelloWorld"

    def test_sanitize_input_keeps_newlines(self, adapter):
        """Test sanitization keeps newline characters."""
        result = adapter.sanitize_input("Hello\nWorld")
        assert result == "Hello\nWorld"

    def test_sanitize_input_enforces_length_limit(self, adapter):
        """Test sanitization enforces length limits."""
        long_text = "a" * 600
        result = adapter.sanitize_input(long_text, max_length=500)
        assert len(result) == 500

    def test_sanitize_input_strips_whitespace(self, adapter):
        """Test sanitization strips leading/trailing whitespace."""
        result = adapter.sanitize_input("  Hello World  ")
        assert result == "Hello World"


class TestSkillCreation:
    """Test suite for skill creation functionality."""

    @pytest.fixture
    def adapter(self, tmp_path):
        """Fixture providing a ClaudeAdapter with temp directory."""
        scope_config = ScopeConfig(
            path=tmp_path / ".claude",
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )
        return ClaudeAdapter(scope_config)

    def test_create_skill_success(self, adapter, tmp_path):
        """Test successful skill creation."""
        result = adapter.create_skill(
            name="test-skill",
            description="A test skill",
            content="# Implementation\n\nTest content",
        )

        assert result.success is True
        assert result.element_type == ElementType.SKILL
        assert result.path == tmp_path / ".claude" / "skills" / "test-skill.md"
        assert result.path.exists()
        assert "test-skill" in result.message

    def test_create_skill_creates_directory(self, adapter, tmp_path):
        """Test that skill creation creates skills/ directory if needed."""
        skills_dir = tmp_path / ".claude" / "skills"
        assert not skills_dir.exists()

        adapter.create_skill(name="test", description="Test", content="Content")

        assert skills_dir.exists()
        assert skills_dir.is_dir()

    def test_create_skill_writes_content(self, adapter, tmp_path):
        """Test that skill file contains correct content."""
        result = adapter.create_skill(
            name="test",
            description="Description",
            content="Implementation content",
        )

        content = result.path.read_text()
        assert "# test" in content
        assert "Description" in content
        assert "Implementation content" in content

    def test_create_skill_invalid_name_fails(self, adapter):
        """Test that skill creation fails with invalid name."""
        with pytest.raises(InvalidNameError):
            adapter.create_skill(
                name="invalid name!",
                description="Test",
                content="Content",
            )

    def test_create_skill_duplicate_fails_without_overwrite(self, adapter, tmp_path):
        """Test that duplicate skill creation fails without overwrite flag."""
        adapter.create_skill(name="test", description="Test", content="Content")

        with pytest.raises(CreationError, match="already exists"):
            adapter.create_skill(name="test", description="Test", content="Content")

    def test_create_skill_duplicate_succeeds_with_overwrite(self, adapter, tmp_path):
        """Test that duplicate skill creation succeeds with overwrite=True."""
        adapter.create_skill(name="test", description="Original", content="Original content")

        result = adapter.create_skill(
            name="test",
            description="Updated",
            content="Updated content",
            overwrite=True,
        )

        assert result.success is True
        content = result.path.read_text()
        assert "Updated" in content
        assert "Updated content" in content

    def test_create_skill_metadata(self, adapter):
        """Test that skill creation includes metadata."""
        result = adapter.create_skill(name="test", description="Test skill", content="Content")

        assert "scope" in result.metadata
        assert result.metadata["scope"] == "global"
        assert "created_at" in result.metadata
        assert "description" in result.metadata
        assert result.metadata["description"] == "Test skill"


class TestCommandCreation:
    """Test suite for command creation functionality."""

    @pytest.fixture
    def adapter(self, tmp_path):
        """Fixture providing a ClaudeAdapter with temp directory."""
        scope_config = ScopeConfig(
            path=tmp_path / ".claude",
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )
        return ClaudeAdapter(scope_config)

    def test_create_command_success(self, adapter, tmp_path):
        """Test successful command creation."""
        result = adapter.create_command(
            name="test-command",
            description="A test command",
            content="Command implementation",
        )

        assert result.success is True
        assert result.element_type == ElementType.COMMAND
        assert result.path == tmp_path / ".claude" / "commands" / "test-command.md"
        assert result.path.exists()

    def test_create_command_creates_directory(self, adapter, tmp_path):
        """Test that command creation creates commands/ directory if needed."""
        commands_dir = tmp_path / ".claude" / "commands"
        assert not commands_dir.exists()

        adapter.create_command(name="test", description="Test", content="Content")

        assert commands_dir.exists()
        assert commands_dir.is_dir()

    def test_create_command_writes_content(self, adapter, tmp_path):
        """Test that command file contains correct content."""
        result = adapter.create_command(
            name="test",
            description="Description",
            content="Implementation",
        )

        content = result.path.read_text()
        assert "# /test" in content
        assert "Description" in content
        assert "Implementation" in content

    def test_create_command_invalid_name_fails(self, adapter):
        """Test that command creation fails with invalid name."""
        with pytest.raises(InvalidNameError):
            adapter.create_command(
                name="invalid!command",
                description="Test",
                content="Content",
            )


class TestAgentCreation:
    """Test suite for agent creation functionality."""

    @pytest.fixture
    def adapter(self, tmp_path):
        """Fixture providing a ClaudeAdapter with temp directory."""
        scope_config = ScopeConfig(
            path=tmp_path / ".claude",
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )
        return ClaudeAdapter(scope_config)

    def test_create_agent_success(self, adapter, tmp_path):
        """Test successful agent creation."""
        result = adapter.create_agent(
            name="test-agent",
            description="A test agent",
            content="Agent implementation",
        )

        assert result.success is True
        assert result.element_type == ElementType.AGENT
        assert result.path == tmp_path / ".claude" / "agents" / "test-agent.md"
        assert result.path.exists()

    def test_create_agent_creates_directory(self, adapter, tmp_path):
        """Test that agent creation creates agents/ directory if needed."""
        agents_dir = tmp_path / ".claude" / "agents"
        assert not agents_dir.exists()

        adapter.create_agent(name="test", description="Test", content="Content")

        assert agents_dir.exists()
        assert agents_dir.is_dir()

    def test_create_agent_writes_content(self, adapter, tmp_path):
        """Test that agent file contains correct content."""
        result = adapter.create_agent(
            name="test",
            description="Description",
            content="Implementation",
        )

        content = result.path.read_text()
        assert "# test Agent" in content
        assert "Description" in content
        assert "Implementation" in content

    def test_create_agent_invalid_name_fails(self, adapter):
        """Test that agent creation fails with invalid name."""
        with pytest.raises(InvalidNameError):
            adapter.create_agent(
                name="invalid agent!",
                description="Test",
                content="Content",
            )


class TestErrorHandling:
    """Test suite for error handling."""

    @pytest.fixture
    def adapter(self, tmp_path):
        """Fixture providing a ClaudeAdapter with temp directory."""
        scope_config = ScopeConfig(
            path=tmp_path / ".claude",
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )
        return ClaudeAdapter(scope_config)

    def test_directory_creation_failure(self, adapter, tmp_path):
        """Test handling of directory creation failures."""
        # Make the scope path read-only
        scope_path = tmp_path / ".claude"
        scope_path.mkdir()
        scope_path.chmod(0o444)

        try:
            with pytest.raises(CreationError, match="Failed to create directory"):
                adapter.create_skill(name="test", description="Test", content="Content")
        finally:
            # Restore permissions for cleanup
            scope_path.chmod(0o755)

    def test_file_write_failure(self, adapter, tmp_path):
        """Test handling of file write failures."""
        # Create skills directory but make it read-only
        skills_dir = tmp_path / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        skills_dir.chmod(0o444)

        try:
            with pytest.raises(CreationError, match="Failed to write"):
                adapter.create_skill(name="test", description="Test", content="Content")
        finally:
            # Restore permissions for cleanup
            skills_dir.chmod(0o755)


class TestHelperMethods:
    """Test suite for helper methods."""

    @pytest.fixture
    def adapter(self, tmp_path):
        """Fixture providing a ClaudeAdapter with temp directory."""
        scope_config = ScopeConfig(
            path=tmp_path / ".claude",
            type=ScopeType.GLOBAL,
            precedence=3,
            exists=True,
        )
        return ClaudeAdapter(scope_config)

    def test_ensure_directory_exists_creates_dir(self, adapter, tmp_path):
        """Test that _ensure_directory_exists creates directories."""
        test_dir = tmp_path / "new" / "nested" / "directory"
        assert not test_dir.exists()

        adapter._ensure_directory_exists(test_dir)

        assert test_dir.exists()
        assert test_dir.is_dir()

    def test_ensure_directory_exists_idempotent(self, adapter, tmp_path):
        """Test that _ensure_directory_exists is idempotent."""
        test_dir = tmp_path / "test"
        test_dir.mkdir()

        # Should not raise even if directory already exists
        adapter._ensure_directory_exists(test_dir)

        assert test_dir.exists()

    def test_generate_skill_content(self, adapter):
        """Test skill content generation."""
        content = adapter._generate_skill_content("test-skill", "Description", "Implementation")

        assert "# test-skill" in content
        assert "Description" in content
        assert "Implementation" in content

    def test_generate_command_content(self, adapter):
        """Test command content generation."""
        content = adapter._generate_command_content("test-command", "Description", "Implementation")

        assert "# /test-command" in content
        assert "Description" in content
        assert "Implementation" in content

    def test_generate_agent_content(self, adapter):
        """Test agent content generation."""
        content = adapter._generate_agent_content("test-agent", "Description", "Implementation")

        assert "# test-agent Agent" in content
        assert "Description" in content
        assert "Implementation" in content
