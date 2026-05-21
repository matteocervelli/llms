"""
Bash command handler for PreToolUse hooks.

Responsibilities:
- Block dangerous commands (STRICT)
- Run pre-commit quality checks for git commit (GRACEFUL)
"""

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

# Import shared utilities
try:
    from handlers.notifications import send_notification
    from handlers.sounds import play_sound
except ImportError:

    def play_sound(sound_type: str) -> None:
        pass

    def send_notification(title: str, subtitle: str, message: str) -> None:
        pass


# Dangerous command patterns - STRICT blocking (exit 2)
DANGEROUS_PATTERNS = [
    (r"rm\s+-[rf]*[rf]\s+[/~]", "Blocked: rm -rf with root or home path"),
    (r"sudo\s+rm", "Blocked: sudo rm commands"),
    (r"chmod\s+777", "Blocked: chmod 777 (dangerous permissions)"),
    (r">\s*/etc/", "Blocked: Writing to /etc/"),
    (r"mkfs\.", "Blocked: mkfs filesystem commands"),
    (r"dd\s+if=.*of=/dev/", "Blocked: dd writing to device"),
    (r":\(\)\{:\|:&\};:", "Blocked: Fork bomb detected"),
    (r"curl.*\|\s*(ba)?sh", "Blocked: Piping curl to shell"),
    (r"wget.*\|\s*(ba)?sh", "Blocked: Piping wget to shell"),
    # Security gate - --no-verify/-n bypasses pre-commit hook that enforces security scan
    (
        r"git\s+commit.*(-n\b|--no-verify)",
        "Blocked: --no-verify/-n bypasses security gate (run /security-verify scan first)",
    ),
    # Destructive git operations — blocked unconditionally
    (
        r"git\s+reset\s+--hard",
        "Blocked: git reset --hard loses commits. Use git stash or git reset --soft instead.",
    ),
    (
        r"git\s+push\s+--force(?!-with-lease)",
        "Blocked: git push --force rewrites remote history. "
        "Use --force-with-lease for safer force push.",
    ),
    (
        r"git\s+push\s+-f\b",
        "Blocked: git push -f rewrites remote history. Use --force-with-lease.",
    ),
    # NOTE: git clean -f is checked in CLEAN_PATTERN below with -n exemption
    (
        r"git\s+checkout\s+--\s+\.",
        "Blocked: git checkout -- . discards all working changes. Use git stash instead.",
    ),
    (
        r"git\s+restore\s+\.",
        "Blocked: git restore . discards all working changes. Use git stash instead.",
    ),
    # NOTE: git branch -D is checked separately in CASE_SENSITIVE_PATTERNS below
    # because DANGEROUS_PATTERNS uses re.IGNORECASE and -d (safe) must not match.
    (
        r"git\s+submodule\s+deinit",
        "Blocked: git submodule deinit removes submodules. Confirm with user first.",
    ),
    (
        r"git\s+reflog\s+expire",
        "Blocked: git reflog expire purges recovery points. Never run this.",
    ),
    # Lockfile deletion — supply-chain guard (lockfile-safety.md)
    (
        r"\brm\b.*(pnpm-lock\.yaml|package-lock\.json|yarn\.lock|uv\.lock)",
        "Blocked [supply-chain]: lockfile deletion not allowed. Only the user can delete lockfiles in the terminal.",
    ),
    # Docker volume wipe — destroys local DB data
    (
        r"docker.*(compose|run).*\bdown\b.*(-v\b|--volumes)",
        "Blocked: docker compose down -v wipes ALL volumes (destroys local DB). Run manually in the terminal if intentional.",
    ),
    # _strip_quoted_strings removes $(...) subshell content before matching, so
    # VAR=$(secrets-cli read ...) and some_cmd $(secrets-cli read ...) are NOT blocked — only bare top-level calls are.
    (
        r"^\s*op\s+(read|get\s+item|item\s+get)\b",
        "Masked: secrets manager CLI (op, vault, aws) as a standalone command would print the secret into conversation context. "
        "Use in a subshell to keep it out of the transcript: "
        "VAR=$(secrets-cli read path/to/secret) or some_cmd --flag $(secrets-cli read path/to/secret). "
        "secrets manager CLI works fine — just not as a bare command.",
    ),
]


def _strip_quoted_strings(command: str) -> str:
    """Strip quoted string content to avoid false positives when strings mention flag names.

    Removes the text inside "...", '...', and $(...) so patterns only match
    against actual command flags, not embedded strings that happen to reference them.
    Preserves the quotes/delimiters so command structure remains recognizable.
    """
    # Strip double-quoted strings (handles escaped quotes inside)
    command = re.sub(r'"(?:[^"\\]|\\.)*"', '""', command, flags=re.DOTALL)
    # Strip single-quoted strings
    command = re.sub(r"'[^']*'", "''", command, flags=re.DOTALL)
    # Strip $(...) subshell content (non-greedy to handle multiple)
    command = re.sub(r"\$\(.*?\)", "$()", command, flags=re.DOTALL)
    return command


