# Product Requirements Prompt: Build Catalog Manifest System (Issue #12)

**Date**: 2025-10-30
**Designer**: Design Orchestrator (Claude Code)
**Issue**: #12 - Build Catalog Manifest System
**Analysis Document**: `/Users/matteocervelli/dev/projects/llms/docs/implementation/analysis/feature-12-analysis.md`
**Design Documents**:
- Architecture: `/Users/matteocervelli/dev/projects/llms/docs/implementation/design/architecture-feature-12.md`
- Libraries: `/Users/matteocervelli/dev/projects/llms/docs/implementation/design/libraries-feature-12.md`
- Dependencies: `/Users/matteocervelli/dev/projects/llms/docs/implementation/design/dependencies-feature-12.md`

---

**Status**: ✅ Ready for Implementation (Phase 3)
**Complexity**: Medium
**Estimated Effort**: 18-24 hours
**Priority**: P1 (High - Core Feature for Sprint 2)

---

## Executive Summary

This document provides comprehensive implementation guidance for the **unified catalog manifest system**, which consolidates tracking and discovery of all installed skills, commands, and agents across global, project, and local scopes. The system provides auto-discovery, search/filter capabilities, and a CLI interface for developers to browse and manage their LLM configuration elements.

**Architectural Approach**: Facade pattern with four core components (CatalogManager, Scanner, Searcher, Syncer) that extend existing catalog models (SkillCatalog, CommandCatalog, AgentCatalog) while maintaining backward compatibility. The design uses composition over inheritance, wrapping existing models with unified interfaces.

**Key Libraries**: Pydantic 2.9.2 (data validation and serialization), Click 8.1.7 (CLI framework), python-frontmatter 1.1.0 (YAML frontmatter parsing), pathlib (filesystem operations), tabulate 0.9.0 (optional table formatting). All libraries except python-frontmatter and tabulate are already available in the project.

**Implementation Strategy**: 4-phase approach: (1) Foundation - unified data models and base components, (2) Core Implementation - Scanner, Searcher, Syncer classes, (3) Integration - CatalogManager facade and CLI interface, (4) Testing & Validation - comprehensive test coverage (80%+) and security validation.

**Key Considerations**: Maintain backward compatibility with existing catalogs (skills.json, commands.json, agents.json), implement atomic write pattern for catalog updates (backup → temp → rename), validate all filesystem paths to prevent traversal attacks, achieve <500ms search performance for 100+ elements.

---

## Requirements Reference

**Source**: `/Users/matteocervelli/dev/projects/llms/docs/implementation/analysis/feature-12-analysis.md`

### Functional Requirements (Summary)

- **FR-001**: Create unified manifest schemas for skills, commands, and agents with standard fields (id, name, description, scope, path, created_at, updated_at, metadata)
- **FR-002**: Implement auto-discovery to scan `.claude/skills`, `.claude/commands`, `.claude/agents` directories and extract metadata from YAML frontmatter
- **FR-003**: Provide search and filter operations (by query text, scope, tags, element type)
- **FR-004**: Create CLI interface with commands: `llm list`, `llm search`, `llm show`, `llm sync`
- **FR-005**: Support multiple output formats (table, JSON, condensed)

### Non-Functional Requirements (Summary)

- **Performance**: Search < 500ms for 100+ elements, Sync < 1000ms, Memory < 50MB
- **Security**: Path validation to prevent traversal, input sanitization, schema validation (Pydantic)
- **Reliability**: Atomic catalog updates (backup + temp + rename), backup creation before writes
- **Compatibility**: Python 3.11+, macOS/Linux/Windows, integrate with existing ScopeManager

### Acceptance Criteria (Key Points)

- [ ] `manifests/skills.json`, `manifests/commands.json`, `manifests/agents.json` schemas defined with Pydantic models
- [ ] Auto-discovery scans directories and extracts frontmatter metadata
- [ ] Search and filter functions operational with scoring algorithm
- [ ] CLI commands implemented: `llm list skills|commands|agents|all`
- [ ] Unit tests with 80%+ coverage
- [ ] All catalog operations < 500ms on 100 elements

**Full Requirements**: See analysis document for complete requirements, OWASP security assessment, risk analysis, and scope boundaries.

---

## Architecture Design

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Interface Layer                       │
│  (llm list, llm search, llm show commands)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│               CatalogManager (Facade)                        │
│  - Unified interface for all catalog operations              │
│  - Coordinates Scanner, Searcher, Syncer                     │
└────┬──────────────────┬──────────────────┬──────────────────┘
     │                  │                  │
┌────▼──────┐  ┌───────▼────────┐  ┌─────▼──────────┐
│  Scanner  │  │    Searcher    │  │     Syncer     │
│  (Auto-   │  │   (Filter &    │  │  (Load/Save)   │
│ Discovery)│  │    Search)     │  │                │
└────┬──────┘  └───────┬────────┘  └─────┬──────────┘
     │                  │                  │
┌────▼──────────────────▼──────────────────▼──────────────────┐
│              Unified Catalog Models                          │
│  - UnifiedCatalogEntry (base)                                │
│  - SkillCatalogEntryUnified                                  │
│  - CommandCatalogEntryUnified                                │
│  - AgentCatalogEntryUnified                                  │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│           Existing Catalog Models (Unchanged)                │
│  - SkillCatalog, SkillCatalogEntry                           │
│  - CommandCatalog, CommandCatalogEntry                       │
│  - AgentCatalog, AgentCatalogEntry                           │
└──────────────────────────────────────────────────────────────┘
```

### Components

#### Component: CatalogManager

**Purpose**: Facade providing unified interface for all catalog operations

**Responsibilities**:
- Initialize and coordinate Scanner, Searcher, Syncer
- Provide high-level API for listing, searching, showing elements
- Handle scope resolution (global/project/local) via ScopeManager
- Manage catalog lifecycle (load → sync → save)

**Library Integration**:
- **Primary Library**: Pydantic 2.9.2 (data validation)
- **APIs Used**: `BaseModel`, `Field`, `model_dump()`, `ValidationError`
- **Pattern**: Facade pattern with dependency injection
- **Dependencies**: Scanner, Searcher, Syncer, ScopeManager

**Implementation Notes**:
- Auto-sync on list operations (with 60-second cache to avoid repeated scans)
- All methods return unified catalog entries (SkillCatalogEntryUnified, etc.)
- Error handling wraps underlying component exceptions

**Code Example**:
```python
from typing import List, Optional
from pathlib import Path
from .scanner import Scanner
from .searcher import Searcher
from .syncer import Syncer
from .models import UnifiedCatalogEntry, ElementType, ScopeType, OutputFormat
from core.scope_manager import ScopeManager

class CatalogManager:
    """
    Unified interface for catalog operations.

    Coordinates Scanner, Searcher, and Syncer to provide
    high-level operations: list, search, show, sync.
    """

    def __init__(self, scope_manager: ScopeManager):
        """Initialize CatalogManager with scope resolution."""
        self.scope_manager = scope_manager
        self.scanner = Scanner(scope_manager)
        self.searcher = Searcher()
        self.syncer = Syncer(scope_manager)
        self._cache = {}  # Simple cache: {catalog_type: (timestamp, entries)}

    def list_elements(
        self,
        element_type: ElementType,
        scope: ScopeType = ScopeType.ALL,
        format: OutputFormat = OutputFormat.TABLE,
        auto_sync: bool = True
    ) -> List[UnifiedCatalogEntry]:
        """
        List all elements of specified type and scope.

        Auto-syncs with filesystem before listing (cached for 60s).
        """
        if auto_sync:
            self.sync_catalogs(element_types=[element_type])

        # Load from catalog files
        if element_type == ElementType.SKILL:
            catalog = self.syncer.load_catalog(element_type, scope)
            entries = catalog.skills
        elif element_type == ElementType.COMMAND:
            catalog = self.syncer.load_catalog(element_type, scope)
            entries = catalog.commands
        elif element_type == ElementType.AGENT:
            catalog = self.syncer.load_catalog(element_type, scope)
            entries = catalog.agents

        # Filter by scope
        if scope != ScopeType.ALL:
            entries = self.searcher.filter_by_scope(entries, scope)

        return entries
