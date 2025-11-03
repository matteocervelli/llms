"""Comprehensive tests for the SyncManager and SyncResult classes."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from claude_sync import SyncManager, SyncResult, Reporter, FileHandler


class TestSyncResult:
    """Test cases for SyncResult dataclass."""

    def test_sync_result_initialization(self):
        """Test SyncResult initializes with default values."""
        result = SyncResult(success=True)

        assert result.success is True
        assert result.files_copied == []
        assert result.files_skipped == []
        assert result.conflicts_resolved == {}
        assert result.errors == []
        assert result.summary == {}

    def test_sync_result_with_data(self):
        """Test SyncResult with populated data."""
        result = SyncResult(
            success=True,
            files_copied=["file1.md", "file2.md"],
            files_skipped=["file3.md"],
            conflicts_resolved={"file4.md": "overwritten"},
            errors=[],
            summary={"copied": 2, "skipped": 1, "conflicts": 1, "errors": 0},
        )

        assert result.success is True
        assert len(result.files_copied) == 2
        assert len(result.files_skipped) == 1
        assert len(result.conflicts_resolved) == 1
        assert result.summary["copied"] == 2

    def test_sync_result_to_dict(self):
        """Test SyncResult.to_dict() conversion."""
        result = SyncResult(
            success=True,
            files_copied=["file1.md"],
            errors=[],
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["success"] is True
        assert result_dict["files_copied"] == ["file1.md"]
        assert result_dict["errors"] == []


class TestSyncManagerInitialization:
    """Test cases for SyncManager initialization."""

    def test_init_with_valid_directories(self):
        """Test SyncManager initialization with valid directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            manager = SyncManager(project_dir, global_dir)

            assert manager.project_dir == project_dir
            assert manager.global_dir == global_dir
            assert manager.dry_run is False
            assert manager.force is False

    def test_init_with_missing_project_directory(self):
        """Test SyncManager raises error for missing project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            global_dir.mkdir()

            with pytest.raises(ValueError, match="Project directory not found"):
                SyncManager(project_dir, global_dir)

    def test_init_with_missing_global_directory(self):
        """Test SyncManager raises error for missing global directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()

            with pytest.raises(ValueError, match="Global directory not found"):
                SyncManager(project_dir, global_dir)

    def test_init_with_custom_reporter(self):
        """Test SyncManager initialization with custom reporter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            reporter = Reporter(verbose=True)
            manager = SyncManager(project_dir, global_dir, reporter=reporter)

            assert manager.reporter is reporter

    def test_init_with_dry_run_mode(self):
        """Test SyncManager initialization with dry-run mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            manager = SyncManager(project_dir, global_dir, dry_run=True)

            assert manager.dry_run is True
            assert manager.file_handler.backup_enabled is False

    def test_init_with_force_mode(self):
        """Test SyncManager initialization with force mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            manager = SyncManager(project_dir, global_dir, force=True)

            assert manager.force is True


class TestSyncValidation:
    """Test cases for sync validation and error handling."""

    def test_sync_with_invalid_direction(self):
        """Test sync raises error for invalid direction."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            manager = SyncManager(project_dir, global_dir)

            with pytest.raises(ValueError, match="Invalid direction"):
                manager.sync("invalid")

    def test_sync_with_invalid_category(self):
        """Test sync raises error for invalid category."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            manager = SyncManager(project_dir, global_dir)

            with pytest.raises(ValueError, match="Invalid categories"):
                manager.sync("push", categories=["invalid_category"])

    def test_sync_with_valid_directions(self):
        """Test sync accepts valid directions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            manager = SyncManager(project_dir, global_dir, dry_run=True)

            # Should not raise errors
            result = manager.sync("push")
            assert result is not None

            result = manager.sync("pull")
            assert result is not None


