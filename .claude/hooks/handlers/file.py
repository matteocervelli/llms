"""
File handler for PreToolUse and PostToolUse hooks.

PreToolUse responsibilities:
- Block .env / secrets / key file modifications (STRICT)
- Block .git directory modifications (STRICT)
- Block lock file edits (STRICT)
- Block reads of secrets / keys / auth files (STRICT) via handle_pretool_read()

PostToolUse responsibilities:
- Auto-format files based on extension (GRACEFUL)
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from handlers.notifications import send_notification
    from handlers.sounds import play_sound
except ImportError:

    def play_sound(sound_type: str) -> None:
        pass

    def send_notification(title: str, subtitle: str, message: str) -> None:
        pass


# Protected file patterns for Edit/Write - STRICT blocking
BLOCKED_FILES = [
    (
        r"\.env($|\.(?!example$|test$))",
        "Blocked: Cannot modify .env files (credentials)",
    ),
    (r"\.dev\.vars$", "Blocked: Cannot modify .dev.vars files (credentials)"),
    (r"\.git/", "Blocked: Cannot modify .git directory"),
    (r"\.ssh/", "Blocked: Cannot modify .ssh directory"),
    (r"credentials\.", "Blocked: Cannot modify credentials files"),
    (r"secrets?\.", "Blocked: Cannot modify secrets files"),
    (r"\.npmrc$", "Blocked: Cannot modify .npmrc (auth tokens)"),
    (r"\.pypirc$", "Blocked: Cannot modify .pypirc (auth tokens)"),
    (r"\.pem$", "Blocked: Cannot modify PEM key files"),
    (r"\.key$", "Blocked: Cannot modify private key files"),
    # Lock files - auto-generated, use package manager instead
    (r"package-lock\.json$", "Blocked: Don't edit lock files. Run npm install instead"),
    (r"yarn\.lock$", "Blocked: Don't edit lock files. Run yarn install instead"),
    (r"pnpm-lock\.yaml$", "Blocked: Don't edit lock files. Run pnpm install instead"),
    (r"Gemfile\.lock$", "Blocked: Don't edit lock files. Run bundle install instead"),
    (r"poetry\.lock$", "Blocked: Don't edit lock files. Run poetry lock instead"),
    (r"uv\.lock$", "Blocked: Don't edit lock files. Run uv lock instead"),
    (r"Pipfile\.lock$", "Blocked: Don't edit lock files. Run pipenv lock instead"),
    (r"Cargo\.lock$", "Blocked: Don't edit lock files. Run cargo build instead"),
    (
        r"composer\.lock$",
        "Blocked: Don't edit lock files. Run composer install instead",
    ),
]

# Protected file patterns for Read - STRICT blocking
# Deny list in settings.json covers .env*, .dev.vars*, .pem, .key, .npmrc, .pypirc.
# These patterns add defense-in-depth and cover paths not matched by settings deny globs.
BLOCKED_READ_PATTERNS = [
    (
        r"(^|[/\\])\.env($|\.(?!example|test)[^/\\]*$)",
        "Blocked: cannot read .env files (secrets)",
    ),
    (r"(^|[/\\])\.dev\.vars$", "Blocked: cannot read .dev.vars (credentials)"),
    (r"\.pem$", "Blocked: cannot read PEM key files"),
    (r"\.key$", "Blocked: cannot read private key files"),
    (r"(^|[/\\])\.npmrc$", "Blocked: cannot read .npmrc (auth tokens)"),
    (r"(^|[/\\])\.pypirc$", "Blocked: cannot read .pypirc (auth tokens)"),
    (r"(^|[/\\])\.ssh([/\\]|$)", "Blocked: cannot read .ssh directory"),
    (r"(^|[/\\])\.aws([/\\]|$)", "Blocked: cannot read .aws directory"),
    (r"(^|[/\\])secrets([/\\]|$)", "Blocked: cannot read secrets directory"),
    (r"(^|[/\\])credentials\.", "Blocked: cannot read credentials files"),
]

# Formatter configuration: extension -> [command, args...]
FORMATTERS = {
    ".py": ["ruff", "format", "--quiet"],
    ".js": ["prettier", "--write"],
    ".jsx": ["prettier", "--write"],
    ".ts": ["prettier", "--write"],
    ".tsx": ["prettier", "--write"],
    ".json": ["prettier", "--write"],
    ".css": ["prettier", "--write"],
    ".scss": ["prettier", "--write"],
    ".md": ["prettier", "--write"],
    ".yaml": ["prettier", "--write"],
    ".yml": ["prettier", "--write"],
    ".sh": ["shfmt", "-w"],
    ".bash": ["shfmt", "-w"],
}


def check_blocked_file(file_path: str) -> str | None:
    """Check if file matches blocked patterns."""
    for pattern, message in BLOCKED_FILES:
        if re.search(pattern, file_path):
            return message
    return None


def format_file(file_path: str) -> str | None:
    """
    Format file based on extension.
    Returns warning message if formatting failed, None on success.
    """
    path = Path(file_path)
    if not path.exists():
        return None

    ext = path.suffix.lower()
    if ext not in FORMATTERS:
        return None

    formatter_cmd = FORMATTERS[ext]
    formatter_bin = formatter_cmd[0]

    # Check if formatter is available
    if not shutil.which(formatter_bin):
        # Try npx for node-based formatters
        if formatter_bin in ["prettier"]:
            formatter_cmd = ["npx"] + formatter_cmd
            if not shutil.which("npx"):
                return None
        else:
            return None

    try:  # noqa: SIM105 — intentional pass; formatter failure should not block hook
        subprocess.run(
            formatter_cmd + [str(file_path)],
            capture_output=True,
            timeout=10,
        )
    except Exception:  # noqa: BLE001
        pass

    return None


def handle_pretool(data: dict) -> dict:
    """
    Handle PreToolUse[Edit|Write] events.

    - STRICT: Block protected files
    """
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    cwd = data.get("cwd", "")

    if not file_path:
        return {}

    # Check for blocked files - STRICT
    block_msg = check_blocked_file(file_path)
    if block_msg:
        project = Path(cwd).name if cwd else "Unknown"
        play_sound("blocked")
        send_notification(f"Claude Code - {project}", "File Blocked", block_msg)
        print(block_msg, file=sys.stderr)
        sys.exit(2)  # Block tool execution

    return {}


def handle_pretool_read(data: dict) -> dict:
    """
    Handle PreToolUse[Read] events.

    - STRICT: Block reads of secrets, keys, auth files
    """
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    cwd = data.get("cwd", "")

    if not file_path:
        return {}

    normalized = file_path.replace("\\", "/")
    for pattern, message in BLOCKED_READ_PATTERNS:
        if re.search(pattern, normalized):
            project = Path(cwd).name if cwd else "Unknown"
            play_sound("blocked")
            send_notification(f"Claude Code - {project}", "Read Blocked", message)
            print(message, file=sys.stderr)
            sys.exit(2)

    return {}


def handle_posttool(data: dict) -> dict:
    """
    Handle PostToolUse[Edit|Write] events.

    - GRACEFUL: Auto-format files silently
    """
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if file_path and file_path != "/dev/null":
        format_file(file_path)

    return {}
