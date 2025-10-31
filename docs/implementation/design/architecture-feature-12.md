# Architecture Design: Feature #12 - Catalog Manifest System

**Designer**: architecture-designer (Opus + sequential-thinking MCP)
**Date**: 2025-10-30
**Issue**: #12
**Status**: DESIGN_COMPLETE

---

## Executive Summary

This document provides the complete architecture design for the unified catalog manifest system. The design extends existing catalog models (SkillCatalog, CommandCatalog, AgentCatalog) with a unified interface while maintaining backward compatibility.

**Key Design Principles**:
1. **Composition over Inheritance**: Wrap existing models rather than refactor
2. **Single Responsibility**: Each class has one clear purpose
3. **Open/Closed**: Extensible for future catalog types (hooks, plugins, prompts)
4. **Type Safety**: Pydantic validation throughout

---

## 1. Component Architecture

### 1.1 High-Level Architecture

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

### 1.2 Component Breakdown

#### Component A: CatalogManager
**Purpose**: Facade providing unified interface for all catalog operations

**Responsibilities**:
- Initialize and coordinate Scanner, Searcher, Syncer
- Provide high-level API for listing, searching, showing elements
- Handle scope resolution (global/project/local)
- Manage catalog lifecycle (load → sync → save)

**Public API**:
```python
class CatalogManager:
    def list_elements(
        element_type: ElementType,
        scope: ScopeType = ScopeType.ALL,
        format: OutputFormat = OutputFormat.TABLE
    ) -> List[UnifiedCatalogEntry]

    def search_elements(
        query: str,
        element_type: ElementType = ElementType.ALL,
        scope: ScopeType = ScopeType.ALL,
        tags: List[str] = None
    ) -> List[UnifiedCatalogEntry]

    def get_element(
        name: str,
        element_type: ElementType = ElementType.ALL
    ) -> Optional[UnifiedCatalogEntry]

    def sync_catalogs(
        force: bool = False
    ) -> SyncResult
```

**Dependencies**: Scanner, Searcher, Syncer, ScopeManager

---

#### Component B: Scanner
**Purpose**: Auto-discovery of installed elements from filesystem

**Responsibilities**:
- Walk directory trees (`.claude/skills`, `.claude/commands`, `.claude/agents`)
- Identify element files based on patterns
- Extract metadata from YAML frontmatter
- Create UnifiedCatalogEntry instances
- Handle malformed or missing files gracefully

**Public API**:
```python
class Scanner:
    def scan_skills(
        scope: ScopeType = ScopeType.ALL
    ) -> List[SkillCatalogEntryUnified]

    def scan_commands(
        scope: ScopeType = ScopeType.ALL
    ) -> List[CommandCatalogEntryUnified]

    def scan_agents(
        scope: ScopeType = ScopeType.ALL
    ) -> List[AgentCatalogEntryUnified]

    def scan_all(
        scope: ScopeType = ScopeType.ALL
    ) -> Dict[str, List[UnifiedCatalogEntry]]
```

**Scanning Rules**:
```python
# Skills: Directories containing .md files
# Pattern: ~/.claude/skills/{skill-name}/*.md
# Metadata: Extract from first .md file with YAML frontmatter

# Commands: .md files in commands/ directory
# Pattern: ~/.claude/commands/{command-name}.md
# Metadata: Extract from YAML frontmatter
# Name: Prefix with '/' if not present

# Agents: .md files in agents/ directory
# Pattern: ~/.claude/agents/{agent-name}.md
# Metadata: Extract from YAML frontmatter including 'model' field
```

**Error Handling**:
- Skip files without YAML frontmatter (warn)
- Skip directories without .md files (silent)
- Skip corrupted YAML (warn, continue)
- Report all warnings via logging

**Dependencies**: ScopeManager, pathlib, YAML parser (PyYAML or frontmatter)

---

#### Component C: Searcher
**Purpose**: Search and filter operations on catalog entries

