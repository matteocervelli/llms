"""Unit tests for settings_analyzer module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from claude_sync.settings_analyzer import SettingsAnalysis, SettingsAnalyzer


@pytest.fixture
def temp_dirs():
    """Create temporary directories for testing."""
    with tempfile.TemporaryDirectory() as project_dir, tempfile.TemporaryDirectory() as global_dir:
        yield Path(project_dir), Path(global_dir)


@pytest.fixture
def sample_settings():
    """Create sample settings configurations."""
    return {
        "project": {
            "permissions": {
                "allow": [
                    "Bash(ls:*)",
                    "Bash(find:*)",
                    "Bash(grep:*)",
                    "mcp__github-mcp__get_issue",
                    "mcp__github-mcp__create_issue",
                ],
                "deny": [],
            },
            "enabledPlugins": {
                "example-skills@anthropic-agent-skills": True,
                "custom-plugin": True,
            },
            "hooks": {
                "PreToolUse": [
                    {
                        "matcher": "Bash",
                        "hooks": [
                            {
                                "type": "command",
                                "command": '"$CLAUDE_PROJECT_DIR"/.claude/hooks/pre-commit.py',
                                "timeout": 180,
                            }
                        ],
                    }
                ]
            },
        },
        "global": {
            "permissions": {
                "allow": [
                    "Bash(ls:*)",
                    "Bash(curl:*)",
                    "mcp__github-mcp__get_issue",
                    "mcp__github-mcp__list_issues",
                ],
                "deny": [],
            },
            "enabledPlugins": {
                "example-skills@anthropic-agent-skills": True,
                "document-skills@anthropic-agent-skills": True,
            },
            "hooks": {
                "PreToolUse": [
                    {
                        "matcher": "Bash",
                        "hooks": [
                            {
                                "type": "command",
                                "command": "~/.claude/hooks/global-hook.py",
                                "timeout": 60,
                            }
                        ],
                    }
                ]
            },
        },
    }


def create_settings_files(project_dir: Path, global_dir: Path, settings: dict) -> None:
    """Helper to create settings.json files."""
    project_dir.mkdir(exist_ok=True)
    global_dir.mkdir(exist_ok=True)

    with open(project_dir / "settings.json", "w") as f:
        json.dump(settings["project"], f)

    with open(global_dir / "settings.json", "w") as f:
        json.dump(settings["global"], f)


class TestSettingsAnalysis:
    """Test SettingsAnalysis dataclass."""

    def test_analysis_initialization(self):
        """Test SettingsAnalysis can be initialized with defaults."""
        analysis = SettingsAnalysis()
        assert analysis.hooks_differences == []
        assert analysis.permission_differences == []
        assert analysis.plugin_differences == []
        assert analysis.recommendations == []
        assert analysis.has_differences() is False

    def test_analysis_with_differences(self):
        """Test has_differences returns True when differences exist."""
        analysis = SettingsAnalysis(
            hooks_differences=[{"type": "test"}],
            permission_differences=[],
            plugin_differences=[],
        )
        assert analysis.has_differences() is True

    def test_analysis_all_fields(self):
        """Test SettingsAnalysis with all fields populated."""
        analysis = SettingsAnalysis(
            hooks_differences=[{"type": "hook_mismatch"}],
            permission_differences=[{"type": "perm_mismatch"}],
            plugin_differences=[{"type": "plugin_mismatch"}],
            project_settings={"test": "value"},
            global_settings={"test": "value"},
            recommendations=["Test recommendation"],
        )
        assert len(analysis.hooks_differences) == 1
        assert len(analysis.permission_differences) == 1
        assert len(analysis.plugin_differences) == 1
        assert analysis.has_differences() is True


class TestSettingsAnalyzer:
    """Test SettingsAnalyzer class."""

    def test_initialization(self, temp_dirs):
        """Test SettingsAnalyzer initialization."""
        project_dir, global_dir = temp_dirs
        analyzer = SettingsAnalyzer(project_dir, global_dir)
        assert analyzer.project_dir == project_dir
        assert analyzer.global_dir == global_dir
        assert analyzer.reporter is None

    def test_initialization_with_reporter(self, temp_dirs):
        """Test SettingsAnalyzer with reporter."""
        project_dir, global_dir = temp_dirs
        reporter = MagicMock()
        analyzer = SettingsAnalyzer(project_dir, global_dir, reporter)
        assert analyzer.reporter is reporter

    def test_load_settings_success(self, temp_dirs, sample_settings):
        """Test loading valid settings.json file."""
        project_dir, _ = temp_dirs
        project_dir.mkdir(exist_ok=True)

        with open(project_dir / "settings.json", "w") as f:
            json.dump(sample_settings["project"], f)

        analyzer = SettingsAnalyzer(project_dir, Path("."))
        settings = analyzer.load_settings(project_dir / "settings.json")

        assert settings is not None
        assert "permissions" in settings
        assert "enabledPlugins" in settings
        assert "hooks" in settings

    def test_load_settings_missing_file(self, temp_dirs):
        """Test loading non-existent settings.json file."""
        project_dir, _ = temp_dirs
        analyzer = SettingsAnalyzer(project_dir, Path("."))
        settings = analyzer.load_settings(project_dir / "settings.json")
        assert settings is None

    def test_load_settings_invalid_json(self, temp_dirs):
        """Test loading invalid JSON file."""
        project_dir, _ = temp_dirs
        project_dir.mkdir(exist_ok=True)

        with open(project_dir / "settings.json", "w") as f:
            f.write("{ invalid json }")

        analyzer = SettingsAnalyzer(project_dir, Path("."))
        settings = analyzer.load_settings(project_dir / "settings.json")
        assert settings is None

    def test_compare_permissions_no_differences(self, temp_dirs):
        """Test comparing identical permissions."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        perms = {
            "allow": ["Bash(ls:*)", "Bash(find:*)", "mcp__test"],
            "deny": [],
        }
        differences = analyzer.compare_permissions(perms, perms)
        assert differences == []

    def test_compare_permissions_unique_project(self, temp_dirs):
        """Test comparing permissions with unique project permissions."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        project_perms = {
            "allow": ["Bash(ls:*)", "Bash(find:*)", "mcp__test"],
            "deny": [],
        }
        global_perms = {"allow": ["Bash(ls:*)"], "deny": []}

        differences = analyzer.compare_permissions(project_perms, global_perms)

        assert len(differences) == 1
        assert differences[0]["type"] == "allow_permissions_unique_to_project"
        assert differences[0]["count"] == 2
        assert "Bash(find:*)" in differences[0]["permissions"]

    def test_compare_permissions_unique_global(self, temp_dirs):
        """Test comparing permissions with unique global permissions."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        project_perms = {"allow": ["Bash(ls:*)"], "deny": []}
        global_perms = {
            "allow": ["Bash(ls:*)", "Bash(curl:*)", "mcp__test"],
            "deny": [],
        }

        differences = analyzer.compare_permissions(project_perms, global_perms)

        assert len(differences) == 1
        assert differences[0]["type"] == "allow_permissions_unique_to_global"

    def test_compare_permissions_deny_differences(self, temp_dirs):
        """Test comparing different deny lists."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        project_perms = {"allow": [], "deny": ["danger:*"]}
        global_perms = {"allow": [], "deny": []}

        differences = analyzer.compare_permissions(project_perms, global_perms)

        assert len(differences) == 1
        assert differences[0]["type"] == "deny_permissions_differ"

    def test_compare_plugins_no_differences(self, temp_dirs):
        """Test comparing identical plugins."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        plugins = {"plugin-a": True, "plugin-b": False}
        differences = analyzer.compare_plugins(plugins, plugins)
        assert differences == []

    def test_compare_plugins_enabled_mismatch(self, temp_dirs):
        """Test comparing plugins with different enabled state."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        project_plugins = {"plugin-a": True, "plugin-b": True}
        global_plugins = {"plugin-a": True, "plugin-b": False}

        differences = analyzer.compare_plugins(project_plugins, global_plugins)

        assert len(differences) == 1
        assert differences[0]["type"] == "plugin_enabled_mismatch"
        assert differences[0]["plugin"] == "plugin-b"
        assert differences[0]["project_enabled"] is True
        assert differences[0]["global_enabled"] is False

    def test_compare_hooks_no_differences(self, temp_dirs):
        """Test comparing identical hooks."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        hooks = {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [{"type": "command", "command": "test.py"}],
                }
            ]
        }
        differences = analyzer.compare_hooks(hooks, hooks)
        assert differences == []

    def test_compare_hooks_count_mismatch(self, temp_dirs):
        """Test comparing hooks with different counts."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        project_hooks = {
            "PreToolUse": [
                {"matcher": "Bash", "hooks": [{"type": "command", "command": "a.py"}]},
                {"matcher": "Bash", "hooks": [{"type": "command", "command": "b.py"}]},
            ]
        }
        global_hooks = {
            "PreToolUse": [
                {"matcher": "Bash", "hooks": [{"type": "command", "command": "a.py"}]}
            ]
        }

        differences = analyzer.compare_hooks(project_hooks, global_hooks)

        assert len(differences) > 0
        assert any(d["type"] == "hook_count_mismatch" for d in differences)

    def test_compare_hooks_different_paths(self, temp_dirs):
        """Test comparing hooks with different paths."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        project_hooks = {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {"type": "command", "command": '"$CLAUDE_PROJECT_DIR"/.claude/hooks/test.py'}
                    ],
                }
            ]
        }
        global_hooks = {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [{"type": "command", "command": "~/.claude/hooks/global.py"}],
                }
            ]
        }

        differences = analyzer.compare_hooks(project_hooks, global_hooks)

        assert len(differences) >= 2  # At least 2 path differences

    def test_extract_hook_paths(self, temp_dirs):
        """Test extracting hook paths from configuration."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        hook_list = [
            {
                "matcher": "Bash",
                "hooks": [
                    {"type": "command", "command": "path/to/hook1.py"},
                    {"type": "command", "command": "path/to/hook2.py"},
                ],
            }
        ]

        paths = analyzer._extract_hook_paths(hook_list)

        assert len(paths) == 2
        assert "path/to/hook1.py" in paths
        assert "path/to/hook2.py" in paths

    def test_extract_hook_paths_empty(self, temp_dirs):
        """Test extracting paths from empty hook list."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        paths = analyzer._extract_hook_paths([])
        assert paths == set()

    def test_generate_recommendations_hooks(self, temp_dirs):
        """Test generating hook recommendations."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        analysis = SettingsAnalysis(
            hooks_differences=[
                {"type": "hook_in_project_only", "hook_type": "PreToolUse", "path": "test.py"}
            ]
        )

        recommendations = analyzer.generate_recommendations(analysis)

        assert len(recommendations) > 0
        assert any("hook" in rec.lower() for rec in recommendations)

    def test_generate_recommendations_permissions(self, temp_dirs):
        """Test generating permission recommendations."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        analysis = SettingsAnalysis(
            permission_differences=[
                {
                    "type": "allow_permissions_unique_to_project",
                    "count": 5,
                    "permissions": ["a", "b", "c", "d", "e"],
                }
            ]
        )

        recommendations = analyzer.generate_recommendations(analysis)

        assert len(recommendations) > 0
        assert any("permission" in rec.lower() for rec in recommendations)

    def test_generate_recommendations_plugins(self, temp_dirs):
        """Test generating plugin recommendations."""
        analyzer = SettingsAnalyzer(temp_dirs[0], temp_dirs[1])
        analysis = SettingsAnalysis(
            plugin_differences=[
                {
                    "type": "plugin_enabled_mismatch",
                    "plugin": "test-plugin",
                    "project_enabled": True,
                    "global_enabled": False,
                }
            ]
        )

        recommendations = analyzer.generate_recommendations(analysis)

        assert len(recommendations) > 0
        assert "test-plugin" in recommendations[0]

    def test_analyze_missing_project_settings(self, temp_dirs):
        """Test analysis when project settings.json is missing."""
        project_dir, global_dir = temp_dirs
        global_dir.mkdir(exist_ok=True)

        with open(global_dir / "settings.json", "w") as f:
            json.dump({"permissions": {"allow": [], "deny": []}}, f)

        analyzer = SettingsAnalyzer(project_dir, global_dir)
        analysis = analyzer.analyze()

        assert analysis.project_settings == {}
        assert len(analysis.recommendations) > 0

    def test_analyze_missing_global_settings(self, temp_dirs):
        """Test analysis when global settings.json is missing."""
        project_dir, global_dir = temp_dirs
        project_dir.mkdir(exist_ok=True)

        with open(project_dir / "settings.json", "w") as f:
            json.dump({"permissions": {"allow": [], "deny": []}}, f)

        analyzer = SettingsAnalyzer(project_dir, global_dir)
        analysis = analyzer.analyze()

        assert analysis.global_settings == {}
        assert len(analysis.recommendations) > 0

    def test_analyze_full_comparison(self, temp_dirs, sample_settings):
        """Test complete analysis with both settings files present."""
        project_dir, global_dir = temp_dirs
        create_settings_files(project_dir, global_dir, sample_settings)

        analyzer = SettingsAnalyzer(project_dir, global_dir)
        analysis = analyzer.analyze()

        assert analysis.project_settings != {}
        assert analysis.global_settings != {}
        assert analysis.has_differences() is True
        assert len(analysis.recommendations) > 0

    def test_analyze_identical_settings(self, temp_dirs):
        """Test analysis when settings are identical."""
        project_dir, global_dir = temp_dirs
        settings = {
            "project": {
                "permissions": {"allow": ["Bash(ls:*)"], "deny": []},
                "enabledPlugins": {"plugin-a": True},
                "hooks": {},
            },
            "global": {
                "permissions": {"allow": ["Bash(ls:*)"], "deny": []},
                "enabledPlugins": {"plugin-a": True},
                "hooks": {},
            },
        }

        create_settings_files(project_dir, global_dir, settings)

        analyzer = SettingsAnalyzer(project_dir, global_dir)
        analysis = analyzer.analyze()

        assert analysis.hooks_differences == []
        assert analysis.permission_differences == []
        assert analysis.plugin_differences == []
