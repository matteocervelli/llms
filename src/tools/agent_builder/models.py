"""
Pydantic models for agent_builder tool.

This module defines the core data structures for agent configuration,
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
    """Scope types for agent installation."""

    GLOBAL = "global"  # ~/.claude/agents/
    PROJECT = "project"  # <project>/.claude/agents/ (committed)
    LOCAL = "local"  # <project>/.claude/agents/ (not committed)


class ModelType(str, Enum):
    """Claude model types for agent configuration."""

    HAIKU = "claude-3-5-haiku-20241022"
    SONNET = "claude-3-5-sonnet-20241022"
    OPUS = "claude-opus-4-20250514"


class AgentConfig(BaseModel):
    """
    Configuration for creating an agent.

    Attributes:
        name: Agent name (lowercase-with-hyphens, 1-64 chars)
        description: Agent description with usage context (max 1024 chars)
        scope: Installation scope (GLOBAL/PROJECT/LOCAL)
        model: Claude model to use for this agent
        template: Template name to use (default: "basic")
        content: Optional custom markdown content
        frontmatter: Additional frontmatter fields
    """

    name: str
    description: str
    scope: ScopeType
    model: ModelType
    template: str = "basic"
    content: Optional[str] = None
    frontmatter: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        Validates agent name follows pattern: ^[a-z0-9-]{1,64}$

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
                "Description should include when to use this agent "
                "(e.g., 'Use when...', 'for processing...')"
            )

        return v

    @field_validator("template")
    @classmethod
    def validate_template(cls, v: str) -> str:
        """Validates template name (alphanumeric and hyphens only)."""
        if not v:
            raise ValueError("Template name cannot be empty")

        # Security: Prevent path traversal (check BEFORE pattern check)
        if ".." in v or "/" in v or "\\" in v:
            raise ValueError("Template name cannot contain path separators")

        pattern = re.compile(r"^[a-z0-9_-]+$")
        if not pattern.match(v):
            raise ValueError(
                "Template name must contain only lowercase letters, "
                "numbers, underscores, and hyphens"
            )

        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "plan-agent",
                    "description": "Strategic planning agent. Use when defining project architecture.",
                    "scope": "project",
                    "model": "claude-3-5-sonnet-20241022",
                    "template": "basic",
                }
            ]
        }
    }


class AgentCatalogEntry(BaseModel):
    """
    Catalog entry for tracking an agent.

    Attributes:
        id: Unique identifier (UUID4)
        name: Agent name
        description: Agent description
        scope: Installation scope
        model: Claude model used by this agent
        path: Absolute path to agent file
        created_at: Creation timestamp
        updated_at: Last update timestamp
        metadata: Additional metadata (template, version, etc.)
    """

    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    scope: ScopeType
    model: ModelType
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


class AgentCatalog(BaseModel):
    """
    Container for agent catalog entries.

    Provides methods for managing the collection of agents,
    including search, retrieval, and filtering operations.

    Attributes:
        schema_version: Catalog schema version
        agents: List of agent catalog entries
    """

    schema_version: str = "1.0"
    agents: List[AgentCatalogEntry] = Field(default_factory=list)

    def get_by_id(self, agent_id: UUID) -> Optional[AgentCatalogEntry]:
        """
        Retrieves an agent by its UUID.

        Args:
            agent_id: UUID of the agent

        Returns:
            AgentCatalogEntry if found, None otherwise
        """
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None

    def get_by_name(
        self, name: str, scope: Optional[ScopeType] = None
    ) -> Optional[AgentCatalogEntry]:
        """
        Retrieves an agent by name and optional scope.

        Args:
            name: Agent name
            scope: Optional scope filter

        Returns:
            AgentCatalogEntry if found, None otherwise
        """
        for agent in self.agents:
            if agent.name == name:
                if scope is None or agent.scope == scope:
                    return agent
        return None

    def search(self, query: str, scope: Optional[ScopeType] = None) -> List[AgentCatalogEntry]:
        """
        Searches agents by name and description.

        Args:
            query: Search query string
            scope: Optional scope filter

        Returns:
            List of matching AgentCatalogEntry objects
        """
        query_lower = query.lower()
        results = []

        for agent in self.agents:
            if scope and agent.scope != scope:
                continue

            if query_lower in agent.name.lower() or query_lower in agent.description.lower():
                results.append(agent)

        return results

    def filter_by_scope(self, scope: ScopeType) -> List[AgentCatalogEntry]:
        """
        Filters agents by scope.

        Args:
            scope: Scope to filter by

        Returns:
            List of agents in the specified scope
        """
        return [a for a in self.agents if a.scope == scope]

    def add_agent(self, entry: AgentCatalogEntry) -> None:
        """
        Adds an agent to the catalog.

        Args:
            entry: Agent catalog entry to add

        Raises:
            ValueError: If agent with same name and scope already exists
        """
        existing = self.get_by_name(entry.name, entry.scope)
        if existing:
            raise ValueError(f"Agent '{entry.name}' already exists in {entry.scope} scope")

        self.agents.append(entry)

    def remove_agent(self, agent_id: UUID) -> bool:
        """
        Removes an agent from the catalog.

        Args:
            agent_id: UUID of agent to remove

        Returns:
            True if removed, False if not found
        """
        initial_count = len(self.agents)
        self.agents = [a for a in self.agents if a.id != agent_id]
        return len(self.agents) < initial_count

    def update_agent(self, agent_id: UUID, **updates: Any) -> bool:
        """
        Updates an agent's fields.

        Args:
            agent_id: UUID of agent to update
            **updates: Fields to update

        Returns:
            True if updated, False if not found
        """
        agent = self.get_by_id(agent_id)
        if not agent:
            return False

        for key, value in updates.items():
            if hasattr(agent, key):
                setattr(agent, key, value)

        agent.updated_at = datetime.now()
        return True