**Responsibilities**:
- Full-text search on name, description, tags
- Filter by scope (global/project/local)
- Filter by tags
- Filter by element type
- Sort results by relevance, date, name

**Public API**:
```python
class Searcher:
    def search(
        entries: List[UnifiedCatalogEntry],
        query: str,
        element_type: ElementType = ElementType.ALL,
        scope: ScopeType = ScopeType.ALL,
        tags: List[str] = None
    ) -> List[UnifiedCatalogEntry]

    def filter_by_scope(
        entries: List[UnifiedCatalogEntry],
        scope: ScopeType
    ) -> List[UnifiedCatalogEntry]

    def filter_by_tags(
        entries: List[UnifiedCatalogEntry],
        tags: List[str],
        match_all: bool = False
    ) -> List[UnifiedCatalogEntry]

    def filter_by_type(
        entries: List[UnifiedCatalogEntry],
        element_type: ElementType
    ) -> List[UnifiedCatalogEntry]
```

**Search Algorithm**:
```python
# 1. Query tokenization (split on whitespace)
# 2. Search fields: name, description, tags
# 3. Scoring:
#    - Exact name match: +100
#    - Name contains: +50
#    - Description contains: +10
#    - Tag match: +20
# 4. Sort by score (descending)
# 5. Return top N results
```

**Dependencies**: None (operates on in-memory data)

---

#### Component D: Syncer
**Purpose**: Load and save catalog manifest files atomically

**Responsibilities**:
- Load existing catalogs from JSON files
- Merge scanned entries with existing catalogs
- Atomic save (temp file + rename pattern)
- Backup creation before writes
- Schema validation on load and save

**Public API**:
```python
class Syncer:
    def load_catalog(
        catalog_type: ElementType,
        scope: ScopeType = ScopeType.PROJECT
    ) -> Union[SkillCatalog, CommandCatalog, AgentCatalog]

    def save_catalog(
        catalog: Union[SkillCatalog, CommandCatalog, AgentCatalog],
        catalog_type: ElementType,
        scope: ScopeType = ScopeType.PROJECT
    ) -> None

    def merge_entries(
        existing: List[UnifiedCatalogEntry],
        discovered: List[UnifiedCatalogEntry]
    ) -> List[UnifiedCatalogEntry]

    def backup_catalog(
        catalog_type: ElementType,
        scope: ScopeType = ScopeType.PROJECT
    ) -> Path
```

**Atomic Write Pattern**:
```python
# 1. Create backup: {catalog}.json.backup
# 2. Write to temp: {catalog}.json.tmp
# 3. Validate temp file (load + schema check)
# 4. Rename temp → original (atomic on POSIX)
# 5. Delete backup after successful write
```

**Merge Strategy**:
```python
# Compare by 'id' field (UUID)
# - Entry in both: Update 'updated_at', merge metadata
# - Entry only in discovered: Add as new
# - Entry only in existing: Keep (don't delete)
# - Conflict resolution: Filesystem wins (discovered > existing)
```

**Dependencies**: pathlib, json, Pydantic models

---

## 2. Data Models

### 2.1 Unified Base Model

```python
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4
from datetime import datetime
from pathlib import Path
from enum import Enum
from typing import Dict, Any, List, Optional

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

    # Core identity
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)

    # Scope and location
    scope: ScopeType = Field(..., exclude={"all"})
    path: Path = Field(...)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Type discriminator (for polymorphism)
    element_type: ElementType = Field(..., exclude={"all"})

    # Generic metadata (element-specific data)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @validator('path')
    def validate_path(cls, v: Path) -> Path:
        """Ensure path is absolute and exists"""
        resolved = v.resolve()
        if not resolved.exists():
            raise ValueError(f"Path does not exist: {resolved}")
        return resolved

    @validator('name')
    def validate_name(cls, v: str) -> str:
        """Ensure name is valid (no slashes except for commands)"""
        if '/' in v and not v.startswith('/'):
            raise ValueError("Name contains invalid characters")
        return v

    class Config:
        json_encoders = {
            Path: str,
            datetime: lambda v: v.isoformat(),
            UUID: str
        }
```

