"""
CLI interface for catalog system.

Provides user-facing commands for catalog management.
"""

import click
from tabulate import tabulate  # type: ignore[import-untyped]

from .catalog_manager import CatalogManager


@click.group()
def cli() -> None:
    """LLM Catalog Management System."""
    pass


@cli.command(name="list")
@click.argument("element_type", type=click.Choice(["skills", "commands", "agents", "all"]))
@click.option(
    "--scope",
    default="all",
    type=click.Choice(["global", "project", "local", "all"]),
    help="Filter by scope",
)
def list_elements(element_type: str, scope: str) -> None:
    """List catalog elements."""
    manager = CatalogManager()
    entries = manager.list(element_type, scope=scope)

    if not entries:
        click.echo(f"No {element_type} found.")
        return

    # Format as table
    table_data = [[entry.name, entry.scope, entry.description[:50]] for entry in entries]
    headers = ["Name", "Scope", "Description"]

    click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))
    click.echo(f"\nTotal: {len(entries)}")


@cli.command()
@click.argument("query")
@click.option(
    "--type",
    "element_type",
    default="all",
    type=click.Choice(["skills", "commands", "agents", "all"]),
    help="Filter by type",
)
def search(query: str, element_type: str) -> None:
    """Search catalog entries."""
    manager = CatalogManager()
    results = manager.search(query, element_type=element_type)

    if not results:
        click.echo(f"No results found for '{query}'.")
        return

    # Format as table
    table_data = [
        [entry.name, entry.scope, type(entry).__name__.replace("CatalogEntry", "")]
        for entry in results
    ]
    headers = ["Name", "Scope", "Type"]

    click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))
    click.echo(f"\nFound {len(results)} results.")


@cli.command()
@click.argument("element_type", type=click.Choice(["skill", "command", "agent"]))
@click.argument("name")
def show(element_type: str, name: str) -> None:
    """Show details for a specific element."""
    manager = CatalogManager()
    entry = manager.show(element_type, name)

    if not entry:
        click.echo(f"{element_type.capitalize()} '{name}' not found.")
        return

    # Display details
    click.echo(f"\n{element_type.capitalize()}: {entry.name}")
    click.echo("=" * (len(element_type) + len(entry.name) + 2))
    click.echo(f"Scope: {entry.scope}")
    click.echo(f"Description: {entry.description}")
    click.echo(f"Path: {entry.file_path}")

    # Type-specific fields
    if hasattr(entry, "template"):
        click.echo(f"Template: {entry.template}")
    if hasattr(entry, "model"):
        click.echo(f"Model: {entry.model}")


@cli.command()
@click.argument(
    "element_type", type=click.Choice(["skills", "commands", "agents", "all"]), default="all"
)
def sync(element_type: str) -> None:
    """Synchronize catalogs with filesystem."""
    manager = CatalogManager()

    click.echo(f"Syncing {element_type}...")
    manager.sync(element_type)
    click.echo("✓ Sync complete.")


@cli.command()
def stats() -> None:
    """Show catalog statistics."""
    manager = CatalogManager()
    statistics = manager.get_stats()

    click.echo("\nCatalog Statistics")
    click.echo("=" * 40)
    click.echo(f"Total entries: {statistics['total']}")

    click.echo("\nBy Type:")
    for etype, count in statistics["by_type"].items():
        click.echo(f"  {etype}: {count}")

    click.echo("\nBy Scope:")
    for scope, count in statistics["by_scope"].items():
        click.echo(f"  {scope}: {count}")


if __name__ == "__main__":
    cli()
