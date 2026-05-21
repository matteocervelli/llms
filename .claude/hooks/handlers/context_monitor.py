"""
Context window monitor — PostToolUse hook (wildcard).

Reads token usage from the JSONL transcript after every tool call,
computes effective context window utilization, and injects warnings
at configurable thresholds.

  WARNING  (≥65% used) → additionalContext soft nudge + context_warning.wav
  CRITICAL (≥75% used) → systemMessage mandatory stop + attention.wav

GRACEFUL: Never blocks tool calls. Returns {} on any error.
"""

import json
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MAX_CONTEXT_TOKENS = 200_000  # Sonnet 4.6 / Opus 4.6
WARNING_THRESHOLD = 0.65  # ≥65% used
CRITICAL_THRESHOLD = 0.75  # ≥75% used
DEBOUNCE_CALLS = 5  # suppress re-fires for N tool calls
TAIL_BYTES = 65_536  # 64 KB tail read — avoids loading multi-MB transcripts

# Patchable in tests
PROJECTS_DIR = Path.home() / ".claude" / "projects"
DEBOUNCE_DIR = Path("/tmp")

# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _encode_cwd(cwd: str) -> str:
    """Convert /Users/foo/bar to -Users-foo-bar (Claude project path encoding)."""
    return cwd.replace("/", "-")


def _find_transcript(cwd: str) -> "Path | None":
    """Find the most recently modified .jsonl transcript for the given cwd."""
    encoded = _encode_cwd(cwd)
    project_dir = PROJECTS_DIR / encoded
    if not project_dir.exists():
        return None
    jsonl_files = list(project_dir.glob("*.jsonl"))
    if not jsonl_files:
        return None
    return max(jsonl_files, key=lambda p: p.stat().st_mtime)


def _get_last_usage(transcript_path: Path) -> "dict | None":
    """
    Read the last assistant entry with usage data from a JSONL transcript.

    Seeks to the last TAIL_BYTES (64 KB) of the file rather than loading
    the full multi-MB transcript. The first line in the tail may be partial
    and is skipped when the seek offset is non-zero.
    Returns the usage dict or None.
    """
    try:
        with transcript_path.open("rb") as f:
            f.seek(0, 2)
            file_size = f.tell()
            read_size = min(TAIL_BYTES, file_size)
            f.seek(-read_size, 2)
            tail = f.read(read_size).decode("utf-8", errors="replace")
        lines = tail.splitlines()
        # If we sought past the start, the first line may be a partial record — skip it
        scan_lines = lines[1:] if read_size < file_size else lines
        for line in reversed(scan_lines):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") != "assistant":
                continue
            usage = obj.get("message", {}).get("usage")
            if usage:
                return usage
    except Exception:
        pass
    return None


def _compute_effective_tokens(usage: dict) -> int:
    """Compute effective input tokens: input_tokens + cache_read + cache_creation."""
    return (
        usage.get("input_tokens", 0)
        + usage.get("cache_read_input_tokens", 0)
        + usage.get("cache_creation_input_tokens", 0)
    )


def _debounce_path(session_id: str) -> Path:
    return DEBOUNCE_DIR / f"claude_ctx_{session_id}.json"


def _load_debounce(session_id: str) -> dict:
    """
    Load debounce state from /tmp/claude_ctx_{session_id}.json.

    Returns fresh state if file is missing, corrupted, or stale (> 1h old).
    """
    fresh = {"call_count": 0, "last_warning_at": 0, "last_critical_at": 0}
    path = _debounce_path(session_id)
    if not path.exists():
        return fresh
    try:
        age = time.time() - path.stat().st_mtime
        if age > 3600:  # 1 hour
            return fresh
        state = json.loads(path.read_text())
        # Validate required keys
        for key in fresh:
            if key not in state:
                return fresh
        return state
    except Exception:
        return fresh


def _save_debounce(session_id: str, state: dict) -> None:
    """Persist debounce state."""
    try:
        _debounce_path(session_id).write_text(json.dumps(state))
    except Exception:
        pass


def _should_warn(state: dict, level: str) -> bool:
    """
    Check if a warning should fire based on debounce state.

    WARNING: suppressed if call_count - last_warning_at < DEBOUNCE_CALLS
    CRITICAL: suppressed if call_count - last_critical_at < DEBOUNCE_CALLS
              BUT always fires if last_critical_at == 0 (first-ever critical).
    """
    call_count = state["call_count"]
    if level == "critical":
        if state["last_critical_at"] == 0:
            return True  # First CRITICAL — always fire regardless of WARNING debounce
        return (call_count - state["last_critical_at"]) >= DEBOUNCE_CALLS
    # level == "warning"
    if state["last_warning_at"] == 0:
        return True  # First WARNING — always fire
    return (call_count - state["last_warning_at"]) >= DEBOUNCE_CALLS


def _play_sound(name: str) -> None:
    """Thin wrapper over sounds.play_sound — patchable in tests."""
    try:
        from sounds import play_sound

        play_sound(name)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def handle_posttool(data: dict) -> dict:
    """
    PostToolUse handler for context window monitoring.

    Returns:
      {}                                         — below threshold or debounced
      {"hookSpecificOutput": {...}}              — WARNING (soft nudge)
      {"systemMessage": "..."}                  — CRITICAL (mandatory)
    """
    try:
        cwd = data.get("cwd", "")
        if not cwd:
            return {}

        transcript = _find_transcript(cwd)
        if transcript is None:
            return {}

        session_id = transcript.stem
        usage = _get_last_usage(transcript)
        if usage is None:
            return {}

        effective = _compute_effective_tokens(usage)
        pct = effective / MAX_CONTEXT_TOKENS
        remaining = MAX_CONTEXT_TOKENS - effective

        if pct < WARNING_THRESHOLD:
            return {}

        state = _load_debounce(session_id)
        state["call_count"] += 1

        pct_display = round(pct * 100, 1)

        if pct >= CRITICAL_THRESHOLD:
            if _should_warn(state, "critical"):
                state["last_critical_at"] = state["call_count"]
                _save_debounce(session_id, state)
                _play_sound("attention")
                return {
                    "systemMessage": (
                        f"🚨 CONTEXT WINDOW CRITICAL: {pct_display}% used "
                        f"({effective:,} / {MAX_CONTEXT_TOKENS:,} tokens).\n"
                        f"Only ~{remaining:,} tokens remaining. You MUST:\n"
                        "1. Finish the immediate task only — no new explorations\n"
                        "2. Write continuation.md with pending work and a resume prompt\n"
                        "3. Tell the user to start a new session\n"
                        "Do NOT read large files or start new features."
                    )
                }
            _save_debounce(session_id, state)
            return {}

        # WARNING zone
        if _should_warn(state, "warning"):
            state["last_warning_at"] = state["call_count"]
            _save_debounce(session_id, state)
            _play_sound("context_warning")
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": (
                        f"⚠️ CONTEXT WINDOW WARNING: {pct_display}% used "
                        f"({effective:,} / {MAX_CONTEXT_TOKENS:,} tokens).\n"
                        f"~{remaining:,} tokens remaining. Consider:\n"
                        "- Completing the current task and starting a new session\n"
                        "- Using /compact to reduce context\n"
                        "- Avoiding large file reads"
                    ),
                }
            }

        _save_debounce(session_id, state)
        return {}

    except Exception:
        return {}
