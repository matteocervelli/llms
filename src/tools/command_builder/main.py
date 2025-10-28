"""
Command Builder CLI.

Command-line interface for creating and managing Claude Code slash commands.

Usage:
    command-builder create                    # Interactive wizard
    command-builder generate --name my-cmd    # Non-interactive
    command-builder list                      # List commands
    command-builder delete my-cmd             # Delete command
"""

from pathlib import Path
from typing import Optional

import click
from pydantic import ValidationError as PydanticValidationError

from .builder import CommandBuilder
from .catalog import CatalogManager
from .exceptions import (
    CatalogError,
    CommandBuilderError,
    CommandExistsError,
    CommandNotFoundError,
)
from .models import CommandCatalogEntry, CommandConfig, ScopeType
from .templates import TemplateManager
from .wizard import CommandWizard


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Command Builder - Create Claude Code slash commands."""
    pass


@cli.command()
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def create(project_root: Optional[str]):
    """Create a new command using interactive wizard."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        wizard = CommandWizard()
        config = wizard.run(project_path)

        if config is None:
            click.echo("Command creation cancelled")
            return

        # Build command
        builder = CommandBuilder()
        command_path, content = builder.build_command(config, project_path)

        # Add to catalog
        catalog_manager = CatalogManager()
        entry = CommandCatalogEntry(
            name=config.name,
            description=config.description,
            scope=config.scope,
            path=str(command_path.resolve()),
            metadata={
                "template": config.template,
                "has_parameters": len(config.parameters) > 0,
                "has_bash": len(config.bash_commands) > 0,
                "has_files": len(config.file_references) > 0,
                "thinking_mode": config.thinking_mode,
            },
        )
        catalog_manager.add_command(entry)

        click.echo(f"\n✅ Command created successfully!")
        click.echo(f"📄 File: {command_path}")
        click.echo(f"🔍 Scope: {config.scope.value}")
        click.echo(f"\n💡 Use: /{config.name}")

    except CommandExistsError as e:
        click.echo(f"❌ Error: {e}", err=True)
        click.echo("Use --overwrite to replace existing command", err=True)
        raise click.Abort()
    except CommandBuilderError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--name", required=True, help="Command name")
