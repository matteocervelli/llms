# Library Documentation Research: Feature #12 - Catalog Manifest System

**Researcher**: documentation-researcher (Haiku + context7/fetch MCPs)
**Date**: 2025-10-30
**Issue**: #12
**Status**: RESEARCH_COMPLETE

---

## Executive Summary

This document provides comprehensive library documentation for implementing the catalog manifest system. Research focused on Pydantic 2.x for data validation, Click 8.x for CLI interfaces, Python pathlib for file operations, and JSON schema validation patterns.

**Key Findings**:
1. **Pydantic 2.x**: Major rewrite with improved performance and new features
2. **Click 8.x**: Mature CLI framework with composable commands
3. **pathlib**: Standard library, robust path operations
4. **JSON Schema**: Built-in validation with Pydantic integration

---

## 1. Pydantic 2.x Documentation

### 1.1 Library Overview

**Version**: 2.x (Latest: 2.9.2)
**Purpose**: Data validation using Python type annotations
**Official Docs**: https://docs.pydantic.dev/latest/

**Key Changes from v1**:
- Complete rewrite in Rust (pydantic-core)
- 5-50x performance improvement
- New `ConfigDict` replaces `Config` class
- Improved error messages
- Stricter validation by default

### 1.2 Core Concepts for Catalog System

#### BaseModel Usage

```python
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

class UnifiedCatalogEntry(BaseModel):
    """
    Pydantic 2.x BaseModel with validation.

    Key features:
    - Automatic validation on instantiation
    - Type coercion where appropriate
    - Custom validators with field_validator decorator
    - JSON serialization with model_dump()
    """

    # Pydantic 2.x: Use ConfigDict instead of Config class
    model_config = ConfigDict(
        # JSON encoders for custom types
        json_encoders={
            Path: str,
            datetime: lambda v: v.isoformat(),
            UUID: str
        },
        # Validate on assignment (default: False in v2)
        validate_assignment=True,
        # Use enum values instead of names
        use_enum_values=True,
        # Strict mode (no type coercion)
        strict=False
    )

    # Fields with validation
    id: UUID = Field(default_factory=uuid4, description="Unique identifier")
    name: str = Field(..., min_length=1, max_length=100)
    path: Path = Field(..., description="Absolute path to element")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Pydantic 2.x: field_validator replaces @validator
    @field_validator('path')
    @classmethod
    def validate_path(cls, v: Path) -> Path:
        """
        Custom validator for path field.

        Pydantic 2.x changes:
        - Use @field_validator instead of @validator
        - Must be @classmethod
        - Mode parameter: 'before' | 'after' | 'wrap'
        """
        resolved = v.resolve()
        if not resolved.exists():
            raise ValueError(f"Path does not exist: {resolved}")
        return resolved

    # Pydantic 2.x: model_validator for cross-field validation
    from pydantic import model_validator

    @model_validator(mode='after')
    def validate_model(self) -> 'UnifiedCatalogEntry':
        """
        Validate entire model after field validation.

        Use for cross-field validation logic.
        """
        # Example: Ensure updated_at >= created_at
        # if hasattr(self, 'updated_at'):
        #     if self.updated_at < self.created_at:
        #         raise ValueError("updated_at must be >= created_at")
        return self
```

#### Field Types and Validation

```python
from pydantic import (
    BaseModel,
    Field,
    EmailStr,        # Email validation
    HttpUrl,         # URL validation
    FilePath,        # Path exists and is file
    DirectoryPath,   # Path exists and is directory
    conint,          # Constrained integer
    constr,          # Constrained string
    conlist          # Constrained list
)
from typing import Literal, Annotated
from pathlib import Path

class SkillCatalogEntry(BaseModel):
    # String with constraints
    name: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-z0-9-]+$')

    # Or use Annotated (Pydantic 2.x preferred)
    name: Annotated[str, Field(min_length=1, max_length=100, pattern=r'^[a-z0-9-]+$')]

    # Integer with constraints
    file_count: int = Field(default=0, ge=0, le=1000)

    # Or use conint
    file_count: conint(ge=0, le=1000) = 0

    # Literal type for enums
    template: Literal["basic", "analysis", "implementation", "validation"]

    # List with constraints
    tags: list[str] = Field(default_factory=list, max_length=10)

    # Or use conlist
    tags: conlist(str, max_length=10) = []

    # Path that must exist and be a file
    path: FilePath

    # Path that must exist and be a directory
    skill_dir: DirectoryPath

    # Email with validation
    contact: EmailStr | None = None

    # URL with validation
    docs_url: HttpUrl | None = None
```

