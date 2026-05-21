---
description: Structure policy for CLAUDE.md and AGENTS.md instruction files
paths:
  - "**/CLAUDE.md"
  - "**/AGENTS.md"
---

# Instruction File Structure Policy

When creating or editing CLAUDE.md (Claude Code) or AGENTS.md (Codex) in any project, apply these rules.

## Line thresholds

| Lines   | Action                                                                          |
| ------- | ------------------------------------------------------------------------------- |
| ≤150    | Fine — no action needed                                                         |
| 151–250 | WARN: extract coding style / tool-specific patterns to `.claude/rules/*.md`     |
| >250    | FAIL: file is bloated — mandatory split (rules extraction or per-package files) |

## What belongs in CLAUDE.md vs rules

**In CLAUDE.md** (always loaded, high-value):

- Project architecture and domain context
- Cross-cutting workflows (how to run, deploy, test at a high level)
- Environment quirks specific to this project
- Pointers to external docs (`rules/`, `docs/`)

**Extract to `.claude/rules/*.md`** (path-scoped, loaded on demand):

- Coding style, naming conventions, type hint requirements
- Tool-specific patterns (alembic, pnpm, docker)
- Test patterns and coverage thresholds
- Commit and PR guidelines

Use `paths:` frontmatter in rule files to scope them to the relevant directories.

## Monorepo trigger

If `pnpm-workspace.yaml`, `turbo.json`, or `lerna.json` exists at root:

- Each package (`apps/*/`, `packages/*/`, `libs/*/`) SHOULD have its own CLAUDE.md
- Root CLAUDE.md keeps only cross-cutting concerns (build system, shared env, CI/CD)
- Per-package CLAUDE.md covers package-specific stack, tests, entry points

This is SHOULD, not MUST. Omit per-package CLAUDE.md only if the package is trivial (<500 lines total, single purpose).

## CLAUDE.md + AGENTS.md coexistence

When both files exist in the same project:

- **CLAUDE.md**: architecture, domain context, workflows (Claude Code-oriented)
- **AGENTS.md**: build commands, style guide, test invocations (Codex-oriented)
- No duplication — if a section exists in both, it belongs in one only
- If a section is tool-agnostic (e.g., coding style), keep it in AGENTS.md (shorter, build-focused) and reference it from CLAUDE.md with a pointer

## Config repos (this repo)

`~/.claude/` and `~/.codex/` are config repos — their instruction files are lean by design.
Do NOT add subdirectory CLAUDE.md files to config repos. Use `rules/*.md` with `paths:` globs instead.
