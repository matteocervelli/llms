"""
Interactive CLI wizard for command creation.

Provides a beautiful, user-friendly command creation experience using questionary
for interactive prompts with validation and real-time feedback.
"""

from pathlib import Path
from typing import List, Optional

import click
import questionary
from questionary import Style

from .builder import CommandBuilder
from .catalog import CatalogManager
from .exceptions import CommandBuilderError
from .models import CommandConfig, CommandParameter, ParameterType, ScopeType
from .templates import TemplateManager
from .validator import Validator

# Custom style for questionary prompts
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


class CommandWizard:
    """Interactive wizard for creating Claude Code slash commands."""

    def __init__(
        self,
        template_manager: Optional[TemplateManager] = None,
        builder: Optional[CommandBuilder] = None,
        catalog_manager: Optional[CatalogManager] = None,
    ):
        """
        Initialize command wizard.

        Args:
            template_manager: Template manager
            builder: Command builder
            catalog_manager: Catalog manager
        """
        self.template_manager = template_manager or TemplateManager()
        self.builder = builder or CommandBuilder(self.template_manager)
        self.catalog_manager = catalog_manager or CatalogManager()

    def run(self, project_root: Optional[Path] = None) -> Optional[CommandConfig]:
        """
        Run the interactive wizard.

        Args:
            project_root: Project root directory

        Returns:
            CommandConfig or None if cancelled
        """
        click.echo("\n🚀 Claude Code Command Builder - Interactive Wizard\n")

        try:
            # Step 1: Command name
            name = self._prompt_command_name()
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

            # Step 5: Parameters (optional)
            parameters = self._prompt_parameters()

            # Step 6: Bash commands (optional)
            bash_commands = self._prompt_bash_commands(project_root)

            # Step 7: File references (optional)
            file_references = self._prompt_file_references(project_root)

            # Step 8: Thinking mode
            thinking_mode = self._prompt_thinking_mode()

            # Step 9: Additional frontmatter (optional)
            frontmatter = self._prompt_additional_frontmatter()

            # Build configuration
            config = CommandConfig(
                name=name,
                description=description,
                scope=scope,
                template=template,
                parameters=parameters,
                bash_commands=bash_commands,
                file_references=file_references,
                thinking_mode=thinking_mode,
                frontmatter=frontmatter,
            )

            # Step 10: Preview and confirm
            if not self._preview_and_confirm(config):
                return None

            return config

        except KeyboardInterrupt:
            click.echo("\n\n❌ Wizard cancelled by user")
            return None
        except Exception as e:
            click.echo(f"\n\n❌ Error: {e}", err=True)
            return None

    def _prompt_command_name(self) -> Optional[str]:
        """Prompt for command name with validation."""
        # Show naming convention hint
        click.echo("\n💡 Naming convention: [context-]object-action[-modifier]")
        click.echo("   Examples: cc-command-create, feature-implement, gh-milestone-create\n")

        while True:
            name = questionary.text(
                "Command name (slug format: lowercase-with-hyphens):",
                style=CUSTOM_STYLE,
                validate=lambda text: Validator.validate_command_name(text)[0]
                or Validator.validate_command_name(text)[1],
            ).ask()

            if name is None:  # User cancelled
                return None

            # First check basic format
            is_valid, error = Validator.validate_command_name(name)
            if not is_valid:
                click.echo(f"❌ {error}", err=True)
                continue

            # Then check naming convention (permissive by default)
            is_compliant, convention_error, warnings = Validator.validate_naming_convention(
                name, strict=False
            )

            if warnings:
                click.echo("\n⚠️  Naming convention notes:")
                for warning in warnings:
                    if warning.startswith("✓"):
                        click.echo(f"   {warning}")
                    else:
                        click.echo(f"   ⚠️  {warning}")

                # Ask if user wants to proceed
                proceed = questionary.confirm(
                    "\nProceed with this name?",
                    default=True,
                    style=CUSTOM_STYLE,
                ).ask()

                if not proceed:
                    continue

            return name

    def _prompt_description(self) -> Optional[str]:
        """Prompt for command description."""
        description = questionary.text(
            "Command description (what does it do?):",
            style=CUSTOM_STYLE,
            validate=lambda text: len(text.strip()) > 0 or "Description cannot be empty",
        ).ask()

        return description.strip() if description else None

    def _prompt_scope(self) -> Optional[ScopeType]:
        """Prompt for command scope."""
        scope_str = questionary.select(
            "Command scope:",
            choices=[
                questionary.Choice("Project (.claude/commands/) - Team-shared", "project"),
                questionary.Choice("Global (~/.claude/commands/) - User-wide", "global"),
                questionary.Choice("Local (.claude/commands/) - Not committed", "local"),
            ],
            style=CUSTOM_STYLE,
        ).ask()

        if scope_str is None:
            return None

        return ScopeType(scope_str)

    def _prompt_template(self) -> Optional[str]:
        """Prompt for template selection."""
        templates = self.template_manager.list_templates()

        if not templates:
            click.echo("⚠️  No templates found. Using 'basic' template.", err=True)
            return "basic"

        # Build choices with descriptions
        choices = []
        template_descriptions = {
            "basic": "Simple command with description and parameters",
            "with_bash": "Command with bash command execution (!command)",
            "with_files": "Command with file references (@file)",
            "advanced": "Full-featured command with all options",
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

    def _prompt_parameters(self) -> List[CommandParameter]:
        """Prompt for command parameters."""
        add_params = questionary.confirm(
            "Add parameters to your command?",
            default=False,
            style=CUSTOM_STYLE,
        ).ask()

        if not add_params:
            return []

        parameters = []

        while True:
            param = self._prompt_single_parameter()
            if param is None:
                break

            parameters.append(param)

            if not questionary.confirm(
                "Add another parameter?",
                default=False,
                style=CUSTOM_STYLE,
            ).ask():
                break

        return parameters

    def _prompt_single_parameter(self) -> Optional[CommandParameter]:
        """Prompt for a single parameter."""
        click.echo("\n--- Parameter Configuration ---")

        # Parameter name
        param_name = questionary.text(
            "Parameter name (lowercase_with_underscores):",
            style=CUSTOM_STYLE,
            validate=lambda text: bool(text.strip()) or "Parameter name cannot be empty",
        ).ask()

        if not param_name:
            return None

        # Parameter type
        param_type_str = questionary.select(
            "Parameter type:",
            choices=["string", "number", "boolean", "choice"],
            style=CUSTOM_STYLE,
        ).ask()

        if not param_type_str:
            return None

        param_type = ParameterType(param_type_str)

        # Parameter description
        param_desc = questionary.text(
            "Parameter description:",
            style=CUSTOM_STYLE,
            validate=lambda text: bool(text.strip()) or "Description cannot be empty",
        ).ask()

        if not param_desc:
            return None

        # Required?
        param_required = questionary.confirm(
            "Is this parameter required?",
            default=False,
            style=CUSTOM_STYLE,
        ).ask()

        # Default value (only if not required)
        param_default = None
        if not param_required:
            add_default = questionary.confirm(
                "Add a default value?",
                default=False,
                style=CUSTOM_STYLE,
            ).ask()

            if add_default:
                param_default = questionary.text(
                    "Default value:",
                    style=CUSTOM_STYLE,
                ).ask()

        # Choices (only for choice type)
        param_choices = None
        if param_type == ParameterType.CHOICE:
            choices_input = questionary.text(
                "Choices (comma-separated):",
                style=CUSTOM_STYLE,
                validate=lambda text: bool(text.strip()) or "Choices cannot be empty",
            ).ask()

            if choices_input:
                param_choices = [c.strip() for c in choices_input.split(",") if c.strip()]

        return CommandParameter(
            name=param_name,
            type=param_type,
            description=param_desc,
            required=param_required,
            default=param_default,
            choices=param_choices,
        )

    def _prompt_bash_commands(self, project_root: Optional[Path]) -> List[str]:
        """Prompt for bash commands."""
        add_bash = questionary.confirm(
            "Add bash command execution (!command syntax)?",
            default=False,
            style=CUSTOM_STYLE,
        ).ask()

        if not add_bash:
            return []

        commands = []

        while True:
            cmd = questionary.text(
                "Bash command (will be prefixed with !):",
                style=CUSTOM_STYLE,
            ).ask()

            if not cmd or not cmd.strip():
                break

            # Validate command safety
            is_safe, error, warnings = Validator.validate_bash_command(cmd)

            if not is_safe:
                click.echo(f"❌ Unsafe command: {error}", err=True)
                if not questionary.confirm("Try again?", default=True, style=CUSTOM_STYLE).ask():
                    break
                continue

            if warnings:
                click.echo("⚠️  Warnings:", err=True)
                for warning in warnings:
                    click.echo(f"   - {warning}", err=True)

                if not questionary.confirm(
                    "Add this command anyway?",
                    default=True,
                    style=CUSTOM_STYLE,
                ).ask():
                    continue

            commands.append(cmd)

            if not questionary.confirm(
                "Add another bash command?",
                default=False,
                style=CUSTOM_STYLE,
            ).ask():
                break

        return commands

    def _prompt_file_references(self, project_root: Optional[Path]) -> List[str]:
        """Prompt for file references."""
        add_files = questionary.confirm(
            "Add file references (@file syntax)?",
            default=False,
            style=CUSTOM_STYLE,
        ).ask()

        if not add_files:
            return []

        if project_root is None:
            project_root = Path.cwd()

        files = []

        while True:
            file_ref = questionary.text(
                "File reference (relative path from project root):",
                style=CUSTOM_STYLE,
            ).ask()

            if not file_ref or not file_ref.strip():
                break

            # Validate file reference
            is_valid, error = Validator.validate_file_reference(file_ref, project_root)

            if not is_valid:
                click.echo(f"❌ Invalid file reference: {error}", err=True)
                if not questionary.confirm("Try again?", default=True, style=CUSTOM_STYLE).ask():
                    break
                continue

            files.append(file_ref)

            if not questionary.confirm(
                "Add another file reference?",
                default=False,
                style=CUSTOM_STYLE,
            ).ask():
                break

        return files

    def _prompt_thinking_mode(self) -> bool:
        """Prompt for thinking mode."""
        return questionary.confirm(
            "Enable extended thinking mode?",
            default=False,
            style=CUSTOM_STYLE,
        ).ask()

    def _prompt_additional_frontmatter(self) -> dict:
        """Prompt for additional YAML frontmatter."""
        add_frontmatter = questionary.confirm(
            "Add additional YAML frontmatter fields?",
            default=False,
            style=CUSTOM_STYLE,
        ).ask()

        if not add_frontmatter:
            return {}

        click.echo("\nℹ️  Enter key-value pairs (empty key to finish)")
        frontmatter = {}

        while True:
            key = questionary.text(
                "Frontmatter key:",
                style=CUSTOM_STYLE,
            ).ask()

            if not key or not key.strip():
                break

            value = questionary.text(
                f"Value for '{key}':",
                style=CUSTOM_STYLE,
            ).ask()

            if value:
                frontmatter[key.strip()] = value.strip()

        return frontmatter

    def _preview_and_confirm(self, config: CommandConfig) -> bool:
        """Preview configuration and confirm creation."""
        click.echo("\n" + "=" * 60)
        click.echo("📋 Command Preview")
        click.echo("=" * 60)
        click.echo(f"Name:        {config.name}")
        click.echo(f"Description: {config.description}")
        click.echo(f"Scope:       {config.scope.value}")
        click.echo(f"Template:    {config.template}")

        if config.parameters:
            click.echo(f"Parameters:  {len(config.parameters)} parameters")
            for param in config.parameters:
                req = "required" if param.required else "optional"
                click.echo(f"  - {param.name} ({param.type.value}, {req}): {param.description}")

        if config.bash_commands:
            click.echo(f"Bash commands: {len(config.bash_commands)}")
            for cmd in config.bash_commands:
                click.echo(f"  !{cmd}")

        if config.file_references:
            click.echo(f"File references: {len(config.file_references)}")
            for ref in config.file_references:
                click.echo(f"  @{ref}")

        if config.thinking_mode:
            click.echo("Thinking mode: ✓ Enabled")

        if config.frontmatter:
            click.echo("Additional frontmatter:")
            for key, value in config.frontmatter.items():
                click.echo(f"  {key}: {value}")

        click.echo("=" * 60 + "\n")

        return questionary.confirm(
            "Create this command?",
            default=True,
            style=CUSTOM_STYLE,
        ).ask()
