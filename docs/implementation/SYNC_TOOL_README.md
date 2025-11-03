# Claude Configuration Sync & Audit Tool

A comprehensive Python tool for syncing and auditing Claude configuration files between project-specific `.claude/` folders and the global `~/.claude/` folder.

## Features

✅ **Audit Mode**: Compare configurations and show differences
✅ **Bidirectional Sync**: Push (project → global) or pull (global → project)
✅ **Interactive Conflict Resolution**: Show diffs and prompt for action
✅ **Settings Analysis**: Compare settings.json files and identify differences
✅ **Dry Run**: Preview sync operations without making changes
✅ **Automatic Backups**: Timestamped backups before overwriting
✅ **Colored Output**: Clear visual feedback with ANSI colors
✅ **Category Filtering**: Sync only specific categories (agents, commands, skills)

## Quick Start

### Installation

No additional dependencies required - uses Python standard library only.

```bash
# Make script executable
chmod +x sync_claude_configs.py
```

### Basic Usage

```bash
# Audit current state (show differences)
python sync_claude_configs.py
# or
make sync-check

# Detailed audit with file lists
python sync_claude_configs.py --audit --verbose
# or
make sync-audit

# Analyze settings.json differences
python sync_claude_configs.py --settings
# or
make sync-settings
```

### Sync Operations

```bash
# Sync project → global (with interactive conflict resolution)
python sync_claude_configs.py --sync
# or
make sync-push

# Sync global → project
python sync_claude_configs.py --sync --pull
# or
make sync-pull

# Preview sync without making changes
python sync_claude_configs.py --sync --dry-run
# or
make sync-dry
```

### Category-Specific Sync

```bash
# Sync only agents
python sync_claude_configs.py --sync --agents-only

# Sync only commands
python sync_claude_configs.py --sync --commands-only

# Sync only skills
python sync_claude_configs.py --sync --skills-only
```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make sync-check` | Quick audit (show sync status) |
| `make sync-audit` | Detailed audit with file lists |
| `make sync-push` | Sync project → global |
| `make sync-pull` | Sync global → project |
| `make sync-dry` | Preview sync operations |
| `make sync-settings` | Analyze settings.json |

## What Gets Synced

The tool syncs the following categories:

- **agents/** - Agent definition files (*.md)
- **commands/** - Slash command files (*.md)
- **skills/** - Skill directories (*/SKILL.md)
- **prompts/** - Prompt files (*.md) - asks for confirmation
- **hooks/** - Hook scripts (Python/Bash)

## Sync Behavior

### Default Direction
**Project → Global (push)** - Treats project as source of truth

### Conflict Resolution
When files exist in both locations with different content:
1. Shows file metadata (size, modification time)
2. Offers actions:
   - `[p]` Keep project version
   - `[g]` Keep global version
   - `[d]` Show full diff
   - `[s]` Skip this file
   - `[a]` Apply project to ALL remaining
   - `[A]` Apply global to ALL remaining

### Special Handling

**Prompts**: Always asks for confirmation before syncing (they're often project-specific)

**Backups**: Automatically creates timestamped backups in `.claude/.backups/YYYY-MM-DD-HHMMSS/` before overwriting

**Validation**: Verifies copied files using SHA256 hash comparison

## Example Output

### Audit Mode
```
============================================================
Audit Mode: Comparing Configurations
============================================================

============================================================
Audit Summary
============================================================

  Total files checked: 79
✅   ✅ In sync: 68
📤   📤 Project-only: 7
      - agents/doc-generator-agent.md
      - agents/transcript-analyzer-agent.md
      - commands/product-assess.md
      - skills/answer-collector/SKILL.md
      - skills/planning-doc-generator/SKILL.md
      - prompts/feature-implementer-main.md
      - prompts/product-assessor.md
📥   📥 Global-only: 4
      - commands/catalog-search.md
      - commands/catalog-show.md
      - commands/catalog-stats.md
      - skills/test/SKILL.md

⚠️  ⚠️  Configuration differences detected.

  Run sync commands:
    make sync-push      # Sync project → global
    make sync-pull      # Sync global → project
    make sync-dry       # Preview changes
```

### Settings Analysis
```
============================================================
Settings Analysis
============================================================

  📋 Hooks Differences:
    - Hook path mismatch: project uses ~/.claude/hooks/pre-commit.py
                         global uses "$CLAUDE_PROJECT_DIR"/.claude/hooks/pre-commit.py

  🔐 Permission Differences:
    - Global has 30 unique allow permissions

  🔌 Plugin Differences:
    - Plugin 'example-skills@anthropic-agent-skills' enabled in global but disabled in project

  💡 Recommendations:
ℹ️      - Standardize PreToolUse hooks - consider consolidating to one location
ℹ️      - Global has 30 unique allow permissions - ensure project has required permissions
ℹ️      - Plugin discrepancies detected - ensure this is intentional
```

## Architecture

### Module Structure
```
claude_sync/
├── __init__.py              # Package exports
├── file_handler.py          # File operations, backups
├── audit.py                 # Directory scanning, comparison
├── reporter.py              # Colored console output
├── sync.py                  # Sync orchestration
├── conflict_resolver.py     # Interactive conflict resolution
└── settings_analyzer.py     # Settings.json comparison
```

### Key Classes

- **FileHandler**: Safe file operations with backups and validation
- **AuditManager**: Scans and compares configurations
- **Reporter**: Colored terminal output with emojis
- **SyncManager**: Orchestrates sync operations
- **ConflictResolver**: Interactive conflict resolution with diff display
- **SettingsAnalyzer**: Compares settings.json files

## Safety Features

✅ **Automatic Backups**: Before overwriting any file
✅ **Hash Validation**: Verify copied files match source
✅ **Dry Run Mode**: Preview changes safely
✅ **Exclusion Patterns**: Skip `.DS_Store`, `__pycache__`, etc.
✅ **Error Handling**: Graceful handling of missing files, permissions
✅ **Operation Logging**: Track all operations for audit trail

## Testing

Comprehensive test suite included:

```bash
# Run all tests
pytest tests/ -v

# Specific module tests
pytest tests/test_file_handler.py -v
pytest tests/test_audit.py -v
pytest tests/test_sync.py -v
pytest tests/test_conflict_resolver.py -v
pytest tests/test_settings_analyzer.py -v
```

## Development

### Code Standards
- **500-line limit** per module
- **Type hints** throughout
- **Google-style** docstrings
- **Single responsibility** principle

### Adding New Features
1. Update relevant module in `claude_sync/`
2. Add tests in `tests/`
3. Update this README
4. Run test suite

## Troubleshooting

**Error: "Project .claude directory not found"**
- Run from project root containing `.claude/` folder
- Or use `--project-dir` flag to specify location

**Error: "Global .claude directory not found"**
- Verify `~/.claude/` exists
- Or use `--global-dir` flag to specify location

**Sync not showing expected files**
- Run with `--verbose` to see all files
- Check file names match expected patterns (*.md for agents/commands)
- For skills, ensure SKILL.md exists in subdirectory

**Settings analysis shows no differences but I know there are**
- Ensure settings.json files exist in both locations
- Check JSON is valid (use `python -m json.tool < settings.json`)
- Run with `--verbose` for detailed output

## License

Part of the LLM Configuration Management System project.

## Author

Matteo Cervelli - Business Transformation & Scalability Engineer
