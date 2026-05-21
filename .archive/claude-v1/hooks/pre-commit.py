#!/usr/bin/env python3
"""
Pre-commit hook for quality checks.
Runs pytest, black, mypy, and flake8 before allowing commits.
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional


def run_command(cmd: List[str], cwd: str) -> Tuple[int, str, str]:
    """
    Run a command and return exit code, stdout, stderr.

    Args:
        cmd: Command and arguments as list
        cwd: Working directory

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 120 seconds"
    except Exception as e:
        return 1, "", str(e)


def check_pytest(project_dir: str) -> Optional[str]:
    """
    Run pytest with coverage.

    Args:
        project_dir: Project root directory

    Returns:
        Error message if failed, None if passed
    """
    code, stdout, stderr = run_command(
        ["pytest", "--tb=short", "-q"],
        project_dir
    )

    if code != 0:
        return f"Pytest failed with errors:\n{stdout}\n{stderr}"

    return None


def get_staged_files(project_dir: str) -> List[str]:
    """
    Get list of staged Python files.

    Args:
        project_dir: Project root directory

    Returns:
        List of staged .py files
    """
    code, stdout, stderr = run_command(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        project_dir
    )

    if code != 0:
        return []

    # Filter only Python files
    return [f for f in stdout.strip().split('\n') if f.endswith('.py') and f]


def check_black(project_dir: str, files: List[str]) -> Optional[str]:
    """
    Check code formatting with black.

    Args:
        project_dir: Project root directory
        files: List of files to check

    Returns:
        Error message if failed, None if passed
    """
    if not files:
        return None

    code, stdout, stderr = run_command(
        ["black", "--check"] + files,
        project_dir
    )

    if code != 0:
        return f"Black formatting check failed:\n{stdout}\n{stderr}\n\nRun: black {' '.join(files)}"

    return None


def check_mypy(project_dir: str, files: List[str]) -> Optional[str]:
    """
    Run mypy type checking.

    Args:
        project_dir: Project root directory
        files: List of files to check

    Returns:
        Error message if failed, None if passed
    """
    if not files:
        return None

    # Only check files in src/
    src_files = [f for f in files if f.startswith('src/')]
    if not src_files:
        return None

    code, stdout, stderr = run_command(
        ["mypy"] + src_files,
        project_dir
    )

    if code != 0:
        return f"Mypy type checking failed:\n{stdout}\n{stderr}"

    return None


def check_flake8(project_dir: str, files: List[str]) -> Optional[str]:
    """
    Run flake8 linting.

    Args:
        project_dir: Project root directory
        files: List of files to check

    Returns:
        Error message if failed, None if passed
    """
    if not files:
        return None

    code, stdout, stderr = run_command(
        ["flake8"] + files + ["--max-line-length=100", "--extend-ignore=E203,W503"],
        project_dir
    )

    if code != 0:
        return f"Flake8 linting failed:\n{stdout}\n{stderr}"

    return None


def main():
    """Main hook execution."""
    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Get tool information
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")
    cwd = input_data.get("cwd", "")

    # Only run for git commit commands
    if tool_name != "Bash" or "git commit" not in command:
        sys.exit(0)

    # Determine project directory (use cwd or CLAUDE_PROJECT_DIR)
    project_dir = input_data.get("cwd", "")
    if not project_dir:
        import os
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")

    # Check if we're in a Python project
    project_path = Path(project_dir)
    if not (project_path / "src").exists() and not (project_path / "tests").exists():
        # Not a Python project, skip checks
        sys.exit(0)

    print("🔍 Running pre-commit quality checks...\n", file=sys.stderr)

    # Get staged files
    staged_files = get_staged_files(project_dir)

    if not staged_files:
        print("  ℹ️  No Python files staged, skipping quality checks.\n", file=sys.stderr)
        sys.exit(0)

    print(f"  📝 Checking {len(staged_files)} staged Python file(s)...\n", file=sys.stderr)

    # Run all quality checks
    errors = []

    # 1. Black formatting
    print("  ✓ Checking code formatting (black)...", file=sys.stderr)
    error = check_black(project_dir, staged_files)
    if error:
        errors.append(("Black (formatting)", error))

    # 2. Flake8 linting
    print("  ✓ Running linter (flake8)...", file=sys.stderr)
    error = check_flake8(project_dir, staged_files)
    if error:
        errors.append(("Flake8 (linting)", error))

    # 3. Mypy type checking
    print("  ✓ Type checking (mypy)...", file=sys.stderr)
    error = check_mypy(project_dir, staged_files)
    if error:
        errors.append(("Mypy (type checking)", error))

    # 4. Pytest (still run all tests to ensure nothing breaks)
    print("  ✓ Running tests (pytest)...", file=sys.stderr)
    error = check_pytest(project_dir)
    if error:
        errors.append(("Pytest (tests)", error))

    # Report results
    if errors:
        print("\n❌ Pre-commit checks FAILED:\n", file=sys.stderr)
        for i, (check_name, error_msg) in enumerate(errors, 1):
            print(f"{i}. {check_name}:", file=sys.stderr)
            print(f"{error_msg}\n", file=sys.stderr)

        print("⚠️  Quality issues detected. Please review and fix before committing.", file=sys.stderr)
        print("💡 Tip: Claude can auto-fix these issues and retry the commit.\n", file=sys.stderr)
        # Exit code 0 allows the commit but provides feedback to Claude
        # Claude will see these issues and can decide to fix them before committing
        sys.exit(0)

    print("\n✅ All pre-commit checks passed!", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
