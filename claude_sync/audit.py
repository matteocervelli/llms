"""Audit module for comparing Claude configuration files between directories.

This module scans and compares files between project-specific and global
directories, detecting differences and generating structured audit reports.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AuditResult:
    """Container for audit results.

    Attributes:
        in_sync: List of files that match between both directories.
        project_only: List of files that exist only in project directory.
        global_only: List of files that exist only in global directory.
        conflicts: List of files with different content in both locations.
        errors: List of error messages encountered during audit.
        total_files: Total number of unique files checked.
    """

    in_sync: List[str] = field(default_factory=list)
    project_only: List[str] = field(default_factory=list)
    global_only: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    total_files: int = 0

    @property
    def success(self) -> bool:
        """Check if audit completed without errors.

        Returns:
            True if no errors were encountered, False otherwise.
        """
        return len(self.errors) == 0

    @property
    def is_in_sync(self) -> bool:
        """Check if all files are in sync across directories.

        Returns:
            True if no conflicts, project_only, or global_only files exist.
        """
        return (
            len(self.conflicts) == 0
            and len(self.project_only) == 0
            and len(self.global_only) == 0
        )

    def to_dict(self) -> Dict:
        """Convert audit result to dictionary format.

        Returns:
            Dictionary representation of audit results.
        """
        return {
            "in_sync": self.in_sync,
            "project_only": self.project_only,
            "global_only": self.global_only,
            "conflicts": self.conflicts,
            "errors": self.errors,
            "total_files": self.total_files,
            "success": self.success,
            "is_in_sync": self.is_in_sync,
        }


class AuditManager:
    """Manages auditing of Claude configuration files across directories.

    Scans project and global directories for agents, commands, skills, prompts,
    and hooks, comparing file lists and content to detect differences.
    """

    def __init__(
        self,
        project_dir: Path,
        global_dir: Path,
        reporter: Optional[object] = None,
        file_handler: Optional[object] = None,
    ) -> None:
        """Initialize audit manager.

        Args:
            project_dir: Path to project directory (.claude).
            global_dir: Path to global directory (~/.claude).
            reporter: Optional reporter for logging output.
            file_handler: Optional file handler with get_file_hash method.
        """
        self.project_dir = Path(project_dir)
        self.global_dir = Path(global_dir)
        self.reporter = reporter
        self.file_handler = file_handler
        self.categories = ["agents", "commands", "skills", "prompts", "hooks"]

    def audit(self) -> AuditResult:
        """Run full audit and return results.

        Scans both directories for all categories and compares files,
        detecting differences in presence and content.

        Returns:
            AuditResult with comprehensive audit findings.
        """
        result = AuditResult()

        try:
            # Audit each category
            for category in self.categories:
                category_result = self._audit_category(category)
                result.in_sync.extend(category_result["in_sync"])
                result.project_only.extend(category_result["project_only"])
                result.global_only.extend(category_result["global_only"])
                result.conflicts.extend(category_result["conflicts"])
                result.errors.extend(category_result["errors"])

            # Calculate totals
            result.total_files = (
                len(result.in_sync)
                + len(result.project_only)
                + len(result.global_only)
                + len(result.conflicts)
            )

            if result.errors:
                logger.warning(f"Audit completed with {len(result.errors)} errors")
            else:
                logger.info(f"Audit completed successfully: {result.total_files} files")

        except Exception as e:
            logger.error(f"Fatal error during audit: {e}")
            result.errors.append(f"Fatal audit error: {str(e)}")

        return result

    def _audit_category(self, category: str) -> Dict[str, List]:
        """Audit a single category.

        Args:
            category: Category name (agents, commands, skills, prompts, hooks).

        Returns:
            Dictionary with in_sync, project_only, global_only, conflicts, errors.
        """
        result = {
            "in_sync": [],
            "project_only": [],
            "global_only": [],
            "conflicts": [],
            "errors": [],
        }

        try:
            project_files = self.scan_directory(self.project_dir, category)
            global_files = self.scan_directory(self.global_dir, category)

            # Compare files
            comparison = self.compare_files(project_files, global_files, category)
            result.update(comparison)

        except Exception as e:
            error_msg = f"Error auditing {category}: {str(e)}"
            logger.error(error_msg)
            result["errors"].append(error_msg)

        return result

    def scan_directory(self, base_dir: Path, category: str) -> List[Path]:
        """Scan directory for files in a category.

        For skills: scans for SKILL.md files in subdirectories.
        For other categories: scans for .md files directly.

        Args:
            base_dir: Base directory to scan.
            category: Category name.

        Returns:
            List of file paths found in the category.
        """
        base_dir = Path(base_dir)
        category_dir = base_dir / category
        files = []

        # Handle missing category directory
        if not category_dir.exists():
            logger.debug(f"Category directory not found: {category_dir}")
            return files

        try:
            if category == "skills":
                # For skills, look for SKILL.md in subdirectories
                for skill_dir in category_dir.iterdir():
                    if skill_dir.is_dir():
                        skill_file = skill_dir / "SKILL.md"
                        if skill_file.exists():
                            files.append(skill_file)
            else:
                # For other categories, look for .md files
                for file_path in category_dir.glob("*.md"):
                    if file_path.is_file():
                        files.append(file_path)

            logger.debug(f"Found {len(files)} files in {category}")

        except Exception as e:
            logger.error(f"Error scanning {category_dir}: {e}")

        return sorted(files)

    def compare_files(
        self, project_files: List[Path], global_files: List[Path], category: str
    ) -> Dict[str, List]:
        """Compare two file lists and categorize differences.

        Args:
            project_files: Files found in project directory.
            global_files: Files found in global directory.
            category: Category name for reporting.

        Returns:
            Dictionary with categorized comparison results.
        """
        result = {
            "in_sync": [],
            "project_only": [],
            "global_only": [],
            "conflicts": [],
            "errors": [],
        }

        try:
            # Create name-based lookup
            project_map = {self.get_relative_path(f, self.project_dir): f for f in project_files}
            global_map = {self.get_relative_path(f, self.global_dir): f for f in global_files}

            # Check files in project directory
            for rel_path, project_file in project_map.items():
                if rel_path in global_map:
                    global_file = global_map[rel_path]
                    if self.files_are_identical(project_file, global_file):
                        result["in_sync"].append(rel_path)
                    else:
                        result["conflicts"].append(rel_path)
                else:
                    result["project_only"].append(rel_path)

            # Check files only in global directory
            for rel_path in global_map:
                if rel_path not in project_map:
                    result["global_only"].append(rel_path)

        except Exception as e:
            error_msg = f"Error comparing files in {category}: {str(e)}"
            logger.error(error_msg)
            result["errors"].append(error_msg)

        return result

    def files_are_identical(self, file1: Path, file2: Path) -> bool:
        """Check if two files have identical content.

        Uses hash comparison if file_handler is available, otherwise
        compares file sizes and modification times.

        Args:
            file1: First file path.
            file2: Second file path.

        Returns:
            True if files are identical, False otherwise.
        """
        file1 = Path(file1)
        file2 = Path(file2)

        # Check existence
        if not file1.exists() or not file2.exists():
            return False

        try:
            # If file_handler available, use hash comparison (most reliable)
            if self.file_handler and hasattr(self.file_handler, "get_file_hash"):
                hash1 = self.file_handler.get_file_hash(file1)
                hash2 = self.file_handler.get_file_hash(file2)
                return hash1 == hash2

            # Fallback: compare size and content
            if file1.stat().st_size != file2.stat().st_size:
                return False

            with open(file1, "rb") as f1, open(file2, "rb") as f2:
                return f1.read() == f2.read()

        except Exception as e:
            logger.error(f"Error comparing files {file1} and {file2}: {e}")
            return False

    def get_relative_path(self, file_path: Path, base_dir: Path) -> str:
        """Get relative path for display.

        Returns path relative to base_dir, handling skills specially
        to include skill name in the path.

        Args:
            file_path: Absolute file path.
            base_dir: Base directory to calculate relative path from.

        Returns:
            Relative path string for display.
        """
        file_path = Path(file_path)
        base_dir = Path(base_dir)

        try:
            relative = file_path.relative_to(base_dir)
            return str(relative)
        except ValueError:
            # Path is not relative to base_dir
            return str(file_path)

    def get_audit_statistics(self, result: AuditResult) -> Dict[str, int]:
        """Get statistics from audit result.

        Args:
            result: AuditResult from audit operation.

        Returns:
            Dictionary with audit statistics.
        """
        return {
            "total_files": result.total_files,
            "in_sync": len(result.in_sync),
            "project_only": len(result.project_only),
            "global_only": len(result.global_only),
            "conflicts": len(result.conflicts),
            "errors": len(result.errors),
            "sync_percentage": (
                (len(result.in_sync) / result.total_files * 100)
                if result.total_files > 0
                else 0
            ),
        }

    def get_audit_summary(self, result: AuditResult) -> str:
        """Get human-readable audit summary.

        Args:
            result: AuditResult from audit operation.

        Returns:
            Formatted summary string.
        """
        stats = self.get_audit_statistics(result)

        summary_lines = [
            f"Total files: {stats['total_files']}",
            f"In sync: {stats['in_sync']}",
            f"Project only: {stats['project_only']}",
            f"Global only: {stats['global_only']}",
            f"Conflicts: {stats['conflicts']}",
            f"Sync percentage: {stats['sync_percentage']:.1f}%",
        ]

        if result.errors:
            summary_lines.append(f"Errors: {stats['errors']}")

        return "\n".join(summary_lines)
