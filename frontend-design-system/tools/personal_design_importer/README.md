# Personal Design System Importer

Import your personal design systems from JSON or YAML files into the design system catalog with automatic validation and metadata generation.

## Features

- **JSON & YAML Support**: Load design systems from JSON or YAML files
- **Schema Validation**: Automatic validation of design token structure
- **Metadata Generation**: Creates metadata.json with import details
- **Simple CLI**: Easy-to-use command-line interface
- **Custom Systems**: Saves as `custom-{name}` for easy identification

## Installation

```bash
# From the project root
cd /Users/matteocervelli/dev/projects/llms/frontend-design-system

# Install dependencies (if needed)
pip install click pyyaml
```

## Usage

### Import a Design System

```bash
# Import from JSON
python -m tools.personal_design_importer import \
    --file my-design.json \
    --name "My Custom Design"

# Import from YAML
python -m tools.personal_design_importer import \
    --file my-design.yaml \
    --name "My Custom Design"

# Overwrite existing system
python -m tools.personal_design_importer import \
    --file my-design.json \
    --overwrite
```

### List Imported Systems

```bash
python -m tools.personal_design_importer list
```

### View Design Tokens

```bash
python -m tools.personal_design_importer show --name "My Custom Design"
```

### Delete a System

```bash
python -m tools.personal_design_importer delete --name "My Custom Design"
```

### View Schema

```bash
python -m tools.personal_design_importer schema
```

## Design System Schema

Your design file must follow this structure:

```json
{
  "name": "My Custom Design",
  "version": "1.0.0",
  "description": "Optional description",
  "author": "Your Name",
  "tokens": {
    "colors": {
      "primary": "#007AFF",
      "secondary": "#5AC8FA",
      "background": "#FFFFFF",
      "text": "#000000"
    },
    "typography": {
      "heading": {
        "font": "Helvetica",
        "size": "32px",
        "weight": "bold"
      },
      "body": {
        "font": "Helvetica",
        "size": "16px",
        "weight": "regular"
      }
    },
    "spacing": [4, 8, 16, 24, 32, 48, 64],
    "shadows": [
      {
        "blur": 2,
        "offset": 1,
        "color": "rgba(0,0,0,0.1)"
      },
      {
        "blur": 8,
        "offset": 4,
        "color": "rgba(0,0,0,0.15)"
      }
    ]
  }
}
```

### Required Fields

- `name` (string): Name of the design system
- `tokens` (object): Design tokens grouped by category
  - `colors` (object): Color definitions (hex, rgb, etc.)
  - `typography` (object): Typography/font definitions
  - `spacing` (array/object): Spacing scale values
  - `shadows` (array/object): Shadow definitions

### Optional Fields

- `version` (string): Version number (default: "1.0.0")
- `description` (string): System description
- `author` (string): Author name

## Output Structure

Imported systems are saved to `design-systems/custom-{name}/`:

```
design-systems/
├── custom-my-design/
│   ├── metadata.json      # System metadata and import info
│   └── tokens.json        # Design tokens
```

### Metadata File

```json
{
  "name": "My Custom Design",
  "version": "1.0.0",
  "description": "Optional description",
  "author": "Your Name",
  "source_type": "personal_import",
  "imported_at": "2025-11-17T14:30:00.123456"
}
```

## Examples

### Basic Color System

```json
{
  "name": "Simple Colors",
  "tokens": {
    "colors": {
      "primary": "#0066FF",
      "success": "#00AA00",
      "warning": "#FFAA00",
      "error": "#FF0000"
    },
    "typography": {},
    "spacing": [4, 8, 16],
    "shadows": []
  }
}
```

### Comprehensive Design System

```json
{
  "name": "Brand Design System",
  "version": "2.0.0",
  "description": "Official brand design tokens",
  "author": "Design Team",
  "tokens": {
    "colors": {
      "primary": "#1A73E8",
      "secondary": "#EA4335",
      "neutral-light": "#F3F3F3",
      "neutral-dark": "#202124"
    },
    "typography": {
      "h1": {
        "font": "Roboto",
        "size": "32px",
        "weight": 700,
        "lineHeight": 1.2
      },
      "body": {
        "font": "Roboto",
        "size": "14px",
        "weight": 400,
        "lineHeight": 1.5
      }
    },
    "spacing": [2, 4, 8, 12, 16, 24, 32, 48, 64],
    "shadows": [
      {
        "name": "sm",
        "blur": 2,
        "offset": 1,
        "color": "rgba(0,0,0,0.05)"
      },
      {
        "name": "md",
        "blur": 8,
        "offset": 4,
        "color": "rgba(0,0,0,0.10)"
      }
    ]
  }
}
```

## Error Messages

### Validation Errors

Common validation errors and how to fix them:

- **Missing required field 'name'**: Add a `name` field with string value
- **Missing required token category 'colors'**: Add a `tokens.colors` object (can be empty `{}`)
- **'tokens.colors' must be a dictionary**: Ensure colors are in object format, not array
- **'tokens.spacing' must be a list or dictionary**: Use array `[]` or object `{}`

## File Paths

- Tool location: `/Users/matteocervelli/dev/projects/llms/frontend-design-system/tools/personal_design_importer/`
- Output location: `/Users/matteocervelli/dev/projects/llms/frontend-design-system/design-systems/`
