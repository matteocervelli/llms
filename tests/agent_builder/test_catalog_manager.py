"""Tests for CatalogManager class."""

import json
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

import pytest

from src.tools.agent_builder.catalog import CatalogManager
from src.tools.agent_builder.exceptions import (
    CatalogCorruptedError,
    CatalogError,
    AgentExistsError,
)
from src.tools.agent_builder.models import (
    ScopeType,
    ModelType,
    AgentCatalog,
    AgentCatalogEntry,
)


class TestCatalogManagerInit:
    """Test catalog initialization."""

    def test_default_catalog_path(self, tmp_path, monkeypatch):
        """Test catalog uses cwd/agents.json by default."""
        monkeypatch.chdir(tmp_path)
        manager = CatalogManager()

        assert manager.catalog_path == tmp_path / "agents.json"
        assert manager.catalog_path.exists()

    def test_custom_catalog_path(self, tmp_path):
        """Test catalog accepts custom path."""
        custom_path = tmp_path / "custom" / "catalog.json"
        manager = CatalogManager(catalog_path=custom_path)

        assert manager.catalog_path == custom_path.resolve()
        assert custom_path.exists()

    def test_creates_empty_catalog_if_missing(self, tmp_path):
        """Test catalog file is created if it doesn't exist."""
        catalog_path = tmp_path / "agents.json"
        manager = CatalogManager(catalog_path)

        assert catalog_path.exists()

        # Verify it's a valid empty catalog
        with open(catalog_path) as f:
            data = json.load(f)

        assert data["schema_version"] == "1.0"
        assert data["agents"] == []


class TestCatalogCRUD:
    """Test CRUD operations."""

    @pytest.fixture
    def catalog_manager(self, tmp_path):
        """CatalogManager with temporary catalog."""
        return CatalogManager(tmp_path / "agents.json")

    @pytest.fixture
    def sample_entry(self, tmp_path):
        """Sample agent catalog entry."""
        agent_file = tmp_path / "test-agent.md"
        agent_file.write_text("# Test Agent")
        return AgentCatalogEntry(
            name="test-agent",
            description="Test agent description. Use when testing.",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=agent_file,
            metadata={"template": "basic"},
        )

    def test_add_agent(self, catalog_manager, sample_entry):
        """Test adding agent to catalog."""
        catalog_manager.add_agent(sample_entry)

        # Verify agent was added
        retrieved = catalog_manager.get_agent(name="test-agent", scope=ScopeType.PROJECT)
        assert retrieved is not None
        assert retrieved.name == "test-agent"
        assert retrieved.description == "Test agent description. Use when testing."

    def test_add_duplicate_agent_raises_error(self, catalog_manager, sample_entry):
        """Test adding duplicate agent raises AgentExistsError."""
        catalog_manager.add_agent(sample_entry)

        # Attempt to add same agent again
        duplicate = AgentCatalogEntry(
            name="test-agent",
            description="Different description",
            scope=ScopeType.PROJECT,
            model=ModelType.HAIKU,
            path=sample_entry.path,
            metadata={},
        )

        with pytest.raises(AgentExistsError, match="already exists"):
            catalog_manager.add_agent(duplicate)

    def test_get_agent_by_id(self, catalog_manager, sample_entry):
        """Test retrieving agent by UUID."""
        catalog_manager.add_agent(sample_entry)

        retrieved = catalog_manager.get_agent(agent_id=sample_entry.id)
        assert retrieved is not None
        assert retrieved.id == sample_entry.id
        assert retrieved.name == "test-agent"

    def test_get_agent_by_name(self, catalog_manager, sample_entry):
        """Test retrieving agent by name and scope."""
        catalog_manager.add_agent(sample_entry)

        retrieved = catalog_manager.get_agent(name="test-agent", scope=ScopeType.PROJECT)
        assert retrieved is not None
        assert retrieved.name == "test-agent"
        assert retrieved.scope == ScopeType.PROJECT

    def test_get_agent_not_found(self, catalog_manager):
        """Test getting non-existent agent returns None."""
        result = catalog_manager.get_agent(name="nonexistent", scope=ScopeType.PROJECT)
        assert result is None

    def test_update_agent(self, catalog_manager, sample_entry):
        """Test updating agent entry."""
        catalog_manager.add_agent(sample_entry)

        # Update description
        success = catalog_manager.update_agent(
            sample_entry.id,
            description="Updated description",
            updated_at=datetime.now(),
        )

        assert success is True

        # Verify update
        retrieved = catalog_manager.get_agent(agent_id=sample_entry.id)
        assert retrieved.description == "Updated description"

    def test_update_nonexistent_agent(self, catalog_manager):
        """Test updating non-existent agent returns False."""
        fake_id = uuid4()
        success = catalog_manager.update_agent(fake_id, description="Updated")
        assert success is False

    def test_remove_agent(self, catalog_manager, sample_entry):
        """Test removing agent from catalog."""
        catalog_manager.add_agent(sample_entry)

        # Remove agent
        success = catalog_manager.remove_agent(sample_entry.id)
        assert success is True

        # Verify removal
        retrieved = catalog_manager.get_agent(agent_id=sample_entry.id)
        assert retrieved is None

    def test_remove_nonexistent_agent(self, catalog_manager):
        """Test removing non-existent agent returns False."""
        fake_id = uuid4()
        success = catalog_manager.remove_agent(fake_id)
        assert success is False


