# SyncManager Quick Start Guide

## Installation & Import

```python
from pathlib import Path
from claude_sync import SyncManager, SyncResult

# Initialize the sync manager
project_dir = Path(".claude")
global_dir = Path.home() / ".claude"

manager = SyncManager(project_dir, global_dir)
```

## Basic Operations

### Push Project Configs to Global

Push all your project configurations to the global location:

```python
result = manager.sync("push")

if result.success:
    print(f"✓ Synced {result.summary['copied']} files")
else:
    print(f"✗ Errors: {result.errors}")
```

### Pull Global Configs to Project

Sync global configs into your project:

```python
result = manager.sync("pull")

print(f"Copied: {result.summary['copied']}")
print(f"Skipped: {result.summary['skipped']} (identical)")
```

### Sync Specific Categories

Only sync certain configuration types:

```python
# Sync agents and commands only
result = manager.sync("push", categories=["agents", "commands"])

# Sync skills (directories)
result = manager.sync("push", categories=["skills"])
```

## Advanced Options

### Dry-Run Mode (Preview Only)

See what would be synced without making changes:

```python
manager = SyncManager(project_dir, global_dir, dry_run=True)
result = manager.sync("push")

print(f"Would copy: {len(result.files_copied)} files")
print(f"Would skip: {len(result.files_skipped)} files")
# No files actually copied in dry-run mode
```

### Force Mode (Auto-Overwrite)

Automatically overwrite conflicting files:

```python
manager = SyncManager(project_dir, global_dir, force=True)
result = manager.sync("push")

# Conflicts are resolved by overwriting destination with source
for file, action in result.conflicts_resolved.items():
    print(f"Resolved {file}: {action}")
```

### Verbose Output

Get detailed diagnostic information:

```python
from claude_sync import Reporter

reporter = Reporter(verbose=True)
manager = SyncManager(
    project_dir,
    global_dir,
    reporter=reporter
)
result = manager.sync("push")
# Shows detailed debug output during sync
```

## Understanding Results

```python
result = manager.sync("push")

# Check overall success
if result.success:
    print("Sync completed successfully")
else:
    print(f"Sync had {len(result.errors)} error(s)")

# Review operations
print(f"\nOperations Summary:")
print(f"  Copied:   {result.summary['copied']}")
print(f"  Skipped:  {result.summary['skipped']}")
print(f"  Conflicts: {result.summary['conflicts']}")
print(f"  Errors:    {result.summary['errors']}")

# Examine specific files
print(f"\nCopied Files:")
for file in result.files_copied:
    print(f"  ✓ {file}")

print(f"\nSkipped (Identical) Files:")
for file in result.files_skipped:
    print(f"  ⊘ {file}")

print(f"\nResolved Conflicts:")
for file, action in result.conflicts_resolved.items():
    print(f"  ⚠ {file}: {action}")

# Check for errors
if result.errors:
    print(f"\nErrors:")
    for error in result.errors:
        print(f"  ✗ {error}")
```

## Common Workflows

### Backup Before Major Changes

```python
# First, preview what would happen
manager = SyncManager(project_dir, global_dir, dry_run=True)
result = manager.sync("push")
print(f"Preview: Would sync {result.summary['copied']} files")

# If happy with preview, run actual sync
manager = SyncManager(project_dir, global_dir)
result = manager.sync("push")
# Backups are created automatically before overwriting
```

### Sync After Creating New Items

```python
# You've created new agents/commands in .claude/
# Push them to global .claude for use in other projects

result = manager.sync("push", categories=["agents", "commands"])

if result.success:
    print(f"✓ Pushed {result.summary['copied']} new items to global")
```

### Merge Global Updates to Project

```python
# Global .claude has been updated by other projects
# Pull the updates into your current project

result = manager.sync("pull")

for file in result.files_copied:
    print(f"Updated: {file}")

for file in result.files_skipped:
    print(f"Already had: {file}")
```

### Resolve Update Conflicts

