"""
LLM Adapter Architecture

Provides adapter pattern implementation for managing multiple LLM providers (Claude,
Codex, OpenCode, etc.) with uniform interfaces for creating skills, commands, and agents.

This module implements the Adapter design pattern to abstract differences between LLM
providers while maintaining a consistent API for element creation and management.

Classes:
    - LLMAdapter: Abstract base class defining the adapter interface
    - ClaudeAdapter: Concrete implementation for Claude Code

Architecture:
    The adapter pattern allows the system to support multiple LLMs with different
    file formats, directory structures, and configuration requirements while presenting
    a unified interface to client code.

Example Usage:
    >>> from pathlib import Path
    >>> from src.core.llm_adapter import ClaudeAdapter
    >>> from src.core.scope_manager import ScopeManager, ScopeType
    >>>
    >>> # Initialize adapter with scope
    >>> scope_manager = ScopeManager()
    >>> scope_config = scope_manager.get_effective_scope('--global')
    >>> adapter = ClaudeAdapter(scope_config)
    >>>
    >>> # Create a skill
    >>> result = adapter.create_skill(
    ...     name="my-skill",
    ...     description="A helpful skill",
    ...     content="Skill implementation here"
    ... )
    >>> print(f"Created: {result.path}")
"""

import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .adapter_exceptions import CreationError, InvalidNameError, UnsupportedScopeError
from .adapter_models import AdapterMetadata, CreationResult, ElementType
from .scope_manager import ScopeConfig


class LLMAdapter(ABC):
    """Abstract base class for LLM adapters.

    This class defines the interface that all LLM adapters must implement.
    Concrete adapters (ClaudeAdapter, CodexAdapter, etc.) must implement
    all abstract methods and can override common methods as needed.

    Attributes:
        scope_config: Configuration for the target scope
        metadata: Adapter metadata (name, version, capabilities)

    Example:
        >>> # Cannot instantiate abstract class directly
        >>> try:
        ...     adapter = LLMAdapter(scope_config)
        ... except TypeError as e:
        ...     print("Cannot instantiate abstract class")
    """

    # Class-level validation patterns
    NAME_PATTERN = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?$")
    MAX_NAME_LENGTH = 64
    MAX_DESCRIPTION_LENGTH = 500

    def __init__(self, scope_config: ScopeConfig) -> None:
        """Initialize the LLM adapter.

        Args:
            scope_config: Scope configuration for this adapter

        Raises:
            UnsupportedScopeError: If the scope is not supported by this adapter
        """
        self.scope_config = scope_config
        self.metadata = self._get_metadata()

        # Validate scope is supported
        if not self.metadata.supports_scope(scope_config.type.value):
            raise UnsupportedScopeError(
                f"{self.metadata.name} adapter does not support " f"{scope_config.type.value} scope"
            )

    @abstractmethod
    def _get_metadata(self) -> AdapterMetadata:
        """Get adapter metadata.

        Returns:
            AdapterMetadata: Metadata describing this adapter's capabilities
        """
        pass

    @abstractmethod
    def create_skill(
        self, name: str, description: str, content: str, overwrite: bool = False, **kwargs: Dict
    ) -> CreationResult:
        """Create a new skill.

        Args:
            name: Skill name (alphanumeric, hyphens, underscores)
            description: Brief description of the skill
            content: Skill implementation content
            overwrite: Whether to overwrite existing files
            **kwargs: Additional LLM-specific parameters

        Returns:
            CreationResult: Result of the creation operation

        Raises:
            InvalidNameError: If the skill name is invalid
            CreationError: If file creation fails
        """
        pass

    @abstractmethod
    def create_command(
        self, name: str, description: str, content: str, overwrite: bool = False, **kwargs: Dict
    ) -> CreationResult:
        """Create a new slash command.

        Args:
            name: Command name (alphanumeric, hyphens, underscores)
            description: Brief description of the command
            content: Command implementation content
            overwrite: Whether to overwrite existing files
            **kwargs: Additional LLM-specific parameters

        Returns:
            CreationResult: Result of the creation operation

        Raises:
            InvalidNameError: If the command name is invalid
            CreationError: If file creation fails
        """
        pass

    @abstractmethod
    def create_agent(
        self, name: str, description: str, content: str, overwrite: bool = False, **kwargs: Dict
    ) -> CreationResult:
        """Create a new sub-agent.

        Args:
            name: Agent name (alphanumeric, hyphens, underscores)
            description: Brief description of the agent
            content: Agent implementation content
            overwrite: Whether to overwrite existing files
            **kwargs: Additional LLM-specific parameters

        Returns:
            CreationResult: Result of the creation operation

        Raises:
            InvalidNameError: If the agent name is invalid
            CreationError: If file creation fails
        """
        pass

    def validate_name(self, name: str, element_type: ElementType) -> None:
        """Validate an element name.

        Valid names must:
        - Contain only alphanumeric characters, hyphens, and underscores
        - Start and end with alphanumeric characters
        - Be between 1 and 64 characters long

        Args:
            name: Name to validate
            element_type: Type of element being validated

        Raises:
            InvalidNameError: If the name is invalid

        Example:
            >>> adapter.validate_name("my-skill", ElementType.SKILL)  # OK
            >>> adapter.validate_name("my skill!", ElementType.SKILL)  # Raises InvalidNameError
        """
        if not name:
            raise InvalidNameError(f"{element_type.value} name cannot be empty")

        if len(name) > self.MAX_NAME_LENGTH:
            raise InvalidNameError(
                f"{element_type.value} name too long (max {self.MAX_NAME_LENGTH} chars): '{name}'"
            )

        if not self.NAME_PATTERN.match(name):
            raise InvalidNameError(
                f"Invalid {element_type.value} name: '{name}'. "
                f"Must contain only alphanumeric characters, hyphens, and underscores, "
                f"and start/end with alphanumeric characters."
            )

    def sanitize_input(self, text: str, max_length: Optional[int] = None) -> str:
        """Sanitize user input text.

        Removes potentially dangerous characters and enforces length limits.

        Args:
            text: Text to sanitize
            max_length: Optional maximum length (defaults to MAX_DESCRIPTION_LENGTH)

        Returns:
            str: Sanitized text

        Example:
            >>> adapter.sanitize_input("Hello\\x00World")
            'HelloWorld'
        """
        if max_length is None:
            max_length = self.MAX_DESCRIPTION_LENGTH

        # Remove null bytes and other control characters
        sanitized = "".join(char for char in text if ord(char) >= 32 or char == "\n")

        # Enforce length limit
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized.strip()

    def _ensure_directory_exists(self, directory: Path) -> None:
        """Ensure a directory exists, creating it if necessary.

        Args:
            directory: Directory path to check/create

        Raises:
            CreationError: If directory creation fails

        Example:
            >>> adapter._ensure_directory_exists(Path("/home/user/.claude/skills"))
        """
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            raise CreationError(f"Failed to create directory {directory}: {e}")


