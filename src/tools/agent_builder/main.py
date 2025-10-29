"""
Agent Builder CLI.

Command-line interface for creating and managing Claude Code agents.

Usage:
    python -m src.tools.agent_builder.main create                    # Interactive wizard
    python -m src.tools.agent_builder.main generate --name my-agent  # Non-interactive
    python -m src.tools.agent_builder.main list                      # List agents
    python -m src.tools.agent_builder.main delete my-agent           # Delete agent
    python -m src.tools.agent_builder.main search "planning"         # Search agents
    python -m src.tools.agent_builder.main stats                     # Catalog statistics
    python -m src.tools.agent_builder.main sync                      # Sync catalog with filesystem
    python -m src.tools.agent_builder.main validate agent-file.md    # Validate agent file
"""

from pathlib import Path
from typing import Optional

import click
from pydantic import ValidationError as PydanticValidationError

from src.tools.agent_builder.builder import AgentBuilder
from src.tools.agent_builder.catalog import CatalogManager
from src.tools.agent_builder.exceptions import (
    CatalogError,
    AgentBuilderError,
    AgentExistsError,
    AgentNotFoundError,
    TemplateError,
)
from src.tools.agent_builder.models import AgentConfig, ScopeType, ModelType
from src.tools.agent_builder.templates import TemplateManager
from src.tools.agent_builder.wizard import AgentWizard
from src.core.scope_manager import ScopeManager


def format_scope_badge(scope: ScopeType) -> str:
    """Format scope as colored badge."""
    badges = {
        ScopeType.GLOBAL: "🌐 global",
        ScopeType.PROJECT: "📦 project",
        ScopeType.LOCAL: "💻 local",
    }
    return badges.get(scope, str(scope))


def format_model_badge(model: ModelType) -> str:
    """Format model as colored badge."""
    badges = {
        ModelType.HAIKU: "⚡ Haiku",
        ModelType.SONNET: "🎯 Sonnet",
        ModelType.OPUS: "🧠 Opus",
    }
    return badges.get(model, str(model))


def format_agent_entry(entry, show_path: bool = False) -> str:
    """Format agent entry for display."""
    scope_badge = format_scope_badge(entry.scope)
    model_badge = format_model_badge(entry.model)

    output = f"""
  Name:        {entry.name}
  Description: {entry.description}
  Scope:       {scope_badge}
  Model:       {model_badge}
  Template:    {entry.metadata.get('template', 'unknown')}
  Created:     {entry.created_at.strftime('%Y-%m-%d %H:%M')}
"""

    if show_path:
        output += f"  Path:        {entry.path}\n"

    return output


@click.group()
@click.version_option(version="1.0.0")
def cli() -> None:
    """Agent Builder - Create Claude Code agents."""
    pass


@cli.command()
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def create(project_root: Optional[str]) -> None:
    """Create a new agent using interactive wizard."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        # Initialize wizard
        wizard = AgentWizard()

        # Run wizard
        config = wizard.run(project_path)

        if config is None:
            click.echo("✋ Agent creation cancelled")
            return

        # Create agent from config
        agent_path = wizard.create_agent_from_config(config, project_path)

        if agent_path:
            click.echo(f"\n💡 Agent is now available in Claude Code")

    except AgentExistsError as e:
        click.echo(f"❌ Error: {e}", err=True)
        click.echo("💡 Use 'delete' command first to replace existing agent", err=True)
        raise click.Abort()
    except AgentBuilderError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--name", required=True, help="Agent name (e.g., 'plan-agent')")
@click.option("--description", required=True, help="Agent description with usage context")
@click.option(
    "--scope",
    type=click.Choice(["global", "project", "local"]),
    default="project",
    help="Agent scope (default: project)",
)
@click.option(
    "--model",
    type=click.Choice(["haiku", "sonnet", "opus"]),
    default="sonnet",
    help="Claude model (default: sonnet)",
)
@click.option(
    "--template",
    type=click.Choice(["basic", "advanced"]),
    default="basic",
    help="Template to use (default: basic)",
)
@click.option("--dry-run", is_flag=True, help="Preview without creating files")
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def generate(
    name: str,
    description: str,
    scope: str,
    model: str,
    template: str,
    dry_run: bool,
    project_root: Optional[str],
) -> None:
    """Create a new agent non-interactively using CLI options."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        # Map model string to ModelType
        model_map = {
            "haiku": ModelType.HAIKU,
            "sonnet": ModelType.SONNET,
            "opus": ModelType.OPUS,
        }
        model_type = model_map[model]

        # Create config
        config = AgentConfig(
            name=name,
            description=description,
            scope=ScopeType(scope),
            model=model_type,
            template=template,
        )

        if dry_run:
            click.echo("🔍 Dry run - no files created")
            click.echo(f"\nWould create agent:")
            click.echo(f"  Name: {name}")
            click.echo(f"  Description: {description}")
            click.echo(f"  Scope: {format_scope_badge(config.scope)}")
            click.echo(f"  Model: {format_model_badge(model_type)}")
            click.echo(f"  Template: {template}")
            return

        # Determine base directory from scope
        if config.scope == ScopeType.GLOBAL:
            scope_manager = ScopeManager()
            base_dir = scope_manager.get_global_path() / "agents"
        else:
            base_dir = project_path / ".claude" / "agents"

        # Ensure base directory exists
        base_dir.mkdir(parents=True, exist_ok=True)

        # Create agent
        builder = AgentBuilder(base_dir=base_dir)
        entry = builder.create_agent(config)

        # Add to catalog
        catalog_mgr = CatalogManager(project_path / "agents.json")
        catalog_mgr.add_agent(entry)

        # Success message
        scope_badge = format_scope_badge(config.scope)
        model_badge = format_model_badge(model_type)
        click.echo(f"\n✅ Agent created successfully!")
        click.echo(f"📄 File: {entry.path}")
        click.echo(f"🔍 Scope: {scope_badge}")
        click.echo(f"🧠 Model: {model_badge}")
        click.echo(f"📝 Template: {template}")
        click.echo(f"\n💡 Agent is now available in Claude Code")

    except AgentExistsError as e:
        click.echo(f"❌ Error: {e}", err=True)
        click.echo("💡 Use 'delete' command first to replace existing agent", err=True)
        raise click.Abort()
    except PydanticValidationError as e:
        click.echo(f"❌ Validation error: {e}", err=True)
        raise click.Abort()
    except AgentBuilderError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command(name="list")
