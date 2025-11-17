#!/usr/bin/env python3
"""
Standalone script to fetch design systems using the design_system_fetcher tool.
"""

import asyncio
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent / "tools"))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from design_system_fetcher.fetcher import DesignSystemFetcher
from design_system_fetcher.token_extractor import DesignTokenExtractor
from design_system_fetcher.storage import DesignTokenStorage


async def fetch_system(name: str, url: str, version: str = "latest"):
    """Fetch a single design system."""
    print(f"Fetching {name} from {url}...")

    fetcher = DesignSystemFetcher(rate_limit=0.5)
    storage_dir = Path(__file__).parent / "design-systems"
    storage = DesignTokenStorage(storage_dir)
    extractor = DesignTokenExtractor()

    try:
        # Fetch the content
        markdown, metadata = await fetcher.fetch(url, name)

        # Extract tokens
        tokens = extractor.extract(markdown)

        # Save
        metadata["version"] = version
        storage.save(
            system_name=name,
            metadata=metadata,
            tokens=tokens,
            content=markdown
        )

        print(f"✓ Successfully fetched {name}")
        print(f"  - Colors: {len(tokens.get('colors', {}))}")
        print(f"  - Typography: {len(tokens.get('typography', {}))}")
        print(f"  - Spacing: {len(tokens.get('spacing', []))}")
        print(f"  - Shadows: {len(tokens.get('shadows', []))}")

    except Exception as e:
        print(f"✗ Error fetching {name}: {e}")


async def main():
    """Fetch all 8 design systems."""
    systems = [
        ("Material Design", "https://m3.material.io/", "3.0"),
        ("Carbon Design System", "https://carbondesignsystem.com/", "11.0"),
        ("Tailwind CSS", "https://tailwindcss.com/docs", "3.4"),
        ("shadcn/ui", "https://ui.shadcn.com/", "latest"),
        ("Chakra UI", "https://chakra-ui.com/docs", "2.8"),
        ("Mantine", "https://mantine.dev/", "7.0"),
        ("Radix UI", "https://www.radix-ui.com/primitives/docs/overview/introduction", "latest"),
        ("Headless UI", "https://headlessui.com/", "2.0"),
    ]

    for name, url, version in systems:
        await fetch_system(name, url, version)
        # Rate limiting between fetches
        await asyncio.sleep(2)

    print("\n✓ All design systems fetched!")


if __name__ == "__main__":
    asyncio.run(main())
