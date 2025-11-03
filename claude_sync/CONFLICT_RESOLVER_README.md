# Conflict Resolver Module

Interactive conflict resolution system for Claude configuration synchronization between project-specific and global file locations.

## Overview

The `conflict_resolver.py` module provides a complete interactive resolution system for handling file conflicts that occur when configuration files exist in both project and global scopes with different content.

### Key Features

- **Interactive Conflict Resolution**: Display conflicts with full file metadata and prompt users for action
- **Diff Viewing**: Show unified diff between conflicting files with syntax coloring
- **Batch Operations**: Apply resolution choice to all remaining conflicts without re-prompting
- **Force Mode**: Auto-resolve using file modification time (newer file wins)
- **Graceful Error Handling**: Handle edge cases like binary files, permission errors, and user interrupts
- **Detailed File Info**: Display file size and modification timestamp for informed decisions

## Architecture

### ConflictAction Enum

Defines all possible user actions for conflict resolution:

```python
class ConflictAction(Enum):
    KEEP_PROJECT = "project"      # Use project file
    KEEP_GLOBAL = "global"        # Use global file
    SHOW_DIFF = "diff"           # Display diff and re-prompt
    SKIP = "skip"                # Skip this file
    APPLY_ALL_PROJECT = "all_project"    # Project for all remaining
    APPLY_ALL_GLOBAL = "all_global"      # Global for all remaining
```

### ConflictResolver Class

Main class handling all conflict resolution logic:

```python
class ConflictResolver:
    def __init__(self, reporter: Reporter, force: bool = False)
    def resolve_conflict(
        self,
        project_file: Path,
        global_file: Path,
        direction: str = "push"
    ) -> ConflictAction
    def show_diff(self, file1: Path, file2: Path) -> None
    def show_file_info(self, file_path: Path) -> None
    def prompt_user(self, project_file: Path, global_file: Path) -> ConflictAction
    def auto_resolve(self, project_file: Path, global_file: Path) -> ConflictAction
    def reset_batch_mode(self) -> None
```

## Usage Examples

### Basic Interactive Resolution

```python
from pathlib import Path
from claude_sync.reporter import Reporter
from claude_sync.conflict_resolver import ConflictResolver, ConflictAction

# Initialize
reporter = Reporter(verbose=True)
resolver = ConflictResolver(reporter, force=False)

# Resolve a conflict
project_file = Path("/path/to/project/.claude/agents/file.md")
global_file = Path.home() / ".claude" / "agents" / "file.md"

action = resolver.resolve_conflict(project_file, global_file, direction="push")

# Handle the action
if action == ConflictAction.KEEP_PROJECT:
    # Copy project to global
    pass
elif action == ConflictAction.KEEP_GLOBAL:
    # Copy global to project
    pass
elif action == ConflictAction.SKIP:
    # Skip this file
    pass
```

### Force Mode (Auto-Resolve)

```python
# Auto-resolve using modification time (no prompts)
resolver = ConflictResolver(reporter, force=True)

action = resolver.resolve_conflict(project_file, global_file)
# Returns KEEP_PROJECT if project is newer, KEEP_GLOBAL if global is newer
```

### Batch Operations

```python
# First conflict - user selects "apply to all"
action1 = resolver.resolve_conflict(file1, file2)
# User pressed "a" (apply project to all)

# Subsequent conflicts automatically use that choice
action2 = resolver.resolve_conflict(file3, file4)  # Returns KEEP_PROJECT
action3 = resolver.resolve_conflict(file5, file6)  # Returns KEEP_PROJECT

# Reset for different choice on next batch
resolver.reset_batch_mode()
action4 = resolver.resolve_conflict(file7, file8)  # Prompts user again
```

### Handling Multiple Conflicts

```python
conflicts = [
    (project_file1, global_file1),
    (project_file2, global_file2),
    (project_file3, global_file3),
]

for proj, glob in conflicts:
    try:
        action = resolver.resolve_conflict(proj, glob)
        if action == ConflictAction.KEEP_PROJECT:
            # Sync: project -> global
            file_handler.copy_file(proj, glob)
        elif action == ConflictAction.KEEP_GLOBAL:
            # Sync: global -> project
            file_handler.copy_file(glob, proj)
        # SKIP and batch actions are handled similarly
    except KeyboardInterrupt:
        print("Conflict resolution cancelled by user")
        break
```

## User Interaction

### Prompt Display

When a conflict is encountered, users see:

```
⚠️  CONFLICT: agents.md exists in both locations with different content

  Project file: /path/to/project/.claude/agents/agents.md
  Size: 1.2 KB
  Modified: 2025-01-30 14:23:10

  Global file: /path/to/.claude/agents/agents.md
  Size: 1.1 KB
  Modified: 2025-01-28 09:15:32

  Actions:
    [p] Keep project version
    [g] Keep global version
    [d] Show diff
    [s] Skip this file
    [a] Apply project to ALL remaining conflicts
    [A] Apply global to ALL remaining conflicts

  Your choice [p/g/d/s/a/A]:
```

