# Codex Instructions

This is the Codex equivalent of `.claude/` — same skills and workflow, different runtime.

## Key Differences from Claude Code

|             | Claude Code                        | Codex                              |
| ----------- | ---------------------------------- | ---------------------------------- |
| Config file | `CLAUDE.md`                        | `AGENTS.md`                        |
| Skills dir  | `.claude/skills/`                  | `.codex/skills/` (symlink or copy) |
| Hook system | `.claude/hooks/` via settings.json | `.codex/hooks/` via config.toml    |
| Danger mode | permission modes                   | `--dangerously-allow-all` flag     |
| Memory      | custom SQLite + skills             | no built-in persistent memory      |

## Setup

```bash
# Link skills from .claude (avoid duplication)
ln -s ../.claude/skills .codex/skills

# Or copy if you want Codex-specific overrides
cp -r ../.claude/skills .codex/skills
```

## config.toml

See `../examples/codex-config.example.toml` for the full reference configuration.

## Hooks

Codex hooks use the same pattern as Claude Code — Python scripts reading JSON from stdin.
The `.claude/hooks/` handlers are compatible with Codex with minor adjustments.