#### Serialization and Deserialization

```python
from pydantic import BaseModel
import json

class CatalogEntry(BaseModel):
    id: UUID
    name: str
    path: Path
    created_at: datetime

# Pydantic 2.x: model_dump() replaces dict()
entry = CatalogEntry(
    id=uuid4(),
    name="example",
    path=Path("/tmp/example"),
    created_at=datetime.utcnow()
)

# Serialize to dict
data = entry.model_dump()
# {'id': UUID('...'), 'name': 'example', 'path': Path('/tmp/example'), ...}

# Serialize to JSON-compatible dict
json_data = entry.model_dump(mode='json')
# {'id': '...', 'name': 'example', 'path': '/tmp/example', ...}

# Serialize to JSON string
json_str = entry.model_dump_json()
# '{"id": "...", "name": "example", "path": "/tmp/example", ...}'

# Deserialize from dict
entry2 = CatalogEntry.model_validate(data)

# Deserialize from JSON string
entry3 = CatalogEntry.model_validate_json(json_str)

# Pydantic 2.x: parse_obj/parse_raw deprecated
# Old (v1): CatalogEntry.parse_obj(data)
# New (v2): CatalogEntry.model_validate(data)
```

#### Error Handling

```python
from pydantic import ValidationError

try:
    entry = CatalogEntry(
        id="not-a-uuid",  # Invalid UUID
        name="",          # Too short
        path="/nonexistent",  # Path doesn't exist
        created_at="invalid-date"  # Invalid datetime
    )
except ValidationError as e:
    # Pydantic 2.x: Improved error messages
    print(e.errors())
    # [
    #   {
    #     'type': 'uuid_parsing',
    #     'loc': ('id',),
    #     'msg': 'Input should be a valid UUID',
    #     'input': 'not-a-uuid'
    #   },
    #   {
    #     'type': 'string_too_short',
    #     'loc': ('name',),
    #     'msg': 'String should have at least 1 character',
    #     'input': ''
    #   },
    #   ...
    # ]

    # JSON error output
    print(e.json())

    # Human-readable error output
    print(str(e))
```

### 1.3 Advanced Features for Catalog System

#### Model Inheritance and Composition

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

# Base model with common fields
class CatalogEntryBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    scope: Literal["global", "project", "local"]
    path: Path
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Skill-specific model extends base
class SkillCatalogEntry(CatalogEntryBase):
    element_type: Literal["skill"] = "skill"
    template: Literal["basic", "analysis", "implementation", "validation"]
    has_scripts: bool = False
    file_count: int = Field(default=0, ge=0)
    allowed_tools: list[str] = Field(default_factory=list)

# Command-specific model extends base
class CommandCatalogEntry(CatalogEntryBase):
    element_type: Literal["command"] = "command"
    aliases: list[str] = Field(default_factory=list)
    requires_tools: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    @field_validator('name')
    @classmethod
    def ensure_slash_prefix(cls, v: str) -> str:
        """Commands must start with /"""
        if not v.startswith('/'):
            return f"/{v}"
        return v

# Discriminated union for polymorphism
from pydantic import Field, Discriminator

CatalogEntry = Annotated[
    SkillCatalogEntry | CommandCatalogEntry | AgentCatalogEntry,
    Field(discriminator='element_type')
]
```

#### Schema Generation

```python
from pydantic import BaseModel

class SkillCatalogEntry(BaseModel):
    id: UUID
    name: str
    template: Literal["basic", "analysis"]

# Pydantic 2.x: model_json_schema() replaces schema()
schema = SkillCatalogEntry.model_json_schema()
print(json.dumps(schema, indent=2))

