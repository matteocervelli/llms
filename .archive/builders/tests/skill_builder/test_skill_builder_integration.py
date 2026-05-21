"""Integration tests for skill_builder - end-to-end workflows.

Tests complete workflows: create → list → validate → delete cycles.
"""

import json
from pathlib import Path

import pytest

from src.core.scope_manager import ScopeManager
from src.tools.skill_builder.builder import SkillBuilder
from src.tools.skill_builder.catalog import CatalogManager
from src.tools.skill_builder.models import ScopeType, SkillConfig
from src.tools.skill_builder.templates import TemplateManager
from src.tools.skill_builder.validator import SkillValidator


class TestEndToEndSkillCreation:
    """Test complete skill creation workflow."""

    def test_create_list_validate_delete_workflow(self, tmp_path):
        """Test full workflow: create → list → validate → delete."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        claude_dir = project_root / ".claude"
        claude_dir.mkdir()
        skills_dir = claude_dir / "skills"
        skills_dir.mkdir()
        catalog_path = project_root / "catalog.json"

        # Initialize components
        scope_manager = ScopeManager(project_root=project_root)
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # 1. CREATE skill
        config = SkillConfig(
            name="integration-test-skill",
            description="Integration test skill. Use when testing workflows.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        result = builder.build_skill(config)
        assert result.success
        assert result.skill_path.exists()
        assert (result.skill_path / "SKILL.md").exists()

        # 2. LIST skills via catalog
        skills = catalog_manager.list_skills()
        assert len(skills) == 1
        assert skills[0].name == "integration-test-skill"

        # 3. VALIDATE skill
        is_valid = validator.validate_skill_directory(result.skill_path)
        assert is_valid

        # 4. DELETE skill
        delete_result = builder.delete_skill("integration-test-skill", ScopeType.PROJECT)
        assert delete_result.success
        assert not result.skill_path.exists()

        # Verify catalog updated
        skills = catalog_manager.list_skills()
        assert len(skills) == 0

    def test_create_update_workflow(self, tmp_path):
        """Test create → update workflow."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        claude_dir = project_root / ".claude"
        claude_dir.mkdir()
        skills_dir = claude_dir / "skills"
        skills_dir.mkdir()
        catalog_path = project_root / "catalog.json"

        scope_manager = ScopeManager(project_root=project_root)
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # 1. CREATE skill
        config = SkillConfig(
            name="update-test-skill",
            description="Original description. Use for testing.",
            scope=ScopeType.PROJECT,
            template="basic",
        )
        create_result = builder.build_skill(config)
        assert create_result.success

        # 2. UPDATE skill
        updated_config = SkillConfig(
            name="update-test-skill",
            description="Updated description. Use for updated testing.",
            scope=ScopeType.PROJECT,
            template="basic",
            allowed_tools=["Read", "Grep"],
        )
        update_result = builder.update_skill(updated_config)
        assert update_result.success

        # Verify update in catalog
        skill = catalog_manager.get_skill("update-test-skill")
        assert skill is not None
        assert skill.description == "Updated description. Use for updated testing."


