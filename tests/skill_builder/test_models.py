"""Tests for skill_builder models."""

import pytest
from pydantic import ValidationError

from src.tools.skill_builder.models import ScopeType, SkillConfig


class TestSkillConfig:
    """Tests for SkillConfig model validation."""

    def test_valid_config(self):
        """Test valid skill configuration."""
        config = SkillConfig(
            name="my-skill",
            description="Description with usage context. Use when needed.",
            scope=ScopeType.GLOBAL,
            template="basic",
        )
        assert config.name == "my-skill"
        assert config.scope == ScopeType.GLOBAL
        assert config.template == "basic"

    def test_invalid_name_uppercase(self):
        """Test that uppercase names are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SkillConfig(
                name="MySkill",  # Invalid: uppercase
                description="Test. Use when testing.",
                scope=ScopeType.GLOBAL,
            )
        assert "lowercase" in str(exc_info.value).lower()

    def test_invalid_name_too_long(self):
        """Test that names over 64 chars are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SkillConfig(
                name="a" * 65,
                description="Test. Use when testing.",
                scope=ScopeType.GLOBAL,
            )
        assert "64" in str(exc_info.value)

    def test_invalid_name_empty(self):
        """Test that empty names are rejected."""
        with pytest.raises(ValidationError):
            SkillConfig(name="", description="Test. Use when testing.", scope=ScopeType.GLOBAL)

    def test_invalid_name_special_chars(self):
        """Test that special characters in names are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SkillConfig(
                name="my_skill!",  # Invalid: underscore and exclamation
                description="Test. Use when testing.",
                scope=ScopeType.GLOBAL,
            )
        assert "lowercase" in str(exc_info.value).lower()

    def test_invalid_name_consecutive_hyphens(self):
        """Test that consecutive hyphens are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SkillConfig(
                name="my--skill",  # Invalid: consecutive hyphens
                description="Test. Use when testing.",
                scope=ScopeType.GLOBAL,
            )
        assert "consecutive" in str(exc_info.value).lower()

    def test_invalid_description_empty(self):
        """Test that empty descriptions are rejected."""
        with pytest.raises(ValidationError):
            SkillConfig(name="test-skill", description="", scope=ScopeType.GLOBAL)

    def test_invalid_description_no_usage_context(self):
        """Test that descriptions without usage context are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SkillConfig(
                name="test-skill",
                description="Process PDFs.",  # Missing "when" or "use"
                scope=ScopeType.GLOBAL,
            )
        error_msg = str(exc_info.value).lower()
        assert "when" in error_msg or "use" in error_msg

    def test_invalid_description_too_long(self):
        """Test that descriptions over 1024 chars are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SkillConfig(name="test-skill", description="A" * 1025, scope=ScopeType.GLOBAL)
        assert "1024" in str(exc_info.value)

    def test_invalid_template_path_traversal(self):
        """Test that path traversal in template names is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SkillConfig(
                name="test-skill",
                description="Test. Use when testing.",
                scope=ScopeType.GLOBAL,
                template="../../../etc/passwd",
            )
        # Path traversal is rejected (contains '.' and '/')
        assert "template" in str(exc_info.value).lower()