# Output: JSON Schema for validation
# {
#   "type": "object",
#   "properties": {
#     "id": {
#       "type": "string",
#       "format": "uuid"
#     },
#     "name": {
#       "type": "string"
#     },
#     "template": {
#       "type": "string",
#       "enum": ["basic", "analysis"]
#     }
#   },
#   "required": ["id", "name", "template"]
# }
```

### 1.4 Best Practices for Catalog System

1. **Use `model_config` instead of `Config` class** (Pydantic 2.x)
2. **Use `field_validator` instead of `@validator`** (Pydantic 2.x)
3. **Use `model_dump()` instead of `dict()`** (Pydantic 2.x)
4. **Use `model_validate()` instead of `parse_obj()`** (Pydantic 2.x)
5. **Enable `validate_assignment=True`** for runtime validation
6. **Use `Literal` for fixed choices instead of Enum** (cleaner syntax)
7. **Use `Annotated` for field constraints** (preferred in v2)
8. **Use `model_validator` for cross-field validation**
9. **Use discriminated unions for polymorphism** (element_type)
10. **Generate JSON schemas for documentation**

### 1.5 Migration Notes (Pydantic v1 → v2)

If existing code uses Pydantic v1:

```python
# v1 → v2 Migration Guide

# Config class → ConfigDict
class MyModel(BaseModel):
    # v1
    class Config:
        validate_assignment = True

    # v2
    model_config = ConfigDict(validate_assignment=True)

# @validator → @field_validator
# v1
@validator('path')
def validate_path(cls, v):
    return v.resolve()

# v2
@field_validator('path')
@classmethod
def validate_path(cls, v: Path) -> Path:
    return v.resolve()

# dict() → model_dump()
# v1: entry.dict()
# v2: entry.model_dump()

# parse_obj() → model_validate()
# v1: MyModel.parse_obj(data)
# v2: MyModel.model_validate(data)

# schema() → model_json_schema()
# v1: MyModel.schema()
# v2: MyModel.model_json_schema()
```

---

## 2. Click 8.x Documentation

### 2.1 Library Overview

**Version**: 8.x (Latest: 8.1.7)
**Purpose**: CLI framework for Python
**Official Docs**: https://click.palletsprojects.com/

**Key Features**:
- Decorator-based command definition
- Automatic help generation
- Type conversion and validation
- Command groups (sub-commands)
- Parameter types (options, arguments, flags)
- Testing support

### 2.2 Core Concepts for Catalog CLI

#### Basic Command Structure

```python
import click

@click.command()
@click.option('--scope', type=click.Choice(['global', 'project', 'local', 'all']), default='all')
@click.option('--format', type=click.Choice(['table', 'json', 'condensed']), default='table')
def list_skills(scope: str, format: str):
    """List all installed skills."""
    click.echo(f"Listing skills (scope={scope}, format={format})")

# Run: python cli.py list-skills --scope project --format json
```

#### Command Groups (Sub-commands)

```python
import click

@click.group()
def cli():
    """LLM Configuration Management CLI"""
    pass

@cli.command()
@click.argument('element_type', type=click.Choice(['skills', 'commands', 'agents', 'all']))
@click.option('--scope', default='all')
@click.option('--format', default='table')
def list(element_type: str, scope: str, format: str):
    """List catalog elements."""
    click.echo(f"Listing {element_type}")

@cli.command()
@click.argument('query')
@click.option('--type', 'element_type', type=click.Choice(['skills', 'commands', 'agents', 'all']), default='all')
@click.option('--scope', default='all')
@click.option('--tags', multiple=True)
@click.option('--limit', type=int, default=20)
def search(query: str, element_type: str, scope: str, tags: tuple, limit: int):
    """Search catalog elements."""
    click.echo(f"Searching for: {query}")
    if tags:
        click.echo(f"Tags: {', '.join(tags)}")

@cli.command()
@click.argument('element_type', type=click.Choice(['skill', 'command', 'agent']))
@click.argument('name')
def show(element_type: str, name: str):
    """Show details for a specific element."""
    click.echo(f"Showing {element_type}: {name}")

if __name__ == '__main__':
    cli()

# Run:
# python cli.py list skills --scope project
# python cli.py search "analysis" --type skills --tags validation --tags testing
# python cli.py show skill analysis-specialist
```

#### Parameter Types

```python
import click
from pathlib import Path

