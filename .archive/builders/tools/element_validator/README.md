# Element Validator

Validate and auto-fix Claude Code elements (agents, skills, commands, prompts) to ensure they have proper YAML frontmatter format.

## Features

- ✅ **Validates YAML frontmatter** for agents, skills, commands, and prompts
- 🔍 **Auto-detects element type** from file path or content
- 🔧 **Auto-fixes common errors** like missing fields and pattern mismatches
- 📊 **Batch validation** for entire directories
- 💡 **Helpful suggestions** for fixing validation errors
- ⚠️  **Warnings for best practices** (non-blocking)

## Usage

### Validate a Single File

```bash
# Auto-detect element type
python -m src.tools.element_validator.main path/to/agent.md

# Specify element type explicitly
python -m src.tools.element_validator.main path/to/file.md --type agent
```

### Validate a Directory

```bash
# Validate all elements in directory (non-recursive)
python -m src.tools.element_validator.main ~/.claude/agents

# Recursive validation
python -m src.tools.element_validator.main ~/.claude --recursive
```

### Auto-Fix Errors

```bash
# Fix single file
python -m src.tools.element_validator.main path/to/agent.md --fix

# Fix all files in directory
python -m src.tools.element_validator.main ~/.claude/agents --fix --recursive
```

### Options

- `--type`, `-t`: Specify element type (`agent`, `skill`, `command`, `prompt`)
- `--fix`, `-f`: Automatically fix validation errors where possible
- `--recursive`, `-r`: Recursively validate all elements in directory
- `--verbose`, `-v`: Show detailed validation information including frontmatter
- `--quiet`, `-q`: Only show files with errors

## Element Types

### Agent/Sub-Agent

**Required fields:**
- `name`: Lowercase letters and hyphens only (e.g., `my-agent`)
- `description`: Natural language description of agent's purpose

**Optional fields:**
- `tools`: Comma-separated list of tools (e.g., `Read, Write, Edit`)
- `model`: Model alias (`sonnet`, `opus`, `haiku`, `inherit`)

**Example:**
```markdown
---
name: my-agent
description: Does something useful
tools: Read, Write
model: sonnet
---

Agent instructions here...
```

### Skill

**Required fields:**
- `name`: Lowercase letters, numbers, and hyphens (max 64 chars)
- `description`: Brief description of what the skill does and when to use it (max 1024 chars)

**Optional fields:**
- `allowed-tools`: Comma-separated list of allowed tools

**Example:**
```markdown
---
name: my-skill
description: Does something specific when triggered
allowed-tools: Read, Grep, Glob
---

Skill instructions here...
```

### Command

**Required fields:** None (all fields are optional)

**Optional fields:**
- `description`: Brief description for `/help` output
- `allowed-tools`: Tools the command can use
- `argument-hint`: Arguments expected for the command
- `model`: Specific Claude model to use
- `disable-model-invocation`: Prevents auto-invocation

**Example:**
```markdown
---
description: Custom command that does X
argument-hint: <file> [options]
model: sonnet
---

Command content here...
Use $ARGUMENTS or $1, $2 for arguments
```

### Prompt

**Required fields:**
- `name`: Lowercase letters and hyphens only
- `description`: Brief description of the prompt's purpose (max 512 chars)

**Optional fields:**
- `variables`: Comma-separated list of variables

**Example:**
```markdown
---
name: my-prompt
description: Template for doing X
variables: project_name, author
---

Prompt template here...
Use {{project_name}} and {{author}} for variables
```

## Validation Rules

### YAML Frontmatter Structure

1. Must start with `---` on the first line
2. Must end with `---` before content
3. Must contain valid YAML dictionary
4. Must include all required fields for element type
5. Field values must match expected types and patterns

### Field Validation

- **Name fields**: Must match pattern `^[a-z0-9-]+$`
- **Description fields**: Cannot be empty, must respect max length
- **Model fields**: Must be one of `sonnet`, `opus`, `haiku`, or `inherit`
- **Tool lists**: Comma-separated string format

### Auto-Fix Capabilities

The validator can automatically fix:

1. **Missing required fields**: Adds placeholder values with TODO markers
2. **Invalid name patterns**: Converts to lowercase, replaces invalid chars with hyphens
3. **Duplicate hyphens**: Consolidates multiple hyphens into single hyphen
4. **Leading/trailing hyphens**: Removes from name fields

## Exit Codes

- `0`: All validations passed
- `1`: Validation errors found or path not found

## Integration with Other Tools

### Catalog System

Integrate with the catalog system to validate elements during manifest generation:

```python
from src.tools.element_validator import ElementValidator

validator = ElementValidator()
result = validator.validate_element(element_path)

if not result.is_valid:
    print(f"Skipping invalid element: {element_path}")
    for error in result.errors:
        print(f"  - {error.message}")
```

### Pre-commit Hook

Add validation as a pre-commit hook to ensure all elements are valid before committing:

```bash
#!/bin/bash
# .git/hooks/pre-commit

python -m src.tools.element_validator.main .claude --recursive --quiet
exit $?
```

## Examples

### Good Agent File

```markdown
---
name: architecture-designer
description: Sub-agent for designing component architecture, data models, and API contracts
tools: Read, Write, Edit
model: opus
---

## Role
The Architecture Designer is a specialized sub-agent...
```

### Bad Agent File (Missing Required Fields)

```markdown
# Transcript Analyzer Agent

## Role
You are a specialized agent...
```

**Validation Output:**
```
📄 transcript-analyzer-agent.md (agent)
   ❌ Invalid (2 errors)

   ❌ Errors:
      • [frontmatter] Missing opening frontmatter delimiter (---)
        💡 Add '---' at the start of the file
      • [name] Required field 'name' is missing
        💡 Add 'name: Unique identifier using lowercase letters and hyphens'
```

**After Auto-Fix:**
```markdown
---
name: transcript-analyzer-agent
description: TODO: Natural language description of the agent's purpose
---

# Transcript Analyzer Agent

## Role
You are a specialized agent...
```

## Development

### Running Tests

```bash
pytest tests/tools/test_element_validator.py
```

### Adding New Element Types

1. Define schema in `schemas.py`:
   ```python
   class NewElementSchema:
       REQUIRED_FIELDS = [...]
       OPTIONAL_FIELDS = [...]
   ```

2. Add to `SCHEMA_MAP`:
   ```python
   SCHEMA_MAP = {
       ElementType.NEW: NewElementSchema,
   }
   ```

3. Update `detect_element_type()` in `validator.py` to recognize the new type

## See Also

- [Catalog System](../catalog_system/README.md)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Sub-Agents Guide](https://docs.claude.com/en/docs/claude-code/sub-agents.md)
- [Skills Guide](https://docs.claude.com/en/docs/claude-code/skills.md)
