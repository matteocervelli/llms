#!/usr/bin/env python3
"""
Claude Code Unified Hook Handler

Main dispatcher for all hook events. Routes to specialized handlers based on CLI args.

Usage:
    hook_handler.py pretool bash     # PreToolUse for Bash commands
    hook_handler.py pretool file     # PreToolUse for Edit/Write
    hook_handler.py posttool bash     # PostToolUse for Bash commands
    hook_handler.py posttool file     # PostToolUse for Edit/Write
    hook_handler.py posttool context  # PostToolUse wildcard — context window monitor
    hook_handler.py session start     # SessionStart
    hook_handler.py session end      # SessionEnd
    hook_handler.py stop             # Stop event
    hook_handler.py notification     # Notification event
"""

import json
import sys
from pathlib import Path

# Add hooks/ and hooks/handlers/ so bare imports in handlers/ resolve correctly
HOOKS_DIR = Path(__file__).parent
HANDLERS_DIR = HOOKS_DIR / "handlers"
sys.path.insert(0, str(HANDLERS_DIR))
sys.path.insert(0, str(HOOKS_DIR))


def load_input() -> dict:
    """Read JSON input from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def output_result(result: dict) -> None:
    """Output JSON result to stdout."""
    if result:
        print(json.dumps(result))


def main():
    if len(sys.argv) < 2:
        print("Usage: hook_handler.py <event> [type]", file=sys.stderr)
        sys.exit(1)

    event = sys.argv[1]
    event_type = sys.argv[2] if len(sys.argv) > 2 else None

    # Load input data
    data = load_input()

    # Route to appropriate handler
    result = {}

    try:
        if event == "pretool":
            if event_type == "bash":
                from handlers.bash import handle_pretool

                result = handle_pretool(data)
            elif event_type == "file":
                from handlers.file import handle_pretool

                result = handle_pretool(data)
            elif event_type == "read":
                from handlers.file import handle_pretool_read

                result = handle_pretool_read(data)

        elif event == "posttool":
            if event_type == "bash":
                from handlers.git import handle_posttool

                result = handle_posttool(data)
            elif event_type == "file":
                from handlers.file import handle_posttool

                result = handle_posttool(data)
            elif event_type == "plan":
                from handlers.plan import handle_posttool

                result = handle_posttool(data)
            elif event_type == "context":
                from handlers.context_monitor import handle_posttool

                result = handle_posttool(data)

        elif event == "session":
            from handlers.session import handle_session

            result = handle_session(data, event_type)

        elif event == "stop":
            # Stop hook - write mechanical stub + remind Claude to enhance
            from handlers.memory import handle_pre_compact

            result = handle_pre_compact(data)

        elif event == "notification":
            from handlers.notifications import handle_notification

            result = handle_notification(data)

    except ImportError as e:
        # Handler not found - allow operation
        result = {"systemMessage": f"Hook handler not found: {e}"}
    except Exception as e:
        # Any error - allow operation but log
        result = {"systemMessage": f"Hook error: {e}"}

    output_result(result)
    sys.exit(0)


if __name__ == "__main__":
    main()
