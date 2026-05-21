---
description: {{ description }}
{% if thinking_mode %}thinking: true{% endif %}
{% for key, value in frontmatter.items() %}{{ key }}: {{ value }}
{% endfor %}
---

# {{ name | upper }}

{{ description }}
{% if has_parameters %}

## Parameters

This command accepts the following arguments with validation:

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
{% for param in parameters %}
| `{{ param.name }}` | {{ param.type }} | {{ '✓' if param.required else '✗' }} | {{ param.description }} | {{ param.default if param.default else '-' }} |
{% endfor %}

### Usage

```bash
/{{ name }} {% for param in parameters %}{% if param.required %}<{{ param.name }}>{% else %}[{{ param.name }}]{% endif %} {% endfor %}

```

### Example

```bash
/{{ name }} {% for param in parameters %}{% if param.required %}my-value{% else %}{% if param.default %}{{ param.default }}{% endif %}{% endif %} {% endfor %}

```
{% endif %}
{% if has_files %}

## Referenced Files

This command automatically references the following files for context:

{% for file_ref in file_references %}
- `@{{ file_ref }}` - Provides context about {{ file_ref }}
{% endfor %}
{% endif %}
{% if has_bash %}

## Execution Steps

This command executes the following operations:

{% for cmd in bash_commands %}
{{ loop.index }}. **{{ cmd.split()[0] if cmd.split() else 'Command' }}**: `!{{ cmd }}`
{% endfor %}

**Note**: All commands are executed with proper error handling and logging.
{% endif %}

## Notes

- This command is available in **{{ scope }}** scope
{% if thinking_mode %}- Extended thinking mode is **enabled** for complex reasoning{% endif %}
- Generated with command_builder tool
