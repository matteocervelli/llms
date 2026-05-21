"""Colored console output reporter for the sync tool.

Provides formatted output with ANSI colors, tables, and progress indicators
for sync operations, audits, and settings analysis.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Colors:
    """ANSI color codes for terminal output."""
    SUCCESS = '\033[92m'      # Green
    WARNING = '\033[93m'      # Yellow
    PROJECT = '\033[94m'      # Blue
    GLOBAL = '\033[96m'       # Cyan
    ERROR = '\033[91m'        # Red
    RESET = '\033[0m'         # Reset
    BOLD = '\033[1m'          # Bold


class Reporter:
    """Colored console output reporter for sync operations.

    Provides methods for printing headers, status messages, tables,
    and summary statistics with ANSI color codes.
    """

    def __init__(self, verbose: bool = False):
        """Initialize reporter with verbosity setting.

        Args:
            verbose: If True, print additional diagnostic information.
        """
        self.verbose = verbose

    def print_header(self, text: str) -> None:
        """Print section header with bold formatting.

        Args:
            text: Header text to display.
        """
        print(f"\n{Colors.BOLD}{'=' * 60}")
        print(f"{text}")
        print(f"{'=' * 60}{Colors.RESET}\n")

    def print_success(self, text: str) -> None:
        """Print success message in green.

        Args:
            text: Message to display.
        """
        print(f"{Colors.SUCCESS}✅ {text}{Colors.RESET}")

    def print_error(self, text: str) -> None:
        """Print error message in red.

        Args:
            text: Error message to display.
        """
        print(f"{Colors.ERROR}❌ {text}{Colors.RESET}")

    def print_warning(self, text: str) -> None:
        """Print warning message in yellow.

        Args:
            text: Warning message to display.
        """
        print(f"{Colors.WARNING}⚠️  {text}{Colors.RESET}")

    def print_info(self, text: str) -> None:
        """Print info message in cyan.

        Args:
            text: Information message to display.
        """
        print(f"{Colors.GLOBAL}ℹ️  {text}{Colors.RESET}")

    def print_project_only(self, text: str) -> None:
        """Print message for project-only items in blue.

        Args:
            text: Message to display.
        """
        print(f"{Colors.PROJECT}📤 {text}{Colors.RESET}")

    def print_global_only(self, text: str) -> None:
        """Print message for global-only items in cyan.

        Args:
            text: Message to display.
        """
        print(f"{Colors.GLOBAL}📥 {text}{Colors.RESET}")

    def print_table(self, headers: List[str], rows: List[List[str]]) -> None:
        """Print formatted table with aligned columns.

        Args:
            headers: List of column headers.
            rows: List of rows, each row is a list of cell values.
        """
        if not rows:
            print("  (no items)")
            return

        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Print header
        header_line = "  " + " | ".join(
            h.ljust(w) for h, w in zip(headers, col_widths)
        )
        print(header_line)
        print("  " + "-" * (len(header_line) - 2))

        # Print rows
        for row in rows:
            row_line = "  " + " | ".join(
                str(cell).ljust(w) for cell, w in zip(row, col_widths)
            )
            print(row_line)

    def print_file_list(self, files: List[str], status: str) -> None:
        """Print list of files with status icon.

        Args:
            files: List of file paths.
            status: Status type ('success', 'warning', 'project', 'global', 'error').
        """
        if not files:
            return

        icon_map = {
            'success': (Colors.SUCCESS, '✅'),
            'warning': (Colors.WARNING, '⚠️'),
            'project': (Colors.PROJECT, '📤'),
            'global': (Colors.GLOBAL, '📥'),
            'error': (Colors.ERROR, '❌'),
        }

        color, icon = icon_map.get(status, (Colors.GLOBAL, 'ℹ️'))

        for file_path in files:
            print(f"{color}{icon} {file_path}{Colors.RESET}")

    def print_audit_summary(self, audit_result) -> None:
        """Print audit summary with statistics.

        Args:
            audit_result: AuditResult dataclass with audit results
        """
        self.print_header("Audit Summary")

        # Get counts from lists
        total = audit_result.total_files
        in_sync_count = len(audit_result.in_sync)
        conflicts_count = len(audit_result.conflicts)
        project_only_count = len(audit_result.project_only)
        global_only_count = len(audit_result.global_only)
        errors_count = len(audit_result.errors)

        print(f"  Total files checked: {total}")
        self.print_success(f"  ✅ In sync: {in_sync_count}")

        if conflicts_count > 0:
            self.print_warning(f"  ⚠️  Conflicts: {conflicts_count}")
            if self.verbose:
                for file in audit_result.conflicts:
                    print(f"      - {file}")

        if project_only_count > 0:
            self.print_project_only(f"  📤 Project-only: {project_only_count}")
            if self.verbose:
                for file in audit_result.project_only:
                    print(f"      - {file}")

        if global_only_count > 0:
            self.print_global_only(f"  📥 Global-only: {global_only_count}")
            if self.verbose:
                for file in audit_result.global_only:
                    print(f"      - {file}")

        if errors_count > 0:
            self.print_error(f"  ❌ Errors: {errors_count}")
            for error in audit_result.errors:
                print(f"      - {error}")

        # Sync status
        print()
        if audit_result.is_in_sync:
            self.print_success("✅ All configurations are in sync!")
        else:
            self.print_warning("⚠️  Configuration differences detected.")
            print()
            print("  Run sync commands:")
            print("    make sync-push      # Sync project → global")
            print("    make sync-pull      # Sync global → project")
            print("    make sync-dry       # Preview changes")

    def print_sync_summary(self, sync_result) -> None:
        """Print sync summary with operations performed.

        Args:
            sync_result: SyncResult dataclass or dict with summary data
        """
        self.print_header("Sync Summary")

        # Handle both dict and SyncResult dataclass
        if hasattr(sync_result, 'summary'):
            summary = sync_result.summary
            files_copied = len(sync_result.files_copied)
            files_skipped = len(sync_result.files_skipped)
            errors = sync_result.errors
            conflicts = sync_result.conflicts_resolved
        else:
            summary = sync_result
            files_copied = summary.get('copied', 0)
            files_skipped = summary.get('skipped', 0)
            errors = summary.get('errors', [])
            conflicts = summary.get('conflicts_resolved', {})

        print(f"  Files copied: {files_copied}")
        print(f"  Files skipped: {files_skipped}")
        print(f"  Conflicts resolved: {len(conflicts)}")
        print()

        if conflicts:
            print("  Conflict resolutions:")
            for file, action in conflicts.items():
                print(f"    - {file}: {action}")
            print()

        if errors:
            self.print_error(f"  ❌ Errors encountered: {len(errors)}")
            for error in errors:
                print(f"      - {error}")
        else:
            self.print_success("  ✅ Sync completed successfully!")

    def print_settings_analysis(self, settings_result) -> None:
        """Print settings comparison analysis.

        Args:
            settings_result: SettingsAnalysis dataclass with analysis results
        """
        self.print_header("Settings Analysis")

        # Hooks differences
        if settings_result.hooks_differences:
            print("\n  📋 Hooks Differences:")
            for diff in settings_result.hooks_differences:
                print(f"    - {diff}")

        # Permissions differences
        if settings_result.permission_differences:
            print("\n  🔐 Permission Differences:")
            for diff in settings_result.permission_differences:
                print(f"    - {diff}")

        # Plugin differences
        if settings_result.plugin_differences:
            print("\n  🔌 Plugin Differences:")
            for diff in settings_result.plugin_differences:
                print(f"    - {diff}")

        # Recommendations
        if settings_result.recommendations:
            print("\n  💡 Recommendations:")
            for rec in settings_result.recommendations:
                self.print_info(f"    - {rec}")

        if not (settings_result.hooks_differences or
                settings_result.permission_differences or
                settings_result.plugin_differences):
            self.print_success("\n  ✅ All settings are in sync!")
        print()

    def print_verbose(self, text: str) -> None:
        """Print verbose diagnostic information if verbose mode is enabled.

        Args:
            text: Diagnostic message to display.
        """
        if self.verbose:
            print(f"{Colors.GLOBAL}[DEBUG] {text}{Colors.RESET}")

    def print_section(self, title: str, items: List[str],
                     icon: str = "•") -> None:
        """Print a section with title and bulleted items.

        Args:
            title: Section title.
            items: List of items to display.
            icon: Icon to use for each item (default: bullet point).
        """
        if not items:
            return

        print(f"\n  {title}:")
        for item in items:
            print(f"    {icon} {item}")