### 2.2 Skill Catalog Entry

```python
class SkillMetadata(BaseModel):
    """Skill-specific metadata"""
    template: str = Field(..., description="Skill template type")
    has_scripts: bool = Field(default=False)
    file_count: int = Field(default=0, ge=0)
    allowed_tools: List[str] = Field(default_factory=list)

class SkillCatalogEntryUnified(UnifiedCatalogEntry):
    """Unified skill catalog entry"""

    element_type: ElementType = Field(default=ElementType.SKILL, const=True)

    # Skill-specific fields (from existing SkillCatalogEntry)
    template: str = Field(...)
    has_scripts: bool = Field(default=False)
    file_count: int = Field(default=0, ge=0)
    allowed_tools: List[str] = Field(default_factory=list)

    @validator('template')
    def validate_template(cls, v: str) -> str:
        """Ensure template is valid"""
        valid_templates = ["basic", "analysis", "implementation", "validation"]
        if v not in valid_templates:
            raise ValueError(f"Invalid template: {v}. Must be one of {valid_templates}")
        return v

    def to_metadata_dict(self) -> SkillMetadata:
        """Convert to metadata dictionary"""
        return SkillMetadata(
            template=self.template,
            has_scripts=self.has_scripts,
            file_count=self.file_count,
            allowed_tools=self.allowed_tools
        )
```

### 2.3 Command Catalog Entry

```python
class CommandMetadata(BaseModel):
    """Command-specific metadata"""
    aliases: List[str] = Field(default_factory=list)
    requires_tools: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

class CommandCatalogEntryUnified(UnifiedCatalogEntry):
    """Unified command catalog entry"""

    element_type: ElementType = Field(default=ElementType.COMMAND, const=True)

    # Command-specific fields
    aliases: List[str] = Field(default_factory=list)
    requires_tools: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    @validator('name')
    def ensure_slash_prefix(cls, v: str) -> str:
        """Ensure command name starts with /"""
        if not v.startswith('/'):
            return f"/{v}"
        return v

    def to_metadata_dict(self) -> CommandMetadata:
        """Convert to metadata dictionary"""
        return CommandMetadata(
            aliases=self.aliases,
            requires_tools=self.requires_tools,
            tags=self.tags
        )
```

### 2.4 Agent Catalog Entry

```python
class AgentMetadata(BaseModel):
    """Agent-specific metadata"""
    model: str = Field(..., description="Claude model variant")
    specialization: str = Field(default="general")
    requires_skills: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

class AgentCatalogEntryUnified(UnifiedCatalogEntry):
    """Unified agent catalog entry"""

    element_type: ElementType = Field(default=ElementType.AGENT, const=True)

    # Agent-specific fields
    model: str = Field(...)
    specialization: str = Field(default="general")
    requires_skills: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

    @validator('model')
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

    def to_metadata_dict(self) -> AgentMetadata:
        """Convert to metadata dictionary"""
        return AgentMetadata(
            model=self.model,
            specialization=self.specialization,
            requires_skills=self.requires_skills,
            tags=self.tags
        )
```

### 2.5 Catalog Manifest Models

```python
class SkillCatalogUnified(BaseModel):
    """Unified skill catalog with schema versioning"""
    schema_version: str = Field(default="1.0")
    last_synced: datetime = Field(default_factory=datetime.utcnow)
    skills: List[SkillCatalogEntryUnified] = Field(default_factory=list)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CommandCatalogUnified(BaseModel):
    """Unified command catalog with schema versioning"""
    schema_version: str = Field(default="1.0")
    last_synced: datetime = Field(default_factory=datetime.utcnow)
    commands: List[CommandCatalogEntryUnified] = Field(default_factory=list)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AgentCatalogUnified(BaseModel):
    """Unified agent catalog with schema versioning"""
    schema_version: str = Field(default="1.0")
    last_synced: datetime = Field(default_factory=datetime.utcnow)
    agents: List[AgentCatalogEntryUnified] = Field(default_factory=list)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

---

## 3. Data Flow

### 3.1 List Elements Flow

```
User: llm list skills
    │
    ▼
