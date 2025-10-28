"""
Data models for command builder.

Defines Pydantic models for command configuration, parameters, and catalog entries.
These models ensure type safety and data validation throughout the command builder.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ParameterType(str, Enum):
    """Parameter types for command arguments."""

    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    CHOICE = "choice"


class ScopeType(str, Enum):
    """Scope types for commands."""

    GLOBAL = "global"
    PROJECT = "project"
    LOCAL = "local"


class ValidationConfig(BaseModel):
    """
    Configuration for command validation settings.

    Attributes:
        strict_naming: Enforce strict naming convention validation
        allowed_contexts: List of allowed context prefixes for command names
        check_naming_convention: Whether to check naming convention at all
    """

    strict_naming: bool = False
    allowed_contexts: List[str] = Field(
        default_factory=lambda: [
            "cc",
            "gh",
            "project",
            "pr",
            "code",
            "feature",
            "issue",
            "ui",
            "infrastructure",
        ]
    )
    check_naming_convention: bool = True


class CommandParameter(BaseModel):
    """
    Configuration for a command parameter.

    Attributes:
        name: Parameter name (lowercase, alphanumeric + underscores)
        type: Parameter type (string, number, boolean, choice)
        description: Human-readable description
        required: Whether parameter is required
        default: Default value if not required
        choices: Valid choices (only for choice type)
    """

    name: str = Field(..., pattern=r"^[a-z][a-z0-9_]*$")
    type: ParameterType
    description: str = Field(..., min_length=1)
    required: bool = False
    default: Optional[Any] = None
    choices: Optional[List[str]] = None

    @model_validator(mode="after")
    def validate_parameter(self) -> "CommandParameter":
        """Validate parameter constraints."""
        # Validate choices for CHOICE type
        if self.type == ParameterType.CHOICE and not self.choices:
            raise ValueError("choices must be provided for choice type")
        if self.type != ParameterType.CHOICE and self.choices:
            raise ValueError(f"choices not allowed for {self.type.value} type")

        # Validate required parameters don't have defaults
        if self.required and self.default is not None:
            raise ValueError("required parameters cannot have default values")

        return self


class CommandConfig(BaseModel):
    """
    Complete configuration for a slash command.

    Attributes:
        name: Command name (slug format: lowercase, alphanumeric + hyphens)
        description: Command description (shown in command list)
        scope: Scope for command (global/project/local)
        parameters: List of command parameters
        bash_commands: List of bash commands to execute (!command syntax)
        file_references: List of file references (@file syntax)
        thinking_mode: Enable extended thinking mode
        template: Template to use for generation
        frontmatter: Additional YAML frontmatter fields
    """

    name: str = Field(..., pattern=r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
    description: str = Field(..., min_length=1, max_length=500)
    scope: ScopeType = ScopeType.PROJECT
    parameters: List[CommandParameter] = Field(default_factory=list)
    bash_commands: List[str] = Field(default_factory=list)
    file_references: List[str] = Field(default_factory=list)
    thinking_mode: bool = False
    template: str = "basic"
    frontmatter: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate command name follows slug format."""
        if len(v) < 2:
            raise ValueError("command name must be at least 2 characters")
        if len(v) > 50:
            raise ValueError("command name must be at most 50 characters")
        if "--" in v:
            raise ValueError("command name cannot contain consecutive hyphens")
        return v

    @field_validator("bash_commands")
    @classmethod
    def validate_bash_commands(cls, v: List[str]) -> List[str]:
        """Validate bash commands are non-empty."""
        return [cmd.strip() for cmd in v if cmd.strip()]

    @field_validator("file_references")
    @classmethod
    def validate_file_references(cls, v: List[str]) -> List[str]:
        """Validate file references are non-empty."""
        return [ref.strip() for ref in v if ref.strip()]

    @field_validator("template")
    @classmethod
    def validate_template(cls, v: str) -> str:
        """Validate template name is safe (no path traversal)."""
        if "/" in v or "\\" in v or ".." in v:
            raise ValueError("template name cannot contain path separators")
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("template name must be alphanumeric with hyphens/underscores")
        return v


class CommandCatalogEntry(BaseModel):
    """
    Catalog entry for tracking created commands.

    Attributes:
        id: Unique identifier (UUID)
        name: Command name
        description: Command description
        scope: Command scope
        path: Absolute path to command file
        created_at: Creation timestamp
        updated_at: Last update timestamp
        metadata: Additional metadata (template, features, etc.)
    """

    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    scope: ScopeType
    path: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now()

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: str,
        }
    )


class CommandCatalog(BaseModel):
    """
    Catalog of all commands managed by command_builder.

    Attributes:
        schema_version: Catalog schema version
        commands: List of command entries
    """

    schema_version: str = "1.0"
    commands: List[CommandCatalogEntry] = Field(default_factory=list)

    def get_by_name(
        self, name: str, scope: Optional[ScopeType] = None
    ) -> Optional[CommandCatalogEntry]:
        """
        Get command entry by name and optional scope.

        Args:
            name: Command name
            scope: Optional scope filter

        Returns:
            Matching command entry or None
        """
        for cmd in self.commands:
            if cmd.name == name:
                if scope is None or cmd.scope == scope:
                    return cmd
        return None

    def get_by_id(self, cmd_id: UUID) -> Optional[CommandCatalogEntry]:
        """
        Get command entry by ID.

        Args:
            cmd_id: Command UUID

        Returns:
            Matching command entry or None
        """
        for cmd in self.commands:
            if cmd.id == cmd_id:
                return cmd
        return None

    def add_command(self, entry: CommandCatalogEntry) -> None:
        """
        Add a command entry to the catalog.

        Args:
            entry: Command catalog entry
        """
        self.commands.append(entry)

    def remove_command(self, cmd_id: UUID) -> bool:
        """
        Remove a command entry from the catalog.

        Args:
            cmd_id: Command UUID

        Returns:
            True if removed, False if not found
        """
        for i, cmd in enumerate(self.commands):
            if cmd.id == cmd_id:
                self.commands.pop(i)
                return True
        return False

    def search(
        self,
        query: Optional[str] = None,
        scope: Optional[ScopeType] = None,
        has_parameters: Optional[bool] = None,
        has_bash: Optional[bool] = None,
    ) -> List[CommandCatalogEntry]:
        """
        Search commands by various criteria.

        Args:
            query: Text query (searches name and description)
            scope: Filter by scope
            has_parameters: Filter by parameter presence
            has_bash: Filter by bash command presence

        Returns:
            List of matching command entries
        """
        results = self.commands.copy()

        if query:
            query_lower = query.lower()
            results = [
                cmd
                for cmd in results
                if query_lower in cmd.name.lower() or query_lower in cmd.description.lower()
            ]

        if scope:
            results = [cmd for cmd in results if cmd.scope == scope]

        if has_parameters is not None:
            results = [
                cmd
                for cmd in results
                if cmd.metadata.get("has_parameters", False) == has_parameters
            ]

        if has_bash is not None:
            results = [cmd for cmd in results if cmd.metadata.get("has_bash", False) == has_bash]

        return results

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: str,
        }
    )
