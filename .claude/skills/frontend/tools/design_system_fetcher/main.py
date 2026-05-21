"""
Design System Fetcher CLI

Command-line interface for fetching design system documentation and extracting
design tokens (colors, typography, spacing, shadows).

Commands:
    fetch:  Fetch a design system from a URL
    list:   List all fetched design systems
    show:   Display design tokens for a system
    delete: Delete a design system

Example Usage:
    $ python -m tools.design_system_fetcher fetch \\
        --url https://m3.material.io/ \\
        --name "Material Design"

    $ python -m tools.design_system_fetcher list

    $ python -m tools.design_system_fetcher show --name "Material Design"

    $ python -m tools.design_system_fetcher delete --name "Material Design"
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Optional

import click

from fetcher import DesignSystemFetcher
from token_extractor import DesignTokenExtractor
from storage import DesignTokenStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DesignSystemFetcherCLI:
    """Command-line interface for Design System Fetcher."""

    def __init__(self, output_dir: str | Path = "design-systems", verbose: bool = False) -> None:
        """
        Initialize CLI.

        Args:
            output_dir: Base directory for design system storage
            verbose: Enable verbose logging
        """
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        self.output_dir = Path(output_dir)
        self.fetcher = DesignSystemFetcher(rate_limit=1.0)
        self.extractor = DesignTokenExtractor()
        self.storage = DesignTokenStorage(output_dir=output_dir)

    async def fetch_system(self, url: str, system_name: str) -> bool:
        """
        Fetch a design system from a URL.

        Args:
            url: URL of the design system documentation
            system_name: Human-readable name for the system

        Returns:
            True if successful, False otherwise
        """
        try:
            click.echo(f"Fetching {system_name} from {url}...")

            # Fetch markdown content
            markdown, metadata = await self.fetcher.fetch(url, system_name)

            # Extract design tokens
            tokens = self.extractor.extract(markdown)

            # Save to disk
            system_dir = self.storage.save(system_name, tokens, markdown, metadata)

            click.secho(f"Success! Design system saved to {system_dir}", fg="green")

            # Print token summary
            self._print_token_summary(tokens)

            return True

        except Exception as e:
            click.secho(f"Error: {e}", fg="red")
            logger.exception("Fetch failed")
            return False

    def list_systems(self) -> None:
        """List all fetched design systems."""
        systems = self.storage.list_systems()

        if not systems:
            click.echo("No design systems found.")
            return

        click.echo("Design Systems:")
        for system in sorted(systems):
            system_dir = self.output_dir / system
            metadata_path = system_dir / "metadata.json"

            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)
                    click.echo(f"  - {metadata.get('name', system)}")
                    click.echo(f"    URL: {metadata.get('source_url', 'N/A')}")
                    click.echo(f"    Fetched: {metadata.get('fetched_at', 'N/A')}")
            else:
                click.echo(f"  - {system}")

    def show_system(self, system_name: str) -> None:
        """
        Display design tokens for a system.

        Args:
            system_name: Name of the design system
        """
        data = self.storage.load(system_name)

        if not data:
            click.secho(f"Design system not found: {system_name}", fg="red")
            return

        metadata = data["metadata"]
        tokens = data["tokens"]

        # Display metadata
        click.echo("\nMetadata:")
        click.echo(f"  Name: {metadata.get('name')}")
        click.echo(f"  URL: {metadata.get('source_url')}")
        click.echo(f"  Fetched: {metadata.get('fetched_at')}")
        click.echo(f"  Hash: {metadata.get('content_hash', 'N/A')[:8]}...")

        # Display token summary
        click.echo("\nTokens:")
        self._print_token_summary(tokens)

    def delete_system(self, system_name: str) -> bool:
        """
        Delete a design system.

        Args:
            system_name: Name of the design system

        Returns:
            True if deleted, False otherwise
        """
        if self.storage.delete(system_name):
            click.secho(f"Design system deleted: {system_name}", fg="green")
            return True
        else:
            click.secho(f"Design system not found: {system_name}", fg="red")
            return False

    @staticmethod
    def _print_token_summary(tokens: dict) -> None:
        """
        Print a summary of extracted tokens.

        Args:
            tokens: Tokens dictionary
        """
        colors = tokens.get("colors", {})
        typography = tokens.get("typography", {})
        spacing = tokens.get("spacing", [])
        shadows = tokens.get("shadows", [])

        click.echo(f"  Colors: {len(colors)}")
        click.echo(f"  Typography: {len(typography)}")
        click.echo(f"  Spacing: {len(spacing)}")
        click.echo(f"  Shadows: {len(shadows)}")


# CLI Commands
@click.group()
@click.option("--output-dir", default="design-systems", help="Output directory for design systems")
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
@click.pass_context
def cli(ctx: click.Context, output_dir: str, verbose: bool) -> None:
    """
    Design System Fetcher - Extract design tokens from design system documentation.

    Fetches design system documentation from URLs and automatically extracts
    design tokens including colors, typography, spacing, and shadows.
    """
    ctx.ensure_object(dict)
    ctx.obj["cli"] = DesignSystemFetcherCLI(output_dir=output_dir, verbose=verbose)


@cli.command()
@click.option("--url", required=True, help="URL of the design system documentation")
@click.option("--name", required=True, help="Name for the design system")
@click.pass_context
def fetch(ctx: click.Context, url: str, name: str) -> None:
    """
    Fetch a design system from a URL.

    Example:
        $ python -m tools.design_system_fetcher fetch \\
            --url https://m3.material.io/ \\
            --name "Material Design"
    """
    cli_instance: DesignSystemFetcherCLI = ctx.obj["cli"]
    success = asyncio.run(cli_instance.fetch_system(url, name))
    sys.exit(0 if success else 1)


@cli.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """
    List all fetched design systems.

    Example:
        $ python -m tools.design_system_fetcher list
    """
    cli_instance: DesignSystemFetcherCLI = ctx.obj["cli"]
    cli_instance.list_systems()


@cli.command()
@click.option("--name", required=True, help="Name of the design system")
@click.pass_context
def show(ctx: click.Context, name: str) -> None:
    """
    Display design tokens for a system.

    Example:
        $ python -m tools.design_system_fetcher show --name "Material Design"
    """
    cli_instance: DesignSystemFetcherCLI = ctx.obj["cli"]
    cli_instance.show_system(name)


@cli.command()
@click.option("--name", required=True, help="Name of the design system")
@click.confirmation_option(prompt="Are you sure you want to delete this system?")
@click.pass_context
def delete(ctx: click.Context, name: str) -> None:
    """
    Delete a design system.

    Example:
        $ python -m tools.design_system_fetcher delete --name "Material Design"
    """
    cli_instance: DesignSystemFetcherCLI = ctx.obj["cli"]
    success = cli_instance.delete_system(name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    cli()
