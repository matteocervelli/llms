"""
Tests for agent_builder validator.

Tests the security-first validation for agent names, descriptions,
model selection, and file paths.
"""

import pytest
from pathlib import Path

from src.tools.agent_builder.validator import AgentValidator
from src.tools.agent_builder.models import ModelType


class TestAgentNameValidation:
    """Tests for agent name validation."""

    def test_valid_names(self):
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
            is_valid, message = AgentValidator.validate_agent_name(name)
            assert is_valid, f"Failed for '{name}': {message}"
            assert message == "Valid agent name"

    def test_invalid_empty(self):
        """Test empty name is invalid."""
        is_valid, message = AgentValidator.validate_agent_name("")
        assert not is_valid
        assert "cannot be empty" in message

    def test_invalid_too_long(self):
        """Test name exceeding 64 characters is invalid."""
        is_valid, message = AgentValidator.validate_agent_name("a" * 65)
        assert not is_valid
        assert "1-64 characters" in message

    def test_invalid_uppercase(self):
        """Test uppercase letters are invalid."""
        is_valid, message = AgentValidator.validate_agent_name("TestAgent")
        assert not is_valid
        assert "lowercase" in message

    def test_invalid_spaces(self):
        """Test spaces are invalid."""
        is_valid, message = AgentValidator.validate_agent_name("test agent")
        assert not is_valid
        assert "lowercase" in message

    def test_invalid_special_characters(self):
        """Test special characters are invalid."""
        invalid_names = [
            "test_agent",
            "test.agent",
            "test@agent",
            "test!",
            "test$agent",
        ]

        for name in invalid_names:
            is_valid, message = AgentValidator.validate_agent_name(name)
            assert not is_valid, f"Should fail for '{name}'"
            assert "lowercase" in message

    def test_invalid_leading_hyphen(self):
        """Test leading hyphen is invalid."""
        is_valid, message = AgentValidator.validate_agent_name("-test")
        assert not is_valid
        assert "cannot start or end with hyphen" in message

    def test_invalid_trailing_hyphen(self):
        """Test trailing hyphen is invalid."""
        is_valid, message = AgentValidator.validate_agent_name("test-")
        assert not is_valid
        assert "cannot start or end with hyphen" in message

    def test_invalid_consecutive_hyphens(self):
        """Test consecutive hyphens are invalid."""
        is_valid, message = AgentValidator.validate_agent_name("test--agent")
        assert not is_valid
        assert "consecutive hyphens" in message

    def test_invalid_path_traversal(self):
        """Test path traversal attempts are invalid."""
        invalid_names = [
            "../test",
            "test/../agent",
            "../../etc/passwd",
            "test/agent",
            "test\\agent",
        ]

        for name in invalid_names:
            is_valid, message = AgentValidator.validate_agent_name(name)
            assert not is_valid, f"Should fail for '{name}'"
            assert "path" in message.lower()


class TestDescriptionValidation:
    """Tests for description validation."""

    def test_valid_descriptions(self):
        """Test valid descriptions with usage context."""
        valid_descriptions = [
            "Use for testing agents",
            "Agent for processing data",
            "Helper when working with files",
            "Use during development if needed",
            "For handling complex workflows",
            "When you need to process PDFs",
        ]

        for desc in valid_descriptions:
            is_valid, message = AgentValidator.validate_description(desc)
            assert is_valid, f"Failed for '{desc}': {message}"
            assert message == "Valid description"

    def test_invalid_empty(self):
        """Test empty description is invalid."""
        is_valid, message = AgentValidator.validate_description("")
        assert not is_valid
        assert "cannot be empty" in message

    def test_invalid_whitespace_only(self):
        """Test whitespace-only description is invalid."""
        is_valid, message = AgentValidator.validate_description("   ")
        assert not is_valid
        assert "cannot be empty" in message

    def test_invalid_too_long(self):
        """Test description exceeding 1024 characters is invalid."""
        is_valid, message = AgentValidator.validate_description("a" * 1025)
        assert not is_valid
        assert "1024 characters" in message

    def test_invalid_no_usage_context(self):
        """Test description without usage context is invalid."""
        invalid_descriptions = [
            "This is an agent.",
            "Test agent.",
            "An agent that does things.",
        ]

        for desc in invalid_descriptions:
            is_valid, message = AgentValidator.validate_description(desc)
            assert not is_valid, f"Should fail for '{desc}'"
            assert "should include when" in message


