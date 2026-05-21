# llms

Production-ready Claude Code and Codex configuration — skills, hooks, rules, and agents used in real AI-driven development workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Run in Smithery](https://smithery.ai/badge/skills/matteocervelli)](https://smithery.ai/skills?ns=matteocervelli&utm_source=github&utm_medium=badge)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/matteocervelli)


## What's inside

| Directory         | Contents                                                       |
| ----------------- | -------------------------------------------------------------- |
| `.claude/`        | Claude Code skills, hooks, rules, agents, settings             |
| `.codex/`         | Codex equivalent — same skills and hooks, Codex config         |
| `docs/anthropic/` | Fetched Anthropic reference docs (API, Claude Code, MCP)       |
| `.archive/`       | Previous versions — builder tools v0.1, Feature-Implementer v2 |


## Quick start

```bash
git clone https://github.com/matteocervelli/llms.git
cd llms

# Copy to your project
cp -r .claude/ /your-project/.claude/

# Or install globally
cp -r .claude/skills/* ~/.claude/skills/
cp -r .claude/rules/* ~/.claude/rules/
cp -r .claude/hooks/* ~/.claude/hooks/
```


## Skills (39)

Full catalog with trigger phrases: [`docs/skill-catalog.md`](docs/skill-catalog.md)

**SDLC Pipeline**
`/discovery` `/story` `/story-verify` `/spec` `/design` `/implementation` `/fix` `/quick` `/diagnose`

**Quality & Security**
`/code-review` `/pre-commit` `/quality-check` `/security` `/security-verify` `/supply-chain-audit` `/docker-audit` `/test-scaffold`

**Git / PR / Release**
`/ship` `/pr-creator` `/pr-fix` `/pr-merge` `/release` `/deploy` `/progress`

**Docs & Ops**
`/docs` `/documentation-updater` `/deps` `/health` `/ops` `/techdebt` `/website-health`

**Meta**
`/map-codebase` `/skillify` `/registry` `/review` `/project-create` `/analytics` `/frontend` `/claude-code-guide`


## Hooks

Unified dispatcher — one entry point, specialized handlers.

```
.claude/hooks/
  hook_handler.py          # dispatcher
  handlers/
    bash.py                # block dangerous commands
    file.py                # protect sensitive files
    context_monitor.py     # warn at 65/75% context usage
    plan.py                # enforce TaskCreate after plan approval
  rules/
    blocked_commands.yaml
    protected_files.yaml
    formatters.yaml
```

Wired in `.claude/settings.json`.


## Rules (21)

`tdd` `safety` `security-gate` `code-quality` `dependencies` `defense-in-depth` `anti-slop` `docker` `python-tools` `scoped-testing` `temporal-awareness` `skill-architecture` `claude-md-structure` `claude-md-branching` `lockfile-safety` `package-freshness` `frontend-verification` `release-workflow` `github-workflow` `github-cli` `migration-safety`


## Codex

`.codex/` mirrors `.claude/` with Codex-specific config:

```bash
codex --config .codex/config.toml
```

See `.codex/instructions.md` for Claude Code vs Codex differences.


## Versions

| Version    | Description                                                                 |
| ---------- | --------------------------------------------------------------------------- |
| **v0.2.0** | Production skill library — 39 skills, unified hook dispatcher, Codex mirror |
| v0.1.x     | Feature-Implementer v2 (archived in `.archive/`)                            |


## Support

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/matteocervelli)


## License

[MIT](LICENSE)
