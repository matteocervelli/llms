"""
Pydantic models for skill_builder tool.

This module defines the core data structures for skill configuration,
catalog entries, and catalog management using Pydantic v2 for validation.
"""

import re
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class ScopeType(str, Enum):
    """Scope types for skill installation."""

    GLOBAL = "global"  # ~/.claude/skills/
    PROJECT = "project"  # <project>/.claude/skills/ (committed)
    LOCAL = "local"  # <project>/.claude/skills/ (not committed)


class SkillConfig(BaseModel):
    """
    Configuration for creating a skill.

    Attributes:
        name: Skill name (lowercase-with-hyphens, 1-64 chars)
        description: Skill description with usage context (max 1024 chars)
        scope: Installation scope (GLOBAL/PROJECT/LOCAL)
        template: Template name to use (default: "basic")
        allowed_tools: Optional list of allowed Claude tools
        content: Optional custom markdown content
        frontmatter: Additional frontmatter fields
    """

    name: str
    description: str
    scope: ScopeType
    template: str = "basic"
    allowed_tools: Optional[List[str]] = None
    content: Optional[str] = None
    frontmatter: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        Validates skill name follows pattern: ^[a-z0-9-]{1,64}$

        Security: Prevents path traversal and special characters
        """
        if not v or len(v) > 64:
            raise ValueError("Name must be 1-64 characters")

        if not v or len(v) < 1:
            raise ValueError("Name cannot be empty")

        pattern = re.compile(r"^[a-z0-9-]+$")
        if not pattern.match(v):
            raise ValueError("Name must contain only lowercase letters, numbers, and hyphens")

        if v.startswith("-") or v.endswith("-"):
            raise ValueError("Name cannot start or end with hyphen")

        if "--" in v:
            raise ValueError("Name cannot contain consecutive hyphens")

        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """
        Validates description (max 1024 chars, must include usage context).
        """
        if not v or len(v.strip()) == 0:
            raise ValueError("Description cannot be empty")

        if len(v) > 1024:
            raise ValueError("Description must be 1024 characters or less")

        # Check for usage context keywords
        usage_keywords = ["when", "use", "for", "during", "if"]
        has_usage_context = any(keyword in v.lower() for keyword in usage_keywords)

        if not has_usage_context:
            raise ValueError(
                "Description should include when to use this skill "
                "(e.g., 'Use when...', 'for processing...')"
            )

        return v

    @field_validator("template")
    @classmethod
    def validate_template(cls, v: str) -> str:
        """Validates template name (alphanumeric and hyphens only)."""
        if not v:
            raise ValueError("Template name cannot be empty")

        pattern = re.compile(r"^[a-z0-9_-]+$")
        if not pattern.match(v):
            raise ValueError(
                "Template name must contain only lowercase letters, "
                "numbers, underscores, and hyphens"
            )

        # Security: Prevent path traversal
        if ".." in v or "/" in v or "\\" in v:
            raise ValueError("Template name cannot contain path separators")

        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "pdf-processor",
                    "description": "Extract text from PDFs. Use when working with PDF files.",
                    "scope": "project",
                    "template": "basic",
                    "allowed_tools": ["Read", "Bash"],
                }
            ]
        }
    }


class SkillCatalogEntry(BaseModel):
    """
    Catalog entry for tracking a skill.

    Attributes:
        id: Unique identifier (UUID4)
        name: Skill name
        description: Skill description
        scope: Installation scope
        path: Absolute path to skill directory
        created_at: Creation timestamp
        updated_at: Last update timestamp
        metadata: Additional metadata (template, file counts, etc.)
    """

    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    scope: ScopeType
    path: Path
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("path")
    @classmethod
    def validate_path(cls, v: Path) -> Path:
        """Ensures path is absolute."""
        if not v.is_absolute():
            raise ValueError("Path must be absolute")
        return v

    model_config = {"json_encoders": {Path: str, UUID: str, datetime: lambda v: v.isoformat()}}


class SkillCatalog(BaseModel):
    """
    Container for skill catalog entries.

    Provides methods for managing the collection of skills,
    including search, retrieval, and filtering operations.

    Attributes:
        schema_version: Catalog schema version
        skills: List of skill catalog entries
    """

    schema_version: str = "1.0"
    skills: List[SkillCatalogEntry] = Field(default_factory=list)

    def get_by_id(self, skill_id: UUID) -> Optional[SkillCatalogEntry]:
        """
        Retrieves a skill by its UUID.

        Args:
            skill_id: UUID of the skill

        Returns:
            SkillCatalogEntry if found, None otherwise
        """
        for skill in self.skills:
            if skill.id == skill_id:
                return skill
        return None

    def get_by_name(
        self, name: str, scope: Optional[ScopeType] = None
    ) -> Optional[SkillCatalogEntry]:
        """
        Retrieves a skill by name and optional scope.

        Args:
            name: Skill name
            scope: Optional scope filter

        Returns:
            SkillCatalogEntry if found, None otherwise
        """
        for skill in self.skills:
            if skill.name == name:
                if scope is None or skill.scope == scope:
                    return skill
        return None

    def search(self, query: str, scope: Optional[ScopeType] = None) -> List[SkillCatalogEntry]:
        """
        Searches skills by name and description.

        Args:
            query: Search query string
            scope: Optional scope filter

        Returns:
            List of matching SkillCatalogEntry objects
        """
        query_lower = query.lower()
        results = []

        for skill in self.skills:
            if scope and skill.scope != scope:
                continue

            if query_lower in skill.name.lower() or query_lower in skill.description.lower():
                results.append(skill)

        return results

    def filter_by_scope(self, scope: ScopeType) -> List[SkillCatalogEntry]:
        """
        Filters skills by scope.

        Args:
            scope: Scope to filter by

        Returns:
            List of skills in the specified scope
        """
        return [s for s in self.skills if s.scope == scope]

    def add_skill(self, entry: SkillCatalogEntry) -> None:
        """
        Adds a skill to the catalog.

        Args:
            entry: Skill catalog entry to add

        Raises:
            ValueError: If skill with same name and scope already exists
        """
        existing = self.get_by_name(entry.name, entry.scope)
        if existing:
            raise ValueError(f"Skill '{entry.name}' already exists in {entry.scope} scope")

        self.skills.append(entry)

    def remove_skill(self, skill_id: UUID) -> bool:
        """
        Removes a skill from the catalog.

        Args:
            skill_id: UUID of skill to remove

        Returns:
            True if removed, False if not found
        """
        initial_count = len(self.skills)
        self.skills = [s for s in self.skills if s.id != skill_id]
        return len(self.skills) < initial_count

    def update_skill(self, skill_id: UUID, **updates: Any) -> bool:
        """
        Updates a skill's fields.

        Args:
            skill_id: UUID of skill to update
            **updates: Fields to update

        Returns:
            True if updated, False if not found
        """
        skill = self.get_by_id(skill_id)
        if not skill:
            return False

        for key, value in updates.items():
            if hasattr(skill, key):
                setattr(skill, key, value)

        skill.updated_at = datetime.now()
        return True