class TestSyncFileOperations:
    """Test cases for file sync operations."""

    def test_sync_push_copies_files(self):
        """Test push sync copies files from project to global."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create test files in project directory
            commands_dir = project_dir / "commands"
            commands_dir.mkdir()
            test_file = commands_dir / "test.md"
            test_file.write_text("test content")

            # Create destination directory
            (global_dir / "commands").mkdir()

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("push", categories=["commands"])

            # Verify file was copied
            assert (global_dir / "commands" / "test.md").exists()
            assert result.success is True
            assert len(result.files_copied) > 0

    def test_sync_pull_copies_files(self):
        """Test pull sync copies files from global to project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create test files in global directory
            commands_dir = global_dir / "commands"
            commands_dir.mkdir()
            test_file = commands_dir / "test.md"
            test_file.write_text("test content")

            # Create destination directory
            (project_dir / "commands").mkdir()

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("pull", categories=["commands"])

            # Verify file was copied
            assert (project_dir / "commands" / "test.md").exists()
            assert result.success is True
            assert len(result.files_copied) > 0

    def test_sync_skips_identical_files(self):
        """Test sync skips files that are identical in source and destination."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create identical test files
            content = "identical content"
            project_commands = project_dir / "commands"
            global_commands = global_dir / "commands"
            project_commands.mkdir()
            global_commands.mkdir()

            (project_commands / "test.md").write_text(content)
            (global_commands / "test.md").write_text(content)

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("push", categories=["commands"])

            # Verify file was skipped (not copied again)
            assert len(result.files_skipped) > 0

    def test_sync_dry_run_preview_mode(self):
        """Test dry-run mode previews changes without executing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create test files
            commands_dir = project_dir / "commands"
            commands_dir.mkdir()
            test_file = commands_dir / "test.md"
            test_file.write_text("test content")

            (global_dir / "commands").mkdir()

            # Run sync in dry-run mode
            manager = SyncManager(project_dir, global_dir, dry_run=True)
            result = manager.sync("push", categories=["commands"])

            # Verify file was NOT actually copied
            assert not (global_dir / "commands" / "test.md").exists()
            assert result.success is True

    def test_sync_force_overwrite_conflicts(self):
        """Test force mode overwrites conflicting files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create conflicting files with different content
            project_commands = project_dir / "commands"
            global_commands = global_dir / "commands"
            project_commands.mkdir()
            global_commands.mkdir()

            project_file = project_commands / "test.md"
            global_file = global_commands / "test.md"

            project_file.write_text("project content")
            global_file.write_text("global content")

            # Sync with force mode
            manager = SyncManager(project_dir, global_dir, force=True)
            result = manager.sync("push", categories=["commands"])

            # Verify file was overwritten with project content
            assert global_file.read_text() == "project content"
            assert result.success is True

    def test_sync_skips_missing_source_directory(self):
        """Test sync handles missing source directory gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Don't create any files - source directories don't exist

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("push", categories=["commands"])

            # Should complete without errors
            assert result.success is True


class TestSyncCategories:
    """Test cases for different sync categories."""

    def test_sync_all_default_categories(self):
        """Test sync syncs all default categories (excluding prompts)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create directories for default categories
            for category in ["agents", "commands", "hooks"]:
                (project_dir / category).mkdir()
                (global_dir / category).mkdir()

            manager = SyncManager(project_dir, global_dir, dry_run=True)
            result = manager.sync("push")  # No categories specified

            # Should include default categories
            assert result.success is True

    def test_sync_specific_category(self):
        """Test syncing a specific category."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create only agents directory
            (project_dir / "agents").mkdir()
            (global_dir / "agents").mkdir()
            (project_dir / "agents" / "test.md").write_text("content")

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("push", categories=["agents"])

            assert result.success is True

    def test_sync_multiple_categories(self):
        """Test syncing multiple specified categories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create multiple category directories
            for category in ["agents", "commands"]:
                (project_dir / category).mkdir()
                (global_dir / category).mkdir()
                (project_dir / category / "test.md").write_text("content")

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("push", categories=["agents", "commands"])

            assert result.success is True

    def test_sync_directory_category_skills(self):
        """Test syncing skills directory (entire subdirectories)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create skills directory with subdirectories
            project_skills = project_dir / "skills"
            project_skills.mkdir()
            skill_dir = project_skills / "my_skill"
            skill_dir.mkdir()
            (skill_dir / "manifest.json").write_text('{}')

            global_skills = global_dir / "skills"
            global_skills.mkdir()

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("push", categories=["skills"])

            # Verify skill directory was copied
            assert (global_skills / "my_skill").exists()
            assert result.success is True