@click.command()
# String option with default
@click.option('--name', default='default', help='Element name')

# Integer option with validation
@click.option('--limit', type=int, default=20, help='Max results')

# Float option
@click.option('--threshold', type=float, default=0.5)

# Boolean flag
@click.option('--force', is_flag=True, help='Force operation')
@click.option('--no-backup', is_flag=True, help='Skip backup')

# Choice (enum)
@click.option('--scope', type=click.Choice(['global', 'project', 'local']))

# Multiple values
@click.option('--tags', multiple=True, help='Filter tags')

# Path (validates existence)
@click.option('--config', type=click.Path(exists=True))

# File (opens file handle)
@click.option('--input', type=click.File('r'))

# Custom type
class ScopeType(click.ParamType):
    name = 'scope'

    def convert(self, value, param, ctx):
        if value not in ['global', 'project', 'local', 'all']:
            self.fail(f'{value} is not a valid scope', param, ctx)
        return value

@click.option('--scope', type=ScopeType())
def command(scope):
    pass
```

#### Output Formatting

```python
import click
from typing import List, Dict, Any
import json
from tabulate import tabulate

@click.command()
@click.option('--format', type=click.Choice(['table', 'json', 'condensed']), default='table')
def list_elements(format: str):
    """List elements with different output formats."""

    # Sample data
    elements = [
        {'name': 'analysis', 'scope': 'global', 'type': 'skill'},
        {'name': 'implementation', 'scope': 'project', 'type': 'skill'},
    ]

    if format == 'json':
        # JSON output
        click.echo(json.dumps(elements, indent=2))

    elif format == 'table':
        # Table output using tabulate
        headers = elements[0].keys()
        rows = [elem.values() for elem in elements]
        table = tabulate(rows, headers=headers, tablefmt='grid')
        click.echo(table)

    elif format == 'condensed':
        # Condensed output
        for elem in elements:
            click.echo(f"{elem['name']} ({elem['scope']}) - {elem['type']}")

# Alternative: Use click.echo with color
@click.command()
def colored_output():
    click.secho('Success', fg='green', bold=True)
    click.secho('Warning', fg='yellow')
    click.secho('Error', fg='red', bold=True)
    click.echo(click.style('Info', fg='blue'))
```

#### Progress and Feedback

```python
import click
import time

@click.command()
def sync_catalogs():
    """Sync all catalogs with progress bar."""

    items = ['skills', 'commands', 'agents']

    # Progress bar
    with click.progressbar(items, label='Syncing catalogs') as bar:
        for item in bar:
            # Simulate work
            time.sleep(0.5)

    click.echo(click.style('✓ Sync complete', fg='green'))

@click.command()
@click.option('--verbose', is_flag=True)
def scan(verbose: bool):
    """Scan with conditional output."""

    if verbose:
        click.echo('Scanning ~/.claude/skills...')

    # Spinner (requires click-spinner package)
    # with click.spinner():
    #     time.sleep(2)

    click.echo('Found 5 skills')
```

#### Error Handling and Exit Codes

```python
import click
import sys

@click.command()
@click.argument('name')
def show_element(name: str):
    """Show element details."""

    try:
        # Lookup element
        element = get_element(name)
        if element is None:
            click.secho(f'Error: Element not found: {name}', fg='red', err=True)
            sys.exit(1)

        click.echo(json.dumps(element, indent=2))

    except Exception as e:
        click.secho(f'Error: {str(e)}', fg='red', err=True)
        sys.exit(1)

# Alternative: Use click.ClickException
@click.command()
def risky_operation():
    try:
        # Do something
        pass
    except ValueError as e:
        raise click.ClickException(str(e))
    except FileNotFoundError as e:
        raise click.FileError(filename, hint='File not found')
```

### 2.3 Testing Click Commands

```python
import click
from click.testing import CliRunner

@click.command()
@click.argument('name')
def greet(name):
    """Greet someone."""
    click.echo(f'Hello {name}!')

