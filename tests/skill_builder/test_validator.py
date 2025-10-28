"""Tests for skill_builder validator."""

from pathlib import Path

from src.tools.skill_builder.validator import SkillValidator


class TestSkillValidator:
    """Tests for SkillValidator class methods."""

    def test_validate_skill_name_valid(self):
        """Test valid skill names are accepted."""
        valid, msg = SkillValidator.validate_skill_name("my-skill")
        assert valid is True
        assert "valid" in msg.lower()

    def test_validate_skill_name_invalid_uppercase(self):
        """Test uppercase names are rejected."""
        valid, msg = SkillValidator.validate_skill_name("MySkill")
        assert valid is False
        assert "lowercase" in msg.lower()

    def test_validate_skill_name_invalid_special_chars(self):
        """Test special characters are rejected."""
        valid, msg = SkillValidator.validate_skill_name("my_skill!")
        assert valid is False
        assert "lowercase" in msg.lower() or "hyphen" in msg.lower()

    def test_validate_skill_name_path_traversal(self):
        """Test path traversal attempts are rejected."""
        valid, msg = SkillValidator.validate_skill_name("../../../etc/passwd")
        assert valid is False
        # Will fail pattern match before path separator check
        assert "lowercase" in msg.lower() or "path" in msg.lower() or "separator" in msg.lower()

    def test_validate_description_valid(self):
        """Test valid descriptions are accepted."""
        valid, msg = SkillValidator.validate_description(
            "Process PDFs. Use when working with PDF files."
        )
        assert valid is True
        assert "valid" in msg.lower()

    def test_validate_description_no_usage_context(self):
        """Test descriptions without usage context are rejected."""
        valid, msg = SkillValidator.validate_description("Process PDFs.")
        assert valid is False
        assert "when" in msg.lower() or "use" in msg.lower()

    def test_validate_description_too_long(self):
        """Test descriptions over 1024 chars are rejected."""
        valid, msg = SkillValidator.validate_description("A" * 1025)
        assert valid is False
        assert "1024" in msg

    def test_validate_allowed_tools_valid(self):
        """Test valid tool lists are accepted."""
        valid, msg = SkillValidator.validate_allowed_tools(["Read", "Grep"])
        assert valid is True
        assert "valid" in msg.lower() or "read" in msg.lower()

    def test_validate_allowed_tools_invalid(self):
        """Test invalid tools are rejected."""
        valid, msg = SkillValidator.validate_allowed_tools(["InvalidTool"])
        assert valid is False
        assert "invalid" in msg.lower()

    def test_validate_template_name_valid(self):
        """Test valid template names are accepted."""
        valid, msg = SkillValidator.validate_template_name("basic")
        assert valid is True
        assert "valid" in msg.lower()

    def test_validate_template_name_path_traversal(self):
        """Test path traversal in template names is rejected."""
        valid, msg = SkillValidator.validate_template_name("../../../etc/passwd")
        assert valid is False
        # Will fail pattern match before path separator check
        assert "lowercase" in msg.lower() or "path" in msg.lower() or "separator" in msg.lower()

    def test_validate_path_security_valid(self, temp_skill_dir):
        """Test valid paths within base directory are accepted."""
        skill_path = temp_skill_dir / "my-skill"
        valid, msg = SkillValidator.validate_path_security(skill_path, temp_skill_dir)
        assert valid is True
        assert "secure" in msg.lower()

    def test_validate_path_security_traversal(self, temp_skill_dir):
        """Test path traversal attempts are rejected."""
        evil_path = Path("/etc/passwd")
        valid, msg = SkillValidator.validate_path_security(evil_path, temp_skill_dir)
        assert valid is False
        assert "outside" in msg.lower()

    def test_validate_frontmatter_keys_valid(self):
        """Test valid frontmatter keys are accepted."""
        frontmatter = {"version": "1.0", "author": "test"}
        valid, msg = SkillValidator.validate_frontmatter_keys(frontmatter)
        assert valid is True

    def test_validate_frontmatter_keys_invalid(self):
        """Test invalid frontmatter keys are rejected."""
        frontmatter = {"invalid key!": "value"}
        valid, msg = SkillValidator.validate_frontmatter_keys(frontmatter)
        assert valid is False
        assert "invalid" in msg.lower()
