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

# LLM Adapter Architecture

The LLM Adapter Architecture provides a uniform interface for creating and managing skills, commands, and agents across multiple LLM providers (Claude Code, Codex, OpenCode, etc.).

## Overview

The adapter system uses the **Adapter Pattern** to abstract differences between LLM providers while maintaining a consistent API. Each LLM has different file formats, directory structures, and configuration requirements, but the adapter provides a unified interface.

### Supported Adapters

- **ClaudeAdapter**: Claude Code (Markdown-based, Sprint 1)
- **CodexAdapter**: OpenAI Codex (Planned, Sprint 5+)
- **OpenCodeAdapter**: Open-source alternatives (Planned, Sprint 5+)

## Quick Start

### Creating Skills

```python
from src.core.llm_adapter import ClaudeAdapter
from src.core.scope_manager import ScopeManager

# Get scope configuration
manager = ScopeManager()
scope = manager.get_effective_scope('--global')

# Create adapter
adapter = ClaudeAdapter(scope)

# Create a skill
result = adapter.create_skill(
    name="my-skill",
    description="A helpful skill for data processing",
    content="# Implementation\n\nSkill logic here"
)

if result.success:
    print(f"Skill created at: {result.path}")
```

### Creating Commands

```python
result = adapter.create_command(
    name="deploy",
    description="Deploy application to production",
    content="# Deploy Command\n\nDeployment steps here"
)
```

### Creating Agents

```python
result = adapter.create_agent(
    name="code-reviewer",
    description="Automated code review agent",
    content="# Code Review Agent\n\nReview logic here"
)
```

## Architecture

### Components

1. **LLMAdapter (Abstract Base Class)**
   - Defines interface for all adapters
   - Provides common validation and sanitization
   - Enforces consistent behavior

2. **ClaudeAdapter (Concrete Implementation)**
   - Implements Claude Code-specific logic
   - Handles Markdown formatting
   - Manages `.claude/` directory structure

3. **Data Models**
   - `CreationResult`: Standardized return values
   - `AdapterMetadata`: Adapter capabilities
   - `ElementType`: Skill/Command/Agent types

4. **Exceptions**
   - `InvalidNameError`: Name validation failures
   - `CreationError`: File creation failures
   - `UnsupportedScopeError`: Scope compatibility errors

### Directory Structure

ClaudeAdapter creates files in the following structure:

```
{scope_path}/
├── skills/
│   ├── skill1.md
│   └── skill2.md
├── commands/
│   ├── command1.md
│   └── command2.md
└── agents/
    ├── agent1.md
    └── agent2.md
```

## API Reference

### LLMAdapter (Abstract Base Class)

#### `create_skill(name: str, description: str, content: str, **kwargs) -> CreationResult`

Create a new skill.

**Parameters:**
- `name`: Skill name (alphanumeric, hyphens, underscores only)
- `description`: Brief description of the skill
- `content`: Skill implementation content
- `**kwargs`: Additional LLM-specific parameters

**Returns:** `CreationResult` with path and status

**Raises:**
- `InvalidNameError`: If the skill name is invalid
- `CreationError`: If file creation fails

**Validation Rules:**
- Name must match pattern: `^[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?$`
- Name length: 1-64 characters
- Must start and end with alphanumeric characters

#### `create_command(name: str, description: str, content: str, **kwargs) -> CreationResult`

Create a new slash command.

**Parameters:** Same as `create_skill()`

**Returns:** `CreationResult` with path and status

#### `create_agent(name: str, description: str, content: str, **kwargs) -> CreationResult`

Create a new sub-agent.

**Parameters:** Same as `create_skill()`

**Returns:** `CreationResult` with path and status

#### `validate_name(name: str, element_type: ElementType) -> None`

Validate an element name.

**Parameters:**
- `name`: Name to validate
- `element_type`: Type of element (SKILL, COMMAND, or AGENT)

**Raises:** `InvalidNameError` if validation fails

#### `sanitize_input(text: str, max_length: Optional[int] = None) -> str`

Sanitize user input text.

**Parameters:**
- `text`: Text to sanitize
- `max_length`: Optional maximum length (default: 500)

**Returns:** Sanitized text

**Sanitization:**
- Removes null bytes and control characters
- Preserves newlines
- Enforces length limits
- Strips leading/trailing whitespace

### ClaudeAdapter

#### `__init__(scope_config: ScopeConfig) -> None`

Initialize the Claude adapter.

**Parameters:**
- `scope_config`: Scope configuration from ScopeManager

**Raises:** `UnsupportedScopeError` if scope is not supported

**Example:**
```python
from src.core.llm_adapter import ClaudeAdapter
from src.core.scope_manager import ScopeManager

manager = ScopeManager()
scope = manager.get_effective_scope('--global')
adapter = ClaudeAdapter(scope)
```

#### `create_skill(name, description, content, overwrite=False) -> CreationResult`

