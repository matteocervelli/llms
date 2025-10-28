"""Tests for CatalogManager class."""

import json
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest

from src.tools.skill_builder.catalog import CatalogManager
from src.tools.skill_builder.exceptions import (
    CatalogCorruptedError,
    CatalogError,
    SkillExistsError,
)
from src.tools.skill_builder.models import (
    ScopeType,
    SkillCatalog,
    SkillCatalogEntry,
)


class TestCatalogManagerInit:
    """Test catalog initialization."""

    def test_default_catalog_path(self, tmp_path, monkeypatch):
        """Test catalog uses cwd/skills.json by default."""
        monkeypatch.chdir(tmp_path)
        manager = CatalogManager()

        assert manager.catalog_path == tmp_path / "skills.json"
        assert manager.catalog_path.exists()

    def test_custom_catalog_path(self, tmp_path):
        """Test catalog accepts custom path."""
        custom_path = tmp_path / "custom" / "catalog.json"
        manager = CatalogManager(catalog_path=custom_path)

        assert manager.catalog_path == custom_path.resolve()
        assert custom_path.exists()

    def test_creates_empty_catalog_if_missing(self, tmp_path):
        """Test catalog file is created if it doesn't exist."""
        catalog_path = tmp_path / "skills.json"
        manager = CatalogManager(catalog_path)

        assert catalog_path.exists()

        # Verify it's a valid empty catalog
        with open(catalog_path) as f:
            data = json.load(f)

        assert data["schema_version"] == "1.0"
        assert data["skills"] == []


class TestCatalogCRUD:
    """Test CRUD operations."""

    @pytest.fixture
    def catalog_manager(self, tmp_path):
        """CatalogManager with temporary catalog."""
        return CatalogManager(tmp_path / "skills.json")

    @pytest.fixture
    def sample_entry(self, tmp_path):
        """Sample skill catalog entry."""
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        return SkillCatalogEntry(
            name="test-skill",
            description="Test skill description",
            scope=ScopeType.PROJECT,
            path=skill_dir,
            metadata={"template": "basic", "has_scripts": False, "file_count": 1},
        )

    def test_add_skill(self, catalog_manager, sample_entry):
        """Test adding skill to catalog."""
        catalog_manager.add_skill(sample_entry)

        # Verify skill was added
        retrieved = catalog_manager.get_skill(name="test-skill", scope=ScopeType.PROJECT)
        assert retrieved is not None
        assert retrieved.name == "test-skill"
        assert retrieved.description == "Test skill description"

    def test_add_duplicate_skill_raises_error(self, catalog_manager, sample_entry):
        """Test adding duplicate skill raises SkillExistsError."""
        catalog_manager.add_skill(sample_entry)

        # Attempt to add same skill again
        duplicate = SkillCatalogEntry(
            name="test-skill",
            description="Different description",
            scope=ScopeType.PROJECT,
            path=sample_entry.path,
            metadata={},
        )

        with pytest.raises(SkillExistsError, match="already exists"):
            catalog_manager.add_skill(duplicate)

    def test_get_skill_by_id(self, catalog_manager, sample_entry):
        """Test retrieving skill by UUID."""
        catalog_manager.add_skill(sample_entry)

        retrieved = catalog_manager.get_skill(skill_id=sample_entry.id)
        assert retrieved is not None
        assert retrieved.id == sample_entry.id
        assert retrieved.name == "test-skill"

    def test_get_skill_by_name(self, catalog_manager, sample_entry):
        """Test retrieving skill by name and scope."""
        catalog_manager.add_skill(sample_entry)

        retrieved = catalog_manager.get_skill(name="test-skill", scope=ScopeType.PROJECT)
        assert retrieved is not None
        assert retrieved.name == "test-skill"
        assert retrieved.scope == ScopeType.PROJECT

    def test_get_skill_not_found(self, catalog_manager):
        """Test getting non-existent skill returns None."""
        result = catalog_manager.get_skill(name="nonexistent", scope=ScopeType.PROJECT)
        assert result is None

    def test_update_skill(self, catalog_manager, sample_entry):
        """Test updating skill entry."""
        catalog_manager.add_skill(sample_entry)

        # Update description
        success = catalog_manager.update_skill(
            sample_entry.id,
            description="Updated description",
            updated_at=datetime.now(),
        )

        assert success is True

        # Verify update
        retrieved = catalog_manager.get_skill(skill_id=sample_entry.id)
        assert retrieved.description == "Updated description"

    def test_update_nonexistent_skill(self, catalog_manager):
        """Test updating non-existent skill returns False."""
        fake_id = uuid4()
        success = catalog_manager.update_skill(fake_id, description="Updated")
        assert success is False

    def test_remove_skill(self, catalog_manager, sample_entry):
        """Test removing skill from catalog."""
        catalog_manager.add_skill(sample_entry)

        # Remove skill
        success = catalog_manager.remove_skill(sample_entry.id)
        assert success is True

        # Verify removal
        retrieved = catalog_manager.get_skill(skill_id=sample_entry.id)
        assert retrieved is None

    def test_remove_nonexistent_skill(self, catalog_manager):
        """Test removing non-existent skill returns False."""
        fake_id = uuid4()
        success = catalog_manager.remove_skill(fake_id)
        assert success is False


