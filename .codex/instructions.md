# Codex Instructions

The skills, hooks, and rules in `.codex/` are battle-tested in both Claude Code and Codex.
They share the same format, same invocation pattern, and same behavioral guarantees — the runtime is different, the skill logic is identical.

## Key Differences from Claude Code

|             | Claude Code                        | Codex                           |
| ----------- | ---------------------------------- | ------------------------------- |
| Config file | `CLAUDE.md`                        | `AGENTS.md`                     |
| Skills dir  | `.claude/skills/`                  | `.codex/skills/`                |
| Hook system | `.claude/hooks/` via settings.json | `.codex/hooks/` via config.toml |
| Danger mode | permission modes                   | `--dangerously-allow-all` flag  |
| Memory      | custom SQLite + skills             | no built-in persistent memory   |

## Setup

```bash
codex --config .codex/config.toml
```

See `config.toml` for hook wiring and approval mode.

## Hooks

Same protocol as Claude Code — Python scripts reading JSON from stdin, exit 2 to block.
The handlers in `.codex/hooks/` are identical to `.claude/hooks/` — no adjustments needed.
