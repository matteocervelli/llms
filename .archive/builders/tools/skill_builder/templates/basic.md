---
name: {{ name }}
description: {{ description }}
{%- if frontmatter %}
{%- for key, value in frontmatter.items() %}
{{ key }}: {{ value }}
{%- endfor %}
{%- endif %}
---

# {{ name }}

{{ description }}

## Instructions

{{ content }}

## Usage

This skill can be invoked by Claude Code when the task matches the description above.

## Examples

Provide examples of when this skill should be used:

1. Example scenario 1
2. Example scenario 2
3. Example scenario 3

## Notes

- This is a basic skill template
- Customize the content above to match your use case
- Add more sections as needed

## Best Practices

- Keep instructions clear and concise
- Provide specific examples
- Include error handling guidance
- Document expected inputs and outputs

## Troubleshooting

Common issues and solutions:

- **Issue 1**: Description and solution
- **Issue 2**: Description and solution

## Related Skills

List related skills that might be useful:

- Related skill 1
- Related skill 2

---

*Generated with skill_builder tool*
