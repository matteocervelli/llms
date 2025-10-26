# Scope Intelligence System

The Scope Intelligence System manages Claude Code's three-tier configuration scope with automatic detection and intelligent precedence handling.

## Overview

The scope system allows configurations to be managed at three different levels:

- **Global Scope** (`~/.claude/`): User-wide settings that apply to all projects
- **Project Scope** (`.claude/`): Project-specific settings shared with the team
- **Local Scope** (`.claude/settings.local.json`): Project-local settings not committed to version control

**Configuration Precedence**: Local > Project > Global

## Quick Start

### Basic Usage

```python
from src.core.scope_manager import ScopeManager, ScopeType

# Auto-detect scope based on current directory
manager = ScopeManager()
scope = manager.detect_scope()
print(f"Detected scope: {scope.value}")

# Get all scopes with precedence
scopes = manager.resolve_all_scopes()
for scope in scopes:
    print(f"{scope.type.value}: {scope.path} (precedence: {scope.precedence})")
```

### CLI Flag Handling

```python
from src.core.scope_manager import ScopeManager

manager = ScopeManager()

# Force global scope
scope = manager.get_effective_scope('--global')
print(f"Using: {scope.path}")

# Force project scope
scope = manager.get_effective_scope('--project')
print(f"Using: {scope.path}")

# Force local scope
scope = manager.get_effective_scope('--local')
print(f"Using: {scope.path}")

# Auto-detect (no flag)
scope = manager.get_effective_scope()
print(f"Auto-detected: {scope.path}")
```

## Scope Types

### Global Scope

- **Location**: `~/.claude/`
- **Purpose**: User-wide settings that apply to all projects
- **Precedence**: Lowest (3)
- **Always Available**: Yes
- **Example Use Cases**:
  - Default templates
  - Personal preferences
  - Global API keys (use with caution)

### Project Scope

- **Location**: `.claude/` in project root
- **Purpose**: Project-specific settings shared with the team
- **Precedence**: Medium (2)
- **Detection**: Searches upward for `.claude/` directory or `.git` marker
- **Example Use Cases**:
  - Project-specific skills
  - Team-shared commands
  - Project agents
  - Committed configuration

### Local Scope

- **Location**: `.claude/settings.local.json` in project root
- **Purpose**: Project-local settings not committed to version control
- **Precedence**: Highest (1)
- **Detection**: Requires project scope to exist first
- **Example Use Cases**:
  - Personal project overrides
  - Development-only settings
  - Local API keys
  - Machine-specific configuration

## API Reference

### ScopeManager

Main class for scope management.

#### `__init__(cwd: Optional[Path] = None)`

Initialize the scope manager.

**Parameters:**
- `cwd`: Current working directory (defaults to `Path.cwd()`)

**Example:**
```python
manager = ScopeManager()  # Uses current directory
manager = ScopeManager(Path("/path/to/project"))  # Explicit path
```

#### `detect_scope() -> ScopeType`

Automatically detect the appropriate scope based on current directory.

**Returns:** Detected scope type (GLOBAL, PROJECT, or LOCAL)

**Detection Logic:**
1. Check for local scope (`.claude/settings.local.json`)
2. Check for project scope (`.claude/` in current or parent dirs)
3. Default to global scope (`~/.claude/`)

**Example:**
```python
manager = ScopeManager(Path("/home/user/project"))
scope = manager.detect_scope()  # Returns ScopeType.PROJECT
```

#### `get_global_path() -> Path`

Get the global scope path.

**Returns:** Resolved path to `~/.claude/`

#### `get_project_path() -> Optional[Path]`

Find the nearest project scope path.

**Returns:** Path to `.claude/` directory, or None if not found

#### `get_local_path() -> Optional[Path]`

Get the local scope path.

**Returns:** Path to `.claude/settings.local.json`, or None if project not found

#### `find_project_root() -> Optional[Path]`

Locate the project root directory.

**Returns:** Path to project root, or None if not in a project

**Project Markers:** `.git`, `.claude/`

#### `resolve_all_scopes() -> List[ScopeConfig]`

Resolve all applicable scopes with correct precedence.

**Returns:** Ordered list of scope configurations (Local > Project > Global)

**Example:**
```python
scopes = manager.resolve_all_scopes()
for scope in scopes:
    print(f"{scope.type.value}: precedence {scope.precedence}")
# Output:
# local: precedence 1
# project: precedence 2
# global: precedence 3
```

#### `get_effective_scope(flag: Optional[str] = None) -> ScopeConfig`

Get the effective scope based on CLI flag or auto-detection.

**Parameters:**
- `flag`: Optional CLI flag ('global', 'project', 'local', '--global', '--project', '--local')

**Returns:** The effective scope configuration to use

**Raises:**
- `InvalidScopeError`: If an invalid scope flag is provided
- `ScopeNotFoundError`: If the requested scope doesn't exist

**Example:**
```python
# Auto-detect
scope = manager.get_effective_scope()

# Explicit flag
scope = manager.get_effective_scope('--project')
```

#### `validate_scope_exists(scope_type: ScopeType) -> bool`

Check if a specific scope exists on the filesystem.

