# Settings Analyzer - Usage Examples

## Example 1: Basic Settings Comparison

Compare settings between project and global Claude configurations:

```python
from pathlib import Path
from claude_sync.settings_analyzer import SettingsAnalyzer

# Initialize the analyzer
analyzer = SettingsAnalyzer(
    project_dir=Path("./.claude"),
    global_dir=Path.home() / ".claude"
)

# Run analysis
analysis = analyzer.analyze()

# Check if differences exist
if analysis.has_differences():
    print("Differences found in settings!")
else:
    print("Settings are identical")
```

## Example 2: Detailed Analysis Report

Generate a detailed report of all differences:

```python
from pathlib import Path
from claude_sync.settings_analyzer import SettingsAnalyzer

def print_analysis_report():
    analyzer = SettingsAnalyzer(
        project_dir=Path("./.claude"),
        global_dir=Path.home() / ".claude"
    )

    analysis = analyzer.analyze()

    print("SETTINGS ANALYSIS REPORT")
    print("=" * 60)

    # Report hooks differences
    if analysis.hooks_differences:
        print(f"\nHOOK DIFFERENCES ({len(analysis.hooks_differences)} found)")
        print("-" * 60)
        for diff in analysis.hooks_differences:
            print(f"Type: {diff['type']}")
            print(f"Hook Type: {diff.get('hook_type', 'N/A')}")
            print(f"Details: {diff['details']}")
            print()

    # Report permission differences
    if analysis.permission_differences:
        print(f"\nPERMISSION DIFFERENCES ({len(analysis.permission_differences)} found)")
        print("-" * 60)
        for diff in analysis.permission_differences:
            print(f"Type: {diff['type']}")
            print(f"Details: {diff['details']}")
            if 'permissions' in diff:
                print(f"Permissions: {', '.join(diff['permissions'][:3])}...")
            print()

    # Report plugin differences
    if analysis.plugin_differences:
        print(f"\nPLUGIN DIFFERENCES ({len(analysis.plugin_differences)} found)")
        print("-" * 60)
        for diff in analysis.plugin_differences:
            print(f"Plugin: {diff['plugin']}")
            print(f"Project Enabled: {diff['project_enabled']}")
            print(f"Global Enabled: {diff['global_enabled']}")
            print()

    # Show recommendations
    if analysis.recommendations:
        print("\nRECOMMENDATIONS")
        print("=" * 60)
        for i, rec in enumerate(analysis.recommendations, 1):
            print(f"{i}. {rec}")
            print()

if __name__ == "__main__":
    print_analysis_report()
```

## Example 3: Check Specific Differences

Focus on a specific type of difference:

```python
from pathlib import Path
from claude_sync.settings_analyzer import SettingsAnalyzer

analyzer = SettingsAnalyzer(
    project_dir=Path("./.claude"),
    global_dir=Path.home() / ".claude"
)

analysis = analyzer.analyze()

# Check only permission differences
if analysis.permission_differences:
    for diff in analysis.permission_differences:
        if diff['type'] == 'allow_permissions_unique_to_project':
            print(f"Project has unique permissions: {diff['permissions']}")
        elif diff['type'] == 'allow_permissions_unique_to_global':
            print(f"Global has unique permissions: {diff['permissions']}")

# Check only plugin differences
if analysis.plugin_differences:
    for diff in analysis.plugin_differences:
        plugin = diff['plugin']
        enabled_in = "project" if diff['project_enabled'] else "global"
        print(f"Plugin '{plugin}' enabled only in {enabled_in}")
```

## Example 4: Integrate with Sync Manager

Use settings analyzer as part of a sync workflow:

```python
from pathlib import Path
from claude_sync import SettingsAnalyzer, SyncManager, FileHandler

def sync_with_analysis():
    """Analyze settings before syncing."""
    project_dir = Path("./.claude")
    global_dir = Path.home() / ".claude"

    # First, analyze differences
    analyzer = SettingsAnalyzer(project_dir, global_dir)
    analysis = analyzer.analyze()

    print(f"Found {len(analysis.hooks_differences)} hook differences")
    print(f"Found {len(analysis.permission_differences)} permission differences")
    print(f"Found {len(analysis.plugin_differences)} plugin differences")

    # Ask user about syncing
    if analysis.has_differences():
        response = input("Proceed with sync? (y/n): ")
        if response.lower() == 'y':
            # Proceed with sync using SyncManager
            file_handler = FileHandler(backup_enabled=True)
            sync_manager = SyncManager(project_dir, global_dir, file_handler)
            # ... continue with sync logic
        else:
            print("Sync cancelled. Review recommendations:")
            for rec in analysis.recommendations:
                print(f"  - {rec}")
    else:
        print("Settings are identical. No sync needed.")

if __name__ == "__main__":
    sync_with_analysis()
```

