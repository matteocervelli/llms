# llms

Reference configuration for Claude Code and Codex — production skills, hooks, rules, and agents.

## Structure

```
.claude/          # Claude Code config
  skills/         # 39 skills (invoke with /skill-name)
  hooks/          # unified dispatcher + 4 handlers + YAML rules
  rules/          # 21 behavioral rules
  agents/         # browser-tester subagent
  settings.json   # hook wiring + permissions

.codex/           # Codex mirror
  skills/         # same 39 skills
  hooks/          # same hooks
  rules/          # same rules
  config.toml     # Codex hook wiring + approval mode
  AGENTS.md       # Codex equivalent of CLAUDE.md

docs/anthropic/   # Anthropic reference docs (API, Claude Code, MCP)
.archive/         # v0.1 content — not maintained
```

## Working on this repo

When adding or modifying a skill:

1. Edit in `.claude/skills/<name>/SKILL.md`
2. Mirror the change to `.codex/skills/<name>/SKILL.md`
3. Run `/skillify` to validate structure
4. Update `docs/skill-catalog.md`

When modifying hooks:

- Edit `.claude/hooks/` — then sync to `.codex/hooks/`
- Test before committing

## Sanitization policy

No personal infrastructure references. Before committing:

```bash
grep -rn "your-internal-host|your-service|your-org" .claude/ .codex/
```

## Version

Current: **v0.2.0**