CLI Layer: Parse command → element_type=SKILL, scope=ALL
    │
    ▼
CatalogManager.list_elements(element_type=SKILL, scope=ALL)
    │
    ├──▶ Syncer.load_catalog(SKILL) → Load existing skills.json
    │
    ├──▶ Scanner.scan_skills(ALL) → Discover skills on filesystem
    │
    ├──▶ Syncer.merge_entries(existing, discovered) → Merge catalogs
    │
    ├──▶ Syncer.save_catalog(merged) → Save updated catalog atomically
    │
    └──▶ Return List[SkillCatalogEntryUnified]
    │
    ▼
CLI Layer: Format output (table/JSON/condensed)
    │
    ▼
Display to user
```

### 3.2 Search Elements Flow

```
User: llm search "analysis" --type skills --scope project
    │
    ▼
CLI Layer: Parse command → query="analysis", element_type=SKILL, scope=PROJECT
    │
    ▼
CatalogManager.search_elements(query="analysis", element_type=SKILL, scope=PROJECT)
    │
    ├──▶ CatalogManager.list_elements(SKILL, PROJECT) → Get all skills
    │
    └──▶ Searcher.search(entries, query="analysis") → Filter & score
    │
    ▼
Return ranked List[SkillCatalogEntryUnified]
    │
    ▼
CLI Layer: Format output
    │
    ▼
Display to user
```

### 3.3 Sync Catalogs Flow

```
User: llm sync catalogs
    │
    ▼
CLI Layer: Trigger sync
    │
    ▼
CatalogManager.sync_catalogs(force=True)
    │
    ├──▶ For each catalog type (skills, commands, agents):
    │     │
    │     ├──▶ Syncer.backup_catalog(type) → Create .backup file
    │     │
    │     ├──▶ Syncer.load_catalog(type) → Load existing
    │     │
    │     ├──▶ Scanner.scan_{type}(ALL) → Discover all scopes
    │     │
    │     ├──▶ Syncer.merge_entries(existing, discovered)
    │     │
    │     └──▶ Syncer.save_catalog(merged) → Atomic write
    │
    └──▶ Return SyncResult (counts, errors)
    │
    ▼
Display sync summary to user
```

### 3.4 Show Element Flow

```
User: llm show skill analysis
    │
    ▼
CLI Layer: Parse command → name="analysis", element_type=SKILL
    │
    ▼
CatalogManager.get_element(name="analysis", element_type=SKILL)
    │
    ├──▶ CatalogManager.list_elements(SKILL, ALL) → Get all skills
    │
    └──▶ Filter by name (exact match or fuzzy)
    │
    ▼
Return Optional[SkillCatalogEntryUnified]
    │
    ▼
CLI Layer: Format detailed output (all fields)
    │
    ▼
Display to user
```

---

## 4. API Contracts

### 4.1 CatalogManager API

```python
from typing import List, Optional, Dict, Any
from pathlib import Path