@click.option("--description", required=True, help="Command description")
@click.option(
    "--scope",
    type=click.Choice(["global", "project", "local"]),
    default="project",
    help="Command scope",
)
@click.option(
    "--template",
    default="basic",
    help="Template to use",
)
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
@click.option("--overwrite", is_flag=True, help="Overwrite existing command")
def generate(
    name: str,
    description: str,
    scope: str,
    template: str,
    project_root: Optional[str],
    overwrite: bool,
):
    """Generate a command non-interactively."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        # Build configuration
        config = CommandConfig(
            name=name,
            description=description,
            scope=ScopeType(scope),
            template=template,
        )

        # Build command
        builder = CommandBuilder()
        command_path, content = builder.build_command(config, project_path, overwrite=overwrite)

        # Add to catalog
        catalog_manager = CatalogManager()
        entry = CommandCatalogEntry(
            name=config.name,
            description=config.description,
            scope=config.scope,
            path=str(command_path.resolve()),
            metadata={
                "template": config.template,
                "has_parameters": False,
                "has_bash": False,
                "has_files": False,
                "thinking_mode": False,
            },
        )
        catalog_manager.add_command(entry)

        click.echo(f"✅ Command '{name}' created at {command_path}")
        click.echo(f"💡 Use: /{name}")

    except PydanticValidationError as e:
        click.echo(f"❌ Validation error: {e}", err=True)
        raise click.Abort()
    except CommandExistsError as e:
        click.echo(f"❌ Error: {e}", err=True)
        click.echo("Use --overwrite to replace existing command", err=True)
        raise click.Abort()
    except CommandBuilderError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option(
    "--scope",
    type=click.Choice(["global", "project", "local", "all"]),
    default="all",
    help="Filter by scope",
)
@click.option("--search", help="Search in name and description")
def list(scope: str, search: Optional[str]):
    """List all commands in catalog."""
    try:
        catalog_manager = CatalogManager()

        scope_filter = None if scope == "all" else ScopeType(scope)

        if search:
            commands = catalog_manager.search_commands(query=search, scope=scope_filter)
        else:
            commands = catalog_manager.list_commands(scope=scope_filter)

        if not commands:
            click.echo("No commands found")
            return

        click.echo(f"\n📋 Commands ({len(commands)} total):\n")

        for cmd in commands:
            scope_badge = {
                ScopeType.GLOBAL: "🌐",
                ScopeType.PROJECT: "📁",
                ScopeType.LOCAL: "🔒",
            }.get(cmd.scope, "❓")

            click.echo(f"{scope_badge} /{cmd.name}")
            click.echo(f"   {cmd.description}")
            click.echo(f"   Scope: {cmd.scope.value} | Path: {cmd.path}")

            features = []
            if cmd.metadata.get("has_parameters"):
                features.append("params")
            if cmd.metadata.get("has_bash"):
                features.append("bash")
            if cmd.metadata.get("has_files"):
                features.append("files")
            if cmd.metadata.get("thinking_mode"):
                features.append("thinking")

            if features:
                click.echo(f"   Features: {', '.join(features)}")

            click.echo()

        # Show stats
        stats = catalog_manager.get_catalog_stats()
        click.echo("─" * 60)
        click.echo(f"Total: {stats['total_commands']} commands")
        click.echo(
            f"By scope: {stats['by_scope']['global']} global, "
            f"{stats['by_scope']['project']} project, {stats['by_scope']['local']} local"
        )

    except CatalogError as e:
        click.echo(f"❌ Error reading catalog: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("name")
@click.option(
    "--scope",
    type=click.Choice(["global", "project", "local"]),
    help="Scope if multiple commands with same name",
)
@click.option("--yes", is_flag=True, help="Skip confirmation")
def delete(name: str, scope: Optional[str], yes: bool):
    """Delete a command."""
    try:
        catalog_manager = CatalogManager()

        scope_filter = ScopeType(scope) if scope else None
        entry = catalog_manager.get_command(name=name, scope=scope_filter)

        if not entry:
            click.echo(f"❌ Command '{name}' not found", err=True)
            raise click.Abort()

        if not yes:
            if not click.confirm(f"Delete command '{name}' from {entry.scope.value} scope?"):
                click.echo("Deletion cancelled")
                return

        # Delete file
        command_path = Path(entry.path)
        if command_path.exists():
            command_path.unlink()

        # Remove from catalog
        catalog_manager.remove_command(entry.id)

        click.echo(f"✅ Command '{name}' deleted successfully")

    except CatalogError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("path", type=click.Path(exists=True))
def validate(path: str):
    """Validate a command file."""
    try:
        builder = CommandBuilder()
        command_path = Path(path)

        is_valid, error = builder.validate_command_file(command_path)

        if is_valid:
            click.echo(f"✅ Command file is valid: {command_path}")
        else:
            click.echo(f"❌ Command file is invalid: {error}", err=True)
            raise click.Abort()

    except Exception as e:
        click.echo(f"❌ Error validating command: {e}", err=True)
        raise click.Abort()


@cli.command()
def templates():
    """List available templates."""
    try:
        template_manager = TemplateManager()
        available_templates = template_manager.list_templates()

        if not available_templates:
            click.echo("No templates found")
            return

        click.echo("\n📝 Available Templates:\n")

        template_descriptions = {
            "basic": "Simple command with description and parameters",
            "with_bash": "Command with bash command execution (!command)",
            "with_files": "Command with file references (@file)",
            "advanced": "Full-featured command with all options",
        }

        for tmpl in available_templates:
            desc = template_descriptions.get(tmpl, "Custom template")
            click.echo(f"  • {tmpl}")
            click.echo(f"    {desc}\n")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
def stats():
    """Show catalog statistics."""
    try:
        catalog_manager = CatalogManager()
        stats = catalog_manager.get_catalog_stats()

        click.echo("\n📊 Command Builder Statistics\n")
        click.echo(f"Total commands: {stats['total_commands']}")
        click.echo("\nBy scope:")
        click.echo(f"  🌐 Global:  {stats['by_scope']['global']}")
        click.echo(f"  📁 Project: {stats['by_scope']['project']}")
        click.echo(f"  🔒 Local:   {stats['by_scope']['local']}")
        click.echo("\nBy features:")
        click.echo(f"  With parameters:  {stats['with_parameters']}")
        click.echo(f"  With bash:        {stats['with_bash']}")
        click.echo(f"  With files:       {stats['with_files']}")

    except CatalogError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option(
    "--project-root",
    type=click.Path(exists=True),
    help="Project root directory",
)
def sync(project_root: Optional[str]):
    """
    Sync catalog with actual command files.

    Scans command directories and updates the catalog:
    - Removes entries for missing files
    - Adds entries for untracked files

    Useful when files are manually added or deleted.
    """
    try:
        project_path = Path(project_root) if project_root else Path.cwd()

        catalog_manager = CatalogManager()

        click.echo("🔄 Syncing catalog with command files...")

        result = catalog_manager.sync_catalog(project_path)

        # Show results
        if result["removed"]:
            click.echo(f"\n❌ Removed {len(result['removed'])} commands:")
            for name in result["removed"]:
                click.echo(f"   - {name}")

        if result["added"]:
            click.echo(f"\n✅ Added {len(result['added'])} commands:")
            for name in result["added"]:
                click.echo(f"   + {name}")

        if result["unchanged"]:
            click.echo(f"\n📝 {result['unchanged']} commands unchanged")

        if not result["removed"] and not result["added"]:
            click.echo("\n✨ Catalog is already in sync!")
        else:
            click.echo("\n✅ Catalog sync complete!")

    except CatalogError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
