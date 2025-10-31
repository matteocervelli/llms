"""
Pydantic data models for the catalog system.

This module defines the data models for catalog entries:
- CatalogEntry: Base model for all catalog entries
- SkillCatalogEntry: Model for skill catalog entries
- CommandCatalogEntry: Model for command catalog entries
- AgentCatalogEntry: Model for agent catalog entries
"""

from datetime import datetime
from pathlib import Path
from typing import List, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CatalogEntry(BaseModel):
    """
    Base model for catalog entries.

    Attributes:
        id: Unique identifier (UUID)
        name: Name of the element (1-100 characters)
        scope: Scope of the element (global/project/local)
        description: Description of the element (max 500 characters)
        created_at: Timestamp when entry was created
        updated_at: Timestamp when entry was last updated
        file_path: Path to the element file
    """

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=100)
    scope: Literal["global", "project", "local"]
    description: str = Field(default="", max_length=500)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    file_path: Path


class SkillCatalogEntry(CatalogEntry):
    """
    Model for skill catalog entries.

    Extends CatalogEntry with skill-specific fields.

    Attributes:
        template: Skill template type (basic, tool-enhanced, custom)
        has_scripts: Whether skill has associated scripts
        file_count: Number of files in the skill
        allowed_tools: List of tools the skill is allowed to use
    """

    template: str
    has_scripts: bool = False
    file_count: int = 1
    allowed_tools: List[str] = Field(default_factory=list)


class CommandCatalogEntry(CatalogEntry):
    """
    Model for command catalog entries.

    Extends CatalogEntry with command-specific fields.

    Attributes:
        aliases: List of command aliases
        requires_tools: List of tools required by the command
        tags: List of tags for categorization
    """

    aliases: List[str] = Field(default_factory=list)
    requires_tools: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class AgentCatalogEntry(CatalogEntry):
    """
    Model for agent catalog entries.

    Extends CatalogEntry with agent-specific fields.

    Attributes:
        model: Model name (haiku, sonnet, opus)
        specialization: Agent specialization description
        requires_skills: List of skills required by the agent
    """

    model: str
    specialization: str = ""
    requires_skills: List[str] = Field(default_factory=list)