class TestMultiTemplateWorkflows:
    """Test workflows with all 4 templates."""

    @pytest.mark.parametrize(
        "template_name",
        ["basic", "with_tools", "with_scripts", "advanced"],
    )
    def test_create_skill_with_each_template(self, tmp_path, template_name):
        """Test creating skills with each available template."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        claude_dir = project_root / ".claude"
        claude_dir.mkdir()
        skills_dir = claude_dir / "skills"
        skills_dir.mkdir()
        catalog_path = project_root / "catalog.json"

        scope_manager = ScopeManager(project_root=project_root)
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # Create skill
        config = SkillConfig(
            name=f"{template_name}-skill",
            description=f"Skill using {template_name} template. Use when testing.",
            scope=ScopeType.PROJECT,
            template=template_name,
            allowed_tools=["Read", "Grep"] if template_name != "basic" else None,
        )

        result = builder.build_skill(config)
        assert result.success
        assert result.skill_path.exists()
        assert (result.skill_path / "SKILL.md").exists()

        # Verify template-specific structure
        if template_name == "with_scripts":
            scripts_dir = result.skill_path / "scripts"
            assert scripts_dir.exists()
            assert scripts_dir.is_dir()


class TestMultiScopeOperations:
    """Test operations across different scopes."""

    def test_create_skills_in_all_scopes(self, tmp_path):
        """Test creating skills in global, project, and local scopes."""
        # Setup global scope (home directory)
        global_dir = tmp_path / "home" / ".claude"
        global_dir.mkdir(parents=True)
        global_skills = global_dir / "skills"
        global_skills.mkdir()

        # Setup project scope
        project_root = tmp_path / "project"
        project_root.mkdir()
        project_claude = project_root / ".claude"
        project_claude.mkdir()
        project_skills = project_claude / "skills"
        project_skills.mkdir()

        # Setup local scope
        local_claude = project_root / ".claude"
        local_skills = local_claude / "skills"
        local_skills.mkdir(exist_ok=True)

        catalog_path = project_root / "catalog.json"

        # Initialize components
        scope_manager = ScopeManager(project_root=project_root, home_dir=tmp_path / "home")
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # Create skills in each scope
        for scope in [ScopeType.GLOBAL, ScopeType.PROJECT, ScopeType.LOCAL]:
            config = SkillConfig(
                name=f"{scope.value}-skill",
                description=f"{scope.value} skill. Use for {scope.value} operations.",
                scope=scope,
                template="basic",
            )
            result = builder.build_skill(config)
            assert result.success

        # Verify all skills created
        skills = catalog_manager.list_skills()
        assert len(skills) == 3
        scopes = {skill.scope for skill in skills}
        assert scopes == {ScopeType.GLOBAL, ScopeType.PROJECT, ScopeType.LOCAL}


class TestCatalogSyncWorkflow:
    """Test catalog sync with filesystem."""

    def test_sync_adds_untracked_skills(self, tmp_path):
        """Test sync detects and adds manually created skills."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        skills_dir = project_root / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        catalog_path = project_root / "catalog.json"

        # Create manual skill (not in catalog)
        manual_skill_dir = skills_dir / "manual-skill"
        manual_skill_dir.mkdir()
        skill_file = manual_skill_dir / "SKILL.md"
        skill_file.write_text(
            """---
name: manual-skill
description: Manually created skill. Use for testing sync.
---

# Manual Skill

Created manually.
"""
        )

        # Initialize catalog (empty)
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        # Sync should detect manual skill
        added, removed = catalog_manager.sync_catalog(scope_path=skills_dir)

        assert len(added) == 1
        assert added[0] == "manual-skill"
        assert len(removed) == 0

        # Verify catalog updated
        skills = catalog_manager.list_skills()
        assert len(skills) == 1
        assert skills[0].name == "manual-skill"

    def test_sync_removes_orphaned_entries(self, tmp_path):
        """Test sync removes catalog entries for deleted skills."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        skills_dir = project_root / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        catalog_path = project_root / "catalog.json"

        scope_manager = ScopeManager(project_root=project_root)
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # Create skill via builder
        config = SkillConfig(
            name="orphan-skill",
            description="Skill to be deleted. Use for sync testing.",
            scope=ScopeType.PROJECT,
            template="basic",
        )
        result = builder.build_skill(config)
        assert result.success

        # Manually delete skill directory (not through builder)
        import shutil

        shutil.rmtree(result.skill_path)

        # Sync should detect orphaned entry
        added, removed = catalog_manager.sync_catalog(scope_path=skills_dir)

        assert len(added) == 0
        assert len(removed) == 1
        assert removed[0] == "orphan-skill"

        # Verify catalog updated
        skills = catalog_manager.list_skills()
        assert len(skills) == 0


class TestSearchAndFilterWorkflows:
    """Test search and filter operations."""

    def test_search_skills_by_query(self, tmp_path):
        """Test searching skills by text query."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        skills_dir = project_root / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        catalog_path = project_root / "catalog.json"

        scope_manager = ScopeManager(project_root=project_root)
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # Create multiple skills with different descriptions
        skills_data = [
            ("api-skill", "API integration skill. Use for REST API calls."),
            ("database-skill", "Database operations. Use for SQL queries."),
            ("testing-skill", "Testing utilities. Use for API testing."),
        ]

        for name, desc in skills_data:
            config = SkillConfig(
                name=name,
                description=desc,
                scope=ScopeType.PROJECT,
                template="basic",
            )
            builder.build_skill(config)

        # Search for "API"
        results = catalog_manager.search_skills(query="API")
        assert len(results) == 2  # api-skill and testing-skill
        names = {skill.name for skill in results}
        assert "api-skill" in names
        assert "testing-skill" in names

    def test_filter_skills_by_template(self, tmp_path):
        """Test filtering skills by template."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        skills_dir = project_root / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        catalog_path = project_root / "catalog.json"

        scope_manager = ScopeManager(project_root=project_root)
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # Create skills with different templates
        for template in ["basic", "with_tools", "with_scripts"]:
            config = SkillConfig(
                name=f"{template}-skill",
                description=f"Skill using {template}. Use for testing.",
                scope=ScopeType.PROJECT,
                template=template,
                allowed_tools=["Read"] if template != "basic" else None,
            )
            builder.build_skill(config)

        # Filter by template
        results = catalog_manager.search_skills(template="basic")
        assert len(results) == 1
        assert results[0].metadata.get("template") == "basic"


class TestStatsGeneration:
    """Test catalog statistics generation."""

    def test_generate_stats_with_multiple_skills(self, tmp_path):
        """Test generating statistics with diverse skill set."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        skills_dir = project_root / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        catalog_path = project_root / "catalog.json"

        scope_manager = ScopeManager(project_root=project_root)
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # Create diverse set of skills
        configs = [
            ("skill-1", ScopeType.PROJECT, "basic"),
            ("skill-2", ScopeType.PROJECT, "with_tools"),
            ("skill-3", ScopeType.GLOBAL, "basic"),
            ("skill-4", ScopeType.LOCAL, "with_scripts"),
        ]

        for name, scope, template in configs:
            config = SkillConfig(
                name=name,
                description=f"{name} description. Use for testing.",
                scope=scope,
                template=template,
                allowed_tools=["Read"] if template != "basic" else None,
            )
            builder.build_skill(config)

        # Generate stats
        stats = catalog_manager.get_catalog_stats()

        assert stats["total_skills"] == 4
        assert stats["by_scope"]["project"] == 2
        assert stats["by_scope"]["global"] == 1
        assert stats["by_scope"]["local"] == 1
        assert "basic" in stats["by_template"]
        assert "with_tools" in stats["by_template"]
        assert "with_scripts" in stats["by_template"]


class TestErrorRecovery:
    """Test error recovery in workflows."""

    def test_recover_from_failed_creation(self, tmp_path):
        """Test system recovers from failed skill creation."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        skills_dir = project_root / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        catalog_path = project_root / "catalog.json"

        scope_manager = ScopeManager(project_root=project_root)
        template_manager = TemplateManager()
        validator = SkillValidator()
        catalog_manager = CatalogManager(catalog_path=catalog_path)
        builder = SkillBuilder(
            scope_manager=scope_manager,
            template_manager=template_manager,
            validator=validator,
            catalog_manager=catalog_manager,
        )

        # Try to create skill with invalid name
        invalid_config = SkillConfig(
            name="invalid../../../etc/passwd",
            description="Invalid skill. Should fail.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        result = builder.build_skill(invalid_config)
        assert not result.success
        assert result.error is not None

        # Catalog should remain clean
        skills = catalog_manager.list_skills()
        assert len(skills) == 0

        # Should be able to create valid skill after failure
        valid_config = SkillConfig(
            name="valid-skill",
            description="Valid skill. Use for recovery testing.",
            scope=ScopeType.PROJECT,
            template="basic",
        )
        valid_result = builder.build_skill(valid_config)
        assert valid_result.success