```

---

#### Component: Scanner

**Purpose**: Auto-discovery of installed elements from filesystem

**Responsibilities**:
- Walk directory trees (`.claude/skills`, `.claude/commands`, `.claude/agents`)
- Identify element files based on patterns
- Extract metadata from YAML frontmatter (using python-frontmatter)
- Create UnifiedCatalogEntry instances
- Handle malformed or missing files gracefully

**Library Integration**:
- **Primary Library**: python-frontmatter 1.1.0 (YAML parsing)
- **APIs Used**: `frontmatter.load()`, `post.metadata`, `post.content`
- **Pattern**: Directory walker with validation
- **Dependencies**: pathlib, ScopeManager, python-frontmatter

**Implementation Notes**:
- Skills: Directories containing `.md` files (extract from first .md)
- Commands: `.md` files in commands/ (prefix name with `/` if missing)
- Agents: `.md` files in agents/ (require `model` field in frontmatter)
- Skip files without frontmatter (log warning)
- Skip corrupted YAML (log warning, continue)

**Code Example**:
```python
from pathlib import Path
from typing import List, Optional
import frontmatter
import logging
from .models import SkillCatalogEntryUnified, ElementType, ScopeType
from core.scope_manager import ScopeManager

logger = logging.getLogger(__name__)

class Scanner:
    """Auto-discovery of elements from filesystem."""

    def __init__(self, scope_manager: ScopeManager):
        self.scope_manager = scope_manager

    def scan_skills(self, scope: ScopeType = ScopeType.ALL) -> List[SkillCatalogEntryUnified]:
        """
        Scan for installed skills.

        Pattern: .claude/skills/{skill-name}/*.md
        Metadata: YAML frontmatter from first .md file
        """
        skills = []

        # Get base paths for scope
        if scope in (ScopeType.ALL, ScopeType.GLOBAL):
            global_path = self.scope_manager.get_global_path() / 'skills'
            skills.extend(self._scan_skills_in_directory(global_path, ScopeType.GLOBAL))

        if scope in (ScopeType.ALL, ScopeType.PROJECT):
            project_path = self.scope_manager.get_project_path() / '.claude' / 'skills'
            skills.extend(self._scan_skills_in_directory(project_path, ScopeType.PROJECT))

        return skills

    def _scan_skills_in_directory(
        self,
        skills_dir: Path,
        scope: ScopeType
    ) -> List[SkillCatalogEntryUnified]:
        """Scan single directory for skills."""
        if not skills_dir.exists():
            return []

        skills = []
        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            # Find first .md file
            md_files = list(skill_dir.glob('*.md'))
            if not md_files:
                logger.warning(f"No .md files in skill directory: {skill_dir}")
                continue

            # Parse frontmatter
            skill_file = md_files[0]
            try:
                post = frontmatter.load(skill_file)

                if not post.metadata:
                    logger.warning(f"No frontmatter in {skill_file}")
                    continue

                # Create catalog entry
                entry = SkillCatalogEntryUnified(
                    name=skill_dir.name,
                    description=post.metadata.get('description', ''),
                    scope=scope,
                    path=skill_dir.resolve(),
                    template=post.metadata.get('template', 'basic'),
                    has_scripts=post.metadata.get('has_scripts', False),
                    file_count=len(list(skill_dir.rglob('*.*'))),
                    allowed_tools=post.metadata.get('allowed_tools', [])
                )
                skills.append(entry)

            except Exception as e:
                logger.error(f"Error scanning skill {skill_dir}: {e}")
                continue

        return skills
```

---

#### Component: Searcher

**Purpose**: Search and filter operations on catalog entries

**Responsibilities**:
- Full-text search on name, description, tags
- Filter by scope (global/project/local)
- Filter by tags (all or any match)
- Filter by element type
- Sort results by relevance score

**Library Integration**:
- **Primary Library**: None (stateless operations on lists)
- **APIs Used**: Python built-ins (list comprehensions, sorting)
- **Pattern**: Functional programming with scoring
- **Dependencies**: None

**Implementation Notes**:
- Search algorithm: tokenize query, score matches (exact name +100, name contains +50, description +10, tag +20)
- Case-insensitive search
- Early exit on exact matches
- Limit results to top N

**Code Example**:
```python
from typing import List, Optional
from .models import UnifiedCatalogEntry, ElementType, ScopeType

class Searcher:
    """Search and filter catalog entries (stateless)."""

    def search(
        self,
        entries: List[UnifiedCatalogEntry],
        query: str,
        element_type: ElementType = ElementType.ALL,
        scope: ScopeType = ScopeType.ALL,
        tags: Optional[List[str]] = None
    ) -> List[UnifiedCatalogEntry]:
        """
        Full-text search with filters.

        Searches: name, description, tags
        Scoring: exact name > name contains > description > tags
        """
        # Filter by type
        if element_type != ElementType.ALL:
            entries = self.filter_by_type(entries, element_type)

        # Filter by scope
        if scope != ScopeType.ALL:
            entries = self.filter_by_scope(entries, scope)

        # Filter by tags
        if tags:
            entries = self.filter_by_tags(entries, tags, match_all=True)

        # Score and rank
        query_lower = query.lower()
        scored_entries = []

        for entry in entries:
            score = 0

            # Exact name match
            if entry.name.lower() == query_lower:
                score += 100
            # Name contains
            elif query_lower in entry.name.lower():
                score += 50

            # Description contains
            if query_lower in entry.description.lower():
                score += 10

            # Tag match
            if hasattr(entry, 'tags'):
                for tag in entry.tags:
                    if query_lower in tag.lower():
                        score += 20

            if score > 0:
                scored_entries.append((score, entry))

        # Sort by score (descending)
        scored_entries.sort(key=lambda x: x[0], reverse=True)

        return [entry for score, entry in scored_entries]

    def filter_by_scope(
        self,
        entries: List[UnifiedCatalogEntry],
        scope: ScopeType
    ) -> List[UnifiedCatalogEntry]:
        """Filter entries by scope."""
        return [e for e in entries if e.scope == scope]

    def filter_by_tags(
        self,
        entries: List[UnifiedCatalogEntry],
        tags: List[str],
        match_all: bool = True
    ) -> List[UnifiedCatalogEntry]:
        """
        Filter entries by tags.

        match_all=True: Require all tags (AND)
        match_all=False: Require any tag (OR)
        """
        filtered = []

        for entry in entries:
            if not hasattr(entry, 'tags'):
                continue

            entry_tags = set(t.lower() for t in entry.tags)
            search_tags = set(t.lower() for t in tags)

            if match_all:
                # All tags must be present
                if search_tags.issubset(entry_tags):
                    filtered.append(entry)
            else:
                # Any tag matches
                if entry_tags.intersection(search_tags):
                    filtered.append(entry)

        return filtered
