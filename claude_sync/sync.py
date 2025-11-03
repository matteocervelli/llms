"""Sync orchestration module for syncing configurations between project and global directories.

This module provides the main SyncManager class that coordinates sync operations,
handles conflicts, manages backups, and tracks operations.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .file_handler import FileHandler
from .reporter import Reporter

logger = logging.getLogger(__name__)


@dataclass
class SyncResult:
    """Container for sync results from a sync operation.

    Attributes:
        success: Whether the sync operation completed successfully.
        files_copied: List of file paths that were copied.
        files_skipped: List of file paths that were skipped.
        conflicts_resolved: Dictionary mapping file paths to resolution actions.
        errors: List of error messages encountered during sync.
        summary: Dictionary with operation counts (copied, skipped, conflicts, errors).
    """

    success: bool
    files_copied: List[str] = field(default_factory=list)
    files_skipped: List[str] = field(default_factory=list)
    conflicts_resolved: Dict[str, str] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert result to dictionary format.

        Returns:
            Dictionary representation of sync results.
        """
        return {
            "success": self.success,
            "files_copied": self.files_copied,
            "files_skipped": self.files_skipped,
            "conflicts_resolved": self.conflicts_resolved,
            "errors": self.errors,
            "summary": self.summary,
        }


class SyncManager:
    """Manages sync operations between project and global directories.

    This manager orchestrates syncing files between project-specific (.claude/)
    and global (~/.claude/) directories, handling conflicts, backups, and validation.
    """

    # Categories that can be synced
    VALID_CATEGORIES = {"agents", "commands", "skills", "prompts", "hooks"}

    # Categories that should sync entire directories (not individual files)
    DIRECTORY_CATEGORIES = {"skills"}

    def __init__(
        self,
        project_dir: Path,
        global_dir: Path,
        reporter: Optional[Reporter] = None,
        dry_run: bool = False,
        force: bool = False,
    ):
        """Initialize sync manager.

        Args:
            project_dir: Path to project-specific .claude directory.
            global_dir: Path to global ~/.claude directory.
            reporter: Reporter instance for output (creates default if None).
            dry_run: If True, preview changes without executing.
            force: If True, overwrite conflicts without asking.

        Raises:
            ValueError: If directories don't exist.
        """
        self.project_dir = Path(project_dir)
        self.global_dir = Path(global_dir)
        self.reporter = reporter or Reporter()
        self.dry_run = dry_run
        self.force = force

        # Validate directories exist
        if not self.project_dir.exists():
            raise ValueError(f"Project directory not found: {self.project_dir}")
        if not self.global_dir.exists():
            raise ValueError(f"Global directory not found: {self.global_dir}")

        self.file_handler = FileHandler(backup_enabled=not dry_run)
        self.operation_count = 0

    def sync(self, direction: str, categories: Optional[List[str]] = None) -> SyncResult:
        """Perform sync operation.

        Args:
            direction: "push" (project → global) or "pull" (global → project).
            categories: List of categories to sync. Defaults to all non-prompt categories.

        Returns:
            SyncResult containing operation details and status.

        Raises:
            ValueError: If direction or categories are invalid.
        """
        if direction not in ("push", "pull"):
            raise ValueError(f"Invalid direction: {direction}. Must be 'push' or 'pull'.")

        # Default categories (exclude prompts as they're usually project-specific)
        if categories is None:
            categories = list(self.VALID_CATEGORIES - {"prompts"})

        # Validate categories
        invalid_categories = set(categories) - self.VALID_CATEGORIES
        if invalid_categories:
            raise ValueError(f"Invalid categories: {invalid_categories}")

        result = SyncResult(success=True)

        self.reporter.print_header(
            f"Starting {direction.upper()} Sync"
            f"{' (DRY RUN)' if self.dry_run else ''}"
        )

        # Ask about prompts if not explicitly included/excluded
        if "prompts" in self.VALID_CATEGORIES and "prompts" not in categories:
            if self._should_sync_prompts():
                categories = list(categories) + ["prompts"]

        # Sync each category
        for category in categories:
            if category in self.DIRECTORY_CATEGORIES:
                category_result = self._sync_category_directory(
                    category, direction
                )
            else:
                category_result = self._sync_category_files(category, direction)

            # Merge results
            result.files_copied.extend(category_result.get("files_copied", []))
            result.files_skipped.extend(category_result.get("files_skipped", []))
            result.conflicts_resolved.update(
                category_result.get("conflicts_resolved", {})
            )
            result.errors.extend(category_result.get("errors", []))

        # Calculate summary
        result.summary = {
            "copied": len(result.files_copied),
            "skipped": len(result.files_skipped),
            "conflicts": len(result.conflicts_resolved),
            "errors": len(result.errors),
            "total": (
                len(result.files_copied)
                + len(result.files_skipped)
                + len(result.conflicts_resolved)
            ),
        }

        # Set success status
        result.success = len(result.errors) == 0

        self._report_sync_summary(result)

        return result

    def _sync_category_files(self, category: str, direction: str) -> Dict:
        """Sync individual files in a category.

        Args:
            category: Category name (agents, commands, etc.).
            direction: "push" or "pull".

        Returns:
            Dictionary with sync results for the category.
        """
        result = {
            "files_copied": [],
            "files_skipped": [],
            "conflicts_resolved": {},
            "errors": [],
        }

        if direction == "push":
            source_dir = self.project_dir / category
            dest_dir = self.global_dir / category
        else:  # pull
            source_dir = self.global_dir / category
            dest_dir = self.project_dir / category

        # Skip if source directory doesn't exist
        if not source_dir.exists():
            self.reporter.print_warning(f"Source directory not found: {source_dir}")
            return result

        # Create destination if it doesn't exist
        if not self.dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)

        # Process files
        for source_file in source_dir.iterdir():
            if source_file.is_file():
                dest_file = dest_dir / source_file.name

                status = self._copy_file_with_conflict_check(
                    source_file, dest_file, direction
                )

                if status == "copied":
                    result["files_copied"].append(str(source_file))
                elif status == "skipped":
                    result["files_skipped"].append(str(source_file))
                elif status == "conflict_resolved":
                    result["conflicts_resolved"][str(source_file)] = "overwritten"
                elif status == "error":
                    result["errors"].append(f"Failed to sync {source_file}")

        self.reporter.print_verbose(
            f"Category '{category}' ({direction}): "
            f"{len(result['files_copied'])} copied, "
            f"{len(result['files_skipped'])} skipped"
        )

        return result

    def _sync_category_directory(self, category: str, direction: str) -> Dict:
        """Sync entire directory for a category (e.g., skills).

        Args:
            category: Category name (skills, etc.).
            direction: "push" or "pull".

        Returns:
            Dictionary with sync results for the category.
        """
        result = {
            "files_copied": [],
            "files_skipped": [],
            "conflicts_resolved": {},
            "errors": [],
        }

        if direction == "push":
            source_dir = self.project_dir / category
            dest_dir = self.global_dir / category
        else:  # pull
            source_dir = self.global_dir / category
            dest_dir = self.project_dir / category

        # Skip if source directory doesn't exist
        if not source_dir.exists():
            self.reporter.print_warning(f"Source directory not found: {source_dir}")
            return result

        # For directory categories, sync each subdirectory as a unit
        for source_subdir in source_dir.iterdir():
            if source_subdir.is_dir():
                dest_subdir = dest_dir / source_subdir.name

                if dest_subdir.exists():
                    # Conflict: destination already exists
                    if self.force or self.dry_run:
                        action = "overwrite" if not self.dry_run else "preview"
                        result["conflicts_resolved"][str(source_subdir)] = action
                        if not self.dry_run:
                            try:
                                self.file_handler.copy_directory(
                                    source_subdir, dest_subdir, create_backup=True
                                )
                                result["files_copied"].append(str(source_subdir))
                            except Exception as e:
                                result["errors"].append(f"Failed to sync {source_subdir}: {e}")
                    else:
                        result["files_skipped"].append(str(source_subdir))
                else:
                    # No conflict, copy directory
                    if not self.dry_run:
                        try:
                            self.file_handler.copy_directory(
                                source_subdir, dest_subdir, create_backup=False
                            )
                            result["files_copied"].append(str(source_subdir))
                        except Exception as e:
                            result["errors"].append(f"Failed to sync {source_subdir}: {e}")
                    else:
                        result["files_copied"].append(str(source_subdir))

        self.reporter.print_verbose(
            f"Category '{category}' ({direction}): "
            f"{len(result['files_copied'])} copied, "
            f"{len(result['files_skipped'])} skipped"
        )

        return result

    def _copy_file_with_conflict_check(
        self, source_file: Path, dest_file: Path, direction: str
    ) -> str:
        """Copy file, handling conflicts if destination exists.

        Args:
            source_file: Source file path.
            dest_file: Destination file path.
            direction: "push" or "pull" (for logging/reporting).

        Returns:
            Status string: "copied", "skipped", "conflict_resolved", or "error".
        """
        source_file = Path(source_file)
        dest_file = Path(dest_file)

        # File doesn't exist in destination - copy it
        if not dest_file.exists():
            if self.dry_run:
                self.reporter.print_verbose(
                    f"[DRY RUN] Would copy: {source_file.name}"
                )
                return "copied"

            try:
                self.file_handler.copy_file(source_file, dest_file)
                self.reporter.print_success(f"Copied: {source_file.name}")
                return "copied"
            except Exception as e:
                logger.error(f"Failed to copy {source_file}: {e}")
                return "error"

        # Destination exists - check if identical
        try:
            source_hash = self.file_handler.get_file_hash(source_file)
            dest_hash = self.file_handler.get_file_hash(dest_file)

            if source_hash == dest_hash:
                # Files are identical - skip
                self.reporter.print_verbose(f"Identical: {source_file.name}")
                return "skipped"

            # Files differ - conflict
            if self.force:
                # Force overwrite without asking
                if self.dry_run:
                    self.reporter.print_warning(
                        f"[DRY RUN] Would overwrite (force): {source_file.name}"
                    )
                    return "conflict_resolved"

                try:
                    self.file_handler.copy_file(source_file, dest_file)
                    self.reporter.print_warning(f"Overwritten (force): {source_file.name}")
                    return "conflict_resolved"
                except Exception as e:
                    logger.error(f"Failed to overwrite {dest_file}: {e}")
                    return "error"
            else:
                # Ask user about conflict
                self.reporter.print_warning(
                    f"Conflict detected: {source_file.name} exists at destination"
                )
                return "skipped"

        except Exception as e:
            logger.error(f"Error checking file conflict for {source_file}: {e}")
            return "error"

    def _should_sync_prompts(self) -> bool:
        """Ask user if prompts should be synced.

        Prompts are often project-specific, so this asks for confirmation.

        Returns:
            True if user wants to sync prompts, False otherwise.
        """
        prompts_dir = self.project_dir / "prompts"
        if not prompts_dir.exists():
            return False

        self.reporter.print_info("Prompts are usually project-specific.")
        response = input("Include prompts in sync? (y/n): ").strip().lower()
        return response in ("y", "yes")

    def _report_sync_summary(self, result: SyncResult) -> None:
        """Report sync operation summary.

        Args:
            result: SyncResult from completed sync operation.
        """
        self.reporter.print_header("Sync Summary")

        # Print statistics
        print(f"\n  Files copied: {result.summary['copied']}")
        print(f"  Files skipped: {result.summary['skipped']}")
        if result.summary["conflicts"] > 0:
            print(f"  Conflicts resolved: {result.summary['conflicts']}")

        # Print file lists
        if result.files_copied:
            self.reporter.print_section("Copied Files", result.files_copied)

        if result.files_skipped:
            self.reporter.print_section(
                "Skipped Files (identical)", result.files_skipped
            )

        if result.conflicts_resolved:
            self.reporter.print_section(
                "Conflicts Resolved", list(result.conflicts_resolved.keys())
            )

        # Print errors
        if result.errors:
            print()
            self.reporter.print_file_list(result.errors, "error")

        # Final status
        print()
        if result.success:
            self.reporter.print_success("Sync completed successfully!")
        else:
            self.reporter.print_error(f"Sync completed with {len(result.errors)} error(s)")
