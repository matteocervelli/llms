"""
Tests for command builder tool.

Comprehensive test suite for models, validator, builder, catalog, and templates.
Target: 80%+ coverage.
"""

import json
import tempfile
from pathlib import Path
from uuid import UUID

import pytest

from src.tools.command_builder.builder import CommandBuilder
from src.tools.command_builder.catalog import CatalogManager
from src.tools.command_builder.exceptions import (
    CatalogError,
    CommandExistsError,
    SecurityError,
    TemplateError,
    ValidationError,
)
from src.tools.command_builder.models import (
    CommandCatalog,
    CommandCatalogEntry,
    CommandConfig,
    CommandParameter,
    ParameterType,
    ScopeType,
)
from src.tools.command_builder.templates import TemplateManager
from src.tools.command_builder.validator import Validator


# ============================================================================
# Test Models
# ============================================================================


class TestCommandParameter:
    """Test CommandParameter model."""

    def test_valid_parameter(self):
        """Test creating valid parameter."""
        param = CommandParameter(
            name="my_param",
            type=ParameterType.STRING,
            description="Test parameter",
            required=True,
        )
        assert param.name == "my_param"
        assert param.type == ParameterType.STRING
        assert param.required is True

    def test_parameter_with_choices(self):
        """Test parameter with choices."""
        param = CommandParameter(
            name="choice_param",
            type=ParameterType.CHOICE,
            description="Choice parameter",
            choices=["option1", "option2"],
        )
        assert param.choices == ["option1", "option2"]

    def test_choice_type_requires_choices(self):
        """Test that choice type requires choices."""
        with pytest.raises(ValueError, match="choices must be provided"):
            CommandParameter(
                name="bad_choice",
                type=ParameterType.CHOICE,
                description="Bad choice",
            )

    def test_invalid_parameter_name(self):
        """Test invalid parameter name."""
        with pytest.raises(ValueError):
            CommandParameter(
                name="Invalid-Name",  # Hyphens not allowed
                type=ParameterType.STRING,
                description="Test",
            )


class TestCommandConfig:
    """Test CommandConfig model."""

    def test_valid_config(self):
        """Test creating valid command configuration."""
        config = CommandConfig(
            name="test-command",
            description="Test command",
            scope=ScopeType.PROJECT,
        )
        assert config.name == "test-command"
        assert config.scope == ScopeType.PROJECT

    def test_invalid_command_name(self):
        """Test invalid command name validation."""
        with pytest.raises(ValueError):
            CommandConfig(
                name="invalid_name",  # Underscores not allowed
                description="Test",
            )

    def test_command_name_length_validation(self):
        """Test command name length limits."""
        with pytest.raises(ValueError, match="at least 2 characters"):
            CommandConfig(name="a", description="Test")

        with pytest.raises(ValueError, match="at most 50 characters"):
            CommandConfig(name="a" * 51, description="Test")

    def test_consecutive_hyphens_not_allowed(self):
        """Test that consecutive hyphens are not allowed."""
        with pytest.raises(ValueError, match="consecutive hyphens"):
            CommandConfig(name="test--command", description="Test")


class TestCommandCatalog:
    """Test CommandCatalog model."""

    def test_empty_catalog(self):
        """Test creating empty catalog."""
        catalog = CommandCatalog()
        assert len(catalog.commands) == 0
        assert catalog.schema_version == "1.0"

    def test_add_command(self):
        """Test adding command to catalog."""
        catalog = CommandCatalog()
        entry = CommandCatalogEntry(
            name="test-cmd",
            description="Test",
            scope=ScopeType.PROJECT,
            path="/path/to/test-cmd.md",
        )
        catalog.add_command(entry)
        assert len(catalog.commands) == 1

    def test_get_by_name(self):
        """Test getting command by name."""
        catalog = CommandCatalog()
        entry = CommandCatalogEntry(
            name="test-cmd",
            description="Test",
            scope=ScopeType.PROJECT,
            path="/path/to/test-cmd.md",
        )
        catalog.add_command(entry)

        found = catalog.get_by_name("test-cmd")
        assert found is not None
        assert found.name == "test-cmd"

    def test_search_commands(self):
        """Test searching commands."""
        catalog = CommandCatalog()
        entry1 = CommandCatalogEntry(
            name="deploy-app",
            description="Deploy application",
            scope=ScopeType.PROJECT,
            path="/path/to/deploy-app.md",
        )
        entry2 = CommandCatalogEntry(
            name="test-app",
            description="Test application",
            scope=ScopeType.PROJECT,
            path="/path/to/test-app.md",
        )
        catalog.add_command(entry1)
        catalog.add_command(entry2)

        results = catalog.search(query="deploy")
        assert len(results) == 1
        assert results[0].name == "deploy-app"