class ClaudeAdapter(LLMAdapter):
    """Concrete adapter implementation for Claude Code.

    This adapter handles Claude Code's specific file formats (Markdown),
    directory structure, and configuration requirements.

    Claude Code Structure:
        - Skills: {scope_path}/skills/{name}.md
        - Commands: {scope_path}/commands/{name}.md
        - Agents: {scope_path}/agents/{name}.md

    Example:
        >>> from src.core.scope_manager import ScopeManager
        >>> manager = ScopeManager()
        >>> scope = manager.get_effective_scope('--global')
        >>> adapter = ClaudeAdapter(scope)
        >>> result = adapter.create_skill(
        ...     name="test-skill",
        ...     description="A test skill",
        ...     content="# Test Skill\\n\\nImplementation here"
        ... )
        >>> print(f"Created at: {result.path}")
    """

    def _get_metadata(self) -> AdapterMetadata:
        """Get Claude adapter metadata.

        Returns:
            AdapterMetadata: Metadata for the Claude adapter
        """
        return AdapterMetadata(
            name="claude",
            version="1.0.0",
            supported_scopes=["global", "project", "local"],
            supported_elements=[
                ElementType.SKILL,
                ElementType.COMMAND,
                ElementType.AGENT,
            ],
            requires_config=False,
        )

    def create_skill(
        self,
        name: str,
        description: str,
        content: str,
        overwrite: bool = False,
        **kwargs: Dict,
    ) -> CreationResult:
        """Create a Claude Code skill.

        Creates a Markdown file in the skills/ directory with the provided
        content and metadata.

        Args:
            name: Skill name (e.g., "my-skill")
            description: Brief description of the skill
            content: Skill implementation content (Markdown)
            overwrite: Whether to overwrite existing file
            **kwargs: Additional parameters (ignored for Claude)

        Returns:
            CreationResult: Result with path and status

        Raises:
            InvalidNameError: If the skill name is invalid
            CreationError: If file creation fails

        Example:
            >>> adapter = ClaudeAdapter(scope_config)
            >>> result = adapter.create_skill(
            ...     name="example",
            ...     description="An example skill",
            ...     content="# Example\\n\\nImplementation"
            ... )
        """
        # Validate inputs
        self.validate_name(name, ElementType.SKILL)
        description = self.sanitize_input(description)
        content = self.sanitize_input(content, max_length=50000)

        # Determine file path
        skills_dir = self.scope_config.path / "skills"
        file_path = skills_dir / f"{name}.md"

        # Check for existing file
        if file_path.exists() and not overwrite:
            raise CreationError(
                f"Skill '{name}' already exists at {file_path}. Use overwrite=True to replace."
            )

        # Create directory if needed
        self._ensure_directory_exists(skills_dir)

        # Generate file content
        file_content = self._generate_skill_content(name, description, content)

        # Write file
        try:
            file_path.write_text(file_content, encoding="utf-8")
        except (PermissionError, OSError) as e:
            raise CreationError(f"Failed to write skill file {file_path}: {e}")

        return CreationResult(
            path=file_path,
            element_type=ElementType.SKILL,
            success=True,
            message=f"Skill '{name}' created successfully",
            metadata={
                "scope": self.scope_config.type.value,
                "created_at": datetime.now().isoformat(),
                "description": description,
            },
        )

    def create_command(
        self,
        name: str,
        description: str,
        content: str,
        overwrite: bool = False,
        **kwargs: Dict,
    ) -> CreationResult:
        """Create a Claude Code slash command.

        Creates a Markdown file in the commands/ directory with the provided
        content and metadata.

        Args:
            name: Command name (e.g., "my-command")
            description: Brief description of the command
            content: Command implementation content (Markdown)
            overwrite: Whether to overwrite existing file
            **kwargs: Additional parameters (ignored for Claude)

        Returns:
            CreationResult: Result with path and status

        Raises:
            InvalidNameError: If the command name is invalid
            CreationError: If file creation fails

        Example:
            >>> adapter = ClaudeAdapter(scope_config)
            >>> result = adapter.create_command(
            ...     name="example",
            ...     description="An example command",
            ...     content="# Example Command\\n\\nImplementation"
            ... )
        """
        # Validate inputs
        self.validate_name(name, ElementType.COMMAND)
        description = self.sanitize_input(description)
        content = self.sanitize_input(content, max_length=50000)

        # Determine file path
        commands_dir = self.scope_config.path / "commands"
        file_path = commands_dir / f"{name}.md"

        # Check for existing file
        if file_path.exists() and not overwrite:
            raise CreationError(
                f"Command '{name}' already exists at {file_path}. Use overwrite=True to replace."
            )

        # Create directory if needed
        self._ensure_directory_exists(commands_dir)

        # Generate file content
        file_content = self._generate_command_content(name, description, content)

        # Write file
        try:
            file_path.write_text(file_content, encoding="utf-8")
        except (PermissionError, OSError) as e:
            raise CreationError(f"Failed to write command file {file_path}: {e}")

        return CreationResult(
            path=file_path,
            element_type=ElementType.COMMAND,
            success=True,
            message=f"Command '{name}' created successfully",
            metadata={
                "scope": self.scope_config.type.value,
                "created_at": datetime.now().isoformat(),
                "description": description,
            },
        )

    def create_agent(
        self,
        name: str,
        description: str,
        content: str,
        overwrite: bool = False,
        **kwargs: Dict,
    ) -> CreationResult:
        """Create a Claude Code sub-agent.

        Creates a Markdown file in the agents/ directory with the provided
        content and metadata.

        Args:
            name: Agent name (e.g., "my-agent")
            description: Brief description of the agent
            content: Agent implementation content (Markdown)
            overwrite: Whether to overwrite existing file
            **kwargs: Additional parameters (ignored for Claude)

        Returns:
            CreationResult: Result with path and status

        Raises:
            InvalidNameError: If the agent name is invalid
            CreationError: If file creation fails

        Example:
            >>> adapter = ClaudeAdapter(scope_config)
            >>> result = adapter.create_agent(
            ...     name="example",
            ...     description="An example agent",
            ...     content="# Example Agent\\n\\nImplementation"
            ... )
        """
        # Validate inputs
        self.validate_name(name, ElementType.AGENT)
        description = self.sanitize_input(description)
        content = self.sanitize_input(content, max_length=50000)

        # Determine file path
        agents_dir = self.scope_config.path / "agents"
        file_path = agents_dir / f"{name}.md"

        # Check for existing file
        if file_path.exists() and not overwrite:
            raise CreationError(
                f"Agent '{name}' already exists at {file_path}. Use overwrite=True to replace."
            )

        # Create directory if needed
        self._ensure_directory_exists(agents_dir)

        # Generate file content
        file_content = self._generate_agent_content(name, description, content)

        # Write file
        try:
            file_path.write_text(file_content, encoding="utf-8")
        except (PermissionError, OSError) as e:
            raise CreationError(f"Failed to write agent file {file_path}: {e}")

        return CreationResult(
            path=file_path,
            element_type=ElementType.AGENT,
            success=True,
            message=f"Agent '{name}' created successfully",
            metadata={
                "scope": self.scope_config.type.value,
                "created_at": datetime.now().isoformat(),
                "description": description,
            },
        )

    def _generate_skill_content(self, name: str, description: str, content: str) -> str:
        """Generate formatted content for a skill file.

        Args:
            name: Skill name
            description: Skill description
            content: Skill implementation

        Returns:
            str: Formatted Markdown content
        """
        return f"""# {name}

{description}

{content}
"""

    def _generate_command_content(self, name: str, description: str, content: str) -> str:
        """Generate formatted content for a command file.

        Args:
            name: Command name
            description: Command description
            content: Command implementation

        Returns:
            str: Formatted Markdown content
        """
        return f"""# /{name}

{description}

{content}
"""

    def _generate_agent_content(self, name: str, description: str, content: str) -> str:
        """Generate formatted content for an agent file.

        Args:
            name: Agent name
            description: Agent description
            content: Agent implementation

        Returns:
            str: Formatted Markdown content
        """
        return f"""# {name} Agent

{description}

{content}
"""


# Public API for easy imports
__all__ = [
    "LLMAdapter",
    "ClaudeAdapter",
]
