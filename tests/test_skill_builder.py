"""
Tests for skill_builder tool - Phase 3: Builder

Comprehensive test suite for SkillBuilder class.
Target: 20+ tests, 80%+ coverage, < 50ms skill creation performance.
"""

import os
import shutil
import tempfile
import time
from pathlib import Path

import pytest

from src.core.scope_manager import ScopeManager
from src.tools.skill_builder.builder import SkillBuilder
from src.tools.skill_builder.exceptions import (
    SkillBuilderError,
    SkillExistsError,
    TemplateError,
)
from src.tools.skill_builder.models import SkillConfig, ScopeType
from src.tools.skill_builder.templates import TemplateManager


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def builder():
    """Create a SkillBuilder instance for tests."""
    return SkillBuilder()


@pytest.fixture
def valid_config():
    """Create a valid SkillConfig for tests."""
    return SkillConfig(
        name="test-skill",
        description="Test skill for unit testing. Use when running tests.",
        scope=ScopeType.PROJECT,
        template="basic",
    )


# ============================================================================
# Test SkillBuilder - get_scope_path()
# ============================================================================


class TestGetScopePath:
    """Test SkillBuilder.get_scope_path() method."""

    def test_global_scope_path(self, builder):
        """Test getting global scope path."""
        path = builder.get_scope_path(ScopeType.GLOBAL)
        assert path == Path.home() / ".claude" / "skills"
        assert path.exists()
        # Verify permissions
        assert oct(os.stat(path).st_mode)[-3:] == "755"

    def test_project_scope_path(self, builder, temp_dir):
        """Test getting project scope path."""
        path = builder.get_scope_path(ScopeType.PROJECT, temp_dir)
        assert path == temp_dir / ".claude" / "skills"
        assert path.exists()
        # Verify permissions
        assert oct(os.stat(path).st_mode)[-3:] == "755"

    def test_local_scope_path(self, builder, temp_dir):
        """Test getting local scope path."""
        path = builder.get_scope_path(ScopeType.LOCAL, temp_dir)
        assert path == temp_dir / ".claude" / "skills"
        assert path.exists()
        # Same directory as project, but tracked differently in catalog
        assert oct(os.stat(path).st_mode)[-3:] == "755"

    def test_invalid_scope_type(self, builder):
        """Test with invalid scope type."""
        with pytest.raises(SkillBuilderError, match="Unknown scope type"):
            builder.get_scope_path("invalid_scope")  # type: ignore


# ============================================================================
# Test SkillBuilder - build_skill()
# ============================================================================


