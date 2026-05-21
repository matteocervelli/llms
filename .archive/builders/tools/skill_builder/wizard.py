"""
Interactive CLI wizard for skill creation.

Provides a beautiful, user-friendly skill creation experience using questionary
for interactive prompts with validation and real-time feedback.
"""

from pathlib import Path
from typing import List, Optional

import click
import questionary
from questionary import Style

from .builder import SkillBuilder
from .catalog import CatalogManager
from .exceptions import SkillBuilderError
from .models import SkillConfig, ScopeType
from .templates import TemplateManager
from .validator import SkillValidator

# Custom style for questionary prompts (Claude Code aesthetics)
CUSTOM_STYLE = Style(
    [
        ("qmark", "fg:#673ab7 bold"),
        ("question", "bold"),
        ("answer", "fg:#2196f3 bold"),
        ("pointer", "fg:#673ab7 bold"),
        ("highlighted", "fg:#673ab7 bold"),
        ("selected", "fg:#2196f3"),
        ("separator", "fg:#cc5454"),
        ("instruction", "fg:#858585"),
        ("text", ""),
        ("disabled", "fg:#858585 italic"),
    ]
)


class SkillWizard:
    """Interactive wizard for creating Claude Code skills."""

    def __init__(
        self,
        template_manager: Optional[TemplateManager] = None,
        builder: Optional[SkillBuilder] = None,
        catalog_manager: Optional[CatalogManager] = None,
    ):
        """
        Initialize skill wizard.

        Args:
            template_manager: Template manager
            builder: Skill builder
            catalog_manager: Catalog manager
        """
        self.template_manager = template_manager or TemplateManager()
        self.builder = (
            builder or SkillBuilder()
        )  # SkillBuilder creates its own ScopeManager internally
        self.catalog_manager = catalog_manager or CatalogManager()

    def run(self, project_root: Optional[Path] = None) -> Optional[SkillConfig]:
        """
        Run the interactive wizard.

        Args:
            project_root: Project root directory

        Returns:
            SkillConfig or None if cancelled

        Examples:
            >>> wizard = SkillWizard()
            >>> config = wizard.run()
            >>> if config:
            ...     print(f"Skill created: {config.name}")
        """
        click.echo("\n🚀 Claude Code Skill Builder - Interactive Wizard\n")

        try:
            # Step 1: Skill name
            name = self._prompt_skill_name()
            if not name:
                return None

            # Step 2: Description
            description = self._prompt_description()
            if not description:
                return None

            # Step 3: Scope
            scope = self._prompt_scope()
            if not scope:
                return None

            # Step 4: Template
            template = self._prompt_template()
            if not template:
                return None

            # Step 5: Allowed tools (optional)
            allowed_tools = self._prompt_allowed_tools()

            # Step 6: Additional files (optional)
            has_scripts = self._prompt_additional_files()

            # Build configuration
            config = SkillConfig(
                name=name,
                description=description,
                scope=scope,
                template=template,
                allowed_tools=allowed_tools if allowed_tools else None,
            )

            # Step 7: Preview and confirm
            if not self._preview_and_confirm(config, has_scripts):
                return None

            return config

        except KeyboardInterrupt:
            click.echo("\n\n❌ Wizard cancelled by user")
            return None
        except Exception as e:
            click.echo(f"\n\n❌ Error: {e}", err=True)
            return None

    def _prompt_skill_name(self) -> Optional[str]:
        """
        Prompt for skill name with validation.

        Returns:
            Skill name or None if cancelled

        Examples:
            >>> wizard = SkillWizard()
            >>> name = wizard._prompt_skill_name()
            Skill name (lowercase-with-hyphens): pdf-processor
        """
        # Show naming convention hint
        click.echo("\n💡 Naming convention: lowercase-with-hyphens")
        click.echo("   Examples: pdf-processor, api-helper, data-analyzer\n")

        while True:
            name = questionary.text(
                "Skill name (lowercase-with-hyphens):",
                style=CUSTOM_STYLE,
                validate=lambda text: SkillValidator.validate_skill_name(text)[0]
                or SkillValidator.validate_skill_name(text)[1],
            ).ask()

            if name is None:  # User cancelled
                return None

            # Validate skill name
            is_valid, error = SkillValidator.validate_skill_name(name)
            if not is_valid:
                click.echo(f"❌ {error}", err=True)
                continue

            return name

    def _prompt_description(self) -> Optional[str]:
        """
        Prompt for skill description with usage context hints.

        Returns:
            Description or None if cancelled

        Examples:
            >>> wizard = SkillWizard()
            >>> desc = wizard._prompt_description()
            Description: Extract text from PDFs. Use when working with PDF files.
        """
        # Show usage context hint
        click.echo("\n💡 Include when to use this skill:")
        click.echo('   Examples: "Use when...", "for processing...", "if working with..."\n')

        while True:
            description = questionary.text(
                "Skill description (what does it do and when to use it):",
                style=CUSTOM_STYLE,
                validate=lambda text: len(text.strip()) > 0 or "Description cannot be empty",
            ).ask()

            if description is None:  # User cancelled
                return None

            # Validate description (must include usage context)
            is_valid, error = SkillValidator.validate_description(description)
            if not is_valid:
                click.echo(f"❌ {error}", err=True)
                click.echo(
                    '   Tip: Add "Use when..." or "for..." to describe when Claude should use this skill\n'
                )
                continue

            return description.strip()

    def _prompt_scope(self) -> Optional[ScopeType]:
        """
        Prompt for skill scope.

        Returns:
            ScopeType or None if cancelled

        Examples:
            >>> wizard = SkillWizard()
            >>> scope = wizard._prompt_scope()
            Scope: Project (.claude/skills/)
        """
        scope_str = questionary.select(
            "Skill scope:",
            choices=[
                questionary.Choice("Project (.claude/skills/) - Team-shared, committed", "project"),
                questionary.Choice(
                    "Global (~/.claude/skills/) - User-wide, all projects", "global"
                ),
                questionary.Choice(
                    "Local (.claude/skills/) - Project-local, not committed", "local"
                ),
            ],
            style=CUSTOM_STYLE,
        ).ask()

        if scope_str is None:
            return None

        return ScopeType(scope_str)

    def _prompt_template(self) -> Optional[str]:
        """
        Prompt for template selection.

        Returns:
            Template name or None if cancelled

        Examples:
            >>> wizard = SkillWizard()
            >>> template = wizard._prompt_template()
            Template: with_tools
        """
        templates = self.template_manager.list_templates()

        if not templates:
            click.echo("⚠️  No templates found. Using 'basic' template.", err=True)
            return "basic"

        # Build choices with descriptions
        choices = []
        template_descriptions = {
            "basic": "Simple skill with description only",
            "with_tools": "Skill with allowed-tools restriction",
            "with_scripts": "Skill with scripts/ directory for helper files",
            "advanced": "Full-featured skill with all options",
        }

        for tmpl in templates:
            desc = template_descriptions.get(tmpl, "Custom template")
            choices.append(questionary.Choice(f"{tmpl} - {desc}", tmpl))

        template = questionary.select(
            "Template:",
            choices=choices,
            style=CUSTOM_STYLE,
        ).ask()

        return template

    def _prompt_allowed_tools(self) -> List[str]:
        """
        Prompt for allowed tools selection (multi-select checkbox).

        Returns:
            List of selected tool names (empty if none selected or cancelled)

        Examples:
            >>> wizard = SkillWizard()
            >>> tools = wizard._prompt_allowed_tools()
            Allowed tools: [x] Read  [x] Bash  [ ] Write
        """
        add_tools = questionary.confirm(
            "Restrict which tools this skill can use?",
            default=False,
            style=CUSTOM_STYLE,
        ).ask()

        if not add_tools:
            return []

        # Show tip about tool restrictions
        click.echo("\n💡 Restricting tools limits what Claude can do when using this skill")
        click.echo("   Only select tools that are essential for this skill's purpose\n")

        # Get available tools from validator
        available_tools = sorted(SkillValidator.ALLOWED_TOOLS)

        # Create checkbox choices
        selected_tools = questionary.checkbox(
            "Select allowed tools (use Space to select, Enter to confirm):",
            choices=available_tools,
            style=CUSTOM_STYLE,
        ).ask()

        if selected_tools is None:
            return []

        return selected_tools

    def _prompt_additional_files(self) -> bool:
        """
        Prompt for additional files (scripts/ directory support).

        Returns:
            True if user wants scripts/ directory, False otherwise

        Examples:
            >>> wizard = SkillWizard()
            >>> has_scripts = wizard._prompt_additional_files()
            Add scripts/ directory for helper files? No
        """
        # Show tip about scripts directory
        click.echo("\n💡 The scripts/ directory can contain helper scripts, configs, or data files")
        click.echo("   Example: python scripts, shell scripts, JSON configs, etc.\n")

        has_scripts = questionary.confirm(
            "Add scripts/ directory for helper files?",
            default=False,
            style=CUSTOM_STYLE,
        ).ask()

        return has_scripts if has_scripts is not None else False

    def _preview_and_confirm(self, config: SkillConfig, has_scripts: bool = False) -> bool:
        """
        Preview configuration and confirm creation.

        Args:
            config: Skill configuration
            has_scripts: Whether to create scripts/ directory

        Returns:
            True if user confirms, False otherwise

        Examples:
            >>> wizard = SkillWizard()
            >>> config = SkillConfig(name="test", description="Test skill", scope=ScopeType.PROJECT)
            >>> confirmed = wizard._preview_and_confirm(config)
        """
        click.echo("\n" + "=" * 60)
        click.echo("📋 Skill Preview")
        click.echo("=" * 60)
        click.echo(f"Name:        {config.name}")
        click.echo(f"Description: {config.description}")
        click.echo(f"Scope:       {config.scope.value}")
        click.echo(f"Template:    {config.template}")

        if config.allowed_tools:
            click.echo(f"Allowed tools: {len(config.allowed_tools)} tools")
            for tool in config.allowed_tools:
                click.echo(f"  - {tool}")
        else:
            click.echo("Allowed tools: All tools (unrestricted)")

        if has_scripts:
            click.echo("Scripts directory: ✓ Will be created")

        # Show installation path
        scope_paths = {
            ScopeType.GLOBAL: "~/.claude/skills/",
            ScopeType.PROJECT: ".claude/skills/",
            ScopeType.LOCAL: ".claude/skills/ (not committed)",
        }
        install_path = scope_paths.get(config.scope, ".claude/skills/")
        click.echo(f"\nInstallation path: {install_path}{config.name}/")

        click.echo("=" * 60 + "\n")

        return questionary.confirm(
            "Create this skill?",
            default=True,
            style=CUSTOM_STYLE,
        ).ask()