```

---

#### Component: Syncer

**Purpose**: Load and save catalog manifest files atomically

**Responsibilities**:
- Load existing catalogs from JSON files (with Pydantic validation)
- Merge scanned entries with existing catalogs
- Atomic save (backup → temp → validate → rename → cleanup)
- Backup creation before writes
- Schema validation on load and save

**Library Integration**:
- **Primary Library**: Pydantic 2.9.2 (validation)
- **APIs Used**: `model_validate_json()`, `model_dump_json()`, `ValidationError`
- **Pattern**: Atomic write pattern (proven by skill_builder, agent_builder)
- **Dependencies**: pathlib, json, Pydantic models

**Implementation Notes**:
- Atomic write: backup → write to .tmp → validate → rename (POSIX atomic)
- Merge strategy: match by ID (UUID), discovered entries override existing on conflict
- Entries only in existing catalog are kept (don't delete)
- Validate with Pydantic before writing

**Code Example**:
```python
from pathlib import Path
from typing import Union, List
import json
from datetime import datetime
from .models import (
    SkillCatalogUnified,
    CommandCatalogUnified,
    AgentCatalogUnified,
    UnifiedCatalogEntry,
    ElementType,
    ScopeType
)
from .exceptions import CatalogLoadError, CatalogSaveError
from core.scope_manager import ScopeManager

class Syncer:
    """Load and save catalog manifests atomically."""

    def __init__(self, scope_manager: ScopeManager):
        self.scope_manager = scope_manager

    def load_catalog(
        self,
        catalog_type: ElementType,
        scope: ScopeType = ScopeType.PROJECT
    ) -> Union[SkillCatalogUnified, CommandCatalogUnified, AgentCatalogUnified]:
        """
        Load catalog from JSON file.

        Raises:
            CatalogLoadError: If file corrupted or invalid
        """
        catalog_path = self._get_catalog_path(catalog_type, scope)

        if not catalog_path.exists():
            # Create empty catalog
            return self._create_empty_catalog(catalog_type)

        try:
            # Load and validate with Pydantic
            json_text = catalog_path.read_text(encoding='utf-8')

            if catalog_type == ElementType.SKILL:
                return SkillCatalogUnified.model_validate_json(json_text)
            elif catalog_type == ElementType.COMMAND:
                return CommandCatalogUnified.model_validate_json(json_text)
            elif catalog_type == ElementType.AGENT:
                return AgentCatalogUnified.model_validate_json(json_text)

        except Exception as e:
            # Try loading from backup
            backup_path = catalog_path.with_suffix('.json.backup')
            if backup_path.exists():
                try:
                    json_text = backup_path.read_text(encoding='utf-8')
                    if catalog_type == ElementType.SKILL:
                        return SkillCatalogUnified.model_validate_json(json_text)
                    # ... similar for other types
                except Exception:
                    pass

            raise CatalogLoadError(f"Failed to load catalog: {e}") from e

    def save_catalog(
        self,
        catalog: Union[SkillCatalogUnified, CommandCatalogUnified, AgentCatalogUnified],
        catalog_type: ElementType,
        scope: ScopeType = ScopeType.PROJECT,
        create_backup: bool = True
    ) -> None:
        """
        Save catalog atomically.

        Pattern: backup → temp → validate → rename → cleanup
        """
        catalog_path = self._get_catalog_path(catalog_type, scope)

        # Ensure parent directory exists
        catalog_path.parent.mkdir(parents=True, exist_ok=True)

        # Create backup
        if create_backup and catalog_path.exists():
            backup_path = self.backup_catalog(catalog_type, scope)

        # Write to temp file
        temp_path = catalog_path.with_suffix('.json.tmp')

        try:
            # Serialize with Pydantic
            json_text = catalog.model_dump_json(indent=2)
            temp_path.write_text(json_text, encoding='utf-8')

            # Validate temp file (load to verify)
            temp_text = temp_path.read_text(encoding='utf-8')
            if catalog_type == ElementType.SKILL:
                SkillCatalogUnified.model_validate_json(temp_text)
            # ... similar for other types

            # Atomic rename (POSIX atomic operation)
            temp_path.replace(catalog_path)

        except Exception as e:
            # Rollback: restore from backup if available
            if create_backup and backup_path.exists():
                backup_path.replace(catalog_path)

            raise CatalogSaveError(f"Failed to save catalog: {e}") from e

        finally:
            # Cleanup temp file if it still exists
            if temp_path.exists():
                temp_path.unlink()

    def merge_entries(
        self,
        existing: List[UnifiedCatalogEntry],
        discovered: List[UnifiedCatalogEntry]
    ) -> List[UnifiedCatalogEntry]:
        """
        Merge existing and discovered entries.

        Strategy:
        - Match by ID (UUID)
        - Entry in both: Update updated_at, merge metadata (discovered wins)
        - Entry only discovered: Add as new
        - Entry only existing: Keep (don't delete)
        """
        # Create lookup by ID
        existing_map = {e.id: e for e in existing}
        discovered_map = {e.id: e for e in discovered}

        merged = []

        # Process discovered entries (new + updates)
        for disc_id, disc_entry in discovered_map.items():
            if disc_id in existing_map:
                # Update: use discovered, update timestamp
                disc_entry.updated_at = datetime.utcnow()
                merged.append(disc_entry)
            else:
                # New entry
                merged.append(disc_entry)

        # Keep existing entries not in discovered
        for exist_id, exist_entry in existing_map.items():
            if exist_id not in discovered_map:
                merged.append(exist_entry)

        return merged
```

---

### Data Models

#### Model: UnifiedCatalogEntry (Base)

**Purpose**: Base class for all catalog entries with common fields

**Fields**:
```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID, uuid4
from datetime import datetime
from pathlib import Path
from enum import Enum
from typing import Dict, Any, Optional

class ElementType(str, Enum):
    """Types of catalog elements"""
    SKILL = "skill"
    COMMAND = "command"
    AGENT = "agent"
    ALL = "all"  # For search/filter operations

class ScopeType(str, Enum):
    """Scope levels for elements"""
    GLOBAL = "global"
    PROJECT = "project"
    LOCAL = "local"
    ALL = "all"  # For search/filter operations

