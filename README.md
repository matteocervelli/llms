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

## 🎯 Scope Intelligence System

The project includes a powerful **three-tier scope system** for managing configurations at different levels:

### Scope Tiers

- **Global Scope** (`~/.claude/`): User-wide settings that apply to all projects
- **Project Scope** (`.claude/`): Project-specific settings shared with the team
- **Local Scope** (`.claude/settings.local.json`): Project-local settings not committed to version control

**Configuration Precedence**: Local > Project > Global

### Quick Example

```python
from src.core.scope_manager import ScopeManager

# Auto-detect scope based on current directory
manager = ScopeManager()
scope = manager.detect_scope()
print(f"Detected scope: {scope.value}")

# Get effective scope with CLI flag
scope_config = manager.get_effective_scope('--project')
print(f"Using path: {scope_config.path}")

# Resolve all scopes with precedence
scopes = manager.resolve_all_scopes()
for scope in scopes:
    print(f"{scope.type.value}: {scope.path} (precedence: {scope.precedence})")
```

### Use Cases

- **Global**: Personal preferences, default templates, user-wide settings
- **Project**: Team-shared skills/commands, project configuration (committed)
- **Local**: Personal overrides, API keys, machine-specific config (gitignored)

See [src/core/README.md](src/core/README.md) for detailed documentation and [ADR-001](docs/architecture/ADR/ADR-001-scope-intelligence-system.md) for design decisions.

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

## 🤖 Automation

### Weekly Documentation Updates

Automatically update LLM provider documentation on a weekly schedule using cron.

#### Quick Setup

1. **Test the script manually**:
```bash
cd ~/.claude/llms
./scripts/update_docs.sh
```

2. **Add to crontab** (Sundays at 2 AM):
```bash
crontab -e
```

Add this line:
```bash
# Update LLM documentation weekly (Sundays at 2 AM)
0 2 * * 0 cd ~/.claude/llms && ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1
```

3. **Verify cron job**:
```bash
crontab -l
```

#### Enable Email Notifications (Optional)

To receive email alerts on errors, set the environment variable:

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export DOC_UPDATER_EMAIL="your-email@example.com"
```

**Requirements**:
- `mail` command (install: `brew install mailutils` on macOS)
- Configured mail server (sendmail, postfix, or SMTP)

#### Log Management

**Log Locations**:
- Detailed logs: `logs/doc_fetcher/update_YYYYMMDD_HHMMSS.log`
- Cron output: `logs/doc_fetcher/cron.log`

**Automatic Rotation**:
- Logs older than 30 days are automatically deleted
- Each run creates a new timestamped log file

**View Recent Logs**:
```bash
# List all logs
ls -lh logs/doc_fetcher/

# View latest log
tail -f logs/doc_fetcher/update_*.log | tail -n 50

# View cron output
tail -f logs/doc_fetcher/cron.log
```

#### Disable Automation

To temporarily disable automatic updates:

```bash
# Comment out the cron job
crontab -e
# Add # at the beginning of the line:
# 0 2 * * 0 cd ~/.claude/llms && ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1
```

To permanently remove:
```bash
crontab -e
# Delete the line completely
```

#### Troubleshooting

**Cron job not running**:
1. Check cron is enabled: `sudo launchctl list | grep cron` (macOS)
2. Check cron logs: `grep CRON /var/log/system.log` (macOS)
3. Verify script permissions: `ls -l scripts/update_docs.sh` (should be `-rwxr-x---`)

**Script fails with errors**:
1. Run manually to see detailed output: `./scripts/update_docs.sh`
2. Check Python installation: `python --version` (should be 3.11+)
3. Verify dependencies: `pip list | grep -E "(click|requests|pydantic|crawl4ai)"`
4. Check manifest exists: `ls -l manifests/docs.json`

**Email notifications not working**:
1. Check `mail` command: `which mail`
2. Test email manually: `echo "test" | mail -s "Test" your-email@example.com`
3. Check environment variable: `echo $DOC_UPDATER_EMAIL`
4. Verify mail server configuration

**Logs filling up disk**:
- Logs are automatically rotated (30-day retention)
- Check disk usage: `du -sh logs/doc_fetcher/`
- Manually delete old logs: `rm logs/doc_fetcher/update_*.log`

#### Advanced Configuration

**Custom Schedule**:
```bash
# Daily at 3 AM
0 3 * * * cd ~/.claude/llms && ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1

# Twice weekly (Monday and Thursday at 1 AM)
0 1 * * 1,4 cd ~/.claude/llms && ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1

# Monthly (first Sunday at 2 AM)
0 2 1-7 * 0 cd ~/.claude/llms && ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1
```

**Custom Python Command**:
```bash
# Use specific Python interpreter
0 2 * * 0 cd ~/.claude/llms && PYTHON_CMD=python3.11 ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1

# Use virtual environment
0 2 * * 0 cd ~/.claude/llms && PYTHON_CMD=.venv/bin/python ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1
```

**Custom Log Retention**:

Edit `scripts/update_docs.sh` and change:
```bash
LOG_RETENTION_DAYS=30  # Change to desired number of days
```

---

## 📚 Documentation

- [CLAUDE.md](CLAUDE.md) - Project instructions for Claude Code
- [AGENTS.md](AGENTS.md) - Generic LLM instructions
- [TASK.md](TASK.md) - Sprint tracking and GitHub issues
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

### Tools Documentation

- **Scope Manager** - [src/core/README.md](src/core/README.md) - Scope intelligence system
- **Documentation Fetcher** - [src/tools/doc_fetcher/README.md](src/tools/doc_fetcher/README.md) - Automated doc fetching
- Skill Builder - `src/tools/skill_builder/README.md` (Sprint 2)
- Command Builder - `src/tools/command_builder/README.md` (Sprint 2)
- Agent Builder - `src/tools/agent_builder/README.md` (Sprint 2)

---

## 🗓️ Roadmap

### Sprint 1: Foundation (Current)
- [x] Initialize project structure
- [x] Build scope intelligence system
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
