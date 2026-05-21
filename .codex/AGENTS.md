# Codex Agent Instructions

You are working in a repository that uses the shared skill system from `.codex/skills/`.

## Core Principles

- Read `AGENTS.md` (this file) for project context before acting
- Skills are in `.codex/skills/` — invoke with `/skill-name`
- Use `--dangerously-allow-all` only in trusted, sandboxed environments
- Run `codex --approval-mode suggest` for safer operation on production code

## Workflow

1. **Plan first** — describe your approach before writing code
2. **Test-driven** — write tests before implementation
3. **Minimal scope** — do exactly what was asked, nothing more
4. **Security gate** — run `/security-verify scan` before committing

## Available Skills

Same skills as Claude Code — see `.codex/skills/` or `.claude/skills/`.

## Hooks

Hook scripts are in `.codex/hooks/` or shared from `.claude/hooks/`.
They follow the same JSON stdin/stdout protocol as Claude Code hooks.
