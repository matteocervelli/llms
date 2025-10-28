# Skill Builder Tool

**Generate Claude Code skills with an interactive wizard and comprehensive CLI**

The Skill Builder is a production-ready tool for creating, managing, and organizing Claude Code skills. It features an interactive questionary-based wizard, template system, JSON catalog management, and full CLI for both interactive and programmatic workflows.

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [CLI Reference](#cli-reference)
5. [Templates Guide](#templates-guide)
6. [Programmatic API](#programmatic-api)
7. [Security](#security)
8. [Performance](#performance)
9. [Troubleshooting](#troubleshooting)
10. [Examples](#examples)

---

## Overview

### Key Features

- **Interactive Wizard**: Beautiful CLI with questionary prompts and real-time validation
- **4 Skill Templates**: Progressive complexity (basic → with_tools → with_scripts → advanced)
- **Scope System**: Global (~/.claude/), Project (.claude/), Local (.claude/ uncommitted)
- **JSON Catalog**: Atomic writes, UUID tracking, search, filesystem sync
- **Security-by-Design**: Path traversal prevention, input validation, sandboxed Jinja2 rendering
- **High Performance**: < 50ms skill creation, < 100ms catalog operations
- **Comprehensive CLI**: 8 commands for complete skill lifecycle management

### What are Skills?

Skills in Claude Code are reusable capabilities defined in Markdown files with YAML frontmatter. They extend Claude's abilities with custom instructions, allowed tools, and optional scripts.

### Architecture

```
skill_builder/
├── models.py          # Pydantic data models (SkillConfig, CatalogEntry)
├── exceptions.py      # Custom exceptions
├── validator.py       # Security-first validation
├── templates.py       # Jinja2 template management
├── builder.py         # Core skill creation logic
├── catalog.py         # JSON catalog management
├── wizard.py          # Interactive CLI wizard
├── main.py            # Click CLI interface
└── templates/         # Built-in skill templates
    ├── basic.md
    ├── with_tools.md
    ├── with_scripts.md
    └── advanced.md
```

---

## Installation

### Prerequisites

- Python 3.9+
- Claude Code installed and configured
- Git (for project-level skills)

### Dependencies

The skill_builder requires the following Python packages:

```bash
# Core dependencies
pydantic>=2.0.0
click>=8.0.0
questionary>=2.0.0
jinja2>=3.1.0
pyyaml>=6.0.0

# These should already be installed with the llms project
```

### Setup

1. **Clone the repository** (if not already done):

```bash
cd ~/.claude
git clone https://github.com/matteocervelli/llms.git
cd llms
```

2. **Install dependencies with uv**:

```bash
uv pip install -r requirements.txt
```

3. **Verify installation**:

```bash
python -m src.tools.skill_builder.main --help
```

You should see the skill_builder CLI help output.

---

## Quick Start

### Create Your First Skill (Interactive)

The easiest way to create a skill is using the interactive wizard:

```bash
python -m src.tools.skill_builder.main create
```

This launches a beautiful CLI that guides you through:

1. **Skill name** - Validated in real-time (alphanumeric, hyphens, underscores)
2. **Description** - What the skill does
3. **Scope** - Global, Project, or Local
4. **Template** - Choose from 4 templates
5. **Allowed tools** - Multi-select from 18 Claude Code tools (if applicable)
6. **Additional files** - For advanced templates
7. **Preview** - Review configuration before creation
8. **Confirmation** - Create or cancel

### Create a Skill (Non-Interactive)

For scripting and automation, use the `generate` command:

```bash
python -m src.tools.skill_builder.main generate \
  --name "my-awesome-skill" \
  --description "Does something awesome" \
  --scope project \
  --template basic
```

### List Your Skills

```bash
python -m src.tools.skill_builder.main list
```

### View Catalog Statistics

```bash
python -m src.tools.skill_builder.main stats
```

---

## CLI Reference

The skill_builder provides 8 commands for complete skill lifecycle management.

### 1. `create` - Interactive Wizard

Launch the interactive wizard for guided skill creation.

**Usage:**

```bash
python -m src.tools.skill_builder.main create
```

**Features:**

- Real-time validation with helpful error messages
- Multi-select checkbox for allowed tools
- Preview configuration before creation
- Cancel at any step (Ctrl+C or decline confirmation)

**Example Output:**

```
? Skill name: data-analyzer
? Description: Analyzes data and generates insights
? Scope: Project
? Template: with_tools
? Select allowed tools: Read, Grep, Bash
✅ Skill created successfully at: /path/to/project/.claude/skills/data-analyzer/
```

---

### 2. `generate` - Non-Interactive Creation

Create a skill with command-line flags (for scripting/automation).

**Usage:**

```bash
python -m src.tools.skill_builder.main generate [OPTIONS]
```

**Options:**

- `--name TEXT` - Skill name (required, alphanumeric + hyphens/underscores)
- `--description TEXT` - Skill description (required)
- `--scope [global|project|local]` - Scope (default: auto-detect)
- `--template [basic|with_tools|with_scripts|advanced]` - Template (default: basic)
- `--allowed-tools TEXT` - Comma-separated list of allowed tools
- `--dry-run` - Validate without creating files

**Examples:**

```bash
# Basic skill
python -m src.tools.skill_builder.main generate \
  --name "quick-search" \
  --description "Quickly search codebase" \
  --template basic

# Skill with tools
python -m src.tools.skill_builder.main generate \
  --name "code-reviewer" \
  --description "Reviews code for best practices" \
  --scope project \
  --template with_tools \
  --allowed-tools "Read,Grep,Bash"

# Dry-run to validate
python -m src.tools.skill_builder.main generate \
  --name "test-skill" \
  --description "Test skill" \
  --dry-run
```

---

### 3. `list` - Display Skills

List skills with filtering and search capabilities.

**Usage:**

```bash
python -m src.tools.skill_builder.main list [OPTIONS]
```

**Options:**

- `--scope [global|project|local]` - Filter by scope
- `--template [basic|with_tools|with_scripts|advanced]` - Filter by template
- `--has-scripts / --no-scripts` - Filter by scripts presence
- `--search TEXT` - Search in name/description

**Examples:**

```bash
# List all skills
python -m src.tools.skill_builder.main list

# Filter by scope
python -m src.tools.skill_builder.main list --scope project

# Filter by template
python -m src.tools.skill_builder.main list --template with_tools

# Search for skills
python -m src.tools.skill_builder.main list --search "analyze"

# Combine filters
python -m src.tools.skill_builder.main list --scope project --has-scripts
```

**Example Output:**

```
📋 Skills Catalog

🔒 data-analyzer (Project)
   Template: with_tools | Tools: Read, Grep, Bash
   /path/to/project/.claude/skills/data-analyzer/

🌐 code-reviewer (Global)
   Template: with_scripts | Scripts: ✓
   ~/.claude/skills/code-reviewer/

Total: 2 skills
```

---

### 4. `delete` - Remove Skills

Delete a skill with confirmation prompt.

**Usage:**

```bash
python -m src.tools.skill_builder.main delete NAME [OPTIONS]
```

**Options:**

- `--scope [global|project|local]` - Scope (default: auto-detect)
- `--yes` - Skip confirmation prompt

**Examples:**

```bash
# Delete with confirmation
python -m src.tools.skill_builder.main delete my-skill

# Delete without confirmation
python -m src.tools.skill_builder.main delete my-skill --yes

# Delete from specific scope
python -m src.tools.skill_builder.main delete my-skill --scope global
```

**Safety Features:**

- Confirmation prompt by default
- Validates skill exists before deletion
- Updates catalog atomically
- Removes skill directory completely

---

### 5. `validate` - Check Skill Structure

Validate skill directory structure and SKILL.md format.

**Usage:**

```bash
python -m src.tools.skill_builder.main validate NAME [OPTIONS]
```

**Options:**

- `--scope [global|project|local]` - Scope (default: auto-detect)

**Examples:**

```bash
# Validate a skill
python -m src.tools.skill_builder.main validate my-skill

# Validate in specific scope
python -m src.tools.skill_builder.main validate my-skill --scope project
```

**What it checks:**

- Skill directory exists
- SKILL.md file present
- Valid YAML frontmatter
- Required fields present (name, description)
- Allowed tools valid (if specified)
- Scripts directory valid (if present)

**Example Output:**

```
✅ Skill 'my-skill' is valid
   Path: /path/to/skills/my-skill/
   Template: with_tools
   Tools: Read, Grep
```

---

### 6. `templates` - List Available Templates

Display all available skill templates with descriptions.

**Usage:**

```bash
python -m src.tools.skill_builder.main templates
```

**Example Output:**

```
📋 Available Skill Templates

1. basic
   Minimal skill with name, description, and content only

2. with_tools
   Skill with allowed-tools list for tool access

3. with_scripts
   Skill with scripts/ directory for executable scripts

4. advanced
   Full-featured skill with tools, scripts, and multiple files

Use --template <name> when creating skills
```

---

### 7. `stats` - Catalog Statistics

Show catalog statistics and breakdown by scope/template.

**Usage:**

```bash
python -m src.tools.skill_builder.main stats
```

**Example Output:**

```
📊 Skill Catalog Statistics

Total Skills: 12

By Scope:
  🌐 Global: 5
  🔒 Local: 3
  📁 Project: 4

By Template:
  basic: 4
  with_tools: 5
  with_scripts: 2
  advanced: 1

Skills with Scripts: 3
```

---

### 8. `sync` - Synchronize Catalog

Sync catalog with filesystem (detect untracked skills, remove orphaned entries).

**Usage:**

```bash
python -m src.tools.skill_builder.main sync
```

**What it does:**

1. **Scans filesystem** for skill directories with SKILL.md
2. **Adds untracked skills** to catalog (parses frontmatter)
3. **Removes orphaned entries** (skills in catalog but not on disk)
4. **Updates catalog** with atomic write

**Example Output:**

```
🔄 Syncing skill catalog with filesystem...

Added 2 untracked skills:
  ✅ new-skill-1 (project)
  ✅ new-skill-2 (global)

Removed 1 orphaned entry:
  ❌ deleted-skill (no longer on disk)

✅ Catalog synchronized successfully
```

**When to use:**

- After manually creating/deleting skill directories
- After git pull that added/removed skills
- To verify catalog integrity
- Periodic maintenance

---

## Templates Guide

The skill_builder includes 4 built-in templates with progressive complexity.

### 1. `basic` - Minimal Skill

**Use when:** You need a simple skill with just instructions.

**Structure:**

```
my-skill/
└── SKILL.md
```

**Frontmatter:**

```yaml
---
name: my-skill
description: Brief description
---
```

**Example:**

```bash
python -m src.tools.skill_builder.main generate \
  --name "greeter" \
  --description "Greets users warmly" \
  --template basic
```

---

### 2. `with_tools` - Skill with Allowed Tools

**Use when:** Your skill needs specific Claude Code tools.

**Structure:**

```
my-skill/
└── SKILL.md
```

**Frontmatter:**

```yaml
---
name: my-skill
description: Brief description
allowed-tools:
  - Read
  - Grep
  - Bash
---
```

**Allowed Tools (18 total):**

- `Read`, `Write`, `Edit`
- `Glob`, `Grep`
- `Bash`
- `Task`, `TodoWrite`
- `WebFetch`, `WebSearch`
- `AskUserQuestion`
- `Skill`, `SlashCommand`
- `NotebookEdit`
- And more...

**Example:**

```bash
python -m src.tools.skill_builder.main generate \
  --name "code-analyzer" \
  --description "Analyzes code structure" \
  --template with_tools \
  --allowed-tools "Read,Grep,Glob"
```

---

### 3. `with_scripts` - Skill with Scripts Directory

**Use when:** Your skill needs executable scripts or helper files.

**Structure:**

```
my-skill/
├── SKILL.md
└── scripts/
    ├── setup.sh
    ├── helper.py
    └── config.json
```

**Frontmatter:**

```yaml
---
name: my-skill
description: Brief description
allowed-tools:
  - Bash
---
```

**Scripts usage:**

- Bash scripts: `!./skills/my-skill/scripts/setup.sh`
- Python scripts: `!python ./skills/my-skill/scripts/helper.py`
- Config files: Reference in SKILL.md content

**Example:**

```bash
python -m src.tools.skill_builder.main create
# Then select "with_scripts" template in wizard
```

---

### 4. `advanced` - Full-Featured Skill

**Use when:** You need a complex skill with tools, scripts, and documentation.

**Structure:**

```
my-skill/
├── SKILL.md
├── README.md
├── config.yaml
└── scripts/
    ├── main.sh
    ├── utils.py
    └── tests/
        └── test_utils.py
```

**Frontmatter:**

```yaml
---
name: my-skill
description: Brief description
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
---
```

**Features:**

- Multiple files for organization
- Scripts with tests
- Configuration files
- Documentation (README.md)

**Example:**

```bash
python -m src.tools.skill_builder.main create
# Select "advanced" template and follow prompts
```

---

### Custom Templates

You can create custom templates by:

1. Creating a new `.md` file in `src/tools/skill_builder/templates/`
2. Using Jinja2 variables: `{{ name }}`, `{{ description }}`, `{{ allowed_tools }}`, `{{ content }}`
3. Referencing it by filename (without .md) in `--template` flag

**Example custom template:**

```markdown
---
name: {{ name }}
description: {{ description }}
author: Matteo Cervelli
version: 1.0.0
---

# {{ name }}

{{ content }}

## Custom Section

This is a custom template with additional metadata.
```

---

## Programmatic API

For advanced use cases, you can use the skill_builder classes directly in Python.

### SkillBuilder API

**Create a skill programmatically:**

```python
from src.tools.skill_builder.builder import SkillBuilder
from src.tools.skill_builder.models import SkillConfig
from src.core.scope_manager import ScopeManager

# Initialize
scope_manager = ScopeManager()
builder = SkillBuilder(scope_manager)

# Create skill config
config = SkillConfig(
    name="my-skill",
    description="My awesome skill",
    template="with_tools",
    allowed_tools=["Read", "Grep"],
    scope="project"
)

# Build skill
result = builder.build_skill(config)
print(f"Skill created at: {result.path}")
```

**Validate a skill:**

```python
# Validate skill structure
is_valid = builder.validate_skill_directory("my-skill", scope="project")
print(f"Valid: {is_valid}")
```

**Update a skill:**

```python
# Update existing skill
updated_config = SkillConfig(
    name="my-skill",
    description="Updated description",
    template="with_tools",
    allowed_tools=["Read", "Grep", "Bash"],
    scope="project"
)

result = builder.update_skill(updated_config)
print(f"Skill updated at: {result.path}")
```

**Delete a skill:**

```python
# Delete skill
builder.delete_skill("my-skill", scope="project")
```

---

### CatalogManager API

**Manage the skill catalog:**

```python
from src.tools.skill_builder.catalog import CatalogManager
from src.core.scope_manager import ScopeManager

# Initialize
scope_manager = ScopeManager()
catalog = CatalogManager(scope_manager)

# Add skill to catalog
from src.tools.skill_builder.models import SkillCatalogEntry

entry = SkillCatalogEntry(
    name="my-skill",
    description="My awesome skill",
    scope="project",
    path="/path/to/skill",
    template="with_tools",
    has_scripts=False
)

catalog.add_skill(entry)

# List all skills
skills = catalog.list_skills()
for skill in skills:
    print(f"{skill.name}: {skill.description}")

# Search skills
results = catalog.search_skills(
    query="analyzer",
    scope="project",
    has_scripts=True
)

# Get statistics
stats = catalog.get_catalog_stats()
print(f"Total skills: {stats['total']}")
print(f"By scope: {stats['by_scope']}")

# Sync with filesystem
catalog.sync_catalog()
```

---

### SkillWizard API

**Run the interactive wizard programmatically:**

```python
from src.tools.skill_builder.wizard import SkillWizard
from src.tools.skill_builder.builder import SkillBuilder
from src.core.scope_manager import ScopeManager

# Initialize
scope_manager = ScopeManager()
builder = SkillBuilder(scope_manager)
wizard = SkillWizard(builder)

# Run wizard
config = wizard.run()

if config:
    print(f"Skill '{config.name}' created successfully!")
else:
    print("Skill creation cancelled")
```

---

## Security

The skill_builder implements multiple security layers:

### 1. Path Traversal Prevention

**Protection against directory traversal attacks:**

```python
# BLOCKED: Attempts to access parent directories
skill_builder.build_skill(SkillConfig(
    name="../../etc/passwd",  # ❌ ValidationError
    description="Evil skill",
    template="basic"
))

# BLOCKED: Absolute paths
skill_builder.build_skill(SkillConfig(
    name="/tmp/evil-skill",   # ❌ ValidationError
    description="Evil skill",
    template="basic"
))
```

**Validation rules:**

- No `..` in skill names
- No absolute paths
- No path separators (/ or \)
- Alphanumeric + hyphens/underscores only

---

### 2. Input Validation

**All inputs validated with Pydantic:**

```python
# Skill name validation
name: str  # 1-50 chars, alphanumeric + hyphens/underscores

# Description validation
description: str  # 1-500 chars

# Allowed tools validation
allowed_tools: List[str]  # Whitelist of 18 valid Claude Code tools

# Template validation
template: Literal["basic", "with_tools", "with_scripts", "advanced"]

# Scope validation
scope: Literal["global", "project", "local"]
```

**Invalid inputs raise `ValidationError`:**

```python
from pydantic import ValidationError

try:
    config = SkillConfig(
        name="my_skill@#$",  # Invalid characters
        description="",       # Empty description
        template="invalid"    # Invalid template
    )
except ValidationError as e:
    print(e.errors())
```

---

### 3. Sandboxed Template Rendering

**Jinja2 templates rendered in sandboxed environment:**

```python
from jinja2.sandbox import SandboxedEnvironment

# Templates cannot execute arbitrary code
env = SandboxedEnvironment()

# Safe rendering
template = env.from_string("{{ name }}")
output = template.render(name="my-skill")  # ✅ Safe

# Blocked: Arbitrary code execution
template = env.from_string("{{ __import__('os').system('rm -rf /') }}")
output = template.render()  # ❌ SecurityError
```

**Template security:**

- No arbitrary Python code execution
- No file system access from templates
- No network access from templates
- Only safe variables passed to templates

---

### 4. Scope Boundary Enforcement

**Skills cannot access data outside their scope:**

```python
# Global skills: ~/.claude/skills/
# Project skills: /project/.claude/skills/
# Local skills: /project/.claude/skills/ (uncommitted)

# Skills can only access files in their scope
# Cross-scope access blocked by scope_manager
```

---

### 5. Catalog Integrity

**Atomic writes prevent corruption:**

```python
# Catalog updates use atomic write pattern:
# 1. Create backup (.bak)
# 2. Write to temp file (.tmp)
# 3. Atomic rename (temp → catalog.json)

# If any step fails, catalog remains intact
```

---

### Best Practices

1. **Never disable validation** - Always use validated models
2. **Review allowed-tools** - Only grant necessary tools
3. **Audit scripts** - Review scripts in with_scripts/advanced templates
4. **Use dry-run** - Test with `--dry-run` before creating
5. **Regular sync** - Run `sync` command to maintain catalog integrity
6. **Backup catalog** - The catalog is backed up automatically, but keep additional backups

---

## Performance

The skill_builder is optimized for high performance:

### Benchmarks

**Measured on Apple M1 Pro, Python 3.11:**

| Operation | Target | Actual | Status |
|-----------|--------|--------|--------|
| Skill creation | < 50ms | 5-15ms | ✅ 3-10x faster |
| Catalog add | < 100ms | 20-40ms | ✅ 2.5-5x faster |
| Catalog search | < 100ms | 10-30ms | ✅ 3-10x faster |
| Template rendering | < 10ms | 1-3ms | ✅ 3-10x faster |
| Validation | < 10ms | 1-2ms | ✅ 5-10x faster |
| Catalog sync | < 100ms | 30-60ms | ✅ 1.5-3x faster |

### Optimization Strategies

**1. Lazy Loading**

```python
# Templates loaded only when needed
template_manager.get_template("basic")  # Load on first use
```

**2. Atomic Operations**

```python
# Single catalog write per operation (no multiple writes)
catalog.add_skill(entry)  # One write
```

**3. Minimal File I/O**

```python
# Read catalog once, cache in memory
catalog.list_skills()  # Cached result
catalog.list_skills()  # No disk read
```

**4. Efficient Validation**

```python
# Pydantic validation in C (fast)
# Regex pre-compiled for repeated validation
```

**5. JSON Optimization**

```python
# Compact JSON (no indentation in production)
# Only pretty-print when debugging
```

### Performance Tips

1. **Batch operations** - Create multiple skills before syncing
2. **Use dry-run** - Validate without file I/O
3. **Filter early** - Use specific filters in `list` command
4. **Cache results** - CatalogManager caches loaded catalog

---

## Troubleshooting

### Common Issues

#### 1. "Skill name already exists"

**Error:**

```
SkillBuilderError: Skill 'my-skill' already exists in project scope
```

**Solution:**

- Choose a different name
- Delete the existing skill: `python -m src.tools.skill_builder.main delete my-skill`
- Use a different scope: `--scope global` or `--scope local`

---

#### 2. "Invalid skill name"

**Error:**

```
ValidationError: Skill name must be alphanumeric with hyphens/underscores
```

**Solution:**

- Use only letters, numbers, hyphens, and underscores
- No spaces, special characters, or path separators
- Valid: `my-skill`, `data_analyzer`, `skill123`
- Invalid: `my skill`, `my/skill`, `my@skill`

---

#### 3. "Template not found"

**Error:**

```
TemplateError: Template 'custom_template' not found
```

**Solution:**

- Check available templates: `python -m src.tools.skill_builder.main templates`
- Verify template file exists in `src/tools/skill_builder/templates/`
- Use one of: `basic`, `with_tools`, `with_scripts`, `advanced`

---

#### 4. "Catalog out of sync"

**Symptoms:**

- Skills listed but not found on disk
- Skills on disk but not in catalog

**Solution:**

```bash
python -m src.tools.skill_builder.main sync
```

This will:
- Add untracked skills to catalog
- Remove orphaned entries
- Fix inconsistencies

---

#### 5. "Permission denied"

**Error:**

```
PermissionError: [Errno 13] Permission denied: '/path/to/skill'
```

**Solution:**

- Check file permissions: `ls -la /path/to/.claude/skills/`
- Fix permissions: `chmod 755 /path/to/.claude/skills/`
- Verify you own the directory: `chown -R $USER /path/to/.claude/`

---

#### 6. "Scope detection failed"

**Error:**

```
ScopeError: Unable to detect scope, not in git repository
```

**Solution:**

- Initialize git: `git init`
- Or explicitly specify scope: `--scope global` or `--scope local`
- For project scope, ensure you're in a git repository

---

#### 7. "Catalog corrupted"

**Symptoms:**

- JSON decode errors
- Catalog operations fail

**Solution:**

```bash
# 1. Restore from backup
cp skills.json.bak skills.json

# 2. Or rebuild from filesystem
rm skills.json
python -m src.tools.skill_builder.main sync
```

The catalog backup (`.bak`) is created before each write.

---

#### 8. "Wizard crashes on input"

**Symptoms:**

- Ctrl+C doesn't work
- Terminal messed up

**Solution:**

```bash
# Reset terminal
reset

# Or
stty sane
```

The wizard uses questionary which handles Ctrl+C gracefully, but terminal issues can occur.

---

### Debug Mode

**Enable verbose logging:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run skill_builder operations
# Will print detailed debug information
```

---

### Getting Help

**If issues persist:**

1. Check the implementation docs: `docs/implementation/issue-8-skill-builder.md`
2. Review test cases: `tests/test_skill_builder.py`
3. Open an issue: https://github.com/matteocervelli/llms/issues
4. Check existing issues for similar problems

---

## Examples

### Example 1: Data Analysis Skill

**Create a skill for analyzing CSV data:**

```bash
python -m src.tools.skill_builder.main create
```

**Wizard inputs:**

- Name: `csv-analyzer`
- Description: `Analyzes CSV files and generates insights`
- Scope: `project`
- Template: `with_tools`
- Allowed tools: `Read`, `Bash`, `Write`

**Generated structure:**

```
.claude/skills/csv-analyzer/
└── SKILL.md
```

**SKILL.md content:**

```yaml
---
name: csv-analyzer
description: Analyzes CSV files and generates insights
allowed-tools:
  - Read
  - Bash
  - Write
---

# CSV Analyzer

This skill analyzes CSV files and generates insights.

## Instructions

When asked to analyze a CSV file:

1. Use Read tool to load the CSV file
2. Use Bash to run pandas/numpy analysis
3. Generate summary statistics
4. Write insights to a report file

## Example

User: "Analyze sales_data.csv"

Response:
- Read the CSV file
- Calculate totals, averages, trends
- Generate visualizations
- Write report.md with findings
```

---

### Example 2: Code Review Automation

**Create a skill for automated code reviews:**

```bash
python -m src.tools.skill_builder.main generate \
  --name "code-reviewer" \
  --description "Automated code review with best practices" \
  --scope project \
  --template with_scripts \
  --allowed-tools "Read,Grep,Bash"
```

**Then add scripts:**

```bash
cd .claude/skills/code-reviewer/scripts/

# Create review script
cat > review.sh << 'EOF'
#!/bin/bash
# Automated code review script

echo "Running code review..."

# Check for TODO/FIXME
grep -r "TODO\|FIXME" src/

# Check for console.log (JS)
grep -r "console.log" src/

# Check for print statements (Python)
grep -r "print(" src/

echo "Review complete!"
EOF

chmod +x review.sh
```

**Use in SKILL.md:**

```yaml
---
name: code-reviewer
description: Automated code review with best practices
allowed-tools:
  - Read
  - Grep
  - Bash
---

# Code Reviewer

Automated code review using static analysis and best practices.

## Review Process

When asked to review code:

1. Run review script: `!./skills/code-reviewer/scripts/review.sh`
2. Check for common issues (TODO, console.log, print)
3. Suggest improvements
4. Generate review report

## Best Practices Checked

- No TODO/FIXME in production code
- No debug statements (console.log, print)
- Proper error handling
- Type hints (Python) or types (TypeScript)
```

---

### Example 3: Documentation Generator

**Create an advanced skill with multiple files:**

```bash
python -m src.tools.skill_builder.main create
```

**Wizard inputs:**

- Name: `doc-generator`
- Description: `Generates comprehensive documentation from code`
- Scope: `global`
- Template: `advanced`
- Allowed tools: `Read`, `Write`, `Grep`, `Bash`
- Additional files: `README.md`, `config.yaml`

**Structure:**

```
~/.claude/skills/doc-generator/
├── SKILL.md
├── README.md
├── config.yaml
└── scripts/
    ├── generate.py
    └── templates/
        ├── api.md.j2
        └── guide.md.j2
```

**config.yaml:**

```yaml
# Documentation generator configuration
output_dir: docs/
templates_dir: skills/doc-generator/scripts/templates/
sections:
  - api
  - guides
  - tutorials
```

**scripts/generate.py:**

```python
#!/usr/bin/env python3
"""Documentation generator script."""

import yaml
import os
from jinja2 import Environment, FileSystemLoader

def load_config():
    with open('skills/doc-generator/config.yaml') as f:
        return yaml.safe_load(f)

def generate_docs(config):
    # Load templates
    env = Environment(
        loader=FileSystemLoader(config['templates_dir'])
    )

    # Generate each section
    for section in config['sections']:
        template = env.get_template(f'{section}.md.j2')
        output = template.render()

        # Write output
        output_path = os.path.join(config['output_dir'], f'{section}.md')
        with open(output_path, 'w') as f:
            f.write(output)

        print(f"Generated: {output_path}")

if __name__ == '__main__':
    config = load_config()
    generate_docs(config)
```

**Usage:**

```bash
# Run from project root
python -m src.tools.skill_builder.main validate doc-generator --scope global

# Use skill in Claude Code
# User: "Generate documentation for this project"
# Claude: !python ~/.claude/skills/doc-generator/scripts/generate.py
```

---

### Example 4: Testing Helper

**Create a skill for running tests with coverage:**

```bash
python -m src.tools.skill_builder.main generate \
  --name "test-runner" \
  --description "Runs tests with coverage and reports" \
  --scope project \
  --template with_tools \
  --allowed-tools "Bash,Read,Write"
```

**SKILL.md:**

```yaml
---
name: test-runner
description: Runs tests with coverage and reports
allowed-tools:
  - Bash
  - Read
  - Write
---

# Test Runner

Runs tests with coverage reporting and failure analysis.

## Commands

### Run all tests
!pytest tests/ -v --cov=src --cov-report=term-missing

### Run specific test file
!pytest tests/test_specific.py -v

### Run with coverage HTML report
!pytest tests/ --cov=src --cov-report=html

## Failure Analysis

When tests fail:
1. Read test output
2. Identify failing tests
3. Suggest fixes based on error messages
4. Re-run specific failing tests

## Coverage Goals

- Maintain 80%+ coverage
- Focus on critical paths
- Test edge cases and error handling
```

---

## Additional Resources

### Documentation

- **Implementation Docs**: `docs/implementation/issue-8-skill-builder.md`
- **Phase Docs**:
  - Phase 1: `docs/implementation/issue-8-skill-builder.md` (models, exceptions, validator)
  - Phase 2: `docs/implementation/issue-21-templates.md`
  - Phase 3: `docs/implementation/issue-22-builder.md`
  - Phase 4: `docs/implementation/issue-23-catalog.md`
  - Phase 5: `docs/implementation/issue-24-wizard.md`
  - Phase 6: `docs/implementation/issue-25-cli.md`

### Testing

- **Test Suite**: `tests/test_skill_builder.py`
- **Run Tests**: `pytest tests/test_skill_builder.py -v --cov`
- **Coverage**: 68% overall (41 tests, all passing)

### Source Code

- **Repository**: https://github.com/matteocervelli/llms
- **Issues**: https://github.com/matteocervelli/llms/issues
- **Skill Builder**: `src/tools/skill_builder/`

---

## License

MIT License - See LICENSE file in repository root.

---

## Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.

**Areas for contribution:**

- Additional templates
- Performance optimizations
- Security enhancements
- Documentation improvements
- Test coverage improvements

---

## Changelog

See CHANGELOG.md for version history and updates.

---

**Last Updated**: 2025-10-28
**Version**: 1.1.0
**Maintainer**: Matteo Cervelli
