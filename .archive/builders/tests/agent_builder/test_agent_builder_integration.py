"""Integration tests for agent_builder tool."""

from pathlib import Path

import pytest

from src.tools.agent_builder.builder import AgentBuilder
from src.tools.agent_builder.catalog import CatalogManager
from src.tools.agent_builder.models import AgentConfig, ScopeType, ModelType


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""

    def test_create_list_delete_workflow(self, tmp_path):
        """Test complete workflow: create -> list -> delete."""
        # Setup
        base_dir = tmp_path / "agents"
        base_dir.mkdir()
        catalog_path = tmp_path / "agents.json"

        builder = AgentBuilder(base_dir=base_dir)
        catalog = CatalogManager(catalog_path=catalog_path)

        # Step 1: Create agent
        config = AgentConfig(
            name="test-agent",
            description="Test agent. Use when testing integration.",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            template="basic",
        )

        entry = builder.create_agent(config)
        catalog.add_agent(entry)

        # Verify creation
        assert entry.path.exists()
        assert entry.name == "test-agent"

        # Step 2: List agents
        agents = catalog.list_agents()
        assert len(agents) == 1
        assert agents[0].name == "test-agent"

        # Step 3: Search agents
        results = catalog.search_agents(query="testing")
        assert len(results) == 1

        # Step 4: Get statistics
        stats = catalog.get_catalog_stats()
        assert stats["total"] == 1
        assert stats["by_scope"]["project"] == 1
        assert stats["by_model"][ModelType.SONNET.value] == 1

        # Step 5: Delete agent
        success = builder.delete_agent(entry.id)
        assert success is True
        assert not entry.path.exists()

        # Also remove from catalog manager
        catalog.remove_agent(entry.id)

        # Step 6: Verify deletion
        agents_after = catalog.list_agents()
        assert len(agents_after) == 0

    def test_multiple_scopes_workflow(self, tmp_path):
        """Test agents across different scopes."""
        base_dir = tmp_path / "agents"
        base_dir.mkdir()
        catalog_path = tmp_path / "agents.json"

        builder = AgentBuilder(base_dir=base_dir)
        catalog = CatalogManager(catalog_path=catalog_path)

        # Create agents in different scopes
        for i, scope in enumerate([ScopeType.GLOBAL, ScopeType.PROJECT, ScopeType.LOCAL]):
            config = AgentConfig(
                name=f"agent-{i}",
                description=f"Agent {i}. Use when testing scope {scope.value}.",
                scope=scope,
                model=ModelType.SONNET,
                template="basic",
            )
            entry = builder.create_agent(config)
            catalog.add_agent(entry)

        # List all
        all_agents = catalog.list_agents()
        assert len(all_agents) == 3

        # Filter by scope
        global_agents = catalog.list_agents(scope=ScopeType.GLOBAL)
        assert len(global_agents) == 1
        assert global_agents[0].name == "agent-0"

        project_agents = catalog.list_agents(scope=ScopeType.PROJECT)
        assert len(project_agents) == 1
        assert project_agents[0].name == "agent-1"

        local_agents = catalog.list_agents(scope=ScopeType.LOCAL)
        assert len(local_agents) == 1
        assert local_agents[0].name == "agent-2"

    def test_multiple_models_workflow(self, tmp_path):
        """Test agents with different Claude models."""
        base_dir = tmp_path / "agents"
        base_dir.mkdir()
        catalog_path = tmp_path / "agents.json"

        builder = AgentBuilder(base_dir=base_dir)
        catalog = CatalogManager(catalog_path=catalog_path)

        # Create agents with different models
        for i, model in enumerate([ModelType.HAIKU, ModelType.SONNET, ModelType.OPUS]):
            config = AgentConfig(
                name=f"agent-{model.name.lower()}",
                description=f"Agent using {model.name}. Use when testing models.",
                scope=ScopeType.PROJECT,
                model=model,
                template="basic",
            )
            entry = builder.create_agent(config)
            catalog.add_agent(entry)

        # List all
        all_agents = catalog.list_agents()
        assert len(all_agents) == 3

        # Filter by model
        haiku_agents = catalog.search_agents(model=ModelType.HAIKU)
        assert len(haiku_agents) == 1
        assert haiku_agents[0].name == "agent-haiku"

        sonnet_agents = catalog.search_agents(model=ModelType.SONNET)
        assert len(sonnet_agents) == 1
        assert sonnet_agents[0].name == "agent-sonnet"

        opus_agents = catalog.search_agents(model=ModelType.OPUS)
        assert len(opus_agents) == 1
        assert opus_agents[0].name == "agent-opus"

        # Check statistics
        stats = catalog.get_catalog_stats()
        assert stats["by_model"][ModelType.HAIKU.value] == 1
        assert stats["by_model"][ModelType.SONNET.value] == 1
        assert stats["by_model"][ModelType.OPUS.value] == 1

    def test_sync_workflow(self, tmp_path):
        """Test catalog sync with filesystem."""
        # Setup: Create agents directory structure matching expected paths
        project_root = tmp_path / "project"
        project_root.mkdir()

        base_dir = project_root / ".claude" / "agents"
        base_dir.mkdir(parents=True)

        catalog_path = project_root / "agents.json"

        catalog = CatalogManager(catalog_path=catalog_path)

        # Create agent file directly in filesystem (not in catalog yet)
        agent_file = base_dir / "orphan-agent.md"
        agent_file.write_text(
            """---
name: orphan-agent
description: Orphan agent. Use when testing orphans.
model: claude-3-5-haiku-20241022
template: basic
---
# Orphan Agent
"""
        )

        # Sync should add orphan
        report = catalog.sync_catalog(project_root)
        assert "orphan-agent" in report["added"]

        # Verify orphan is now in catalog
        orphan = catalog.get_agent(name="orphan-agent", scope=ScopeType.PROJECT)
        assert orphan is not None
        assert orphan.model == ModelType.HAIKU

    def test_update_workflow(self, tmp_path):
        """Test agent update workflow."""
        base_dir = tmp_path / "agents"
        base_dir.mkdir()
        catalog_path = tmp_path / "agents.json"

        builder = AgentBuilder(base_dir=base_dir)
        catalog = CatalogManager(catalog_path=catalog_path)

        # Create agent
        config = AgentConfig(
            name="update-test",
            description="Original description. Use when testing updates.",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            template="basic",
        )
        entry = builder.create_agent(config)
        catalog.add_agent(entry)

        # Update description
        success = catalog.update_agent(
            entry.id, description="Updated description. Use when testing modifications."
        )
        assert success is True

        # Verify update
        updated = catalog.get_agent(agent_id=entry.id)
        assert updated.description == "Updated description. Use when testing modifications."

    def test_search_workflow(self, tmp_path):
        """Test comprehensive search workflow."""
        base_dir = tmp_path / "agents"
        base_dir.mkdir()
        catalog_path = tmp_path / "agents.json"

        builder = AgentBuilder(base_dir=base_dir)
        catalog = CatalogManager(catalog_path=catalog_path)

        # Create multiple agents
        agents_data = [
            ("plan-agent", "Strategic planning. Use when defining architecture."),
            ("code-reviewer", "Code review automation. Use for pull requests."),
            ("feature-implementer", "Feature implementation. Use when building features."),
        ]

        for name, desc in agents_data:
            config = AgentConfig(
                name=name,
                description=desc,
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                template="basic",
            )
            entry = builder.create_agent(config)
            catalog.add_agent(entry)

        # Search by query
        results = catalog.search_agents(query="use")
        assert len(results) == 3  # All have "use"

        results = catalog.search_agents(query="planning")
        assert len(results) == 1
        assert results[0].name == "plan-agent"

        results = catalog.search_agents(query="review")
        assert len(results) == 1
        assert results[0].name == "code-reviewer"

        results = catalog.search_agents(query="implementation")
        assert len(results) == 1
        assert results[0].name == "feature-implementer"


