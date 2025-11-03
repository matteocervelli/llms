# SyncManager - Configuration Sync Module

## Overview

The `sync.py` module provides a comprehensive synchronization system for managing Claude configurations between project-specific (`.claude/`) and global (`~/.claude/`) directories.

## Classes

### SyncResult

Container dataclass for sync operation results.

**Attributes:**
- `success` (bool): Whether the sync completed successfully
- `files_copied` (List[str]): Paths of files that were copied
- `files_skipped` (List[str]): Paths of identical files that were skipped
- `conflicts_resolved` (Dict[str, str]): Files with conflicts and actions taken
- `errors` (List[str]): Error messages encountered during sync
- `summary` (Dict[str, int]): Operation counts (copied, skipped, conflicts, errors, total)

**Methods:**
- `to_dict()`: Convert result to dictionary format for easy serialization

### SyncManager

Main class orchestrating sync operations between project and global directories.

#### Initialization

```python
from pathlib import Path
from claude_sync import SyncManager, Reporter

project_dir = Path(".claude")
global_dir = Path.home() / ".claude"

manager = SyncManager(
    project_dir=project_dir,
    global_dir=global_dir,
    reporter=None,  # Creates default Reporter if None
    dry_run=False,  # Preview changes without executing
    force=False     # Overwrite conflicts without asking
)
```

**Parameters:**
- `project_dir` (Path): Project-specific configuration directory
- `global_dir` (Path): Global user configuration directory
- `reporter` (Reporter, optional): Reporter for output (creates default if None)
- `dry_run` (bool): If True, preview changes without executing them
- `force` (bool): If True, overwrite conflicts without asking

#### Main Methods

##### sync(direction, categories=None)

Perform sync operation between directories.

```python
# Push project configs to global
result = manager.sync("push")

# Pull global configs to project
result = manager.sync("pull")

# Sync specific categories
result = manager.sync("push", categories=["agents", "commands"])
```

**Parameters:**
- `direction` (str): "push" (project → global) or "pull" (global → project)
- `categories` (List[str], optional): Categories to sync. Defaults to all except prompts
  - Valid categories: `agents`, `commands`, `skills`, `prompts`, `hooks`
  - `skills` syncs entire directories; others sync individual files
  - Prompts are excluded by default (project-specific) and require user confirmation

**Returns:**
- `SyncResult` containing operation details

**Raises:**
- `ValueError`: If direction or categories are invalid
- `FileNotFoundError`: If source files don't exist

## Sync Behavior

### Direction: Push (Project → Global)

```python
result = manager.sync("push")
```

Copies files from project directory to global directory:
- New files in project → copied to global
- Identical files → skipped
- Different files → conflict handling (force/skip)

### Direction: Pull (Global → Project)

```python
result = manager.sync("pull")
```

Copies files from global directory to project directory:
- New files in global → copied to project
- Identical files → skipped
- Different files → conflict handling (force/skip)

### Category Behavior

**Individual File Categories** (`agents`, `commands`, `prompts`, `hooks`):
- Syncs individual markdown files
- Checks for conflicts by file hash
- Skips identical files (same content hash)

**Directory Categories** (`skills`):
- Syncs entire skill subdirectories as units
- Replaces destination directory if it exists (with backup)
- Preserves directory structure

### Conflict Resolution

