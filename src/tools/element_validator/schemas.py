"""YAML schema definitions for Claude Code elements."""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


class ElementType(Enum):
    """Types of Claude Code elements."""

    AGENT = "agent"
    SKILL = "skill"
    COMMAND = "command"


@dataclass
class FieldSchema:
    """Schema for a single YAML field."""

    name: str
    required: bool
    field_type: type
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    description: str = ""
    validator: Optional[callable] = None


class AgentSchema:
    """YAML schema for agents/sub-agents."""

    REQUIRED_FIELDS = [
        FieldSchema(
            name="name",
            required=True,
            field_type=str,
            pattern=r"^[a-z0-9-]+$",
            description="Unique identifier using lowercase letters and hyphens",
        ),
        FieldSchema(
            name="description",
            required=True,
            field_type=str,
            max_length=1024,
            description="Natural language description of the agent's purpose",
        ),
    ]

    OPTIONAL_FIELDS = [
        FieldSchema(
            name="tools",
            required=False,
            field_type=str,
            description="Comma-separated list of specific tools (inherits all if omitted)",
        ),
        FieldSchema(
            name="model",
            required=False,
            field_type=str,
            pattern=r"^(sonnet|opus|haiku|inherit)$",
            description="Model alias: sonnet, opus, haiku, or inherit",
        ),
        FieldSchema(
            name="color",
            required=False,
            field_type=str,
            pattern=r"^(cyan|green|purple|red|yellow)$",
            description="Color to distinguish agent (undocumented but valid)",
        ),
    ]

    @classmethod
    def get_all_fields(cls) -> Dict[str, FieldSchema]:
        """Get all fields as a dictionary."""
        fields = {}
        for field in cls.REQUIRED_FIELDS + cls.OPTIONAL_FIELDS:
            fields[field.name] = field
        return fields

    @classmethod
    def get_required_field_names(cls) -> List[str]:
        """Get names of required fields."""
        return [field.name for field in cls.REQUIRED_FIELDS]


class SkillSchema:
    """YAML schema for skills."""

    REQUIRED_FIELDS = [
        FieldSchema(
            name="name",
            required=True,
            field_type=str,
            pattern=r"^[a-z0-9-]+$",
            max_length=64,
            description="Lowercase letters, numbers, and hyphens only (max 64 chars)",
        ),
        FieldSchema(
            name="description",
            required=True,
            field_type=str,
            max_length=1024,
            description="Brief description of what the Skill does and when to use it",
        ),
    ]

    OPTIONAL_FIELDS = [
        FieldSchema(
            name="allowed-tools",
            required=False,
            field_type=str,
            description="Comma-separated list of allowed tools (e.g., Read, Grep, Glob)",
        ),
    ]

    @classmethod
    def get_all_fields(cls) -> Dict[str, FieldSchema]:
        """Get all fields as a dictionary."""
        fields = {}
        for field in cls.REQUIRED_FIELDS + cls.OPTIONAL_FIELDS:
            fields[field.name] = field
        return fields

    @classmethod
    def get_required_field_names(cls) -> List[str]:
        """Get names of required fields."""
        return [field.name for field in cls.REQUIRED_FIELDS]


class CommandSchema:
    """YAML schema for custom commands."""

    REQUIRED_FIELDS = []  # No strictly required fields for commands

    OPTIONAL_FIELDS = [
        FieldSchema(
            name="description",
            required=False,
            field_type=str,
            max_length=512,
            description="Brief description used in /help output",
        ),
        FieldSchema(
            name="allowed-tools",
            required=False,
            field_type=str,
            description="Comma-separated list of tools the command can use",
        ),
        FieldSchema(
            name="argument-hint",
            required=False,
            field_type=str,
            max_length=128,
            description="The arguments expected for the slash command",
        ),
        FieldSchema(
            name="model",
            required=False,
            field_type=str,
            pattern=r"^(sonnet|opus|haiku)$",
            description="Specific Claude model to use for this command",
        ),
        FieldSchema(
            name="disable-model-invocation",
            required=False,
            field_type=bool,
            description="Prevents the SlashCommand tool from invoking it",
        ),
    ]

    @classmethod
    def get_all_fields(cls) -> Dict[str, FieldSchema]:
        """Get all fields as a dictionary."""
        fields = {}
        for field in cls.REQUIRED_FIELDS + cls.OPTIONAL_FIELDS:
            fields[field.name] = field
        return fields

    @classmethod
    def get_required_field_names(cls) -> List[str]:
        """Get names of required fields."""
        return []  # No required fields


# Mapping of element types to their schemas
SCHEMA_MAP = {
    ElementType.AGENT: AgentSchema,
    ElementType.SKILL: SkillSchema,
    ElementType.COMMAND: CommandSchema,
}
