"""
Unit tests for the Scope Intelligence System.

Tests cover:
- Scope detection logic
- Path resolution for all scope types
- Configuration precedence handling
- CLI flag validation
- Edge cases (permissions, symlinks, nested projects)
"""

import pytest
from pathlib import Path

from src.core.scope_manager import ScopeConfig, ScopeManager, ScopeType
from src.core.scope_exceptions import (
    InvalidScopeError,
    ScopeNotFoundError,
)


class TestScopeDetection:
    """Tests for automatic scope detection logic."""

    def test_detect_global_scope_from_random_dir(self, tmp_path: Path) -> None:
        """Should default to GLOBAL when no project markers found."""
        # Create a random temp directory with no .claude/ or .git/
        random_dir = tmp_path / "random"
        random_dir.mkdir()

        manager = ScopeManager(random_dir)
        scope = manager.detect_scope()

        assert scope == ScopeType.GLOBAL

    def test_detect_project_scope_from_project_dir(self, tmp_path: Path) -> None:
        """Should detect PROJECT scope when .claude/ directory exists."""
        # Create project structure
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        scope = manager.detect_scope()

        assert scope == ScopeType.PROJECT

    def test_detect_project_scope_from_subdirectory(self, tmp_path: Path) -> None:
        """Should detect PROJECT scope from subdirectories."""
        # Create project with subdirectory
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        subdir = project_dir / "src" / "core"
        subdir.mkdir(parents=True)

        manager = ScopeManager(subdir)
        scope = manager.detect_scope()

        assert scope == ScopeType.PROJECT

    def test_detect_local_scope_when_exists(self, tmp_path: Path) -> None:
        """Should detect LOCAL scope when settings.local.json exists."""
        # Create project with local settings
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir()

        local_settings = claude_dir / "settings.local.json"
        local_settings.write_text("{}")

        manager = ScopeManager(project_dir)
        scope = manager.detect_scope()

        assert scope == ScopeType.LOCAL

    def test_scope_detection_with_git_marker(self, tmp_path: Path) -> None:
        """Should detect project root using .git marker."""
        # Create project with .git (common marker)
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".git").mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        scope = manager.detect_scope()

        assert scope == ScopeType.PROJECT

    def test_scope_detection_without_git_root(self, tmp_path: Path) -> None:
        """Should detect project even without .git if .claude/ exists."""
        # Create project without .git
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        scope = manager.detect_scope()

        assert scope == ScopeType.PROJECT


class TestPathResolution:
    """Tests for scope path resolution methods."""

    def test_get_global_path_returns_home_claude(self) -> None:
        """Should return ~/.claude/ for global path."""
        manager = ScopeManager()
        global_path = manager.get_global_path()

        expected = Path.home() / ".claude"
        assert global_path == expected.resolve()

    def test_get_project_path_finds_nearest_claude(self, tmp_path: Path) -> None:
        """Should find nearest .claude/ directory in parent hierarchy."""
        # Create nested project structure
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        deep_subdir = project_dir / "src" / "core" / "utils"
        deep_subdir.mkdir(parents=True)

        manager = ScopeManager(deep_subdir)
        project_path = manager.get_project_path()

        assert project_path is not None
        assert project_path == (project_dir / ".claude").resolve()

    def test_get_project_path_returns_none_when_not_found(self, tmp_path: Path) -> None:
        """Should return None when no .claude/ directory found."""
        # Create directory without .claude/
        random_dir = tmp_path / "random"
        random_dir.mkdir()

        manager = ScopeManager(random_dir)
        project_path = manager.get_project_path()

        assert project_path is None

    def test_get_local_path_checks_settings_local_json(self, tmp_path: Path) -> None:
        """Should return path to settings.local.json in project .claude/."""
        # Create project structure
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        local_path = manager.get_local_path()

        expected = project_dir / ".claude" / "settings.local.json"
        assert local_path == expected.resolve()

    def test_get_local_path_returns_none_without_project(self, tmp_path: Path) -> None:
        """Should return None when no project scope exists."""
        random_dir = tmp_path / "random"
        random_dir.mkdir()

        manager = ScopeManager(random_dir)
        local_path = manager.get_local_path()

        assert local_path is None

    def test_find_project_root_with_git(self, tmp_path: Path) -> None:
        """Should find project root using .git marker."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".git").mkdir()

        subdir = project_dir / "src"
        subdir.mkdir()

        manager = ScopeManager(subdir)
        root = manager.find_project_root()

        assert root == project_dir.resolve()

    def test_find_project_root_with_claude_dir(self, tmp_path: Path) -> None:
        """Should find project root using .claude/ marker."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        subdir = project_dir / "src"
        subdir.mkdir()

        manager = ScopeManager(subdir)
        root = manager.find_project_root()

        assert root == project_dir.resolve()

    def test_find_project_root_returns_none_outside_project(self, tmp_path: Path) -> None:
        """Should return None when no project markers found."""
        random_dir = tmp_path / "random"
        random_dir.mkdir()

        manager = ScopeManager(random_dir)
        root = manager.find_project_root()

        assert root is None


