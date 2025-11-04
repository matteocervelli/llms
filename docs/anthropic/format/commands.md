# Slash Commands Format Guide

## YAML Frontmatter

### Required Fields

None - all fields are optional.

### Optional Fields

```yaml
description: Brief command description      # Defaults to first line of prompt if omitted
allowed-tools: Read, Write, Bash           # Tool access control
argument-hint: [param1] [param2]           # Shows expected arguments in auto-complete
model: claude-3-5-haiku-20241022          # Which Claude model to use
disable-model-invocation: false            # Prevents SlashCommand tool from invoking this
```

## Template

```yaml
---
description: Create a new feature
argument-hint: [feature-name] [description]
allowed-tools: Read, Write, Edit, Bash
model: sonnet
---

# Command prompt content here
```

## Constraints

- **description**: Recommended for tool access via SlashCommand tool
- **allowed-tools**: Inherits conversation settings if omitted
- **argument-hint**: Use `[param]` syntax for clarity
- **model**: Inherits from conversation's selected model if omitted
- **disable-model-invocation**: Default is `false`

## Official Documentation

https://docs.claude.com/en/docs/claude-code/slash-commands
