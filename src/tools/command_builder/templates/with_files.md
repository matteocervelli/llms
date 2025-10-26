---
description: {{ description }}
{% if thinking_mode %}thinking: true{% endif %}
{% for key, value in frontmatter.items() %}{{ key }}: {{ value }}
{% endfor %}
---

{{ description }}
{% if has_parameters %}

## Parameters

This command accepts the following arguments:
{% for param in parameters %}
- `{{ param.name }}`: {{ param.description }}{% if param.required %} (required){% else %} (optional{% if param.default %}, default: {{ param.default }}{% endif %}){% endif %}
{% endfor %}

Usage: `/{{ name }} {% for param in parameters %}{% if param.required %}<{{ param.name }}>{% else %}[{{ param.name }}]{% endif %} {% endfor %}`
{% endif %}
{% if has_files %}

## Referenced Files

This command references the following files:
{% for file_ref in file_references %}
- @{{ file_ref }}
{% endfor %}
{% endif %}
{% if has_bash %}

## Execution

```bash
{% for cmd in bash_commands %}
!{{ cmd }}
{% endfor %}
```
{% endif %}