def test_greet():
    runner = CliRunner()

    # Test successful execution
    result = runner.invoke(greet, ['World'])
    assert result.exit_code == 0
    assert 'Hello World!' in result.output

    # Test with missing argument
    result = runner.invoke(greet, [])
    assert result.exit_code != 0
    assert 'Missing argument' in result.output

    # Test with options
    @click.command()
    @click.option('--count', default=1)
    def greet_multiple(count):
        for _ in range(count):
            click.echo('Hello!')

    result = runner.invoke(greet_multiple, ['--count', '3'])
    assert result.exit_code == 0
    assert result.output.count('Hello!') == 3
```

### 2.4 Best Practices for Catalog CLI

1. **Use command groups** for organized sub-commands (`llm list`, `llm search`, etc.)
2. **Provide clear help text** for all commands, options, and arguments
3. **Use `click.Choice`** for enum-like options (scope, format, type)
4. **Use `is_flag=True`** for boolean flags (`--force`, `--no-backup`)
5. **Use `multiple=True`** for lists (`--tags tag1 --tags tag2`)
6. **Color output** with `click.secho()` for errors, warnings, success
7. **Show progress** with `click.progressbar()` for long operations
8. **Test with `CliRunner`** for comprehensive CLI testing
9. **Handle errors gracefully** with try/except and exit codes
10. **Use `click.echo()`** instead of `print()` for testability

---

## 3. Python pathlib Documentation

### 3.1 Library Overview

**Version**: Built-in (Python 3.4+)
**Purpose**: Object-oriented filesystem paths
**Official Docs**: https://docs.python.org/3/library/pathlib.html

**Key Features**:
- Cross-platform path handling
- Intuitive path operations (/, joinpath)
- File existence and type checking
- Globbing and pattern matching
- Path resolution and normalization

### 3.2 Core Operations for Catalog System

#### Path Creation and Resolution

```python
from pathlib import Path
import os

# Create Path objects
home = Path.home()  # /Users/username
cwd = Path.cwd()    # Current working directory

# Build paths
claude_dir = home / '.claude'
skills_dir = claude_dir / 'skills'
skill_path = skills_dir / 'analysis' / 'skill.md'

# Alternative: joinpath
skill_path = home.joinpath('.claude', 'skills', 'analysis', 'skill.md')

# From string
path = Path('/Users/username/.claude/skills/analysis')

# Resolve to absolute path (follows symlinks)
absolute = path.resolve()

# Expand user home directory
path = Path('~/.claude').expanduser()  # /Users/username/.claude
```

#### Path Inspection

```python
from pathlib import Path

path = Path('/Users/username/.claude/skills/analysis/skill.md')

# Path components
path.name        # 'skill.md'
path.stem        # 'skill'
path.suffix      # '.md'
path.suffixes    # ['.md']
path.parent      # Path('/Users/username/.claude/skills/analysis')
path.parents[0]  # Path('/Users/username/.claude/skills/analysis')
path.parents[1]  # Path('/Users/username/.claude/skills')
path.parts       # ('/', 'Users', 'username', '.claude', 'skills', 'analysis', 'skill.md')

# Existence and type
path.exists()       # True/False
path.is_file()      # True/False
path.is_dir()       # True/False
path.is_symlink()   # True/False
path.is_absolute()  # True/False

# String representation
str(path)           # '/Users/username/.claude/skills/analysis/skill.md'
path.as_posix()     # '/' separators on all platforms
path.as_uri()       # 'file:///Users/username/.claude/skills/analysis/skill.md'
```

#### Directory Operations

```python
from pathlib import Path

# Create directory
skills_dir = Path.home() / '.claude' / 'skills'
skills_dir.mkdir(parents=True, exist_ok=True)

# parents=True: Create intermediate directories
# exist_ok=True: Don't raise error if exists

# List directory contents
for item in skills_dir.iterdir():
    if item.is_dir():
        print(f"Directory: {item.name}")
    elif item.is_file():
        print(f"File: {item.name}")

# Recursive directory listing
for item in skills_dir.rglob('*.md'):
    print(f"Markdown file: {item}")

# Walk directory tree (like os.walk)
for root, dirs, files in os.walk(skills_dir):
    root_path = Path(root)
    for file in files:
        file_path = root_path / file
        print(file_path)
```

#### Glob Patterns

```python
from pathlib import Path

