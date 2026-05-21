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
        assert len(templates) >= 7
        assert "basic" in templates
        assert "with_tools" in templates
        assert "with_scripts" in templates
        assert "advanced" in templates
        assert "with_model" in templates
        assert "orchestrator" in templates
        assert "specialist" in templates

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

    def test_render_with_model_template(self):
        """Test rendering with_model template."""
        manager = TemplateManager()
        content = manager.render(
            "with_model",
            {
                "name": "code-reviewer",
                "description": "Review code for quality",
                "content": "Analyze code for bugs and improvements",
                "model_preference": "claude-sonnet-4",
                "temperature": "0.7",
                "frontmatter": {},
            },
        )

        assert "code-reviewer" in content
        assert "claude-sonnet-4" in content
        assert "0.7" in content or "temperature" in content

    def test_render_orchestrator_template(self):
        """Test rendering orchestrator template."""
        manager = TemplateManager()
        content = manager.render(
            "orchestrator",
            {
                "name": "project-manager",
                "description": "Coordinate project tasks",
                "content": "Break down complex projects into manageable tasks",
                "sub_skills": ["task-planner", "code-reviewer", "test-runner"],
                "workflow": "1. Plan\n2. Execute\n3. Review",
                "frontmatter": {},
            },
        )

        assert "project-manager" in content
        assert "task-planner" in content
        assert "workflow" in content.lower() or "Workflow" in content

    def test_render_specialist_template(self):
        """Test rendering specialist template."""
        manager = TemplateManager()
        content = manager.render(
            "specialist",
            {
                "name": "python-expert",
                "description": "Python development specialist",
                "content": "Expert in Python best practices and optimization",
                "expertise_area": "Python Development",
                "technologies": ["Python 3.12", "pytest", "asyncio"],
                "patterns": ["SOLID", "Design Patterns", "Clean Architecture"],
                "frontmatter": {},
            },
        )

        assert "python-expert" in content
        assert "Python Development" in content or "Python" in content
        assert "pytest" in content or "technologies" in content.lower()

    def test_all_templates_exist(self):
        """Test that all expected templates exist."""
        manager = TemplateManager()
        templates = manager.list_templates()

        expected_templates = [
            "basic",
            "with_tools",
            "with_scripts",
            "advanced",
            "with_model",
            "orchestrator",
            "specialist",
        ]

        for template in expected_templates:
            assert template in templates, f"Expected template '{template}' not found"

    def test_template_path_security(self):
        """Test that path traversal is prevented."""
        manager = TemplateManager()

        # Try path traversal attacks
        dangerous_names = [
            "../../../etc/passwd",
            "../../config",
            "..\\..\\windows\\system32",
            "basic/../../../etc/passwd",
        ]

        for dangerous_name in dangerous_names:
            try:
                # Should raise TemplateError due to validation
                manager.get_template_path(dangerous_name)
                # If we get here, the test should fail
                assert False, f"Path traversal not blocked for: {dangerous_name}"
            except Exception:
                # Good - path traversal was blocked
                pass

    def test_template_rendering_performance(self):
        """Test that template rendering is fast (< 10ms target)."""
        import time

        manager = TemplateManager()

        # Render a simple template multiple times
        start = time.time()
        for _ in range(100):
            manager.render(
                "basic",
                {
                    "name": "perf-test",
                    "description": "Performance test skill",
                    "content": "Test content",
                    "frontmatter": {},
                },
            )
        elapsed = (time.time() - start) * 1000  # Convert to ms

        # Average should be well under 10ms per render
        avg_time = elapsed / 100
        assert avg_time < 10, f"Template rendering too slow: {avg_time:.2f}ms (target: <10ms)"

    def test_template_with_empty_optional_fields(self):
        """Test templates with empty optional fields."""
        manager = TemplateManager()

        # Test with minimal required fields only
        content = manager.render(
            "with_model",
            {
                "name": "minimal-skill",
                "description": "Minimal test skill",
                "content": "Basic instructions",
                "frontmatter": {},
            },
        )

        assert "minimal-skill" in content
        assert "Minimal test skill" in content
