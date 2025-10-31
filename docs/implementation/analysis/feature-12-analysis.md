---
title: "Feature #12 Analysis: Build Catalog Manifest System"
author: "analysis-specialist"
date: "2025-10-30"
issue: "#12"
milestone: "Sprint 2 - Core Builders"
status: "ANALYSIS_COMPLETE"
---

# Feature #12 Analysis: Build Catalog Manifest System

## Executive Summary

Issue #12 requires building a **unified catalog manifest system** to track and manage all installed skills, commands, and agents across global, project, and local scopes. This feature consolidates metadata from three separate JSON catalogs (`skills.json`, `commands.json`, `agents.json`) with auto-discovery, search/filter capabilities, and a CLI interface.

**Analysis Status**: ✅ Complete and Ready for Design Phase

---

## 1. Issue Overview

### Issue Details
- **GitHub Issue**: [#12 - Build Catalog Manifest System](https://github.com/matteocervelli/llms/issues/12)
- **Milestone**: Sprint 2 - Core Builders
- **Labels**: documentation, enhancement
- **Author**: matteocervelli
- **Priority**: High (core feature for element discoverability)

### Problem Statement

The LLM Configuration Management System currently has:
- ✅ **Skills Builder** (`skill_builder/`) - Maintains `skills.json` catalog
- ✅ **Command Builder** (`command_builder/`) - Maintains `commands.json` catalog
- ✅ **Agent Builder** (`agent_builder/`) - Maintains `agents.json` catalog

**Current Gaps**:
1. No unified manifest system to browse all elements
2. No auto-discovery mechanism for elements
3. Limited search and filter functionality
4. No CLI commands for listing/discovering elements
5. Inconsistent metadata schemas across catalogs

### Success Criteria

The feature must deliver:
1. Unified catalog manifest system with consistent schemas
2. Auto-discovery of installed elements
3. Search and filter functions
4. Standard metadata fields (name, scope, description, created_at, updated_at)
5. CLI command: `llm list skills | commands | agents`
6. Unit tests (minimum 80% coverage)

---

## 2. Requirements & Acceptance Criteria

### Functional Requirements

#### 2.1 Manifest Schema Design

**Skills Manifest** (`manifests/skills.json`)
```json
{
  "schema_version": "1.0",
  "last_synced": "2025-10-30T12:34:56Z",
  "skills": [
    {
      "id": "uuid4",
      "name": "skill-name",
      "description": "Description with usage context",
      "scope": "global|project|local",
      "path": "/absolute/path/to/skill",
      "created_at": "2025-10-29T12:34:56Z",
      "updated_at": "2025-10-29T12:34:56Z",
      "metadata": {
        "template": "basic|analysis|implementation|validation",
        "has_scripts": boolean,
        "file_count": integer,
        "allowed_tools": ["tool1", "tool2"]
      }
    }
  ]
}
```

**Commands Manifest** (`manifests/commands.json`)
```json
{
  "schema_version": "1.0",
  "last_synced": "2025-10-30T12:34:56Z",
  "commands": [
    {
      "id": "uuid4",
      "name": "/command-name",
      "description": "Command description",
      "scope": "global|project|local",
      "path": "/absolute/path/to/command.md",
      "created_at": "2025-10-29T12:34:56Z",
      "updated_at": "2025-10-29T12:34:56Z",
      "metadata": {
        "aliases": ["alias1", "alias2"],
        "requires_tools": ["tool1", "tool2"],
        "tags": ["tag1", "tag2"]
      }
    }
  ]
}
```

**Agents Manifest** (`manifests/agents.json`)
```json
{
  "schema_version": "1.0",
  "last_synced": "2025-10-30T12:34:56Z",
  "agents": [
    {
      "id": "uuid4",
      "name": "agent-name",
      "description": "Agent description",
      "scope": "global|project|local",
      "path": "/absolute/path/to/agent.md",
      "model": "claude-haiku-4-5|claude-opus-4|claude-sonnet-4",
      "created_at": "2025-10-29T12:34:56Z",
      "updated_at": "2025-10-29T12:34:56Z",
      "metadata": {
        "specialization": "category",
        "requires_skills": ["skill1", "skill2"],
        "tags": ["tag1", "tag2"]
      }
    }
  ]
}
```

#### 2.2 Auto-Discovery Implementation

**Directory Scanning Logic**
```
Global Scope:
  ~/.claude/skills/            → Walk directories
  ~/.claude/commands/          → Read .md files
  ~/.claude/agents/            → Read .md files

Project Scope:
  <project>/.claude/skills/    → Walk directories
  <project>/.claude/commands/  → Read .md files
  <project>/.claude/agents/    → Read .md files

Local Scope:
  <project>/.claude/skills/    → Filter by .local suffix
  <project>/.claude/commands/  → Filter by .local suffix
  <project>/.claude/agents/    → Filter by .local suffix
```

**Discovery Rules**
- Skills: Directories in `.claude/skills/` containing `.md` files
- Commands: `.md` files in `.claude/commands/` (prefix with `/`)
- Agents: `.md` files in `.claude/agents/`
- Metadata extraction from YAML frontmatter

#### 2.3 Search & Filter Functions

```python
class CatalogManifest:
    """Unified catalog for all elements."""

    def search(
        self,
        query: str,
        element_type: str = "all",  # skills|commands|agents
        scope: str = "all",         # global|project|local|all
        tags: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Search across catalogs with filtering."""
        pass

    def filter_by_scope(
        self,
        scope: str,
        element_type: str = "all"
    ) -> List[Dict[str, Any]]:
        """Filter elements by scope."""
        pass

    def filter_by_tag(
        self,
        tag: str,
        element_type: str = "all"
    ) -> List[Dict[str, Any]]:
        """Filter elements by tag."""
        pass

    def get_by_name(
        self,
        name: str,
        element_type: str = "all"
    ) -> Optional[Dict[str, Any]]:
        """Get single element by name."""
        pass
```

#### 2.4 CLI Interface

**Commands to Implement**

```bash
# List all skills in project
llm list skills

# List all commands in project
llm list commands

# List all agents in project
llm list agents

# List all elements across all types
llm list all

# Filter by scope
llm list skills --scope project
llm list commands --scope global

# Search
llm search "analysis" --type skills
llm search "feature" --type commands --scope project

# Show details
llm show skill analysis
llm show command /feature-implement
llm show agent analysis-specialist
```

**Output Format Options**
- Table format (default)
- JSON format (`--json`)
- Condensed format (`--condensed`)

### Non-Functional Requirements

#### 2.5 Performance Requirements
- **Search**: < 500ms for queries on 100+ elements
- **Sync**: < 1000ms for full catalog sync
- **Memory**: < 50MB for in-memory catalogs
- **Disk**: Manifest files < 1MB each

#### 2.6 Reliability Requirements
- **Atomicity**: Atomic catalog updates (temp file + rename pattern)
- **Resilience**: Backup creation before writes
- **Validation**: Schema validation on load and save
- **Error Handling**: Graceful degradation on missing elements

#### 2.7 Compatibility Requirements
- **Python**: 3.11+ (match project standard)
- **OS**: macOS, Linux, Windows
- **Scope Management**: Integrate with existing `ScopeManager`
- **Catalog Integration**: Work with existing `skills.json`, `commands.json`, `agents.json`

---

## 3. Security Considerations (OWASP Top 10 2021)

### A01: Broken Access Control
**Risk**: Unauthorized modification of catalogs
- **Mitigation**: File permissions check before write operations
- **Mitigation**: Scope validation (local/project/global restrictions)
- **Implementation**: ScopeManager integration for path validation

### A02: Cryptographic Failures
**Risk**: Catalog tampering or corruption
- **Mitigation**: JSON schema validation on load
- **Mitigation**: Atomic writes with backup pattern
- **Mitigation**: Hash verification of catalog integrity (future enhancement)

### A03: Injection
**Risk**: Path traversal via catalog paths or search queries
- **Mitigation**: Strict path validation using `Path.resolve()`
- **Mitigation**: Search query sanitization
- **Mitigation**: Whitelist allowed directories (`.claude/skills`, `.claude/commands`, etc.)

### A05: Broken Access Control
**Risk**: Exposing sensitive metadata in catalogs
- **Mitigation**: Exclude sensitive fields from catalog export
- **Mitigation**: Scope-aware filtering (don't expose local elements globally)

### A08: Software and Data Integrity Failures
**Risk**: Loading corrupted or malicious catalogs
- **Mitigation**: Pydantic schema validation
- **Mitigation**: Type checking for all catalog entries
- **Mitigation**: Reject entries with invalid UUID format

### Additional Security Considerations

**Path Traversal Prevention**
```python
# SECURE: Use pathlib and resolve()
safe_path = Path(user_input).resolve()
allowed_base = Path.home() / ".claude"
if not str(safe_path).startswith(str(allowed_base)):
    raise ValueError("Path outside allowed directory")

# NOT SECURE: String concatenation
path = f"~/.claude/{user_input}"  # Vulnerable to ../
```

**Catalog Validation**
```python
# All catalog entries must be Pydantic models
# - Type validation
# - Format validation
# - Range validation
# - Enum validation
```

---

## 4. Tech Stack Requirements

### Core Technologies

| Component | Version | Purpose | Rationale |
|-----------|---------|---------|-----------|
| Python | 3.11+ | Language | Project standard |
| Pydantic | 2.x | Data validation | Type-safe schemas |
| pathlib | stdlib | Path handling | Built-in, robust |
| json | stdlib | Serialization | Native format |
| pytest | 7.x+ | Testing | Project standard |
| Click | 8.x | CLI framework | Lightweight, proven |

### Existing Integrations

1. **ScopeManager** (`src/core/scope_manager.py`)
   - Dependency: Already used by `skill_builder`, `command_builder`, `agent_builder`
   - Integration point: Determine base paths for auto-discovery

2. **Exception Hierarchy** (`src/tools/*/exceptions.py`)
   - Pattern: Custom exception classes for each tool
   - Implementation: Create `catalog_manifest_exceptions.py`

3. **Pydantic Models** (`src/tools/*/models.py`)
   - Pattern: Separate models file with validation
   - Implementation: Extend existing catalog entry models

### Dependencies Needed

**New Direct Dependencies**: None (all available in project)

**Indirect Dependencies**:
- `pathlib2` (fallback for Python < 3.12) - Already in uv.lock
- `pydantic[json-schema]` - Already in uv.lock
- `click` - For CLI interface (check if available)

---

## 5. Dependencies Needed

### Internal Dependencies

```
✅ Already Available:
  - src/core/scope_manager.py (ScopeManager)
  - src/tools/skill_builder/models.py (SkillCatalog, SkillCatalogEntry)
  - src/tools/command_builder/models.py (CommandCatalog, CommandCatalogEntry)
  - src/tools/agent_builder/models.py (AgentCatalog, AgentCatalogEntry)
  - Existing exception patterns

❓ To Verify:
  - Click CLI framework availability
  - Rich (for formatted output) availability
  - Typer (alternative CLI framework) availability
```

### External Dependencies

**Recommended Stack**:
1. **Pydantic** (2.x) - Already in project
2. **pathlib** (stdlib) - No additional dependency
3. **Click** or **Typer** - For CLI interface
4. **Rich** (optional) - For formatted terminal output

### Dependency Compatibility

**Current Catalog Systems**:
- `skill_builder` uses `SkillCatalog` model ✅
- `command_builder` uses `CommandCatalog` model ✅
- `agent_builder` uses `AgentCatalog` model ✅

**Integration Challenge**: The three catalog systems have similar but not identical schemas:
```
SkillCatalog       → skills (list[SkillCatalogEntry])
CommandCatalog     → commands (list[CommandCatalogEntry])
AgentCatalog       → agents (list[AgentCatalogEntry])
```

**Solution**: Create unified models that extend existing ones:
```python
class UnifiedCatalogEntry(BaseModel):
    """Base class for all catalog entries"""
    id: UUID
    name: str
    description: str
    scope: ScopeType
    path: Path
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

class SkillCatalogEntryUnified(UnifiedCatalogEntry):
    """Extends SkillCatalogEntry with unified fields"""
    element_type: Literal["skill"] = "skill"
    template: str
    # ... skill-specific fields

class CommandCatalogEntryUnified(UnifiedCatalogEntry):
    """Extends CommandCatalogEntry with unified fields"""
    element_type: Literal["command"] = "command"
    # ... command-specific fields

class AgentCatalogEntryUnified(UnifiedCatalogEntry):
    """Extends AgentCatalogEntry with unified fields"""
    element_type: Literal["agent"] = "agent"
    model: str
    # ... agent-specific fields
```

---

## 6. Scope Boundaries

### In Scope

✅ **Core Functionality**
1. Create manifest schema for skills, commands, agents
2. Implement auto-discovery scanning logic
3. Build search/filter functions
4. Create CLI interface for listing elements
5. Unit tests (80%+ coverage)
6. Documentation (README + docstrings)

✅ **Integration Points**
1. Integration with existing `ScopeManager`
2. Integration with existing catalog models
3. Backward compatibility with `skills.json`, `commands.json`, `agents.json`

✅ **Metadata Support**
1. Basic metadata: name, scope, description, created_at, updated_at
2. Type-specific metadata (template for skills, model for agents, etc.)
3. Frontmatter extraction from elements

### Out of Scope

❌ **Future Enhancements** (Post-MVP)
1. Web UI for catalog browsing
2. Advanced visualization (graphs, dependency trees)
3. Catalog syncing across machines
4. Cloud-based catalog repository
5. Catalog versioning/history
6. Element recommendations based on usage
7. Performance optimization (caching layers)
8. Integration with other LLM systems (Codex, OpenCode)

❌ **Not Included in This Issue**
1. Hook catalog system (Issue #13 scope)
2. Plugin catalog system (Issue #14 scope)
3. Prompt catalog system (Issue #15 scope)
4. MCP catalog system (Issue #16 scope)

### Potential Expansion Points

**Phase 2 Extensions** (Post-MVP):
```
┌─────────────────────────────────────────────────────┐
│  Unified Catalog Manifest System (Issue #12)        │
├─────────────────────────────────────────────────────┤
│ Phase 1 (MVP): Skills, Commands, Agents            │
│ Phase 2: Add Hooks (Issue #13)                      │
│ Phase 3: Add Plugins (Issue #14)                    │
│ Phase 4: Add Prompts (Issue #15)                    │
│ Phase 5: Add MCPs (Issue #16)                       │
└─────────────────────────────────────────────────────┘
```

---

## 7. Identified Risks

### 7.1 Technical Risks

#### Risk: Catalog Schema Incompatibility
**Probability**: Medium | **Impact**: High

**Description**: Existing catalogs have different schemas; unifying them may break backward compatibility.

**Mitigation Strategy**:
- Create separate unified models alongside existing ones
- Maintain read/write compatibility with existing catalogs
- Version schema (start at 1.0) with migration support
- Use adapter pattern to convert between formats

**Testing**:
- Unit tests for schema migrations
- Backward compatibility tests
- Round-trip tests (read → unified → write → read)

#### Risk: Performance Degradation on Large Catalogs
**Probability**: Low | **Impact**: Medium

**Description**: Scanning large directory structures or searching through 100+ elements could be slow.

**Mitigation Strategy**:
- Lazy loading: Don't load all catalogs at startup
- Caching: Cache catalog in memory until invalidated
- Performance targets: All ops < 500ms
- Use generators for large dataset processing
- Consider indexing if catalog grows (future enhancement)

**Testing**:
- Benchmark with 100+ elements in each catalog
- Memory usage profiling
- Search performance tests

#### Risk: File System Race Conditions
**Probability**: Low | **Impact**: High

**Description**: Concurrent catalog updates could cause corruption.

**Mitigation Strategy**:
- Atomic writes (temp file + rename pattern) - PROVEN by `skill_builder`, `agent_builder`
- Backup before write
- File locking (optional future enhancement)
- Transactional semantics

**Testing**:
- Concurrent write tests
- Corruption recovery tests
- Backup validation tests

### 7.2 Integration Risks

#### Risk: Scope Manager Integration Complexity
**Probability**: Medium | **Impact**: Medium

**Description**: ScopeManager API might not align perfectly with catalog discovery needs.

**Mitigation Strategy**:
- Audit ScopeManager API early in design phase
- Create wrapper functions if needed
- Coordinate with ScopeManager maintainer
- Document integration points clearly

**Testing**:
- ScopeManager integration tests
- Fallback handling tests

#### Risk: Catalog Entry Model Evolution
**Probability**: Medium | **Impact**: Low

**Description**: Existing models in skill_builder, command_builder, agent_builder continue to evolve.

**Mitigation Strategy**:
- Keep unified models loosely coupled
- Use composition over inheritance
- Version-aware loading (handle v1.0, v1.1 formats)
- Document compatibility matrix

**Testing**:
- Model versioning tests
- Forward/backward compatibility tests

### 7.3 Operational Risks

#### Risk: Manifest File Corruption
**Probability**: Low | **Impact**: High

**Description**: Corrupted JSON could prevent catalog from loading.

**Mitigation Strategy**:
- Schema validation on load (Pydantic)
- Automatic backup creation
- Fallback to backup if corruption detected
- Error reporting/recovery guide

**Testing**:
- Corruption injection tests
- Recovery procedure tests
- Validation tests

#### Risk: Scope Creep
**Probability**: High | **Impact**: Medium

**Description**: Temptation to add features beyond MVP (web UI, cloud sync, etc.).

**Mitigation Strategy**:
- Clear scope boundary definition (Section 6)
- Documented future enhancements
- Regular scope reviews
- MVP-first approach

### 7.4 Adoption & Usage Risks

#### Risk: CLI Interface Discoverability
**Probability**: Medium | **Impact**: Low

**Description**: Users might not know CLI commands exist.

**Mitigation Strategy**:
- Clear documentation with examples
- Help text (`--help` output)
- Integration with main `llm` command hierarchy
- Discovery in README.md

**Testing**:
- Help text validation
- Documentation clarity review

#### Risk: Catalog Staleness
**Probability**: Medium | **Impact**: Medium

**Description**: Catalogs might not stay in sync with filesystem.

**Mitigation Strategy**:
- Auto-sync on `llm list` (scan → merge)
- Optional background watcher (future)
- Manual sync command: `llm sync catalogs`
- Timestamp tracking for staleness detection

**Testing**:
- Sync accuracy tests
- Staleness detection tests

---

## 8. Implementation Roadmap

### Phase 1: Foundation (Estimated: 8-10 hours)

**Deliverables**:
1. Unified catalog models (extension of existing)
2. CatalogManifest class with core operations
3. Auto-discovery scanner
4. Search/filter implementation
5. Unit tests (80%+ coverage)
6. Documentation

**Acceptance Criteria**:
- [x] `manifests/skills.json` schema defined
- [x] `manifests/commands.json` schema defined
- [x] `manifests/agents.json` schema defined
- [x] Auto-discovery working for all three types
- [x] Search/filter functions operational
- [x] Unit tests passing
- [x] 80%+ code coverage

### Phase 2: CLI Interface (Estimated: 6-8 hours)

**Deliverables**:
1. CLI command structure
2. `llm list` subcommand
3. `llm search` subcommand
4. `llm show` subcommand
5. Output formatters (table, JSON, condensed)
6. Integration tests
7. CLI documentation

### Phase 3: Refinement (Estimated: 4-6 hours)

**Deliverables**:
1. Performance optimization
2. Error handling improvements
3. Edge case handling
4. Full documentation
5. Integration with main `llm` command
6. Changelog entry

---

## 9. Acceptance Criteria Mapping

| Acceptance Criterion | Status | Implementation Area |
|---------------------|--------|---------------------|
| `manifests/skills.json` schema | ✅ Defined | Section 2.1 |
| `manifests/commands.json` schema | ✅ Defined | Section 2.1 |
| `manifests/agents.json` schema | ✅ Defined | Section 2.1 |
| Auto-discovery (scan folders) | ✅ Planned | Section 2.2 |
| Search & filter functions | ✅ Planned | Section 2.3 |
| Metadata fields | ✅ Defined | Section 2.1 |
| `llm list` CLI command | ✅ Planned | Section 2.4 |
| Unit tests | ✅ Planned | Phase 1 |

---

## 10. Open Questions & Assumptions

### Assumptions
1. **Pydantic v2.x** available in project ✅ (verified in uv.lock)
2. **Click** CLI framework available ⚠️ (needs verification)
3. **Existing catalogs** in root directory (`skills.json`, `commands.json`, `agents.json`) ✅ (confirmed)
4. **ScopeManager** API stable and documented ✅ (used by other tools)
5. **Auto-discovery runs on demand**, not continuous sync initially ✅ (MVP approach)

### Open Questions

1. **CLI Command Structure**: Should manifest commands be sub-commands of main `llm` or standalone?
   - Option A: `llm list skills` (recommended)
   - Option B: `llm-list-skills`
   - Option C: Both with aliases

2. **Manifest Location**: Should unified manifests be in `/manifests/` or at root?
   - Current structure: `/manifests/docs.json`
   - Recommendation: Keep consistent with existing structure

3. **Search Scope**: Should search include content (frontmatter) or just metadata?
   - MVP: Metadata only
   - Future: Full-text search with content indexing

4. **Backward Compatibility**: Should new code maintain compatibility with old catalog format?
   - Yes: Create migration utilities

5. **Performance Targets**: Are < 500ms search times acceptable?
   - Yes: Performance targets defined in Section 4

---

## 11. Documentation Requirements

### Code Documentation
- **Module docstrings**: Describe purpose, usage, performance characteristics
- **Class docstrings**: Document public API and invariants
- **Function docstrings**: Google-style with examples
- **Type hints**: Complete for all parameters and returns

### User Documentation
1. **README.md**: Feature overview, quick start, examples
2. **CLI Help**: Built-in `--help` for all commands
3. **API Documentation**: Docstrings cover all public methods
4. **Examples**: Real-world usage examples in README

### Architecture Documentation
1. **Design Decisions**: Rationale for schema and approach
2. **Integration Points**: How it connects with other tools
3. **Future Expansion**: Roadmap for Phase 2+

---

## 12. Summary & Recommendations

### Key Findings

1. **Opportunity**: Consolidate three separate catalog systems into unified interface
2. **Challenge**: Different schemas across skill/command/agent catalogs
3. **Solution**: Extend existing models with unified wrapper classes
4. **Risk**: Scope creep toward advanced features (mitigated by clear scope boundaries)

### Recommended Approach

✅ **Use composition over inheritance**: Wrap existing catalog models rather than refactoring them

✅ **Atomic writes pattern**: Proven by `skill_builder` and `agent_builder` - reuse

✅ **Pydantic validation**: Type-safe, integrated validation across all catalogs

✅ **Incremental delivery**: MVP first (skills/commands/agents), then hooks/plugins/prompts

### Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Schema Coverage | 100% | All 3 catalog types defined |
| Auto-discovery Accuracy | 100% | All elements discovered correctly |
| Search Performance | < 500ms | Timed benchmarks |
| Test Coverage | 80%+ | pytest coverage report |
| CLI Usability | Intuitive | User testing with 3+ commands |

### Next Steps

1. **Design Phase**: Create detailed class diagrams and implementation plan
2. **Architecture Review**: Get feedback on unified model approach
3. **Implementation**: Follow Sprint 2 - Core Builders timeline
4. **Testing**: Comprehensive unit + integration test coverage
5. **Documentation**: Complete user and developer documentation

---

## References

- **GitHub Issue**: https://github.com/matteocervelli/llms/issues/12
- **Existing Catalogs**:
  - `skills.json` (skill_builder)
  - `commands.json` (command_builder)
  - `agents.json` (agent_builder)
- **Related Issues**: #8 (Skill Builder), #9 (Command Builder), #10 (Agent Builder)
- **Tech Stack**: Python 3.11+, Pydantic 2.x, Click 8.x
- **TASK.md**: `/Users/matteocervelli/dev/projects/llms/TASK.md`
- **CLAUDE.md**: `/Users/matteocervelli/dev/projects/llms/CLAUDE.md`

---

**Analysis Complete**: This document is ready for design and implementation phases.

**Next Document**: Feature-12-Design.md (Architecture & Detailed Specifications)