Create a Claude Code skill.

**Additional Parameters:**
- `overwrite`: Whether to overwrite existing file (default: False)

**Example:**
```python
result = adapter.create_skill(
    name="data-processor",
    description="Process and transform data",
    content="# Data Processor\n\nImplementation here",
    overwrite=False
)
```

### CreationResult

Dataclass representing the result of a creation operation.

**Attributes:**
- `path: Path` - Path to the created file
- `element_type: ElementType` - Type of element created
- `success: bool` - Whether creation was successful
- `message: str` - Human-readable status message
- `metadata: Dict[str, Any]` - Additional metadata

**Example:**
```python
result = adapter.create_skill(...)
if result.success:
    print(f"Created at: {result.path}")
    print(f"Scope: {result.metadata['scope']}")
    print(f"Created: {result.metadata['created_at']}")
```

### AdapterMetadata

Dataclass describing adapter capabilities.

**Attributes:**
- `name: str` - Adapter name
- `version: str` - Adapter version
- `supported_scopes: List[str]` - Supported scope types
- `supported_elements: List[ElementType]` - Supported element types
- `requires_config: bool` - Whether adapter requires configuration

**Methods:**
- `supports_scope(scope: str) -> bool` - Check scope support
- `supports_element(element_type: ElementType) -> bool` - Check element support

**Example:**
```python
adapter = ClaudeAdapter(scope)
metadata = adapter.metadata

print(f"Adapter: {metadata.name} v{metadata.version}")
print(f"Scopes: {', '.join(metadata.supported_scopes)}")

if metadata.supports_element(ElementType.SKILL):
    print("Skills are supported")
```

### ElementType

Enum of supported element types.

**Values:**
- `SKILL = "skill"` - Reusable skill
- `COMMAND = "command"` - Slash command
- `AGENT = "agent"` - Sub-agent

## Error Handling

### AdapterError

Base exception for all adapter errors.

**Example:**
```python
from src.core.adapter_exceptions import AdapterError

try:
    result = adapter.create_skill(...)
except AdapterError as e:
    print(f"Adapter error: {e}")
```

### InvalidNameError

Raised when a skill/command/agent name fails validation.

**Example:**
```python
from src.core.adapter_exceptions import InvalidNameError

try:
    adapter.create_skill(name="invalid name!", ...)
except InvalidNameError as e:
    print(f"Invalid name: {e}")
```

### CreationError

Raised when file or directory creation fails.

**Common Causes:**
- Insufficient write permissions
- File already exists (without `overwrite=True`)
- Parent directory doesn't exist
- Disk space issues

**Example:**
```python
from src.core.adapter_exceptions import CreationError

try:
    adapter.create_skill(name="test", ...)
except CreationError as e:
    print(f"Creation failed: {e}")
```

### UnsupportedScopeError

Raised when an adapter doesn't support a scope type.

**Example:**
```python
from src.core.adapter_exceptions import UnsupportedScopeError

try:
    adapter = CustomAdapter(scope_config)
except UnsupportedScopeError as e:
    print(f"Scope not supported: {e}")
```

## Security & Performance

### Security Measures

1. **Input Validation**
   - Names: alphanumeric, hyphens, underscores only
   - Length limits: names ≤ 64 chars, descriptions ≤ 500 chars
   - Pattern matching: `^[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?$`

2. **Path Traversal Prevention**
   - Use `Path.resolve()` for all paths
   - No `../` allowed in names
   - Absolute paths blocked

3. **Sanitization**
   - Remove null bytes and control characters
   - Preserve newlines only
   - Strip leading/trailing whitespace

4. **Permission Checks**
   - Verify write permissions before operations
   - Handle permission errors gracefully

### Performance Targets

- Single file creation: < 50ms
- Name validation: < 5ms
- Template rendering: < 10ms

*Targets based on local filesystem operations*

## Best Practices

### Naming Conventions

✅ **Good Names:**
- `my-skill`
- `data_processor`
- `api-client-v2`
- `ML-model`

❌ **Bad Names:**
- `my skill` (spaces)
- `my-skill!` (special chars)
- `-myskill` (starts with hyphen)
- `myskill-` (ends with hyphen)

### File Organization

```
# Global scope (personal tools)
~/.claude/
├── skills/
│   └── personal-helper.md
└── commands/
    └── quick-deploy.md

# Project scope (team-shared)
project/.claude/
├── skills/
│   └── project-analyzer.md
├── commands/
│   └── project-build.md
└── agents/
    └── code-reviewer.md
```

### Error Handling

```python
from src.core.adapter_exceptions import InvalidNameError, CreationError

try:
    result = adapter.create_skill(
        name=user_input_name,
        description=description,
        content=content
    )

    if result.success:
        print(f"✓ Created: {result.path}")

except InvalidNameError as e:
    print(f"✗ Invalid name: {e}")
    # Prompt user for valid name

except CreationError as e:
    print(f"✗ Creation failed: {e}")
    # Handle filesystem error
```

