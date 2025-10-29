"""
Interactive CLI wizard for agent creation.

Provides a beautiful, user-friendly agent creation experience using questionary
for interactive prompts with validation and real-time feedback.

This wizard guides users through:
1. Agent name (with validation)
2. Description (must include usage context)
3. Scope (global/project/local)
4. Claude model selection (Haiku/Sonnet/Opus)
5. Template selection
6. Preview and confirmation
"""

from pathlib import Path
from typing import List, Optional

import click
import questionary
from questionary import Style

from src.tools.agent_builder.builder import AgentBuilder
from src.tools.agent_builder.catalog import CatalogManager
from src.tools.agent_builder.exceptions import AgentBuilderError
from src.tools.agent_builder.models import AgentConfig, ScopeType, ModelType
from src.tools.agent_builder.templates import TemplateManager
from src.tools.agent_builder.validator import AgentValidator

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


class AgentWizard:
    """Interactive wizard for creating Claude Code agents."""

    def __init__(
        self,
        template_manager: Optional[TemplateManager] = None,
        builder: Optional[AgentBuilder] = None,
        catalog_manager: Optional[CatalogManager] = None,
    ):
        """
        Initialize agent wizard.

        Args:
            template_manager: Template manager
            builder: Agent builder
            catalog_manager: Catalog manager
        """
        self.template_manager = template_manager or TemplateManager()
        self.builder = builder  # Will be initialized with correct base_dir later
        self.catalog_manager = catalog_manager or CatalogManager()

    def run(self, project_root: Optional[Path] = None) -> Optional[AgentConfig]:
        """
        Run the interactive wizard.

        Args:
            project_root: Project root directory

        Returns:
            AgentConfig or None if cancelled

        Examples:
            >>> wizard = AgentWizard()
            >>> config = wizard.run()
            >>> if config:
            ...     print(f"Agent created: {config.name}")
        """
        click.echo("\n🤖 Claude Code Agent Builder - Interactive Wizard\n")

        try:
            # Step 1: Agent name
            name = self._prompt_agent_name()
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

            # Step 4: Claude model selection
            model = self._prompt_model()
            if not model:
                return None

            # Step 5: Template
            template = self._prompt_template()
            if not template:
                return None

            # Build configuration
            config = AgentConfig(
                name=name,
                description=description,
                scope=scope,
                model=model,
                template=template,
            )

            # Step 6: Preview and confirm
            if not self._preview_and_confirm(config):
                return None

            return config

        except KeyboardInterrupt:
            click.echo("\n\n❌ Wizard cancelled by user")
            return None
        except Exception as e:
            click.echo(f"\n\n❌ Error: {e}", err=True)
            return None

    def _prompt_agent_name(self) -> Optional[str]:
        """
        Prompt for agent name with validation.

        Returns:
            Agent name or None if cancelled

        Examples:
            >>> wizard = AgentWizard()
            >>> name = wizard._prompt_agent_name()
            Agent name (lowercase-with-hyphens): plan-agent
        """
        # Show naming convention hint
        click.echo("\n💡 Naming convention: lowercase-with-hyphens")
        click.echo("   Examples: plan-agent, code-reviewer, feature-implementer\n")

        while True:
            name = questionary.text(
                "Agent name (lowercase-with-hyphens):",
                style=CUSTOM_STYLE,
                validate=lambda text: AgentValidator.validate_agent_name(text)[0]
                or AgentValidator.validate_agent_name(text)[1],
            ).ask()

            if name is None:  # User cancelled
                return None

            # Validate agent name
            is_valid, error = AgentValidator.validate_agent_name(name)
            if not is_valid:
                click.echo(f"❌ {error}", err=True)
                continue

            return name

    def _prompt_description(self) -> Optional[str]:
        """
        Prompt for agent description with usage context hints.

        Returns:
            Description or None if cancelled

        Examples:
            >>> wizard = AgentWizard()
            >>> desc = wizard._prompt_description()
            Description: Strategic planning agent. Use when defining architecture.
        """
        # Show usage context hint
        click.echo("\n💡 Include when to use this agent:")
        click.echo('   Examples: "Use when...", "for defining...", "during planning..."\n')

        while True:
            description = questionary.text(
                "Agent description (what does it do and when to use it):",
                style=CUSTOM_STYLE,
                validate=lambda text: len(text.strip()) > 0 or "Description cannot be empty",
            ).ask()

            if description is None:  # User cancelled
                return None

            # Validate description (must include usage context)
            is_valid, error = AgentValidator.validate_description(description)
            if not is_valid:
                click.echo(f"❌ {error}", err=True)
                click.echo(
                    '   Tip: Add "Use when..." or "for..." to describe when Claude should use this agent\n'
                )
                continue

            return description.strip()

    def _prompt_scope(self) -> Optional[ScopeType]:
        """
        Prompt for installation scope.

        Returns:
            ScopeType or None if cancelled

        Examples:
            >>> wizard = AgentWizard()
            >>> scope = wizard._prompt_scope()
        """
        click.echo("\n💡 Scope determines where the agent will be installed:")
        click.echo("   • global: Available in all projects (~/.claude/agents/)")
        click.echo("   • project: Available in this project (.claude/agents/, committed)")
        click.echo("   • local: Available locally (.claude/agents/, not committed)\n")

        choice = questionary.select(
            "Installation scope:",
            choices=[
                {"name": "🌐 global - Available in all projects", "value": ScopeType.GLOBAL},
                {
                    "name": "📦 project - Available in this project (committed)",
                    "value": ScopeType.PROJECT,
                },
                {
                    "name": "💻 local - Available locally (not committed)",
                    "value": ScopeType.LOCAL,
                },
            ],
            style=CUSTOM_STYLE,
        ).ask()

        return choice

    def _prompt_model(self) -> Optional[ModelType]:
        """
        Prompt for Claude model selection.

        Returns:
            ModelType or None if cancelled

        Examples:
            >>> wizard = AgentWizard()
            >>> model = wizard._prompt_model()
        """
        click.echo("\n💡 Choose Claude model for this agent:")
        click.echo("   • Haiku: Fast, cost-effective for simple tasks")
        click.echo("   • Sonnet: Balanced performance and quality (recommended)")
        click.echo("   • Opus: Most capable for complex reasoning\n")

        choice = questionary.select(
            "Claude model:",
            choices=[
                {
                    "name": "⚡ Haiku (claude-3-5-haiku-20241022) - Fast, cost-effective",
                    "value": ModelType.HAIKU,
                },
                {
                    "name": "🎯 Sonnet (claude-3-5-sonnet-20241022) - Recommended",
                    "value": ModelType.SONNET,
                },
                {
                    "name": "🧠 Opus (claude-opus-4-20250514) - Most capable",
                    "value": ModelType.OPUS,
                },
            ],
            style=CUSTOM_STYLE,
        ).ask()

        return choice

    def _prompt_template(self) -> Optional[str]:
        """
        Prompt for template selection.

        Returns:
            Template name or None if cancelled

        Examples:
            >>> wizard = AgentWizard()
            >>> template = wizard._prompt_template()
        """
        click.echo("\n💡 Templates provide agent structure:")
        click.echo("   • basic: Standard agent template (recommended)")
        click.echo("   • advanced: Advanced agent with additional sections\n")

        # Get available templates
        available_templates = ["basic", "advanced"]  # Placeholder - templates not yet implemented

        choice = questionary.select(
            "Agent template:",
            choices=[
                {"name": "📝 basic - Standard agent template (recommended)", "value": "basic"},
                {"name": "🚀 advanced - Advanced agent features", "value": "advanced"},
            ],
            style=CUSTOM_STYLE,
        ).ask()

        return choice

    def _preview_and_confirm(self, config: AgentConfig) -> bool:
        """
        Preview configuration and ask for confirmation.

        Args:
            config: Agent configuration to preview

        Returns:
            True if confirmed, False otherwise

        Examples:
            >>> wizard = AgentWizard()
            >>> config = AgentConfig(...)
            >>> confirmed = wizard._preview_and_confirm(config)
        """
        click.echo("\n" + "=" * 60)
        click.echo("📋 Agent Configuration Preview")
        click.echo("=" * 60)
        click.echo(f"\n  Name:        {config.name}")
        click.echo(f"  Description: {config.description}")
        click.echo(f"  Scope:       {config.scope.value}")
        click.echo(f"  Model:       {config.model.value}")
        click.echo(f"  Template:    {config.template}")
        click.echo("\n" + "=" * 60 + "\n")

        confirmed = questionary.confirm(
            "Create this agent?", default=True, style=CUSTOM_STYLE
        ).ask()

        return confirmed if confirmed is not None else False

    def create_agent_from_config(
        self, config: AgentConfig, project_root: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Create agent from configuration.

        Args:
            config: Agent configuration
            project_root: Project root directory

        Returns:
            Path to created agent file or None on failure

        Examples:
            >>> wizard = AgentWizard()
            >>> config = AgentConfig(...)
            >>> path = wizard.create_agent_from_config(config)
        """
        try:
            # Determine base directory from scope
            if config.scope == ScopeType.GLOBAL:
                from src.core.scope_manager import ScopeManager

                scope_manager = ScopeManager()
                base_dir = scope_manager.get_global_path() / "agents"
            else:
                # Project or local scope
                if project_root is None:
                    project_root = Path.cwd()
                base_dir = project_root / ".claude" / "agents"

            # Ensure base directory exists
            base_dir.mkdir(parents=True, exist_ok=True)

            # Initialize builder with correct base_dir
            builder = AgentBuilder(base_dir=base_dir)

            # Create agent
            entry = builder.create_agent(config)

            # Add to catalog
            self.catalog_manager.add_agent(entry)

            click.echo(f"\n✅ Agent '{config.name}' created successfully!")
            click.echo(f"   Location: {entry.path}")
            click.echo(f"   Scope: {config.scope.value}")
            click.echo(f"   Model: {config.model.value}")

            return entry.path

        except AgentBuilderError as e:
            click.echo(f"\n❌ Failed to create agent: {e}", err=True)
            return None
        except Exception as e:
            click.echo(f"\n❌ Unexpected error: {e}", err=True)
            return None