class TestModelValidation:
    """Tests for model validation."""

    def test_valid_models(self):
        """Test all defined models are valid."""
        for model in ModelType:
            is_valid, message = AgentValidator.validate_model(model.value)
            assert is_valid, f"Failed for '{model.value}': {message}"
            assert "Valid model" in message

    def test_invalid_model(self):
        """Test invalid model names."""
        invalid_models = [
            "gpt-4",
            "claude-2",
            "invalid-model",
        ]

        for model in invalid_models:
            is_valid, message = AgentValidator.validate_model(model)
            assert not is_valid, f"Should fail for '{model}'"
            assert "Invalid model" in message

    def test_invalid_empty_model(self):
        """Test empty model is invalid."""
        is_valid, message = AgentValidator.validate_model("")
        assert not is_valid
        assert "cannot be empty" in message


class TestTemplateNameValidation:
    """Tests for template name validation."""

    def test_valid_template_names(self):
        """Test valid template names."""
        valid_names = [
            "basic",
            "advanced",
            "my_template",
            "template-v2",
            "template123",
        ]

        for name in valid_names:
            is_valid, message = AgentValidator.validate_template_name(name)
            assert is_valid, f"Failed for '{name}': {message}"
            assert message == "Valid template name"

    def test_invalid_empty(self):
        """Test empty template name is invalid."""
        is_valid, message = AgentValidator.validate_template_name("")
        assert not is_valid
        assert "cannot be empty" in message

    def test_invalid_path_traversal(self):
        """Test path traversal is invalid."""
        invalid_names = [
            "../template",
            "../../etc/passwd",
            "template/../test",
            "template/test",
            "template\\test",
        ]

        for name in invalid_names:
            is_valid, message = AgentValidator.validate_template_name(name)
            assert not is_valid, f"Should fail for '{name}'"
            assert "path separators" in message


class TestPathSecurityValidation:
    """Tests for path security validation."""

    def test_valid_path_within_base(self, tmp_path):
        """Test valid path within base directory."""
        base_dir = tmp_path / "agents"
        base_dir.mkdir()
        agent_path = base_dir / "test-agent"

        is_valid, message = AgentValidator.validate_path_security(agent_path, base_dir)
        assert is_valid
        assert message == "Path is secure"

    def test_invalid_path_outside_base(self, tmp_path):
        """Test path outside base directory is invalid."""
        base_dir = tmp_path / "agents"
        base_dir.mkdir()
        outside_path = tmp_path / "other" / "test-agent"

        is_valid, message = AgentValidator.validate_path_security(outside_path, base_dir)
        assert not is_valid
        assert "outside allowed directory" in message

    def test_invalid_path_traversal_attempt(self, tmp_path):
        """Test path traversal attempt is detected."""
        base_dir = tmp_path / "agents"
        base_dir.mkdir()
        # Attempt to traverse up and then down
        evil_path = base_dir / ".." / ".." / "etc" / "passwd"

        is_valid, message = AgentValidator.validate_path_security(evil_path, base_dir)
        assert not is_valid
        assert "outside" in message.lower()


