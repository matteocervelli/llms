"""Shared test fixtures for skill_builder tests."""

from datetime import datetime
from uuid import uuid4

import pytest

from src.tools.skill_builder.models import (
    ScopeType,
    SkillCatalogEntry,
    SkillConfig,
)


@pytest.fixture
def temp_skill_dir(tmp_path):
    """Creates temporary skill directory structure."""
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    return skills_dir


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
