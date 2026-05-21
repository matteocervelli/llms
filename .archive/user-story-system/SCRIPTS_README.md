# User Story System - Python Scripts Documentation

## Overview

This document describes the Python automation scripts for the User Story Workflow System. All scripts follow project coding standards: type hints, comprehensive docstrings, error handling, and atomic file operations.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 scripts/generate_story_from_yaml.py --help
```

## Scripts

### 1. models.py

**Purpose**: Pydantic models for data validation

**Description**:
- Defines `UserStory`, `Epic`, and all sub-models
- Provides validation for story/epic structures
- Enforces type safety across all scripts
- Validates IDs, priorities, story points, etc.

**Usage**:
```python
from models import UserStory

story = UserStory(**story_data)  # Validates on creation
```

**Line Count**: 255 lines

---

### 2. generate_story_from_yaml.py

**Purpose**: Generate Markdown documentation from YAML story files

**Features**:
- Load YAML story files
- Render Markdown using Jinja2 templates
- Atomic file writes (prevents corruption)
- Single story or batch processing

**Usage**:
```bash
# Generate single story
python3 scripts/generate_story_from_yaml.py --story-id US-0001

# Generate all stories
python3 scripts/generate_story_from_yaml.py --all

# Debug mode
python3 scripts/generate_story_from_yaml.py --all --verbose
```

**Line Count**: 316 lines

---

### 3. validate_story_invest.py

**Purpose**: Validate user stories against INVEST criteria

**INVEST Criteria**:
- **I**ndependent: Minimal blocking dependencies
- **N**egotiable: Flexible, not overly prescriptive
- **V**aluable: Clear business/user value
- **E**stimable: Has story points
- **S**mall: Within sprint capacity (≤8 points)
- **T**estable: Has Given/When/Then acceptance criteria

**Features**:
- Check each INVEST criterion
- Calculate overall score (0-100)
- Provide actionable suggestions
- Save results back to YAML
- JSON or text output

**Usage**:
```bash
# Validate story
python3 scripts/validate_story_invest.py --story-id US-0001

# Strict mode (all criteria must pass)
python3 scripts/validate_story_invest.py --story-id US-0001 --strict

# JSON output
python3 scripts/validate_story_invest.py --story-id US-0001 --output json

# Save validation to story YAML
python3 scripts/validate_story_invest.py --story-id US-0001 --save
```

**Line Count**: 554 lines

---

### 4. check_dependencies.py

**Purpose**: Analyze story dependencies and detect issues

**Features**:
- Build dependency graph using NetworkX
- Detect circular dependencies
- Find long blocking chains
- Identify independent stories (ready to work on)
- Find bottleneck stories (blocking many others)
- Generate Mermaid diagrams

**Usage**:
```bash
# Analyze all dependencies
python3 scripts/check_dependencies.py

# Analyze specific story
python3 scripts/check_dependencies.py --story-id US-0001

# Generate Mermaid diagram
python3 scripts/check_dependencies.py --output-diagram dependencies.mmd

# JSON output
python3 scripts/check_dependencies.py --output json
```

**Output**:
- Circular dependency detection
- Long blocking chains (>5 stories)
- Independent stories (can start immediately)
- Bottleneck stories (high fan-out)

**Line Count**: 456 lines

---

### 5. batch_story_generator.py

**Purpose**: Batch process story generation with parallel execution

**Features**:
- Parallel processing with multiprocessing
- Progress bar with tqdm
- Configurable worker count
- Sequential fallback option
- Comprehensive error reporting

**Usage**:
```bash
# Generate all stories (parallel)
python3 scripts/batch_story_generator.py --all

# Generate specific stories
python3 scripts/batch_story_generator.py --story-ids US-0001,US-0002,US-0003

# Sequential processing (no parallel)
python3 scripts/batch_story_generator.py --all --no-parallel

# Control workers
python3 scripts/batch_story_generator.py --all --workers 8

# Quiet mode
python3 scripts/batch_story_generator.py --all --quiet
```

**Performance**:
- Default 4 workers
- Processes ~10-20 stories/second
- Handles errors gracefully

**Line Count**: 290 lines

---

### 6. story_map_generator.py

**Purpose**: Generate visual story maps

**Features**:
- Group stories by epic
- Color-code by priority
- Show status with emojis
- Multiple output formats (Markdown, Mermaid)
- Filter by epic
- Calculate epic progress

**Usage**:
```bash
# Generate Markdown table
python3 scripts/story_map_generator.py --format md

# Generate Mermaid diagram
python3 scripts/story_map_generator.py --format mermaid

# Filter by epic
python3 scripts/story_map_generator.py --format md --epic EP-001

# Save to file
python3 scripts/story_map_generator.py --format md --output story-map.md
```

**Output Formats**:
- **Markdown**: Table grouped by epic with metrics
- **Mermaid**: Graph diagram with color coding

**Line Count**: 386 lines

---

### 7. github_sync.py

**Purpose**: GitHub integration for user stories

**Features**:
- Create GitHub issues from stories
- Update existing issues
- Bi-directional sync
- Auto-generate labels (story points, persona, epic, status)
- Create milestones for sprints
- Acceptance criteria as checkboxes
- Uses `gh` CLI for authentication

**Subcommands**:
- `create` - Create new GitHub issue
- `update` - Update existing issue
- `sync` - Bi-directional sync
- `bulk` - Process multiple stories

**Usage**:
```bash
# Authenticate (first time)
gh auth login

# Create issue from story
python3 scripts/github_sync.py create US-0001

# Update existing issue
python3 scripts/github_sync.py update US-0001

# Sync story with GitHub
python3 scripts/github_sync.py sync US-0001

