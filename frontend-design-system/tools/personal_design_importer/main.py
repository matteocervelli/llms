"""
Personal Design System Importer CLI.

Command-line interface for importing personal design systems from JSON/YAML files.

Commands:
    import: Import a design system from a file
    list:   List imported design systems
    show:   Display tokens for a system
    delete: Delete an imported design system

Example Usage:
    $ python -m personal_design_importer import \\
        --file my-design.json \\
        --name "My Design"

    $ python -m personal_design_importer list

    $ python -m personal_design_importer show --name "My Design"

    $ python -m personal_design_importer delete --name "My Design"
"""

import json
import logging
import sys
from pathlib import Path
from typing import Optional

import click

from .importer import PersonalDesignImporter
from .validator import DesignTokenValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ImporterCLI:
    """CLI for Personal Design Importer."""

    def __init__(self, output_dir: str | Path = "design-systems", verbose: bool = False) -> None:
        """Initialize CLI."""
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.output_dir = Path(output_dir)
        self.importer = PersonalDesignImporter(output_dir=output_dir)

    def import_design(self, file_path: str, system_name: Optional[str] = None, overwrite: bool = False) -> bool:
        """Import a design system."""
        success, message, system_dir = self.importer.import_design(file_path, system_name, overwrite)
        if success:
            click.secho(message, fg="green")
            if system_dir:
                self._show_summary(system_dir)
        else:
            click.secho(f"Error: {message}", fg="red")
        return success

    def list_systems(self) -> None:
        """List all imported design systems."""
        systems = sorted([d.name for d in self.output_dir.iterdir() if d.is_dir() and d.name.startswith("custom-")])
        if not systems:
            click.echo("No imported design systems found.")
            return
        click.echo("Imported Design Systems:")
        for system_dir in systems:
            metadata_path = self.output_dir / system_dir / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path) as f:
                    m = json.load(f)
                    click.echo(f"  - {m.get('name', system_dir)}")
                    click.echo(f"    Version: {m.get('version', 'N/A')}")
                    click.echo(f"    Imported: {m.get('imported_at', 'N/A')}")

    def show_system(self, system_name: str) -> None:
        """Display tokens for a system."""
        norm = self.importer._normalize_name(system_name)
        system_dir = self.output_dir / f"custom-{norm}"
        if not system_dir.exists():
            click.secho(f"Design system not found: {system_name}", fg="red")
            return
        self._show_summary(system_dir)

    def delete_system(self, system_name: str) -> bool:
        """Delete a design system."""
        import shutil
        norm = self.importer._normalize_name(system_name)
        system_dir = self.output_dir / f"custom-{norm}"
        if not system_dir.exists():
            click.secho(f"Design system not found: {system_name}", fg="red")
            return False
        shutil.rmtree(system_dir)
        click.secho(f"Deleted: {system_name}", fg="green")
        return True

    @staticmethod
    def _show_summary(system_dir: Path) -> None:
        """Print token summary."""
        tokens_file = system_dir / "tokens.json"
        if not tokens_file.exists():
            return
        with open(tokens_file) as f:
            t = json.load(f)
        click.echo("\nTokens:")
        click.echo(f"  Colors: {len(t.get('colors', {}))}")
        click.echo(f"  Typography: {len(t.get('typography', {}))}")
        click.echo(f"  Spacing: {len(t.get('spacing', []))}")
        click.echo(f"  Shadows: {len(t.get('shadows', []))}")


# CLI Commands
@click.group()
@click.option("--output-dir", default="design-systems", help="Output directory")
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
@click.pass_context
def cli(ctx: click.Context, output_dir: str, verbose: bool) -> None:
    """
    Personal Design System Importer - Import custom design systems.

    Import your personal design systems from JSON or YAML files and add them
    to the design system catalog with automatic validation.
    """
    ctx.ensure_object(dict)
    ctx.obj["cli"] = ImporterCLI(output_dir=output_dir, verbose=verbose)


@cli.command("import")
@click.option("--file", required=True, help="Path to design file (JSON or YAML)")
@click.option("--name", default=None, help="Override system name (optional)")
@click.option("--overwrite", is_flag=True, help="Overwrite existing system")
@click.pass_context
def import_cmd(ctx: click.Context, file: str, name: Optional[str], overwrite: bool) -> None:
    """Import a design system from a file."""
    cli_instance: ImporterCLI = ctx.obj["cli"]
    success = cli_instance.import_design(file, system_name=name, overwrite=overwrite)
    sys.exit(0 if success else 1)


@cli.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List all imported design systems."""
    ctx.obj["cli"].list_systems()


@cli.command()
@click.option("--name", required=True, help="System name")
@click.pass_context
def show(ctx: click.Context, name: str) -> None:
    """Display tokens for a design system."""
    ctx.obj["cli"].show_system(name)


@cli.command()
@click.option("--name", required=True, help="System name")
@click.confirmation_option(prompt="Delete this design system?")
@click.pass_context
def delete(ctx: click.Context, name: str) -> None:
    """Delete a design system."""
    success = ctx.obj["cli"].delete_system(name)
    sys.exit(0 if success else 1)


@cli.command()
@click.pass_context
def schema(ctx: click.Context) -> None:
    """Display the design system schema."""
    schema_info = DesignTokenValidator.get_schema()
    click.echo(json.dumps(schema_info, indent=2))


if __name__ == "__main__":
    cli()