claude_dir = Path.home() / '.claude'

# Glob in current directory
for md_file in claude_dir.glob('*.md'):
    print(md_file)

# Recursive glob
for md_file in claude_dir.rglob('*.md'):
    print(md_file)

# Glob with pattern
for skill in claude_dir.glob('skills/*/skill.md'):
    print(skill)

# Multiple patterns (use list comprehension)
patterns = ['*.md', '*.json']
files = [f for pattern in patterns for f in claude_dir.rglob(pattern)]
```

#### File Operations

```python
from pathlib import Path

skill_file = Path.home() / '.claude' / 'skills' / 'analysis' / 'skill.md'

# Read text
content = skill_file.read_text(encoding='utf-8')

# Read bytes
data = skill_file.read_bytes()

# Write text
skill_file.write_text('New content', encoding='utf-8')

# Write bytes
skill_file.write_bytes(b'Binary data')

# Open file (returns file handle)
with skill_file.open('r', encoding='utf-8') as f:
    lines = f.readlines()

# File stats
stats = skill_file.stat()
stats.st_size      # File size in bytes
stats.st_mtime     # Last modification time
stats.st_ctime     # Creation time

# Timestamps
from datetime import datetime
mtime = datetime.fromtimestamp(skill_file.stat().st_mtime)
```

### 3.3 Path Validation for Security

```python
from pathlib import Path

def validate_path_in_directory(path: Path, base: Path) -> bool:
    """
    Validate path is within allowed base directory.

    Prevents path traversal attacks (../).
    """
    try:
        # Resolve both paths to absolute
        path_resolved = path.resolve()
        base_resolved = base.resolve()

        # Check if path is relative to base
        path_resolved.relative_to(base_resolved)
        return True

    except ValueError:
        # relative_to() raises ValueError if not relative
        return False

# Example usage
base = Path.home() / '.claude'
safe_path = base / 'skills' / 'analysis'
unsafe_path = Path('/etc/passwd')

assert validate_path_in_directory(safe_path, base) == True
assert validate_path_in_directory(unsafe_path, base) == False

# Handle symbolic links
base = Path.home() / '.claude'
symlink_path = base / 'skills' / 'link-to-etc'  # Symlinks to /etc

# resolve() follows symlinks, so this will fail validation
assert validate_path_in_directory(symlink_path, base) == False
```

### 3.4 Best Practices for Catalog System

1. **Use `Path` instead of string paths** for type safety
2. **Use `/` operator** for path joining (cleaner than `joinpath`)
3. **Always resolve() paths** before validation to handle symlinks
4. **Use `mkdir(parents=True, exist_ok=True)`** for safe directory creation
5. **Use `rglob()` for recursive searches** (simpler than os.walk)
6. **Use `read_text()` / `write_text()`** for simple file operations
7. **Validate paths** with `relative_to()` to prevent traversal
8. **Check existence** with `exists()` before operations
9. **Use `iterdir()` for directory listing** (returns Path objects)
10. **Use `as_posix()`** for cross-platform path strings

---

## 4. JSON Schema Validation

### 4.1 Overview

**Purpose**: Validate JSON data against schemas
**Integration**: Pydantic generates JSON schemas automatically

### 4.2 Pydantic → JSON Schema

```python
from pydantic import BaseModel, Field
import json

class SkillCatalogEntry(BaseModel):
    id: str = Field(..., description="UUID of skill")
    name: str = Field(..., min_length=1, max_length=100)
    template: Literal["basic", "analysis"]

# Generate JSON schema
schema = SkillCatalogEntry.model_json_schema()

print(json.dumps(schema, indent=2))
# {
#   "$defs": {},
#   "properties": {
#     "id": {
#       "description": "UUID of skill",
#       "title": "Id",
#       "type": "string"
#     },
#     "name": {
#       "maxLength": 100,
#       "minLength": 1,
#       "title": "Name",
#       "type": "string"
#     },
#     "template": {
#       "enum": ["basic", "analysis"],
#       "title": "Template",
#       "type": "string"
#     }
#   },
#   "required": ["id", "name", "template"],
#   "title": "SkillCatalogEntry",
#   "type": "object"
# }
```

### 4.3 Validation with jsonschema

```python
import jsonschema
from jsonschema import validate, ValidationError