## Example 5: Monitor Settings Changes Over Time

Track how settings change with each analysis:

```python
from pathlib import Path
from datetime import datetime
from claude_sync.settings_analyzer import SettingsAnalyzer
import json

class SettingsMonitor:
    """Monitor settings changes over time."""

    def __init__(self):
        self.history = []

    def check_settings(self):
        """Check and record settings."""
        analyzer = SettingsAnalyzer(
            project_dir=Path("./.claude"),
            global_dir=Path.home() / ".claude"
        )

        analysis = analyzer.analyze()

        record = {
            'timestamp': datetime.now().isoformat(),
            'hooks_diff_count': len(analysis.hooks_differences),
            'perms_diff_count': len(analysis.permission_differences),
            'plugins_diff_count': len(analysis.plugin_differences),
            'total_differences': (
                len(analysis.hooks_differences) +
                len(analysis.permission_differences) +
                len(analysis.plugin_differences)
            ),
            'recommendations_count': len(analysis.recommendations)
        }

        self.history.append(record)
        return record

    def get_trend(self):
        """Get trend of differences."""
        if len(self.history) < 2:
            return "Not enough data"

        current = self.history[-1]['total_differences']
        previous = self.history[-2]['total_differences']

        if current > previous:
            return f"Differences increased: {previous} → {current}"
        elif current < previous:
            return f"Differences decreased: {previous} → {current}"
        else:
            return "No change in differences"

    def save_history(self, filepath):
        """Save monitoring history to file."""
        with open(filepath, 'w') as f:
            json.dump(self.history, f, indent=2)

# Usage
monitor = SettingsMonitor()
result = monitor.check_settings()
print(f"Check complete: {result['total_differences']} differences found")
print(f"Trend: {monitor.get_trend()}")
```

## Example 6: Validate Settings Before Applying

Analyze settings and suggest consolidation:

```python
from pathlib import Path
from claude_sync.settings_analyzer import SettingsAnalyzer

def validate_before_apply(source_dir: Path, target_dir: Path) -> bool:
    """Validate that applying source settings to target is safe."""

    # Analyze current differences
    analyzer = SettingsAnalyzer(target_dir, source_dir)
    analysis = analyzer.analyze()

    # Check for problematic differences
    issues = []

    # Check for many new permissions
    for diff in analysis.permission_differences:
        if diff['type'] == 'allow_permissions_unique_to_global':
            if diff['count'] > 10:
                issues.append(
                    f"Source would add {diff['count']} new permissions. "
                    "Review for security implications."
                )

    # Check for hook changes
    if analysis.hooks_differences:
        issues.append(
            f"Hook configuration would change ({len(analysis.hooks_differences)} differences). "
            "Ensure hooks are compatible."
        )

    # Check for plugin disabling
    for diff in analysis.plugin_differences:
        if diff['global_enabled'] and not diff['project_enabled']:
            issues.append(
                f"Plugin '{diff['plugin']}' would be disabled. "
                "Verify this is intentional."
            )

    if issues:
        print("VALIDATION WARNINGS:")
        for issue in issues:
            print(f"  ⚠ {issue}")
        return False

    print("✓ Settings are safe to apply")
    return True

# Usage
if validate_before_apply(
    source_dir=Path.home() / ".claude",
    target_dir=Path("./.claude")
):
    print("Proceeding with settings application...")
```

## Example 7: Command-Line Integration

Create a CLI tool using the analyzer:

