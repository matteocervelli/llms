# Catalog System

Unified catalog manifest system for tracking skills, commands, and agents.

## Features

- **Auto-Discovery**: Automatically scan filesystem for installed elements
- **Search & Filter**: Find elements by name, description, tags, or scope
- **Multi-Scope**: Support for global, project, and local scopes
- **Auto-Sync**: Catalogs auto-sync with filesystem (cached for performance)
- **CLI Interface**: User-friendly commands (`llm list`, `llm search`, `llm show`)

## Architecture

### Components

1. **CatalogManager** - Main facade coordinating all operations
2. **Scanner** - Auto-discovers elements by walking filesystem
3. **Searcher** - Provides search/filter with scoring algorithm
4. **Syncer** - Synchronizes catalogs with filesystem

### Data Models

- `SkillCatalogEntry` - Tracks skills (template, has_scripts, file_count)
- `CommandCatalogEntry` - Tracks commands (aliases, requires_tools, tags)
- `AgentCatalogEntry` - Tracks agents (model, specialization, requires_skills)

## Usage

### Python API

```python
from catalog_system import CatalogManager

manager = CatalogManager()

# List all skills
skills = manager.list("skills")

# Search across all catalogs
results = manager.search("test", element_type="skills")

# Show specific element
entry = manager.show("skills", "example-skill")

# Force sync
manager.sync("skills")
```

### CLI Commands

```bash
# List all skills
llm list skills

# List all commands
llm list commands

# List all agents
llm list agents

# Search for elements
llm search "authentication"

# Show specific element
llm show skills example-skill
```

## Implementation Details

### File Structure

```
src/tools/catalog_system/
├── __init__.py          # Package exports
├── exceptions.py        # Custom exceptions
├── models.py            # Pydantic data models
├── scanner.py           # Filesystem scanner
├── searcher.py          # Search and filter
├── syncer.py            # Catalog synchronization
├── catalog_manager.py   # Main facade
└── cli.py               # Click CLI interface
```

### Catalog Files

Catalogs are stored as JSON files in `manifests/`:

- `manifests/skills.json`
- `manifests/commands.json`
- `manifests/agents.json`

### Auto-Discovery

The scanner walks the following directories:

- Skills: `.claude/skills/`
- Commands: `.claude/commands/`
- Agents: `.claude/agents/`

It parses YAML frontmatter from Markdown files to extract metadata.

### Caching

Auto-sync is cached for 60 seconds to minimize filesystem overhead. The cache is invalidated when:

- 60 seconds have elapsed since last sync
- Catalog file is modified
- Manual sync is requested

### Security

- Path validation prevents directory traversal attacks
- Input sanitization prevents injection in search queries
- Atomic writes prevent catalog corruption
- File permissions checked before read/write

## Testing

Run tests with pytest:

```bash
pytest tests/test_catalog_system/ -v
pytest tests/test_catalog_system/ --cov=src/tools/catalog_system --cov-report=term-missing
```

## Dependencies

- **python-frontmatter** - YAML frontmatter parsing
- **tabulate** - CLI table formatting
- **Pydantic** - Data validation
- **Click** - CLI framework

## See Also

- [Product Requirements Prompt](../../../docs/implementation/prp/feature-12-prp.md)
- [Architecture Design](../../../docs/implementation/design/architecture-feature-12.md)
- [GitHub Issue #12](https://github.com/matteocervelli/llms/issues/12)
