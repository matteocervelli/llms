"""
Plan mode handler for PostToolUse hook.

Fires after ExitPlanMode (plan approved by user). Injects a mandatory
systemMessage requiring TaskCreate before any implementation begins.
This enforces the CLAUDE.md rule ("start every non-trivial implementation
by creating tasks") at the hook level, where it can't be skipped.
"""


def handle_posttool(data: dict) -> dict:
    """Return systemMessage forcing task list creation after plan approval."""
    return {
        "systemMessage": (
            "TASK LIST REQUIRED — Plan approved.\n"
            "Before writing any code, calling Edit/Write, or running Bash:\n"
            "1. Call TaskCreate for EACH major step in the approved plan\n"
            "2. Call TaskUpdate to mark the first task as in_progress\n"
            "Skip only if the plan has a single trivial step (≤5 min of work).\n"
            "This is mandatory per CLAUDE.md workflow rules."
        )
    }