class TestCatalogQuery:
    """Test query operations."""

    @pytest.fixture
    def populated_catalog(self, tmp_path):
        """CatalogManager with multiple skills."""
        manager = CatalogManager(tmp_path / "skills.json")

        # Create skill directories
        for i, (name, scope, template, has_scripts) in enumerate(
            [
                ("skill-one", ScopeType.GLOBAL, "basic", False),
                ("skill-two", ScopeType.PROJECT, "with_tools", False),
                ("skill-three", ScopeType.PROJECT, "with_scripts", True),
                ("skill-four", ScopeType.LOCAL, "advanced", True),
            ]
        ):
            skill_dir = tmp_path / name
            skill_dir.mkdir()
            if has_scripts:
                (skill_dir / "scripts").mkdir()

            entry = SkillCatalogEntry(
                name=name,
                description=f"Description for {name}. Use for testing.",
                scope=scope,
                path=skill_dir,
                metadata={
                    "template": template,
                    "has_scripts": has_scripts,
                    "file_count": 2 if has_scripts else 1,
                },
            )
            manager.add_skill(entry)

        return manager

    def test_list_skills_all(self, populated_catalog):
        """Test listing all skills."""
        skills = populated_catalog.list_skills()
        assert len(skills) == 4
        assert all(isinstance(s, SkillCatalogEntry) for s in skills)

    def test_list_skills_by_scope_global(self, populated_catalog):
        """Test listing skills filtered by GLOBAL scope."""
        skills = populated_catalog.list_skills(scope=ScopeType.GLOBAL)
        assert len(skills) == 1
        assert skills[0].name == "skill-one"

    def test_list_skills_by_scope_project(self, populated_catalog):
        """Test listing skills filtered by PROJECT scope."""
        skills = populated_catalog.list_skills(scope=ScopeType.PROJECT)
        assert len(skills) == 2
        names = {s.name for s in skills}
        assert names == {"skill-two", "skill-three"}

    def test_search_skills_by_query(self, populated_catalog):
        """Test searching skills by text query."""
        # Search for "testing" in description
        results = populated_catalog.search_skills(query="testing")
        assert len(results) == 4  # All have "testing" in description

        # Search for specific skill name
        results = populated_catalog.search_skills(query="skill-two")
        assert len(results) == 1
        assert results[0].name == "skill-two"

    def test_search_skills_by_scope_filter(self, populated_catalog):
        """Test searching with scope filter."""
        results = populated_catalog.search_skills(scope=ScopeType.PROJECT)
        assert len(results) == 2
        assert all(s.scope == ScopeType.PROJECT for s in results)

    def test_search_skills_by_has_scripts(self, populated_catalog):
        """Test searching by has_scripts metadata."""
        results = populated_catalog.search_skills(has_scripts=True)
        assert len(results) == 2
        assert all(s.metadata.get("has_scripts") is True for s in results)

        results = populated_catalog.search_skills(has_scripts=False)
        assert len(results) == 2
        assert all(s.metadata.get("has_scripts") is False for s in results)

    def test_search_skills_by_template(self, populated_catalog):
        """Test searching by template metadata."""
        results = populated_catalog.search_skills(template="basic")
        assert len(results) == 1
        assert results[0].name == "skill-one"

    def test_search_skills_multiple_filters(self, populated_catalog):
        """Test searching with multiple filters."""
        results = populated_catalog.search_skills(
            scope=ScopeType.PROJECT, has_scripts=True
        )
        assert len(results) == 1
        assert results[0].name == "skill-three"