```python
#!/usr/bin/env python3
"""CLI tool for analyzing Claude settings."""

from pathlib import Path
from claude_sync.settings_analyzer import SettingsAnalyzer
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Analyze Claude settings differences"
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=Path("./.claude"),
        help="Path to project settings directory"
    )
    parser.add_argument(
        "--global",
        dest="global_dir",
        type=Path,
        default=Path.home() / ".claude",
        help="Path to global settings directory"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed information"
    )

    args = parser.parse_args()

    analyzer = SettingsAnalyzer(args.project, args.global_dir)
    analysis = analyzer.analyze()

    if args.json:
        import json
        output = {
            'has_differences': analysis.has_differences(),
            'hooks_differences_count': len(analysis.hooks_differences),
            'permission_differences_count': len(analysis.permission_differences),
            'plugin_differences_count': len(analysis.plugin_differences),
            'recommendations': analysis.recommendations
        }
        print(json.dumps(output, indent=2))
    else:
        if analysis.has_differences():
            print("✗ Differences found")
            print(f"  Hooks: {len(analysis.hooks_differences)}")
            print(f"  Permissions: {len(analysis.permission_differences)}")
            print(f"  Plugins: {len(analysis.plugin_differences)}")

            if args.verbose:
                print("\nRecommendations:")
                for rec in analysis.recommendations:
                    print(f"  - {rec}")
        else:
            print("✓ Settings are identical")

    return 0 if analysis.has_differences() else 1

if __name__ == "__main__":
    sys.exit(main())
```

## Example 8: Integration Test

Test the analyzer with sample configurations:

```python
from pathlib import Path
from claude_sync.settings_analyzer import SettingsAnalyzer, SettingsAnalysis
import tempfile
import json

def test_analyzer_integration():
    """Integration test for settings analyzer."""

    with tempfile.TemporaryDirectory() as project_dir, \
         tempfile.TemporaryDirectory() as global_dir:

        project_path = Path(project_dir)
        global_path = Path(global_dir)

        # Create project settings
        project_settings = {
            "permissions": {
                "allow": ["Bash(ls:*)", "mcp__test"],
                "deny": []
            },
            "enabledPlugins": {"plugin-a": True},
            "hooks": {}
        }

        # Create global settings
        global_settings = {
            "permissions": {
                "allow": ["Bash(ls:*)", "Bash(find:*)"],
                "deny": []
            },
            "enabledPlugins": {"plugin-a": True, "plugin-b": True},
            "hooks": {}
        }

        # Write files
        with open(project_path / "settings.json", "w") as f:
            json.dump(project_settings, f)
        with open(global_path / "settings.json", "w") as f:
            json.dump(global_settings, f)

        # Analyze
        analyzer = SettingsAnalyzer(project_path, global_path)
        analysis = analyzer.analyze()

        # Verify results
        assert analysis.has_differences()
        assert len(analysis.permission_differences) > 0
        assert len(analysis.plugin_differences) > 0
        assert len(analysis.recommendations) > 0

        print("✓ Integration test passed")

if __name__ == "__main__":
    test_analyzer_integration()
```

## Real-World Workflow

```python
#!/usr/bin/env python3
"""Real-world workflow for Claude settings management."""

from pathlib import Path
from claude_sync.settings_analyzer import SettingsAnalyzer
from datetime import datetime

def daily_settings_check():
    """Daily check of Claude settings."""

    analyzer = SettingsAnalyzer(
        project_dir=Path("./.claude"),
        global_dir=Path.home() / ".claude"
    )

    analysis = analyzer.analyze()

    # Log results
    log_file = Path.home() / ".claude" / "settings_audit.log"

    with open(log_file, "a") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Check at {datetime.now().isoformat()}\n")
        f.write(f"{'='*60}\n")
        f.write(f"Hooks differences: {len(analysis.hooks_differences)}\n")
        f.write(f"Permission differences: {len(analysis.permission_differences)}\n")
        f.write(f"Plugin differences: {len(analysis.plugin_differences)}\n")

        if analysis.recommendations:
            f.write("\nRecommendations:\n")
            for rec in analysis.recommendations:
                f.write(f"  - {rec}\n")

    # Alert if significant changes detected
    total_diffs = (len(analysis.hooks_differences) +
                   len(analysis.permission_differences) +
                   len(analysis.plugin_differences))

    if total_diffs > 10:
        print(f"⚠  WARNING: {total_diffs} differences detected!")
        print("Review your settings configuration")
        return False

    return True

if __name__ == "__main__":
    success = daily_settings_check()
    exit(0 if success else 1)
```
