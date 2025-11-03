#!/usr/bin/env python3
"""
Claude Configuration Sync & Audit Script

Syncs and audits Claude configuration files between project-specific
.claude/ folder and global ~/.claude/ folder.

Usage:
    python sync_claude_configs.py                    # Audit mode (default)
    python sync_claude_configs.py --audit            # Audit with report
    python sync_claude_configs.py --sync             # Sync project → global
    python sync_claude_configs.py --sync --pull      # Sync global → project
    python sync_claude_configs.py --sync --dry-run   # Preview sync operations
"""

import argparse
import sys
from pathlib import Path

from claude_sync import (
    AuditManager,
    SyncManager,
    SettingsAnalyzer,
    Reporter,
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Sync and audit Claude configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Audit mode (show differences)
  %(prog)s --audit --verbose            # Detailed audit report
  %(prog)s --sync                       # Sync project → global
  %(prog)s --sync --pull                # Sync global → project
  %(prog)s --sync --dry-run             # Preview sync without changes
  %(prog)s --sync --agents-only         # Sync only agents
  %(prog)s --settings                   # Analyze settings.json
        """,
    )

    parser.add_argument(
        "--audit",
        action="store_true",
        help="Run audit mode (default if no other mode specified)",
    )

    parser.add_argument(
        "--sync",
        action="store_true",
        help="Run sync mode (default: project → global)",
    )

    parser.add_argument(
        "--settings",
        action="store_true",
        help="Analyze and compare settings.json files",
    )

    parser.add_argument(
        "--pull",
        action="store_true",
        help="Sync direction: global → project (requires --sync)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be synced without making changes",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Auto-resolve conflicts (newer file wins)",
    )

    parser.add_argument(
        "--agents-only",
        action="store_true",
        help="Sync only agents",
    )

    parser.add_argument(
        "--commands-only",
        action="store_true",
        help="Sync only commands",
    )

    parser.add_argument(
        "--skills-only",
        action="store_true",
        help="Sync only skills",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)",
    )

    parser.add_argument(
        "--global-dir",
        type=Path,
        default=Path.home() / ".claude",
        help="Global .claude directory (default: ~/.claude)",
    )

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    # Initialize paths
    project_claude = args.project_dir / ".claude"
    global_claude = args.global_dir

    # Validate directories exist
    if not project_claude.exists():
        print(f"❌ Project .claude directory not found: {project_claude}")
        sys.exit(1)

    if not global_claude.exists():
        print(f"❌ Global .claude directory not found: {global_claude}")
        sys.exit(1)

    # Initialize reporter
    reporter = Reporter(verbose=args.verbose)

    # Determine mode
    if args.sync:
        # Sync mode
        direction = "pull" if args.pull else "push"
        categories = []

        if args.agents_only:
            categories.append("agents")
        if args.commands_only:
            categories.append("commands")
        if args.skills_only:
            categories.append("skills")

        if not categories:
            categories = ["agents", "commands", "skills", "prompts", "hooks"]

        reporter.print_header(
            f"{'[DRY RUN] ' if args.dry_run else ''}Sync Mode: "
            f"{'Global → Project' if args.pull else 'Project → Global'}"
        )

        sync_manager = SyncManager(
            project_dir=project_claude,
            global_dir=global_claude,
            reporter=reporter,
            dry_run=args.dry_run,
            force=args.force,
        )

        result = sync_manager.sync(
            direction=direction,
            categories=categories,
        )

        if result.success:
            reporter.print_success("\n✅ Sync completed successfully!")
            reporter.print_sync_summary(result.summary)
        else:
            reporter.print_error(f"\n❌ Sync failed: {result.error}")
            sys.exit(1)

    elif args.settings:
        # Settings analysis mode
        reporter.print_header("Settings Analysis")

        analyzer = SettingsAnalyzer(
            project_dir=project_claude,
            global_dir=global_claude,
            reporter=reporter,
        )

        result = analyzer.analyze()
        reporter.print_settings_analysis(result)

    else:
        # Audit mode (default)
        reporter.print_header("Audit Mode: Comparing Configurations")

        audit_manager = AuditManager(
            project_dir=project_claude,
            global_dir=global_claude,
            reporter=reporter,
        )

        result = audit_manager.audit()
        reporter.print_audit_summary(result)

        # Always run settings analysis in audit mode
        if not args.verbose:
            reporter.print_info("\n💡 Run with --settings for detailed settings analysis")


if __name__ == "__main__":
    main()
