---
description: Create a new Claude Code command using the command builder tool
argument-hint: [name] [description]
---

# Create Claude Code Command

Create a new Claude Code slash command using the interactive command builder.

## Usage

```bash
/cc-create-command                      # Interactive wizard
/cc-create-command my-command          # With name (will prompt for details)
/cc-create-command my-command "Description"  # Quick create
```

## What it does

1. Launches interactive command builder wizard
2. Guides you through command creation:
   - Command name (slug format)
   - Description
   - Scope (global/project/local)
   - Template selection
   - Parameters (optional)
   - Bash commands (optional)
   - File references (optional)
   - Thinking mode (optional)
3. Generates command file in `.claude/commands/`
4. Adds to catalog for tracking
5. Shows usage example

## Execution

### Interactive mode (recommended)
!python -m src.tools.command_builder.main create

### Quick non-interactive mode
!python -m src.tools.command_builder.main generate --name "$1" --description "$2" --scope project --template basic

### Show available templates
!python -m src.tools.command_builder.main templates

### List all commands
!python -m src.tools.command_builder.main list

### Sync catalog with files
!python -m src.tools.command_builder.main sync

## Available Templates

- **basic**: Simple command with description and parameters
- **with_bash**: Command with bash command execution (!command)
- **with_files**: Command with file references (@file)
- **advanced**: Full-featured command with all options

## Command Naming Rules

- Use lowercase with hyphens (slug format)
- Start and end with alphanumeric
- No consecutive hyphens
- Max 63 characters
- Avoid reserved names (help, version, list, etc.)

## Examples

### Create a simple command
```bash
/cc-create-command
# Follow wizard prompts
```

### Create a test runner command
```bash
/cc-create-command run-tests "Run project tests with pytest"
# Add bash commands: pytest tests/ -v
# Select template: with_bash
```

### Create a documentation command
```bash
/cc-create-command generate-docs "Generate API documentation"
# Add file references: @README.md, @docs/api.md
# Select template: with_files
```

## After Creation

Your command will be available immediately:
```bash
/your-command-name
```

## Managing Commands

```bash
# List all commands
python -m src.tools.command_builder.main list

# Show statistics
python -m src.tools.command_builder.main stats

# Delete a command
python -m src.tools.command_builder.main delete command-name

# Sync catalog (after manual file changes)
python -m src.tools.command_builder.main sync

# Validate a command file
python -m src.tools.command_builder.main validate .claude/commands/my-command.md
```

## Tips

- Use descriptive command names that indicate the action
- Add comprehensive descriptions for better discoverability
- Choose the right template for your use case
- Test bash commands before adding them
- Use project scope for team-shared commands
- Use global scope for personal commands across all projects
- Document your commands well for future reference

## Related Tools

- **Command Builder**: `python -m src.tools.command_builder.main`
- **List Templates**: `/cc-create-command` then choose interactive mode
- **Documentation**: See `src/tools/command_builder/README.md`
