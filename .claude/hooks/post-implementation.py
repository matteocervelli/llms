#!/usr/bin/env python3
"""
Post-implementation hook for triggering validation workflow.
Runs after implementation phase completes to validate code quality,
test coverage, performance, and security.
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Optional


def check_if_implementation_complete(transcript_path: str) -> bool:
    """
    Check if implementation phase is complete by analyzing the transcript.

    Args:
        transcript_path: Path to the conversation transcript

    Returns:
        True if implementation is complete, False otherwise
    """
    try:
        if not Path(transcript_path).exists():
            return False

        # Read the last few lines of the transcript
        with open(transcript_path, 'r') as f:
            lines = f.readlines()

        # Look for implementation completion markers
        recent_messages = ''.join(lines[-50:]).lower() if len(lines) > 50 else ''.join(lines).lower()

        # Check for completion indicators
        completion_markers = [
            "implementation complete",
            "implementation phase complete",
            "phase 3: implementation",
            "all tests pass",
            "tests passing",
            "ready for validation",
        ]

        return any(marker in recent_messages for marker in completion_markers)

    except Exception:
        return False


def get_project_type(project_dir: str) -> Optional[str]:
    """
    Determine the project type.

    Args:
        project_dir: Project root directory

    Returns:
        Project type ('python', 'javascript', etc.) or None
    """
    project_path = Path(project_dir)

    if (project_path / "pyproject.toml").exists() or (project_path / "setup.py").exists():
        return "python"
    elif (project_path / "package.json").exists():
        return "javascript"

    return None


def main():
    """Main hook execution."""
    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Get hook event information
    hook_event = input_data.get("hook_event_name", "")
    transcript_path = input_data.get("transcript_path", "")
    cwd = input_data.get("cwd", "")
    stop_hook_active = input_data.get("stop_hook_active", False)

    # Only run on Stop or SubagentStop events
    if hook_event not in ["Stop", "SubagentStop"]:
        sys.exit(0)

    # Prevent infinite loops
    if stop_hook_active:
        sys.exit(0)

    # Check if we should trigger validation
    if not check_if_implementation_complete(transcript_path):
        # Implementation not complete yet
        sys.exit(0)

    # Determine project directory
    import os
    project_dir = cwd or os.environ.get("CLAUDE_PROJECT_DIR", ".")

    # Check project type
    project_type = get_project_type(project_dir)
    if not project_type:
        # Not a supported project type
        sys.exit(0)

    print("\n🎯 Implementation complete! Triggering validation workflow...\n", file=sys.stderr)

    # Create validation prompt for Claude
    validation_prompt = """
Now that implementation is complete, please run the comprehensive validation workflow:

1. **Code Quality Checks**:
   - Run black for code formatting
   - Run mypy for type checking
   - Run flake8 for linting
   - Ensure all checks pass

2. **Test Coverage**:
   - Run pytest with coverage report
   - Verify >= 80% code coverage target
   - Ensure all tests are passing

3. **Performance Validation**:
   - Check response times are within acceptable limits
   - Verify no performance regressions
   - Profile resource usage if applicable

4. **Security Assessment**:
   - Verify input validation is implemented
   - Check for security vulnerabilities
   - Ensure no secrets in code
   - Validate authentication/authorization if applicable

5. **Acceptance Criteria**:
   - Review all requirements from the GitHub issue
   - Confirm each criterion is met
   - Document any deviations or notes

6. **Generate Validation Report**:
   - Summarize all validation results
   - Document pass/fail status for each check
   - Provide metrics and measurements
   - List any issues that need to be addressed

Please proceed with the validation workflow using the @validation skill.
"""

    # Output the validation prompt
    # For Stop/SubagentStop hooks, use JSON output to block stopping
    # and provide a reason for Claude to continue
    output = {
        "decision": "block",
        "reason": validation_prompt.strip()
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