class TestFrontmatterValidation:
    """Tests for frontmatter key validation."""

    def test_valid_frontmatter_keys(self):
        """Test valid frontmatter keys."""
        valid_frontmatter = {
            "custom_field": "value",
            "version": "1.0",
            "author": "test",
            "created-date": "2024-01-01",
        }

        is_valid, message = AgentValidator.validate_frontmatter_keys(valid_frontmatter)
        assert is_valid
        assert message == "Valid frontmatter keys"

    def test_empty_frontmatter(self):
        """Test empty frontmatter is valid."""
        is_valid, message = AgentValidator.validate_frontmatter_keys({})
        assert is_valid
        assert "No frontmatter" in message

    def test_none_frontmatter(self):
        """Test None frontmatter is valid."""
        is_valid, message = AgentValidator.validate_frontmatter_keys(None)
        assert is_valid
        assert "No frontmatter" in message

    def test_invalid_frontmatter_keys(self):
        """Test invalid frontmatter keys."""
        invalid_frontmatter = {
            "invalid key": "value",  # Space
            "key@value": "test",  # Special char
            "key.value": "test",  # Dot
        }

        is_valid, message = AgentValidator.validate_frontmatter_keys(invalid_frontmatter)
        assert not is_valid
        assert "Invalid frontmatter keys" in message


class TestStringSanitization:
    """Tests for string sanitization."""

    def test_sanitize_clean_string(self):
        """Test sanitizing a clean string."""
        result = AgentValidator.sanitize_string("Hello World")
        assert result == "Hello World"

    def test_sanitize_control_characters(self):
        """Test removing control characters."""
        result = AgentValidator.sanitize_string("Hello\x00World\x01Test")
        assert result == "HelloWorldTest"

    def test_sanitize_whitespace_normalization(self):
        """Test normalizing whitespace."""
        result = AgentValidator.sanitize_string("Hello   \n  World")
        assert result == "Hello World"

    def test_sanitize_max_length(self):
        """Test trimming to max length."""
        result = AgentValidator.sanitize_string("a" * 100, max_length=10)
        assert len(result) == 10
        assert result == "a" * 10

    def test_sanitize_empty_string(self):
        """Test sanitizing empty string."""
        result = AgentValidator.sanitize_string("")
        assert result == ""


class TestFilenameValidation:
    """Tests for filename validation."""

    def test_valid_filenames(self):
        """Test valid filenames."""
        valid_filenames = [
            "AGENT.md",
            "test-agent.md",
            "agent_v2.md",
            "123.md",
        ]

        for filename in valid_filenames:
            is_valid, message = AgentValidator.is_safe_filename(filename)
            assert is_valid, f"Failed for '{filename}': {message}"
            assert message == "Safe filename"

    def test_invalid_empty(self):
        """Test empty filename is invalid."""
        is_valid, message = AgentValidator.is_safe_filename("")
        assert not is_valid
        assert "cannot be empty" in message

    def test_invalid_path_traversal(self):
        """Test path traversal is invalid."""
        invalid_filenames = [
            "../test.md",
            "../../etc/passwd",
            "test/../file.md",
            "path/to/file.md",
            "path\\to\\file.md",
        ]

        for filename in invalid_filenames:
            is_valid, message = AgentValidator.is_safe_filename(filename)
            assert not is_valid, f"Should fail for '{filename}'"
            assert "path traversal" in message.lower()

    def test_invalid_reserved_names(self):
        """Test Windows reserved names are invalid."""
        reserved_names = ["CON", "PRN", "AUX", "NUL", "COM1", "LPT1"]

        for name in reserved_names:
            is_valid, message = AgentValidator.is_safe_filename(f"{name}.md")
            assert not is_valid, f"Should fail for '{name}'"
            assert "reserved name" in message.lower()

    def test_invalid_special_characters(self):
        """Test special characters are invalid."""
        invalid_filenames = [
            "test*.md",
            "test?.md",
            "test|.md",
            "test<.md",
            "test>.md",
        ]

        for filename in invalid_filenames:
            is_valid, message = AgentValidator.is_safe_filename(filename)
            assert not is_valid, f"Should fail for '{filename}'"
            assert "invalid characters" in message.lower()