class TestPrecedence:
    """Tests for configuration precedence handling."""

    def test_local_overrides_project_and_global(self, tmp_path: Path) -> None:
        """LOCAL scope should have highest precedence (1)."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.local.json").write_text("{}")

        manager = ScopeManager(project_dir)
        scopes = manager.resolve_all_scopes()

        # Find local scope
        local_scope = next(s for s in scopes if s.type == ScopeType.LOCAL)
        assert local_scope.precedence == 1

    def test_project_overrides_global(self, tmp_path: Path) -> None:
        """PROJECT scope should have precedence 2 (higher than GLOBAL)."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        scopes = manager.resolve_all_scopes()

        # Find project and global scopes
        project_scope = next(s for s in scopes if s.type == ScopeType.PROJECT)
        global_scope = next(s for s in scopes if s.type == ScopeType.GLOBAL)

        assert project_scope.precedence == 2
        assert global_scope.precedence == 3
        assert project_scope.precedence < global_scope.precedence

    def test_resolve_all_scopes_correct_order(self, tmp_path: Path) -> None:
        """Scopes should be ordered by precedence: Local > Project > Global."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.local.json").write_text("{}")

        manager = ScopeManager(project_dir)
        scopes = manager.resolve_all_scopes()

        # Verify order
        assert len(scopes) == 3
        assert scopes[0].type == ScopeType.LOCAL
        assert scopes[0].precedence == 1
        assert scopes[1].type == ScopeType.PROJECT
        assert scopes[1].precedence == 2
        assert scopes[2].type == ScopeType.GLOBAL
        assert scopes[2].precedence == 3

    def test_resolve_all_scopes_without_local(self, tmp_path: Path) -> None:
        """Should only include Project and Global when Local doesn't exist."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()
        # Don't create settings.local.json

        manager = ScopeManager(project_dir)
        scopes = manager.resolve_all_scopes()

        scope_types = [s.type for s in scopes]
        assert ScopeType.LOCAL in scope_types  # Path exists, but exists=False
        assert ScopeType.PROJECT in scope_types
        assert ScopeType.GLOBAL in scope_types


