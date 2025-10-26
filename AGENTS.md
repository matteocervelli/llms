# CLAUDE.md - LLM Configuration Management System

## Project Overview

This is the **LLM Configuration Management System** - a centralized tool for managing LLM configurations, documentation, and building skills, commands, agents, prompts, and plugins. Currently focused on Claude Code, with architecture designed for multi-LLM support (Codex, OpenCode, etc.).

## Development Principles

### Code Organization
- **500-Line Limit**: No file should exceed 500 lines of code
- **Automatic Splitting**: Split files by logical responsibilities when exceeding the limit
- **Modular Design**: Prefer multiple focused files over single large files
- **Clean Separation**: Maintain clear interfaces between modules

### Code Quality
- **Single Responsibility**: Each file/module has one clear purpose
- **Type Hints**: Use Python type hints for all functions
- **Documentation**: Comprehensive docstrings for all public functions
- **Testing**: 80%+ test coverage for all modules

### Architecture
- **Hybrid Multi-LLM**: Claude format as primary, adapters for future LLMs
- **Scope Intelligence**: Automatic detection of global/project/local scopes
- **Configuration Precedence**: Local > Project > Global

## Project Structure

```
~/.claude/llms/
├── commands/          # Slash commands for this project
├── agents/            # Sub-agents for this project
├── skills/            # Skills for this project
├── prompts/           # Prompts
├── .claude/           # Claude-specific settings
├── src/               # Source code (tools, core, utils)
├── templates/         # Templates for creating elements
├── docs/              # Fetched documentation
├── manifests/         # Metadata catalogs
└── tests/             # Test suite
```

## Current Sprint: Sprint 1 - Foundation

See [TASK.md](TASK.md) for detailed sprint tracking and GitHub issue links.

### Sprint 1 Focus
1. Initialize complete project structure
2. Build scope intelligence system (global/project/local)
3. Build LLM adapter architecture (Claude + future LLMs)
4. Build documentation fetcher tool
5. Create documentation manifest system
6. Fetch initial Anthropic/Claude Code documentation
7. Set up weekly documentation update automation

## Development Workflow

### Setting Up Development Environment

```bash
# Navigate to project
cd ~/.claude/llms

# Install dependencies with uv
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/ tests/

# Type checking
mypy src/
```

### Creating New Tools

All tools follow this structure:

```
src/tools/tool_name/
├── __init__.py
├── main.py          # CLI entry point
├── core.py          # Core logic
├── README.md        # Tool documentation
└── tests/
    └── test_tool_name.py
```

### Scope Management

When building tools that create skills/commands/agents:

- **Global scope** (`~/.claude/`): User-wide, all projects
- **Project scope** (`.claude/`): Project-specific, team-shared
- **Local scope** (`.claude/settings.local.json`): Project-local, not committed

Tools should:
1. Auto-detect scope based on current directory
2. Support `--global`, `--project`, `--local` flags
3. Respect precedence: Local > Project > Global

## Testing Guidelines

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test tool workflows end-to-end
- **Coverage**: Minimum 80% coverage for all modules
- **Fixtures**: Use pytest fixtures for common test data
- **Mocking**: Mock external dependencies (HTTP requests, file I/O)

## Documentation Standards

- **README**: Every tool needs a README with usage examples
- **Docstrings**: Google-style docstrings for all functions
- **Type Hints**: All function parameters and return values
- **Comments**: Explain complex logic, not obvious code

## Git Workflow

- **Commit messages**: Follow conventional commits (feat:, fix:, docs:, etc.)
- **Branch strategy**: Work on feature branches, merge to main
- **Pull requests**: Create PRs for code review (even if solo)
- **Testing**: All tests must pass before merging

## Tools Being Built

### Sprint 1
- **doc_fetcher**: Fetch and update LLM provider documentation
- **scope_manager**: Detect and manage scope (global/project/local)
- **llm_adapter**: Adapter pattern for multi-LLM support

### Sprint 2
- **skill_builder**: Generate Claude Code skills
- **command_builder**: Generate slash commands
- **agent_builder**: Generate sub-agents
- **catalog_system**: Track all skills/commands/agents

### Sprint 3
- **hook_builder**: Generate hook configurations
- **plugin_builder**: Package plugins for distribution
- **prompt_builder**: Generate and validate prompts
- **mcp_manager**: Manage MCP configurations

### Sprint 4
- **utilities**: Parsers, validators, helpers
- **comprehensive documentation**: Guides, tutorials, API docs
- **testing suite**: End-to-end and integration tests
- **migration tools**: Move to ~/dev/projects/llms

## Multi-LLM Vision

This project is architected for multi-LLM support:

1. **Current**: Claude Code (Sprint 1-4)
2. **Future**: Codex, OpenCode, other LLMs (Sprint 5+)
3. **Approach**: Hybrid - Claude format as primary, adapters for others
4. **Storage**: Generic folders (commands/, agents/, skills/) with LLM-specific configs in (.claude/, .codex/, etc.)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution guidelines.

## Links

- **GitHub Repository**: https://github.com/matteocervelli/llms
- **Issues**: https://github.com/matteocervelli/llms/issues
- **Documentation**: Coming in Sprint 4

---

**Current Status**: Sprint 1 - Foundation ⚙️

See [TASK.md](TASK.md) for detailed progress tracking.