class TestErrorHandling:
    """Test error handling in workflows."""

    def test_duplicate_agent_error(self, tmp_path):
        """Test error when creating duplicate agent."""
        from src.tools.agent_builder.exceptions import AgentExistsError

        base_dir = tmp_path / "agents"
        base_dir.mkdir()

        builder = AgentBuilder(base_dir=base_dir)

        config = AgentConfig(
            name="duplicate-test",
            description="Test agent. Use when testing duplicates.",
            scope=ScopeType.PROJECT,
            model=ModelType.SONNET,
            template="basic",
        )

        # First creation succeeds
        builder.create_agent(config)

        # Second creation fails
        with pytest.raises(AgentExistsError):
            builder.create_agent(config)

    def test_invalid_agent_name(self, tmp_path):
        """Test error with invalid agent name."""
        from pydantic import ValidationError

        base_dir = tmp_path / "agents"
        base_dir.mkdir()

        with pytest.raises(ValidationError):
            config = AgentConfig(
                name="Invalid Name",  # Spaces not allowed
                description="Test agent. Use when testing.",
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                template="basic",
            )

    def test_missing_description_context(self, tmp_path):
        """Test error when description lacks usage context."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError, match="should include when to use"):
            config = AgentConfig(
                name="test-agent",
                description="A test agent.",  # No "use when" context
                scope=ScopeType.PROJECT,
                model=ModelType.SONNET,
                template="basic",
            )
