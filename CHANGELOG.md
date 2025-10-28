# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **BREAKING**: Renamed commands for consistent `<object>-<action>` naming pattern
  - `/feature` → `/feature-implement`: "Implement new feature from GitHub issue with security-by-design and performance optimization"
  - `/issue` → `/issue-fix`: "Fix bugs and resolve problems from GitHub issues with security and performance validation"
  - Clearer distinction between feature implementation and bug fixing workflows
  - No backward compatibility - old command names removed

### Added
- **Plan Mode documentation** across command builder commands
  - Added comprehensive Plan Mode guidance to `/cc-improve-command`
  - Added Plan Mode best practices to `/cc-create-command`
  - Added Plan Mode tips to complex workflow commands: `/setup-infrastructure`, `/ui-component`, `/new-project`, `/issue-fix`, `/feature-implement`
  - Documented Plan Mode limitations (user-controlled, cannot be forced programmatically)
  - Explained activation methods (Shift+Tab twice) and benefits
- Initial project structure
- GitHub repository and issue tracking
- Sprint-based task management (4 sprints planned)
- Project documentation (README, CONTRIBUTING, CLAUDE.md, AGENTS.md, TASK.md)
- Python project configuration (pyproject.toml, requirements.txt)
- MIT License
- Multi-LLM hybrid architecture design

