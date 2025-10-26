"""
Documentation Fetcher CLI

Command-line interface for fetching and managing LLM provider documentation.

Commands:
    fetch: Fetch documentation from providers
    update: Update all changed documents
    list: List tracked documents

Example Usage:
    $ python -m src.tools.doc_fetcher fetch --all
    $ python -m src.tools.doc_fetcher fetch --provider anthropic
    $ python -m src.tools.doc_fetcher update
    $ python -m src.tools.doc_fetcher list --provider openai
"""

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import yaml
from pydantic import HttpUrl, ValidationError

from .converter import DocumentConverter
from .crawler import DocumentationCrawler
from .exceptions import ConversionError, CrawlError, DocFetcherError, FetchError
from .fetcher import DocumentFetcher
from .manifest import ManifestManager
from .models import DocumentSource, ManifestEntry, ProviderConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DocFetcherCLI:
    """Command-line interface for Documentation Fetcher."""

    PROVIDERS_DIR = Path("src/tools/doc_fetcher/providers")
    DOCS_DIR = Path("docs")

    def __init__(self, verbose: bool = False) -> None:
        """
        Initialize CLI.

        Args:
            verbose: Enable verbose logging
        """
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        self.manifest_manager = ManifestManager()
        self.fetcher = DocumentFetcher()
        self.converter = DocumentConverter()
        self.crawler = DocumentationCrawler()  # Crawl4AI for LLM-optimized markdown

    def load_provider_config(self, provider: str) -> ProviderConfig:
        """
        Load provider configuration from YAML file.

        Args:
            provider: Provider name

        Returns:
            ProviderConfig object

        Raises:
            click.ClickException: If config file not found or invalid
        """
        config_path = self.PROVIDERS_DIR / f"{provider}.yaml"
        if not config_path.exists():
            raise click.ClickException(
                f"Provider config not found: {config_path}\n"
                f"Available providers: {self.list_available_providers()}"
            )

        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)

            return ProviderConfig(**data)

        except yaml.YAMLError as e:
            raise click.ClickException(f"Invalid YAML in {config_path}: {e}")
        except ValidationError as e:
            raise click.ClickException(f"Invalid provider config: {e}")

    def list_available_providers(self) -> list[str]:
        """
        List available provider configurations.

        Returns:
            List of provider names
        """
        if not self.PROVIDERS_DIR.exists():
            return []

        return [p.stem for p in self.PROVIDERS_DIR.glob("*.yaml") if p.is_file()]

    def fetch_document(self, source: DocumentSource, provider_config: ProviderConfig) -> bool:
        """
        Fetch and save a single document.

        Args:
            source: DocumentSource to fetch
            provider_config: Provider configuration

        Returns:
            True if successful, False otherwise
        """
        url_str = str(source.url)

        try:
            # Check if document needs update
            existing_entry = self.manifest_manager.get_entry(url_str)
            if existing_entry:
                click.echo(f"  Checking for changes: {url_str}")
            else:
                click.echo(f"  Fetching new document: {url_str}")

            # Fetch content
            result = self.fetcher.fetch(source.url)

            if not result.success:
                click.secho(f"  ✗ Failed: {result.error}", fg="red")
                return False

            # Check if content changed
            if existing_entry and result.hash == existing_entry.hash:
                click.secho(f"  ✓ No changes (hash: {result.hash[:8]}...)", fg="yellow")
                return True

            # Convert to Markdown
            markdown, metadata = self.converter.convert(result.content or "", url_str)

            # Determine local path
            local_path = (
                self.DOCS_DIR
                / provider_config.name
                / source.category
                / f"{Path(source.url.path).stem}.md"
            )

            # Save to file
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(markdown)

            # Update manifest
            entry = ManifestEntry(
                provider=provider_config.name,
                url=source.url,
                local_path=local_path,
                hash=result.hash or "",
                last_fetched=datetime.now(),
                category=source.category,
                title=metadata.get("title"),
                description=metadata.get("description"),
            )
            self.manifest_manager.add_entry(entry)

            if existing_entry:
                click.secho(f"  ✓ Updated: {local_path} ({len(markdown)} chars)", fg="green")
            else:
                click.secho(f"  ✓ Saved: {local_path} ({len(markdown)} chars)", fg="green")

            return True

        except (FetchError, ConversionError, DocFetcherError) as e:
            click.secho(f"  ✗ Error: {e}", fg="red")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error fetching {url_str}")
            click.secho(f"  ✗ Unexpected error: {e}", fg="red")
            return False

    async def fetch_document_crawl4ai(
        self, source: DocumentSource, provider_config: ProviderConfig
    ) -> bool:
        """
        Fetch and save a single document using Crawl4AI.

        Uses Crawl4AI for superior LLM-optimized markdown extraction with
        automatic noise removal and semantic structure preservation.

        Args:
            source: DocumentSource to fetch
            provider_config: Provider configuration

        Returns:
            True if successful, False otherwise
        """
        url_str = str(source.url)

        try:
            # Check if document needs update
            existing_entry = self.manifest_manager.get_entry(url_str)
            if existing_entry:
                click.echo(f"  Checking for changes: {url_str}")
            else:
                click.echo(f"  Fetching new document: {url_str}")

            # Fetch content using Crawl4AI
            markdown, metadata, content_hash = await self.crawler.crawl_url(url_str)

            # Check if content changed
            if existing_entry and content_hash == existing_entry.hash:
                click.secho(
                    f"  ✓ No changes (hash: {content_hash[:8]}...)", fg="yellow"
                )
                return True

            # Determine local path
            local_path = (
                self.DOCS_DIR
                / provider_config.name
                / source.category
                / f"{Path(source.url.path).stem}.md"
            )

            # Save to file
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(markdown)

            # Update manifest
            entry = ManifestEntry(
                provider=provider_config.name,
                url=source.url,
                local_path=local_path,
                hash=content_hash,
                last_fetched=datetime.now(),
                category=source.category,
                title=metadata.get("title"),
                description=metadata.get("description"),
            )
            self.manifest_manager.add_entry(entry)

            if existing_entry:
                click.secho(
                    f"  ✓ Updated: {local_path} ({len(markdown)} chars)", fg="green"
                )
            else:
                click.secho(
                    f"  ✓ Saved: {local_path} ({len(markdown)} chars)", fg="green"
                )

            return True

        except CrawlError as e:
            click.secho(f"  ✗ Crawl error: {e}", fg="red")
            return False
        except Exception as e:
            logger.exception(f"Unexpected error fetching {url_str}")
            click.secho(f"  ✗ Unexpected error: {e}", fg="red")
            return False

    def fetch_provider(self, provider: str) -> tuple[int, int]:
        """
        Fetch all documents for a provider.

        Args:
            provider: Provider name

        Returns:
            Tuple of (success_count, total_count)
        """
        click.echo(f"\nFetching documents for provider: {provider}")
        click.echo("=" * 60)

        try:
            config = self.load_provider_config(provider)
        except click.ClickException:
            raise

        if not config.sources:
            click.secho(f"No sources configured for {provider}", fg="yellow")
            return (0, 0)

        success_count = 0
        total_count = len(config.sources)

        with click.progressbar(
            config.sources,
            label=f"Processing {total_count} documents",
            show_pos=True,
        ) as sources:
            for source in sources:
                if self.fetch_document(source, config):
                    success_count += 1

        return (success_count, total_count)

    async def fetch_provider_crawl4ai(self, provider: str) -> tuple[int, int]:
        """
        Fetch all documents for a provider using Crawl4AI.

        Args:
            provider: Provider name

        Returns:
            Tuple of (success_count, total_count)
        """
        click.echo(f"\nFetching documents for provider: {provider} (using Crawl4AI)")
        click.echo("=" * 60)

        try:
            config = self.load_provider_config(provider)
        except click.ClickException:
            raise

        if not config.sources:
            click.secho(f"No sources configured for {provider}", fg="yellow")
            return (0, 0)

        success_count = 0
        total_count = len(config.sources)

        click.echo(f"Processing {total_count} documents with LLM-optimized extraction...")
        for source in config.sources:
            if await self.fetch_document_crawl4ai(source, config):
                success_count += 1

        return (success_count, total_count)


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """
    Documentation Fetcher - Manage LLM provider documentation.

    Automatically fetch, convert, and track documentation from multiple
    LLM providers (Anthropic, OpenAI, etc.).
    """
    ctx.obj = DocFetcherCLI(verbose=verbose)


