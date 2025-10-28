"""Tests for skill_builder template manager."""

import pytest

from src.tools.skill_builder.exceptions import TemplateError
from src.tools.skill_builder.templates import TemplateManager


class TestTemplateManager:
    """Tests for TemplateManager class."""

    def test_template_manager_init(self):
        """Test TemplateManager initialization."""
        manager = TemplateManager()
        assert manager.templates_dir.exists()
        assert manager.templates_dir.is_dir()
        assert manager.env is not None

    def test_list_templates(self):
        """Test listing available templates."""
        manager = TemplateManager()
        templates = manager.list_templates()

        assert isinstance(templates, list)
        assert len(templates) >= 4
        assert "basic" in templates
        assert "with_tools" in templates
        assert "with_scripts" in templates
        assert "advanced" in templates

    def test_get_template_path(self):
        """Test getting template path."""
        manager = TemplateManager()
        path = manager.get_template_path("basic")

        assert path.exists()
        assert path.name == "basic.md"
        assert path.is_file()

    def test_render_basic_template(self):
        """Test rendering basic template."""
        manager = TemplateManager()
        content = manager.render(
            "basic",
            {
                "name": "test-skill",
                "description": "Test description",
                "content": "Test instructions",
                "frontmatter": {},
            },
        )

        assert "test-skill" in content
        assert "Test description" in content
        assert "Test instructions" in content

    def test_render_with_variables(self):
        """Test rendering with all variables."""
        manager = TemplateManager()
        content = manager.render(
            "with_tools",
            {
                "name": "pdf-processor",
                "description": "Process PDF files",
                "content": "Extract text from PDFs",
                "allowed_tools": ["Read", "Bash"],
                "frontmatter": {"version": "1.0"},
            },
        )

        assert "pdf-processor" in content
        assert "Read" in content
        assert "Bash" in content
        assert "version" in content

    def test_sandboxing_prevents_code_execution(self):
        """Test that sandboxing prevents code execution."""
        manager = TemplateManager()

        # Create a temporary template with malicious code attempt
        malicious_template = manager.templates_dir / "malicious.md"
        malicious_template.write_text("{{ name.__class__.__bases__[0].__subclasses__() }}")

        try:
            # This should fail due to sandboxing
            with pytest.raises(Exception):  # Could be SecurityError or TemplateError
                manager.render("malicious", {"name": "test"})
        finally:
            # Clean up
            malicious_template.unlink()

    def test_template_not_found_error(self):
        """Test error handling for missing templates."""
        manager = TemplateManager()

        with pytest.raises(TemplateError) as exc_info:
            manager.render("nonexistent", {"name": "test"})

        assert "not found" in str(exc_info.value).lower()

    def test_invalid_template_syntax(self):
        """Test error handling for invalid template syntax."""
        manager = TemplateManager()

        # Create template with syntax error
        bad_template = manager.templates_dir / "bad_syntax.md"
        bad_template.write_text("{{ name ")  # Missing closing braces

        try:
            with pytest.raises(TemplateError) as exc_info:
                manager.render("bad_syntax", {"name": "test"})

            assert "syntax" in str(exc_info.value).lower()
        finally:
            # Clean up
            bad_template.unlink()