1. **No Conflict** (destination doesn't exist):
   - File is copied directly
   - Backup created if destination exists (non-dry-run)

2. **Identical Files** (same content hash):
   - File is skipped (no operation needed)

3. **Different Files** (content mismatch):
   - If `force=True`: Automatically overwrites (with backup)
   - If `force=False`: File is skipped (user review recommended)

### Dry-Run Mode

When `dry_run=True`:
- No files are copied
- No backups are created
- Verbose output shows what would be synced
- Results still include "files_copied" for dry-run preview

```python
manager = SyncManager(project_dir, global_dir, dry_run=True)
result = manager.sync("push")  # Preview only, no changes
```

### Force Mode

When `force=True`:
- Conflicting files are automatically overwritten
- Backups are created before overwriting (non-dry-run)
- User is not prompted for confirmation

```python
manager = SyncManager(project_dir, global_dir, force=True)
result = manager.sync("push")  # Overwrites conflicting files
```

## Usage Examples

### Basic Sync Operations

```python
from pathlib import Path
from claude_sync import SyncManager

# Initialize manager
project_dir = Path(".claude")
global_dir = Path.home() / ".claude"
manager = SyncManager(project_dir, global_dir)

# Push project configs to global
result = manager.sync("push")
if result.success:
    print(f"Copied {result.summary['copied']} files")
else:
    print(f"Errors: {result.errors}")

# Pull global configs to project
result = manager.sync("pull")
```

### Selective Syncing

```python
# Sync only agents and commands
result = manager.sync("push", categories=["agents", "commands"])

# Sync skills (directory category)
result = manager.sync("push", categories=["skills"])
```

### Preview Changes (Dry-Run)

```python
# Preview push without making changes
manager = SyncManager(project_dir, global_dir, dry_run=True)
result = manager.sync("push")

print(f"Would copy: {len(result.files_copied)} files")
print(f"Would skip: {len(result.files_skipped)} files")
```

### Force Overwrite Conflicts

```python
# Automatically overwrite conflicting files with project versions
manager = SyncManager(project_dir, global_dir, force=True)
result = manager.sync("push")

for file, action in result.conflicts_resolved.items():
    print(f"Resolved {file}: {action}")
```

### Include Prompts

```python
# Prompts are excluded by default; include them by specifying category
result = manager.sync("push", categories=["agents", "commands", "prompts"])

# Or answer "y" when prompted during default sync
# manager.sync("push") → "Include prompts in sync? (y/n):"
```

### Result Analysis

```python
result = manager.sync("push")

# Check success status
if result.success:
    # Print summary
    print(f"Total operations: {result.summary['total']}")
    print(f"Copied: {result.summary['copied']}")
    print(f"Skipped: {result.summary['skipped']}")
    print(f"Conflicts: {result.summary['conflicts']}")

    # Analyze specific results
    for file in result.files_copied:
        print(f"✓ Copied: {file}")

    for file in result.files_skipped:
        print(f"⊘ Skipped (identical): {file}")

    for file, action in result.conflicts_resolved.items():
        print(f"⚠ Conflict resolved ({action}): {file}")
else:
    # Handle errors
    for error in result.errors:
        print(f"❌ Error: {error}")
```

## File Validation

All copied files are validated using SHA256 hash comparison:
- Source and destination file contents must match
- Validation ensures copy integrity before reporting success
- Failed validations are logged and reported as errors

## Backups

Before overwriting existing files (non-dry-run, non-identical):
- Automatic backups are created with timestamps
- Backups stored in `~/.claude/.backups/{timestamp}/`
- Allows rollback of sync operations if needed
- Disabled in dry-run mode (no files actually copied)

## Reporting

Sync operations produce colored console output via Reporter:
- Headers and sections for easy reading
- Color-coded status messages (success, warning, error, info)
- File lists grouped by status
- Summary statistics
- Support for verbose/debug output

```python
from claude_sync import Reporter

reporter = Reporter(verbose=True)
manager = SyncManager(project_dir, global_dir, reporter=reporter)
result = manager.sync("push")  # Detailed output with debug messages
```

## Error Handling

The SyncManager gracefully handles errors:
- Missing directories are logged as warnings, not failures
- Individual file copy failures don't stop entire sync
- Errors are tracked in `SyncResult.errors` list
- Hash validation failures are caught and reported
- Permission errors are logged with details

## Constants

**VALID_CATEGORIES:**
```python
{"agents", "commands", "skills", "prompts", "hooks"}
```

**DIRECTORY_CATEGORIES** (sync entire directories):
```python
{"skills"}
```

All other categories sync individual files.

## Performance Considerations

- **Dry-run is fast**: No file I/O, just directory scanning
- **Hash comparison overhead**: O(n) where n = file size, necessary for conflict detection
- **Large skill directories**: Can take time due to recursive directory copy
- **Excluded patterns** (`.pyc`, `__pycache__`, etc.) reduce copy volume

## Design Principles

1. **Safety First**: Always backup before overwriting (non-dry-run)
2. **User Control**: Dry-run preview and force mode for user preference
3. **Transparency**: Detailed reporting of all operations
4. **Error Resilience**: Continue syncing other files on individual failures
5. **Data Integrity**: Hash validation for all file copies
6. **Project-Specific Handling**: Special treatment for prompts (usually local)

## Testing

Comprehensive test suite in `tests/test_sync.py`:
- 29 test cases covering all sync scenarios
- Tests for initialization, validation, file operations
- Tests for all categories and directory sync
- Error handling and edge cases
- Integration tests for complete workflows
- 100% coverage of core functionality

Run tests:
```bash
pytest tests/test_sync.py -v
```

## Limitations and Future Enhancements

**Current Limitations:**
- No incremental sync (timestamp-based)
- No bidirectional conflict resolution (always favors source)
- No exclusion filters (syncs all files in category)
- Prompts require explicit confirmation (not automated)

**Potential Enhancements:**
- Timestamp-based incremental sync
- Interactive conflict resolution UI
- Custom exclusion filters
- Sync scheduling/automation
- Three-way merge for conflicts
- Sync history and rollback capability
