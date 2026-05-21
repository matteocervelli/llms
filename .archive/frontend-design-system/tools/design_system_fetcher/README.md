# Design System Fetcher Tool

Extract design tokens (colors, typography, spacing, shadows) from design system documentation URLs.

## Overview

The Design System Fetcher is a tool for automatically fetching design system documentation and extracting design tokens. It uses the existing `DocumentationCrawler` to fetch content and provides sophisticated pattern matching to identify design tokens in markdown.

## Features

- **Automated Crawling**: Uses DocumentationCrawler for LLM-optimized markdown extraction
- **Token Extraction**: Automatically identifies design tokens from markdown content
- **Multiple Token Types**: Supports colors, typography, spacing, and shadows
- **Metadata Management**: Tracks fetched design systems with metadata and content hashes
- **CLI Interface**: Easy-to-use command-line interface with multiple commands
- **Storage**: Organized file structure with metadata and original content preservation

## Installation

Requires Python 3.10+ and dependencies from the main project.

```bash
pip install -r requirements.txt
```

## Usage

### Fetch a Design System

```bash
python -m tools.design_system_fetcher fetch \
    --url https://m3.material.io/ \
    --name "Material Design"
```

### List All Design Systems

```bash
python -m tools.design_system_fetcher list
```

### View Design Tokens

```bash
python -m tools.design_system_fetcher show --name "Material Design"
```

### Delete a Design System

```bash
python -m tools.design_system_fetcher delete --name "Material Design"
```

## Output Structure

Design systems are stored in `design-systems/{system-name}/`:

```
design-systems/
├── material-design/
│   ├── metadata.json      # Metadata with timestamps, URL, hash
│   ├── tokens.json        # Extracted design tokens
│   └── content.md         # Original markdown content
├── figma-design/
│   ├── metadata.json
│   ├── tokens.json
│   └── content.md
```

## Metadata Schema

`metadata.json` contains:

```json
{
  "name": "Material Design",
  "version": "3.0",
  "source_url": "https://m3.material.io/",
  "fetched_at": "2024-01-15T10:30:00.000000",
  "content_hash": "abc123def456...",
  "title": "Material Design 3",
  "description": "Material Design is an adaptable system of guidelines, components, and tools..."
}
```

## Tokens Schema

`tokens.json` contains extracted design tokens:

```json
{
  "colors": {
    "primary": "#2196f3",
    "secondary": "#ff9800",
    "error": "#f44336"
  },
  "typography": {
    "heading-large": {
      "font_family": "Roboto",
      "font_size": "32px",
      "font_weight": "400",
      "line_height": "40px"
    }
  },
  "spacing": [
    {"name": "xs", "value": "4px"},
    {"name": "sm", "value": "8px"},
    {"name": "md", "value": "16px"}
  ],
  "shadows": [
    {"name": "elevation-1", "value": "0 2px 4px rgba(0,0,0,0.1)"}
  ]
}
```

## Module Architecture

### `fetcher.py` (Core Fetching)
- `DesignSystemFetcher`: Manages URL crawling using DocumentationCrawler
- Handles retries with exponential backoff
- Returns markdown content and metadata

### `token_extractor.py` (Token Extraction)
- `DesignTokenExtractor`: Extracts design tokens from markdown
- Pattern matching for colors, typography, spacing, shadows
- Returns structured token dictionary

### `storage.py` (File Management)
- `DesignTokenStorage`: Manages saving/loading design systems
- Handles directory creation and normalization
- Provides listing and deletion functionality

### `main.py` (CLI Interface)
- `DesignSystemFetcherCLI`: Command-line interface
- Click-based commands: fetch, list, show, delete
- Pretty-printed output

## Design Token Types

### Colors
Extracts from patterns like:
- `Primary: #2196F3`
- `Secondary: rgb(255, 152, 0)`
- Named colors: `error: #f44336`

### Typography
Identifies:
- `Font-Family: Roboto`
- `Font-Size: 16px`
- `Font-Weight: 500`
- `Line-Height: 24px`
- `Letter-Spacing: 0.5px`

### Spacing
Extracts:
- `xs: 4px`
- `sm: 8px`
- `md: 16px`
- `lg: 24px`

### Shadows
Identifies:
- `elevation-1: 0 2px 4px rgba(0,0,0,0.1)`
- `elevation-2: 0 4px 8px rgba(0,0,0,0.15)`

## Examples

### Python API

```python
import asyncio
from tools.design_system_fetcher import DesignSystemFetcher, DesignTokenExtractor
from tools.design_system_fetcher.storage import DesignTokenStorage

async def main():
    # Fetch design system
    fetcher = DesignSystemFetcher(rate_limit=1.0)
    markdown, metadata = await fetcher.fetch(
        url="https://m3.material.io/",
        system_name="Material Design"
    )

    # Extract tokens
    extractor = DesignTokenExtractor()
    tokens = extractor.extract(markdown)

    # Save to disk
    storage = DesignTokenStorage(output_dir="design-systems")
    storage.save(
        system_name="Material Design",
        tokens=tokens,
        content=markdown,
        metadata=metadata
    )

asyncio.run(main())
```

### CLI Workflow

```bash
# Fetch multiple design systems
python -m tools.design_system_fetcher fetch \
    --url https://m3.material.io/ \
    --name "Material Design"

python -m tools.design_system_fetcher fetch \
    --url https://design.figma.com/ \
    --name "Figma Design"

# List all systems
python -m tools.design_system_fetcher list

# Compare tokens
python -m tools.design_system_fetcher show --name "Material Design"
python -m tools.design_system_fetcher show --name "Figma Design"
```

## Error Handling

The tool handles:
- Network errors with automatic retry (exponential backoff)
- Invalid URLs
- Crawling failures
- File I/O errors
- Invalid markdown formats

All errors are logged and reported to the user.

## Rate Limiting

Default rate limit is 1 request per second. Configurable via:

```python
fetcher = DesignSystemFetcher(rate_limit=2.0)
```

## Notes

- Requires internet connection for fetching
- Content hashes track changes for update detection
- Original markdown preserved for future processing
- System names are normalized to lowercase with hyphens
- Maximum 500 lines per file per development standards

## Future Enhancements

- JSON Schema validation for tokens
- Token comparison between systems
- Diff detection for updates
- Export to CSS variables
- Export to Figma plugin format
- Auto-update on schedule