class TestCatalogQuery:
    """Test query operations."""

    @pytest.fixture
    def populated_catalog(self, tmp_path):
        """CatalogManager with multiple agents."""
        manager = CatalogManager(tmp_path / "agents.json")

        # Create agent files
        for i, (name, scope, model, template) in enumerate(
            [
                ("agent-one", ScopeType.GLOBAL, ModelType.HAIKU, "basic"),
                ("agent-two", ScopeType.PROJECT, ModelType.SONNET, "advanced"),
                ("agent-three", ScopeType.PROJECT, ModelType.OPUS, "basic"),
                ("agent-four", ScopeType.LOCAL, ModelType.SONNET, "custom"),
            ]
        ):
            agent_file = tmp_path / f"{name}.md"
            agent_file.write_text(f"# {name}")

            entry = AgentCatalogEntry(
                name=name,
                description=f"Description for {name}. Use for testing.",
                scope=scope,
                model=model,
                path=agent_file,
                metadata={"template": template},
            )
            manager.add_agent(entry)

        return manager

    def test_list_agents_all(self, populated_catalog):
        """Test listing all agents."""
        agents = populated_catalog.list_agents()
        assert len(agents) == 4
        assert all(isinstance(a, AgentCatalogEntry) for a in agents)

    def test_list_agents_by_scope_global(self, populated_catalog):
        """Test listing agents filtered by GLOBAL scope."""
        agents = populated_catalog.list_agents(scope=ScopeType.GLOBAL)
        assert len(agents) == 1
        assert agents[0].name == "agent-one"

    def test_list_agents_by_scope_project(self, populated_catalog):
        """Test listing agents filtered by PROJECT scope."""
        agents = populated_catalog.list_agents(scope=ScopeType.PROJECT)
        assert len(agents) == 2
        names = {a.name for a in agents}
        assert names == {"agent-two", "agent-three"}

    def test_search_agents_by_query(self, populated_catalog):
        """Test searching agents by text query."""
        # Search for "testing" in description
        results = populated_catalog.search_agents(query="testing")
        assert len(results) == 4  # All have "testing" in description

        # Search for specific agent name
        results = populated_catalog.search_agents(query="agent-two")
        assert len(results) == 1
        assert results[0].name == "agent-two"

    def test_search_agents_by_scope_filter(self, populated_catalog):
        """Test searching with scope filter."""
        results = populated_catalog.search_agents(scope=ScopeType.PROJECT)
        assert len(results) == 2
        assert all(a.scope == ScopeType.PROJECT for a in results)

    def test_search_agents_by_model(self, populated_catalog):
        """Test searching by Claude model."""
        results = populated_catalog.search_agents(model=ModelType.SONNET)
        assert len(results) == 2
        assert all(a.model == ModelType.SONNET for a in results)

        results = populated_catalog.search_agents(model=ModelType.HAIKU)
        assert len(results) == 1
        assert results[0].name == "agent-one"

    def test_search_agents_by_template(self, populated_catalog):
        """Test searching by template metadata."""
        results = populated_catalog.search_agents(template="basic")
        assert len(results) == 2
        assert {a.name for a in results} == {"agent-one", "agent-three"}

    def test_search_agents_multiple_filters(self, populated_catalog):
        """Test searching with multiple filters."""
        results = populated_catalog.search_agents(scope=ScopeType.PROJECT, model=ModelType.OPUS)
        assert len(results) == 1
        assert results[0].name == "agent-three"