class UnifiedCatalogEntry(BaseModel):
    """Base class for all catalog entries with common fields"""

    # Pydantic 2.x: Use ConfigDict instead of Config class
    model_config = ConfigDict(
        json_encoders={
            Path: str,
            datetime: lambda v: v.isoformat(),
            UUID: str
        },
        validate_assignment=True,  # Validate on field assignment
        use_enum_values=True       # Use enum values in dict/json
    )

    # Core identity
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)

    # Scope and location
    scope: ScopeType = Field(...)
    path: Path = Field(...)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Type discriminator (for polymorphism)
    element_type: ElementType = Field(...)

    # Generic metadata (element-specific data)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Pydantic 2.x: field_validator replaces @validator
    @field_validator('path')
    @classmethod
    def validate_path(cls, v: Path) -> Path:
        """Ensure path is absolute and exists"""
        resolved = v.resolve()
        if not resolved.exists():
            raise ValueError(f"Path does not exist: {resolved}")
        return resolved

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Ensure name is valid (no slashes except for commands)"""
        if '/' in v and not v.startswith('/'):
            raise ValueError("Name contains invalid characters")
        return v
```

**Validation Rules**:
- `id`: Valid UUID v4
- `name`: 1-100 characters, no special chars except `/` prefix for commands
- `description`: 1-500 characters
- `scope`: One of global/project/local
- `path`: Must exist and be absolute (resolved)
- `element_type`: One of skill/command/agent

**Library Integration**:
- **Validation**: Pydantic 2.x with `field_validator` decorator
- **Serialization**: `model_dump()` for dict, `model_dump_json()` for JSON string
- **Deserialization**: `model_validate()` for dict, `model_validate_json()` for JSON

---

#### Model: SkillCatalogEntryUnified

**Purpose**: Unified skill catalog entry extending base model

**Fields**:
```python
from typing import List, Literal

class SkillCatalogEntryUnified(UnifiedCatalogEntry):
    """Unified skill catalog entry"""

    element_type: Literal["skill"] = "skill"  # Fixed type

    # Skill-specific fields
    template: str = Field(...)
    has_scripts: bool = Field(default=False)
    file_count: int = Field(default=0, ge=0)
    allowed_tools: List[str] = Field(default_factory=list)

    @field_validator('template')
    @classmethod
    def validate_template(cls, v: str) -> str:
        """Ensure template is valid"""
        valid_templates = ["basic", "analysis", "implementation", "validation"]
        if v not in valid_templates:
            raise ValueError(f"Invalid template: {v}. Must be one of {valid_templates}")
        return v
```

---

#### Model: CommandCatalogEntryUnified

**Purpose**: Unified command catalog entry extending base model

**Fields**:
```python
class CommandCatalogEntryUnified(UnifiedCatalogEntry):
    """Unified command catalog entry"""

    element_type: Literal["command"] = "command"

    # Command-specific fields
    aliases: List[str] = Field(default_factory=list)
    requires_tools: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    @field_validator('name')
    @classmethod
    def ensure_slash_prefix(cls, v: str) -> str:
        """Ensure command name starts with /"""
        if not v.startswith('/'):
            return f"/{v}"
        return v
```

---

#### Model: AgentCatalogEntryUnified

**Purpose**: Unified agent catalog entry extending base model

**Fields**:
```python
class AgentCatalogEntryUnified(UnifiedCatalogEntry):
    """Unified agent catalog entry"""

    element_type: Literal["agent"] = "agent"

    # Agent-specific fields
    model: str = Field(...)
    specialization: str = Field(default="general")
    requires_skills: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    @field_validator('model')
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Ensure model is valid Claude variant"""
        valid_models = [
            "claude-haiku-4-5",
            "claude-opus-4",
            "claude-sonnet-4",
            "claude-sonnet-4-5"
        ]
        if v not in valid_models:
            raise ValueError(f"Invalid model: {v}. Must be one of {valid_models}")
        return v
```

---

### Data Flow

#### Flow 1: List Elements

```
User: llm list skills --scope project
    │
    ▼
CLI: Parse args → element_type=SKILL, scope=PROJECT
    │
    ▼
CatalogManager.list_elements(SKILL, PROJECT)
    │
    ├──▶ Syncer.load_catalog(SKILL, PROJECT) → Load manifests/skills.json
    │
    ├──▶ Scanner.scan_skills(PROJECT) → Scan .claude/skills/
    │
    ├──▶ Syncer.merge_entries(existing, discovered) → Merge
    │
    ├──▶ Syncer.save_catalog(merged, SKILL, PROJECT) → Atomic save
    │
    └──▶ Return List[SkillCatalogEntryUnified]
    │
    ▼
CLI: Format output (table/JSON/condensed)
    │
    ▼
Display: Show table with skills
```

#### Flow 2: Search Elements

```
User: llm search "analysis" --type skills --scope project --tags validation
    │
    ▼
CLI: Parse args → query="analysis", type=SKILL, scope=PROJECT, tags=["validation"]
    │
    ▼
CatalogManager.search_elements(query="analysis", type=SKILL, scope=PROJECT, tags=["validation"])
    │
    ├──▶ CatalogManager.list_elements(SKILL, PROJECT) → Get all skills
    │
    └──▶ Searcher.search(entries, query="analysis") → Score & rank
          │
          ├──▶ Filter by type (SKILL)
          ├──▶ Filter by scope (PROJECT)
          ├──▶ Filter by tags (["validation"])
          ├──▶ Score matches (name, description, tags)
          └──▶ Sort by score (descending)
    │
    ▼
Return ranked List[SkillCatalogEntryUnified]
    │
    ▼
CLI: Format output
    │
    ▼
Display: Show ranked results
```

#### Flow 3: Sync Catalogs

```
User: llm sync catalogs --force
    │
    ▼
CLI: Trigger sync with force=True
    │
    ▼
CatalogManager.sync_catalogs(force=True)
    │
    ├──▶ For each catalog type (SKILL, COMMAND, AGENT):
    │     │
    │     ├──▶ Syncer.backup_catalog(type) → Create .backup
    │     │
    │     ├──▶ Syncer.load_catalog(type) → Load existing
    │     │
    │     ├──▶ Scanner.scan_{type}(ALL) → Scan filesystem
    │     │
    │     ├──▶ Syncer.merge_entries(existing, discovered) → Merge
    │     │
    │     └──▶ Syncer.save_catalog(merged, type) → Atomic write
    │
    └──▶ Return SyncResult (counts, errors)
    │
    ▼
CLI: Display sync summary
```

---

### Error Handling Strategy

**Exception Hierarchy**:
```python
class CatalogManifestError(Exception):
    """Base exception for catalog manifest system"""
    pass

class CatalogLoadError(CatalogManifestError):
    """Raised when catalog file cannot be loaded"""
    pass

class CatalogSaveError(CatalogManifestError):
    """Raised when catalog file cannot be saved"""
    pass

class ScanError(CatalogManifestError):
    """Raised when filesystem scan fails"""
    pass

class SearchError(CatalogManifestError):
    """Raised when search operation fails"""
    pass

class SyncError(CatalogManifestError):
    """Raised when catalog sync fails"""
    pass

class ValidationError(CatalogManifestError):
    """Raised when schema validation fails (wrap Pydantic ValidationError)"""
    pass
```

**Error Recovery**:
- **CatalogLoadError**: Try backup file → Create empty catalog → Log error
- **ScanError**: Skip unreadable files (warn) → Continue scan → Report warnings
- **SyncError**: Rollback to backup → Preserve original → Report error with resolution steps

---

## Library Documentation

### Library: Pydantic 2.9.2

**Purpose**: Data validation using Python type annotations
**Documentation**: https://docs.pydantic.dev/latest/
**Repository**: https://github.com/pydantic/pydantic

**Installation**:
```bash
# Already installed in project
uv pip show pydantic
```

**Key APIs Used**:
- `BaseModel`: Base class for data models
- `Field()`: Define field constraints and metadata
- `field_validator()`: Custom field validation (replaces `@validator` in v1)
- `model_config`: Configuration dict (replaces `Config` class in v1)
- `model_dump()`: Serialize to dict (replaces `.dict()` in v1)
- `model_dump_json()`: Serialize to JSON string
- `model_validate()`: Deserialize from dict (replaces `.parse_obj()` in v1)
- `model_validate_json()`: Deserialize from JSON string (replaces `.parse_raw()` in v1)

**Integration Pattern**:
```python
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from pathlib import Path

class CatalogEntry(BaseModel):
    # Pydantic 2.x configuration
    model_config = ConfigDict(
        json_encoders={Path: str, datetime: lambda v: v.isoformat()},
        validate_assignment=True
    )

    name: str = Field(..., min_length=1, max_length=100)
    path: Path = Field(...)

    # Pydantic 2.x validator
    @field_validator('path')
    @classmethod
    def validate_path(cls, v: Path) -> Path:
        return v.resolve()

# Serialize
entry = CatalogEntry(name="test", path=Path("/tmp"))
json_str = entry.model_dump_json()

