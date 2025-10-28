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

## Directory Structure

This skill includes helper scripts in the `scripts/` directory:

```
{{ name }}/
├── SKILL.md          # This file
└── scripts/          # Helper scripts
    ├── setup.sh      # Setup and initialization
    ├── process.py    # Main processing logic
    └── cleanup.sh    # Cleanup operations
```

## Instructions

{{ content }}

## Helper Scripts

### setup.sh

Initialization script for setting up the environment.

**Usage:**
```bash
bash scripts/setup.sh
```

**Purpose:**
- Initialize required directories
- Check dependencies
- Set up configuration

### process.py

Main processing script for core functionality.

**Usage:**
```python
python scripts/process.py [args]
```

**Purpose:**
- Execute main skill logic
- Process inputs
- Generate outputs

### cleanup.sh

Cleanup script for removing temporary files and resources.

**Usage:**
```bash
bash scripts/cleanup.sh
```

**Purpose:**
- Remove temporary files
- Clean up working directories
- Reset state

## Workflow

1. Run `setup.sh` to initialize
2. Execute `process.py` for main operations
3. Run `cleanup.sh` to clean up

## Examples

Provide examples of when this skill should be used:

1. Example with setup → process → cleanup workflow
2. Example with custom script parameters
3. Example with error recovery

## Best Practices

- Always run setup before processing
- Check script exit codes
- Handle script errors gracefully
- Clean up resources after completion
- Make scripts idempotent (safe to run multiple times)

## Script Development Guidelines

When creating helper scripts:

1. **Use clear naming**: Scripts should be self-documenting
2. **Add error handling**: Exit with non-zero codes on errors
3. **Document parameters**: Use comments to explain arguments
4. **Make executable**: Set appropriate permissions (`chmod +x`)
5. **Test thoroughly**: Verify scripts work in isolation

## Troubleshooting

Common script-related issues:

- **Permission denied**: Run `chmod +x scripts/*.sh`
- **Script not found**: Verify working directory
- **Dependency missing**: Check setup.sh ran successfully

## Notes

- Scripts enable complex multi-step operations
- Keep scripts focused and modular
- Use Bash for simple operations, Python for complex logic
- Version control all scripts with the skill

---

*Generated with skill_builder tool*