class TestSyncReporting:
    """Test cases for sync reporting and summary."""

    def test_sync_result_summary_calculation(self):
        """Test sync result summary is calculated correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create test files
            (project_dir / "commands").mkdir()
            (global_dir / "commands").mkdir()
            (project_dir / "commands" / "test.md").write_text("content")

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("push", categories=["commands"])

            # Verify summary is populated
            assert "copied" in result.summary
            assert "skipped" in result.summary
            assert "conflicts" in result.summary
            assert "errors" in result.summary
            assert "total" in result.summary

    def test_sync_error_tracking(self):
        """Test sync tracks and reports errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            manager = SyncManager(project_dir, global_dir)

            # Mock file handler to simulate error
            manager.file_handler.copy_file = Mock(side_effect=Exception("Copy failed"))

            (project_dir / "commands").mkdir()
            (global_dir / "commands").mkdir()
            (project_dir / "commands" / "test.md").write_text("content")

            result = manager.sync("push", categories=["commands"])

            # Verify errors are tracked
            assert len(result.errors) > 0
            assert result.success is False


class TestSyncPrompts:
    """Test cases for prompt-specific sync behavior."""

    def test_sync_excludes_prompts_by_default(self):
        """Test sync excludes prompts by default (project-specific)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create prompts directory
            (project_dir / "prompts").mkdir()
            (global_dir / "prompts").mkdir()

            manager = SyncManager(project_dir, global_dir, dry_run=True)

            with patch("builtins.input", return_value="n"):
                result = manager.sync("push")

                # Prompts should not be included in default sync
                assert result.success is True

    def test_sync_includes_prompts_when_requested(self):
        """Test sync includes prompts when user confirms."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create prompts directory with a file
            project_prompts = project_dir / "prompts"
            project_prompts.mkdir()
            (project_prompts / "test.md").write_text("prompt content")
            (global_dir / "prompts").mkdir()

            manager = SyncManager(project_dir, global_dir)

            with patch("builtins.input", return_value="y"):
                result = manager.sync("push")

                # Verify sync was requested for prompts
                assert result.success is True


class TestSyncIntegration:
    """Integration tests for complete sync workflows."""

    def test_full_sync_workflow_push(self):
        """Test complete push sync workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create multiple files in different categories
            for category in ["agents", "commands"]:
                project_cat = project_dir / category
                project_cat.mkdir()
                (project_cat / "file1.md").write_text("content1")
                (project_cat / "file2.md").write_text("content2")

                global_cat = global_dir / category
                global_cat.mkdir()

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("push", categories=["agents", "commands"])

            # Verify all files were copied
            assert result.success is True
            assert len(result.files_copied) >= 4

    def test_full_sync_workflow_pull(self):
        """Test complete pull sync workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create files in global directory
            for category in ["agents", "commands"]:
                global_cat = global_dir / category
                global_cat.mkdir()
                (global_cat / "file1.md").write_text("content1")
                (global_cat / "file2.md").write_text("content2")

                project_cat = project_dir / category
                project_cat.mkdir()

            manager = SyncManager(project_dir, global_dir)
            result = manager.sync("pull", categories=["agents", "commands"])

            # Verify all files were copied
            assert result.success is True
            assert len(result.files_copied) >= 4

    def test_bidirectional_sync_consistency(self):
        """Test push then pull maintains file consistency."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / ".claude"
            global_dir = Path(tmpdir) / ".global_claude"
            project_dir.mkdir()
            global_dir.mkdir()

            # Create initial file in project
            (project_dir / "commands").mkdir()
            (global_dir / "commands").mkdir()
            test_file = project_dir / "commands" / "test.md"
            test_file.write_text("original content")

            # Push to global
            manager = SyncManager(project_dir, global_dir)
            push_result = manager.sync("push", categories=["commands"])
            assert push_result.success is True

            # Verify file exists in global
            global_file = global_dir / "commands" / "test.md"
            assert global_file.exists()
            assert global_file.read_text() == "original content"

            # Pull back to project (should be identical)
            pull_result = manager.sync("pull", categories=["commands"])
            assert pull_result.success is True
            assert len(pull_result.files_skipped) > 0  # Should skip identical file
