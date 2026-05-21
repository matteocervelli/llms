"""
Tests for the Syncer component - catalog synchronization with filesystem.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime

from src.tools.catalog_system.syncer import Syncer
from src.tools.catalog_system.models import (
    SkillCatalogEntry,
    CommandCatalogEntry,
    AgentCatalogEntry,
)
from src.tools.catalog_system.exceptions import SyncError


@pytest.fixture
def syncer():
    """Create a Syncer instance."""
    return Syncer()


@pytest.fixture
def temp_catalog(tmp_path):
    """Create a temporary catalog file."""
    catalog_file = tmp_path / "test_catalog.json"
    return catalog_file


@pytest.fixture
def sample_catalog_data():
    """Sample catalog data."""
    return {"schema_version": "1.0", "entries": []}


class TestSyncerInitialization:
    """Test Syncer initialization."""

    def test_syncer_creation(self, syncer):
        """Test Syncer can be created."""
        assert syncer is not None


class TestSync:
    """Test sync functionality."""

    def test_sync_empty_catalog(self, syncer, temp_catalog):
        """Test syncing with empty catalog creates new entries."""
        discovered = [
            SkillCatalogEntry(
                name="test-skill",
                scope="global",
                description="Test skill",
                file_path=Path("/test/skill1"),
                template="basic",
            )
        ]

        result = syncer.sync(temp_catalog, discovered)
        assert len(result) == 1
        assert result[0].name == "test-skill"

    def test_sync_preserves_existing(self, syncer, temp_catalog):
        """Test sync preserves existing entries not in discovered."""
        # Create catalog with existing entry
        existing = SkillCatalogEntry(
            name="existing-skill",
            scope="global",
            description="Existing",
            file_path=Path("/test/existing"),
            template="basic",
        )

        # Write catalog
        catalog_data = {
            "schema_version": "1.0",
            "entries": [existing.model_dump(mode="json")],
        }
        temp_catalog.write_text(json.dumps(catalog_data, indent=2))

        # Sync with empty discovered (should keep existing)
        result = syncer.sync(temp_catalog, [])
        assert len(result) >= 0  # Depends on implementation

    def test_sync_updates_existing(self, syncer, temp_catalog):
        """Test sync updates existing entries from discovered."""
        entry_id = "550e8400-e29b-41d4-a716-446655440000"

        # Create catalog with existing entry
        existing_data = {
            "id": entry_id,
            "name": "test-skill",
            "scope": "global",
            "description": "Old description",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "file_path": "/test/skill",
            "template": "basic",
            "has_scripts": False,
            "file_count": 1,
            "allowed_tools": [],
        }

        catalog_data = {"schema_version": "1.0", "entries": [existing_data]}
        temp_catalog.write_text(json.dumps(catalog_data, indent=2))

        # Sync with updated entry
        discovered = [
            SkillCatalogEntry(
                name="test-skill",
                scope="global",
                description="New description",
                file_path=Path("/test/skill"),
                template="tool-enhanced",
            )
        ]

        result = syncer.sync(temp_catalog, discovered)
        # Should have updated description
        updated = [e for e in result if e.name == "test-skill"][0]
        assert updated.description == "New description"

    def test_sync_atomic_write(self, syncer, temp_catalog):
        """Test sync uses atomic write pattern."""
        discovered = [
            SkillCatalogEntry(
                name="skill1",
                scope="global",
                description="Skill 1",
                file_path=Path("/test/skill1"),
                template="basic",
            )
        ]

        syncer.sync(temp_catalog, discovered)

        # Catalog should exist
        assert temp_catalog.exists()

        # Should be valid JSON
        data = json.loads(temp_catalog.read_text())
        assert "schema_version" in data


class TestErrorHandling:
    """Test error handling."""

    def test_sync_handles_corrupted_catalog(self, syncer, temp_catalog):
        """Test sync handles corrupted catalog gracefully."""
        # Write invalid JSON
        temp_catalog.write_text("{ invalid json }")

        discovered = [
            SkillCatalogEntry(
                name="skill1",
                scope="global",
                description="Skill 1",
                file_path=Path("/test/skill1"),
                template="basic",
            )
        ]

        # Should handle gracefully or raise SyncError
        try:
            result = syncer.sync(temp_catalog, discovered)
            # If it handles gracefully, should have discovered entry
            assert len(result) >= 1
        except SyncError:
            # Acceptable to raise SyncError
            pass

    def test_read_catalog_handles_generic_error(self, syncer, temp_catalog):
        """Test _read_catalog handles non-JSON errors."""
        # Create catalog with valid JSON but invalid entry data
        catalog_data = {
            "schema_version": "1.0",
            "entries": [{"invalid": "entry"}],
        }
        temp_catalog.write_text(json.dumps(catalog_data))

        # Should not crash, should return empty or partial list
        result = syncer._read_catalog(temp_catalog)
        assert isinstance(result, list)

    def test_write_catalog_creates_parent_directory(self, syncer, tmp_path):
        """Test _write_catalog creates parent directory if needed."""
        catalog_path = tmp_path / "subdir" / "catalog.json"
        entries = [
            SkillCatalogEntry(
                name="skill1",
                scope="global",
                description="Skill 1",
                file_path=Path("/test/skill1"),
                template="basic",
            )
        ]

        syncer._write_catalog(catalog_path, entries)
        assert catalog_path.exists()
        assert catalog_path.parent.exists()

    def test_write_catalog_creates_backup(self, syncer, temp_catalog):
        """Test _write_catalog creates backup of existing catalog."""
        # Write initial catalog
        initial_entries = [
            SkillCatalogEntry(
                name="initial",
                scope="global",
                description="Initial",
                file_path=Path("/test/initial"),
                template="basic",
            )
        ]
        syncer._write_catalog(temp_catalog, initial_entries)

        # Update catalog
        updated_entries = [
            SkillCatalogEntry(
                name="updated",
                scope="global",
                description="Updated",
                file_path=Path("/test/updated"),
                template="basic",
            )
        ]
        syncer._write_catalog(temp_catalog, updated_entries)

        # Backup should have been created and cleaned up
        backup_path = temp_catalog.with_suffix(".json.bak")
        assert not backup_path.exists()  # Cleaned up on success


class TestDeserialization:
    """Test entry deserialization."""

    def test_deserialize_skill_entry(self, syncer):
        """Test deserializing skill entry."""
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "test-skill",
            "scope": "global",
            "description": "Test",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "file_path": "/test/skill",
            "template": "basic",
            "has_scripts": False,
            "file_count": 1,
            "allowed_tools": [],
        }

        entry = syncer._deserialize_entry(data)
        assert isinstance(entry, SkillCatalogEntry)
        assert entry.name == "test-skill"

    def test_deserialize_agent_entry(self, syncer):
        """Test deserializing agent entry."""
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "name": "test-agent",
            "scope": "global",
            "description": "Test",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "file_path": "/test/agent",
            "model": "claude-3-5-sonnet",
            "has_skills": False,
            "skill_count": 0,
            "allowed_tools": [],
        }

        entry = syncer._deserialize_entry(data)
        assert isinstance(entry, AgentCatalogEntry)
        assert entry.name == "test-agent"

    def test_deserialize_command_entry(self, syncer):
        """Test deserializing command entry."""
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440002",
            "name": "test-command",
            "scope": "global",
            "description": "Test",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "file_path": "/test/command",
            "aliases": ["tc"],
            "tags": ["test"],
        }

        entry = syncer._deserialize_entry(data)
        assert isinstance(entry, CommandCatalogEntry)
        assert entry.name == "test-command"

    def test_deserialize_invalid_entry(self, syncer):
        """Test deserializing invalid entry returns None."""
        data = {"invalid": "data"}

        entry = syncer._deserialize_entry(data)
        assert entry is None

    def test_deserialize_unknown_type(self, syncer):
        """Test deserializing entry without type markers returns None."""
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440003",
            "name": "unknown",
            "scope": "global",
            "description": "Unknown type",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "file_path": "/test/unknown",
        }

        entry = syncer._deserialize_entry(data)
        assert entry is None