# Define schema manually (or use Pydantic-generated)
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "scope": {"type": "string", "enum": ["global", "project", "local"]}
    },
    "required": ["name", "scope"]
}

# Valid data
valid_data = {"name": "analysis", "scope": "global"}

try:
    validate(instance=valid_data, schema=schema)
    print("Valid!")
except ValidationError as e:
    print(f"Validation error: {e.message}")

# Invalid data
invalid_data = {"name": "", "scope": "invalid"}

try:
    validate(instance=invalid_data, schema=schema)
except ValidationError as e:
    print(f"Validation error: {e.message}")
    # "'' is too short"
```

### 4.4 Best Practices

1. **Use Pydantic for validation** (simpler than manual jsonschema)
2. **Generate JSON schemas** with `model_json_schema()` for documentation
3. **Version schemas** (`schema_version` field in catalog)
4. **Validate on load and save** to catch corruption early
5. **Provide clear error messages** from Pydantic ValidationError

---

## 5. YAML Frontmatter Parsing

### 5.1 Library: python-frontmatter

**Package**: `python-frontmatter`
**Install**: `pip install python-frontmatter`

```python
import frontmatter
from pathlib import Path

# Read Markdown file with YAML frontmatter
skill_file = Path.home() / '.claude' / 'skills' / 'analysis' / 'skill.md'

# Parse frontmatter
post = frontmatter.load(skill_file)

# Access metadata
post.metadata  # Dict of YAML frontmatter
post.content   # Markdown content (without frontmatter)

# Example:
# ---
# title: Analysis Specialist
# description: Analyze feature requirements
# model: claude-opus-4
# ---
# # Skill content here...

print(post.metadata['title'])        # 'Analysis Specialist'
print(post.metadata['description'])  # 'Analyze feature requirements'
print(post.content)                   # '# Skill content here...'

# Handling missing frontmatter
if not post.metadata:
    print("No frontmatter found")

# Handling missing fields
template = post.metadata.get('template', 'basic')  # Default to 'basic'
```

### 5.2 Alternative: PyYAML

```python
import yaml
from pathlib import Path

skill_file = Path.home() / '.claude' / 'skills' / 'analysis' / 'skill.md'

content = skill_file.read_text(encoding='utf-8')

# Split frontmatter and content
if content.startswith('---'):
    parts = content.split('---', 2)
    if len(parts) >= 3:
        frontmatter_text = parts[1]
        markdown_content = parts[2]

        # Parse YAML
        metadata = yaml.safe_load(frontmatter_text)

        print(metadata)
        # {'title': 'Analysis Specialist', 'description': '...', ...}
```

### 5.3 Best Practices

1. **Use `python-frontmatter`** for simplicity (recommended)
2. **Handle missing frontmatter** gracefully (default values)
3. **Validate metadata** with Pydantic after extraction
4. **Use `safe_load()`** with PyYAML to prevent code execution
5. **Skip files without frontmatter** (log warning)

---

## 6. Integration Examples

### 6.1 Complete Catalog Entry Loading

```python
from pydantic import BaseModel, Field, ValidationError
from pathlib import Path
from datetime import datetime
from uuid import uuid4
import frontmatter
import logging

logger = logging.getLogger(__name__)

class SkillCatalogEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    scope: Literal["global", "project", "local"]
    path: Path
    template: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

def load_skill_from_file(skill_dir: Path, scope: str) -> Optional[SkillCatalogEntry]:
    """
    Load skill catalog entry from directory.

    Args:
        skill_dir: Path to skill directory
        scope: Scope (global/project/local)

    Returns:
        SkillCatalogEntry or None if invalid
    """
    try:
        # Find first .md file in directory
        md_files = list(skill_dir.glob('*.md'))
        if not md_files:
            logger.warning(f"No .md files in skill directory: {skill_dir}")
            return None

        skill_file = md_files[0]

        # Parse frontmatter
        post = frontmatter.load(skill_file)

        if not post.metadata:
            logger.warning(f"No frontmatter in skill file: {skill_file}")
            return None

        # Extract metadata
        metadata = post.metadata

        # Create catalog entry
        entry = SkillCatalogEntry(
            name=skill_dir.name,  # Use directory name as skill name
            description=metadata.get('description', ''),
            scope=scope,
            path=skill_dir.resolve(),
            template=metadata.get('template', 'basic'),
            created_at=metadata.get('created_at', datetime.utcnow()),
            updated_at=metadata.get('updated_at', datetime.utcnow())
        )

        return entry

    except ValidationError as e:
        logger.error(f"Validation error loading skill {skill_dir}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error loading skill {skill_dir}: {e}")
        return None
