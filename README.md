# LLMs - Configuration Management System

> Centralized LLM configuration and documentation management system. Tools for building skills, commands, agents, prompts, and managing MCP servers. Multi-LLM support (Claude Code, Codex, OpenCode).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 Vision

Build a unified system for managing LLM configurations, documentation, and tooling across multiple LLM providers (Claude Code, Codex, OpenCode, etc.). Enable developers to:

- **Fetch and maintain** up-to-date documentation from LLM providers
- **Build and manage** skills, commands, agents, and prompts
- **Package and distribute** plugins for team sharing
- **Manage MCPs** (Model Context Protocol servers)
- **Work across LLMs** with a single toolset

---

## ✨ Features

### Current (Sprint 1-4: Claude Code Focus)

- ✅ **Documentation Fetcher**: Automatically fetch and update docs from Anthropic, OpenAI, etc.
- ✅ **Scope Intelligence**: Auto-detect global/project/local configurations
- ✅ **Skill Builder**: Generate Claude Code skills with templates
- ✅ **Command Builder**: Create slash commands for automation
- ✅ **Agent Builder**: Build sub-agents for specialized tasks
- ✅ **Prompt Builder**: Generate and validate master prompts
- ✅ **Plugin Builder**: Package skills/commands/agents for distribution
- ✅ **MCP Manager**: Manage Model Context Protocol servers
- ✅ **Hook Builder**: Create hook configurations

### Future (Sprint 5+: Multi-LLM)

- 🔮 **Codex Support**: Adapt tools for OpenAI Codex
- 🔮 **OpenCode Support**: Extend to OpenCode
- 🔮 **Universal Format**: LLM-agnostic configuration format
- 🔮 **RAG Integration**: Personal documentation knowledge base

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/matteocervelli/llms.git
cd llms

# Install dependencies with uv
uv pip install -r requirements.txt

# Install in development mode
uv pip install -e ".[dev]"
```

### Usage

```bash
# Fetch documentation
python -m src.tools.doc_fetcher fetch --provider anthropic

# Build a skill
python -m src.tools.skill_builder create --name my-skill --template basic

# Build a command
python -m src.tools.command_builder create --name my-command

# Build an agent
python -m src.tools.agent_builder create --name my-agent
```

---

## 📁 Project Structure

```
~/.claude/llms/
├── commands/              # Slash commands (LLM-agnostic)
├── agents/                # Sub-agents (LLM-agnostic)
├── skills/                # Skills/capabilities (LLM-agnostic)
├── prompts/               # Prompts
├── .claude/               # Claude-specific settings
│   └── settings.json
├── src/                   # Source code
│   ├── tools/             # Builder tools
│   ├── core/              # Core functionality
│   └── utils/             # Utilities
├── templates/             # Templates for creation
│   ├── claude/            # Claude Code templates
│   ├── codex/             # Codex templates (future)
│   └── opencode/          # OpenCode templates (future)
├── docs/                  # Fetched documentation
│   ├── anthropic/
│   ├── openai/
│   └── mcp/
├── manifests/             # Metadata catalogs
└── tests/                 # Test suite
```

---

## 🏃 Development

### Setup Development Environment

```bash
cd ~/.claude/llms

# Install with development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src/ tests/

# Type checking
mypy src/

# Lint
flake8 src/ tests/
```

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_doc_fetcher.py

# With coverage
pytest --cov=src --cov-report=term-missing

# Verbose
pytest -v
```

---

## 📚 Documentation

- [CLAUDE.md](CLAUDE.md) - Project instructions for Claude Code
- [AGENTS.md](AGENTS.md) - Generic LLM instructions
- [TASK.md](TASK.md) - Sprint tracking and GitHub issues
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

### Tools Documentation

- Documentation Fetcher - `src/tools/doc_fetcher/README.md`
- Skill Builder - `src/tools/skill_builder/README.md` (Sprint 2)
- Command Builder - `src/tools/command_builder/README.md` (Sprint 2)
- Agent Builder - `src/tools/agent_builder/README.md` (Sprint 2)

---

## 🗓️ Roadmap

### Sprint 1: Foundation (Current)
- [x] Initialize project structure
- [ ] Build scope intelligence system
- [ ] Build LLM adapter architecture
- [ ] Build documentation fetcher
- [ ] Fetch Anthropic/Claude Code documentation
- [ ] Set up weekly documentation updates

### Sprint 2: Core Builders
- [ ] Build skill builder tool
- [ ] Build command builder tool
- [ ] Build agent builder tool
- [ ] Create templates library
- [ ] Build catalog manifest system

### Sprint 3: Advanced Builders
- [ ] Build hook builder tool
- [ ] Build plugin builder tool
- [ ] Build prompt builder tool
- [ ] Build MCP manager tool

### Sprint 4: Polish & Documentation
- [ ] Build utilities and validators
- [ ] Create comprehensive documentation
- [ ] End-to-end testing
- [ ] Prepare migration to ~/dev/projects/llms

### Sprint 5+: Multi-LLM Support
- [ ] Add Codex support
- [ ] Add OpenCode support
- [ ] Universal configuration format
- [ ] RAG integration

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Development setup
- Code style and standards
- Testing requirements
- Pull request process

---

## 📋 Project Status

**Current Sprint**: Sprint 1 - Foundation
**Progress**: See [TASK.md](TASK.md) and [GitHub Issues](https://github.com/matteocervelli/llms/issues)

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Matteo Cervelli**
- Business Scalability Engineer
- Website: [matteocervelli.com](https://matteocervelli.com)
- GitHub: [@matteocervelli](https://github.com/matteocervelli)
- LinkedIn: [matteocervelli](https://linkedin.com/in/matteocervelli)

---

## 🔗 Links

- **GitHub Repository**: https://github.com/matteocervelli/llms
- **Issues**: https://github.com/matteocervelli/llms/issues
- **Milestones**: https://github.com/matteocervelli/llms/milestones
- **Anthropic Documentation**: https://docs.anthropic.com
- **Claude Code Documentation**: https://docs.claude.com/en/docs/claude-code

---

**Built with ❤️ in Tuscany, Italy**