**Parameters:**
- `scope_type`: The scope type to validate

**Returns:** True if the scope exists, False otherwise

### ScopeConfig

Dataclass representing scope metadata.

**Attributes:**
- `path: Path` - Path to the scope directory or file
- `type: ScopeType` - Type of scope (GLOBAL, PROJECT, or LOCAL)
- `precedence: int` - Priority order (1=highest, 3=lowest)
- `exists: bool` - Whether the scope path currently exists on filesystem

### ScopeType

Enum of supported scope types.

**Values:**
- `GLOBAL = "global"` - User-wide scope
- `PROJECT = "project"` - Project-specific scope
- `LOCAL = "local"` - Project-local scope

## Error Handling

### ScopeError

Base exception for scope-related errors.

### ScopeNotFoundError

Raised when a requested scope does not exist.

**Example:**
```python
from src.core.scope_exceptions import ScopeNotFoundError

try:
    scope = manager.get_effective_scope('--project')
except ScopeNotFoundError as e:
    print(f"Error: {e}")
    # Handle missing project scope
```

### InvalidScopeError

Raised when an invalid scope type or configuration is specified.

**Example:**
```python
from src.core.scope_exceptions import InvalidScopeError

try:
    scope = manager.get_effective_scope('--invalid')
except InvalidScopeError as e:
    print(f"Error: {e}")
    # Handle invalid flag
```

### MultipleScopeFlagsError

Raised when multiple mutually exclusive scope flags are provided.

**Note:** This exception is typically handled by the CLI argument parser (e.g., Click) before reaching the ScopeManager.

## Best Practices

### Security

1. **Never commit secrets to Project scope** - Use Local scope for API keys
2. **Validate paths** - Always use resolved paths to prevent traversal attacks
3. **Check permissions** - Handle permission errors gracefully

### Performance

1. **Cache scope detection** - Detection is cached automatically
2. **Lazy loading** - Configs are only loaded when needed
3. **Minimize filesystem calls** - Use `resolve_all_scopes()` once

### Configuration Management

1. **Use precedence wisely** - Local > Project > Global
2. **Document scope choices** - Explain why settings are at specific scopes
3. **Version control** - Only commit Global and Project scopes, not Local

## Integration with CLI Tools

### Click Integration

```python
import click
from src.core.scope_manager import ScopeManager

@click.command()
@click.option('--global', 'scope_flag', flag_value='global', help='Use global scope')
@click.option('--project', 'scope_flag', flag_value='project', help='Use project scope')
@click.option('--local', 'scope_flag', flag_value='local', help='Use local scope')
def create_skill(scope_flag: Optional[str]) -> None:
    """Create a new skill."""
    manager = ScopeManager()

    try:
        scope = manager.get_effective_scope(scope_flag)
        click.echo(f"Creating skill in {scope.type.value} scope: {scope.path}")

        # Create skill at scope.path
        # ...

    except ScopeNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()
```

## Examples

### Example 1: Auto-detect Scope

```python
from src.core.scope_manager import ScopeManager

# In project directory: /home/user/myproject/src/
manager = ScopeManager()
scope = manager.detect_scope()

# Output: ScopeType.PROJECT
print(f"Detected: {scope.value}")
```

### Example 2: Get All Scopes with Precedence

```python
from src.core.scope_manager import ScopeManager

manager = ScopeManager()
scopes = manager.resolve_all_scopes()

for scope in scopes:
    exists_str = "✓" if scope.exists else "✗"
    print(f"{exists_str} {scope.type.value:8} (priority {scope.precedence}): {scope.path}")

# Output:
# ✓ local    (priority 1): /home/user/myproject/.claude/settings.local.json
# ✓ project  (priority 2): /home/user/myproject/.claude
# ✓ global   (priority 3): /home/user/.claude
```

### Example 3: Handle Missing Scope

```python
from src.core.scope_manager import ScopeManager
from src.core.scope_exceptions import ScopeNotFoundError

manager = ScopeManager()

try:
    scope = manager.get_effective_scope('--project')
    print(f"Using project at: {scope.path}")
except ScopeNotFoundError:
    print("Not in a project directory. Creating global scope instead.")
    scope = manager.get_effective_scope('--global')
    print(f"Using global at: {scope.path}")
```

### Example 4: Validate Scope Exists

```python
from src.core.scope_manager import ScopeManager, ScopeType

manager = ScopeManager()

if manager.validate_scope_exists(ScopeType.PROJECT):
    print("Project scope found!")
else:
    print("No project scope - run from project directory")
```

## Testing

Run the test suite:

```bash
# All tests
pytest tests/test_scope_manager.py

# With coverage
pytest tests/test_scope_manager.py --cov=src/core --cov-report=term-missing

# Verbose output
pytest tests/test_scope_manager.py -v
```

## Future Enhancements

- Multi-LLM support (`.codex/`, `.opencode/`)
- Custom scope patterns via plugins
- Configuration merging across scopes
- Encrypted settings support
- Remote scope synchronization

---

For more information, see the [Architecture Decision Record](../../docs/architecture/ADR/ADR-001-scope-intelligence-system.md).