# Case-sensitive patterns — for flags where case matters (e.g. -D vs -d)
CASE_SENSITIVE_PATTERNS = [
    (
        r"git\s+branch\s+-[a-zA-Z]*D",
        "Blocked: git branch -D force-deletes without merge check. "
        "Use -d (lowercase) for safe delete.",
    ),
]


def _is_dangerous_git_clean(command: str) -> bool:
    """Check if git clean command is destructive (has -f but not -n dry-run)."""
    match = re.search(r"git\s+clean\s+((?:-[a-zA-Z]+\s*)+)", command, re.IGNORECASE)
    if not match:
        return False
    flags = match.group(1)
    has_force = bool(re.search(r"f", flags))
    has_dryrun = bool(re.search(r"n", flags))
    return has_force and not has_dryrun


def check_dangerous_command(command: str) -> str | None:
    """Check if command matches dangerous patterns."""
    # Strip quoted string content first to avoid matching flag names inside strings
    check_command = _strip_quoted_strings(command)
    for pattern, message in DANGEROUS_PATTERNS:
        if re.search(pattern, check_command, re.IGNORECASE):
            return message
    for pattern, message in CASE_SENSITIVE_PATTERNS:
        if re.search(pattern, check_command):
            return message
    # git clean -f without -n (dry-run exemption)
    if _is_dangerous_git_clean(check_command):
        return (
            "Blocked: git clean -f permanently deletes untracked files. "
            "Review with git clean -n first."
        )
    return None


def run_quality_checks(project_dir: str) -> str | None:
    """
    Run pre-commit quality checks for Python projects.
    Returns error message if checks fail, None if passed.
    GRACEFUL: Returns warning message but doesn't block.
    """
    project_path = Path(project_dir)

    # Check if Python project
    if not (project_path / "src").exists() and not (project_path / "tests").exists():
        return None

    # Get staged Python files
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=10,
        )
        staged_files = [f for f in result.stdout.strip().split("\n") if f.endswith(".py") and f]
    except Exception:
        return None

    if not staged_files:
        return None

    errors = []

    # Check ruff format
    try:
        result = subprocess.run(
            ["ruff", "format", "--check", "--quiet"] + staged_files,
            cwd=project_dir,
            capture_output=True,
            timeout=30,
        )
        if result.returncode != 0:
            errors.append("Formatting issues (run: ruff format)")
    except Exception:
        pass

    # Check ruff lint
    try:
        result = subprocess.run(
            ["ruff", "check", "--quiet"] + staged_files,
            cwd=project_dir,
            capture_output=True,
            timeout=30,
        )
        if result.returncode != 0:
            errors.append("Linting issues (run: ruff check --fix)")
    except Exception:
        pass

    if errors:
        return f"Quality check warnings: {', '.join(errors)}"

    return None


# Extensions that carry no executable risk — scan not needed
_CONFIG_ONLY_EXTENSIONS = {".md", ".yaml", ".yml", ".txt", ".toml", ".rst", ".json"}
# Extensions that always require a scan
_CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".sh",
    ".rb",
    ".go",
    ".rs",
    ".java",
    ".c",
    ".cpp",
    ".cs",
    ".mjs",
    ".cjs",
}


def _extract_git_add_files(command: str) -> list[str]:
    """Extract filenames from a `git add <files>` fragment in a compound command.

    Handles `git add a.md b.md && git commit` patterns. Returns [] if no git add found
    or if `git add .` / `-A` / `--all` is used (can't enumerate files safely).
    """
    match = re.search(r"git add\s+(.+?)(?:\s*(?:&&|;|\|)\s*|$)", command)
    if not match:
        return []
    args = match.group(1).strip()
    parts = args.split()
    # Flags like -A, --all, -u, --update mean "all files" — can't enumerate safely
    if any(p.startswith("-") for p in parts):
        return []
    # Filter out empty strings
    return [p for p in parts if p]


def _scan_is_fresh(cwd: str) -> bool:
    """Return True if /security-verify scan was run for the current HEAD in this repo."""
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=5,
        ).stdout.strip()
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=5,
        ).stdout.strip()
        repo_hash = hashlib.md5(root.encode()).hexdigest()[:8]  # nosec B324 — non-crypto, temp file naming only
        return os.path.exists(f"/tmp/security-scan-{repo_hash}-{sha}")
    except Exception:
        return False


