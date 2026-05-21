# Agent Builder

**Create and manage Claude Code agents with ease.**

Agent Builder is a comprehensive tool for generating, managing, and validating Claude Code agent markdown files. It provides an interactive wizard, CLI commands, and programmatic API for agent lifecycle management.

## Features

- **Interactive Wizard**: User-friendly prompts with validation and real-time feedback
- **CLI Commands**: 8 commands for complete agent management
- **Model Selection**: Choose between Haiku, Sonnet, or Opus for each agent
- **Scope Management**: Install agents globally, per-project, or locally
- **Catalog System**: Track agents with searchable metadata
- **Template Support**: Pre-built templates for rapid agent creation
- **Validation**: Built-in validation for agent files and configurations
- **Sync System**: Automatic synchronization with filesystem

## Quick Start

### Interactive Creation (Recommended)

```bash
python -m src.tools.agent_builder.main create
```

This launches an interactive wizard that guides you through:
1. Agent name (e.g., `plan-agent`)
2. Description with usage context
3. Scope selection (global/project/local)
4. Claude model selection (Haiku/Sonnet/Opus)
5. Template selection
6. Preview and confirmation

### Non-Interactive Creation

```bash
python -m src.tools.agent_builder.main generate \
  --name plan-agent \
  --description "Strategic planning agent. Use when defining architecture." \
  --scope project \
  --model sonnet \
  --template basic
```

## CLI Commands

### 1. `create` - Interactive Wizard

Launch the interactive agent creation wizard.

```bash
python -m src.tools.agent_builder.main create [--project-root PATH]
```

**Options:**
- `--project-root`: Specify project directory (default: current directory)

**Example:**
```bash
python -m src.tools.agent_builder.main create
```

---

### 2. `generate` - Non-Interactive Creation

Create an agent using command-line options.

```bash
python -m src.tools.agent_builder.main generate \
  --name AGENT_NAME \
  --description DESCRIPTION \
  [--scope {global|project|local}] \
  [--model {haiku|sonnet|opus}] \
  [--template {basic|advanced}] \
  [--dry-run] \
  [--project-root PATH]
```

**Required Options:**
- `--name`: Agent name (lowercase-with-hyphens)
- `--description`: Agent description with usage context

**Optional Options:**
- `--scope`: Installation scope (default: `project`)
- `--model`: Claude model (default: `sonnet`)
- `--template`: Template to use (default: `basic`)
- `--dry-run`: Preview without creating files
- `--project-root`: Project directory

**Example:**
```bash
python -m src.tools.agent_builder.main generate \
  --name feature-implementer \
  --description "Implements features with TDD. Use when building new features." \
  --scope project \
  --model opus \
  --template advanced
```

---

### 3. `list` - List Agents

List all agents with optional filtering.

```bash
python -m src.tools.agent_builder.main list \
  [--scope {all|global|project|local}] \
  [--search QUERY] \
  [--template TEMPLATE] \
  [--model {haiku|sonnet|opus}] \
  [--project-root PATH]
```

**Options:**
- `--scope`: Filter by scope (default: `all`)
- `--search`: Search in name and description
- `--template`: Filter by template name
- `--model`: Filter by Claude model
- `--project-root`: Project directory

**Examples:**
```bash
# List all agents
python -m src.tools.agent_builder.main list

# List only project-scoped agents
python -m src.tools.agent_builder.main list --scope project

# Search for "planning" agents
python -m src.tools.agent_builder.main list --search planning

# List agents using Opus model
python -m src.tools.agent_builder.main list --model opus
```

---

### 4. `delete` - Delete Agent

Delete an agent by name.

```bash
python -m src.tools.agent_builder.main delete AGENT_NAME \
  [--scope {global|project|local}] \
  [--yes] \
  [--project-root PATH]
```

**Arguments:**
- `AGENT_NAME`: Name of agent to delete

**Options:**
- `--scope`: Scope to search in (optional)
- `--yes`: Skip confirmation prompt
- `--project-root`: Project directory

**Examples:**
```bash
# Delete with confirmation
python -m src.tools.agent_builder.main delete plan-agent

# Delete from specific scope without confirmation
python -m src.tools.agent_builder.main delete plan-agent --scope project --yes
```

---

### 5. `search` - Search Agents

Search agents by query string.

```bash
python -m src.tools.agent_builder.main search QUERY [--project-root PATH]
```

**Arguments:**
- `QUERY`: Search query (matches name and description)

**Options:**
- `--project-root`: Project directory

**Examples:**
```bash
# Search for "planning" agents
python -m src.tools.agent_builder.main search planning

# Search for "code review" agents
python -m src.tools.agent_builder.main search "code review"
```

---

### 6. `stats` - Catalog Statistics

Display catalog statistics.

```bash
python -m src.tools.agent_builder.main stats [--project-root PATH]
```

