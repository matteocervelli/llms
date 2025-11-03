"""Interactive conflict resolution for Claude configuration sync.

Handles interactive conflict resolution when files exist in both locations
with different content. Provides diff viewing, user prompts, and batch operations.
"""

import sys
from difflib import unified_diff
from enum import Enum
from pathlib import Path
from typing import Optional

from .reporter import Reporter


class ConflictAction(Enum):
    """Actions user can take for a conflict."""

    KEEP_PROJECT = "project"
    KEEP_GLOBAL = "global"
    SHOW_DIFF = "diff"
    SKIP = "skip"
    APPLY_ALL_PROJECT = "all_project"
    APPLY_ALL_GLOBAL = "all_global"


class ConflictResolver:
    """Resolve file conflicts interactively with diff viewing and batch operations.

    Handles conflict resolution between project-specific and global file versions,
    with support for diff viewing, batch operations, and force mode auto-resolution.
    """

    def __init__(self, reporter: Reporter, force: bool = False) -> None:
        """Initialize conflict resolver.

        Args:
            reporter: Reporter instance for colored console output.
            force: If True, auto-resolve using modification time (newer wins).
        """
        self.reporter = reporter
        self.force = force
        self.apply_all: Optional[ConflictAction] = None

    def resolve_conflict(
        self, project_file: Path, global_file: Path, direction: str = "push"
    ) -> ConflictAction:
        """Resolve a single file conflict.

        Args:
            project_file: Path to project-specific file.
            global_file: Path to global file.
            direction: "push" (project->global) or "pull" (global->project).

        Returns:
            ConflictAction indicating the resolution choice.

        Raises:
            KeyboardInterrupt: If user cancels operation.
        """
        # Return cached batch decision if available
        if self.apply_all is not None:
            return self.apply_all

        # Auto-resolve in force mode
        if self.force:
            return self.auto_resolve(project_file, global_file)

        # Interactive resolution
        return self.prompt_user(project_file, global_file)

    def show_diff(self, file1: Path, file2: Path) -> None:
        """Display unified diff between two files.

        Args:
            file1: First file path (typically project).
            file2: Second file path (typically global).
        """
        try:
            with open(file1, "r", encoding="utf-8") as f1:
                lines1 = f1.readlines()
            with open(file2, "r", encoding="utf-8") as f2:
                lines2 = f2.readlines()

            diff = unified_diff(
                lines1,
                lines2,
                fromfile=f"{file1.name} (project)",
                tofile=f"{file2.name} (global)",
                lineterm="",
            )

            print("\n" + "=" * 70)
            print("DIFF: Project vs Global")
            print("=" * 70)
            for line in diff:
                # Color diff output
                if line.startswith("+++") or line.startswith("---"):
                    print(f"\033[96m{line}\033[0m")  # Cyan
                elif line.startswith("+"):
                    print(f"\033[92m{line}\033[0m")  # Green
                elif line.startswith("-"):
                    print(f"\033[91m{line}\033[0m")  # Red
                elif line.startswith("@@"):
                    print(f"\033[93m{line}\033[0m")  # Yellow
                else:
                    print(line)
            print("=" * 70 + "\n")

        except UnicodeDecodeError:
            self.reporter.print_warning("Binary file - cannot display diff")
        except Exception as e:
            self.reporter.print_error(f"Failed to display diff: {e}")

    def show_file_info(self, file_path: Path) -> None:
        """Display file metadata (size, modification time).

        Args:
            file_path: Path to file.
        """
        try:
            stat = file_path.stat()
            size_kb = stat.st_size / 1024
            mtime = Path(file_path).stat().st_mtime

            # Format modification time
            from datetime import datetime

            mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

            print(f"  Size: {size_kb:.1f} KB")
            print(f"  Modified: {mtime_str}")

        except Exception as e:
            self.reporter.print_error(f"Failed to read file info: {e}")

    def prompt_user(
        self, project_file: Path, global_file: Path
    ) -> ConflictAction:
        """Prompt user for conflict resolution action.

        Args:
            project_file: Path to project-specific file.
            global_file: Path to global file.

        Returns:
            ConflictAction chosen by user.

        Raises:
            KeyboardInterrupt: If user cancels (Ctrl+C).
        """
        # Display conflict header
        print()
        self.reporter.print_warning(
            f"CONFLICT: {project_file.name} exists in both locations "
            "with different content"
        )

        # Show file information
        print(f"\n  Project file: {project_file}")
        self.show_file_info(project_file)

        print(f"\n  Global file: {global_file}")
        self.show_file_info(global_file)

        # Show action menu
        print("\n  Actions:")
        print("    [p] Keep project version")
        print("    [g] Keep global version")
        print("    [d] Show diff")
        print("    [s] Skip this file")
        print("    [a] Apply project to ALL remaining conflicts")
        print("    [A] Apply global to ALL remaining conflicts")

        while True:
            try:
                choice = input("\n  Your choice [p/g/d/s/a/A]: ").strip()

                if choice == "p":
                    return ConflictAction.KEEP_PROJECT
                elif choice == "g":
                    return ConflictAction.KEEP_GLOBAL
                elif choice == "d":
                    self.show_diff(project_file, global_file)
                    # Loop back to prompt again
                    continue
                elif choice == "s":
                    return ConflictAction.SKIP
                elif choice == "a":
                    self.apply_all = ConflictAction.KEEP_PROJECT
                    return ConflictAction.APPLY_ALL_PROJECT
                elif choice == "A":
                    self.apply_all = ConflictAction.KEEP_GLOBAL
                    return ConflictAction.APPLY_ALL_GLOBAL
                else:
                    print("  Invalid choice. Please enter p, g, d, s, a, or A")
                    continue

            except KeyboardInterrupt:
                print("\n")
                raise KeyboardInterrupt("User cancelled conflict resolution")
            except EOFError:
                # Handle pipe/redirect scenario
                raise KeyboardInterrupt("EOF encountered during input")

    def auto_resolve(
        self, project_file: Path, global_file: Path
    ) -> ConflictAction:
        """Auto-resolve using modification time (force mode).

        In force mode, the file with the newer modification time wins.

        Args:
            project_file: Path to project-specific file.
            global_file: Path to global file.

        Returns:
            ConflictAction: Keep project or keep global based on mtime.
        """
        try:
            project_mtime = project_file.stat().st_mtime
            global_mtime = global_file.stat().st_mtime

            if project_mtime >= global_mtime:
                self.reporter.print_info(
                    f"Auto-resolving (force mode): keeping project version "
                    f"of {project_file.name} (newer)"
                )
                return ConflictAction.KEEP_PROJECT
            else:
                self.reporter.print_info(
                    f"Auto-resolving (force mode): keeping global version "
                    f"of {project_file.name} (newer)"
                )
                return ConflictAction.KEEP_GLOBAL

        except Exception as e:
            self.reporter.print_error(f"Failed to auto-resolve: {e}")
            # Default to project in case of error
            return ConflictAction.KEEP_PROJECT

    def reset_batch_mode(self) -> None:
        """Reset batch operation mode.

        Clears any "apply to all" decisions, allowing user to be prompted
        again for subsequent conflicts.
        """
        self.apply_all = None
