---
name: {{ name }}
description: {{ description }}
{%- if model_preference %}
model-preference: {{ model_preference }}
{%- endif %}
{%- if temperature %}
temperature: {{ temperature }}
{%- endif %}
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

## Model Configuration

{%- if model_preference %}
**Preferred Model**: {{ model_preference }}

This skill is optimized for {{ model_preference }} with specific prompting patterns and capabilities.
{%- else %}
This skill works with any Claude model but may have model-specific optimizations.
{%- endif %}

{%- if temperature %}

**Temperature Setting**: {{ temperature }}

- Lower values (0.0-0.3): More deterministic, factual responses
- Medium values (0.4-0.7): Balanced creativity and accuracy
- Higher values (0.8-1.0): More creative, varied responses
{%- endif %}

## Instructions

{{ content }}

## Model-Specific Guidelines

{%- if model_preference %}

### Using {{ model_preference }}

This skill leverages specific capabilities of {{ model_preference }}:

- **Context Window**: Take advantage of the extended context
- **Reasoning**: Utilize advanced reasoning capabilities
- **Tool Use**: Optimize tool calling patterns
- **Code Generation**: Leverage code understanding and generation
{%- else %}

### Model Compatibility

This skill is designed to work across Claude models:

- **Claude Opus**: Use for complex reasoning and analysis
- **Claude Sonnet**: Use for balanced performance
- **Claude Haiku**: Use for fast, simple tasks
{%- endif %}

## Performance Considerations

{%- if temperature %}

With temperature set to {{ temperature }}:

- **Consistency**: {% if temperature|float < 0.4 %}High - responses will be very consistent{% elif temperature|float < 0.7 %}Moderate - good balance{% else %}Variable - creative but less predictable{% endif %}
- **Creativity**: {% if temperature|float < 0.4 %}Low - focused on accuracy{% elif temperature|float < 0.7 %}Moderate - balanced approach{% else %}High - more creative variations{% endif %}
- **Best For**: {% if temperature|float < 0.4 %}Factual tasks, analysis, code{% elif temperature|float < 0.7 %}General purpose tasks{% else %}Creative writing, brainstorming{% endif %}
{%- endif %}

## Examples

Provide examples of when this skill should be used:

1. **Example 1**: Task requiring model-specific capabilities
2. **Example 2**: Task optimized for temperature setting
3. **Example 3**: Task leveraging context window

## Best Practices

- **Context Management**: Structure prompts to fit within context limits
- **Temperature Tuning**: Adjust based on task requirements
- **Model Selection**: Use appropriate model for task complexity
- **Prompt Engineering**: Optimize prompts for chosen model
- **Response Validation**: Verify outputs meet quality standards

## Temperature Guidelines

Choose temperature based on task type:

| Temperature | Best For | Avoid For |
|------------|----------|-----------|
| 0.0-0.3 | Code, analysis, facts | Creative writing |
| 0.4-0.7 | General tasks, balanced | Extreme precision needs |
| 0.8-1.0 | Creative writing, brainstorming | Factual accuracy needs |

## Troubleshooting

Common model-related issues:

- **Inconsistent Responses**: Lower temperature for more consistency
- **Too Repetitive**: Increase temperature for variety
- **Context Overflow**: Reduce input size or use summarization
- **Wrong Model**: Verify model-preference in frontmatter

## Advanced Configuration

Optional parameters for fine-tuning:

```yaml
model-preference: claude-sonnet-4
temperature: 0.7
max-tokens: 4000
top-p: 0.9
top-k: 40
```

## Related Skills

List related skills with different model configurations:

- Skill with higher temperature for creative tasks
- Skill with different model for specialized tasks
- Skill with stricter tool restrictions

---

*Generated with skill_builder tool*
