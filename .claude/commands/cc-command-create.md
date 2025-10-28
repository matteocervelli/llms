---
description: Create a new Claude Code command using the command builder tool
argument-hint: [name] [description] [--tech <library>] [--doc-url <url>] [--depth <n>]
---

# Create Claude Code Command

Create a new Claude Code slash command using the interactive command builder with optional documentation integration.

## Usage

```bash
/cc-command-create                      # Interactive wizard
/cc-command-create my-command          # With name (will prompt for details)
/cc-command-create my-command "Description"  # Quick create

# With documentation integration
/cc-command-create test-runner "Run pytest tests" --tech pytest
/cc-command-create api-docs "Generate API docs" --doc-url https://docs.example.com --depth 2
```

**💡 Pro Tip:** For safer command planning, activate Plan Mode (press Shift+Tab twice) before running this command. This allows you to review the command structure before creation.

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
3. **Optional:** Fetch library documentation via Context7
4. **Optional:** Deep-crawl documentation sites via Crawl4AI
5. Generates command file with inline documentation references
6. Adds to catalog for tracking
7. Shows usage example

## Parameters

- `name`: Command name (slug format, follows [context-]object-action[-modifier] pattern)
- `description`: Brief description of what the command does
- `--tech <library>`: Fetch documentation for a specific library/framework via Context7
- `--doc-url <url>`: URL to documentation site to crawl
- `--depth <n>`: Crawl depth for multi-level documentation (1-3, default: 1)

## Documentation Integration

### Context7 Integration

Fetch up-to-date library documentation when creating commands:

```bash
# Resolve library and fetch docs
!mcp__context7__resolve-library-id "$tech"
!mcp__context7__get-library-docs "$context7_library_id" --tokens 3000 --topic "$topic"
```

**Example:**

```bash
/cc-command-create test-runner "Run pytest tests" --tech pytest
```

This will:

- Resolve "pytest" to Context7 library ID
- Fetch pytest documentation (CLI, fixtures, markers)
- Add relevant snippets as reference comments in command template

### Crawl4AI Deep Crawling

Crawl documentation sites with configurable depth:

```bash
# Deep crawl documentation (multi-level)
!python -m src.tools.doc_fetcher.crawler "$doc_url" --depth "$depth"
```

**Example:**

```bash
/cc-command-create api-guide "API integration guide" --doc-url https://docs.example.com/api --depth 2
```

This will:

- Start from the provided URL
- Extract internal documentation links
- Crawl linked pages up to depth 2
- Consolidate markdown content
- Inject aggregated docs into command template

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

## Command Naming Convention

Commands must follow the **[context-]object-action[-modifier]** pattern:

### Pattern Structure

- **context** (optional): Domain prefix (cc-, gh-, project-, pr-, code-, feature-, issue-, ui-, infrastructure-)
- **object** (required): Noun describing what you work with (command, skill, agent, feature, issue, pr, component, etc.)
- **action** (required): Verb describing what you do (create, improve, fix, implement, analyze, setup, configure, etc.)
- **modifier** (optional): Additional context or specifier

### Examples

✅ **Good naming:**
- `cc-command-create` - context: cc, object: command, action: create
- `cc-command-improve` - context: cc, object: command, action: improve
- `feature-implement` - object: feature, action: implement
- `gh-milestone-create` - context: gh, object: milestone, action: create
- `pr-analyze-failure` - context: pr, object: analyze, action: failure (with modifier)

⚠️ **Acceptable with warnings:**
- `create-command` - Wrong order (should be command-create)
- `setup-infrastructure` - Action-object order (suggest infrastructure-setup)

❌ **Invalid:**
- `create` - Missing object
- `command` - Missing action
- `my-awesome-new-command-that-is-very-long-with-many-parts` - Too long (max 50 chars)

### Additional Rules

- Use lowercase with hyphens (slug format)
- Start and end with alphanumeric
- No consecutive hyphens
- Max 50 characters
- Avoid reserved names (help, version, list, etc.)

### Validation Modes

The command builder supports two validation modes:

- **Permissive (default)**: Allows non-standard names with warnings and suggestions
- **Strict**: Enforces naming convention, blocks non-compliant names

Use `--strict-naming` flag for strict validation.

## Examples

### Create a simple command

```bash
/cc-command-create
# Follow wizard prompts
```

### Create a test runner with pytest docs

```bash
/cc-command-create test-runner "Run project tests with pytest" --tech pytest
```

This fetches pytest documentation and generates a command with:

- Best practices for test organization
- Common pytest CLI options
- Fixture usage examples
- Marker strategies

### Create API integration guide with deep crawling

```bash
/cc-command-create api-integration "FastAPI integration guide" --doc-url https://fastapi.tiangolo.com --depth 2
```

This crawls FastAPI documentation (2 levels deep) and creates a command with:

- API route definitions
- Dependency injection patterns
- Request/response models
- Authentication examples

### Create command with both integrations

```bash
/cc-command-create db-migrate "Database migration command" --tech alembic --doc-url https://alembic.sqlalchemy.org/en/latest/ --depth 1
```

Combines Context7 library docs with site crawling for comprehensive reference.

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

- **Use Plan Mode** (Shift+Tab twice) to preview command structure before creation, especially for complex commands with multiple bash commands or file references
- **Fetch documentation** when creating tech-specific commands to get up-to-date API references
- **Use deep crawling** (depth 2-3) for comprehensive documentation sites with multiple related pages
- Use descriptive command names that indicate the action
- Add comprehensive descriptions for better discoverability
- Choose the right template for your use case
- Test bash commands before adding them
- Use project scope for team-shared commands
- Use global scope for personal commands across all projects
- Document your commands well for future reference
- **Combine Context7 + Crawl4AI** for maximum documentation coverage

## Best Practices

### Use Plan Mode for Complex Commands

When creating commands with multiple bash commands, file references, or advanced features:

1. Activate Plan Mode (Shift+Tab twice) before running this command
2. Review the generated command structure in read-only mode
3. Confirm the template selection is appropriate
4. Validate bash commands are safe and correct
5. Exit Plan Mode (Ctrl+D) to proceed with creation

**Why Plan Mode?**

- Prevents accidental command creation with errors
- Allows safe review of bash command syntax
- Validates file references before creation
- Ensures proper template selection

**Note:** Plan Mode cannot be forced programmatically. It's a user-controlled permission mode that provides read-only analysis before making changes.

## Related Commands

- `/cc-command-improve` - Improve an existing command
- `python -m src.tools.command_builder.main list` - List all commands
- `python -m src.tools.command_builder.main templates` - Show available templates