class TestCatalogSync:
    """Test filesystem sync operations."""

    @pytest.fixture
    def sync_setup(self, tmp_path, monkeypatch):
        """Setup for sync tests."""
        # Create mock project structure
        project_root = tmp_path / "project"
        project_root.mkdir()

        # Create project agents directory
        agents_dir = project_root / ".claude" / "agents"
        agents_dir.mkdir(parents=True)

        # Create an agent with frontmatter
        agent_file = agents_dir / "test-agent.md"
        agent_file.write_text(
            """---
name: test-agent
description: Test agent from filesystem. Use when syncing.
model: claude-3-5-sonnet-20241022
template: basic
---
# Test Agent Content
"""
        )

        # Create catalog manager
        catalog_path = project_root / "agents.json"
        manager = CatalogManager(catalog_path)

        return manager, project_root

    def test_sync_adds_untracked_agents(self, sync_setup):
        """Test sync adds agents not in catalog."""
        manager, project_root = sync_setup

        # Sync should add the agent
        report = manager.sync_catalog(project_root)

        assert "test-agent" in report["added"]
        assert len(report["added"]) == 1
        assert len(report["removed"]) == 0

        # Verify agent was added to catalog
        agent = manager.get_agent(name="test-agent", scope=ScopeType.PROJECT)
        assert agent is not None
        assert agent.description == "Test agent from filesystem. Use when syncing."

    def test_sync_removes_orphaned_entries(self, sync_setup, tmp_path):
        """Test sync removes catalog entries for deleted agents."""
        manager, project_root = sync_setup

        # Add agent to catalog manually
        orphaned_file = tmp_path / "orphaned-agent.md"
        orphaned_entry = AgentCatalogEntry(
            name="orphaned-agent",
            description="This agent was deleted",
            scope=ScopeType.PROJECT,
            model=ModelType.HAIKU,
            path=orphaned_file,  # Path doesn't exist
            metadata={},
        )
        manager.add_agent(orphaned_entry)

        # Sync should remove orphaned entry
        report = manager.sync_catalog(project_root)

        assert "orphaned-agent" in report["removed"]
        assert len(report["removed"]) == 1

        # Verify agent was removed from catalog
        agent = manager.get_agent(name="orphaned-agent", scope=ScopeType.PROJECT)
        assert agent is None

    def test_sync_accurate_report(self, sync_setup, tmp_path):
        """Test sync returns accurate report."""
        manager, project_root = sync_setup

        # Add orphaned agent
        orphaned_file = tmp_path / "orphaned.md"
        orphaned_entry = AgentCatalogEntry(
            name="orphaned",
            description="Orphaned",
            scope=ScopeType.PROJECT,
            model=ModelType.HAIKU,
            path=orphaned_file,
            metadata={},
        )
        manager.add_agent(orphaned_entry)

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
        assert "test-agent" in report["added"]
        assert "orphaned" in report["removed"]


