"""
Template management for skill_builder tool.

This module provides secure template loading and rendering using Jinja2's
SandboxedEnvironment. Templates are loaded from the templates/ directory
and rendered with user-provided variables.

Security Focus:
- SandboxedEnvironment prevents code execution
- Path traversal prevention
- Template validation before rendering
- No custom filters or functions
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import TemplateNotFound
from jinja2.exceptions import TemplateSyntaxError
from jinja2.sandbox import SandboxedEnvironment

from src.tools.skill_builder.exceptions import TemplateError
from src.tools.skill_builder.validator import SkillValidator


class TemplateManager:
    """
    Manages skill templates with secure rendering.

    Uses Jinja2's SandboxedEnvironment to prevent code execution from
    templates. Only variable substitution is allowed.

    Attributes:
        templates_dir: Path to templates directory
        env: Jinja2 SandboxedEnvironment instance
    """

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initializes the template manager.

        Args:
            templates_dir: Optional custom templates directory.
                          Defaults to src/tools/skill_builder/templates/

        Raises:
            TemplateError: If templates directory doesn't exist
        """
        if templates_dir is None:
            # Default to templates/ in same directory as this file
            templates_dir = Path(__file__).parent / "templates"

        if not templates_dir.exists():
            raise TemplateError(
                f"Templates directory not found: {templates_dir}"
            )

        if not templates_dir.is_dir():
            raise TemplateError(
                f"Templates path is not a directory: {templates_dir}"
            )

        self.templates_dir = templates_dir.resolve()

        # Create sandboxed environment for security
        # This prevents code execution from templates
        self.env = SandboxedEnvironment(
            autoescape=False,  # We're generating Markdown, not HTML
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def list_templates(self) -> List[str]:
        """
        Lists available template names.

        Returns:
            List of template names (without .md extension)

        Examples:
            >>> manager = TemplateManager()
            >>> manager.list_templates()
            ['basic', 'with_tools', 'with_scripts', 'advanced']
        """
        template_files = sorted(self.templates_dir.glob("*.md"))
        return [f.stem for f in template_files]

    def get_template_path(self, template_name: str) -> Path:
        """
        Gets the absolute path to a template file.

        Security: Validates template name and ensures path is within
        templates directory.

        Args:
            template_name: Name of template (without .md extension)

        Returns:
            Absolute path to template file

        Raises:
            TemplateError: If template name is invalid or file doesn't exist

        Examples:
            >>> manager = TemplateManager()
            >>> path = manager.get_template_path("basic")
            >>> path.name
            'basic.md'
        """
        # Validate template name
        is_valid, message = SkillValidator.validate_template_name(template_name)
        if not is_valid:
            raise TemplateError(f"Invalid template name: {message}")

        # Construct path
        template_path = self.templates_dir / f"{template_name}.md"

        # Security: Ensure path is within templates directory
        try:
            resolved_path = template_path.resolve()
            if not resolved_path.is_relative_to(self.templates_dir):
                raise TemplateError(
                    f"Template path outside templates directory: {template_name}"
                )
        except Exception as e:
            raise TemplateError(f"Path validation failed: {str(e)}")

        # Check if file exists
        if not template_path.exists():
            raise TemplateError(
                f"Template not found: {template_name}. "
                f"Available: {', '.join(self.list_templates())}"
            )

        return resolved_path

    def render(
        self,
        template_name: str,
        variables: Dict[str, Any]
    ) -> str:
        """
        Renders a template with provided variables.

        Security: Uses SandboxedEnvironment to prevent code execution.
        Only variable substitution is performed.

        Args:
            template_name: Name of template to render
            variables: Dictionary of template variables

        Returns:
            Rendered template content

        Raises:
            TemplateError: If template not found or rendering fails

        Performance:
            - Template rendering: < 10ms
            - Template loading: < 5ms

        Examples:
            >>> manager = TemplateManager()
            >>> content = manager.render("basic", {
            ...     "name": "test-skill",
            ...     "description": "Test skill",
            ...     "content": "Instructions here"
            ... })
            >>> "test-skill" in content
            True
        """
        # Get and validate template path
        template_path = self.get_template_path(template_name)

        # Read template content
        try:
            template_content = template_path.read_text(encoding="utf-8")
        except Exception as e:
            raise TemplateError(
                f"Failed to read template {template_name}: {str(e)}"
            )

        # Sanitize variables
        sanitized_vars = self._sanitize_variables(variables)

        # Render template using sandboxed environment
        try:
            template = self.env.from_string(template_content)
            rendered = template.render(**sanitized_vars)
            return rendered
        except TemplateSyntaxError as e:
            raise TemplateError(
                f"Template syntax error in {template_name}: {str(e)}"
            )
        except TemplateNotFound as e:
            raise TemplateError(
                f"Template not found: {str(e)}"
            )
        except Exception as e:
            raise TemplateError(
                f"Failed to render template {template_name}: {str(e)}"
            )

    def _sanitize_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes template variables for safe rendering.

        Args:
            variables: Raw template variables

        Returns:
            Sanitized variables dictionary

        Security:
            - Sanitizes string values
            - Validates frontmatter keys
            - Converts allowed_tools list to YAML-safe format
        """
        sanitized = {}

        for key, value in variables.items():
            # Sanitize string values
            if isinstance(value, str):
                sanitized[key] = SkillValidator.sanitize_string(value)
            # Handle allowed_tools list
            elif key == "allowed_tools" and isinstance(value, list):
                # Validate and format as YAML list
                is_valid, _ = SkillValidator.validate_allowed_tools(value)
                if is_valid:
                    sanitized[key] = value
                else:
                    sanitized[key] = []
            # Handle frontmatter dict
            elif key == "frontmatter" and isinstance(value, dict):
                # Validate frontmatter keys
                is_valid, _ = SkillValidator.validate_frontmatter_keys(value)
                if is_valid:
                    sanitized[key] = value
                else:
                    sanitized[key] = {}
            else:
                sanitized[key] = value

        return sanitized