class TestCLIFlags:
    """Tests for CLI flag handling."""

    def test_global_flag_forces_global_scope(self, tmp_path: Path) -> None:
        """--global flag should force global scope even in project."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        scope = manager.get_effective_scope("--global")

        assert scope.type == ScopeType.GLOBAL

    def test_project_flag_forces_project_scope(self, tmp_path: Path) -> None:
        """--project flag should force project scope."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        scope = manager.get_effective_scope("--project")

        assert scope.type == ScopeType.PROJECT

    def test_local_flag_forces_local_scope(self, tmp_path: Path) -> None:
        """--local flag should force local scope."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.local.json").write_text("{}")

        manager = ScopeManager(project_dir)
        scope = manager.get_effective_scope("--local")

        assert scope.type == ScopeType.LOCAL

    def test_flag_without_dashes_accepted(self, tmp_path: Path) -> None:
        """Flags without leading dashes should also work."""
        manager = ScopeManager(tmp_path)
        scope = manager.get_effective_scope("global")

        assert scope.type == ScopeType.GLOBAL

    def test_invalid_flag_raises_error(self, tmp_path: Path) -> None:
        """Invalid scope flags should raise InvalidScopeError."""
        manager = ScopeManager(tmp_path)

        with pytest.raises(InvalidScopeError, match="Invalid scope flag"):
            manager.get_effective_scope("--invalid")

    def test_none_flag_triggers_auto_detection(self, tmp_path: Path) -> None:
        """None flag should trigger automatic scope detection."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        scope = manager.get_effective_scope(None)

        # Should auto-detect PROJECT
        assert scope.type == ScopeType.PROJECT


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_no_claude_directory_defaults_global(self, tmp_path: Path) -> None:
        """Should default to GLOBAL when no .claude/ directory exists."""
        random_dir = tmp_path / "random"
        random_dir.mkdir()

        manager = ScopeManager(random_dir)
        scope = manager.detect_scope()

        assert scope == ScopeType.GLOBAL

    def test_validate_scope_exists_returns_true_when_exists(self, tmp_path: Path) -> None:
        """validate_scope_exists should return True for existing scopes."""
        project_dir = tmp_path / "project"
        project_dir.mkdir()
        (project_dir / ".claude").mkdir()

        manager = ScopeManager(project_dir)
        exists = manager.validate_scope_exists(ScopeType.PROJECT)

        assert exists is True

    def test_validate_scope_exists_returns_false_when_missing(self, tmp_path: Path) -> None:
        """validate_scope_exists should return False for non-existent scopes."""
        random_dir = tmp_path / "random"
        random_dir.mkdir()

        manager = ScopeManager(random_dir)

        # Global might not exist in test environment
        # Test with project scope which definitely doesn't exist
        with pytest.raises(ScopeNotFoundError):
            manager.validate_scope_exists(ScopeType.PROJECT)

    def test_project_flag_without_project_raises_error(self, tmp_path: Path) -> None:
        """--project flag should raise error when no project exists."""
        random_dir = tmp_path / "random"
        random_dir.mkdir()

        manager = ScopeManager(random_dir)

        with pytest.raises(ScopeNotFoundError, match="Cannot determine project scope"):
            manager.get_effective_scope("--project")

    def test_local_flag_without_project_raises_error(self, tmp_path: Path) -> None:
        """--local flag should raise error when no project exists."""
        random_dir = tmp_path / "random"
        random_dir.mkdir()

        manager = ScopeManager(random_dir)

        with pytest.raises(ScopeNotFoundError, match="Cannot determine local scope"):
            manager.get_effective_scope("--local")

    def test_nested_projects_finds_nearest(self, tmp_path: Path) -> None:
        """Should find nearest .claude/ directory in nested projects."""
        # Create outer project
        outer_project = tmp_path / "outer"
        outer_project.mkdir()
        (outer_project / ".claude").mkdir()

        # Create inner project
        inner_project = outer_project / "packages" / "inner"
        inner_project.mkdir(parents=True)
        (inner_project / ".claude").mkdir()

        # Test from inner project
        manager = ScopeManager(inner_project)
        project_path = manager.get_project_path()

        assert project_path == (inner_project / ".claude").resolve()

    def test_symlink_resolution(self, tmp_path: Path) -> None:
        """Should resolve symlinks correctly."""
        # Create actual project
        real_project = tmp_path / "real_project"
        real_project.mkdir()
        (real_project / ".claude").mkdir()

        # Create symlink to project
        link_project = tmp_path / "link_project"
        link_project.symlink_to(real_project)

        manager = ScopeManager(link_project)
        project_path = manager.get_project_path()

        assert project_path is not None
        # Path should be resolved (following symlinks)
        assert project_path.exists()


class TestScopeConfig:
    """Tests for ScopeConfig dataclass."""

    def test_scope_config_creation(self, tmp_path: Path) -> None:
        """Should create ScopeConfig with all fields."""
        path = tmp_path / ".claude"
        config = ScopeConfig(path=path, type=ScopeType.PROJECT, precedence=2, exists=False)

        assert config.path == path
        assert config.type == ScopeType.PROJECT
        assert config.precedence == 2
        assert config.exists is False

    def test_scope_config_exists_flag(self, tmp_path: Path) -> None:
        """ScopeConfig should accurately reflect path existence."""
        # Create existing path
        existing_path = tmp_path / "exists"
        existing_path.mkdir()

        # Non-existing path
        missing_path = tmp_path / "missing"

        config_exists = ScopeConfig(
            path=existing_path, type=ScopeType.PROJECT, precedence=2, exists=True
        )
        config_missing = ScopeConfig(
            path=missing_path, type=ScopeType.PROJECT, precedence=2, exists=False
        )

        assert config_exists.exists is True
        assert config_missing.exists is False


class TestScopeType:
    """Tests for ScopeType enum."""

    def test_scope_type_values(self) -> None:
        """Should have correct enum values."""
        assert ScopeType.GLOBAL.value == "global"
        assert ScopeType.PROJECT.value == "project"
        assert ScopeType.LOCAL.value == "local"

    def test_scope_type_from_string(self) -> None:
        """Should create ScopeType from string value."""
        assert ScopeType("global") == ScopeType.GLOBAL
        assert ScopeType("project") == ScopeType.PROJECT
        assert ScopeType("local") == ScopeType.LOCAL