class TestCatalogSync:
    """Test filesystem sync operations."""

    @pytest.fixture
    def sync_setup(self, tmp_path, monkeypatch):
        """Setup for sync tests."""
        # Create mock project structure
        project_root = tmp_path / "project"
        project_root.mkdir()

        # Create project skills directory
        skills_dir = project_root / ".claude" / "skills"
        skills_dir.mkdir(parents=True)

        # Create a skill with SKILL.md
        skill_dir = skills_dir / "test-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            """---
name: test-skill
description: Test skill from filesystem
template: basic
---
# Test Skill Content
"""
        )

        # Create catalog manager
        catalog_path = project_root / "skills.json"
        manager = CatalogManager(catalog_path)

        return manager, project_root

    def test_sync_adds_untracked_skills(self, sync_setup):
        """Test sync adds skills not in catalog."""
        manager, project_root = sync_setup

        # Sync should add the skill
        report = manager.sync_catalog(project_root)

        assert "test-skill" in report["added"]
        assert len(report["added"]) == 1
        assert len(report["removed"]) == 0

        # Verify skill was added to catalog
        skill = manager.get_skill(name="test-skill", scope=ScopeType.PROJECT)
        assert skill is not None
        assert skill.description == "Test skill from filesystem"

    def test_sync_removes_orphaned_entries(self, sync_setup, tmp_path):
        """Test sync removes catalog entries for deleted skills."""
        manager, project_root = sync_setup

        # Add skill to catalog manually
        orphaned_dir = tmp_path / "orphaned-skill"
        orphaned_entry = SkillCatalogEntry(
            name="orphaned-skill",
            description="This skill was deleted",
            scope=ScopeType.PROJECT,
            path=orphaned_dir,  # Path doesn't exist
            metadata={},
        )
        manager.add_skill(orphaned_entry)

        # Sync should remove orphaned entry
        report = manager.sync_catalog(project_root)

        assert "orphaned-skill" in report["removed"]
        assert len(report["removed"]) == 1

        # Verify skill was removed from catalog
        skill = manager.get_skill(name="orphaned-skill", scope=ScopeType.PROJECT)
        assert skill is None

    def test_sync_accurate_report(self, sync_setup, tmp_path):
        """Test sync returns accurate report."""
        manager, project_root = sync_setup

        # Add orphaned skill
        orphaned_dir = tmp_path / "orphaned"
        orphaned_entry = SkillCatalogEntry(
            name="orphaned",
            description="Orphaned",
            scope=ScopeType.PROJECT,
            path=orphaned_dir,
            metadata={},
        )
        manager.add_skill(orphaned_entry)

        # Sync
        report = manager.sync_catalog(project_root)

        # Verify report structure
        assert "added" in report
        assert "removed" in report
        assert "errors" in report

        assert isinstance(report["added"], list)
        assert isinstance(report["removed"], list)
        assert isinstance(report["errors"], list)

        # Verify contents
        assert "test-skill" in report["added"]
        assert "orphaned" in report["removed"]


class TestCatalogResilience:
    """Test error handling and atomic writes."""

    def test_atomic_write_no_tmp_files(self, tmp_path):
        """Test atomic write doesn't leave temp files."""
        catalog_path = tmp_path / "skills.json"
        manager = CatalogManager(catalog_path)

        # Add skill
        skill_dir = tmp_path / "test-skill"
        skill_dir.mkdir()
        entry = SkillCatalogEntry(
            name="test-skill",
            description="Test",
            scope=ScopeType.PROJECT,
            path=skill_dir,
            metadata={},
        )
        manager.add_skill(entry)

        # Check for temp files
        temp_files = list(tmp_path.glob("*.tmp"))
        json_temp_files = list(tmp_path.glob("*.json.*"))

        assert len(temp_files) == 0, "Found .tmp files after write"
        # Allow .bak files but not other temp files
        assert all(
            f.suffix == ".bak" for f in json_temp_files
        ), "Found unexpected temp files"

    def test_corrupted_json_recovery(self, tmp_path):
        """Test handling of corrupted JSON file."""
        catalog_path = tmp_path / "skills.json"

        # Create corrupted JSON
        catalog_path.write_text("{ invalid json content")

        # Attempting to read should raise CatalogCorruptedError
        with pytest.raises(CatalogCorruptedError, match="Invalid JSON"):
            manager = CatalogManager(catalog_path)
            # Force read attempt
            manager._read_catalog()