# Deserialize
entry2 = CatalogEntry.model_validate_json(json_str)
```

**Best Practices**:
1. Use `model_config` instead of `Config` class (Pydantic 2.x)
2. Use `field_validator` instead of `@validator` (Pydantic 2.x)
3. Use `model_dump()` instead of `dict()` (Pydantic 2.x)
4. Enable `validate_assignment=True` for runtime validation
5. Use `Literal` for fixed choices instead of Enum (cleaner)

**Known Issues**: None for this use case

**Testing Notes**:
- **Mocking**: No need to mock Pydantic (use real validation in tests)
- **Test Data**: Use Pydantic models directly in fixtures

---

### Library: Click 8.1.7

**Purpose**: CLI framework for Python
**Documentation**: https://click.palletsprojects.com/
**Repository**: https://github.com/pallets/click

**Installation**:
```bash
# Already installed in project
uv pip show click
```

**Key APIs Used**:
- `@click.group()`: Define command group
- `@click.command()`: Define sub-command
- `@click.argument()`: Positional argument
- `@click.option()`: Named option with default and validation
- `click.Choice()`: Enum-like validation
- `click.echo()`: Print output (testable)
- `click.secho()`: Print colored output
- `CliRunner()`: Test CLI commands

**Integration Pattern**:
```python
import click
from .catalog_manager import CatalogManager

@click.group()
def cli():
    """LLM Configuration Management CLI"""
    pass

@cli.command()
@click.argument('element_type', type=click.Choice(['skills', 'commands', 'agents', 'all']))
@click.option('--scope', type=click.Choice(['global', 'project', 'local', 'all']), default='all')
@click.option('--format', type=click.Choice(['table', 'json', 'condensed']), default='table')
def list(element_type: str, scope: str, format: str):
    """List catalog elements."""
    catalog_mgr = CatalogManager(scope_manager)

    # Map string to enum
    elem_type = ElementType(element_type.rstrip('s'))  # 'skills' → 'skill'
    scope_enum = ScopeType(scope)

    elements = catalog_mgr.list_elements(elem_type, scope_enum)

    # Format output
    if format == 'json':
        click.echo(json.dumps([e.model_dump(mode='json') for e in elements], indent=2))
    elif format == 'table':
        # Use tabulate for table
        from tabulate import tabulate
        headers = ['Name', 'Type', 'Scope', 'Description']
        rows = [[e.name, e.element_type, e.scope, e.description[:50]] for e in elements]
        click.echo(tabulate(rows, headers=headers, tablefmt='grid'))

if __name__ == '__main__':
    cli()
```

**Best Practices**:
1. Use command groups for organized sub-commands
2. Use `click.Choice` for enum-like options
3. Use `click.echo()` instead of `print()` for testability
4. Color output with `click.secho()` for errors/warnings/success
5. Test with `CliRunner` for comprehensive CLI testing

**Testing Notes**:
```python
from click.testing import CliRunner

def test_list_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['list', 'skills', '--scope', 'project'])

    assert result.exit_code == 0
    assert 'Total:' in result.output
```

---

### Library: python-frontmatter 1.1.0

**Purpose**: Parse YAML frontmatter from Markdown files
**Documentation**: https://python-frontmatter.readthedocs.io/
**Repository**: https://github.com/eyeseast/python-frontmatter

**Installation**:
```bash
# ADD TO REQUIREMENTS
uv pip install python-frontmatter
```

**Key APIs Used**:
- `frontmatter.load(path)`: Load Markdown file with frontmatter
- `post.metadata`: Dict of YAML frontmatter
- `post.content`: Markdown content (without frontmatter)

**Integration Pattern**:
```python
import frontmatter
from pathlib import Path

skill_file = Path("/path/to/skill.md")

# Parse frontmatter
post = frontmatter.load(skill_file)

# Access metadata
title = post.metadata.get('title', '')
description = post.metadata.get('description', '')
template = post.metadata.get('template', 'basic')

# Access content
markdown = post.content
```

**Best Practices**:
1. Use `python-frontmatter` instead of manual YAML parsing
2. Handle missing frontmatter gracefully (check `post.metadata`)
3. Provide default values with `.get(key, default)`
4. Validate metadata with Pydantic after extraction

**Known Issues**: None

**Testing Notes**:
- **Mocking**: Create temporary Markdown files with frontmatter for tests
- **Fixtures**: Use `tmpdir` fixture with sample .md files

---

### Library: pathlib (stdlib)

**Purpose**: Object-oriented filesystem paths
**Documentation**: https://docs.python.org/3/library/pathlib.html

**Installation**: Built-in (Python 3.4+)

**Key APIs Used**:
- `Path()`: Create path object
- `Path.home()`: Get home directory
- `Path.cwd()`: Get current directory
- `path.resolve()`: Resolve to absolute path (follow symlinks)
- `path.exists()`: Check if path exists
- `path.is_dir()`: Check if directory
- `path.is_file()`: Check if file
- `path.iterdir()`: List directory contents
- `path.rglob(pattern)`: Recursive glob
- `path.read_text()`: Read file as text
- `path.write_text()`: Write text to file

**Integration Pattern**:
```python
from pathlib import Path

# Build paths
claude_dir = Path.home() / '.claude'
skills_dir = claude_dir / 'skills'

# Scan directory
for skill_dir in skills_dir.iterdir():
    if skill_dir.is_dir():
        # Find .md files
        for md_file in skill_dir.rglob('*.md'):
            content = md_file.read_text(encoding='utf-8')

# Validate path
def validate_path(path: Path, base: Path) -> bool:
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
```

**Best Practices**:
1. Use `Path` instead of string paths
2. Use `/` operator for path joining
3. Always `resolve()` paths before validation
4. Use `rglob()` for recursive searches
5. Validate with `relative_to()` to prevent path traversal

**Testing Notes**: Use `tmpdir` fixture for temporary directories in tests

---

### Library: tabulate 0.9.0 (Optional)

**Purpose**: Table formatting for CLI output
**Documentation**: https://github.com/astanin/python-tabulate

**Installation**:
```bash
# OPTIONAL (recommended for better UX)
uv pip install tabulate
```

**Key APIs Used**:
- `tabulate(data, headers, tablefmt)`: Format table

**Integration Pattern**:
```python
from tabulate import tabulate

headers = ['Name', 'Type', 'Scope']
rows = [
    ['analysis', 'skill', 'global'],
    ['implementation', 'skill', 'project']
]

table = tabulate(rows, headers=headers, tablefmt='grid')
print(table)

# Output:
# +--------------+-------+---------+
# | Name         | Type  | Scope   |
# +==============+=======+=========+
# | analysis     | skill | global  |
# +--------------+-------+---------+
# | implementation | skill | project |
# +--------------+-------+---------+
```

**Best Practices**: Use for table output format (default CLI output)

---

## Dependencies

### Dependency Tree

```
catalog_manifest/
├── pydantic==2.9.2          ✅ Available
│   ├── pydantic-core==2.23.4
│   ├── typing-extensions>=4.6.1
│   └── annotated-types>=0.4.0
├── click==8.1.7             ✅ Available
│   └── (no dependencies)
├── python-frontmatter==1.1.0 ⚠️ ADD TO REQUIREMENTS
│   └── PyYAML>=3.8
├── tabulate>=0.9.0          ⚠️ OPTIONAL (recommended)
│   └── (no dependencies)
└── pathlib                  ✅ Stdlib
```

### Installation Commands

**Required Dependencies**:
```bash
# Add to requirements.txt
echo "python-frontmatter>=1.0.0" >> requirements.txt

# Install with uv
uv pip install python-frontmatter

