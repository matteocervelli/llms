# Skills Format Guide

## YAML Frontmatter

### Required Fields

```yaml
name: skill-name                    # Lowercase, hyphens, numbers (max 64 chars)
description: Skill purpose          # Natural language (max 1024 chars)
```

### Optional Fields

```yaml
allowed-tools: Read, Grep, Glob    # Comma or space-separated tool names
```

## Template

```yaml
---
name: my-skill
description: What this skill does and when Claude should use it
allowed-tools: Read, Grep, Glob
---

# Skill prompt content here
```

## Constraints

- **name**: Lowercase letters, numbers, hyphens only; max 64 characters
- **description**: Max 1024 characters; critical for Claude to discover when to use skill
- **allowed-tools**: Restricts tools Claude can use when skill is active (inherits standard permissions if omitted)

## Official Documentation

https://docs.claude.com/en/docs/claude-code/skills