## Examples

### Example 1: Create Skill with Auto-Detected Scope

```python
from src.core.llm_adapter import ClaudeAdapter
from src.core.scope_manager import ScopeManager

# Auto-detect scope
manager = ScopeManager()
scope = manager.get_effective_scope()

# Create adapter
adapter = ClaudeAdapter(scope)

# Create skill
result = adapter.create_skill(
    name="json-formatter",
    description="Format JSON with proper indentation",
    content="""# JSON Formatter

Format and validate JSON data.

## Usage

Provide JSON string to format and validate.
"""
)

print(f"Created in {result.metadata['scope']} scope")
print(f"Path: {result.path}")
```

### Example 2: Create Multiple Elements

```python
from src.core.llm_adapter import ClaudeAdapter
from src.core.scope_manager import ScopeManager

manager = ScopeManager()
scope = manager.get_effective_scope('--project')
adapter = ClaudeAdapter(scope)

# Create skill
skill = adapter.create_skill(
    name="api-client",
    description="REST API client helper",
    content="# API Client\n\nImplementation"
)

# Create command
command = adapter.create_command(
    name="deploy",
    description="Deploy to production",
    content="# Deploy\n\nDeployment steps"
)

# Create agent
agent = adapter.create_agent(
    name="reviewer",
    description="Code review agent",
    content="# Reviewer\n\nReview logic"
)

print(f"Created {len([skill, command, agent])} elements")
```

### Example 3: Overwrite Existing Skill

```python
from src.core.llm_adapter import ClaudeAdapter
from src.core.adapter_exceptions import CreationError

# First creation
result1 = adapter.create_skill(
    name="test",
    description="Version 1",
    content="Content v1"
)

# Second creation (fails without overwrite)
try:
    result2 = adapter.create_skill(
        name="test",
        description="Version 2",
        content="Content v2"
    )
except CreationError as e:
    print(f"Expected error: {e}")

# Second creation (succeeds with overwrite)
result3 = adapter.create_skill(
    name="test",
    description="Version 2",
    content="Content v2",
    overwrite=True
)

print(f"Updated: {result3.path}")
```

### Example 4: Cross-Scope Creation

```python
from src.core.llm_adapter import ClaudeAdapter
from src.core.scope_manager import ScopeManager

manager = ScopeManager()

# Create global skill
global_scope = manager.get_effective_scope('--global')
global_adapter = ClaudeAdapter(global_scope)
global_skill = global_adapter.create_skill(
    name="personal-helper",
    description="Personal productivity helper",
    content="# Personal Helper\n\nPersonal tools"
)

# Create project skill
project_scope = manager.get_effective_scope('--project')
project_adapter = ClaudeAdapter(project_scope)
project_skill = project_adapter.create_skill(
    name="team-analyzer",
    description="Team collaboration analyzer",
    content="# Team Analyzer\n\nTeam tools"
)

print(f"Global: {global_skill.path}")
print(f"Project: {project_skill.path}")
```

## Adding New Adapters

To add support for a new LLM provider:

1. **Create Adapter Class**
   ```python
   from src.core.llm_adapter import LLMAdapter
   from src.core.adapter_models import AdapterMetadata, ElementType

   class MyAdapter(LLMAdapter):
       def _get_metadata(self) -> AdapterMetadata:
           return AdapterMetadata(
               name="my-llm",
               version="1.0.0",
               supported_scopes=["global", "project"],
               supported_elements=[ElementType.SKILL]
           )

       def create_skill(self, name, description, content, **kwargs):
           # Implement skill creation
           pass

       def create_command(self, name, description, content, **kwargs):
           # Implement command creation
           pass

       def create_agent(self, name, description, content, **kwargs):
           # Implement agent creation
           pass
   ```

2. **Implement Provider-Specific Logic**
   - File format handling
   - Directory structure
   - Template rendering

3. **Add Tests**
   - Unit tests for all methods
   - Integration tests with ScopeManager
   - Target 85%+ coverage

4. **Document**
   - Update this README
   - Add usage examples
   - Create ADR if needed

See [ADR-002: LLM Adapter Architecture](../../docs/architecture/ADR/ADR-002-llm-adapter-architecture.md) for design rationale.

## Testing

Run adapter tests:

```bash
# All adapter tests
pytest tests/test_llm_adapter.py tests/test_adapter_integration.py

# With coverage
pytest tests/test_llm_adapter.py --cov=src/core/llm_adapter --cov-report=term-missing

# Verbose output
pytest tests/test_llm_adapter.py -v
```

---

For more information:
- [Scope Intelligence ADR](../../docs/architecture/ADR/ADR-001-scope-intelligence-system.md)
- [LLM Adapter ADR](../../docs/architecture/ADR/ADR-002-llm-adapter-architecture.md)