# Update lock file
uv sync
```

**Optional Dependencies**:
```bash
# Add tabulate for better CLI output
echo "tabulate>=0.9.0" >> requirements.txt
uv pip install tabulate
uv sync
```

**Verify Installation**:
```bash
uv pip show pydantic click python-frontmatter tabulate
uv pip check  # Verify no conflicts
```

### Compatibility Notes

**Python Version**: 3.11+ (project standard)

**All Dependencies Compatible**:
- pydantic 2.9.2 → Python ≥3.8 ✅
- click 8.1.7 → Python ≥3.7 ✅
- python-frontmatter 1.1.0 → Python ≥3.6 ✅
- tabulate 0.9.0 → Python ≥3.7 ✅

**No Dependency Conflicts**: All dependencies are mutually compatible

---

## Implementation Plan

### Overview

This implementation follows a **4-phase approach**, progressing from foundation (data models) to core components to integration to testing. Each phase builds on the previous and has validation checkpoints. Total estimated effort: **18-24 hours**.

### Phase 1: Foundation (6-8 hours)

**Goal**: Create unified data models and base infrastructure

**Tasks**:

1. **Project Structure** (30 min)
   - [ ] Create `src/tools/catalog_manifest/` directory
   - [ ] Create `__init__.py` with version and exports
   - [ ] Create `models.py` for Pydantic models
   - [ ] Create `exceptions.py` for custom exceptions
   - [ ] Create `constants.py` for constants (cache TTL, etc.)

2. **Data Models** (2-3 hours)
   - [ ] Create `ElementType` and `ScopeType` enums
   - [ ] Create `UnifiedCatalogEntry` base model with Pydantic 2.x
   - [ ] Create `SkillCatalogEntryUnified` with template validation
   - [ ] Create `CommandCatalogEntryUnified` with slash prefix validation
   - [ ] Create `AgentCatalogEntryUnified` with model validation
   - [ ] Create `SkillCatalogUnified`, `CommandCatalogUnified`, `AgentCatalogUnified` catalog models
   - [ ] Add JSON encoders for Path, datetime, UUID
   - [ ] Write unit tests for model validation (test_models.py)

3. **Exception Hierarchy** (30 min)
   - [ ] Create `CatalogManifestError` base exception
   - [ ] Create specific exceptions: `CatalogLoadError`, `CatalogSaveError`, `ScanError`, `SearchError`, `SyncError`
   - [ ] Write exception tests (test_exceptions.py)

4. **Dependencies** (1 hour)
   - [ ] Add `python-frontmatter>=1.0.0` to requirements.txt
   - [ ] Add `tabulate>=0.9.0` to requirements.txt (optional)
   - [ ] Run `uv sync` to update lock file
   - [ ] Verify installation with `uv pip check`
   - [ ] Commit updated `uv.lock`

**Validation Checkpoint**:
- [ ] All data models validate correctly with Pydantic
- [ ] Model serialization/deserialization works (JSON round-trip)
- [ ] All dependencies installed without conflicts
- [ ] Phase 1 tests pass: `pytest tests/test_catalog_manifest/unit/test_models.py`

---

### Phase 2: Core Components (6-8 hours)

**Goal**: Implement Scanner, Searcher, Syncer classes

**Tasks**:

1. **Scanner Implementation** (3-4 hours)
   - [ ] Create `scanner.py` with `Scanner` class
   - [ ] Implement `scan_skills()` with directory walking and frontmatter parsing
   - [ ] Implement `scan_commands()` with .md file parsing and slash prefix
   - [ ] Implement `scan_agents()` with .md file parsing and model validation
   - [ ] Implement `scan_all()` to scan all types
   - [ ] Add error handling for missing frontmatter, corrupted YAML
   - [ ] Add logging for warnings (skip files gracefully)
   - [ ] Write unit tests with mocked filesystem (test_scanner.py)

2. **Searcher Implementation** (1-2 hours)
   - [ ] Create `searcher.py` with `Searcher` class
   - [ ] Implement `search()` with scoring algorithm
   - [ ] Implement `filter_by_scope()`
   - [ ] Implement `filter_by_tags()` with match_all/match_any
   - [ ] Implement `filter_by_type()`
   - [ ] Write unit tests with sample data (test_searcher.py)

3. **Syncer Implementation** (2-3 hours)
   - [ ] Create `syncer.py` with `Syncer` class
   - [ ] Implement `load_catalog()` with Pydantic validation
   - [ ] Implement `save_catalog()` with atomic write (backup → temp → rename)
   - [ ] Implement `merge_entries()` with UUID matching strategy
   - [ ] Implement `backup_catalog()` for .backup file creation
   - [ ] Add error recovery (fallback to backup on load failure)
   - [ ] Write unit tests with temp directories (test_syncer.py)

**Validation Checkpoint**:
- [ ] Scanner discovers all test elements correctly
- [ ] Searcher ranks results by relevance
- [ ] Syncer loads/saves catalogs atomically
- [ ] Merge strategy works (discovered overrides existing)
- [ ] Phase 2 tests pass: `pytest tests/test_catalog_manifest/unit/test_scanner.py test_searcher.py test_syncer.py`

---

### Phase 3: Integration (4-6 hours)

**Goal**: Create CatalogManager facade and CLI interface

**Tasks**:

1. **CatalogManager Implementation** (2-3 hours)
   - [ ] Create `catalog_manager.py` with `CatalogManager` class
   - [ ] Implement `list_elements()` with auto-sync
   - [ ] Implement `search_elements()` with filters
   - [ ] Implement `get_element()` for single element lookup
   - [ ] Implement `sync_catalogs()` for manual sync
   - [ ] Add simple caching (60-second TTL)
   - [ ] Write integration tests with real Scanner/Searcher/Syncer (test_catalog_manager.py)

2. **CLI Interface** (2-3 hours)
   - [ ] Create `cli.py` with Click command group
   - [ ] Implement `llm list` command with element_type, scope, format options
   - [ ] Implement `llm search` command with query, type, scope, tags, limit options
   - [ ] Implement `llm show` command for single element details
   - [ ] Implement `llm sync` command for manual catalog sync
   - [ ] Add table formatting with tabulate
   - [ ] Add JSON output format
   - [ ] Add condensed output format
   - [ ] Write CLI tests with CliRunner (test_cli.py)

3. **Integration with Main CLI** (30 min)
   - [ ] Register catalog commands with main `llm` CLI
   - [ ] Update main CLI help text
   - [ ] Test CLI integration end-to-end

**Validation Checkpoint**:
- [ ] All CLI commands work correctly
- [ ] Table output is readable and formatted
- [ ] JSON output is valid
- [ ] End-to-end flows work (list → search → show)
- [ ] Phase 3 tests pass: `pytest tests/test_catalog_manifest/integration/`

---

### Phase 4: Testing & Validation (2-4 hours)

**Goal**: Comprehensive testing and final validation

**Tasks**:

1. **Unit Test Coverage** (1-2 hours)
   - [ ] Achieve 80%+ unit test coverage
   - [ ] Test all edge cases (empty catalogs, missing files, corrupted YAML)
   - [ ] Test all validation errors (invalid UUID, bad paths, etc.)
   - [ ] Run coverage report: `pytest --cov=src/tools/catalog_manifest --cov-report=html`
   - [ ] Review coverage report and add missing tests

2. **Integration Testing** (1 hour)
   - [ ] Test complete sync workflow (scan → merge → save)
   - [ ] Test search with various filters
   - [ ] Test CLI commands end-to-end
   - [ ] Test with real .claude/ directory structure

3. **Security Validation** (30 min)
   - [ ] Test path validation (prevent ../../../etc/passwd)
   - [ ] Test input sanitization in search queries
   - [ ] Test YAML parsing with malicious input
   - [ ] Verify no secrets in logs or output

4. **Documentation** (30 min)
   - [ ] Add docstrings to all public methods (Google style)
   - [ ] Create README.md for catalog_manifest tool
   - [ ] Add usage examples to README
   - [ ] Update main project README with catalog commands

**Final Validation**:
- [ ] All acceptance criteria met (see Success Criteria section)
- [ ] All tests pass: `pytest tests/test_catalog_manifest/`
- [ ] Coverage ≥ 80%: Check htmlcov/index.html
- [ ] Security validation complete
- [ ] Documentation complete
- [ ] No linting errors: `black src/tools/catalog_manifest/ tests/test_catalog_manifest/`
- [ ] Type checking passes: `mypy src/tools/catalog_manifest/`

---

## Testing Strategy

### Overview

Comprehensive testing approach with **80%+ code coverage target**, including unit tests (with mocks), integration tests (with temp directories), and CLI tests (with CliRunner).

### Unit Testing

**Scope**: Individual classes and methods in isolation

**Framework**: pytest

**Coverage Target**: 80%+ for all modules

**Mocking Strategy**:
- Mock filesystem with `tmpdir` fixture
- Mock ScopeManager for isolated Scanner/Syncer tests
- No need to mock Pydantic (use real validation)

**Test Structure**:
```
tests/test_catalog_manifest/
├── unit/
│   ├── test_models.py          # Pydantic model validation
│   ├── test_scanner.py         # Scanner with mocked filesystem
│   ├── test_searcher.py        # Searcher with sample data
│   ├── test_syncer.py          # Syncer with temp directories
│   └── test_exceptions.py      # Exception hierarchy
```

**Example Unit Test**:
```python
import pytest
from pathlib import Path
from catalog_manifest.scanner import Scanner
from catalog_manifest.models import SkillCatalogEntryUnified, ScopeType

