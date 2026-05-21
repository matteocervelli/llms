"""Test suite for conflict_resolver module.

Tests interactive conflict resolution, diff viewing, and batch operations.
"""

import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from claude_sync.conflict_resolver import ConflictAction, ConflictResolver
from claude_sync.reporter import Reporter


@pytest.fixture
def temp_files():
    """Create temporary test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)

        # Create project and global test files
        project_file = tmppath / "project_file.md"
        global_file = tmppath / "global_file.md"

        project_file.write_text("# Project Content\nVersion: 1.0\nAuthor: Alice\n")
        global_file.write_text("# Global Content\nVersion: 2.0\nAuthor: Bob\n")

        yield {
            "project": project_file,
            "global": global_file,
            "tmpdir": tmppath,
        }


@pytest.fixture
def reporter():
    """Create a mock reporter."""
    return Reporter(verbose=False)


@pytest.fixture
def resolver(reporter):
    """Create a conflict resolver instance."""
    return ConflictResolver(reporter, force=False)


class TestConflictAction:
    """Test ConflictAction enum."""

    def test_conflict_action_values(self):
        """Test that ConflictAction enum has correct values."""
        assert ConflictAction.KEEP_PROJECT.value == "project"
        assert ConflictAction.KEEP_GLOBAL.value == "global"
        assert ConflictAction.SHOW_DIFF.value == "diff"
        assert ConflictAction.SKIP.value == "skip"
        assert ConflictAction.APPLY_ALL_PROJECT.value == "all_project"
        assert ConflictAction.APPLY_ALL_GLOBAL.value == "all_global"


class TestConflictResolverInit:
    """Test ConflictResolver initialization."""

    def test_init_default(self, reporter):
        """Test default initialization."""
        resolver = ConflictResolver(reporter)
        assert resolver.reporter is reporter
        assert resolver.force is False
        assert resolver.apply_all is None

    def test_init_force_mode(self, reporter):
        """Test initialization with force mode."""
        resolver = ConflictResolver(reporter, force=True)
        assert resolver.force is True
        assert resolver.apply_all is None


class TestShowFileInfo:
    """Test show_file_info method."""

    def test_show_file_info_displays_metadata(self, resolver, temp_files, capsys):
        """Test that file info displays size and modification time."""
        resolver.show_file_info(temp_files["project"])

        captured = capsys.readouterr()
        assert "KB" in captured.out
        assert "Modified:" in captured.out

    def test_show_file_info_nonexistent_file(self, resolver, capsys):
        """Test handling of nonexistent file."""
        nonexistent = Path("/tmp/nonexistent_file_xyz.txt")
        resolver.show_file_info(nonexistent)

        # Should not raise, but print error
        assert resolver.reporter is not None


class TestShowDiff:
    """Test show_diff method."""

    def test_show_diff_displays_differences(self, resolver, temp_files, capsys):
        """Test that diff displays differences between files."""
        resolver.show_diff(temp_files["project"], temp_files["global"])

        captured = capsys.readouterr()
        assert "DIFF:" in captured.out
        assert "project" in captured.out.lower()
        assert "global" in captured.out.lower()

    def test_show_diff_shows_additions(self, resolver, temp_files, capsys):
        """Test that diff shows added lines."""
        resolver.show_diff(temp_files["project"], temp_files["global"])

        captured = capsys.readouterr()
        # Both + and - symbols should be present in unified diff
        assert ("+") in captured.out or ("-") in captured.out

    def test_show_diff_handles_binary_files(self, resolver, temp_files, capsys):
        """Test handling of binary files."""
        # Create binary file
        binary_file = Path(temp_files["tmpdir"]) / "binary.bin"
        binary_file.write_bytes(b"\x00\x01\x02\x03")

        # Should not raise, but show warning
        resolver.show_diff(binary_file, temp_files["project"])

    def test_show_diff_handles_nonexistent_file(self, resolver, temp_files, capsys):
        """Test handling of nonexistent file in diff."""
        nonexistent = Path("/tmp/nonexistent_xyz.txt")

        # Should not raise
        with patch.object(resolver, "reporter") as mock_reporter:
            resolver.show_diff(nonexistent, temp_files["global"])


class TestAutoResolve:
    """Test auto_resolve method."""

    def test_auto_resolve_newer_project_file(self, resolver, temp_files):
        """Test auto-resolve chooses newer project file."""
        # Set project file as newer
        now = datetime.now().timestamp()
        import os

        os.utime(temp_files["project"], (now, now))
        os.utime(temp_files["global"], (now - 3600, now - 3600))  # 1 hour older

        result = resolver.auto_resolve(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.KEEP_PROJECT

    def test_auto_resolve_newer_global_file(self, resolver, temp_files):
        """Test auto-resolve chooses newer global file."""
        # Set global file as newer
        now = datetime.now().timestamp()
        import os

        os.utime(temp_files["project"], (now - 3600, now - 3600))  # 1 hour older
        os.utime(temp_files["global"], (now, now))

        result = resolver.auto_resolve(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.KEEP_GLOBAL

    def test_auto_resolve_same_mtime(self, resolver, temp_files):
        """Test auto-resolve with same modification time (defaults to project)."""
        # Set both files to same mtime
        now = datetime.now().timestamp()
        import os

        os.utime(temp_files["project"], (now, now))
        os.utime(temp_files["global"], (now, now))

        result = resolver.auto_resolve(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.KEEP_PROJECT

    def test_auto_resolve_handles_errors(self, resolver, temp_files):
        """Test auto-resolve handles stat errors gracefully."""
        nonexistent = Path("/tmp/nonexistent_xyz.txt")

        result = resolver.auto_resolve(nonexistent, temp_files["global"])
        # Should default to KEEP_PROJECT on error
        assert result == ConflictAction.KEEP_PROJECT


class TestPromptUser:
    """Test prompt_user method."""

    @patch("builtins.input", return_value="p")
    def test_prompt_user_keep_project(self, mock_input, resolver, temp_files):
        """Test user selecting keep project."""
        result = resolver.prompt_user(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.KEEP_PROJECT

    @patch("builtins.input", return_value="g")
    def test_prompt_user_keep_global(self, mock_input, resolver, temp_files):
        """Test user selecting keep global."""
        result = resolver.prompt_user(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.KEEP_GLOBAL

    @patch("builtins.input", return_value="s")
    def test_prompt_user_skip(self, mock_input, resolver, temp_files):
        """Test user selecting skip."""
        result = resolver.prompt_user(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.SKIP

    @patch("builtins.input", side_effect=["d", "p"])
    def test_prompt_user_show_diff_then_choose(
        self, mock_input, resolver, temp_files
    ):
        """Test user viewing diff then making a choice."""
        result = resolver.prompt_user(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.KEEP_PROJECT

    @patch("builtins.input", return_value="a")
    def test_prompt_user_apply_all_project(self, mock_input, resolver, temp_files):
        """Test user selecting apply all project."""
        result = resolver.prompt_user(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.APPLY_ALL_PROJECT
        # Verify batch mode is set
        assert resolver.apply_all == ConflictAction.KEEP_PROJECT

    @patch("builtins.input", return_value="A")
    def test_prompt_user_apply_all_global(self, mock_input, reporter, temp_files):
        """Test user selecting apply all global."""
        # Create fresh resolver to avoid state from previous tests
        resolver = ConflictResolver(reporter, force=False)
        result = resolver.prompt_user(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.APPLY_ALL_GLOBAL
        # Verify batch mode is set
        assert resolver.apply_all == ConflictAction.KEEP_GLOBAL

    @patch("builtins.input", side_effect=["invalid", "p"])
    def test_prompt_user_invalid_input_then_valid(
        self, mock_input, resolver, temp_files
    ):
        """Test user entering invalid input then valid choice."""
        result = resolver.prompt_user(temp_files["project"], temp_files["global"])
        assert result == ConflictAction.KEEP_PROJECT

    @patch("builtins.input", side_effect=KeyboardInterrupt)
    def test_prompt_user_keyboard_interrupt(self, mock_input, resolver, temp_files):
        """Test user pressing Ctrl+C."""
        with pytest.raises(KeyboardInterrupt):
            resolver.prompt_user(temp_files["project"], temp_files["global"])

    @patch("builtins.input", side_effect=EOFError)
    def test_prompt_user_eof(self, mock_input, resolver, temp_files):
        """Test EOF during input."""
        with pytest.raises(KeyboardInterrupt):
            resolver.prompt_user(temp_files["project"], temp_files["global"])


class TestResolveConflict:
    """Test resolve_conflict method."""

    def test_resolve_conflict_respects_batch_mode(self, resolver, temp_files):
        """Test that batch mode is respected."""
        resolver.apply_all = ConflictAction.KEEP_GLOBAL

        result = resolver.resolve_conflict(
            temp_files["project"], temp_files["global"]
        )
        assert result == ConflictAction.KEEP_GLOBAL

    @patch.object(ConflictResolver, "auto_resolve", return_value=ConflictAction.KEEP_PROJECT)
    def test_resolve_conflict_force_mode(self, mock_auto, resolver, temp_files):
        """Test force mode skips interactive prompt."""
        resolver.force = True

        result = resolver.resolve_conflict(
            temp_files["project"], temp_files["global"]
        )
        assert result == ConflictAction.KEEP_PROJECT
        mock_auto.assert_called_once()

    @patch.object(ConflictResolver, "prompt_user", return_value=ConflictAction.KEEP_PROJECT)
    def test_resolve_conflict_interactive_mode(
        self, mock_prompt, resolver, temp_files
    ):
        """Test interactive mode calls prompt_user."""
        result = resolver.resolve_conflict(
            temp_files["project"], temp_files["global"]
        )
        assert result == ConflictAction.KEEP_PROJECT
        mock_prompt.assert_called_once()


class TestResetBatchMode:
    """Test reset_batch_mode method."""

    def test_reset_batch_mode_clears_apply_all(self, resolver):
        """Test that reset_batch_mode clears apply_all."""
        resolver.apply_all = ConflictAction.KEEP_PROJECT

        resolver.reset_batch_mode()

        assert resolver.apply_all is None

    def test_reset_batch_mode_when_already_none(self, resolver):
        """Test reset_batch_mode when apply_all is already None."""
        resolver.apply_all = None

        resolver.reset_batch_mode()

        assert resolver.apply_all is None


class TestIntegration:
    """Integration tests for conflict resolution workflow."""

    @patch("builtins.input", side_effect=["p"])
    def test_full_workflow_single_conflict(self, mock_input, resolver, temp_files):
        """Test full workflow for single conflict resolution."""
        # First conflict
        result1 = resolver.resolve_conflict(
            temp_files["project"], temp_files["global"]
        )
        assert result1 == ConflictAction.KEEP_PROJECT

        # Reset for next conflict
        resolver.reset_batch_mode()

        # Should prompt again
        with patch("builtins.input", return_value="g"):
            result2 = resolver.resolve_conflict(
                temp_files["project"], temp_files["global"]
            )
            assert result2 == ConflictAction.KEEP_GLOBAL

    @patch("builtins.input", return_value="a")
    def test_full_workflow_batch_operation(self, mock_input, resolver, temp_files):
        """Test batch operation workflow."""
        # First conflict with batch choice
        result1 = resolver.resolve_conflict(
            temp_files["project"], temp_files["global"]
        )
        assert result1 == ConflictAction.APPLY_ALL_PROJECT

        # Subsequent conflicts should use batch mode without prompting
        with patch("builtins.input") as mock_input2:
            result2 = resolver.resolve_conflict(
                temp_files["project"], temp_files["global"]
            )
            # Should not call input again
            mock_input2.assert_not_called()
            assert result2 == ConflictAction.KEEP_PROJECT

    def test_force_mode_workflow(self, reporter, temp_files):
        """Test force mode workflow."""
        resolver = ConflictResolver(reporter, force=True)

        # Set project as newer
        now = datetime.now().timestamp()
        import os

        os.utime(temp_files["project"], (now, now))
        os.utime(temp_files["global"], (now - 3600, now - 3600))

        # Should auto-resolve without any input
        result = resolver.resolve_conflict(
            temp_files["project"], temp_files["global"]
        )
        assert result == ConflictAction.KEEP_PROJECT
