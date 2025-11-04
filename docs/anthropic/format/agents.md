# Sub-Agents Format Guide

## YAML Frontmatter

### Required Fields

```yaml
name: agent-name            # Lowercase letters and hyphens only
description: Agent purpose  # Natural language description
```

### Optional Fields

```yaml
tools: Read, Write, Edit   # Comma-separated tool names (inherits all if omitted)
model: sonnet              # sonnet | opus | haiku | inherit (defaults to configured model)
color: green               # cyan | green | purple | red | yellow (undocumented but valid)
```

## Template

```yaml
---
name: my-agent
description: Brief description of what this agent does
tools: Read, Write, Edit
model: sonnet
color: green
---

# Agent prompt content here
```

## Constraints

- **name**: Lowercase letters, numbers, and hyphens only
- **description**: Required for Claude to understand agent's purpose
- **tools**: When omitted, inherits all tools from main thread including MCP tools
- **model**: Defaults to configured subagent model if omitted
- **color**: Optional field (undocumented) for visually distinguishing agents

## Official Documentation

https://docs.claude.com/en/docs/claude-code/sub-agents