@cli.command()
@click.option("--all", "fetch_all", is_flag=True, help="Fetch all configured providers")
@click.option("--provider", "-p", type=str, help="Fetch specific provider")
@click.option(
    "--url",
    "-u",
    type=str,
    help="Fetch single URL (requires --provider and --category)",
)
@click.option("--category", "-c", type=str, help="Category for single URL fetch")
@click.pass_obj
def fetch(
    cli_obj: DocFetcherCLI,
    fetch_all: bool,
    provider: Optional[str],
    url: Optional[str],
    category: Optional[str],
) -> None:
    """
    Fetch documentation from providers.

    Examples:
        # Fetch all providers
        $ doc_fetcher fetch --all

        # Fetch specific provider
        $ doc_fetcher fetch --provider anthropic

        # Fetch single URL
        $ doc_fetcher fetch --provider anthropic --url https://docs.anthropic.com/... --category guides
    """
    if not any([fetch_all, provider, url]):
        click.echo("Error: Must specify --all, --provider, or --url")
        click.echo("Use 'doc_fetcher fetch --help' for more information")
        sys.exit(1)

    # Single URL fetch
    if url:
        if not provider or not category:
            click.echo("Error: --url requires both --provider and --category")
            sys.exit(1)

        try:
            # Validate URL
            validated_url = HttpUrl(url)
            source = DocumentSource(
                url=validated_url,
                provider=provider,
                category=category,
            )
            config = cli_obj.load_provider_config(provider)
            success = cli_obj.fetch_document(source, config)
            sys.exit(0 if success else 1)

        except ValidationError as e:
            click.secho(f"Invalid URL: {e}", fg="red")
            sys.exit(1)

    # Fetch all providers
    if fetch_all:
        providers = cli_obj.list_available_providers()
        if not providers:
            click.secho("No provider configurations found", fg="yellow")
            sys.exit(0)

        total_success = 0
        total_count = 0

        for prov in providers:
            try:
                # Use Crawl4AI for LLM-optimized markdown
                success, count = asyncio.run(cli_obj.fetch_provider_crawl4ai(prov))
                total_success += success
                total_count += count
            except click.ClickException as e:
                click.secho(f"Error: {e.message}", fg="red")

        click.echo("\n" + "=" * 60)
        click.secho(
            f"Summary: {total_success}/{total_count} documents fetched successfully",
            fg="green" if total_success == total_count else "yellow",
        )
        sys.exit(0 if total_success == total_count else 1)

    # Fetch specific provider
    if provider:
        try:
            # Use Crawl4AI for LLM-optimized markdown
            success, count = asyncio.run(cli_obj.fetch_provider_crawl4ai(provider))
            click.echo("\n" + "=" * 60)
            click.secho(
                f"Summary: {success}/{count} documents fetched successfully",
                fg="green" if success == count else "yellow",
            )
            sys.exit(0 if success == count else 1)
        except click.ClickException as e:
            click.secho(f"Error: {e.message}", fg="red")
            sys.exit(1)


