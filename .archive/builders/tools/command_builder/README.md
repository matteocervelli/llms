# Command Builder Tool

Generate Claude Code slash command `.md` files with YAML frontmatter, parameter configuration, bash command integration, and file references.

## Features

✨ **Interactive Wizard** - Beautiful CLI prompts with questionary
🔒 **Security-First** - Input validation, path traversal prevention, bash safety checks
📝 **Templates** - 4 built-in templates (basic, with_bash, with_files, advanced)
🎯 **Scope Management** - Global, project, and local scopes
📊 **Catalog System** - Track all commands with JSON catalog
⚡ **CLI & Programmatic** - Both interactive and non-interactive modes

## Installation

```bash
# Install dependencies
uv pip install -r requirements.txt

# Or install individually
uv pip install click pydantic pyyaml jinja2 questionary python-frontmatter
```

## Usage

### Interactive Mode (Recommended)

```bash
python -m src.tools.command_builder.main create
```

The interactive wizard guides you through:
1. Command name (slug format)
2. Description
3. Scope selection (global/project/local)
4. Template selection
5. Parameters (optional)
6. Bash commands (optional, with safety checks)
7. File references (optional, with validation)
8. Thinking mode toggle
9. Additional YAML frontmatter
10. Preview and confirmation

### Non-Interactive Mode

```bash
# Simple command
python -m src.tools.command_builder.main generate \
  --name my-command \
  --description "My custom command" \
  --scope project \
  --template basic

# With options
python -m src.tools.command_builder.main generate \
  --name deploy \
  --description "Deploy to production" \
  --scope project \
  --template with_bash \
  --overwrite
```

### List Commands

```bash
# List all commands
python -m src.tools.command_builder.main list

# Filter by scope
python -m src.tools.command_builder.main list --scope global

# Search commands
python -m src.tools.command_builder.main list --search "deploy"
```

### Delete Commands

```bash
# Interactive confirmation
python -m src.tools.command_builder.main delete my-command

# Skip confirmation
python -m src.tools.command_builder.main delete my-command --yes

# Specify scope if ambiguous
python -m src.tools.command_builder.main delete my-command --scope project
```

### Sync Catalog

When you manually add or delete command files, use sync to update the catalog:

```bash
# Sync catalog with actual files
python -m src.tools.command_builder.main sync

# Sync with specific project root
python -m src.tools.command_builder.main sync --project-root /path/to/project
```

**What sync does:**
- Scans `.claude/commands/` (project and global)
- Removes catalog entries for missing files
- Adds catalog entries for untracked files
- Shows detailed sync report (added, removed, unchanged)

**When to use sync:**
- After manually deleting command files
- After manually creating command files
- When catalog seems out of sync
- After moving files between scopes

### Other Commands

```bash
# List available templates
python -m src.tools.command_builder.main templates

# Show statistics
python -m src.tools.command_builder.main stats

# Validate a command file
python -m src.tools.command_builder.main validate path/to/command.md
```

## Programmatic Usage

```python
from pathlib import Path
from src.tools.command_builder import CommandConfig, CommandBuilder, ScopeType

# Create configuration
config = CommandConfig(
    name="my-command",
    description="My custom command",
    scope=ScopeType.PROJECT,
    template="basic",
)

# Build command
builder = CommandBuilder()
command_path, content = builder.build_command(config)

print(f"Command created at: {command_path}")
```

### With Parameters

```python
from src.tools.command_builder import CommandConfig, CommandParameter, ParameterType

config = CommandConfig(
    name="greet",
    description="Greet someone",
    parameters=[
        CommandParameter(
            name="name",
            type=ParameterType.STRING,
            description="Person's name",
            required=True,
        ),
        CommandParameter(
            name="greeting",
            type=ParameterType.CHOICE,
            description="Greeting type",
            required=False,
            default="hello",
            choices=["hello", "hi", "hey"],
        ),
    ],
)
```

### With Bash Commands

```python
config = CommandConfig(
    name="run-tests",
    description="Run project tests",
    bash_commands=[
        "pytest tests/",
        "coverage report",
    ],
    template="with_bash",
)
```

### With File References

```python
config = CommandConfig(
    name="review",
    description="Review code changes",
    file_references=[
        "src/main.py",
        "tests/test_main.py",
        "README.md",
    ],
    template="with_files",
)
```

## Templates

### basic
Simple command with description and optional parameters.

### with_bash
Command with bash command execution (`!command` syntax).

### with_files
Command with file references (`@file` syntax).

### advanced
Full-featured template with all options, table formatting, and examples.

## Security Features

