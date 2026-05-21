"""
Template management for command builder.

Handles loading, rendering, and managing Jinja2 templates for command generation.
Supports variable substitution, conditional sections, and custom template creation.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from jinja2.sandbox import SandboxedEnvironment

from .exceptions import TemplateError
from .models import CommandConfig
from .validator import Validator


class TemplateManager:
    """Manages Jinja2 templates for command generation."""

    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize template manager.

        Args:
            templates_dir: Directory containing templates (default: ./templates)
        """
        if templates_dir is None:
            templates_dir = Path(__file__).parent / "templates"

        self.templates_dir = templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Use sandboxed environment for security
        self.env = SandboxedEnvironment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=False,  # Markdown doesn't need HTML escaping
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def list_templates(self) -> List[str]:
        """
        List available template names.

        Returns:
            List of template names (without .md extension)
        """
        if not self.templates_dir.exists():
            return []

        return [p.stem for p in self.templates_dir.glob("*.md") if p.is_file()]

    def template_exists(self, template_name: str) -> bool:
        """
        Check if a template exists.

        Args:
            template_name: Template name

        Returns:
            True if template exists
        """
        # Validate template name for security
        is_valid, _ = Validator.validate_template_name(template_name)
        if not is_valid:
            return False

        template_path = self.templates_dir / f"{template_name}.md"
        return template_path.exists()

    def load_template(self, template_name: str) -> Template:
        """
        Load a Jinja2 template by name.

        Args:
            template_name: Template name (without .md extension)

        Returns:
            Jinja2 Template object

        Raises:
            TemplateError: If template cannot be loaded
        """
        # Validate template name for security
        is_valid, error = Validator.validate_template_name(template_name)
        if not is_valid:
            raise TemplateError(f"Invalid template name: {error}")

        try:
            return self.env.get_template(f"{template_name}.md")
        except TemplateNotFound:
            available = self.list_templates()
            raise TemplateError(
                f"Template '{template_name}' not found. "
                f"Available templates: {', '.join(available) if available else 'none'}"
            )
        except Exception as e:
            raise TemplateError(f"Failed to load template '{template_name}': {e}")

    def render_template(
        self,
        template_name: str,
        config: CommandConfig,
    ) -> str:
        """
        Render a template with command configuration.

        Args:
            template_name: Template name
            config: Command configuration

        Returns:
            Rendered template content

        Raises:
            TemplateError: If rendering fails
        """
        try:
            template = self.load_template(template_name)

            # Prepare template context
            context = self._prepare_context(config)

            # Render template
            return template.render(**context)

        except TemplateError:
            raise
        except Exception as e:
            raise TemplateError(f"Failed to render template '{template_name}': {e}")

    def _prepare_context(self, config: CommandConfig) -> Dict[str, Any]:
        """
        Prepare Jinja2 context from command configuration.

        Args:
            config: Command configuration

        Returns:
            Dictionary of template variables
        """
        # Sanitize all YAML frontmatter values
        sanitized_frontmatter = Validator.sanitize_yaml_value(config.frontmatter)

        # Build context
        context = {
            "name": config.name,
            "description": config.description,
            "scope": config.scope.value,
            "parameters": [
                {
                    "name": param.name,
                    "type": param.type.value,
                    "description": param.description,
                    "required": param.required,
                    "default": param.default,
                    "choices": param.choices,
                }
                for param in config.parameters
            ],
            "has_parameters": len(config.parameters) > 0,
            "bash_commands": config.bash_commands,
            "has_bash": len(config.bash_commands) > 0,
            "file_references": config.file_references,
            "has_files": len(config.file_references) > 0,
            "thinking_mode": config.thinking_mode,
            "frontmatter": sanitized_frontmatter,
        }

        return context

    def create_custom_template(
        self,
        template_name: str,
        content: str,
    ) -> Path:
        """
        Create a custom template file.

        Args:
            template_name: Template name (without .md extension)
            content: Template content (Jinja2 markdown)

        Returns:
            Path to created template

        Raises:
            TemplateError: If template creation fails
        """
        # Validate template name
        is_valid, error = Validator.validate_template_name(template_name)
        if not is_valid:
            raise TemplateError(f"Invalid template name: {error}")

        template_path = self.templates_dir / f"{template_name}.md"

        # Check if template already exists
        if template_path.exists():
            raise TemplateError(f"Template '{template_name}' already exists")

        try:
            template_path.write_text(content)
            return template_path
        except Exception as e:
            raise TemplateError(f"Failed to create template '{template_name}': {e}")

    def get_template_path(self, template_name: str) -> Path:
        """
        Get the file path for a template.

        Args:
            template_name: Template name

        Returns:
            Path to template file

        Raises:
            TemplateError: If template doesn't exist
        """
        # Validate template name
        is_valid, error = Validator.validate_template_name(template_name)
        if not is_valid:
            raise TemplateError(f"Invalid template name: {error}")

        template_path = self.templates_dir / f"{template_name}.md"

        if not template_path.exists():
            raise TemplateError(f"Template '{template_name}' not found")

        return template_path
