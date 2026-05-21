"""Shared test fixtures for skill_builder tests."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from click.testing import CliRunner

from src.tools.skill_builder.models import (
    ScopeType,
    SkillCatalog,
    SkillCatalogEntry,
    SkillConfig,
)


# ============================================================================
# Directory and Path Fixtures
# ============================================================================


@pytest.fixture
def temp_skill_dir(tmp_path):
    """Creates temporary skill directory structure."""
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    return skills_dir


@pytest.fixture
def temp_project_root(tmp_path):
    """Creates temporary project root with .claude directory."""
    project_root = tmp_path / "project"
    project_root.mkdir()
    claude_dir = project_root / ".claude"
    claude_dir.mkdir()
    skills_dir = claude_dir / "skills"
    skills_dir.mkdir()
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
def sample_skill_config():
    """Sample skill configuration for testing."""
    return SkillConfig(
        name="test-skill",
        description="Test skill description. Use when testing.",
        scope=ScopeType.PROJECT,
        template="basic",
        allowed_tools=["Read", "Grep"],
    )


@pytest.fixture
def sample_skill_config_with_tools():
    """Sample skill configuration with multiple tools."""
    return SkillConfig(
        name="advanced-skill",
        description="Advanced skill with multiple tools. Use for complex operations.",
        scope=ScopeType.PROJECT,
        template="with_tools",
        allowed_tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
    )


@pytest.fixture
def sample_skill_config_with_scripts():
    """Sample skill configuration with scripts directory."""
    return SkillConfig(
        name="scripted-skill",
        description="Skill with helper scripts. Use for automated operations.",
        scope=ScopeType.PROJECT,
        template="with_scripts",
        allowed_tools=["Bash", "Read", "Write"],
    )


# ============================================================================
# Catalog Fixtures
# ============================================================================


@pytest.fixture
def sample_catalog_entry(temp_skill_dir):
    """Sample catalog entry for testing."""
    return SkillCatalogEntry(
        id=uuid4(),
        name="test-skill",
        description="Test skill",
        scope=ScopeType.PROJECT,
        path=temp_skill_dir / "test-skill",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        metadata={"template": "basic"},
    )


@pytest.fixture
def sample_catalog_with_entries(temp_skill_dir) -> SkillCatalog:
    """Sample catalog with multiple entries for testing."""
    entries = [
        SkillCatalogEntry(
            id=uuid4(),
            name="skill-one",
            description="First test skill",
            scope=ScopeType.PROJECT,
            path=temp_skill_dir / "skill-one",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"template": "basic"},
        ),
        SkillCatalogEntry(
            id=uuid4(),
            name="skill-two",
            description="Second test skill",
            scope=ScopeType.GLOBAL,
            path=temp_skill_dir / "skill-two",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"template": "with_tools", "has_scripts": False},
        ),
        SkillCatalogEntry(
            id=uuid4(),
            name="skill-three",
            description="Third test skill with scripts",
            scope=ScopeType.LOCAL,
            path=temp_skill_dir / "skill-three",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"template": "with_scripts", "has_scripts": True},
        ),
    ]
    return SkillCatalog(skills=entries)


@pytest.fixture
def large_catalog(temp_skill_dir) -> SkillCatalog:
    """Large catalog with 100+ entries for performance testing."""
    entries = []
    for i in range(120):
        entries.append(
            SkillCatalogEntry(
                id=uuid4(),
                name=f"skill-{i:03d}",
                description=f"Test skill number {i}",
                scope=ScopeType.PROJECT if i % 3 == 0 else ScopeType.GLOBAL,
                path=temp_skill_dir / f"skill-{i:03d}",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={
                    "template": ["basic", "with_tools", "with_scripts"][i % 3],
                    "has_scripts": i % 3 == 2,
                },
            )
        )
    return SkillCatalog(skills=entries)


# ============================================================================
# SKILL.md Content Fixtures
# ============================================================================


@pytest.fixture
def sample_skill_md_content() -> str:
    """Sample SKILL.md file content."""
    return """---
name: test-skill
description: Test skill description. Use when testing.
allowed-tools:
  - Read
  - Grep
---

# Test Skill

This is a test skill for automated testing purposes.

## Usage

Use this skill when you need to test the skill builder functionality.

## Tools

This skill can use the following tools:
- Read: For reading files
- Grep: For searching code
"""


@pytest.fixture
def sample_skill_md_with_frontmatter() -> str:
    """Sample SKILL.md with complex frontmatter."""
    return """---
name: advanced-skill
description: Advanced skill with multiple tools. Use for complex operations.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
metadata:
  template: with_tools
  version: "1.0"
  author: test
---

# Advanced Skill

Complex skill for testing.
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
    mock.text = MagicMock(return_value=MagicMock(ask=MagicMock(return_value="test-skill")))

    # Mock select
    mock.select = MagicMock(return_value=MagicMock(ask=MagicMock(return_value="basic")))

    # Mock checkbox
    mock.checkbox = MagicMock(return_value=MagicMock(ask=MagicMock(return_value=["Read", "Grep"])))

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
        "skills": [
            {
                "id": str(uuid4()),
                "name": "test-skill",
                "description": "Test skill",
                "scope": "project",
                "path": str(tmp_path / "skills" / "test-skill"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": {"template": "basic"},
            }
        ]
    }
    catalog_file.write_text(json.dumps(catalog_data, indent=2))
    return catalog_file


@pytest.fixture
def corrupted_catalog_json(tmp_path) -> Path:
    """Creates a corrupted catalog.json for error testing."""
    catalog_file = tmp_path / "catalog.json"
    catalog_file.write_text('{"skills": [{"name": "broken", "invalid"}')
    return catalog_file


# ============================================================================
# Template Fixtures
# ============================================================================


@pytest.fixture
def template_variables() -> Dict[str, str]:
    """Common template variables for testing."""
    return {
        "name": "test-skill",
        "description": "Test skill description. Use when testing.",
        "allowed_tools": "- Read\n- Grep",
        "content": "This is the skill content.",
    }


@pytest.fixture
def all_template_names() -> List[str]:
    """List of all available template names."""
    return ["basic", "with_tools", "with_scripts", "advanced"]