# ============================================================================
# Test Validator
# ============================================================================


class TestValidator:
    """Test Validator class."""

    def test_validate_command_name_valid(self):
        """Test valid command name validation."""
        is_valid, error = Validator.validate_command_name("my-command")
        assert is_valid is True
        assert error == ""

    def test_validate_command_name_invalid(self):
        """Test invalid command name patterns."""
        test_cases = [
            ("", "cannot be empty"),
            ("a", "at least 2 characters"),
            ("a" * 51, "at most 50 characters"),
            ("My-Command", "lowercase"),
            ("my_command", "slug format"),
            ("my--command", "consecutive hyphens"),
            ("-mycommand", "start and end with alphanumeric"),
            ("mycommand-", "start and end with alphanumeric"),
        ]

        for name, expected_error in test_cases:
            is_valid, error = Validator.validate_command_name(name)
            assert is_valid is False, f"Expected {name} to be invalid"
            assert expected_error in error.lower()

    def test_validate_command_name_reserved(self):
        """Test reserved command names."""
        reserved = ["help", "version", "list"]
        for name in reserved:
            is_valid, error = Validator.validate_command_name(name)
            assert is_valid is False
            assert "reserved" in error.lower()

    def test_validate_bash_command_safe(self):
        """Test safe bash commands."""
        safe_commands = [
            "git status",
            "npm test",
            "python main.py",
            "pytest tests/",
        ]

        for cmd in safe_commands:
            is_safe, error, warnings = Validator.validate_bash_command(cmd)
            assert is_safe is True
            assert error == ""

    def test_validate_bash_command_dangerous(self):
        """Test dangerous bash commands."""
        dangerous_commands = [
            "rm -rf /",
            "dd if=/dev/zero of=/dev/sda",
            ":(){ :|:& };:",  # Fork bomb
        ]

        for cmd in dangerous_commands:
            is_safe, error, warnings = Validator.validate_bash_command(cmd)
            assert is_safe is False
            assert "dangerous" in error.lower() or "not allowed" in error.lower()

    def test_validate_bash_command_warnings(self):
        """Test bash commands that generate warnings."""
        cmd = "ls | grep test"
        is_safe, error, warnings = Validator.validate_bash_command(cmd)
        assert is_safe is True
        assert len(warnings) > 0

    def test_validate_file_reference_valid(self):
        """Test valid file reference."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            is_valid, error = Validator.validate_file_reference("README.md", project_root)
            assert is_valid is True

    def test_validate_file_reference_path_traversal(self):
        """Test path traversal prevention."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            is_valid, error = Validator.validate_file_reference("../etc/passwd", project_root)
            assert is_valid is False
            assert "traversal" in error.lower()

    def test_validate_template_name_valid(self):
        """Test valid template names."""
        valid_names = ["basic", "with-bash", "my_template", "template123"]
        for name in valid_names:
            is_valid, error = Validator.validate_template_name(name)
            assert is_valid is True

    def test_validate_template_name_invalid(self):
        """Test invalid template names."""
        invalid_names = [
            "../../etc/passwd",  # Path traversal
            "template/name",  # Path separator
            "template\\name",  # Windows path separator
        ]
        for name in invalid_names:
            is_valid, error = Validator.validate_template_name(name)
            assert is_valid is False

    def test_parse_command_name_with_context(self):
        """Test parsing command name with context prefix."""
        context, obj, action, modifier = Validator.parse_command_name("cc-command-create")
        assert context == "cc"
        assert obj == "command"
        assert action == "create"
        assert modifier == ""

    def test_parse_command_name_without_context(self):
        """Test parsing command name without context prefix."""
        # Use a name that doesn't start with a known context
        context, obj, action, modifier = Validator.parse_command_name("task-create")
        assert context == ""
        assert obj == "task"
        assert action == "create"
        assert modifier == ""

    def test_parse_command_name_with_modifier(self):
        """Test parsing command name with modifier."""
        context, obj, action, modifier = Validator.parse_command_name("pr-analyze-failure")
        assert context == "pr"
        assert obj == "analyze"
        assert action == "failure"
        assert modifier == ""

    def test_parse_command_name_invalid(self):
        """Test parsing invalid command names."""
        # Single part
        context, obj, action, modifier = Validator.parse_command_name("command")
        assert context == ""
        assert obj == ""
        assert action == ""

        # Context only
        context, obj, action, modifier = Validator.parse_command_name("cc-command")
        assert context == "cc"
        assert obj == ""
        assert action == ""

    def test_suggest_naming_improvements_single_part(self):
        """Test suggestions for single-part names."""
        suggestions = Validator.suggest_naming_improvements("command")
        assert len(suggestions) > 0
        assert any("action verb" in s.lower() for s in suggestions)

    def test_suggest_naming_improvements_wrong_order(self):
        """Test suggestions for action-object order."""
        suggestions = Validator.suggest_naming_improvements("create-command")
        assert len(suggestions) > 0
        assert any("command-create" in s for s in suggestions)

    def test_validate_naming_convention_compliant_with_context(self):
        """Test compliant naming with context."""
        is_valid, error, warnings = Validator.validate_naming_convention(
            "cc-command-create", strict=False
        )
        assert is_valid is True
        assert error == ""
        assert any("✓" in w for w in warnings)  # Should have parsed info

    def test_validate_naming_convention_compliant_without_context(self):
        """Test compliant naming without context."""
        is_valid, error, warnings = Validator.validate_naming_convention(
            "feature-implement", strict=False
        )
        assert is_valid is True
        assert error == ""

    def test_validate_naming_convention_non_compliant_permissive(self):
        """Test non-compliant naming in permissive mode."""
        is_valid, error, warnings = Validator.validate_naming_convention(
            "create-command", strict=False
        )
        assert is_valid is True  # Permissive allows it
        assert error == ""
        assert len(warnings) > 0  # But warns

    def test_validate_naming_convention_non_compliant_strict(self):
        """Test non-compliant naming in strict mode."""
        is_valid, error, warnings = Validator.validate_naming_convention("command", strict=True)
        assert is_valid is False  # Strict blocks it
        assert "must follow" in error.lower()

    def test_validate_naming_convention_invalid_context_permissive(self):
        """Test invalid context in permissive mode."""
        # xyz is not in ALLOWED_CONTEXTS, but xyz-command-create still parses correctly
        # because xyz is not recognized as a context, so "xyz" becomes the object
        is_valid, error, warnings = Validator.validate_naming_convention(
            "xyz-command-create", strict=False
        )
        assert is_valid is True  # Permissive allows it
        # Since "xyz" is not in ALLOWED_CONTEXTS, it's treated as an object, not context
        # So the parsing will be: context="", obj="xyz", action="command", modifier="create"
        assert len(warnings) > 0  # Should have parsing info

    def test_validate_naming_convention_invalid_context_strict(self):
        """Test a name that would fail strict validation."""
        # A name with only one part should fail in strict mode
        is_valid, error, warnings = Validator.validate_naming_convention("command", strict=True)
        assert is_valid is False  # Strict blocks it
        assert "must follow" in error.lower()

    def test_validate_naming_convention_common_patterns(self):
        """Test validation of common naming patterns."""
        good_names = [
            "cc-command-create",
            "cc-command-improve",
            "feature-implement",
            "issue-fix",
            "gh-milestone-create",
            "pr-analyze-failure",
            "code-analyze-quality",
            "infrastructure-setup",
        ]

        for name in good_names:
            is_valid, error, warnings = Validator.validate_naming_convention(name, strict=False)
            assert is_valid is True, f"{name} should be valid"

    def test_validate_naming_convention_with_custom_contexts(self):
        """Test validation with custom allowed contexts."""
        is_valid, error, warnings = Validator.validate_naming_convention(
            "custom-tool-run", strict=False, allowed_contexts=["cc", "gh", "custom"]
        )
        assert is_valid is True