### Input Validation
- Command names: slug format (lowercase-with-hyphens)
- Reserved names blocked
- Length limits enforced

### Bash Safety
- Dangerous commands detected (rm -rf, dd, fork bombs, etc.)
- Warnings for shell operators and redirects
- Safe command whitelist

### Path Security
- Path traversal prevention (..)
- File references validated within project
- Template names sanitized

### YAML Safety
- Safe YAML loading
- Value sanitization
- Control character removal

## Scope System

### Global (`~/.claude/commands/`)
- User-wide commands
- Available in all projects
- Stored in home directory

### Project (`.claude/commands/`)
- Project-specific commands
- Team-shared (committed to git)
- Scoped to project directory

### Local (`.claude/commands/`)
- Project-local commands
- Not committed (add to .gitignore)
- Same directory as project scope

## Catalog System

Commands are tracked in `commands.json`:

```json
{
  "schema_version": "1.0",
  "commands": [
    {
      "id": "uuid-v4",
      "name": "command-name",
      "description": "Command description",
      "scope": "project",
      "path": "/absolute/path/to/command.md",
      "created_at": "2025-10-26T...",
      "updated_at": "2025-10-26T...",
      "metadata": {
        "template": "basic",
        "has_parameters": false,
        "has_bash": false,
        "has_files": false,
        "thinking_mode": false
      }
    }
  ]
}
```

## API Reference

### CommandConfig

Main configuration model for commands.

**Fields:**
- `name` (str): Command name (slug format)
- `description` (str): Command description
- `scope` (ScopeType): Command scope
- `parameters` (List[CommandParameter]): Command parameters
- `bash_commands` (List[str]): Bash commands to execute
- `file_references` (List[str]): File references
- `thinking_mode` (bool): Enable extended thinking
- `template` (str): Template name
- `frontmatter` (Dict[str, Any]): Additional YAML fields

### CommandParameter

Parameter configuration for commands.

**Fields:**
- `name` (str): Parameter name (lowercase_with_underscores)
- `type` (ParameterType): Parameter type
- `description` (str): Parameter description
- `required` (bool): Whether required
- `default` (Any): Default value (if not required)
- `choices` (List[str]): Valid choices (for choice type)

### CommandBuilder

Core builder for command generation.

**Methods:**
- `build_command(config, project_root, overwrite)` - Build command file
- `update_command(command_path, config)` - Update existing command
- `delete_command(command_path)` - Delete command file
- `validate_command_file(command_path)` - Validate command file

### CatalogManager

Manages commands.json catalog.

**Methods:**
- `add_command(entry)` - Add command to catalog
- `update_command(entry)` - Update command in catalog
- `remove_command(cmd_id)` - Remove command from catalog
- `get_command(name, cmd_id, scope)` - Get command entry
- `list_commands(scope)` - List commands
- `search_commands(query, scope, has_parameters, has_bash)` - Search commands
- `get_catalog_stats()` - Get catalog statistics

### TemplateManager

Manages Jinja2 templates.

**Methods:**
- `list_templates()` - List available templates
- `template_exists(template_name)` - Check if template exists
- `load_template(template_name)` - Load Jinja2 template
- `render_template(template_name, config)` - Render template
- `create_custom_template(template_name, content)` - Create custom template

### Validator

Static validation methods.

**Methods:**
- `validate_command_name(name)` - Validate command name
- `validate_bash_command(command)` - Validate bash command safety
- `validate_file_reference(file_ref, project_root)` - Validate file reference
- `validate_template_name(template)` - Validate template name
- `sanitize_yaml_value(value)` - Sanitize YAML value
- `validate_scope_path(scope_path)` - Validate scope path

## Examples

See [docs/guides/command-builder-guide.md](../../../docs/guides/command-builder-guide.md) for comprehensive examples and tutorials.

## Troubleshooting

### "Command already exists"
Use `--overwrite` flag or delete the existing command first.

### "Unsafe bash command detected"
The command contains dangerous patterns. Review the error message and adjust the command.

### "Path traversal detected"
File references must be within the project directory. Remove `..` from paths.

### "Template not found"
Run `command-builder templates` to see available templates.

## Development

### Running Tests

```bash
pytest tests/test_command_builder.py -v --cov=src/tools/command_builder
```

### Code Quality

```bash
# Format
black src/tools/command_builder/

# Lint
flake8 src/tools/command_builder/

# Type check
mypy src/tools/command_builder/
```

## License

Part of the LLM Configuration Management System.

## Related

- [Skill Builder](../skill_builder/) - Build Claude Code skills
- [Agent Builder](../agent_builder/) - Build sub-agents
- [Documentation](../../../docs/guides/) - Full documentation