class CatalogManager:
    """
    Unified interface for catalog operations.

    Coordinates Scanner, Searcher, and Syncer to provide
    high-level operations: list, search, show, sync.
    """

    def __init__(self, scope_manager: ScopeManager):
        """
        Initialize CatalogManager with scope resolution.

        Args:
            scope_manager: ScopeManager instance for path resolution
        """
        self.scope_manager = scope_manager
        self.scanner = Scanner(scope_manager)
        self.searcher = Searcher()
        self.syncer = Syncer(scope_manager)

    def list_elements(
        self,
        element_type: ElementType,
        scope: ScopeType = ScopeType.ALL,
        format: OutputFormat = OutputFormat.TABLE,
        auto_sync: bool = True
    ) -> List[UnifiedCatalogEntry]:
        """
        List all elements of specified type and scope.

        Args:
            element_type: Type of elements (skill/command/agent)
            scope: Scope filter (global/project/local/all)
            format: Output format (table/json/condensed)
            auto_sync: Auto-sync before listing

        Returns:
            List of unified catalog entries

        Raises:
            CatalogLoadError: If catalog file is corrupted
            ScanError: If filesystem scan fails
        """
        pass

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

        Args:
            query: Search query string
            element_type: Filter by type
            scope: Filter by scope
            tags: Filter by tags (all must match)
            limit: Max results to return

        Returns:
            Ranked list of matching entries

        Raises:
            SearchError: If search query is invalid
        """
        pass

    def get_element(
        self,
        name: str,
        element_type: ElementType = ElementType.ALL,
        fuzzy: bool = False
    ) -> Optional[UnifiedCatalogEntry]:
        """
        Get single element by name.

        Args:
            name: Element name (exact or fuzzy)
            element_type: Filter by type
            fuzzy: Enable fuzzy matching

        Returns:
            Matching entry or None
        """
        pass

    def sync_catalogs(
        self,
        element_types: Optional[List[ElementType]] = None,
        force: bool = False
    ) -> SyncResult:
        """
        Synchronize catalogs with filesystem.

        Args:
            element_types: Types to sync (default: all)
            force: Force sync even if recently synced

        Returns:
            SyncResult with counts and errors

        Raises:
            SyncError: If sync fails critically
        """
        pass
```

### 4.2 Scanner API

```python
class Scanner:
    """
    Auto-discovery of elements from filesystem.

    Scans .claude/ directories for skills, commands, agents
    and extracts metadata from YAML frontmatter.
    """

    def __init__(self, scope_manager: ScopeManager):
        """
        Initialize Scanner with scope resolution.

        Args:
            scope_manager: ScopeManager for base path resolution
        """
        self.scope_manager = scope_manager

    def scan_skills(
        self,
        scope: ScopeType = ScopeType.ALL
    ) -> List[SkillCatalogEntryUnified]:
        """
        Scan for installed skills.

        Pattern: .claude/skills/{skill-name}/*.md
        Metadata: YAML frontmatter from first .md file

        Args:
            scope: Scope to scan (global/project/local/all)

        Returns:
            List of discovered skill entries

        Raises:
            ScanError: If directory permissions prevent scan
        """
        pass

    def scan_commands(
        self,
        scope: ScopeType = ScopeType.ALL
    ) -> List[CommandCatalogEntryUnified]:
        """
        Scan for installed commands.

        Pattern: .claude/commands/{command-name}.md
        Metadata: YAML frontmatter
        Name: Prefix with '/' if not present

        Args:
            scope: Scope to scan

        Returns:
            List of discovered command entries
        """
        pass

    def scan_agents(
        self,
        scope: ScopeType = ScopeType.ALL
    ) -> List[AgentCatalogEntryUnified]:
        """
        Scan for installed agents.

        Pattern: .claude/agents/{agent-name}.md
        Metadata: YAML frontmatter (must include 'model')

        Args:
            scope: Scope to scan

        Returns:
            List of discovered agent entries
        """
        pass

    def scan_all(
        self,
        scope: ScopeType = ScopeType.ALL
    ) -> Dict[str, List[UnifiedCatalogEntry]]:
        """
        Scan all element types.

        Args:
            scope: Scope to scan

        Returns:
            Dict with keys: 'skills', 'commands', 'agents'
        """
        pass
```

### 4.3 Searcher API

```python
class Searcher:
    """
    Search and filter catalog entries.

    Stateless operations on in-memory entry lists.
    """

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

        Args:
            entries: Entries to search
            query: Search query
            element_type: Filter by type
            scope: Filter by scope
            tags: Filter by tags (all must match)

        Returns:
            Ranked list of matching entries
        """
        pass

    def filter_by_scope(
        self,
        entries: List[UnifiedCatalogEntry],
        scope: ScopeType
    ) -> List[UnifiedCatalogEntry]:
        """Filter entries by scope"""
        pass

    def filter_by_tags(
        self,
        entries: List[UnifiedCatalogEntry],
        tags: List[str],
        match_all: bool = True
    ) -> List[UnifiedCatalogEntry]:
        """
        Filter entries by tags.

        Args:
            entries: Entries to filter
            tags: Tags to match
            match_all: Require all tags (AND) vs any tag (OR)
        """
        pass

    def filter_by_type(
        self,
        entries: List[UnifiedCatalogEntry],
        element_type: ElementType
    ) -> List[UnifiedCatalogEntry]:
        """Filter entries by element type"""
        pass
```

### 4.4 Syncer API

```python
class Syncer:
    """
    Load and save catalog manifests atomically.

    Implements backup + temp file + rename pattern.
    """

    def __init__(self, scope_manager: ScopeManager):
        """
        Initialize Syncer with scope resolution.

        Args:
            scope_manager: ScopeManager for manifest path resolution
        """
        self.scope_manager = scope_manager

    def load_catalog(
        self,
        catalog_type: ElementType,
        scope: ScopeType = ScopeType.PROJECT
    ) -> Union[SkillCatalogUnified, CommandCatalogUnified, AgentCatalogUnified]:
        """
        Load catalog from JSON file.

        Args:
            catalog_type: Type of catalog
            scope: Scope level

        Returns:
            Loaded catalog model

        Raises:
            CatalogLoadError: If file is corrupted or invalid
        """
        pass

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

        Args:
            catalog: Catalog model to save
            catalog_type: Type of catalog
            scope: Scope level
            create_backup: Create .backup file before write

        Raises:
            CatalogSaveError: If atomic write fails
        """
        pass

    def merge_entries(
        self,
        existing: List[UnifiedCatalogEntry],
        discovered: List[UnifiedCatalogEntry]
    ) -> List[UnifiedCatalogEntry]:
        """
        Merge existing and discovered entries.

        Strategy:
        - Match by ID (UUID)
        - Entry in both: Update updated_at, merge metadata
        - Entry only discovered: Add as new
        - Entry only existing: Keep (don't delete)

        Args:
            existing: Entries from catalog file
            discovered: Entries from filesystem scan

        Returns:
            Merged list of entries
        """
        pass

    def backup_catalog(
        self,
        catalog_type: ElementType,
        scope: ScopeType = ScopeType.PROJECT
    ) -> Path:
        """
        Create backup of catalog file.

        Args:
            catalog_type: Type of catalog
            scope: Scope level

        Returns:
            Path to backup file

        Raises:
            BackupError: If backup creation fails
        """
        pass
```

---

## 5. Error Handling Strategy

### 5.1 Exception Hierarchy

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
    """Raised when schema validation fails"""
    pass

class BackupError(CatalogManifestError):
    """Raised when backup creation fails"""
    pass
```

### 5.2 Error Recovery Strategies

**CatalogLoadError Recovery**:
1. Check for backup file (.backup)
2. Attempt to load backup
3. If backup fails, create empty catalog
4. Log error for user review

**ScanError Recovery**:
1. Skip unreadable files (warn)
2. Skip corrupted YAML (warn)
3. Continue scan for remaining files
4. Report all warnings in summary

**SyncError Recovery**:
1. Rollback to backup if available
2. Preserve original catalog file
3. Report detailed error message
4. Suggest manual resolution steps

---

## 6. Performance Considerations

### 6.1 Performance Targets

| Operation | Target | Strategy |
|-----------|--------|----------|
| List 100 elements | < 500ms | In-memory operations |
| Search 100 elements | < 200ms | Simple scoring algorithm |
| Sync all catalogs | < 1000ms | Parallel scans |
| Load catalog | < 100ms | Lazy validation |
| Save catalog | < 200ms | Atomic write |

### 6.2 Optimization Strategies

**Lazy Loading**:
- Don't load catalogs at initialization
- Load on first access
- Cache in memory until invalidated

**Parallel Scanning**:
- Use ThreadPoolExecutor for scanning multiple scopes
- Process skills, commands, agents in parallel
- Aggregate results after completion

**Efficient Search**:
- Tokenize query once
- Early exit on exact matches
- Limit results to top N

**Caching Strategy**:
```python
# Cache catalog in memory with TTL
_catalog_cache: Dict[str, Tuple[datetime, Catalog]] = {}
CACHE_TTL = 60  # seconds

def get_cached_catalog(catalog_type: ElementType) -> Optional[Catalog]:
    if catalog_type in _catalog_cache:
        cached_at, catalog = _catalog_cache[catalog_type]
        if (datetime.utcnow() - cached_at).seconds < CACHE_TTL:
            return catalog
    return None
```

---

## 7. Testing Strategy

### 7.1 Unit Tests

**Scanner Tests** (`test_scanner.py`):
- Test skill scanning with valid frontmatter
- Test command scanning with slash prefix normalization
- Test agent scanning with model validation
- Test handling of malformed YAML
- Test handling of missing files
- Test scope filtering (global/project/local)

**Searcher Tests** (`test_searcher.py`):
- Test exact name match
- Test partial name match
- Test description search
- Test tag filtering
- Test scope filtering
- Test ranking algorithm

**Syncer Tests** (`test_syncer.py`):
- Test atomic write pattern
- Test backup creation
- Test backup restoration
- Test merge strategy (existing + discovered)
- Test schema validation
- Test concurrent write handling

**CatalogManager Tests** (`test_catalog_manager.py`):
- Test list operation with auto-sync
- Test search with multiple filters
- Test get element by name
- Test sync catalogs (force and incremental)

### 7.2 Integration Tests

**End-to-End Workflow Tests**:
1. Create test elements on filesystem
2. Run sync operation
3. Verify catalog files created
4. Test search on synced catalogs
5. Modify filesystem
6. Re-sync and verify updates

**CLI Integration Tests**:
1. Test `llm list skills` command
2. Test `llm search "query"` command
3. Test `llm show skill name` command
4. Test output formats (table/JSON/condensed)

### 7.3 Performance Tests

**Benchmark Tests**:
- List 100+ elements (target: < 500ms)
- Search 100+ elements (target: < 200ms)
- Sync all catalogs (target: < 1000ms)

### 7.4 Test Coverage Target

- **Minimum**: 80% overall coverage
- **Scanner**: 90% (critical path)
- **Syncer**: 95% (data integrity critical)
- **Searcher**: 85%
- **CatalogManager**: 85%

---

## 8. Security Controls

### 8.1 Path Validation

```python
def validate_path(path: Path, base: Path) -> Path:
    """
    Validate path is within allowed directory.

    Prevents path traversal attacks via ../../ sequences.
    """
    resolved = path.resolve()
    if not str(resolved).startswith(str(base.resolve())):
        raise ValueError(f"Path outside allowed directory: {resolved}")
    return resolved
```

### 8.2 Input Sanitization

```python
def sanitize_search_query(query: str) -> str:
    """
    Sanitize search query to prevent injection.

    - Remove control characters
    - Limit length to 200 chars
    - Strip dangerous patterns
    """
    # Remove control characters
    query = ''.join(c for c in query if c.isprintable())

    # Limit length
    query = query[:200]

    # Strip dangerous patterns (regex injection)
    dangerous = ['\\', '^', '$', '(', ')', '[', ']', '{', '}']
    for char in dangerous:
        query = query.replace(char, '')

    return query.strip()
```

### 8.3 Schema Validation

All catalog entries validated with Pydantic:
- Type validation (strings, ints, UUIDs, datetimes)
- Range validation (min_length, max_length, ge, le)
- Enum validation (ScopeType, ElementType, model names)
- Custom validators (path existence, name format)

### 8.4 File Permissions

```python
def check_write_permissions(path: Path) -> None:
    """Check write permissions before attempting save"""
    if path.exists() and not os.access(path, os.W_OK):
        raise PermissionError(f"No write permission: {path}")

    # Check parent directory if file doesn't exist
    parent = path.parent
    if not parent.exists():
        raise FileNotFoundError(f"Parent directory does not exist: {parent}")
    if not os.access(parent, os.W_OK):
        raise PermissionError(f"No write permission in directory: {parent}")
```

---

## 9. Design Decisions & Rationale

### Decision 1: Composition Over Inheritance
**Rationale**: Existing catalog models (SkillCatalog, CommandCatalog, AgentCatalog) have different structures. Rather than refactor them (breaking change), we create unified wrapper models that extend them.

**Trade-off**: Slight duplication of fields vs. backward compatibility

**Risk**: Low - Pydantic handles serialization cleanly

---

### Decision 2: Atomic Write Pattern
**Rationale**: Prevent catalog corruption from crashes or interruptions

**Approach**: Backup → temp file → validate → rename (atomic on POSIX)

**Proven**: Already used by skill_builder and agent_builder

**Risk**: None - industry standard pattern

---

### Decision 3: Auto-Sync on List
**Rationale**: Catalogs should always be fresh when user requests listing

**Approach**: Run sync before list operation (with caching to minimize overhead)

**Trade-off**: Slight delay vs. stale catalogs

**Mitigation**: Cache for 60 seconds to avoid repeated scans

---

### Decision 4: Filesystem as Source of Truth
**Rationale**: Catalog files are derived data; filesystem is authoritative

**Merge Strategy**: Discovered entries override existing entries on conflict

**Implication**: Manual edits to catalog JSON will be overwritten

**Mitigation**: Document clearly, provide sync flag to disable overwrite

---

### Decision 5: Stateless Searcher
**Rationale**: Search operates on in-memory lists, no persistent state

**Benefits**: Simple, fast, no cache invalidation complexity

**Trade-off**: No full-text indexing for large catalogs (future enhancement)

---

## 10. Future Expansion Points

### Phase 2: Additional Catalog Types
- Hooks catalog (Issue #13)
- Plugins catalog (Issue #14)
- Prompts catalog (Issue #15)
- MCPs catalog (Issue #16)

**Extension Point**: Add new `HookCatalogEntryUnified`, `PluginCatalogEntryUnified`, etc.

---

### Phase 3: Advanced Search
- Full-text indexing (Whoosh or Elasticsearch)
- Semantic search (embedding-based)
- Fuzzy matching with Levenshtein distance
- Search suggestions / autocomplete

---

### Phase 4: Catalog Sync
- Cloud-based catalog repository
- Sync across machines
- Catalog versioning/history
- Conflict resolution for distributed edits

---

## 11. Architecture Review Checklist

- [x] All components have single clear responsibility
- [x] API contracts are complete with types and docstrings
- [x] Data models use Pydantic validation
- [x] Error handling strategy defined
- [x] Security controls specified (path validation, input sanitization)
- [x] Performance targets defined (< 500ms search, < 1000ms sync)
- [x] Testing strategy covers 80%+ of code
- [x] Design decisions documented with rationale
- [x] Future expansion points identified
- [x] Integration with existing systems (ScopeManager) defined

---

**Architecture Status**: ✅ COMPLETE

**Next Step**: Documentation Researcher & Dependency Manager outputs
