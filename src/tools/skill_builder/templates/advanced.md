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

## Overview

This is an advanced multi-file skill with comprehensive features:

- Tool restrictions for security
- Helper scripts for complex operations
- Configuration files for customization
- Documentation and examples
- Testing support

## Directory Structure

```
{{ name }}/
├── SKILL.md              # This file
├── config/               # Configuration files
│   ├── settings.yaml     # Skill settings
│   └── defaults.json     # Default values
├── scripts/              # Helper scripts
│   ├── setup.sh          # Setup and initialization
│   ├── process.py        # Main processing logic
│   ├── utils.py          # Utility functions
│   └── cleanup.sh        # Cleanup operations
├── templates/            # Output templates
│   ├── report.md         # Report template
│   └── summary.txt       # Summary template
├── tests/                # Test files
│   ├── test_skill.py     # Skill tests
│   └── fixtures/         # Test fixtures
└── docs/                 # Additional documentation
    ├── examples.md       # Usage examples
    └── api.md            # API documentation
```

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

## Configuration

### settings.yaml

Configure skill behavior:

```yaml
skill_name: {{ name }}
version: 1.0.0
settings:
  debug: false
  verbose: true
  timeout: 30
```

### defaults.json

Default values for parameters:

```json
{
  "max_retries": 3,
  "batch_size": 100,
  "output_format": "markdown"
}
```

## Helper Scripts

### setup.sh

Initialization script for setting up the environment.

**Usage:**
```bash
bash scripts/setup.sh [options]
```

**Options:**
- `--clean`: Clean setup (remove existing config)
- `--verbose`: Verbose output

### process.py

Main processing script with advanced features.

**Usage:**
```python
python scripts/process.py --input INPUT --output OUTPUT [options]
```

**Options:**
- `--input`: Input file or directory
- `--output`: Output destination
- `--config`: Custom config file
- `--dry-run`: Preview without executing

### utils.py

Utility functions for common operations.

**Functions:**
- `validate_input(data)`: Validate input data
- `format_output(result)`: Format output
- `handle_error(error)`: Error handling

### cleanup.sh

Cleanup script with options.

**Usage:**
```bash
bash scripts/cleanup.sh [options]
```

**Options:**
- `--all`: Remove all generated files
- `--temp`: Remove only temporary files

## Workflow

### Standard Workflow

1. **Setup**: `bash scripts/setup.sh`
2. **Configure**: Edit `config/settings.yaml`
3. **Process**: `python scripts/process.py --input data/`
4. **Verify**: Check output
5. **Cleanup**: `bash scripts/cleanup.sh --temp`

### Advanced Workflow

1. **Setup with options**: `bash scripts/setup.sh --clean --verbose`
2. **Dry run**: `python scripts/process.py --input data/ --dry-run`
3. **Custom config**: `python scripts/process.py --config custom.yaml`
4. **Batch processing**: Loop through inputs
5. **Full cleanup**: `bash scripts/cleanup.sh --all`

## Examples

### Example 1: Basic Usage

```bash
# Setup
bash scripts/setup.sh

# Process single file
python scripts/process.py --input data/file.txt --output results/

# Cleanup
bash scripts/cleanup.sh --temp
```

### Example 2: Batch Processing

```bash
# Process multiple files
for file in data/*.txt; do
    python scripts/process.py --input "$file" --output "results/"
done
```

### Example 3: Custom Configuration

```bash
# Create custom config
cp config/settings.yaml config/custom.yaml
# Edit custom.yaml...

# Use custom config
python scripts/process.py --config config/custom.yaml --input data/
```

## Testing

Run tests to verify skill functionality:

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_skill.py::test_basic_processing

# Run with coverage
pytest --cov=scripts tests/
```

## Best Practices

- **Version control**: Commit all skill files
- **Configuration**: Use config files, not hardcoded values
- **Testing**: Write tests for critical functionality
- **Documentation**: Keep docs updated
- **Error handling**: Graceful degradation
- **Logging**: Use structured logging
- **Security**: Validate all inputs

## API Reference

### Core Functions

#### validate_input(data)

Validates input data format and content.

**Parameters:**
- `data` (dict): Input data to validate

**Returns:**
- `bool`: True if valid, False otherwise

**Raises:**
- `ValueError`: If data format is invalid

#### process_data(input_path, output_path, config)

Main processing function.

**Parameters:**
- `input_path` (str): Path to input data
- `output_path` (str): Path for output
- `config` (dict): Configuration settings

**Returns:**
- `dict`: Processing results and statistics

## Troubleshooting

### Common Issues

**Setup fails**
- Check Python version (3.8+)
- Verify dependencies installed
- Check file permissions

**Processing errors**
- Validate input format
- Check available disk space
- Review logs in `logs/skill.log`

**Output issues**
- Verify output directory exists
- Check write permissions
- Validate config settings

### Debug Mode

Enable debug mode for detailed logging:

```yaml
# config/settings.yaml
settings:
  debug: true
  verbose: true
```

## Performance Considerations

- **Batch size**: Adjust based on available memory
- **Timeout**: Increase for large datasets
- **Caching**: Enable for repeated operations
- **Parallel processing**: Use for independent operations

## Security

- Input validation on all external data
- Path traversal prevention
- No arbitrary code execution
- Secrets in environment variables, not config files

## Maintenance

### Regular Tasks

- Review and update dependencies
- Run test suite
- Clean up old logs and temp files
- Update documentation

### Version Updates

1. Update version in `config/settings.yaml`
2. Document changes in `CHANGELOG.md`
3. Run full test suite
4. Tag release in version control

---

*Generated with skill_builder tool*