class TestCatalogStats:
    """Test catalog statistics."""

    def test_catalog_stats(self, tmp_path):
        """Test get_catalog_stats returns accurate counts."""
        manager = CatalogManager(tmp_path / "skills.json")

        # Add skills across different scopes and templates
        for i, (name, scope, template, has_scripts) in enumerate(
            [
                ("skill1", ScopeType.GLOBAL, "basic", False),
                ("skill2", ScopeType.GLOBAL, "basic", True),
                ("skill3", ScopeType.PROJECT, "with_tools", False),
                ("skill4", ScopeType.PROJECT, "advanced", True),
                ("skill5", ScopeType.LOCAL, "advanced", False),
            ]
        ):
            skill_dir = tmp_path / name
            skill_dir.mkdir()
            entry = SkillCatalogEntry(
                name=name,
                description=f"Skill {i}",
                scope=scope,
                path=skill_dir,
                metadata={"template": template, "has_scripts": has_scripts},
            )
            manager.add_skill(entry)

        # Get stats
        stats = manager.get_catalog_stats()

        # Verify totals
        assert stats["total"] == 5

        # Verify by-scope counts
        assert stats["by_scope"]["global"] == 2
        assert stats["by_scope"]["project"] == 2
        assert stats["by_scope"]["local"] == 1

        # Verify by-template counts
        assert stats["by_template"]["basic"] == 2
        assert stats["by_template"]["with_tools"] == 1
        assert stats["by_template"]["advanced"] == 2

        # Verify with_scripts count
        assert stats["with_scripts"] == 2


class TestPerformance:
    """Test performance requirements."""

    def test_operations_under_100ms(self, tmp_path):
        """Test all operations complete in < 100ms."""
        manager = CatalogManager(tmp_path / "skills.json")

        # Create skill entry
        skill_dir = tmp_path / "perf-test"
        skill_dir.mkdir()
        entry = SkillCatalogEntry(
            name="perf-test",
            description="Performance test skill",
            scope=ScopeType.PROJECT,
            path=skill_dir,
            metadata={"template": "basic"},
        )

        # Test add_skill
        start = time.perf_counter()
        manager.add_skill(entry)
        add_time = (time.perf_counter() - start) * 1000
        assert add_time < 100, f"add_skill took {add_time:.2f}ms"

        # Test get_skill
        start = time.perf_counter()
        manager.get_skill(skill_id=entry.id)
        get_time = (time.perf_counter() - start) * 1000
        assert get_time < 100, f"get_skill took {get_time:.2f}ms"

        # Test list_skills
        start = time.perf_counter()
        manager.list_skills()
        list_time = (time.perf_counter() - start) * 1000
        assert list_time < 100, f"list_skills took {list_time:.2f}ms"

        # Test search_skills
        start = time.perf_counter()
        manager.search_skills(query="test")
        search_time = (time.perf_counter() - start) * 1000
        assert search_time < 100, f"search_skills took {search_time:.2f}ms"

        # Test update_skill
        start = time.perf_counter()
        manager.update_skill(entry.id, description="Updated")
        update_time = (time.perf_counter() - start) * 1000
        assert update_time < 100, f"update_skill took {update_time:.2f}ms"

        # Test remove_skill
        start = time.perf_counter()
        manager.remove_skill(entry.id)
        remove_time = (time.perf_counter() - start) * 1000
        assert remove_time < 100, f"remove_skill took {remove_time:.2f}ms"

        # Test get_catalog_stats
        start = time.perf_counter()
        manager.get_catalog_stats()
        stats_time = (time.perf_counter() - start) * 1000
        assert stats_time < 100, f"get_catalog_stats took {stats_time:.2f}ms"