def test_scanner_discovers_skills(tmpdir):
    """Test Scanner discovers skills from directory."""
    # Create test skill directory
    skills_dir = Path(tmpdir) / '.claude' / 'skills' / 'test-skill'
    skills_dir.mkdir(parents=True)

    # Create skill.md with frontmatter
    skill_file = skills_dir / 'skill.md'
    skill_file.write_text("""---
description: Test skill
template: basic
---
# Test Skill
""")

    # Mock ScopeManager
    mock_scope = Mock()
    mock_scope.get_global_path.return_value = Path(tmpdir) / '.claude'

    # Test scan
    scanner = Scanner(mock_scope)
    skills = scanner.scan_skills(ScopeType.GLOBAL)

    assert len(skills) == 1
    assert skills[0].name == 'test-skill'
    assert skills[0].description == 'Test skill'
    assert skills[0].template == 'basic'
```

**Key Test Cases**:
- [ ] **Models**: Test all field validations, JSON serialization, edge cases
- [ ] **Scanner**: Test skill/command/agent discovery, frontmatter parsing, error handling
- [ ] **Searcher**: Test search scoring, tag filtering, scope filtering
- [ ] **Syncer**: Test load/save, atomic writes, backup/restore, merge strategy

---

### Integration Testing

**Scope**: Components working together

**Framework**: pytest with temp directories

**Test Structure**:
```
tests/test_catalog_manifest/
├── integration/
│   ├── test_catalog_manager.py   # CatalogManager integration
│   ├── test_sync_workflow.py     # Complete sync flow
│   └── test_cli.py               # CLI integration with CliRunner
```

**Example Integration Test**:
```python
from click.testing import CliRunner
from catalog_manifest.cli import cli

def test_list_command_integration(tmpdir):
    """Test 'llm list skills' command end-to-end."""
    # Set up test directory structure
    setup_test_catalog_structure(tmpdir)

    # Run CLI command
    runner = CliRunner()
    result = runner.invoke(cli, ['list', 'skills', '--scope', 'project'])

    assert result.exit_code == 0
    assert 'Total: 2 elements' in result.output
    assert 'test-skill-1' in result.output
```

**Key Test Cases**:
- [ ] **CatalogManager**: Test list, search, sync operations
- [ ] **Sync Workflow**: Test complete scan → merge → save flow
- [ ] **CLI**: Test all commands with different options

---

### Performance Testing

**Scope**: Verify performance meets targets

**Tools**: pytest-benchmark

**Target Metrics**:
- List 100 elements: < 500ms
- Search 100 elements: < 200ms
- Sync all catalogs: < 1000ms

**Test Cases**:
```python
def test_search_performance(benchmark):
    """Benchmark search on 100 elements."""
    # Create 100 test entries
    entries = create_test_entries(100)
    searcher = Searcher()

    # Benchmark search
    result = benchmark(searcher.search, entries, "test query")

    assert benchmark.stats.stats.mean < 0.2  # < 200ms
```

---

### Security Testing

**Scope**: Verify security controls

**Test Cases**:
- [ ] Path traversal prevention (validate `../../../etc/passwd` rejected)
- [ ] Search query sanitization (no regex injection)
- [ ] YAML parsing safety (no code execution from frontmatter)
- [ ] Secrets not in logs or catalog output

**Example Security Test**:
```python
def test_path_traversal_prevention():
    """Test path validation prevents traversal."""
    base = Path.home() / '.claude'
    malicious_path = base / '..' / '..' / 'etc' / 'passwd'

    with pytest.raises(ValueError):
        validate_path(malicious_path, base)
```

---

### Running Tests

**All Tests**:
```bash
pytest tests/test_catalog_manifest/
```

**Unit Tests Only**:
```bash
pytest tests/test_catalog_manifest/unit/
```

**With Coverage**:
```bash
pytest --cov=src/tools/catalog_manifest --cov-report=html
open htmlcov/index.html  # View coverage report
```

**With Verbose Output**:
```bash
pytest -v tests/test_catalog_manifest/
```

---

## Documentation Requirements

### Code Documentation

**All public methods must have Google-style docstrings**:
```python
def search_elements(
    self,
    query: str,
    element_type: ElementType = ElementType.ALL,
    scope: ScopeType = ScopeType.ALL,
    tags: Optional[List[str]] = None,
    limit: int = 20
) -> List[UnifiedCatalogEntry]:
    """
    Search elements with query and filters.

    Searches across name, description, and tags with relevance scoring.
    Results are ranked by score (exact name > name contains > description > tags).

    Args:
        query: Search query string (case-insensitive)
        element_type: Filter by type (skill/command/agent/all)
        scope: Filter by scope (global/project/local/all)
        tags: Filter by tags (all must match if provided)
        limit: Max results to return (default: 20)

    Returns:
        Ranked list of matching catalog entries

    Raises:
        SearchError: If search query is invalid

    Example:
        >>> catalog_mgr = CatalogManager(scope_manager)
        >>> results = catalog_mgr.search_elements(
        ...     query="analysis",
        ...     element_type=ElementType.SKILL,
        ...     scope=ScopeType.PROJECT,
        ...     tags=["validation"]
        ... )
        >>> print(f"Found {len(results)} skills")
    """
```

### User Documentation

**Create README.md** in `src/tools/catalog_manifest/`:
- Overview of catalog manifest system
- Installation instructions
- CLI command reference with examples
- Troubleshooting guide

**Example README Section**:
```markdown
## Usage

### List All Skills

```bash
llm list skills
```

### List Project-Scoped Commands

```bash
llm list commands --scope project
```

### Search for Elements

```bash
llm search "analysis" --type skills --tags validation
```

### Show Element Details

```bash
llm show skill analysis-specialist
```

### Manually Sync Catalogs