class TestBuildSkill:
    """Test SkillBuilder.build_skill() method."""

    def test_successful_skill_creation_project_scope(self, builder, temp_dir, valid_config):
        """Test successful skill creation in project scope."""
        skill_path, content = builder.build_skill(valid_config, temp_dir)

        # Verify skill directory created
        assert skill_path.exists()
        assert skill_path.is_dir()
        assert skill_path.name == "test-skill"

        # Verify SKILL.md exists
        skill_file = skill_path / "SKILL.md"
        assert skill_file.exists()
        assert skill_file.is_file()

        # Verify content
        assert "test-skill" in content
        assert "Test skill for unit testing" in content
        assert content.startswith("---")  # Has frontmatter

        # Verify permissions
        assert oct(os.stat(skill_path).st_mode)[-3:] == "755"
        assert oct(os.stat(skill_file).st_mode)[-3:] == "644"

    def test_successful_skill_creation_global_scope(self, builder):
        """Test successful skill creation in global scope."""
        config = SkillConfig(
            name="global-test-skill",
            description="Global test skill. Use when testing globally.",
            scope=ScopeType.GLOBAL,
            template="basic",
        )

        try:
            skill_path, content = builder.build_skill(config)

            # Verify creation
            assert skill_path.exists()
            assert skill_path.is_dir()
            assert (skill_path / "SKILL.md").exists()

            # Cleanup
            shutil.rmtree(skill_path)
        except Exception:
            # Cleanup in case of failure
            global_skills = Path.home() / ".claude" / "skills" / "global-test-skill"
            if global_skills.exists():
                shutil.rmtree(global_skills)
            raise

    def test_duplicate_skill_rejected(self, builder, temp_dir, valid_config):
        """Test that duplicate skill creation is rejected."""
        # Create skill first time
        skill_path, _ = builder.build_skill(valid_config, temp_dir)

        # Try to create again - should fail
        with pytest.raises(SkillExistsError, match="already exists"):
            builder.build_skill(valid_config, temp_dir)

        # Cleanup
        shutil.rmtree(skill_path)

    def test_dry_run_mode(self, builder, temp_dir, valid_config):
        """Test dry-run mode doesn't create files."""
        skill_path, content = builder.build_skill(valid_config, temp_dir, dry_run=True)

        # Verify path is returned but directory NOT created
        assert not skill_path.exists()

        # But content is rendered
        assert "test-skill" in content
        assert content.startswith("---")

    def test_skill_with_allowed_tools(self, builder, temp_dir):
        """Test skill creation with allowed tools."""
        config = SkillConfig(
            name="tools-skill",
            description="Skill with tools. Use when testing tools.",
            scope=ScopeType.PROJECT,
            template="with_tools",
            allowed_tools=["Read", "Bash", "Grep"],
        )

        skill_path, content = builder.build_skill(config, temp_dir)

        # Verify content includes allowed tools
        assert "Read" in content
        assert "Bash" in content
        assert "Grep" in content

        # Cleanup
        shutil.rmtree(skill_path)

    def test_skill_with_custom_content(self, builder, temp_dir):
        """Test skill creation with custom content."""
        custom_instructions = "Custom instructions for this skill."
        config = SkillConfig(
            name="custom-skill",
            description="Custom skill. Use when testing custom content.",
            scope=ScopeType.PROJECT,
            template="basic",
            content=custom_instructions,
        )

        skill_path, content = builder.build_skill(config, temp_dir)

        # Verify custom content is included
        assert custom_instructions in content

        # Cleanup
        shutil.rmtree(skill_path)

    def test_invalid_template_name(self, builder, temp_dir):
        """Test skill creation with invalid template."""
        config = SkillConfig(
            name="bad-template",
            description="Bad template skill. Use when testing errors.",
            scope=ScopeType.PROJECT,
            template="nonexistent-template",
        )

        with pytest.raises((TemplateError, SkillBuilderError), match="[Tt]emplate"):
            builder.build_skill(config, temp_dir)

    def test_path_security_validation(self, builder, temp_dir):
        """Test path security validation prevents traversal."""
        # This should be caught by SkillConfig validation, but test builder too
        config = SkillConfig(
            name="normal-skill",
            description="Normal skill for path testing. Use when testing paths.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        # Build the skill normally first
        skill_path, _ = builder.build_skill(config, temp_dir)

        # Try to manipulate path (simulating attack)
        evil_path = skill_path.parent.parent.parent / "etc" / "passwd"

        # Validator should catch this
        is_valid, error = builder.validate_skill_directory(evil_path)
        assert not is_valid
        assert "not found" in error or "security" in error.lower()

        # Cleanup
        shutil.rmtree(skill_path)


# ============================================================================
# Test SkillBuilder - update_skill()
# ============================================================================


class TestUpdateSkill:
    """Test SkillBuilder.update_skill() method."""

    def test_successful_skill_update(self, builder, temp_dir, valid_config):
        """Test successful skill update."""
        # Create skill first
        skill_path, original_content = builder.build_skill(valid_config, temp_dir)

        # Update with new configuration
        new_config = SkillConfig(
            name="test-skill",
            description="Updated description. Use when testing updates.",
            scope=ScopeType.PROJECT,
            template="with_tools",
            allowed_tools=["Read", "Write"],
        )

        updated_path, new_content = builder.update_skill(skill_path, new_config)

        # Verify update
        assert updated_path == skill_path
        assert new_content != original_content
        assert "Updated description" in new_content
        assert "Read" in new_content
        assert "Write" in new_content

        # Verify file was actually updated
        skill_file = skill_path / "SKILL.md"
        file_content = skill_file.read_text()
        assert file_content == new_content

        # Cleanup
        shutil.rmtree(skill_path)

    def test_update_nonexistent_skill(self, builder, temp_dir):
        """Test updating skill that doesn't exist."""
        config = SkillConfig(
            name="missing-skill",
            description="Missing skill. Use when testing errors.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        nonexistent_path = temp_dir / ".claude" / "skills" / "missing-skill"

        with pytest.raises(SkillBuilderError, match="not found"):
            builder.update_skill(nonexistent_path, config)

    def test_update_file_not_directory(self, builder, temp_dir, valid_config):
        """Test updating when path is a file not directory."""
        # Create a file (not directory)
        fake_skill = temp_dir / "fake-skill.txt"
        fake_skill.write_text("I'm a file, not a directory")

        with pytest.raises(SkillBuilderError, match="not a directory"):
            builder.update_skill(fake_skill, valid_config)


# ============================================================================
# Test SkillBuilder - delete_skill()
# ============================================================================


class TestDeleteSkill:
    """Test SkillBuilder.delete_skill() method."""

    def test_successful_skill_deletion(self, builder, temp_dir, valid_config):
        """Test successful skill deletion."""
        # Create skill
        skill_path, _ = builder.build_skill(valid_config, temp_dir)
        assert skill_path.exists()

        # Delete skill
        success = builder.delete_skill(skill_path)
        assert success is True
        assert not skill_path.exists()

    def test_delete_nonexistent_skill(self, builder, temp_dir):
        """Test deleting skill that doesn't exist."""
        nonexistent_path = temp_dir / ".claude" / "skills" / "nonexistent"
        success = builder.delete_skill(nonexistent_path)
        assert success is False

    def test_delete_file_not_directory(self, builder, temp_dir):
        """Test deleting when path is a file."""
        fake_skill = temp_dir / "fake-skill.txt"
        fake_skill.write_text("I'm a file")

        with pytest.raises(SkillBuilderError, match="not a directory"):
            builder.delete_skill(fake_skill)

    def test_delete_validates_parent_directory(self, builder, temp_dir):
        """Test that delete validates parent directory is 'skills'."""
        # Create a directory outside skills/
        wrong_location = temp_dir / "wrong" / "test-skill"
        wrong_location.mkdir(parents=True)

        with pytest.raises(SkillBuilderError, match="parent directory must be 'skills'"):
            builder.delete_skill(wrong_location)

        # Cleanup
        shutil.rmtree(temp_dir / "wrong")


# ============================================================================
# Test SkillBuilder - validate_skill_directory()
# ============================================================================


class TestValidateSkillDirectory:
    """Test SkillBuilder.validate_skill_directory() method."""

    def test_valid_skill_directory(self, builder, temp_dir, valid_config):
        """Test validation of valid skill directory."""
        # Create skill
        skill_path, _ = builder.build_skill(valid_config, temp_dir)

        # Validate
        is_valid, message = builder.validate_skill_directory(skill_path)
        assert is_valid is True
        assert message == ""

        # Cleanup
        shutil.rmtree(skill_path)

    def test_nonexistent_directory(self, builder, temp_dir):
        """Test validation of nonexistent directory."""
        nonexistent = temp_dir / "nonexistent"
        is_valid, message = builder.validate_skill_directory(nonexistent)
        assert is_valid is False
        assert "not found" in message

    def test_path_is_file_not_directory(self, builder, temp_dir):
        """Test validation when path is file."""
        fake_skill = temp_dir / "fake-skill.txt"
        fake_skill.write_text("I'm a file")

        is_valid, message = builder.validate_skill_directory(fake_skill)
        assert is_valid is False
        assert "not a directory" in message

    def test_missing_skill_md_file(self, builder, temp_dir):
        """Test validation when SKILL.md is missing."""
        # Create directory without SKILL.md
        skill_dir = temp_dir / ".claude" / "skills" / "incomplete-skill"
        skill_dir.mkdir(parents=True)

        is_valid, message = builder.validate_skill_directory(skill_dir)
        assert is_valid is False
        assert "SKILL.md not found" in message

        # Cleanup
        shutil.rmtree(skill_dir)

    def test_empty_skill_md_file(self, builder, temp_dir, valid_config):
        """Test validation when SKILL.md is empty."""
        # Create skill
        skill_path, _ = builder.build_skill(valid_config, temp_dir)

        # Overwrite SKILL.md with empty content
        skill_file = skill_path / "SKILL.md"
        skill_file.write_text("")

        is_valid, message = builder.validate_skill_directory(skill_path)
        assert is_valid is False
        assert "empty" in message.lower()

        # Cleanup
        shutil.rmtree(skill_path)

    def test_skill_md_without_frontmatter(self, builder, temp_dir, valid_config):
        """Test validation when SKILL.md lacks frontmatter."""
        # Create skill
        skill_path, _ = builder.build_skill(valid_config, temp_dir)

        # Overwrite SKILL.md without frontmatter
        skill_file = skill_path / "SKILL.md"
        skill_file.write_text("Just content, no frontmatter")

        is_valid, message = builder.validate_skill_directory(skill_path)
        assert is_valid is False
        assert "frontmatter" in message.lower()

        # Cleanup
        shutil.rmtree(skill_path)


# ============================================================================
# Performance Tests
# ============================================================================


class TestPerformance:
    """Test SkillBuilder performance requirements."""

    def test_skill_creation_performance(self, builder, temp_dir, valid_config):
        """Test that skill creation is < 50ms."""
        # Measure skill creation time
        start_time = time.time()
        skill_path, _ = builder.build_skill(valid_config, temp_dir)
        elapsed_ms = (time.time() - start_time) * 1000

        # Verify performance target
        assert elapsed_ms < 50, f"Skill creation took {elapsed_ms:.2f}ms, expected < 50ms"

        # Cleanup
        shutil.rmtree(skill_path)


# ============================================================================
# Integration Tests
# ============================================================================


class TestIntegration:
    """Test SkillBuilder integration with other components."""

    def test_builder_with_custom_template_manager(self, temp_dir):
        """Test builder with custom TemplateManager."""
        template_manager = TemplateManager()
        builder = SkillBuilder(template_manager=template_manager)

        config = SkillConfig(
            name="integration-skill",
            description="Integration test skill. Use when testing integration.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        skill_path, content = builder.build_skill(config, temp_dir)
        assert skill_path.exists()
        assert "integration-skill" in content

        # Cleanup
        shutil.rmtree(skill_path)

    def test_builder_with_custom_scope_manager(self, temp_dir):
        """Test builder with custom ScopeManager."""
        scope_manager = ScopeManager(cwd=temp_dir)
        builder = SkillBuilder(scope_manager=scope_manager)

        config = SkillConfig(
            name="scope-integration",
            description="Scope integration test. Use when testing scope integration.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        skill_path, _ = builder.build_skill(config, temp_dir)
        assert skill_path.exists()

        # Cleanup
        shutil.rmtree(skill_path)


# ============================================================================
# Wizard Integration Tests (Phase 5)
# ============================================================================


class TestWizardIntegration:
    """Test SkillWizard integration with other components."""

    def test_wizard_end_to_end_creation(self, temp_dir, monkeypatch):
        """Test end-to-end skill creation workflow through wizard."""
        from src.tools.skill_builder.wizard import SkillWizard

        # Mock questionary inputs
        inputs = [
            "pdf-processor",  # name
            "Extract text from PDFs. Use when working with PDF files.",  # description
            "project",  # scope
            "basic",  # template
            False,  # add tools?
            False,  # add scripts?
            True,  # confirm
        ]
        input_iter = iter(inputs)

        def mock_ask(*args, **kwargs):
            return next(input_iter)

        # Patch all questionary methods
        monkeypatch.setattr("questionary.text", lambda *a, **k: type("", (), {"ask": mock_ask})())
        monkeypatch.setattr("questionary.select", lambda *a, **k: type("", (), {"ask": mock_ask})())
        monkeypatch.setattr(
            "questionary.confirm", lambda *a, **k: type("", (), {"ask": mock_ask})()
        )

        wizard = SkillWizard()
        config = wizard.run(temp_dir)

        assert config is not None
        assert config.name == "pdf-processor"
        assert "Use when" in config.description
        assert config.scope == ScopeType.PROJECT
        assert config.template == "basic"

    def test_wizard_validation_feedback(self, temp_dir, monkeypatch):
        """Test wizard provides real-time validation feedback."""
        from src.tools.skill_builder.validator import SkillValidator

        # Test invalid name (uppercase) - We test the validator directly
        is_valid, error = SkillValidator.validate_skill_name("Invalid Name")
        assert not is_valid
        assert "lowercase" in error

        # Test invalid description (no usage context)
        is_valid, error = SkillValidator.validate_description("Just a description")
        assert not is_valid
        assert "when to use" in error.lower()

        # Test valid inputs
        is_valid, _ = SkillValidator.validate_skill_name("pdf-processor")
        assert is_valid

        is_valid, _ = SkillValidator.validate_description(
            "Extract text from PDFs. Use when working with PDF files."
        )
        assert is_valid

    def test_wizard_catalog_integration(self, temp_dir, monkeypatch):
        """Test wizard integrates with catalog manager."""
        from src.tools.skill_builder.catalog import CatalogManager
        from src.tools.skill_builder.wizard import SkillWizard

        catalog_manager = CatalogManager(catalog_path=temp_dir / "skills.json")
        builder = SkillBuilder()
        builder.catalog_manager = catalog_manager
        wizard = SkillWizard(builder=builder, catalog_manager=catalog_manager)

        # Mock questionary inputs
        inputs = [
            "catalog-test",  # name
            "Test catalog integration. Use when testing catalog.",  # description
            "project",  # scope
            "basic",  # template
            False,  # add tools?
            False,  # add scripts?
            True,  # confirm
        ]
        input_iter = iter(inputs)

        def mock_ask(*args, **kwargs):
            return next(input_iter)

        # Patch questionary
        monkeypatch.setattr("questionary.text", lambda *a, **k: type("", (), {"ask": mock_ask})())
        monkeypatch.setattr("questionary.select", lambda *a, **k: type("", (), {"ask": mock_ask})())
        monkeypatch.setattr(
            "questionary.confirm", lambda *a, **k: type("", (), {"ask": mock_ask})()
        )

        config = wizard.run(temp_dir)
        assert config is not None

        # Build the skill to trigger catalog update
        skill_path, _ = builder.build_skill(config, temp_dir)

        # Verify catalog was updated
        catalog_manager.sync_catalog(temp_dir)
        skills = catalog_manager.list_skills()
        assert len(skills) == 1
        assert skills[0].name == "catalog-test"
        assert skills[0].scope == ScopeType.PROJECT
        # Template is stored in metadata
        assert skills[0].metadata["template"] == "basic"

        # Cleanup
        shutil.rmtree(skill_path)

    def test_wizard_error_handling(self, temp_dir, monkeypatch):
        """Test wizard handles errors gracefully."""
        from src.tools.skill_builder.wizard import SkillWizard

        wizard = SkillWizard()

        # Test KeyboardInterrupt handling
        def mock_keyboard_interrupt(*args, **kwargs):
            raise KeyboardInterrupt()

        monkeypatch.setattr(
            "questionary.text", lambda *a, **k: type("", (), {"ask": mock_keyboard_interrupt})()
        )

        config = wizard.run(temp_dir)
        assert config is None  # Should return None on KeyboardInterrupt

    def test_wizard_cancel_operation(self, temp_dir, monkeypatch):
        """Test wizard can be cancelled at various steps."""
        from src.tools.skill_builder.wizard import SkillWizard

        wizard = SkillWizard()

        # Test cancel at name prompt
        monkeypatch.setattr(
            "questionary.text", lambda *a, **k: type("", (), {"ask": lambda: None})()
        )
        config = wizard.run(temp_dir)
        assert config is None

        # Test cancel at confirm prompt
        inputs = [
            "test-skill",  # name
            "Test skill. Use when testing.",  # description
            "project",  # scope
            "basic",  # template
            False,  # add tools?
            False,  # add scripts?
            False,  # confirm (cancel here)
        ]
        input_iter = iter(inputs)

        def mock_ask(*args, **kwargs):
            return next(input_iter)

        monkeypatch.setattr("questionary.text", lambda *a, **k: type("", (), {"ask": mock_ask})())
        monkeypatch.setattr("questionary.select", lambda *a, **k: type("", (), {"ask": mock_ask})())
        monkeypatch.setattr(
            "questionary.confirm", lambda *a, **k: type("", (), {"ask": mock_ask})()
        )

        config = wizard.run(temp_dir)
        assert config is None  # Should return None when user declines confirmation

    def test_wizard_scope_detection(self, temp_dir, monkeypatch):
        """Test wizard correctly handles scope selection."""
        from src.tools.skill_builder.wizard import SkillWizard

        wizard = SkillWizard()

        # Test all three scopes
        for scope_value in ["global", "project", "local"]:
            inputs = [
                f"test-{scope_value}",  # name
                f"Test {scope_value} scope. Use when testing {scope_value}.",  # description
                scope_value,  # scope
                "basic",  # template
                False,  # add tools?
                False,  # add scripts?
                True,  # confirm
            ]
            input_iter = iter(inputs)

            def mock_ask(*args, **kwargs):
                return next(input_iter)

            monkeypatch.setattr(
                "questionary.text", lambda *a, **k: type("", (), {"ask": mock_ask})()
            )
            monkeypatch.setattr(
                "questionary.select", lambda *a, **k: type("", (), {"ask": mock_ask})()
            )
            monkeypatch.setattr(
                "questionary.confirm", lambda *a, **k: type("", (), {"ask": mock_ask})()
            )

            config = wizard.run(temp_dir)
            assert config is not None
            assert config.scope == ScopeType(scope_value)


# ============================================================================
# CLI Tests (Phase 6)
# ============================================================================


class TestCLI:
    """Test CLI commands from main.py."""

    def test_create_command_with_wizard(self, temp_dir, monkeypatch):
        """Test create command integrates with wizard."""
        from click.testing import CliRunner
        from src.tools.skill_builder.main import cli

        # Mock wizard to return a config
        def mock_wizard_run(self, project_root):
            return SkillConfig(
                name="cli-test-skill",
                description="CLI test skill. Use when testing CLI.",
                scope=ScopeType.PROJECT,
                template="basic",
            )

        monkeypatch.setattr("src.tools.skill_builder.main.SkillWizard.run", mock_wizard_run)

        runner = CliRunner()
        with runner.isolated_filesystem(temp_dir=temp_dir) as td:
            result = runner.invoke(cli, ["create", "--project-root", td])
            assert result.exit_code == 0
            assert "✅ Skill created successfully" in result.output
            assert "cli-test-skill" in result.output

    def test_list_command_with_filters(self, temp_dir):
        """Test list command with filtering."""
        from click.testing import CliRunner
        from src.tools.skill_builder.catalog import CatalogManager
        from src.tools.skill_builder.main import cli
        from src.tools.skill_builder.models import SkillCatalogEntry

        runner = CliRunner()

        # Create catalog with test skills
        catalog_mgr = CatalogManager(catalog_path=temp_dir / "skills.json")

        # Add test skills
        skill1 = SkillCatalogEntry(
            name="test-skill-1",
            description="First test skill",
            scope=ScopeType.PROJECT,
            path=str(temp_dir / "skill1"),
            metadata={"template": "basic"},
        )
        skill2 = SkillCatalogEntry(
            name="test-skill-2",
            description="Second test skill",
            scope=ScopeType.GLOBAL,
            path=str(temp_dir / "skill2"),
            metadata={"template": "with_tools", "has_scripts": True},
        )
        catalog_mgr.add_skill(skill1)
        catalog_mgr.add_skill(skill2)

        # Test list all
        result = runner.invoke(cli, ["list", "--project-root", str(temp_dir)])
        assert result.exit_code == 0
        assert "test-skill-1" in result.output
        assert "test-skill-2" in result.output
        assert "2 total" in result.output

        # Test filter by scope
        result = runner.invoke(cli, ["list", "--scope", "project", "--project-root", str(temp_dir)])
        assert result.exit_code == 0
        assert "test-skill-1" in result.output
        assert "test-skill-2" not in result.output

        # Test filter by template
        result = runner.invoke(
            cli, ["list", "--template", "with_tools", "--project-root", str(temp_dir)]
        )
        assert result.exit_code == 0
        assert "test-skill-2" in result.output
        assert "test-skill-1" not in result.output

        # Test filter by has-scripts
        result = runner.invoke(cli, ["list", "--has-scripts", "--project-root", str(temp_dir)])
        assert result.exit_code == 0
        assert "test-skill-2" in result.output
        assert "test-skill-1" not in result.output

    def test_delete_command_with_confirmation(self, temp_dir, valid_config):
        """Test delete command with confirmation."""
        from click.testing import CliRunner
        from src.tools.skill_builder.catalog import CatalogManager
        from src.tools.skill_builder.main import cli
        from src.tools.skill_builder.models import SkillCatalogEntry

        runner = CliRunner()
        builder = SkillBuilder()

        # Create skill
        skill_path, _ = builder.build_skill(valid_config, temp_dir)

        # Add to catalog
        catalog_mgr = CatalogManager(catalog_path=temp_dir / "skills.json")
        entry = SkillCatalogEntry(
            name="test-skill",
            description="Test skill",
            scope=ScopeType.PROJECT,
            path=str(skill_path),
            metadata={"template": "basic"},
        )
        catalog_mgr.add_skill(entry)

        # Test delete with --yes flag (no confirmation)
        result = runner.invoke(
            cli, ["delete", "test-skill", "--yes", "--project-root", str(temp_dir)]
        )
        assert result.exit_code == 0
        assert "✅ Skill 'test-skill' deleted successfully" in result.output
        assert not skill_path.exists()

    def test_validate_command(self, temp_dir, valid_config):
        """Test validate command."""
        from click.testing import CliRunner
        from src.tools.skill_builder.main import cli

        runner = CliRunner()
        builder = SkillBuilder()

        # Create valid skill
        skill_path, _ = builder.build_skill(valid_config, temp_dir)

        # Test validation of valid skill
        result = runner.invoke(cli, ["validate", str(skill_path)])
        assert result.exit_code == 0
        assert "✅ Skill directory is valid" in result.output

        # Test validation of invalid skill (missing SKILL.md)
        invalid_skill = temp_dir / "invalid-skill"
        invalid_skill.mkdir()

        result = runner.invoke(cli, ["validate", str(invalid_skill)])
        assert result.exit_code == 1
        assert "❌ Skill directory is invalid" in result.output
        assert "SKILL.md not found" in result.output

        # Cleanup
        shutil.rmtree(skill_path)
        shutil.rmtree(invalid_skill)


# ============================================================================
# Additional Performance Tests (Phase 6)
# ============================================================================


class TestCLIPerformance:
    """Test CLI performance requirements."""

    def test_catalog_operations_performance(self, temp_dir):
        """Test that catalog operations are < 100ms."""
        from src.tools.skill_builder.catalog import CatalogManager
        from src.tools.skill_builder.models import SkillCatalogEntry

        catalog_mgr = CatalogManager(catalog_path=temp_dir / "skills.json")

        # Add 10 test skills
        for i in range(10):
            entry = SkillCatalogEntry(
                name=f"perf-test-{i}",
                description=f"Performance test skill {i}",
                scope=ScopeType.PROJECT,
                path=str(temp_dir / f"skill{i}"),
                metadata={"template": "basic"},
            )
            catalog_mgr.add_skill(entry)

        # Test search performance
        start_time = time.time()
        results = catalog_mgr.search_skills(query="test")
        elapsed_ms = (time.time() - start_time) * 1000
        assert elapsed_ms < 100, f"Catalog search took {elapsed_ms:.2f}ms, expected < 100ms"
        assert len(results) == 10

        # Test list performance
        start_time = time.time()
        results = catalog_mgr.list_skills()
        elapsed_ms = (time.time() - start_time) * 1000
        assert elapsed_ms < 100, f"Catalog list took {elapsed_ms:.2f}ms, expected < 100ms"
        assert len(results) == 10

        # Test stats performance
        start_time = time.time()
        stats = catalog_mgr.get_catalog_stats()
        elapsed_ms = (time.time() - start_time) * 1000
        assert elapsed_ms < 100, f"Catalog stats took {elapsed_ms:.2f}ms, expected < 100ms"
        assert stats["total"] == 10

    def test_validation_performance(self, temp_dir, valid_config):
        """Test that validation is < 10ms."""
        builder = SkillBuilder()

        # Create skill
        skill_path, _ = builder.build_skill(valid_config, temp_dir)

        # Measure validation time
        start_time = time.time()
        is_valid, message = builder.validate_skill_directory(skill_path)
        elapsed_ms = (time.time() - start_time) * 1000

        assert is_valid
        assert elapsed_ms < 10, f"Validation took {elapsed_ms:.2f}ms, expected < 10ms"

        # Cleanup
        shutil.rmtree(skill_path)

    def test_template_rendering_performance(self):
        """Test that template rendering is < 10ms."""
        from src.tools.skill_builder.templates import TemplateManager

        template_mgr = TemplateManager()

        config = SkillConfig(
            name="perf-test",
            description="Performance test. Use when testing performance.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        # Measure template rendering time
        start_time = time.time()
        content = template_mgr.render("basic", config.model_dump())
        elapsed_ms = (time.time() - start_time) * 1000

        assert "perf-test" in content
        assert elapsed_ms < 10, f"Template rendering took {elapsed_ms:.2f}ms, expected < 10ms"