```

### 6.2 Complete CLI Command

```python
import click
from pathlib import Path
from typing import List
import json
from tabulate import tabulate

@click.group()
def cli():
    """LLM Catalog Management CLI"""
    pass

@cli.command()
@click.argument('element_type', type=click.Choice(['skills', 'commands', 'agents', 'all']))
@click.option('--scope', type=click.Choice(['global', 'project', 'local', 'all']), default='all')
@click.option('--format', type=click.Choice(['table', 'json', 'condensed']), default='table')
def list(element_type: str, scope: str, format: str):
    """
    List catalog elements.

    Examples:
        llm list skills
        llm list commands --scope project
        llm list all --format json
    """
    try:
        # Load catalog manager
        from catalog_manifest import CatalogManager
        from core.scope_manager import ScopeManager

        scope_mgr = ScopeManager()
        catalog_mgr = CatalogManager(scope_mgr)

        # List elements
        if element_type == 'all':
            skills = catalog_mgr.list_elements(ElementType.SKILL, scope)
            commands = catalog_mgr.list_elements(ElementType.COMMAND, scope)
            agents = catalog_mgr.list_elements(ElementType.AGENT, scope)
            elements = skills + commands + agents
        else:
            elem_type = ElementType(element_type.rstrip('s'))  # 'skills' → 'skill'
            elements = catalog_mgr.list_elements(elem_type, scope)

        # Format output
        if format == 'json':
            data = [elem.model_dump(mode='json') for elem in elements]
            click.echo(json.dumps(data, indent=2))

        elif format == 'table':
            if not elements:
                click.echo("No elements found.")
                return

            headers = ['Name', 'Type', 'Scope', 'Description']
            rows = [
                [e.name, e.element_type, e.scope, e.description[:50]]
                for e in elements
            ]
            table = tabulate(rows, headers=headers, tablefmt='grid')
            click.echo(table)

        elif format == 'condensed':
            for elem in elements:
                click.echo(f"{elem.name} ({elem.scope}) - {elem.element_type}")

        # Summary
        click.secho(f"\nTotal: {len(elements)} elements", fg='green')

    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red', err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
```

---

## 7. Summary of Library Integration

### 7.1 Component → Library Mapping

| Component | Primary Library | Purpose | Version |
|-----------|----------------|---------|---------|
| Data Models | Pydantic | Validation & serialization | 2.x |
| CLI Interface | Click | Command-line framework | 8.x |
| File Operations | pathlib | Path handling | stdlib |
| Frontmatter | python-frontmatter | YAML parsing | 1.x |
| JSON Validation | Pydantic | Schema validation | 2.x |

### 7.2 Installation Commands

```bash
# Core dependencies (already in project)
pip install pydantic>=2.0
pip install click>=8.0

# Additional dependencies
pip install python-frontmatter>=1.0
pip install tabulate>=0.9  # For table formatting (optional)
pip install rich>=13.0      # For rich CLI output (optional)

# Or with uv (project standard)
uv pip install pydantic click python-frontmatter tabulate
```

### 7.3 Key Takeaways

1. **Pydantic 2.x**: Use `model_config`, `field_validator`, `model_dump()`, `model_validate()`
2. **Click 8.x**: Use command groups, `click.Choice`, `click.secho`, `CliRunner` for testing
3. **pathlib**: Use `Path`, `/` operator, `rglob()`, `resolve()`, `relative_to()` for validation
4. **Frontmatter**: Use `python-frontmatter` for YAML extraction
5. **Validation**: Pydantic handles both runtime and schema validation

---

**Research Status**: ✅ COMPLETE

**Next Step**: Dependency Manager output