@click.option(
    "--scope",
    type=click.Choice(["all", "global", "project", "local"]),
    default="all",
    help="Filter by scope (default: all)",
)
@click.option("--search", help="Search query (matches name, description)")
@click.option("--template", help="Filter by template name")
@click.option(
    "--model",
    type=click.Choice(["haiku", "sonnet", "opus"]),
    help="Filter by Claude model",
)
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def list_agents(
    scope: str,
    search: Optional[str],
    template: Optional[str],
    model: Optional[str],
    project_root: Optional[str],
) -> None:
    """List all agents with optional filtering."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = CatalogManager(project_path / "agents.json")

        # Prepare filters
        scope_filter = None if scope == "all" else ScopeType(scope)
        model_filter = None
        if model:
            model_map = {
                "haiku": ModelType.HAIKU,
                "sonnet": ModelType.SONNET,
                "opus": ModelType.OPUS,
            }
            model_filter = model_map[model]

        # Search agents
        agents = catalog_mgr.search_agents(
            query=search,
            scope=scope_filter,
            model=model_filter,
            template=template,
        )

        if not agents:
            click.echo("📋 No agents found matching criteria")
            return

        # Display header
        click.echo(f"\n📋 Agents ({len(agents)} total):\n")
        click.echo("─" * 60)

        # Display each agent
        for agent in agents:
            click.echo(format_agent_entry(agent))
            click.echo("─" * 60)

        # Display filter info
        filters = []
        if scope != "all":
            filters.append(f"scope={scope}")
        if search:
            filters.append(f"search='{search}'")
        if template:
            filters.append(f"template={template}")
        if model:
            filters.append(f"model={model}")

        if filters:
            click.echo(f"\n🔍 Filters: {', '.join(filters)}")

    except CatalogError as e:
        click.echo(f"❌ Catalog error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("agent_name")
@click.option(
    "--scope",
    type=click.Choice(["global", "project", "local"]),
    help="Scope to search in (optional)",
)
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def delete(agent_name: str, scope: Optional[str], yes: bool, project_root: Optional[str]) -> None:
    """Delete an agent by name."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = CatalogManager(project_path / "agents.json")

        # Find agent in catalog
        scope_filter = ScopeType(scope) if scope else None
        agent = catalog_mgr.get_agent(name=agent_name, scope=scope_filter)

        if not agent:
            scope_msg = f" in {scope} scope" if scope else ""
            click.echo(f"❌ Agent '{agent_name}'{scope_msg} not found", err=True)
            raise click.Abort()

        # Show agent info
        click.echo(f"\n🗑️  Agent to delete:")
        click.echo(format_agent_entry(agent, show_path=True))

        # Confirm deletion
        if not yes:
            if not click.confirm("\n⚠️  Are you sure you want to delete this agent?"):
                click.echo("✋ Deletion cancelled")
                return

        # Delete agent file
        if agent.path.exists():
            agent.path.unlink()

        # Remove from catalog
        success = catalog_mgr.remove_agent(agent.id)

        if success:
            click.echo(f"\n✅ Agent '{agent_name}' deleted successfully")
        else:
            click.echo(f"❌ Failed to delete agent '{agent_name}'", err=True)
            raise click.Abort()

    except AgentNotFoundError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except AgentBuilderError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("query")
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def search(query: str, project_root: Optional[str]) -> None:
    """Search agents by query string."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = CatalogManager(project_path / "agents.json")

        # Search agents
        agents = catalog_mgr.search_agents(query=query)

        if not agents:
            click.echo(f"📋 No agents found matching '{query}'")
            return

        # Display results
        click.echo(f"\n🔍 Search results for '{query}' ({len(agents)} found):\n")
        click.echo("─" * 60)

        for agent in agents:
            click.echo(format_agent_entry(agent))
            click.echo("─" * 60)

    except CatalogError as e:
        click.echo(f"❌ Catalog error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def stats(project_root: Optional[str]) -> None:
    """Display catalog statistics."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = CatalogManager(project_path / "agents.json")

        # Get statistics
        stats_data = catalog_mgr.get_catalog_stats()

        # Display stats
        click.echo("\n📊 Agent Catalog Statistics\n")
        click.echo("=" * 60)
        click.echo(f"\n  Total agents: {stats_data['total']}")

        # By scope
        click.echo(f"\n  By scope:")
        click.echo(f"    🌐 Global:  {stats_data['by_scope']['global']}")
        click.echo(f"    📦 Project: {stats_data['by_scope']['project']}")
        click.echo(f"    💻 Local:   {stats_data['by_scope']['local']}")

        # By model
        if stats_data['by_model']:
            click.echo(f"\n  By model:")
            for model, count in stats_data['by_model'].items():
                model_type = ModelType(model)
                badge = format_model_badge(model_type)
                click.echo(f"    {badge}: {count}")

        # By template
        if stats_data['by_template']:
            click.echo(f"\n  By template:")
            for template, count in stats_data['by_template'].items():
                click.echo(f"    {template}: {count}")

        click.echo("\n" + "=" * 60)

    except CatalogError as e:
        click.echo(f"❌ Catalog error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def sync(project_root: Optional[str]) -> None:
    """Sync catalog with filesystem (add missing, remove orphaned)."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = CatalogManager(project_path / "agents.json")

        click.echo("\n🔄 Syncing catalog with filesystem...")

        # Perform sync
        report = catalog_mgr.sync_catalog(project_path)

        # Display results
        click.echo("\n📋 Sync Report:")
        click.echo("=" * 60)

        if report["added"]:
            click.echo(f"\n✅ Added {len(report['added'])} agent(s):")
            for name in report["added"]:
                click.echo(f"  + {name}")

        if report["removed"]:
            click.echo(f"\n🗑️  Removed {len(report['removed'])} orphaned agent(s):")
            for name in report["removed"]:
                click.echo(f"  - {name}")

        if report["errors"]:
            click.echo(f"\n❌ Errors ({len(report['errors'])}):")
            for error in report["errors"]:
                click.echo(f"  ! {error}")

        if not report["added"] and not report["removed"] and not report["errors"]:
            click.echo("\n✅ Catalog is already in sync")

        click.echo("\n" + "=" * 60)

    except CatalogError as e:
        click.echo(f"❌ Catalog error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("agent_path", type=click.Path(exists=True))
def validate(agent_path: str) -> None:
    """Validate an agent markdown file."""
    path = Path(agent_path)

    try:
        # Check file extension
        if not path.suffix == ".md":
            click.echo("❌ Agent file must have .md extension", err=True)
            raise click.Abort()

        # Try to parse frontmatter
        import yaml

        content = path.read_text()

        if not content.startswith("---"):
            click.echo("❌ Agent file must start with YAML frontmatter (---)", err=True)
            raise click.Abort()

        parts = content.split("---", 2)
        if len(parts) < 3:
            click.echo("❌ Invalid frontmatter format", err=True)
            raise click.Abort()

        frontmatter = yaml.safe_load(parts[1])

        # Validate required fields
        required_fields = ["name", "description", "model"]
        missing_fields = [f for f in required_fields if f not in frontmatter]

        if missing_fields:
            click.echo(f"❌ Missing required fields: {', '.join(missing_fields)}", err=True)
            raise click.Abort()

        # Validate name
        from src.tools.agent_builder.validator import AgentValidator

        is_valid, error = AgentValidator.validate_agent_name(frontmatter["name"])
        if not is_valid:
            click.echo(f"❌ Invalid name: {error}", err=True)
            raise click.Abort()

        # Validate description
        is_valid, error = AgentValidator.validate_description(frontmatter["description"])
        if not is_valid:
            click.echo(f"❌ Invalid description: {error}", err=True)
            raise click.Abort()

        # Validate model
        is_valid, error = AgentValidator.validate_model(frontmatter["model"])
        if not is_valid:
            click.echo(f"❌ Invalid model: {error}", err=True)
            raise click.Abort()

        # All validations passed
        click.echo(f"\n✅ Agent file '{path.name}' is valid!")
        click.echo(f"\n  Name:        {frontmatter['name']}")
        click.echo(f"  Description: {frontmatter['description']}")
        click.echo(f"  Model:       {frontmatter['model']}")

        if "template" in frontmatter:
            click.echo(f"  Template:    {frontmatter['template']}")

        click.echo("\n💡 Agent is ready to use in Claude Code")

    except yaml.YAMLError as e:
        click.echo(f"❌ YAML parsing error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Validation error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