def is_config_only_commit(cwd: str, command: str = "") -> bool:
    """Return True if every staged file is a config/doc file (no executable code).

    Checks both the current git staged area AND any files being added in the same
    compound command (e.g. `git add a.md && git commit`), since PreToolUse fires
    before the command executes so git diff --cached may not yet reflect the adds.

    Qualifies when ALL candidate files have extensions in _CONFIG_ONLY_EXTENSIONS
    AND none have extensions in _CODE_EXTENSIONS. Unrecognised extensions are
    treated conservatively (not config-only → scan required).
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        staged = [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]
    except Exception:
        return False

    # Also include files declared in `git add` in the same command (not yet staged)
    pending = _extract_git_add_files(command)
    all_files = list({*staged, *pending})  # deduplicate

    if not all_files:
        return False  # nothing staged — don't suppress, something unexpected

    for filepath in all_files:
        ext = Path(filepath).suffix.lower()
        if ext in _CODE_EXTENSIONS:
            return False
        if ext not in _CONFIG_ONLY_EXTENSIONS:
            return False  # unknown extension → be conservative

    return True


def check_supply_chain(command: str) -> str | None:
    """
    Check for unguarded supply-chain risky commands.

    Exemptions:
    - Commands prefixed with 'sfw' (Socket Firewall active)
    - 'uv sync --frozen' / 'uv sync --locked' (no live resolution)
    - 'pnpm install --frozen-lockfile' (no live resolution)
    """
    stripped = _strip_quoted_strings(command).strip()

    # sfw-prefixed: Socket Firewall wraps the command — safe
    if re.match(r"sfw\s+", stripped, re.IGNORECASE):
        return None

    # uv sync without --frozen/--locked performs live dependency resolution
    if re.search(r"\buv\s+sync\b", stripped, re.IGNORECASE):
        if not re.search(r"--frozen|--locked", stripped):
            return (
                "SUPPLY CHAIN ALERT: 'uv sync' without --frozen/--locked re-resolves deps. "
                "Use 'uv sync --frozen' or 'sfw uv sync'."
            )
        return None

    uv_add = re.search(r"\buv\s+add\s+(\S+)", stripped, re.IGNORECASE)
    if uv_add:
        first_arg = uv_add.group(1)
        if not first_arg.startswith("-"):
            return "SUPPLY CHAIN ALERT: 'uv add' blocked for external packages. "
        return None

    # pip install
    if re.search(r"\bpip(?:3)?\s+install\b", stripped, re.IGNORECASE):
        return "SUPPLY CHAIN ALERT: 'pip install' blocked. Use 'sfw pip install <pkg>' or 'uv add <pkg>'."

    # npm install/ci/add
    if re.search(r"\bnpm\s+(install|ci|add)\b", stripped, re.IGNORECASE):
        return (
            "SUPPLY CHAIN ALERT: 'npm install/add' blocked. "
            "Use 'sfw npm install' or 'pnpm install --frozen-lockfile'."
        )

    # pnpm install/add without --frozen-lockfile
    if re.search(r"\bpnpm\s+(install|add)\b", stripped, re.IGNORECASE):
        if not re.search(r"--frozen-lockfile", stripped):
            return (
                "SUPPLY CHAIN ALERT: 'pnpm install/add' without --frozen-lockfile blocked. "
                "Use 'pnpm install --frozen-lockfile' or 'sfw pnpm install'."
            )

    # yarn install/add
    if re.search(r"\byarn\s+(install|add)\b", stripped, re.IGNORECASE):
        return "SUPPLY CHAIN ALERT: 'yarn install/add' blocked. Use 'sfw yarn install'."

    # pip-sync
    if re.search(r"\bpip-sync\b", stripped, re.IGNORECASE):
        return "SUPPLY CHAIN ALERT: 'pip-sync' blocked. Use 'sfw pip-sync'."

    return None


def handle_pretool(data: dict) -> dict:
    """
    Handle PreToolUse[Bash] events.

    - STRICT: Block dangerous commands and supply-chain risks
    - GRACEFUL: Warn on quality issues
    """
    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")
    cwd = data.get("cwd", "")

    # Check for dangerous commands - STRICT blocking
    danger_msg = check_dangerous_command(command)
    if danger_msg:
        project = Path(cwd).name if cwd else "Unknown"
        play_sound("blocked")
        send_notification(f"Claude Code - {project}", "Command Blocked", danger_msg)
        print(danger_msg, file=sys.stderr)
        sys.exit(2)  # Block tool execution

    # Check for supply-chain risks - STRICT blocking
    supply_msg = check_supply_chain(command)
    if supply_msg:
        project = Path(cwd).name if cwd else "Unknown"
        play_sound("blocked")
        send_notification(f"Claude Code - {project}", "Supply Chain Alert", supply_msg)
        print(supply_msg, file=sys.stderr)
        sys.exit(2)

    # Check for git commit - run quality checks + security reminder (GRACEFUL)
    if "git commit" in command and cwd:
        warning = run_quality_checks(cwd)
        context_parts = []
        if warning:
            context_parts.append(warning)

        # Hard block if code files staged and scan not fresh.
        # Config-only commits (md/yaml/txt/toml) are exempt — no executable risk.
        if not is_config_only_commit(cwd, command) and not _scan_is_fresh(cwd):
            play_sound("blocked")
            send_notification(
                Path(cwd).name if cwd else "Unknown",
                "Security Gate",
                "Run /security-verify scan before committing code.",
            )
            print(
                "Blocked: /security-verify scan required before committing code files. "
                "Run /security-verify scan, then retry.",
                file=sys.stderr,
            )
            sys.exit(2)

        if context_parts:
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": " | ".join(context_parts),
                }
            }

    return {}
