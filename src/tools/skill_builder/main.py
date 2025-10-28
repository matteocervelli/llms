"""
Skill Builder CLI.

Command-line interface for creating and managing Claude Code skills.

Usage:
    python -m src.tools.skill_builder.main create                    # Interactive wizard
    python -m src.tools.skill_builder.main generate --name my-skill  # Non-interactive
    python -m src.tools.skill_builder.main list                      # List skills
    python -m src.tools.skill_builder.main delete my-skill           # Delete skill
"""

from pathlib import Path
from typing import List, Optional

import click
from pydantic import ValidationError as PydanticValidationError

from src.core.scope_manager import ScopeManager
from .builder import SkillBuilder
from .catalog import CatalogManager
from .exceptions import (
    CatalogError,
    SkillBuilderError,
    SkillExistsError,
    SkillNotFoundError,
    TemplateError,
)
from .models import SkillCatalogEntry, SkillConfig, ScopeType
from .templates import TemplateManager
from .wizard import SkillWizard


# Helper functions for manager instantiation
def get_scope_manager() -> ScopeManager:
    """Get ScopeManager instance."""
    return ScopeManager()


def get_template_manager() -> TemplateManager:
    """Get TemplateManager instance."""
    return TemplateManager()


def get_catalog_manager(project_root: Optional[Path] = None) -> CatalogManager:
    """Get CatalogManager instance."""
    if project_root:
        catalog_path = project_root / "skills.json"
        return CatalogManager(catalog_path=catalog_path)
    return CatalogManager()


def get_builder(
    scope_manager: Optional[ScopeManager] = None,
    template_manager: Optional[TemplateManager] = None,
    catalog_manager: Optional[CatalogManager] = None,
) -> SkillBuilder:
    """Get SkillBuilder instance with dependencies."""
    scope_mgr = scope_manager or get_scope_manager()
    template_mgr = template_manager or get_template_manager()
    catalog_mgr = catalog_manager
    return SkillBuilder(
        scope_manager=scope_mgr,
        template_manager=template_mgr,
        catalog_manager=catalog_mgr,
    )


def format_scope_badge(scope: ScopeType) -> str:
    """Format scope with emoji badge."""
    badges = {
        ScopeType.GLOBAL: "🌐",
        ScopeType.PROJECT: "📁",
        ScopeType.LOCAL: "🔒",
    }
    return f"{badges.get(scope, '❓')} {scope.value}"


def format_skill_entry(entry: SkillCatalogEntry, show_path: bool = False) -> str:
    """Format skill catalog entry for display."""
    lines = []

    # Name and scope
    scope_badge = format_scope_badge(entry.scope)
    lines.append(f"  {entry.name} ({scope_badge})")

    # Description
    if entry.description:
        lines.append(f"    {entry.description}")

    # Metadata
    meta_parts = []
    if entry.metadata:
        if entry.metadata.get("template"):
            meta_parts.append(f"template:{entry.metadata['template']}")
        if entry.metadata.get("has_scripts"):
            meta_parts.append("scripts")
        if entry.metadata.get("allowed_tools"):
            tool_count = len(entry.metadata["allowed_tools"])
            meta_parts.append(f"{tool_count} tools")

    if meta_parts:
        lines.append(f"    💡 {', '.join(meta_parts)}")

    # Path (optional)
    if show_path and entry.path:
        lines.append(f"    📂 {entry.path}")

    return "\n".join(lines)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Skill Builder - Create Claude Code skills."""
    pass


@cli.command()
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def create(project_root: Optional[str]):
    """Create a new skill using interactive wizard."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        # Get managers
        template_mgr = get_template_manager()
        catalog_mgr = get_catalog_manager(project_path)
        builder = get_builder(template_manager=template_mgr, catalog_manager=catalog_mgr)

        # Run wizard
        wizard = SkillWizard(
            template_manager=template_mgr,
            builder=builder,
            catalog_manager=catalog_mgr,
        )
        config = wizard.run(project_path)

        if config is None:
            click.echo("✋ Skill creation cancelled")
            return

        # Skill is already created by wizard, just show success
        scope_badge = format_scope_badge(config.scope)
        skill_path = builder.get_scope_path(config.scope, project_path) / config.name

        click.echo(f"\n✅ Skill created successfully!")
        click.echo(f"📄 Directory: {skill_path}")
        click.echo(f"🔍 Scope: {scope_badge}")
        click.echo(f"\n💡 Skill is now available in Claude Code")

    except SkillExistsError as e:
        click.echo(f"❌ Error: {e}", err=True)
        click.echo("💡 Use 'delete' command first to replace existing skill", err=True)
        raise click.Abort()
    except SkillBuilderError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--name", required=True, help="Skill name (e.g., 'pdf-processor')")
