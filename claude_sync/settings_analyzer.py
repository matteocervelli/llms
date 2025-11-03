"""Analyze and compare settings.json files between project and global locations."""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class SettingsAnalysis:
    """Container for settings analysis results."""

    hooks_differences: List[Dict[str, Any]] = field(default_factory=list)
    permission_differences: List[Dict[str, Any]] = field(default_factory=list)
    plugin_differences: List[Dict[str, Any]] = field(default_factory=list)
    project_settings: Dict[str, Any] = field(default_factory=dict)
    global_settings: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

    def has_differences(self) -> bool:
        """Check if any differences were found."""
        return bool(
            self.hooks_differences
            or self.permission_differences
            or self.plugin_differences
        )


class SettingsAnalyzer:
    """Analyze and compare settings.json files from different locations."""

    def __init__(self, project_dir: Path, global_dir: Path, reporter=None) -> None:
        """
        Initialize settings analyzer.

        Args:
            project_dir: Path to project directory (e.g., ./.claude/)
            global_dir: Path to global directory (e.g., ~/.claude/)
            reporter: Optional reporter object for logging findings
        """
        self.project_dir = Path(project_dir)
        self.global_dir = Path(global_dir)
        self.reporter = reporter

    def analyze(self) -> SettingsAnalysis:
        """
        Analyze settings.json from both locations.

        Returns:
            SettingsAnalysis object with all findings and recommendations
        """
        # Load settings from both locations
        project_settings = self.load_settings(self.project_dir / "settings.json")
        global_settings = self.load_settings(self.global_dir / "settings.json")

        # Initialize analysis
        analysis = SettingsAnalysis(
            project_settings=project_settings or {},
            global_settings=global_settings or {},
        )

        # Skip comparison if either settings file is missing
        if not project_settings or not global_settings:
            logger.warning(
                "Skipping comparison: one or both settings files are missing"
            )
            if not project_settings:
                analysis.recommendations.append(
                    "Project settings.json not found - create one for project-specific settings"
                )
            if not global_settings:
                analysis.recommendations.append(
                    "Global settings.json not found - consider creating one"
                )
            return analysis

        # Perform detailed comparisons
        analysis.hooks_differences = self.compare_hooks(
            project_settings.get("hooks", {}), global_settings.get("hooks", {})
        )

        analysis.permission_differences = self.compare_permissions(
            project_settings.get("permissions", {}),
            global_settings.get("permissions", {}),
        )

        analysis.plugin_differences = self.compare_plugins(
            project_settings.get("enabledPlugins", {}),
            global_settings.get("enabledPlugins", {}),
        )

        # Generate recommendations
        analysis.recommendations = self.generate_recommendations(analysis)

        return analysis

    def load_settings(self, settings_file: Path) -> Optional[Dict[str, Any]]:
        """
        Load and parse settings.json file.

        Args:
            settings_file: Path to settings.json file

        Returns:
            Parsed settings dict or None if file doesn't exist or is invalid
        """
        settings_file = Path(settings_file)

        if not settings_file.exists():
            logger.debug(f"Settings file not found: {settings_file}")
            return None

        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
            logger.debug(f"Loaded settings from {settings_file}")
            return settings
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {settings_file}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading {settings_file}: {e}")
            return None

    def compare_hooks(
        self, project_hooks: Dict[str, Any], global_hooks: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Compare hooks configuration between project and global.

        Args:
            project_hooks: Hooks from project settings
            global_hooks: Hooks from global settings

        Returns:
            List of differences found (each with 'type', 'location', 'details')
        """
        differences = []

        # Get all hook types
        all_types = set(project_hooks.keys()) | set(global_hooks.keys())

        for hook_type in all_types:
            project_list = project_hooks.get(hook_type, [])
            global_list = global_hooks.get(hook_type, [])

            # Compare hook configurations
            if len(project_list) != len(global_list):
                differences.append(
                    {
                        "type": "hook_count_mismatch",
                        "hook_type": hook_type,
                        "project_count": len(project_list),
                        "global_count": len(global_list),
                        "details": f"Different number of {hook_type} hooks",
                    }
                )

            # Compare hook paths and properties
            project_paths = self._extract_hook_paths(project_list)
            global_paths = self._extract_hook_paths(global_list)

            # Find hooks in project but not global
            for path in project_paths - global_paths:
                differences.append(
                    {
                        "type": "hook_in_project_only",
                        "hook_type": hook_type,
                        "path": path,
                        "location": "project",
                        "details": f"Hook found in project but not in global: {path}",
                    }
                )

            # Find hooks in global but not project
            for path in global_paths - project_paths:
                differences.append(
                    {
                        "type": "hook_in_global_only",
                        "hook_type": hook_type,
                        "path": path,
                        "location": "global",
                        "details": f"Hook found in global but not in project: {path}",
                    }
                )

        return differences

    def compare_permissions(
        self, project_perms: Dict[str, Any], global_perms: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Compare permissions (allow/deny lists).

        Args:
            project_perms: Permissions from project settings
            global_perms: Permissions from global settings

        Returns:
            List of permission differences
        """
        differences = []

        project_allow = set(project_perms.get("allow", []))
        global_allow = set(global_perms.get("allow", []))
        project_deny = set(project_perms.get("deny", []))
        global_deny = set(global_perms.get("deny", []))

        # Find permissions in project allow but not global
        unique_project = project_allow - global_allow
        if unique_project:
            differences.append(
                {
                    "type": "allow_permissions_unique_to_project",
                    "count": len(unique_project),
                    "permissions": sorted(list(unique_project)),
                    "details": f"Project has {len(unique_project)} unique allow permissions",
                }
            )

        # Find permissions in global allow but not project
        unique_global = global_allow - project_allow
        if unique_global:
            differences.append(
                {
                    "type": "allow_permissions_unique_to_global",
                    "count": len(unique_global),
                    "permissions": sorted(list(unique_global)),
                    "details": f"Global has {len(unique_global)} unique allow permissions",
                }
            )

        # Compare deny lists
        if project_deny != global_deny:
            differences.append(
                {
                    "type": "deny_permissions_differ",
                    "project_deny": sorted(list(project_deny)),
                    "global_deny": sorted(list(global_deny)),
                    "details": "Deny permission lists differ",
                }
            )

        return differences

    def compare_plugins(
        self, project_plugins: Dict[str, Any], global_plugins: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Compare enabled plugins.

        Args:
            project_plugins: Enabled plugins from project settings
            global_plugins: Enabled plugins from global settings

        Returns:
            List of plugin differences
        """
        differences = []

        all_plugins = set(project_plugins.keys()) | set(global_plugins.keys())

        for plugin in all_plugins:
            project_enabled = project_plugins.get(plugin, False)
            global_enabled = global_plugins.get(plugin, False)

            if project_enabled != global_enabled:
                differences.append(
                    {
                        "type": "plugin_enabled_mismatch",
                        "plugin": plugin,
                        "project_enabled": project_enabled,
                        "global_enabled": global_enabled,
                        "details": (
                            f"Plugin '{plugin}' enabled in "
                            f"{'project' if project_enabled else 'global'} "
                            f"but disabled in {'global' if project_enabled else 'project'}"
                        ),
                    }
                )

        return differences

    def generate_recommendations(self, analysis: SettingsAnalysis) -> List[str]:
        """
        Generate actionable recommendations based on analysis.

        Args:
            analysis: SettingsAnalysis object with findings

        Returns:
            List of actionable recommendation strings
        """
        recommendations = []

        # Hook recommendations
        if analysis.hooks_differences:
            hook_types = {d.get("hook_type") for d in analysis.hooks_differences}
            for hook_type in hook_types:
                count = len(
                    [d for d in analysis.hooks_differences if d.get("hook_type") == hook_type]
                )
                if count > 0:
                    recommendations.append(
                        f"Standardize {hook_type} hooks - found {count} difference(s). "
                        f"Consider consolidating hooks to global settings.json if they're "
                        f"project-wide, or to .claude/settings.json if they're project-specific"
                    )

        # Permission recommendations
        if analysis.permission_differences:
            # Check for significant permission discrepancies
            unique_project_perms = next(
                (d for d in analysis.permission_differences
                 if d.get("type") == "allow_permissions_unique_to_project"),
                None,
            )
            if unique_project_perms and unique_project_perms.get("count", 0) > 3:
                recommendations.append(
                    f"Project has {unique_project_perms['count']} unique allow permissions. "
                    f"Consider moving commonly-used permissions to global settings.json"
                )

            unique_global_perms = next(
                (d for d in analysis.permission_differences
                 if d.get("type") == "allow_permissions_unique_to_global"),
                None,
            )
            if unique_global_perms and unique_global_perms.get("count", 0) > 3:
                recommendations.append(
                    f"Global has {unique_global_perms['count']} unique allow permissions. "
                    f"Ensure project has required permissions for its specific needs"
                )

            # Check for deny list differences
            deny_diff = next(
                (d for d in analysis.permission_differences
                 if d.get("type") == "deny_permissions_differ"),
                None,
            )
            if deny_diff:
                recommendations.append(
                    "Deny permission lists differ between project and global. "
                    "Ensure project-specific restrictions are intentional"
                )

        # Plugin recommendations
        if analysis.plugin_differences:
            for diff in analysis.plugin_differences:
                plugin = diff.get("plugin")
                enabled_in = "project" if diff.get("project_enabled") else "global"
                disabled_in = "global" if diff.get("project_enabled") else "project"
                recommendations.append(
                    f"Plugin '{plugin}' enabled in {enabled_in} but disabled in {disabled_in}. "
                    f"Ensure this is intentional for your use case"
                )

        return recommendations

    @staticmethod
    def _extract_hook_paths(hook_list: List[Dict[str, Any]]) -> set:
        """
        Extract hook paths from hook configuration list.

        Args:
            hook_list: List of hook configurations

        Returns:
            Set of unique hook paths
        """
        paths = set()
        for item in hook_list:
            if isinstance(item, dict):
                # Handle nested hooks structure
                if "hooks" in item:
                    for hook in item["hooks"]:
                        if "command" in hook:
                            paths.add(hook["command"])
                elif "command" in item:
                    paths.add(item["command"])
        return paths
