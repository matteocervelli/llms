"""
Scope Intelligence System

Manages Claude Code's three-tier scope system (global/project/local) with automatic
detection and intelligent precedence handling.

Scope Types:
    - GLOBAL: ~/.claude/ (user-wide, all projects)
    - PROJECT: .claude/ (project-specific, team-shared)
    - LOCAL: .claude/settings.local.json (project-local, not committed)

Configuration Precedence: Local > Project > Global

Example Usage:
    >>> from pathlib import Path
    >>> from src.core.scope_manager import ScopeManager, ScopeType
    >>>
    >>> # Auto-detect scope
    >>> manager = ScopeManager()
    >>> scope = manager.detect_scope()
    >>> print(f"Detected scope: {scope}")
    >>>
    >>> # Get effective scope with CLI flag
    >>> scope_config = manager.get_effective_scope('--project')
    >>> print(f"Using path: {scope_config.path}")
    >>>
    >>> # Resolve all scopes with precedence
    >>> all_scopes = manager.resolve_all_scopes()
    >>> for scope in all_scopes:
    ...     print(f"{scope.type.value}: {scope.path} (precedence: {scope.precedence})")
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional

from .scope_exceptions import (
    InvalidScopeError,
    ScopeNotFoundError,
)


class ScopeType(Enum):
    """Enumeration of supported scope types.

    Attributes:
        GLOBAL: User-wide scope (~/.claude/)
        PROJECT: Project-specific scope (.claude/)
        LOCAL: Project-local scope (.claude/settings.local.json)
    """

    GLOBAL = "global"
    PROJECT = "project"
    LOCAL = "local"


@dataclass
class ScopeConfig:
    """Configuration metadata for a scope.

    Attributes:
        path: Path to the scope directory or file
        type: Type of scope (GLOBAL, PROJECT, or LOCAL)
        precedence: Priority order (1=highest, 3=lowest)
        exists: Whether the scope path currently exists on filesystem
    """

    path: Path
    type: ScopeType
    precedence: int
    exists: bool


class ScopeManager:
    """Manages scope detection, resolution, and configuration precedence.

    The ScopeManager provides intelligent scope detection based on the current
    working directory and supports explicit scope selection via CLI flags.

    Attributes:
        cwd: Current working directory (defaults to Path.cwd())
    """

    # Class constants
    GLOBAL_DIR_NAME = ".claude"
    PROJECT_DIR_NAME = ".claude"
    LOCAL_FILE_NAME = "settings.local.json"
    PROJECT_MARKERS = [".git", ".claude"]

    def __init__(self, cwd: Optional[Path] = None) -> None:
        """Initialize the ScopeManager.

        Args:
            cwd: Current working directory. Defaults to Path.cwd() if not provided.

        Examples:
            >>> manager = ScopeManager()  # Uses current directory
            >>> manager = ScopeManager(Path("/path/to/project"))  # Explicit path
        """
        self.cwd = (cwd or Path.cwd()).resolve()

    def detect_scope(self) -> ScopeType:
        """Automatically detect the appropriate scope based on current directory.

        Detection logic:
        1. Check for local scope (.claude/settings.local.json in project)
        2. Check for project scope (.claude/ in current or parent directories)
        3. Default to global scope (~/.claude/)

        Returns:
            ScopeType: The detected scope type (LOCAL, PROJECT, or GLOBAL)

        Examples:
            >>> manager = ScopeManager(Path("/home/user/project"))
            >>> scope = manager.detect_scope()
            >>> print(scope)
            ScopeType.PROJECT
        """
        # Check for local scope first (highest precedence)
        local_path = self.get_local_path()
        if local_path and local_path.exists():
            return ScopeType.LOCAL

        # Check for project scope
        project_path = self.get_project_path()
        if project_path:
            return ScopeType.PROJECT

        # Default to global scope
        return ScopeType.GLOBAL

    def get_global_path(self) -> Path:
        """Get the global scope path (~/.claude/).

        Returns:
            Path: Resolved path to the global Claude configuration directory

        Examples:
            >>> manager = ScopeManager()
            >>> global_path = manager.get_global_path()
            >>> print(global_path)
            PosixPath('/home/user/.claude')
        """
        return (Path.home() / self.GLOBAL_DIR_NAME).resolve()

    def get_project_path(self) -> Optional[Path]:
        """Find the nearest project scope path (.claude/ in current or parent dirs).

        Searches upward from the current working directory until finding a .claude/
        directory or reaching the filesystem root.

        Returns:
            Optional[Path]: Path to project .claude/ directory, or None if not found

        Examples:
            >>> manager = ScopeManager(Path("/home/user/project/src"))
            >>> project_path = manager.get_project_path()
            >>> print(project_path)
            PosixPath('/home/user/project/.claude')
        """
        project_root = self.find_project_root()
        if not project_root:
            return None

        project_claude_dir = project_root / self.PROJECT_DIR_NAME
        if project_claude_dir.exists() and project_claude_dir.is_dir():
            return project_claude_dir.resolve()

        return None

    def get_local_path(self) -> Optional[Path]:
        """Get the local scope path (.claude/settings.local.json).

        Returns:
            Optional[Path]: Path to settings.local.json file, or None if project not found

        Examples:
            >>> manager = ScopeManager(Path("/home/user/project"))
            >>> local_path = manager.get_local_path()
            >>> print(local_path)
            PosixPath('/home/user/project/.claude/settings.local.json')
        """
        project_path = self.get_project_path()
        if not project_path:
            return None

        return (project_path / self.LOCAL_FILE_NAME).resolve()

    def find_project_root(self) -> Optional[Path]:
        """Locate the project root directory.

        Searches upward from current directory for project markers (.git or .claude/).
        Stops at filesystem root if no markers found.

        Returns:
            Optional[Path]: Path to project root, or None if not in a project

        Examples:
            >>> manager = ScopeManager(Path("/home/user/project/src/core"))
            >>> root = manager.find_project_root()
            >>> print(root)
            PosixPath('/home/user/project')
        """
        current = self.cwd
        root = Path(current.root)

        # Traverse upward looking for project markers
        while current != root:
            for marker in self.PROJECT_MARKERS:
                marker_path = current / marker
                if marker_path.exists():
                    return current.resolve()

            # Move to parent directory
            current = current.parent

        # Check root directory as well
        for marker in self.PROJECT_MARKERS:
            if (root / marker).exists():
                return root.resolve()

        return None

    def resolve_all_scopes(self) -> List[ScopeConfig]:
        """Resolve all applicable scopes with correct precedence.

        Returns scopes in precedence order: Local (1) > Project (2) > Global (3)

        Returns:
            List[ScopeConfig]: Ordered list of scope configurations

        Examples:
            >>> manager = ScopeManager()
            >>> scopes = manager.resolve_all_scopes()
            >>> for scope in scopes:
            ...     print(f"{scope.type.value}: precedence {scope.precedence}")
            local: precedence 1
            project: precedence 2
            global: precedence 3
        """
        scopes: List[ScopeConfig] = []

        # Local scope (precedence 1)
        local_path = self.get_local_path()
        if local_path:
            scopes.append(
                ScopeConfig(
                    path=local_path,
                    type=ScopeType.LOCAL,
                    precedence=1,
                    exists=local_path.exists(),
                )
            )

        # Project scope (precedence 2)
        project_path = self.get_project_path()
        if project_path:
            scopes.append(
                ScopeConfig(
                    path=project_path,
                    type=ScopeType.PROJECT,
                    precedence=2,
                    exists=project_path.exists(),
                )
            )

        # Global scope (precedence 3, always available)
        global_path = self.get_global_path()
        scopes.append(
            ScopeConfig(
                path=global_path,
                type=ScopeType.GLOBAL,
                precedence=3,
                exists=global_path.exists(),
            )
        )

        return scopes

    def get_effective_scope(self, flag: Optional[str] = None) -> ScopeConfig:
        """Get the effective scope based on CLI flag or auto-detection.

        Args:
            flag: Optional CLI flag ('global', 'project', 'local', '--global',
                  '--project', '--local'). If None, auto-detects scope.

        Returns:
            ScopeConfig: The effective scope configuration to use

        Raises:
            InvalidScopeError: If an invalid scope flag is provided
            ScopeNotFoundError: If the requested scope doesn't exist
            MultipleScopeFlagsError: If multiple flags are provided (handled by caller)

        Examples:
            >>> manager = ScopeManager()
            >>> scope = manager.get_effective_scope('--project')
            >>> print(f"Using {scope.type.value} at {scope.path}")
            Using project at /home/user/project/.claude
        """
        # Auto-detect if no flag provided
        if flag is None:
            scope_type = self.detect_scope()
            return self._get_scope_config(scope_type)

        # Normalize flag (remove leading dashes)
        normalized_flag = flag.lstrip("-").lower()

        # Validate flag
        valid_flags = {e.value for e in ScopeType}
        if normalized_flag not in valid_flags:
            raise InvalidScopeError(
                f"Invalid scope flag: '{flag}'. Must be one of: "
                f"{', '.join('--' + f for f in valid_flags)}"
            )

        # Convert flag to ScopeType
        scope_type = ScopeType(normalized_flag)

        # Get and validate scope configuration
        scope_config = self._get_scope_config(scope_type)

        # Validate that the scope exists (except global, which we can create)
        if not scope_config.exists and scope_type != ScopeType.GLOBAL:
            raise ScopeNotFoundError(
                f"{scope_type.value.capitalize()} scope not found. "
                f"Expected at: {scope_config.path}"
            )

        return scope_config

    def validate_scope_exists(self, scope_type: ScopeType) -> bool:
        """Check if a specific scope exists on the filesystem.

        Args:
            scope_type: The scope type to validate

        Returns:
            bool: True if the scope exists, False otherwise

        Examples:
            >>> manager = ScopeManager()
            >>> exists = manager.validate_scope_exists(ScopeType.PROJECT)
            >>> print(f"Project scope exists: {exists}")
            Project scope exists: True
        """
        scope_config = self._get_scope_config(scope_type)
        return scope_config.exists

    def _get_scope_config(self, scope_type: ScopeType) -> ScopeConfig:
        """Internal helper to get scope configuration for a given type.

        Args:
            scope_type: The scope type to get configuration for

        Returns:
            ScopeConfig: Configuration for the requested scope

        Raises:
            ScopeNotFoundError: If project/local scope cannot be determined
        """
        if scope_type == ScopeType.GLOBAL:
            global_path = self.get_global_path()
            return ScopeConfig(
                path=global_path, type=scope_type, precedence=3, exists=global_path.exists()
            )

        elif scope_type == ScopeType.PROJECT:
            project_path: Optional[Path] = self.get_project_path()
            if project_path is None:
                raise ScopeNotFoundError(
                    "Cannot determine project scope: no .claude/ directory found in "
                    "current directory or parents"
                )
            return ScopeConfig(
                path=project_path, type=scope_type, precedence=2, exists=project_path.exists()
            )

        elif scope_type == ScopeType.LOCAL:
            local_path: Optional[Path] = self.get_local_path()
            if local_path is None:
                raise ScopeNotFoundError(
                    "Cannot determine local scope: no project root found for local settings"
                )
            return ScopeConfig(
                path=local_path, type=scope_type, precedence=1, exists=local_path.exists()
            )

        else:
            raise InvalidScopeError(f"Unknown scope type: {scope_type}")


# Public API for easy imports
__all__ = [
    "ScopeType",
    "ScopeConfig",
    "ScopeManager",
]
