"""Tests for skill_builder catalog functionality."""

from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

# Note: SkillCatalog raises ValueError, not custom exceptions
from src.tools.skill_builder.models import (
    ScopeType,
    SkillCatalog,
    SkillCatalogEntry,
)


class TestSkillCatalogEntry:
    """Tests for SkillCatalogEntry model."""

    def test_valid_catalog_entry(self, temp_skill_dir):
        """Test valid catalog entry creation."""
        entry = SkillCatalogEntry(
            id=uuid4(),
            name="test-skill",
            description="Test",
            scope=ScopeType.PROJECT,
            path=temp_skill_dir / "test-skill",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={},
        )
        assert entry.name == "test-skill"
        assert entry.scope == ScopeType.PROJECT
        assert isinstance(entry.id, UUID)

    def test_catalog_entry_with_metadata(self, temp_skill_dir):
        """Test catalog entry with metadata."""
        entry = SkillCatalogEntry(
            id=uuid4(),
            name="test-skill",
            description="Test",
            scope=ScopeType.PROJECT,
            path=temp_skill_dir / "test-skill",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"template": "basic", "has_scripts": True},
        )
        assert entry.metadata["template"] == "basic"
        assert entry.metadata["has_scripts"] is True

    def test_catalog_entry_path_must_be_absolute(self):
        """Test that relative paths are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SkillCatalogEntry(
                id=uuid4(),
                name="test-skill",
                description="Test",
                scope=ScopeType.PROJECT,
                path=Path("relative/path"),  # Invalid: relative
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={},
            )
        assert "absolute" in str(exc_info.value).lower()


class TestSkillCatalog:
    """Tests for SkillCatalog model and operations."""

    def test_empty_catalog(self):
        """Test creating empty catalog."""
        catalog = SkillCatalog(skills=[])
        assert len(catalog.skills) == 0

    def test_catalog_with_entries(self, temp_skill_dir):
        """Test catalog with multiple entries."""
        entries = [
            SkillCatalogEntry(
                id=uuid4(),
                name=f"skill-{i}",
                description="Test",
                scope=ScopeType.PROJECT,
                path=temp_skill_dir / f"skill-{i}",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={},
            )
            for i in range(3)
        ]
        catalog = SkillCatalog(skills=entries)
        assert len(catalog.skills) == 3

    def test_get_by_name_found(self, sample_catalog_entry):
        """Test finding skill by name."""
        catalog = SkillCatalog(skills=[sample_catalog_entry])
        found = catalog.get_by_name("test-skill")
        assert found is not None
        assert found.name == "test-skill"

    def test_get_by_name_not_found(self, sample_catalog_entry):
        """Test finding non-existent skill."""
        catalog = SkillCatalog(skills=[sample_catalog_entry])
        found = catalog.get_by_name("nonexistent")
        assert found is None

    def test_filter_by_scope(self, temp_skill_dir):
        """Test filtering by scope."""
        entries = [
            SkillCatalogEntry(
                id=uuid4(),
                name="global-skill",
                description="Test",
                scope=ScopeType.GLOBAL,
                path=temp_skill_dir / "global-skill",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={},
            ),
            SkillCatalogEntry(
                id=uuid4(),
                name="project-skill",
                description="Test",
                scope=ScopeType.PROJECT,
                path=temp_skill_dir / "project-skill",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={},
            ),
        ]
        catalog = SkillCatalog(skills=entries)

        global_skills = catalog.filter_by_scope(ScopeType.GLOBAL)
        assert len(global_skills) == 1
        assert global_skills[0].name == "global-skill"

        project_skills = catalog.filter_by_scope(ScopeType.PROJECT)
        assert len(project_skills) == 1
        assert project_skills[0].name == "project-skill"

    def test_add_skill(self, sample_catalog_entry):
        """Test adding skill to catalog."""
        catalog = SkillCatalog(skills=[])
        catalog.add_skill(sample_catalog_entry)
        assert len(catalog.skills) == 1
        assert catalog.skills[0].name == "test-skill"

    def test_add_duplicate_skill_raises_error(self, sample_catalog_entry):
        """Test that adding duplicate skill raises ValueError."""
        catalog = SkillCatalog(skills=[sample_catalog_entry])
        with pytest.raises(ValueError):
            catalog.add_skill(sample_catalog_entry)

    def test_update_skill(self, sample_catalog_entry):
        """Test updating existing skill."""
        catalog = SkillCatalog(skills=[sample_catalog_entry])
        result = catalog.update_skill(sample_catalog_entry.id, description="Updated description")
        assert result is True

        found = catalog.get_by_name("test-skill")
        assert found is not None
        assert found.description == "Updated description"

    def test_update_nonexistent_skill(self):
        """Test that updating non-existent skill returns False."""
        catalog = SkillCatalog(skills=[])
        result = catalog.update_skill(uuid4(), description="Test")
        assert result is False

    def test_remove_skill(self, sample_catalog_entry):
        """Test removing skill from catalog."""
        catalog = SkillCatalog(skills=[sample_catalog_entry])
        result = catalog.remove_skill(sample_catalog_entry.id)
        assert result is True
        assert len(catalog.skills) == 0

    def test_remove_nonexistent_skill(self):
        """Test that removing non-existent skill returns False."""
        catalog = SkillCatalog(skills=[])
        result = catalog.remove_skill(uuid4())
        assert result is False

    def test_get_by_id(self, sample_catalog_entry):
        """Test finding skill by UUID."""
        catalog = SkillCatalog(skills=[sample_catalog_entry])
        found = catalog.get_by_id(sample_catalog_entry.id)
        assert found is not None
        assert found.id == sample_catalog_entry.id

    def test_search(self, temp_skill_dir):
        """Test searching skills."""
        entries = [
            SkillCatalogEntry(
                id=uuid4(),
                name="pdf-processor",
                description="Process PDF files",
                scope=ScopeType.PROJECT,
                path=temp_skill_dir / "pdf-processor",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={},
            ),
            SkillCatalogEntry(
                id=uuid4(),
                name="image-processor",
                description="Process images",
                scope=ScopeType.PROJECT,
                path=temp_skill_dir / "image-processor",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={},
            ),
        ]
        catalog = SkillCatalog(skills=entries)

        results = catalog.search("pdf")
        assert len(results) == 1
        assert results[0].name == "pdf-processor"

        results = catalog.search("processor")
        assert len(results) == 2