# ============================================================================
# Test Template Manager
# ============================================================================


class TestTemplateManager:
    """Test TemplateManager class."""

    def test_list_templates(self):
        """Test listing templates."""
        manager = TemplateManager()
        templates = manager.list_templates()
        assert "basic" in templates
        assert "with_bash" in templates
        assert "with_files" in templates
        assert "advanced" in templates

    def test_template_exists(self):
        """Test checking template existence."""
        manager = TemplateManager()
        assert manager.template_exists("basic") is True
        assert manager.template_exists("nonexistent") is False

    def test_load_template(self):
        """Test loading a template."""
        manager = TemplateManager()
        template = manager.load_template("basic")
        assert template is not None

    def test_load_nonexistent_template(self):
        """Test loading nonexistent template."""
        manager = TemplateManager()
        with pytest.raises(TemplateError, match="not found"):
            manager.load_template("nonexistent")

    def test_render_template(self):
        """Test rendering a template."""
        manager = TemplateManager()
        config = CommandConfig(
            name="test-command",
            description="Test command",
        )
        content = manager.render_template("basic", config)
        assert "test-command" in content
        assert "Test command" in content
        assert content.startswith("---")  # Frontmatter


# ============================================================================
# Test Command Builder
# ============================================================================


class TestCommandBuilder:
    """Test CommandBuilder class."""

    def test_get_scope_path_global(self):
        """Test getting global scope path."""
        builder = CommandBuilder()
        path = builder.get_scope_path(ScopeType.GLOBAL)
        assert path == Path.home() / ".claude" / "commands"

    def test_get_scope_path_project(self):
        """Test getting project scope path."""
        builder = CommandBuilder()
        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            path = builder.get_scope_path(ScopeType.PROJECT, project_root)
            assert path == project_root / ".claude" / "commands"

    def test_build_command(self):
        """Test building a command."""
        builder = CommandBuilder()
        config = CommandConfig(
            name="test-cmd",
            description="Test command",
            scope=ScopeType.PROJECT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            command_path, content = builder.build_command(config, project_root)

            assert command_path.exists()
            assert command_path.name == "test-cmd.md"
            assert "test-cmd" in content

    def test_build_command_already_exists(self):
        """Test building command that already exists."""
        builder = CommandBuilder()
        config = CommandConfig(
            name="test-cmd",
            description="Test command",
            scope=ScopeType.PROJECT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)

            # Create first time
            builder.build_command(config, project_root)

            # Try to create again without overwrite
            with pytest.raises(CommandExistsError):
                builder.build_command(config, project_root, overwrite=False)

    def test_validate_command_file(self):
        """Test validating command file."""
        builder = CommandBuilder()
        config = CommandConfig(
            name="test-cmd",
            description="Test command",
            scope=ScopeType.PROJECT,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            project_root = Path(tmpdir)
            command_path, _ = builder.build_command(config, project_root)

            is_valid, error = builder.validate_command_file(command_path)
            assert is_valid is True
            assert error == ""


# ============================================================================
# Test Catalog Manager
# ============================================================================


class TestCatalogManager:
    """Test CatalogManager class."""

    def test_create_catalog(self):
        """Test creating catalog file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            catalog_path = Path(tmpdir) / "commands.json"
            manager = CatalogManager(catalog_path)
            assert catalog_path.exists()

    def test_add_command(self):
        """Test adding command to catalog."""
        with tempfile.TemporaryDirectory() as tmpdir:
            catalog_path = Path(tmpdir) / "commands.json"
            manager = CatalogManager(catalog_path)

            entry = CommandCatalogEntry(
                name="test-cmd",
                description="Test",
                scope=ScopeType.PROJECT,
                path="/path/to/test-cmd.md",
            )
            manager.add_command(entry)

            # Verify command was added
            found = manager.get_command(name="test-cmd")
            assert found is not None
            assert found.name == "test-cmd"

    def test_add_duplicate_command(self):
        """Test adding duplicate command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            catalog_path = Path(tmpdir) / "commands.json"
            manager = CatalogManager(catalog_path)

            entry = CommandCatalogEntry(
                name="test-cmd",
                description="Test",
                scope=ScopeType.PROJECT,
                path="/path/to/test-cmd.md",
            )
            manager.add_command(entry)

            # Try to add again
            with pytest.raises(CatalogError, match="already exists"):
                manager.add_command(entry)

    def test_list_commands(self):
        """Test listing commands."""
        with tempfile.TemporaryDirectory() as tmpdir:
            catalog_path = Path(tmpdir) / "commands.json"
            manager = CatalogManager(catalog_path)

            entry1 = CommandCatalogEntry(
                name="cmd1",
                description="Test 1",
                scope=ScopeType.PROJECT,
                path="/path/to/cmd1.md",
            )
            entry2 = CommandCatalogEntry(
                name="cmd2",
                description="Test 2",
                scope=ScopeType.GLOBAL,
                path="/path/to/cmd2.md",
            )
            manager.add_command(entry1)
            manager.add_command(entry2)

            all_commands = manager.list_commands()
            assert len(all_commands) == 2

            project_commands = manager.list_commands(scope=ScopeType.PROJECT)
            assert len(project_commands) == 1
            assert project_commands[0].name == "cmd1"

    def test_get_catalog_stats(self):
        """Test getting catalog statistics."""
        with tempfile.TemporaryDirectory() as tmpdir:
            catalog_path = Path(tmpdir) / "commands.json"
            manager = CatalogManager(catalog_path)

            entry = CommandCatalogEntry(
                name="test-cmd",
                description="Test",
                scope=ScopeType.PROJECT,
                path="/path/to/test-cmd.md",
                metadata={"has_parameters": True, "has_bash": False},
            )
            manager.add_command(entry)

            stats = manager.get_catalog_stats()
            assert stats["total_commands"] == 1
            assert stats["by_scope"]["project"] == 1
            assert stats["with_parameters"] == 1
            assert stats["with_bash"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src/tools/command_builder", "--cov-report=term-missing"])
