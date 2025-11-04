# Element Validation & Catalog Management

This document describes the validation and catalog management workflow for Claude Code elements (agents, skills, commands).

## Quick Start

### Complete Validation Workflow

Run the complete workflow to validate, fix, and update the catalog:

```bash
make validate-and-sync
```

This runs three steps automatically:
1. **Validate** all elements (project + global)
2. **Auto-fix** validation errors
3. **Regenerate** catalog manifests

## Individual Commands

### 1. Validate YAML Frontmatter

Check all elements for valid YAML frontmatter without making changes:

```bash
make validate
```

**What it checks:**
- Required fields (name, description)
- Field types (string vs list)
- Name patterns (lowercase, hyphens only)
- Max lengths
- YAML syntax

**Output:**
- ✅ Valid files (quiet mode only shows errors)
- ❌ Invalid files with error details
- Summary statistics

### 2. Auto-Fix Validation Errors

Automatically fix common validation issues:

```bash
make validate-fix
```

**What it fixes:**
- Missing frontmatter delimiters (`---`)
- List-to-string conversions (`allowed-tools`)
- Invalid name patterns
- Missing required fields (adds placeholders)

**Important:** Review changes before committing!

### 3. Update Catalog Manifests

Regenerate catalog manifests from validated elements:

```bash
make catalog-sync
```

**What it does:**
- Scans `.claude/` directories (project + global)
- Validates all elements (skips invalid)
- Generates JSON manifests in `manifests/`
- Shows catalog statistics

**Output files:**
- `manifests/agents.json`
- `manifests/skills.json`
- `manifests/commands.json`

## Sync to Global

Copy project `.claude/` files to global `~/.claude/`:

```bash
make sync-global          # One-time copy
make watch-sync           # Auto-sync on changes (development)
```

Use `sync-push` for intelligent syncing with conflict resolution:

```bash
make sync-push            # Interactive sync project → global
make sync-pull            # Interactive sync global → project
make sync-dry             # Preview without changes
make sync-audit           # Check differences
```

## Element Validation Rules

### Agents/Sub-Agents

**Required:**
- `name`: lowercase, hyphens (e.g., `my-agent`)
- `description`: natural language description

**Optional:**
- `tools`: comma-separated string (e.g., `Read, Write, Edit`)
- `model`: `sonnet`, `opus`, `haiku`, or `inherit`

**Example:**
```yaml
---
name: architecture-designer
description: Designs component architecture and data models
tools: Read, Write, Edit
model: opus
---
```

### Skills

**Required:**
- `name`: lowercase, hyphens, max 64 chars
- `description`: max 1024 chars

**Optional:**
- `allowed-tools`: comma-separated string

**Example:**
```yaml
---
name: analysis
description: Analyze feature requirements and dependencies
allowed-tools: Read, Grep, Glob, Bash
---
```

### Commands

**Required:** None (all optional)

**Optional:**
- `description`: brief description for `/help`
- `allowed-tools`: comma-separated string
- `argument-hint`: expected arguments
- `model`: `sonnet`, `opus`, `haiku`
- `disable-model-invocation`: boolean

**Example:**
```yaml
---
description: Create a new Claude Code command
argument-hint: [name] [description]
allowed-tools: Read, Write, Bash
model: sonnet
---
```

## Common Validation Errors

### 1. Missing Frontmatter

**Error:**
```
Missing opening frontmatter delimiter (---)
```

**Fix:**
```bash
make validate-fix
```

Adds frontmatter with default values.

### 2. List Instead of String

**Error:**
```
[allowed-tools] Expected str, got list
```

**Cause:**
```yaml
allowed-tools:
  - Read
  - Write
```

**Fix:**
Converts to:
```yaml
allowed-tools: Read, Write
```

### 3. Invalid Name Pattern

**Error:**
```
[name] Does not match required pattern: ^[a-z0-9-]+$
```

**Fix:**
Converts `My_Agent` → `my-agent`

## Integration with Catalog System

The catalog system automatically validates elements during scanning:

```python
from src.tools.catalog_system import Scanner

# Validation enabled by default
scanner = Scanner(validate=True, skip_invalid=True)
skills = scanner.scan_skills([path])
```

**Options:**
- `validate=True`: Enable validation (default)
- `skip_invalid=True`: Skip invalid elements with warnings (default)
- `skip_invalid=False`: Fail on invalid elements (strict mode)

## Manual Validation

For fine-grained control, use the validator directly:

```bash
# Single file
python -m src.tools.element_validator.main .claude/agents/my-agent.md

# Directory (non-recursive)
python -m src.tools.element_validator.main .claude/skills

# Recursive with auto-fix
python -m src.tools.element_validator.main .claude --fix --recursive

# Verbose mode
python -m src.tools.element_validator.main .claude/agents/my-agent.md --verbose

# Quiet mode (only errors)
python -m src.tools.element_validator.main .claude --quiet
```

## Workflow Best Practices

### Before Committing

Always validate and update catalog before committing:

```bash
make validate-and-sync
git add .
git commit -m "feat: update elements and catalog"
```

### After Creating New Elements

1. Create your element file
2. Validate: `make validate`
3. Fix errors: `make validate-fix`
4. Update catalog: `make catalog-sync`
5. Sync to global: `make sync-push`

### During Development

Use watch mode for auto-syncing:

```bash
make watch-sync
# Edit files in .claude/
# Changes automatically sync to ~/.claude/
```

## Troubleshooting

### Validation Fails with YAML Error

Check your YAML syntax:
- Proper indentation (spaces, not tabs)
- Quoted strings with special characters
- Proper list/string format

### Catalog Missing Elements

1. Check validation: `make validate`
2. Fix errors: `make validate-fix`
3. Regenerate: `make catalog-sync`

### Elements Not Syncing to Global

```bash
# Check what would be copied
make sync-dry

# Audit differences
make sync-audit

# Force sync
make sync-push
```

## See Also

- [Element Validator Documentation](../src/tools/element_validator/README.md)
- [Catalog System Documentation](../src/tools/catalog_system/README.md)
- [Sync Configuration Tool](../sync_claude_configs.py)
