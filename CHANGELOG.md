# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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

### Sprint 2 - Core Builders (Planned)
- [ ] Skill builder tool
- [ ] Command builder tool
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
