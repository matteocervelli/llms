"""File handling module with safety features, backups, and validation."""

import hashlib
import logging
from datetime import datetime
from pathlib import Path
from shutil import copy2, copytree, rmtree
from typing import Optional, Set

logger = logging.getLogger(__name__)

# Patterns to exclude when copying directories
EXCLUDE_PATTERNS: Set[str] = {
    ".DS_Store",
    "__pycache__",
    ".git",
    "*.pyc",
    ".pytest_cache",
    ".coverage",
    "*.egg-info",
}


class FileHandler:
    """Handle file operations with automatic backups and validation."""

    def __init__(self, backup_enabled: bool = True) -> None:
        """
        Initialize file handler with backup configuration.

        Args:
            backup_enabled: Whether to create backups before operations.
        """
        self.backup_enabled = backup_enabled
        self.backup_base = Path.home() / ".claude" / ".backups"
        self.operations_log: list[dict] = []

    def copy_file(self, source: Path, dest: Path, create_backup: bool = True) -> bool:
        """
        Copy a single file with optional backup.

        Args:
            source: Source file path.
            dest: Destination file path.
            create_backup: Whether to create backup of destination if it exists.

        Returns:
            True if copy was successful, False otherwise.

        Raises:
            FileNotFoundError: If source file doesn't exist.
        """
        source = Path(source)
        dest = Path(dest)

        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {source}")

        if not source.is_file():
            raise ValueError(f"Source is not a file: {source}")

        try:
            # Create backup if destination exists and backup is enabled
            if dest.exists() and self.backup_enabled and create_backup:
                self.create_backup(dest)

            # Ensure destination directory exists
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Copy file preserving metadata
            copy2(source, dest)

            # Validate the copy
            if not self.validate_copy(source, dest):
                logger.error(f"Copy validation failed: {source} -> {dest}")
                return False

            self.operations_log.append(
                {
                    "operation": "copy_file",
                    "source": str(source),
                    "dest": str(dest),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                }
            )

            logger.info(f"Successfully copied file: {source} -> {dest}")
            return True

        except Exception as e:
            logger.error(f"Failed to copy file {source} to {dest}: {e}")
            return False

    def copy_directory(
        self, source: Path, dest: Path, create_backup: bool = True
    ) -> bool:
        """
        Copy entire directory with optional backup (for skills).

        Args:
            source: Source directory path.
            dest: Destination directory path.
            create_backup: Whether to create backup of destination if it exists.

        Returns:
            True if copy was successful, False otherwise.

        Raises:
            NotADirectoryError: If source is not a directory.
        """
        source = Path(source)
        dest = Path(dest)

        if not source.is_dir():
            raise NotADirectoryError(f"Source is not a directory: {source}")

        try:
            # Create backup if destination exists and backup is enabled
            if dest.exists() and self.backup_enabled and create_backup:
                self.create_backup(dest)

            # Remove destination if it exists
            if dest.exists():
                rmtree(dest)

            # Copy directory with exclusion
            def ignore_patterns(directory: str, files: list[str]) -> Set[str]:
                """Return set of files/dirs to ignore during copy."""
                ignored = set()
                for file in files:
                    if any(
                        file == pattern.replace("*", "")
                        or file.endswith(pattern.replace("*", ""))
                        for pattern in EXCLUDE_PATTERNS
                    ):
                        ignored.add(file)
                return ignored

            copytree(source, dest, ignore=ignore_patterns)

            self.operations_log.append(
                {
                    "operation": "copy_directory",
                    "source": str(source),
                    "dest": str(dest),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                }
            )

            logger.info(f"Successfully copied directory: {source} -> {dest}")
            return True

        except Exception as e:
            logger.error(f"Failed to copy directory {source} to {dest}: {e}")
            return False

    def create_backup(self, file_path: Path) -> Path:
        """
        Create timestamped backup of a file or directory.

        Args:
            file_path: Path to file or directory to backup.

        Returns:
            Path to the backup location.

        Raises:
            FileNotFoundError: If file_path doesn't exist.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Path not found: {file_path}")

        # Create timestamped backup directory
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        backup_dir = self.backup_base / timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Create backup
        backup_path = backup_dir / file_path.name

        try:
            if file_path.is_file():
                copy2(file_path, backup_path)
            else:
                copytree(file_path, backup_path)

            self.operations_log.append(
                {
                    "operation": "create_backup",
                    "source": str(file_path),
                    "backup": str(backup_path),
                    "timestamp": datetime.now().isoformat(),
                    "status": "success",
                }
            )

            logger.info(f"Backup created: {file_path} -> {backup_path}")
            return backup_path

        except Exception as e:
            logger.error(f"Failed to create backup for {file_path}: {e}")
            raise

    def validate_copy(self, source: Path, dest: Path) -> bool:
        """
        Validate copied file matches source (hash comparison).

        Args:
            source: Source file path.
            dest: Destination file path.

        Returns:
            True if hashes match, False otherwise.
        """
        source = Path(source)
        dest = Path(dest)

        if not source.exists() or not dest.exists():
            return False

        try:
            source_hash = self.get_file_hash(source)
            dest_hash = self.get_file_hash(dest)
            return source_hash == dest_hash
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return False

    def should_exclude(self, path: Path) -> bool:
        """
        Check if path matches exclusion patterns.

        Args:
            path: Path to check.

        Returns:
            True if path should be excluded, False otherwise.
        """
        path_str = str(path)
        return any(
            pattern.replace("*", "") in path_str
            or path_str.endswith(pattern.replace("*", ""))
            for pattern in EXCLUDE_PATTERNS
        )

    def get_file_hash(self, file_path: Path) -> str:
        """
        Get SHA256 hash of file for validation.

        Args:
            file_path: Path to file.

        Returns:
            Hex digest of file hash.

        Raises:
            FileNotFoundError: If file doesn't exist.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        hash_sha256 = hashlib.sha256()

        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Failed to hash file {file_path}: {e}")
            raise

    def get_operations_log(self) -> list[dict]:
        """
        Get log of all operations for audit/rollback.

        Returns:
            List of operation records.
        """
        return self.operations_log.copy()

    def clear_operations_log(self) -> None:
        """Clear the operations log."""
        self.operations_log.clear()