### Diff View

When user selects "d", a unified diff is displayed:

```
======================================================================
DIFF: Project vs Global
======================================================================
--- agents.md (project)
+++ agents.md (global)
@@ -1,5 +1,5 @@
 # Agents Configuration
-Version: 1.0
+Version: 2.0
-Author: Alice
+Author: Bob

 Description of available agents
======================================================================
```

## Implementation Details

### File Metadata Display

```python
def show_file_info(self, file_path: Path) -> None:
    """Display file size and modification time."""
    stat = file_path.stat()
    size_kb = stat.st_size / 1024
    mtime_str = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"  Size: {size_kb:.1f} KB")
    print(f"  Modified: {mtime_str}")
```

### Diff Generation

Uses Python's `difflib.unified_diff()` with:
- ANSI color coding for diff headers, additions, deletions
- Line numbers and context
- Graceful handling of binary files (detects and shows warning)

### Batch Mode Management

```python
self.apply_all: Optional[ConflictAction] = None
```

- `None` = Normal mode, prompt user for each conflict
- `ConflictAction.KEEP_PROJECT` = Apply project to all remaining
- `ConflictAction.KEEP_GLOBAL` = Apply global to all remaining
- Call `reset_batch_mode()` to clear and resume prompting

### Force Mode Behavior

When `force=True`:
1. Compares modification times: `project_mtime` vs `global_mtime`
2. Returns `KEEP_PROJECT` if `project_mtime >= global_mtime`
3. Returns `KEEP_GLOBAL` otherwise
4. Defaults to `KEEP_PROJECT` on stat errors
5. No user interaction - completely automated

### Error Handling

- **KeyboardInterrupt**: User pressed Ctrl+C during prompt
- **EOFError**: EOF during input (e.g., piped input)
- **Binary Files**: Detected via UnicodeDecodeError, shows warning instead of diff
- **Nonexistent Files**: Handled gracefully without raising exceptions
- **Permission Errors**: Caught and reported via reporter

## Testing

Comprehensive test suite with 30 tests covering:

- Enum values and behavior
- Initialization with/without force mode
- File info display (metadata, error handling)
- Diff generation (additions, deletions, binary files)
- Auto-resolve logic (newer file selection, tie-breaking)
- User prompts (all action types, invalid input, keyboard interrupt)
- Batch operations (apply all, state management)
- Integration workflows (multi-conflict scenarios)

Run tests:
```bash
pytest tests/test_conflict_resolver.py -v
```

All 30 tests pass with comprehensive coverage of:
- Happy paths (normal operation)
- Edge cases (binary files, nonexistent files, EOF)
- Error scenarios (permission errors, invalid input)
- Integration flows (batch operations, force mode)

## Integration with Sync System

The conflict resolver is used by the `SyncManager` to handle conflicts during sync operations:

```python
from claude_sync.conflict_resolver import ConflictResolver, ConflictAction

# In SyncManager.sync()
resolver = ConflictResolver(self.reporter, force=self.force)

for conflict in conflicts:
    action = resolver.resolve_conflict(
        conflict.project_file,
        conflict.global_file,
        direction=self.direction
    )

    if action == ConflictAction.KEEP_PROJECT:
        self.file_handler.copy_file(conflict.project_file, conflict.global_file)
    elif action == ConflictAction.KEEP_GLOBAL:
        self.file_handler.copy_file(conflict.global_file, conflict.project_file)
    elif action == ConflictAction.SKIP:
        continue  # Skip this conflict
```

## Dependencies

- **Standard Library**:
  - `difflib`: Unified diff generation
  - `enum`: ConflictAction enum
  - `pathlib`: Path handling
  - `sys`: System-level operations
  - `datetime`: Modification time formatting

- **Internal**:
  - `claude_sync.reporter.Reporter`: Colored console output

## Design Principles

1. **User-Centric**: Clear prompts with all necessary information
2. **Non-Destructive**: Users always have the option to skip
3. **Transparent**: Show diffs before decisions for informed choices
4. **Efficient**: Batch mode to avoid repetitive prompts
5. **Robust**: Handles edge cases gracefully
6. **Clean Code**: Under 200 lines, single responsibility
7. **Well-Tested**: 30 comprehensive tests covering all scenarios

## Limitations and Future Enhancements

### Current Limitations
- Text files only for diff display (binary files show warning)
- No merge option (only keep one or skip)
- No undo capability (handled by FileHandler backups)

### Possible Future Enhancements
- Merge option for configuration files
- Side-by-side diff view
- File size/content preview
- Automatic backup of both versions
- Selective line merging
