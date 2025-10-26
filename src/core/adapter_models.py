"""
Data models and configuration objects for LLM adapters.

This module provides dataclass-based models for representing adapter configuration,
creation results, and metadata used throughout the LLM adapter system.

Models:
    - CreationResult: Result of creating a skill/command/agent
    - AdapterMetadata: Metadata describing an LLM adapter
    - ElementType: Enum for skill/command/agent types

Example Usage:
    >>> from src.core.adapter_models import CreationResult, ElementType
    >>> from pathlib import Path
    >>>
    >>> result = CreationResult(
    ...     path=Path("/home/user/.claude/skills/my-skill.md"),
    ...     element_type=ElementType.SKILL,
    ...     success=True,
    ...     message="Skill created successfully",
    ...     metadata={"scope": "global", "version": "1.0.0"}
    ... )
    >>> print(f"Created {result.element_type.value} at {result.path}")
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class ElementType(Enum):
    """Enumeration of LLM element types.

    Attributes:
        SKILL: A reusable skill that can be invoked
        COMMAND: A slash command for CLI interaction
        AGENT: A sub-agent for specialized tasks
    """

    SKILL = "skill"
    COMMAND = "command"
    AGENT = "agent"


@dataclass
class CreationResult:
    """Result of creating a skill, command, or agent.

    This dataclass encapsulates the outcome of an adapter creation operation,
    including success status, file path, messages, and additional metadata.

    Attributes:
        path: Path to the created file
        element_type: Type of element created (skill/command/agent)
        success: Whether the creation was successful
        message: Human-readable status message
        metadata: Additional metadata about the created element

    Example:
        >>> result = CreationResult(
        ...     path=Path("/home/user/.claude/commands/test.md"),
        ...     element_type=ElementType.COMMAND,
        ...     success=True,
        ...     message="Command created successfully",
        ...     metadata={"author": "user", "version": "1.0.0"}
        ... )
        >>> if result.success:
        ...     print(f"Created at: {result.path}")
    """

    path: Path
    element_type: ElementType
    success: bool
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate the CreationResult after initialization."""
        if not isinstance(self.path, Path):
            self.path = Path(self.path)


@dataclass
class AdapterMetadata:
    """Metadata describing an LLM adapter.

    This dataclass contains information about an adapter's capabilities,
    supported scopes, and configuration requirements.

    Attributes:
        name: Adapter name (e.g., "claude", "codex")
        version: Adapter version string
        supported_scopes: List of supported scope types
        supported_elements: List of supported element types
        requires_config: Whether the adapter requires additional configuration
        config_schema: Optional JSON schema for configuration validation

    Example:
        >>> metadata = AdapterMetadata(
        ...     name="claude",
        ...     version="1.0.0",
        ...     supported_scopes=["global", "project", "local"],
        ...     supported_elements=[ElementType.SKILL, ElementType.COMMAND],
        ...     requires_config=False
        ... )
        >>> print(f"{metadata.name} v{metadata.version}")
    """

    name: str
    version: str
    supported_scopes: List[str]
    supported_elements: List[ElementType]
    requires_config: bool = False
    config_schema: Optional[Dict[str, Any]] = None

    def supports_scope(self, scope: str) -> bool:
        """Check if the adapter supports a given scope.

        Args:
            scope: Scope type to check (global, project, or local)

        Returns:
            bool: True if the scope is supported, False otherwise

        Example:
            >>> metadata = AdapterMetadata(
            ...     name="test",
            ...     version="1.0.0",
            ...     supported_scopes=["global", "project"],
            ...     supported_elements=[ElementType.SKILL]
            ... )
            >>> metadata.supports_scope("global")
            True
            >>> metadata.supports_scope("local")
            False
        """
        return scope in self.supported_scopes

    def supports_element(self, element_type: ElementType) -> bool:
        """Check if the adapter supports a given element type.

        Args:
            element_type: Element type to check

        Returns:
            bool: True if the element type is supported, False otherwise

        Example:
            >>> metadata = AdapterMetadata(
            ...     name="test",
            ...     version="1.0.0",
            ...     supported_scopes=["global"],
            ...     supported_elements=[ElementType.SKILL, ElementType.COMMAND]
            ... )
            >>> metadata.supports_element(ElementType.SKILL)
            True
            >>> metadata.supports_element(ElementType.AGENT)
            False
        """
        return element_type in self.supported_elements


# Public API for easy imports
__all__ = [
    "ElementType",
    "CreationResult",
    "AdapterMetadata",
]
