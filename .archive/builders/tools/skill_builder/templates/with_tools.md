---
name: {{ name }}
description: {{ description }}
{%- if allowed_tools %}
allowed-tools:
{%- for tool in allowed_tools %}
  - {{ tool }}
{%- endfor %}
{%- endif %}
{%- if frontmatter %}
{%- for key, value in frontmatter.items() %}
{{ key }}: {{ value }}
{%- endfor %}
{%- endif %}
---

# {{ name }}

{{ description }}

## Tool Restrictions

{%- if allowed_tools %}
This skill is restricted to the following tools:
{%- for tool in allowed_tools %}
- **{{ tool }}**: Use for appropriate operations
{%- endfor %}
{%- else %}
This skill has no tool restrictions.
{%- endif %}

## Instructions

{{ content }}

## Tool Usage Guidelines

{%- if allowed_tools %}
{%- for tool in allowed_tools %}

### {{ tool }}

Describe when and how to use the {{ tool }} tool in this skill context.

{%- endfor %}
{%- endif %}

## Examples

Provide examples of when this skill should be used:

1. Example scenario 1
2. Example scenario 2
3. Example scenario 3

## Best Practices

- Use only the allowed tools listed above
- Follow tool-specific best practices
- Handle errors gracefully
- Validate inputs before tool operations

## Error Handling

Common tool-related errors and solutions:

- **Tool not available**: Verify tool is in allowed-tools list
- **Permission denied**: Check file/directory permissions
- **Operation failed**: Provide fallback behavior

## Notes

- Tool restrictions improve security and predictability
- Choose minimal tool set needed for the task
- Document tool dependencies clearly

---

*Generated with skill_builder tool*
