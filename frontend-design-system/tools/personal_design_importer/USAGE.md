# Quick Start Guide

## Installation

```bash
cd /Users/matteocervelli/dev/projects/llms/frontend-design-system
pip install click pyyaml  # If not already installed
```

## Basic Usage

### 1. Import a Design System

```bash
python -m tools.personal_design_importer import \
  --file path/to/my-design.json
```

### 2. View Your Systems

```bash
python -m tools.personal_design_importer list
```

### 3. Check System Details

```bash
python -m tools.personal_design_importer show --name "My Design"
```

### 4. Delete a System

```bash
python -m tools.personal_design_importer delete --name "My Design"
```

## File Format

Your design file must be valid JSON or YAML with this structure:

```json
{
  "name": "My Design System",
  "version": "1.0.0",
  "description": "Optional description",
  "author": "Your Name",
  "tokens": {
    "colors": {
      "primary": "#007AFF",
      "secondary": "#5AC8FA"
    },
    "typography": {
      "heading": {
        "font": "Helvetica",
        "size": "32px",
        "weight": "bold"
      }
    },
    "spacing": [4, 8, 16, 24, 32],
    "shadows": [
      {"blur": 2, "offset": 1, "color": "rgba(0,0,0,0.1)"}
    ]
  }
}
```

All four token categories (colors, typography, spacing, shadows) are required.

## Output

Imported systems are saved to:
```
design-systems/custom-{system-name}/
├── metadata.json    # System info + import timestamp
└── tokens.json      # Design tokens
```

## Features

- JSON and YAML support
- Schema validation
- Automatic metadata generation
- Simple CLI interface
- Token summary display