@cli.command()
@click.pass_obj
def update(cli_obj: DocFetcherCLI) -> None:
    """
    Update all changed documents.

    Checks all documents in manifest and refetches only those that have changed.
    """
    click.echo("Checking for document updates...")
    click.echo("=" * 60)

    entries = cli_obj.manifest_manager.list_entries()
    if not entries:
        click.secho("No documents in manifest", fg="yellow")
        sys.exit(0)

    updated_count = 0
    unchanged_count = 0
    error_count = 0

    with click.progressbar(
        entries, label=f"Checking {len(entries)} documents", show_pos=True
    ) as entries_iter:
        for entry in entries_iter:
            try:
                # Fetch current version
                result = cli_obj.fetcher.fetch(entry.url)

                if not result.success:
                    click.echo(f"\n  ✗ Failed: {entry.url} - {result.error}")
                    error_count += 1
                    continue

                # Check if changed
                if result.hash == entry.hash:
                    unchanged_count += 1
                    continue

                # Content changed - convert and save
                markdown, metadata = cli_obj.converter.convert(result.content or "", str(entry.url))

                with open(entry.local_path, "w", encoding="utf-8") as f:
                    f.write(markdown)

                # Update manifest
                updated_entry = ManifestEntry(
                    provider=entry.provider,
                    url=entry.url,
                    local_path=entry.local_path,
                    hash=result.hash or "",
                    last_fetched=datetime.now(),
                    category=entry.category,
                    title=metadata.get("title") or entry.title,
                    description=metadata.get("description") or entry.description,
                )
                cli_obj.manifest_manager.add_entry(updated_entry)

                click.echo(f"\n  ✓ Updated: {entry.local_path}")
                updated_count += 1

            except Exception as e:
                click.echo(f"\n  ✗ Error: {entry.url} - {e}")
                error_count += 1

    click.echo("\n" + "=" * 60)
    click.secho(
        f"Summary: {updated_count} updated, {unchanged_count} unchanged, {error_count} errors",
        fg="green" if error_count == 0 else "yellow",
    )


@cli.command()
@click.option("--provider", "-p", type=str, help="Filter by provider")
@click.option("--category", "-c", type=str, help="Filter by category")
@click.pass_obj
def list(cli_obj: DocFetcherCLI, provider: Optional[str], category: Optional[str]) -> None:
    """
    List tracked documents.

    Examples:
        # List all documents
        $ doc_fetcher list

        # List by provider
        $ doc_fetcher list --provider anthropic

        # List by category
        $ doc_fetcher list --category guides
    """
    entries = cli_obj.manifest_manager.list_entries(provider=provider, category=category)

    if not entries:
        click.secho("No documents found", fg="yellow")
        sys.exit(0)

    click.echo(f"\nFound {len(entries)} document(s):")
    click.echo("=" * 80)

    for entry in entries:
        click.echo(f"\n{entry.title or 'Untitled'}")
        click.echo(f"  Provider:     {entry.provider}")
        click.echo(f"  Category:     {entry.category}")
        click.echo(f"  URL:          {entry.url}")
        click.echo(f"  Local Path:   {entry.local_path}")
        click.echo(f"  Hash:         {entry.hash[:16]}...")
        click.echo(f"  Last Fetched: {entry.last_fetched.strftime('%Y-%m-%d %H:%M:%S')}")
        if entry.description:
            click.echo(f"  Description:  {entry.description[:100]}...")


if __name__ == "__main__":
    cli()