**Options:**
- `--project-root`: Project directory

**Example:**
```bash
python -m src.tools.agent_builder.main stats
```

**Output:**
```
📊 Agent Catalog Statistics
============================================================

  Total agents: 12

  By scope:
    🌐 Global:  3
    📦 Project: 7
    💻 Local:   2

  By model:
    ⚡ Haiku: 2
    🎯 Sonnet: 8
    🧠 Opus: 2

  By template:
    basic: 10
    advanced: 2
```

---

### 7. `sync` - Sync Catalog

Synchronize catalog with filesystem (add missing agents, remove orphaned entries).

```bash
python -m src.tools.agent_builder.main sync [--project-root PATH]
```

**Options:**
- `--project-root`: Project directory

**Example:**
```bash
python -m src.tools.agent_builder.main sync
```

**Output:**
```
🔄 Syncing catalog with filesystem...

📋 Sync Report:
============================================================

✅ Added 2 agent(s):
  + new-agent
  + another-agent

🗑️  Removed 1 orphaned agent(s):
  - deleted-agent
```

---

### 8. `validate` - Validate Agent File

Validate an agent markdown file.

```bash
python -m src.tools.agent_builder.main validate AGENT_PATH
```

**Arguments:**
- `AGENT_PATH`: Path to agent .md file

**Example:**
```bash
python -m src.tools.agent_builder.main validate ~/.claude/agents/plan-agent.md
```

**Output:**
```
✅ Agent file 'plan-agent.md' is valid!

  Name:        plan-agent
  Description: Strategic planning. Use when defining architecture.
  Model:       claude-3-5-sonnet-20241022
  Template:    basic

💡 Agent is ready to use in Claude Code
```

---

## Agent File Structure

Agents are single markdown files with YAML frontmatter:

```markdown
---
name: plan-agent
description: Strategic planning agent. Use when defining architecture.
model: claude-3-5-sonnet-20241022
template: basic
---

# Plan Agent

Strategic planning agent. Use when defining project architecture.

## When to Use

Use this agent when you need specialized assistance for planning tasks.

## Approach

1. Analyze the requirements
2. Plan the solution
3. Execute with precision
4. Verify results
```

### Required Frontmatter Fields

- `name`: Agent name (lowercase-with-hyphens, 1-64 chars)
- `description`: Agent description with usage context (max 1024 chars)
- `model`: Claude model identifier

### Optional Frontmatter Fields

- `template`: Template used (for tracking)
- Custom fields as needed

---

## Scope Types

### Global Scope (`~/.claude/agents/`)

- Available in **all projects**
- Ideal for general-purpose agents
- Shared across your development environment

**Use when:** Agent is useful across multiple projects

### Project Scope (`<project>/.claude/agents/`, committed)

- Available in **specific project**
- Committed to version control
- Shared with team members

**Use when:** Agent is project-specific and team-shared

### Local Scope (`<project>/.claude/agents/`, not committed)

- Available **locally only**
- Not committed to version control
- Personal customizations

**Use when:** Agent is for personal use in a project

---

## Claude Model Types

### Haiku (claude-3-5-haiku-20241022)

- **Speed**: Fastest
- **Cost**: Most economical
- **Use for**: Simple, routine tasks

### Sonnet (claude-3-5-sonnet-20241022) - Recommended

- **Speed**: Balanced
- **Cost**: Moderate
- **Use for**: Most tasks (default choice)

### Opus (claude-opus-4-20250514)

- **Speed**: Slowest
- **Cost**: Highest
- **Use for**: Complex reasoning, critical tasks

---

## Programmatic Usage

### Create Agent

```python
from pathlib import Path
from src.tools.agent_builder.builder import AgentBuilder
from src.tools.agent_builder.models import AgentConfig, ScopeType, ModelType

# Create configuration
config = AgentConfig(
    name="plan-agent",
    description="Strategic planning. Use when defining architecture.",
    scope=ScopeType.PROJECT,
    model=ModelType.SONNET,
    template="basic"
)

# Create agent
builder = AgentBuilder(base_dir=Path(".claude/agents"))
entry = builder.create_agent(config)

print(f"Agent created: {entry.path}")
```

### Catalog Management

```python
from src.tools.agent_builder.catalog import CatalogManager
from src.tools.agent_builder.models import ScopeType

# Initialize catalog
catalog = CatalogManager()

# List agents
agents = catalog.list_agents(scope=ScopeType.PROJECT)
for agent in agents:
    print(f"{agent.name}: {agent.description}")

# Search agents
results = catalog.search_agents(query="planning")
print(f"Found {len(results)} agents")

# Get statistics
stats = catalog.get_catalog_stats()
print(f"Total agents: {stats['total']}")
```

### Interactive Wizard

