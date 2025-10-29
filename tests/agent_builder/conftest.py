"""Shared test fixtures for agent_builder tests."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from click.testing import CliRunner

from src.tools.agent_builder.models import (
    ScopeType,
    ModelType,
    AgentCatalog,
    AgentCatalogEntry,
    AgentConfig,
)


# ============================================================================
# Directory and Path Fixtures
# ============================================================================


@pytest.fixture
def temp_agent_dir(tmp_path):
    """Creates temporary agent directory structure."""
    agents_dir = tmp_path / ".claude" / "agents"
    agents_dir.mkdir(parents=True)
    return agents_dir


@pytest.fixture
def temp_project_root(tmp_path):
    """Creates temporary project root with .claude directory."""
    project_root = tmp_path / "project"
    project_root.mkdir()
    claude_dir = project_root / ".claude"
    claude_dir.mkdir()
    agents_dir = claude_dir / "agents"
    agents_dir.mkdir()
    return project_root


@pytest.fixture
def temp_git_repo(tmp_path):
    """Creates temporary git repository for scope testing."""
    repo_dir = tmp_path / "git-repo"
    repo_dir.mkdir()
    git_dir = repo_dir / ".git"
    git_dir.mkdir()
    claude_dir = repo_dir / ".claude"
    claude_dir.mkdir()
    return repo_dir


# ============================================================================
# Configuration Fixtures
# ============================================================================


@pytest.fixture
def sample_agent_config():
    """Sample agent configuration for testing."""
    return AgentConfig(
        name="plan-agent",
        description="Strategic planning agent. Use when defining project architecture.",
        scope=ScopeType.PROJECT,
        model=ModelType.SONNET,
        template="basic",
    )


@pytest.fixture
def sample_agent_config_with_content():
    """Sample agent configuration with custom content."""
    return AgentConfig(
        name="custom-agent",
        description="Custom agent with custom content. Use for specialized tasks.",
        scope=ScopeType.PROJECT,
        model=ModelType.HAIKU,
        template="basic",
        content="# Custom Agent\n\nThis is custom content.",
    )


@pytest.fixture
def sample_agent_config_with_frontmatter():
    """Sample agent configuration with custom frontmatter."""
    return AgentConfig(
        name="advanced-agent",
        description="Advanced agent with custom frontmatter. Use for complex workflows.",
        scope=ScopeType.GLOBAL,
        model=ModelType.OPUS,
        template="basic",
        frontmatter={"version": "1.0", "tags": ["planning", "architecture"]},
    )


# ============================================================================
# Catalog Fixtures
# ============================================================================


@pytest.fixture
def sample_catalog_entry(temp_agent_dir):
    """Sample catalog entry for testing."""
    return AgentCatalogEntry(
        id=uuid4(),
        name="test-agent",
        description="Test agent",
        scope=ScopeType.PROJECT,
        model=ModelType.SONNET,
        path=temp_agent_dir / "test-agent.md",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={"template": "basic"},
    )


@pytest.fixture
def sample_catalog_with_entries(temp_agent_dir) -> AgentCatalog:
    """Sample catalog with multiple entries for testing."""
    entries = [
        AgentCatalogEntry(
            id=uuid4(),
            name="agent-one",
            description="First test agent",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=temp_agent_dir / "agent-one.md",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"template": "basic"},
        ),
        AgentCatalogEntry(
            id=uuid4(),
            name="agent-two",
            description="Second test agent",
            scope=ScopeType.GLOBAL,
            model=ModelType.HAIKU,
            path=temp_agent_dir / "agent-two.md",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"template": "basic"},
        ),
        AgentCatalogEntry(
            id=uuid4(),
            name="agent-three",
            description="Third test agent",
            scope=ScopeType.LOCAL,
            model=ModelType.OPUS,
            path=temp_agent_dir / "agent-three.md",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"template": "basic"},
        ),
    ]
    return AgentCatalog(agents=entries)


@pytest.fixture
def large_catalog(temp_agent_dir) -> AgentCatalog:
    """Large catalog with 100+ entries for performance testing."""
    entries = []
    for i in range(120):
        entries.append(
            AgentCatalogEntry(
                id=uuid4(),
                name=f"agent-{i:03d}",
                description=f"Test agent number {i}",
                scope=ScopeType.PROJECT if i % 3 == 0 else ScopeType.GLOBAL,
                model=ModelType.SONNET if i % 3 == 0 else ModelType.HAIKU,
                path=temp_agent_dir / f"agent-{i:03d}.md",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={"template": "basic"},
            )
        )
    return AgentCatalog(agents=entries)


# ============================================================================
# Agent Markdown Content Fixtures
# ============================================================================


@pytest.fixture
def sample_agent_md_content() -> str:
    """Sample agent markdown file content."""
    return """---
name: test-agent
description: Test agent description. Use when testing.
model: claude-3-5-sonnet-20241022
---

# Test Agent

This is a test agent for automated testing purposes.

## When to Use

Use this agent when you need to test the agent builder functionality.

## Approach

1. Read the requirements
2. Execute the test
3. Report results
"""


@pytest.fixture
def sample_agent_md_with_frontmatter() -> str:
    """Sample agent markdown with complex frontmatter."""
    return """---
name: advanced-agent
description: Advanced agent with complex configuration. Use for complex workflows.
model: claude-opus-4-20250514
metadata:
  version: "1.0"
  author: test
  tags:
    - planning
    - architecture
---

# Advanced Agent

Complex agent for testing.

## When to Use

Use for complex multi-step workflows requiring planning.
"""


# ============================================================================
# CLI Testing Fixtures
# ============================================================================


@pytest.fixture
def cli_runner():
    """Click CLI runner for testing CLI commands."""
    return CliRunner()


@pytest.fixture
def mock_questionary():
    """Mock questionary module for wizard testing."""
    mock = MagicMock()

    # Mock text input
    mock.text = MagicMock(return_value=MagicMock(ask=MagicMock(return_value="test-agent")))

    # Mock select
    mock.select = MagicMock(return_value=MagicMock(ask=MagicMock(return_value="basic")))

    # Mock confirm
    mock.confirm = MagicMock(return_value=MagicMock(ask=MagicMock(return_value=True)))

    return mock


# ============================================================================
# Catalog File Fixtures
# ============================================================================


@pytest.fixture
def catalog_json_file(tmp_path) -> Path:
    """Creates a catalog.json file for testing."""
    catalog_file = tmp_path / "catalog.json"
    catalog_data = {
        "schema_version": "1.0",
        "agents": [
            {
                "id": str(uuid4()),
                "name": "test-agent",
                "description": "Test agent",
                "scope": "project",
                "model": "claude-3-5-sonnet-20241022",
                "path": str(tmp_path / "agents" / "test-agent.md"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {"template": "basic"},
            }
        ],
    }
    catalog_file.write_text(json.dumps(catalog_data, indent=2))
    return catalog_file


@pytest.fixture
def corrupted_catalog_json(tmp_path) -> Path:
    """Creates a corrupted catalog.json for error testing."""
    catalog_file = tmp_path / "catalog.json"
    catalog_file.write_text('{"agents": [{"name": "broken", "invalid"}')
    return catalog_file


# ============================================================================
# Template Fixtures
# ============================================================================


@pytest.fixture
def template_variables() -> Dict[str, str]:
    """Common template variables for testing."""
    return {
        "name": "test-agent",
        "description": "Test agent description. Use when testing.",
        "model": "claude-3-5-sonnet-20241022",
        "content": "This is the agent content.",
    }


@pytest.fixture
def all_template_names() -> List[str]:
    """List of all available template names."""
    return ["basic"]