### Sprint 1 - Foundation (In Progress)
- [x] **Scope Intelligence System** (#2) - Three-tier configuration scope management
  - `src/core/scope_manager.py` - Core scope detection and resolution
  - `src/core/scope_exceptions.py` - Custom exceptions for scope errors
  - `tests/test_scope_manager.py` - Comprehensive test suite (35 tests, 96% coverage)
  - `src/core/README.md` - API documentation and usage examples
  - `docs/architecture/ADR/ADR-001-scope-intelligence-system.md` - Architecture decision record
  - Automatic scope detection (Global > Project > Local)
  - CLI flag support (--global, --project, --local)
  - Configuration precedence handling (Local > Project > Global)
  - Security: Path traversal prevention, input validation
  - Performance: < 10ms scope detection
- [x] **LLM Adapter Architecture** (#3) - Multi-LLM adapter pattern for skills, commands, agents
  - `src/core/llm_adapter.py` - Abstract base class and ClaudeAdapter implementation
  - `src/core/adapter_exceptions.py` - Custom exceptions for adapter operations
  - `src/core/adapter_models.py` - Data models (CreationResult, AdapterMetadata, ElementType)
  - `tests/test_llm_adapter.py` - Comprehensive test suite (43 tests)
  - `tests/test_adapter_integration.py` - Integration tests (12 tests, 89% coverage)
  - `docs/architecture/ADR/ADR-002-llm-adapter-architecture.md` - Architecture decision record
  - `src/core/README.md` - Updated with adapter API documentation
  - LLMAdapter abstract base class with validation and sanitization
  - ClaudeAdapter for Claude Code (Markdown-based)
  - Support for skills, commands, and agents creation
  - Scope integration (global/project/local)
  - Security: Input validation, path traversal prevention, sanitization
  - Performance: < 50ms file creation, < 5ms validation
  - Extensible design for future adapters (CodexAdapter, OpenCodeAdapter)
- [x] **Documentation Fetcher Tool** (#4) - Automated documentation fetching and management
  - `src/tools/doc_fetcher/models.py` - Pydantic data models with validation
  - `src/tools/doc_fetcher/exceptions.py` - Custom exceptions for doc_fetcher operations
  - `src/tools/doc_fetcher/fetcher.py` - HTTP fetching with rate limiting and robots.txt compliance
  - `src/tools/doc_fetcher/converter.py` - HTML to Markdown conversion with sanitization
  - `src/tools/doc_fetcher/manifest.py` - Manifest management with atomic writes
  - `src/tools/doc_fetcher/main.py` - CLI interface with Click (fetch, update, list commands)
  - `src/tools/doc_fetcher/providers/` - Provider configurations (anthropic.yaml, openai.yaml)
  - `tests/test_doc_fetcher.py` - Comprehensive test suite (38 tests, 36 passing)
  - `src/tools/doc_fetcher/README.md` - API documentation and usage examples
  - `docs/architecture/ADR/ADR-003-documentation-fetcher.md` - Architecture decision record
  - Multi-provider support (Anthropic, OpenAI, extensible)
  - SHA-256 hash-based change detection
  - Token bucket rate limiting (configurable)
  - robots.txt compliance with automatic checking
  - XSS prevention and HTML sanitization
  - Security: URL validation, path traversal prevention, size limits
  - Performance: < 5s fetch, < 500ms conversion, < 100ms manifest operations
  - CLI commands: fetch --all, fetch --provider, update, list
- [x] **Documentation Manifest System** (#5) - Enhanced manifest schema v1.1
  - `src/tools/doc_fetcher/models.py` - Enhanced ManifestEntry with id and topics fields
  - `src/tools/doc_fetcher/models.py` - Added ManifestSchema model for top-level validation
  - `src/tools/doc_fetcher/manifest.py` - Updated to v1.1 schema with providers/categories tracking
  - `src/tools/doc_fetcher/manifest.py` - New methods: update_page(), search_pages(), get_providers(), get_categories(), migrate_schema()
  - `tests/test_doc_fetcher.py` - 19 new tests for v1.1 features (all passing, 76% coverage)
  - `src/tools/doc_fetcher/README.md` - Updated with v1.1 features documentation
  - `docs/architecture/ADR/ADR-004-manifest-schema-v1.1.md` - Architecture decision record
  - UUID v4 unique identifiers for documents (auto-generated)
  - Topic tags for categorization (max 20, max 50 chars each, validated)
  - Provider/category tracking at schema level (auto-populated, sorted)
  - Full-text search across title, description, topics with filters
  - Field-level updates by document ID
  - Automatic schema migration from v1.0 to v1.1
  - Security: UUID validation, topics sanitization, search query sanitization
  - Performance: < 50ms update, < 100ms search (1000 docs), < 10ms helpers
- [x] **Crawl4AI Integration for LLM-Optimized Documentation Fetching** (#6) - Enhanced doc_fetcher with Crawl4AI
  - `src/tools/doc_fetcher/crawler.py` - Crawl4AI-based documentation crawler with async support
  - `src/tools/doc_fetcher/exceptions.py` - Added CrawlError exception type
  - `src/tools/doc_fetcher/main.py` - Integrated Crawl4AI with fetch_document_crawl4ai() and fetch_provider_crawl4ai()
  - `src/tools/doc_fetcher/fetcher.py` - Updated ALLOWED_DOMAINS to include docs.claude.com
  - `src/tools/doc_fetcher/providers/anthropic.yaml` - Updated with 22 priority Claude Code documentation URLs
  - `requirements.txt` - Added crawl4ai>=0.7.0 and playwright>=1.40.0 dependencies
  - **Fetched 22 priority documentation pages** (100% success rate):
    - Claude Code (12 pages): overview, quickstart, workflows, skills, commands, subagents, hooks, memory, MCP, output-styles, headless
    - Agent Skills (5 pages): overview, quickstart, best practices, MCP connector, remote MCP servers
    - Agent SDK (3 pages): overview, TypeScript, Python references
    - API (2 pages): messages, models endpoints
  - **LLM-optimized markdown** with superior quality vs BeautifulSoup/Markdownify
  - **Automatic content extraction** with JavaScript rendering support
  - **Rate limiting** respected (1 req/sec)
  - **Async crawling** for improved performance (~1.5s per page)
  - **Manifest tracking** with 22 documents, proper metadata, and hash-based change detection
  - Security: All existing doc_fetcher security measures maintained
  - Performance: ~50 seconds total fetch time (22 pages @ ~2.3s/page including rate limiting)
  - Files: 22 markdown files totaling ~500KB in docs/anthropic/{claude-code,agent-skills,api-sdk,api}/
- [x] **Weekly Documentation Update Automation** (#7) - Cron-based automation for unattended doc updates
  - `scripts/update_docs.sh` - Bash wrapper script with comprehensive error handling (231 lines)
  - `logs/doc_fetcher/.gitkeep` - Log directory structure documentation
  - `docs/architecture/ADR/ADR-007-weekly-documentation-automation.md` - Architecture decision record
  - `docs/implementation/issue-7-automation.md` - Implementation guide with testing results
  - `README.md` - Added "Automation" section with complete setup guide
  - **Cron-based scheduling** for weekly updates (Sundays 2 AM)
  - **Environment validation**: Python version, dependencies, project structure
  - **Log rotation**: Automatic cleanup (30-day retention)
  - **Optional email notifications** via `mail` command (on errors only)
  - **Exit codes**: 0=success, 1=partial failure, 2=fatal error
  - Security: Script permissions 750, log permissions 640, no hardcoded credentials
  - Performance: < 60s typical execution, ~10KB log files
  - Tested manually: All scenarios validated (normal execution, wrong directory, log rotation)

### Sprint 2 - Core Builders (In Progress)
- [ ] **Skill Builder Tool** - Phase 2-5 completed, Phase 6 pending
  - [x] Phase 1: Models, Exceptions, Validator (#8)
  - [x] **Phase 2: Templates and Template Manager** (#21) - Jinja2-based template system
    - `src/tools/skill_builder/templates.py` - TemplateManager with SandboxedEnvironment (220 lines)
    - `src/tools/skill_builder/templates/basic.md` - Simple skill template (80 lines)
    - `src/tools/skill_builder/templates/with_tools.md` - Skill with allowed-tools (90 lines)
    - `src/tools/skill_builder/templates/with_scripts.md` - Skill with scripts/ directory (100 lines)
    - `src/tools/skill_builder/templates/advanced.md` - Full-featured multi-file skill (120 lines)
    - `tests/test_skill_builder.py` - Added 23 tests (15 validator + 8 template), 48 total passing
    - `docs/implementation/issue-21-templates.md` - Implementation documentation
    - Security: Jinja2 SandboxedEnvironment prevents code execution
    - Performance: < 10ms template rendering, < 5ms loading
    - Template variables: name, description, allowed_tools, content, frontmatter
    - 4 templates with progressive complexity (basic → with_tools → with_scripts → advanced)
  - [x] **Phase 3: Builder and Catalog Integration** (#22) - SkillBuilder core logic
    - `src/tools/skill_builder/builder.py` - SkillBuilder class (429 lines)
    - `tests/test_skill_builder.py` - Comprehensive test suite (28 tests, all passing, 77% coverage)
    - `docs/implementation/issue-22-builder.md` - Implementation documentation
    - Core methods: get_scope_path(), build_skill(), update_skill(), delete_skill(), validate_skill_directory()
    - Creates skill **directories** (not single files) with SKILL.md inside
    - Security: Path traversal prevention, file permissions (755 dirs, 644 files), input validation
    - Performance: < 50ms skill creation (5-15ms average in tests)
    - Dry-run mode: Validate without filesystem changes
    - Integration: ScopeManager, TemplateManager, SkillValidator, SkillConfig
  - [x] **Phase 4: Catalog Management System** (#23) - CatalogManager for tracking skills
    - `src/tools/skill_builder/catalog.py` - CatalogManager class (420 lines)
    - `tests/skill_builder/test_catalog_manager.py` - Comprehensive test suite (27 tests, all passing, 82% coverage)
    - `docs/implementation/issue-23-catalog.md` - Implementation documentation
    - Core methods: add_skill(), update_skill(), remove_skill(), get_skill(), list_skills(), search_skills(), sync_catalog(), get_catalog_stats()
    - Atomic write operations (backup + temp + rename) for corruption prevention
    - CRUD operations with duplicate detection and UUID-based identification
    - Query operations: list by scope, search with filters (query, scope, has_scripts, template)
    - Filesystem sync: adds untracked skills, removes orphaned entries, parses YAML frontmatter
    - Catalog stats: total count, by-scope breakdown, by-template counts, scripts count
    - Security: JSON validation, path validation, duplicate prevention, atomic writes
    - Performance: All operations < 100ms (tested), catalog stored at project_root/skills.json
    - Integration: Optional CatalogManager in SkillBuilder (dependency injection pattern)
    - Builder auto-updates catalog on build/update/delete operations
  - [x] **Phase 5: Interactive Wizard** (#24) - SkillWizard for beautiful CLI skill creation
    - `src/tools/skill_builder/wizard.py` - SkillWizard class (368 lines)
    - `tests/test_skill_builder.py` - Added 6 integration tests (all passing, 80% coverage)
    - `docs/implementation/issue-24-wizard.md` - Implementation documentation
    - Custom questionary style matching Claude Code aesthetics
    - 9-step interactive flow: name, description, scope, template, tools, files, preview, confirm
    - Real-time validation with helpful error messages and usage tips
    - Multi-select checkbox for allowed tools (18 Claude Code tools)
    - Preview configuration before creation
    - Cancel at any step (Ctrl+C or decline confirmation)
    - Security: Input validation, path traversal prevention, whitelist validation
    - Performance: < 50ms skill creation, 80% test coverage (122 stmts, 25 missed)
  - [ ] Phase 6: CLI Interface (#25)
- [x] **Command Builder Tool** (#9) - Generate Claude Code slash commands with interactive wizard
  - `src/tools/command_builder/models.py` - Pydantic models (331 lines): CommandConfig, CommandParameter, CommandCatalogEntry, CommandCatalog
  - `src/tools/command_builder/exceptions.py` - Custom exceptions (45 lines): CommandBuilderError hierarchy
  - `src/tools/command_builder/validator.py` - Security-first validation (286 lines): name, bash, file ref, template validation
  - `src/tools/command_builder/templates.py` - Jinja2 template management (203 lines): sandboxed rendering, custom templates
  - `src/tools/command_builder/templates/` - 4 built-in templates: basic, with_bash, with_files, advanced
  - `src/tools/command_builder/builder.py` - Core generation logic (220 lines): scope-aware command building
  - `src/tools/command_builder/catalog.py` - JSON catalog management (252 lines): atomic writes, search, CRUD operations
  - `src/tools/command_builder/wizard.py` - Interactive CLI wizard (422 lines): questionary-based prompts with validation
  - `src/tools/command_builder/main.py` - Click CLI interface (343 lines): create, generate, list, delete, validate, stats
  - `src/tools/command_builder/README.md` - Complete API documentation and usage guide
  - `tests/test_command_builder.py` - Comprehensive test suite (37 tests, 34 passing, command_builder ~70% coverage)
  - **Enhanced Documentation**: 6 additional Claude Code pages fetched (28 total, up from 22)
  - **Interactive wizard**: Beautiful questionary prompts with real-time validation
  - **4 templates**: basic, with_bash (bash commands), with_files (file references), advanced (full-featured)
  - **Security**: Command name validation, dangerous bash detection (rm -rf, dd, fork bombs), path traversal prevention
  - **Scope system**: Global (~/.claude/), Project (.claude/), Local (.claude/ uncommitted)
  - **Catalog**: JSON-based tracking with UUID, search, atomic writes (temp + rename)
  - **CLI modes**: Interactive (wizard) and non-interactive (generate with flags)
  - **Performance**: < 50ms command generation, < 100ms catalog ops, < 10ms validation
  - Features: Parameter configuration, bash execution (!command), file references (@file), thinking mode
- [ ] Agent builder tool
- [ ] Templates library for Claude Code
- [ ] Catalog manifest system

### Sprint 3 - Advanced Builders (Planned)
- [ ] Hook builder tool
- [ ] Plugin builder tool
- [ ] Prompt builder tool
- [ ] MCP manager tool

### Sprint 4 - Polish & Documentation (Planned)
- [ ] Utilities and validators
- [ ] Comprehensive project documentation
- [ ] End-to-end testing suite
- [ ] Migration tools for ~/dev/projects/llms

## [0.1.0] - 2025-10-26

### Added
- Initial project setup
- Git repository initialized at ~/.claude/llms
- GitHub repository created: matteocervelli/llms
- 4 GitHub milestones created (Sprint 1-4)
- 20 GitHub issues created with proper labels and milestones
- Complete folder structure for multi-LLM architecture
- Core documentation files (README, CONTRIBUTING, CLAUDE.md, AGENTS.md, TASK.md)
- Python project configuration
- MIT License

### Infrastructure
- Directory structure supporting Claude Code, Codex, OpenCode (future)
- Scope-based organization (global, project, local)
- Template system for skills, commands, agents, hooks, plugins
- Documentation storage system (docs/anthropic/, docs/openai/, docs/mcp/)
- Manifest system for tracking documentation and catalogs

---

## Version History

- **0.1.0** (2025-10-26) - Initial release, project setup
- **Unreleased** - Sprint 1-4 development in progress

---

## Links

- [GitHub Repository](https://github.com/matteocervelli/llms)
- [Issues](https://github.com/matteocervelli/llms/issues)
- [Milestones](https://github.com/matteocervelli/llms/milestones)