```python
from src.tools.agent_builder.wizard import AgentWizard

# Run wizard
wizard = AgentWizard()
config = wizard.run()

if config:
    path = wizard.create_agent_from_config(config)
    print(f"Agent created: {path}")
```

---

## Validation Rules

### Agent Name

- Pattern: `^[a-z0-9-]{1,64}$`
- Lowercase letters, numbers, hyphens only
- 1-64 characters
- Cannot start/end with hyphen
- No consecutive hyphens
- No path separators

**Valid:**
- `plan-agent`
- `code-reviewer`
- `feature-implementer`

**Invalid:**
- `Plan-Agent` (uppercase)
- `-plan-agent` (starts with hyphen)
- `plan--agent` (consecutive hyphens)
- `plan/agent` (path separator)

### Description

- Max 1024 characters
- Must include usage context keywords: "when", "use", "for", "during", "if"
- Cannot be empty

**Valid:**
- "Strategic planning. Use when defining architecture."
- "Code review automation for pull requests."

**Invalid:**
- "A planning agent." (no usage context)
- "" (empty)

### Model

- Must be one of the whitelisted Claude models:
  - `claude-3-5-haiku-20241022`
  - `claude-3-5-sonnet-20241022`
  - `claude-opus-4-20250514`

---

## Best Practices

### 1. Clear Agent Names

Use descriptive, hyphenated names:
```
✅ feature-implementer
✅ code-reviewer
✅ plan-agent

❌ fi
❌ CodeReviewer
❌ agent_1
```

### 2. Include Usage Context

Always describe **when** to use the agent:
```
✅ "Strategic planning. Use when defining architecture."
✅ "Code review automation. Use during pull request reviews."

❌ "A planning agent."
❌ "Helps with code."
```

### 3. Choose Appropriate Model

- **Haiku**: Simple, routine tasks
- **Sonnet**: Most tasks (default)
- **Opus**: Complex reasoning, critical tasks

### 4. Select Correct Scope

- **Global**: General-purpose, multi-project agents
- **Project**: Project-specific, team-shared agents
- **Local**: Personal customizations, not committed

### 5. Use Templates

Templates provide consistent structure:
- `basic`: Standard agent (recommended for most cases)
- `advanced`: Advanced features for complex agents

### 6. Validate Before Commit

Always validate agent files before committing:
```bash
python -m src.tools.agent_builder.main validate agent-file.md
```

### 7. Sync Regularly

Keep catalog in sync with filesystem:
```bash
python -m src.tools.agent_builder.main sync
```

---

## Troubleshooting

### Agent Not Found

**Problem:** Agent appears in filesystem but not in catalog

**Solution:** Run sync command
```bash
python -m src.tools.agent_builder.main sync
```

### Validation Errors

**Problem:** Agent file fails validation

**Solution:** Check frontmatter format and required fields
```bash
python -m src.tools.agent_builder.main validate agent-file.md
```

### Duplicate Agent

**Problem:** "Agent already exists" error

**Solution:** Delete existing agent first or choose different name
```bash
python -m src.tools.agent_builder.main delete old-agent
```

### Catalog Corrupted

**Problem:** Catalog file is corrupted or invalid JSON

**Solution:** Delete `agents.json` and resync
```bash
rm agents.json
python -m src.tools.agent_builder.main sync
```

---

## Architecture

### Components

1. **Models** (`models.py`): Pydantic models for agent configuration and catalog
2. **Builder** (`builder.py`): Agent creation and file management
3. **Catalog** (`catalog.py`): Catalog management with atomic writes
4. **Validator** (`validator.py`): Security-first validation
5. **Wizard** (`wizard.py`): Interactive creation experience
6. **Templates** (`templates.py`): Template management (placeholder)
7. **CLI** (`main.py`): Command-line interface

### Security Features

- **Path Traversal Prevention**: All paths validated before use
- **Input Sanitization**: All user inputs sanitized
- **Model Whitelist**: Only approved Claude models allowed
- **Secure File Permissions**: Files created with 644 permissions
- **Atomic Writes**: Catalog updates use atomic operations

### Performance Targets

- All catalog operations: < 100ms
- Agent creation: < 30ms
- File I/O optimized for minimal disk access

---

## Contributing

See main project [CONTRIBUTING.md](../../CONTRIBUTING.md) for development guidelines.

### Running Tests

```bash
# Run all agent_builder tests
pytest tests/agent_builder/ -v

# Run specific test file
pytest tests/agent_builder/test_catalog_manager.py -v

# Run with coverage
pytest tests/agent_builder/ --cov=src.tools.agent_builder --cov-report=html
```

---

## License

Part of the LLM Configuration Management System.

---

## Support

For issues, questions, or contributions, see the main project repository:
- GitHub: https://github.com/matteocervelli/llms
- Issues: https://github.com/matteocervelli/llms/issues