class TestCatalogResilience:
    """Test error handling and atomic writes."""

    def test_atomic_write_no_tmp_files(self, tmp_path):
        """Test atomic write doesn't leave temp files."""
        catalog_path = tmp_path / "agents.json"
        manager = CatalogManager(catalog_path)

        # Add agent
        agent_file = tmp_path / "test-agent.md"
        agent_file.write_text("# Test")
        entry = AgentCatalogEntry(
            name="test-agent",
            description="Test",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=agent_file,
            metadata={},
        )
        manager.add_agent(entry)

        # Check for temp files
        temp_files = list(tmp_path.glob("*.tmp"))
        json_temp_files = list(tmp_path.glob("*.json.*"))

        assert len(temp_files) == 0, "Found .tmp files after write"
        # Allow .bak files but not other temp files
        assert all(f.suffix == ".bak" for f in json_temp_files), "Found unexpected temp files"

    def test_corrupted_json_recovery(self, tmp_path):
        """Test handling of corrupted JSON file."""
        catalog_path = tmp_path / "agents.json"

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
        manager = CatalogManager(tmp_path / "agents.json")

        # Add agents across different scopes, models, and templates
        for i, (name, scope, model, template) in enumerate(
            [
                ("agent1", ScopeType.GLOBAL, ModelType.HAIKU, "basic"),
                ("agent2", ScopeType.GLOBAL, ModelType.HAIKU, "basic"),
                ("agent3", ScopeType.PROJECT, ModelType.SONNET, "advanced"),
                ("agent4", ScopeType.PROJECT, ModelType.OPUS, "custom"),
                ("agent5", ScopeType.LOCAL, ModelType.OPUS, "custom"),
            ]
        ):
            agent_file = tmp_path / f"{name}.md"
            agent_file.write_text(f"# {name}")
            entry = AgentCatalogEntry(
                name=name,
                description=f"Agent {i}",
                scope=scope,
                model=model,
                path=agent_file,
                metadata={"template": template},
            )
            manager.add_agent(entry)

        # Get stats
        stats = manager.get_catalog_stats()

        # Verify totals
        assert stats["total"] == 5

        # Verify by-scope counts
        assert stats["by_scope"]["global"] == 2
        assert stats["by_scope"]["project"] == 2
        assert stats["by_scope"]["local"] == 1

        # Verify by-model counts
        assert stats["by_model"][ModelType.HAIKU.value] == 2
        assert stats["by_model"][ModelType.SONNET.value] == 1
        assert stats["by_model"][ModelType.OPUS.value] == 2

        # Verify by-template counts
        assert stats["by_template"]["basic"] == 2
        assert stats["by_template"]["advanced"] == 1
        assert stats["by_template"]["custom"] == 2


class TestPerformance:
    """Test performance requirements."""

    def test_operations_under_100ms(self, tmp_path):
        """Test all operations complete in < 100ms."""
        manager = CatalogManager(tmp_path / "agents.json")

        # Create agent entry
        agent_file = tmp_path / "perf-test.md"
        agent_file.write_text("# Perf Test")
        entry = AgentCatalogEntry(
            name="perf-test",
            description="Performance test agent",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            path=agent_file,
            metadata={"template": "basic"},
        )

        # Test add_agent
        start = time.perf_counter()
        manager.add_agent(entry)
        add_time = (time.perf_counter() - start) * 1000
        assert add_time < 100, f"add_agent took {add_time:.2f}ms"

        # Test get_agent
        start = time.perf_counter()
        manager.get_agent(agent_id=entry.id)
        get_time = (time.perf_counter() - start) * 1000
        assert get_time < 100, f"get_agent took {get_time:.2f}ms"

        # Test list_agents
        start = time.perf_counter()
        manager.list_agents()
        list_time = (time.perf_counter() - start) * 1000
        assert list_time < 100, f"list_agents took {list_time:.2f}ms"

        # Test search_agents
        start = time.perf_counter()
        manager.search_agents(query="test")
        search_time = (time.perf_counter() - start) * 1000
        assert search_time < 100, f"search_agents took {search_time:.2f}ms"

        # Test update_agent
        start = time.perf_counter()
        manager.update_agent(entry.id, description="Updated")
        update_time = (time.perf_counter() - start) * 1000
        assert update_time < 100, f"update_agent took {update_time:.2f}ms"

        # Test remove_agent
        start = time.perf_counter()
        manager.remove_agent(entry.id)
        remove_time = (time.perf_counter() - start) * 1000
        assert remove_time < 100, f"remove_agent took {remove_time:.2f}ms"

        # Test get_catalog_stats
        start = time.perf_counter()
        manager.get_catalog_stats()
        stats_time = (time.perf_counter() - start) * 1000
        assert stats_time < 100, f"get_catalog_stats took {stats_time:.2f}ms"