@click.option("--description", required=True, help="Skill description")
@click.option(
    "--scope",
    type=click.Choice(["global", "project", "local"]),
    default="project",
    help="Skill scope (default: project)",
)
@click.option(
    "--template",
    type=click.Choice(["basic", "with_tools", "with_scripts", "advanced"]),
    default="basic",
    help="Template to use (default: basic)",
)
@click.option("--allowed-tools", help="Comma-separated list of allowed tools")
@click.option("--dry-run", is_flag=True, help="Preview without creating files")
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def generate(
    name: str,
    description: str,
    scope: str,
    template: str,
    allowed_tools: Optional[str],
    dry_run: bool,
    project_root: Optional[str],
):
    """Create a new skill non-interactively using CLI options."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        # Parse allowed tools
        tools_list = []
        if allowed_tools:
            tools_list = [tool.strip() for tool in allowed_tools.split(",")]

        # Create config
        config = SkillConfig(
            name=name,
            description=description,
            scope=ScopeType(scope),
            template=template,
            allowed_tools=tools_list,
        )

        # Build skill
        catalog_mgr = get_catalog_manager(project_path)
        builder = get_builder(catalog_manager=catalog_mgr)
        skill_dir, content = builder.build_skill(config, project_path, dry_run=dry_run)

        if dry_run:
            click.echo("🔍 Dry run - no files created")
            click.echo(f"\nWould create skill at: {skill_dir}")
            click.echo(f"Template: {template}")
            click.echo(f"Scope: {format_scope_badge(config.scope)}")
            if tools_list:
                click.echo(f"Allowed tools: {', '.join(tools_list)}")
            return

        scope_badge = format_scope_badge(config.scope)
        click.echo(f"\n✅ Skill created successfully!")
        click.echo(f"📄 Directory: {skill_dir}")
        click.echo(f"🔍 Scope: {scope_badge}")
        click.echo(f"📝 Template: {template}")
        if tools_list:
            click.echo(f"🛠️  Allowed tools: {', '.join(tools_list)}")
        click.echo(f"\n💡 Skill is now available in Claude Code")

    except SkillExistsError as e:
        click.echo(f"❌ Error: {e}", err=True)
        click.echo("💡 Use 'delete' command first to replace existing skill", err=True)
        raise click.Abort()
    except PydanticValidationError as e:
        click.echo(f"❌ Validation error: {e}", err=True)
        raise click.Abort()
    except SkillBuilderError as e:
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
@click.option("--has-scripts", is_flag=True, help="Show only skills with scripts")
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def list_skills(
    scope: str,
    search: Optional[str],
    template: Optional[str],
    has_scripts: bool,
    project_root: Optional[str],
):
    """List all skills with optional filtering."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = get_catalog_manager(project_path)

        # Prepare filters
        scope_filter = None if scope == "all" else ScopeType(scope)
        has_scripts_filter = True if has_scripts else None

        # Search skills
        skills = catalog_mgr.search_skills(
            query=search,
            scope=scope_filter,
            has_scripts=has_scripts_filter,
            template=template,
        )

        if not skills:
            click.echo("📋 No skills found matching criteria")
            return

        # Display header
        click.echo(f"\n📋 Skills ({len(skills)} total):\n")
        click.echo("─" * 60)

        # Display each skill
        for skill in skills:
            click.echo(format_skill_entry(skill))
            click.echo("─" * 60)

        # Display filter info
        filters = []
        if scope != "all":
            filters.append(f"scope={scope}")
        if search:
            filters.append(f"search='{search}'")
        if template:
            filters.append(f"template={template}")
        if has_scripts:
            filters.append("has-scripts")

        if filters:
            click.echo(f"\n🔍 Filters: {', '.join(filters)}")

    except CatalogError as e:
        click.echo(f"❌ Catalog error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("skill_name")
@click.option(
    "--scope",
    type=click.Choice(["global", "project", "local"]),
    help="Scope to search in (optional)",
)
@click.option("--yes", is_flag=True, help="Skip confirmation prompt")
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def delete(skill_name: str, scope: Optional[str], yes: bool, project_root: Optional[str]):
    """Delete a skill by name."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = get_catalog_manager(project_path)
        builder = get_builder(catalog_manager=catalog_mgr)

        # Find skill in catalog
        scope_filter = ScopeType(scope) if scope else None
        skill = catalog_mgr.get_skill(name=skill_name, scope=scope_filter)

        if not skill:
            scope_msg = f" in {scope} scope" if scope else ""
            click.echo(f"❌ Skill '{skill_name}'{scope_msg} not found", err=True)
            raise click.Abort()

        # Show skill info
        click.echo(f"\n🗑️  Skill to delete:")
        click.echo(format_skill_entry(skill, show_path=True))

        # Confirm deletion
        if not yes:
            if not click.confirm("\n⚠️  Are you sure you want to delete this skill?"):
                click.echo("✋ Deletion cancelled")
                return

        # Delete skill
        skill_path = Path(skill.path)
        success = builder.delete_skill(skill_path)

        if success:
            click.echo(f"\n✅ Skill '{skill_name}' deleted successfully")
        else:
            click.echo(f"❌ Failed to delete skill '{skill_name}'", err=True)
            raise click.Abort()

    except SkillNotFoundError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except SkillBuilderError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument("skill_path", type=click.Path(exists=True))
def validate(skill_path: str):
    """Validate a skill directory or SKILL.md file."""
    path = Path(skill_path)

    try:
        builder = get_builder()

        # If path is SKILL.md, use parent directory
        if path.is_file() and path.name == "SKILL.md":
            path = path.parent

        # Validate
        is_valid, message = builder.validate_skill_directory(path)

        if is_valid:
            click.echo(f"✅ Skill directory is valid")
            click.echo(f"📂 {path}")
        else:
            click.echo(f"❌ Skill directory is invalid", err=True)
            click.echo(f"📂 {path}", err=True)
            click.echo(f"\nValidation errors:", err=True)
            click.echo(f"  {message}", err=True)
            raise click.Abort()

    except SkillBuilderError as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
def templates():
    """List available skill templates."""
    try:
        template_mgr = get_template_manager()
        available_templates = template_mgr.list_templates()

        click.echo(f"\n📝 Available Templates ({len(available_templates)}):\n")
        click.echo("─" * 60)

        descriptions = {
            "basic": "Simple skill with name and description",
            "with_tools": "Skill with allowed-tools configuration",
            "with_scripts": "Skill with scripts/ directory for custom code",
            "advanced": "Full-featured skill with all options",
        }

        for template_name in available_templates:
            desc = descriptions.get(template_name, "No description")
            click.echo(f"  {template_name}")
            click.echo(f"    {desc}")
            click.echo("─" * 60)

        click.echo(f"\n💡 Use --template option to specify template")

    except TemplateError as e:
        click.echo(f"❌ Template error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def stats(project_root: Optional[str]):
    """Show catalog statistics."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = get_catalog_manager(project_path)
        statistics = catalog_mgr.get_catalog_stats()

        click.echo(f"\n📊 Skill Catalog Statistics:\n")
        click.echo("─" * 60)

        # Total skills
        click.echo(f"  Total skills: {statistics['total']}")

        # By scope
        if statistics.get("by_scope"):
            click.echo(f"\n  By Scope:")
            for scope_name, count in statistics["by_scope"].items():
                scope_type = ScopeType(scope_name)
                badge = format_scope_badge(scope_type)
                click.echo(f"    {badge}: {count}")

        # By template
        if statistics.get("by_template"):
            click.echo(f"\n  By Template:")
            for template_name, count in statistics["by_template"].items():
                click.echo(f"    {template_name}: {count}")

        # Skills with scripts
        if "with_scripts" in statistics:
            click.echo(f"\n  With scripts: {statistics['with_scripts']}")

        click.echo("─" * 60)

    except CatalogError as e:
        click.echo(f"❌ Catalog error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option("--project-root", type=click.Path(exists=True), help="Project root directory")
def sync(project_root: Optional[str]):
    """Synchronize catalog with filesystem."""
    project_path = Path(project_root) if project_root else Path.cwd()

    try:
        catalog_mgr = get_catalog_manager(project_path)

        click.echo("🔄 Synchronizing catalog with filesystem...")

        results = catalog_mgr.sync_catalog(project_path)

        click.echo(f"\n✅ Sync complete!\n")
        click.echo("─" * 60)
        click.echo(f"  Added: {results.get('added', 0)}")
        click.echo(f"  Updated: {results.get('updated', 0)}")
        click.echo(f"  Removed: {results.get('removed', 0)}")
        click.echo("─" * 60)

        total_changes = (
            results.get("added", 0) + results.get("updated", 0) + results.get("removed", 0)
        )
        if total_changes == 0:
            click.echo("\n💡 Catalog was already in sync")

    except CatalogError as e:
        click.echo(f"❌ Catalog error: {e}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
