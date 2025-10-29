"""
Agent Builder - Core building logic.

Handles agent file generation, including frontmatter creation, markdown content,
and file management with proper permissions and validation.

This module provides the AgentBuilder class which creates agent markdown files
in the specified directory. Unlike skills (which are directories), agents are
single .md files with frontmatter and content.

Security Focus:
- Path traversal prevention
- Secure file permissions (644 for files)
- Input validation through AgentConfig and AgentValidator
- Content sanitization

Performance Target:
- < 30ms agent creation time
"""

import os
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from src.tools.agent_builder.exceptions import (
    AgentBuilderError,
    AgentExistsError,
    AgentValidationError,
    AgentSecurityError,
)
from src.tools.agent_builder.models import (
    AgentCatalog,
    AgentCatalogEntry,
    AgentConfig,
    ScopeType,
)
from src.tools.agent_builder.validator import AgentValidator


class AgentBuilder:
    """
    Builds Claude Code agent markdown files from configuration.

    The AgentBuilder creates agent .md files (not directories) with frontmatter
    and content. Each agent is a single markdown file.

    Attributes:
        base_dir: Base directory for agent files
        catalog: In-memory catalog of agents
    """

    # File permissions constant
    FILE_PERMISSIONS = 0o644  # rw-r--r--

    def __init__(self, base_dir: Path):
        """
        Initialize agent builder.

        Args:
            base_dir: Base directory for agent files (creates if not exists)

        Examples:
            >>> builder = AgentBuilder(base_dir=Path("/path/to/agents"))
            >>> builder = AgentBuilder(base_dir=Path.home() / ".claude" / "agents")
        """
        self.base_dir = Path(base_dir)
        self.catalog = AgentCatalog()

        # Create base directory if it doesn't exist
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True, exist_ok=True)
            os.chmod(self.base_dir, 0o755)

    def create_agent(self, config: AgentConfig) -> AgentCatalogEntry:
        """
        Create an agent file from configuration.

        Args:
            config: Agent configuration (validated AgentConfig instance)

        Returns:
            AgentCatalogEntry for the created agent

        Raises:
            AgentExistsError: If agent already exists
            AgentValidationError: If configuration is invalid
            AgentSecurityError: If security validation fails

        Examples:
            >>> config = AgentConfig(
            ...     name="plan-agent",
            ...     description="Strategic planning. Use when defining architecture.",
            ...     scope=ScopeType.PROJECT,
            ...     model=ModelType.SONNET,
            ...     template="basic"
            ... )
            >>> builder = AgentBuilder(base_dir=Path("/path/to/agents"))
            >>> entry = builder.create_agent(config)
        """
        # Validate agent name
        is_valid, error = AgentValidator.validate_agent_name(config.name)
        if not is_valid:
            raise AgentValidationError(error)

        # Build agent file path
        agent_file = self.base_dir / f"{config.name}.md"

        # Security: Validate path is within base directory
        is_valid, error = AgentValidator.validate_path_security(agent_file, self.base_dir)
        if not is_valid:
            raise AgentSecurityError(error)

        # Check if agent already exists
        existing = self.catalog.get_by_name(config.name, config.scope)
        if existing:
            raise AgentExistsError(
                f"Agent '{config.name}' already exists in {config.scope.value} scope"
            )

        # Check if file exists on disk
        if agent_file.exists():
            raise AgentExistsError(
                f"Agent file '{agent_file}' already exists. "
                "Delete it first or use a different name."
            )

        # Generate content
        content = self._generate_agent_content(config)

        # Write file
        agent_file.write_text(content, encoding="utf-8")
        os.chmod(agent_file, self.FILE_PERMISSIONS)

        # Create catalog entry
        entry = AgentCatalogEntry(
            id=uuid4(),
            name=config.name,
            description=config.description,
            scope=config.scope,
            model=config.model,
            path=agent_file.resolve(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={
                "template": config.template,
                **config.frontmatter,
            },
        )

        # Add to catalog
        self.catalog.add_agent(entry)

        return entry

    def _generate_agent_content(self, config: AgentConfig) -> str:
        """
        Generate agent markdown content with frontmatter.

        Args:
            config: Agent configuration

        Returns:
            Complete markdown content with frontmatter
        """
        # Build frontmatter
        frontmatter = {
            "name": config.name,
            "description": config.description,
            "model": config.model.value,
        }

        # Add custom frontmatter fields
        if config.frontmatter:
            # Validate frontmatter keys
            is_valid, error = AgentValidator.validate_frontmatter_keys(config.frontmatter)
            if not is_valid:
                raise AgentValidationError(error)

            frontmatter.update(config.frontmatter)

        # Generate YAML frontmatter
        yaml_frontmatter = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)

        # Build content
        if config.content:
            # Use custom content (sanitized)
            content_body = AgentValidator.sanitize_string(config.content)
        else:
            # Generate default content from template
            content_body = self._generate_default_content(config)

        # Combine frontmatter and content
        return f"---\n{yaml_frontmatter}---\n\n{content_body}"

    def _generate_default_content(self, config: AgentConfig) -> str:
        """
        Generate default agent content based on template.

        Args:
            config: Agent configuration

        Returns:
            Default markdown content
        """
        # For now, use basic template
        # In Phase 2, this will use TemplateManager
        content = f"""# {config.name.replace('-', ' ').title()}

{config.description}

## When to Use

Use this agent when you need specialized assistance for this task.

## Approach

1. Analyze the requirements
2. Plan the solution
3. Execute with precision
4. Verify results
"""
        return content

    def delete_agent(self, agent_id: UUID) -> bool:
        """
        Delete an agent by ID.

        Args:
            agent_id: UUID of agent to delete

        Returns:
            True if deleted, False if not found
        """
        # Find agent in catalog
        agent = self.catalog.get_by_id(agent_id)
        if not agent:
            return False

        # Delete file if it exists
        if agent.path.exists():
            agent.path.unlink()

        # Remove from catalog
        return self.catalog.remove_agent(agent_id)

    def get_agent(
        self, name: Optional[str] = None, agent_id: Optional[UUID] = None
    ) -> Optional[AgentCatalogEntry]:
        """
        Get an agent by name or ID.

        Args:
            name: Agent name
            agent_id: Agent UUID

        Returns:
            AgentCatalogEntry if found, None otherwise
        """
        if agent_id:
            return self.catalog.get_by_id(agent_id)
        elif name:
            return self.catalog.get_by_name(name)
        return None

    def list_agents(self, scope: Optional[ScopeType] = None) -> List[AgentCatalogEntry]:
        """
        List all agents, optionally filtered by scope.

        Args:
            scope: Optional scope filter

        Returns:
            List of AgentCatalogEntry objects
        """
        if scope:
            return self.catalog.filter_by_scope(scope)
        return self.catalog.agents