```bash
llm sync catalogs --force
```
```

### API Documentation

- All public methods have complete docstrings
- Pydantic models self-document via Field descriptions
- Generate API docs with Sphinx (future enhancement)

---

## Success Criteria

### Acceptance Criteria (from Requirements)

From analysis document:

- [ ] **AC-001**: `manifests/skills.json` schema defined with Pydantic models
- [ ] **AC-002**: `manifests/commands.json` schema defined with Pydantic models
- [ ] **AC-003**: `manifests/agents.json` schema defined with Pydantic models
- [ ] **AC-004**: Auto-discovery scans `.claude/` directories and extracts frontmatter metadata
- [ ] **AC-005**: Search and filter functions operational with relevance scoring
- [ ] **AC-006**: Standard metadata fields present: id, name, description, scope, path, created_at, updated_at
- [ ] **AC-007**: CLI command `llm list skills|commands|agents|all` implemented
- [ ] **AC-008**: Unit tests with minimum 80% coverage

### Implementation Criteria

- [ ] **IC-001**: All unified data models (UnifiedCatalogEntry, Skill/Command/Agent variants) implemented with Pydantic 2.x validation
- [ ] **IC-002**: Scanner component scans all three element types with frontmatter extraction
- [ ] **IC-003**: Searcher component filters and ranks results with scoring algorithm
- [ ] **IC-004**: Syncer component loads/saves catalogs atomically with backup pattern
- [ ] **IC-005**: CatalogManager facade coordinates all operations with auto-sync
- [ ] **IC-006**: CLI interface implemented with Click (list, search, show, sync commands)
- [ ] **IC-007**: All library integrations working (Pydantic, Click, python-frontmatter, pathlib)

### Testing Criteria

- [ ] **TC-001**: Unit test coverage ≥ 80% (verify with pytest --cov)
- [ ] **TC-002**: All unit tests passing (models, scanner, searcher, syncer)
- [ ] **TC-003**: All integration tests passing (catalog_manager, sync workflow, CLI)
- [ ] **TC-004**: Performance tests meet targets (list <500ms, search <200ms, sync <1000ms)
- [ ] **TC-005**: Security tests passing (path validation, input sanitization)

### Code Quality Criteria

- [ ] **QC-001**: Linting passes (black, isort)
- [ ] **QC-002**: Type checking passes (mypy)
- [ ] **QC-003**: All functions have Google-style docstrings
- [ ] **QC-004**: Complex logic has explanatory comments
- [ ] **QC-005**: No critical security vulnerabilities (bandit scan)

### Documentation Criteria

- [ ] **DC-001**: README.md created with usage examples
- [ ] **DC-002**: All public methods have complete docstrings
- [ ] **DC-003**: CLI help text is clear and accurate (`llm list --help`)
- [ ] **DC-004**: Main project README updated with catalog manifest commands
- [ ] **DC-005**: CHANGELOG.md updated with feature entry

### Deployment Criteria

- [ ] **DEP-001**: All dependencies added to requirements.txt and uv.lock committed
- [ ] **DEP-002**: Feature works on clean install (`uv sync` → `llm list skills`)
- [ ] **DEP-003**: No breaking changes to existing catalogs (backward compatible)
- [ ] **DEP-004**: Feature integrated with main `llm` CLI
- [ ] **DEP-005**: No critical errors in production usage

### Definition of Done

All of the following must be true:
- ✅ All acceptance criteria met
- ✅ All implementation criteria met
- ✅ All testing criteria met (80%+ coverage)
- ✅ All code quality criteria met (linting, type checking, docstrings)
- ✅ All documentation criteria met (README, docstrings, CHANGELOG)
- ✅ All deployment criteria met (dependencies installed, CLI integrated)
- ✅ Feature reviewed and approved
- ✅ Feature in use and stable

---

## Risks & Mitigations

### Risk 1: Catalog Schema Incompatibility

**Probability**: Medium | **Impact**: High

**Description**: Existing catalogs (skills.json, commands.json, agents.json) have different schemas; unifying them may break backward compatibility.

**Mitigation**:
- Create separate unified models alongside existing ones (composition, not refactoring)
- Maintain read/write compatibility with existing catalog formats
- Version schema (start at 1.0) with migration support
- Use adapter pattern to convert between formats

**Testing**: Unit tests for schema migrations, backward compatibility tests, round-trip tests

---

### Risk 2: Performance Degradation on Large Catalogs

**Probability**: Low | **Impact**: Medium

**Description**: Scanning large directory structures or searching 100+ elements could be slow.

**Mitigation**:
- Lazy loading (don't load catalogs at initialization)
- Caching (cache catalog in memory for 60s)
- Performance targets enforced (search <500ms, sync <1000ms)
- Use generators for large datasets
- Consider indexing if catalog grows (future enhancement)

**Testing**: Benchmark with 100+ elements, memory profiling, search performance tests

---

### Risk 3: File System Race Conditions

**Probability**: Low | **Impact**: High

**Description**: Concurrent catalog updates could cause corruption.

**Mitigation**:
- Atomic writes (backup → temp → rename pattern) - PROVEN by skill_builder, agent_builder
- Backup before write
- File locking (optional future enhancement)
- Transactional semantics

**Testing**: Concurrent write tests, corruption recovery tests, backup validation tests

---

### Risk 4: Scope Manager Integration Complexity

**Probability**: Medium | **Impact**: Medium

**Description**: ScopeManager API might not align perfectly with catalog discovery needs.

**Mitigation**:
- Audit ScopeManager API early in Phase 1
- Create wrapper functions if needed
- Document integration points clearly
- Fallback to hardcoded paths if ScopeManager unavailable

**Testing**: ScopeManager integration tests, fallback handling tests

---

### Risk 5: Catalog Staleness

**Probability**: Medium | **Impact**: Medium

**Description**: Catalogs might not stay in sync with filesystem.

**Mitigation**:
- Auto-sync on `llm list` (scan → merge) with 60s cache
- Optional background watcher (future)
- Manual sync command: `llm sync catalogs`
- Timestamp tracking for staleness detection

**Testing**: Sync accuracy tests, staleness detection tests

---

## Appendix: File Structure

**Complete file structure after implementation**:

```
src/tools/catalog_manifest/
├── __init__.py              # Package init with exports
├── models.py                # Pydantic models (400 lines)
├── exceptions.py            # Exception hierarchy (50 lines)
├── constants.py             # Constants (cache TTL, etc.) (30 lines)
├── scanner.py               # Scanner class (300 lines)
├── searcher.py              # Searcher class (150 lines)
├── syncer.py                # Syncer class (250 lines)
├── catalog_manager.py       # CatalogManager facade (200 lines)
├── cli.py                   # Click CLI interface (200 lines)
└── README.md                # User documentation

tests/test_catalog_manifest/
├── unit/
│   ├── test_models.py       # Model validation tests
│   ├── test_scanner.py      # Scanner tests (mocked)
│   ├── test_searcher.py     # Searcher tests
│   ├── test_syncer.py       # Syncer tests (temp dirs)
│   └── test_exceptions.py   # Exception tests
├── integration/
│   ├── test_catalog_manager.py  # Integration tests
│   ├── test_sync_workflow.py    # Complete sync flow
│   └── test_cli.py              # CLI tests (CliRunner)
└── fixtures/
    └── sample_elements/     # Sample skills/commands/agents for tests
```

**Total Lines of Code**: ~1,800 (within 500-line limit per file)

---

## Appendix: Commands Reference

**CLI Commands Quick Reference**:

```bash
# List elements
llm list skills                      # List all skills
llm list commands --scope project    # List project commands
llm list agents --scope global       # List global agents
llm list all --format json           # List all as JSON

# Search elements
llm search "analysis"                # Search all types
llm search "test" --type skills      # Search skills only
llm search "api" --scope project --tags validation  # Search with filters

# Show element details
llm show skill analysis-specialist   # Show skill details
llm show command /feature-implement  # Show command details
llm show agent implementation        # Show agent details

# Sync catalogs
llm sync catalogs                    # Sync with filesystem
llm sync catalogs --force            # Force sync (ignore cache)
```

---

**PRP Complete**: 2025-10-30

**Status**: ✅ Ready for Phase 3 (Implementation)

**Next Step**: Begin Phase 1 - Foundation
