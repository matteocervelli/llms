# Prompts Format Guide

## Status

**Prompts are NOT a supported element type** in Claude Code.

The official documentation does not include prompts as a configurable element. The supported element types are:

- **Sub-agents** (.claude/agents/)
- **Skills** (.claude/skills/)
- **Slash Commands** (.claude/commands/)
- **Hooks** (settings.json)
- **MCP Servers** (settings.json)

## Note

If you have files in a `.claude/prompts/` directory, they are not recognized by Claude Code's configuration system. Consider converting them to:

- **Skills** - For reusable functionality Claude should auto-discover
- **Slash Commands** - For user-invoked operations
- **Sub-agents** - For complex multi-step workflows

## Official Documentation

No official documentation exists for prompts as they are not a Claude Code feature.