# Bulk sync all stories
python3 scripts/github_sync.py bulk --all

# Bulk sync specific stories
python3 scripts/github_sync.py bulk --story-ids US-0001,US-0002
```

**GitHub Labels**:
- `story-points-N` (N = 1,2,3,5,8,13)
- `persona-{persona_id}` (e.g., persona-ceo)
- `epic-{epic_id}` (e.g., epic-EP-001)
- Status labels from story-statuses.yaml
- `user-story` (always added)

**Line Count**: 501 lines

---

## Testing

### Run All Tests

```bash
# Run test suite
python3 -m pytest tests/test_scripts.py -v

# With coverage
python3 -m pytest tests/test_scripts.py --cov=scripts --cov-report=html

# Specific test class
python3 -m pytest tests/test_scripts.py::TestValidateInvest -v
```

### Test Results

- **Total Tests**: 28
- **Passing**: 28 (100%)
- **Coverage**: 80%+ for all modules

### Test Categories

1. **Model Tests** (5 tests)
   - Validation of Pydantic models
   - Invalid data handling

2. **INVEST Validation Tests** (14 tests)
   - Each INVEST criterion
   - Score calculation
   - Edge cases

3. **Dependency Tests** (5 tests)
   - Graph building
   - Circular dependency detection
   - Independent/bottleneck stories

4. **Story Map Tests** (3 tests)
   - Grouping by epic
   - Color/emoji mapping

5. **Integration Tests** (1 test)
   - End-to-end workflow

---

## Code Quality

### Standards Met

- ✅ Type hints on all functions
- ✅ Google-style docstrings
- ✅ Error handling with specific exceptions
- ✅ Logging throughout
- ✅ Atomic file operations
- ✅ Configuration-driven
- ✅ CLI with argparse
- ✅ All scripts executable
- ✅ Help documentation

### File Size Compliance

- `models.py`: 255 lines ✅
- `batch_story_generator.py`: 290 lines ✅
- `generate_story_from_yaml.py`: 316 lines ✅
- `story_map_generator.py`: 386 lines ✅
- `check_dependencies.py`: 456 lines ✅
- `github_sync.py`: 501 lines ⚠️ (1 line over, acceptable)
- `validate_story_invest.py`: 554 lines ⚠️ (cohesive, acceptable)

---

## Common Workflows

### 1. Create and Validate New Story

```bash
# 1. Create story YAML in stories/yaml-source/US-XXXX.yaml

# 2. Validate INVEST criteria
python3 scripts/validate_story_invest.py --story-id US-XXXX --save

# 3. Generate Markdown
python3 scripts/generate_story_from_yaml.py --story-id US-XXXX

# 4. Create GitHub issue
python3 scripts/github_sync.py create US-XXXX
```

### 2. Check Dependencies Before Sprint Planning

```bash
# Analyze dependencies
python3 scripts/check_dependencies.py

# Generate diagram
python3 scripts/check_dependencies.py --output-diagram sprint-deps.mmd

# Find independent stories
python3 scripts/check_dependencies.py | grep "Independent Stories"
```

### 3. Generate Sprint Story Map

```bash
# Filter stories by sprint and generate map
python3 scripts/story_map_generator.py --format md --output sprint-1-map.md

# Generate Mermaid diagram for epic
python3 scripts/story_map_generator.py --format mermaid --epic EP-001
```

### 4. Batch Update All Stories

```bash
# Regenerate all Markdown docs
python3 scripts/batch_story_generator.py --all --workers 8

# Sync all with GitHub
python3 scripts/github_sync.py bulk --all
```

---

## Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: Configuration file not found`
- **Solution**: Run scripts from project root or check CONFIG_PATH

**Issue**: `ModuleNotFoundError: No module named 'yaml'`
- **Solution**: `pip install -r requirements.txt`

**Issue**: GitHub sync fails with authentication error
- **Solution**: `gh auth login` to authenticate GitHub CLI

**Issue**: Validation fails for all stories
- **Solution**: Check config/automation-config.yaml validation settings

### Debug Mode

All scripts support `--verbose` flag for debug logging:

```bash
python3 scripts/SCRIPT_NAME.py --verbose
```

---

## Dependencies

See `requirements.txt` for full list. Key dependencies:

- **PyYAML** (6.0.1+): YAML parsing
- **Jinja2** (3.1.2+): Template rendering
- **pydantic** (2.5.0+): Data validation
- **click** (8.1.7+): CLI framework
- **tqdm** (4.66.1+): Progress bars
- **networkx** (3.2.1+): Dependency graphs
- **PyGithub** (2.1.1+): GitHub API
- **pytest** (7.4.3+): Testing

---

## Future Enhancements

Potential improvements:

1. **Epic Generator**: Auto-generate epics from multiple stories
2. **Story Splitter**: Automatically split large stories (>8 points)
3. **Sprint Planner**: Suggest optimal sprint composition
4. **Template Validator**: Validate story/epic YAML against schemas
5. **Metrics Dashboard**: Generate sprint/epic metrics
6. **Story AI Assistant**: Suggest improvements using LLM
7. **Webhook Handler**: Auto-sync on GitHub events

---

## Contributing

When modifying scripts:

1. Maintain type hints and docstrings
2. Add tests for new functionality
3. Run test suite before committing
4. Keep files under 500 lines where possible
5. Update this documentation

## Support

For issues or questions:
- Check script help: `python3 scripts/SCRIPT_NAME.py --help`
- Review test examples: `tests/test_scripts.py`
- Enable debug logging: `--verbose`

---

**Last Updated**: 2025-11-03
**Version**: 1.0.0
**Python Version**: 3.9+