```python
# You have local changes, global also has changes
# Use force mode to keep your local versions

manager = SyncManager(project_dir, global_dir, force=True)
result = manager.sync("push")

print(f"Synced local changes (overwriting {len(result.conflicts_resolved)} conflicts)")
```

## Category Reference

**Available Categories:**
- `agents` - Claude Code agents
- `commands` - Slash commands
- `skills` - Skill bundles (syncs entire directories)
- `prompts` - Prompt templates
- `hooks` - Hook configurations

**Special Handling:**
- Prompts are excluded by default (project-specific)
- Skills sync entire directories as units
- Other categories sync individual files

**Default Categories** (when none specified):
```python
["agents", "commands", "hooks", "skills"]
# Note: prompts excluded by default, user must confirm
```

## Important Notes

### File Conflict Detection

SyncManager detects real conflicts using SHA256 hashes:
- Identical files → skipped (no action needed)
- Different files → depends on mode:
  - `force=False`: skipped (user review recommended)
  - `force=True`: overwritten with backup

### Automatic Backups

Before overwriting files (non-dry-run):
- Backups created in `~/.claude/.backups/{timestamp}/`
- Allows rollback if needed
- Backup naming includes the backup timestamp

### Prompts Warning

Prompts are usually project-specific. They're excluded by default:
```python
# This WON'T sync prompts
result = manager.sync("push")

# This WILL sync prompts (if specified)
result = manager.sync("push", categories=["agents", "prompts"])
```

### Dry-Run Best Practice

Always preview before running without dry-run:
```python
# Step 1: Preview
dry_manager = SyncManager(project_dir, global_dir, dry_run=True)
preview = dry_manager.sync("push")
print(f"Would sync {preview.summary['copied']} files")

# Step 2: Execute if happy
real_manager = SyncManager(project_dir, global_dir)
result = real_manager.sync("push")
```

## Troubleshooting

### Files Not Being Synced

1. Check source directory exists
2. Verify files are in correct category folder
3. Check directory permissions
4. Use dry-run to see what's being found

```python
manager = SyncManager(project_dir, global_dir, dry_run=True)
result = manager.sync("push", categories=["agents"])
print(f"Found {result.summary['copied']} files to sync")
```

### Conflicts Not Resolving

In non-force mode, conflicting files are skipped:
```python
# See which files have conflicts
for file in result.conflicts_resolved:
    print(f"Conflict: {file}")

# Use force mode to resolve
force_manager = SyncManager(project_dir, global_dir, force=True)
result = force_manager.sync("push")
```

### Missing Destination Directory

SyncManager automatically creates destination directories:
```python
# Safe even if .global/.claude/agents doesn't exist yet
result = manager.sync("push")
# Directories created automatically
```

### Validation Failed

If a copied file fails validation:
1. Check disk space
2. Check file permissions
3. Try again (might be temporary issue)
4. Check error details in `result.errors`

## API Reference (Compact)

```python
# Initialize
manager = SyncManager(
    project_dir: Path,      # Path to .claude
    global_dir: Path,       # Path to ~/.claude
    reporter: Reporter = None,  # Custom reporter
    dry_run: bool = False,  # Preview only
    force: bool = False     # Auto-overwrite conflicts
)

# Main operation
result = manager.sync(
    direction: str,         # "push" or "pull"
    categories: List[str] = None  # Categories to sync
) -> SyncResult

# Result details
result.success              # bool - Overall success
result.files_copied         # List[str] - Files copied
result.files_skipped        # List[str] - Files skipped
result.conflicts_resolved   # Dict[str, str] - Conflicts
result.errors               # List[str] - Errors
result.summary              # Dict[str, int] - Counts
result.to_dict()           # -> Dict - Serialization
```

## Next Steps

- Read [SYNC_README.md](SYNC_README.md) for comprehensive documentation
- Check [tests/test_sync.py](../tests/test_sync.py) for more examples
- Review source code in sync.py for implementation details

## Support

For issues or questions:
1. Check error messages in `result.errors`
2. Use dry-run mode to preview operations
3. Review SYNC_README.md for detailed behavior
4. Check test cases for usage examples
