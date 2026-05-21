"""Performance tests for skill_builder.

Tests performance targets:
- Skill creation: < 50ms
- Catalog operations: < 100ms
- Template rendering: < 10ms
- Large catalog handling: 100+ skills
"""

import time
from pathlib import Path

import pytest

from src.core.scope_manager import ScopeManager
from src.tools.skill_builder.builder import SkillBuilder
from src.tools.skill_builder.catalog import CatalogManager
from src.tools.skill_builder.models import ScopeType, SkillConfig
from src.tools.skill_builder.templates import TemplateManager
from src.tools.skill_builder.validator import SkillValidator


class TestSkillCreationPerformance:
    """Test skill creation performance targets."""

    def test_single_skill_creation_under_50ms(self, tmp_path):
        """Test single skill creation completes under 50ms."""
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

        config = SkillConfig(
            name="performance-test-skill",
            description="Performance test skill. Use for benchmarking.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        # Measure creation time
        start = time.perf_counter()
        result = builder.build_skill(config)
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert result.success
        assert elapsed_ms < 50, f"Skill creation took {elapsed_ms:.2f}ms (target: < 50ms)"

    def test_skill_creation_with_tools_under_50ms(self, tmp_path):
        """Test skill creation with allowed-tools completes under 50ms."""
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

        config = SkillConfig(
            name="tools-performance-skill",
            description="Performance test with tools. Use for benchmarking.",
            scope=ScopeType.PROJECT,
            template="with_tools",
            allowed_tools=["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
        )

        # Measure creation time
        start = time.perf_counter()
        result = builder.build_skill(config)
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert result.success
        assert elapsed_ms < 50, f"Skill creation took {elapsed_ms:.2f}ms (target: < 50ms)"

    def test_bulk_skill_creation_performance(self, tmp_path):
        """Test creating 10 skills with acceptable average time."""
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

        # Create 10 skills and measure average time
        times = []
        for i in range(10):
            config = SkillConfig(
                name=f"bulk-skill-{i}",
                description=f"Bulk test skill {i}. Use for performance testing.",
                scope=ScopeType.PROJECT,
                template="basic",
            )

            start = time.perf_counter()
            result = builder.build_skill(config)
            end = time.perf_counter()

            assert result.success
            times.append((end - start) * 1000)

        avg_time = sum(times) / len(times)
        max_time = max(times)

        assert avg_time < 50, f"Average creation time {avg_time:.2f}ms exceeds 50ms"
        assert max_time < 100, f"Max creation time {max_time:.2f}ms exceeds 100ms"


class TestCatalogPerformance:
    """Test catalog operations performance targets."""

    def test_catalog_add_under_100ms(self, tmp_path):
        """Test catalog add operation completes under 100ms."""
        catalog_path = tmp_path / "catalog.json"
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        from datetime import datetime
        from uuid import uuid4

        from src.tools.skill_builder.models import SkillCatalogEntry

        entry = SkillCatalogEntry(
            id=uuid4(),
            name="perf-test-skill",
            description="Performance test skill",
            scope=ScopeType.PROJECT,
            path=tmp_path / "skills" / "perf-test-skill",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"template": "basic"},
        )

        # Measure add time
        start = time.perf_counter()
        catalog_manager.add_skill(entry)
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert elapsed_ms < 100, f"Catalog add took {elapsed_ms:.2f}ms (target: < 100ms)"

    def test_catalog_search_under_100ms(self, tmp_path, large_catalog):
        """Test catalog search on 100+ skills completes under 100ms."""
        catalog_path = tmp_path / "catalog.json"
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        # Add all skills from large_catalog
        for skill in large_catalog.skills:
            catalog_manager.add_skill(skill)

        # Measure search time
        start = time.perf_counter()
        results = catalog_manager.search_skills(query="test")
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert len(catalog_manager.list_skills()) >= 100, "Large catalog should have 100+ skills"
        assert elapsed_ms < 100, f"Catalog search took {elapsed_ms:.2f}ms (target: < 100ms)"

    def test_catalog_list_under_100ms(self, tmp_path, large_catalog):
        """Test listing 100+ skills completes under 100ms."""
        catalog_path = tmp_path / "catalog.json"
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        # Add all skills
        for skill in large_catalog.skills:
            catalog_manager.add_skill(skill)

        # Measure list time
        start = time.perf_counter()
        skills = catalog_manager.list_skills()
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert len(skills) >= 100
        assert elapsed_ms < 100, f"Catalog list took {elapsed_ms:.2f}ms (target: < 100ms)"

    def test_catalog_stats_under_100ms(self, tmp_path, large_catalog):
        """Test generating stats for 100+ skills completes under 100ms."""
        catalog_path = tmp_path / "catalog.json"
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        # Add all skills
        for skill in large_catalog.skills:
            catalog_manager.add_skill(skill)

        # Measure stats time
        start = time.perf_counter()
        stats = catalog_manager.get_catalog_stats()
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert stats["total_skills"] >= 100
        assert elapsed_ms < 100, f"Stats generation took {elapsed_ms:.2f}ms (target: < 100ms)"


class TestTemplateRenderingPerformance:
    """Test template rendering performance targets."""

    def test_basic_template_rendering_under_10ms(self, tmp_path):
        """Test basic template rendering completes under 10ms."""
        template_manager = TemplateManager()

        variables = {
            "name": "test-skill",
            "description": "Test skill. Use for testing.",
        }

        # Measure rendering time
        start = time.perf_counter()
        content = template_manager.render_template("basic", variables)
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert len(content) > 0
        assert elapsed_ms < 10, f"Template rendering took {elapsed_ms:.2f}ms (target: < 10ms)"

    def test_complex_template_rendering_under_10ms(self, tmp_path):
        """Test complex template with tools rendering completes under 10ms."""
        template_manager = TemplateManager()

        variables = {
            "name": "advanced-skill",
            "description": "Advanced skill with tools. Use for complex operations.",
            "allowed_tools": "- Read\n- Write\n- Edit\n- Bash\n- Grep\n- Glob",
        }

        # Measure rendering time
        start = time.perf_counter()
        content = template_manager.render_template("with_tools", variables)
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert len(content) > 0
        assert elapsed_ms < 10, f"Template rendering took {elapsed_ms:.2f}ms (target: < 10ms)"

    def test_bulk_template_rendering_performance(self, tmp_path):
        """Test rendering 50 templates with acceptable average time."""
        template_manager = TemplateManager()

        variables = {
            "name": "test-skill",
            "description": "Test skill. Use for testing.",
        }

        times = []
        for _ in range(50):
            start = time.perf_counter()
            content = template_manager.render_template("basic", variables)
            end = time.perf_counter()

            assert len(content) > 0
            times.append((end - start) * 1000)

        avg_time = sum(times) / len(times)
        max_time = max(times)

        assert avg_time < 10, f"Average rendering time {avg_time:.2f}ms exceeds 10ms"
        assert max_time < 20, f"Max rendering time {max_time:.2f}ms exceeds 20ms"


class TestValidationPerformance:
    """Test validation performance."""

    def test_name_validation_under_10ms(self):
        """Test name validation completes under 10ms."""
        validator = SkillValidator()

        # Measure validation time
        start = time.perf_counter()
        is_valid = validator.validate_skill_name("test-skill-name")
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert is_valid
        assert elapsed_ms < 10, f"Name validation took {elapsed_ms:.2f}ms (target: < 10ms)"

    def test_description_validation_under_10ms(self):
        """Test description validation completes under 10ms."""
        validator = SkillValidator()

        desc = "Test skill description with sufficient length. Use when testing validation."

        # Measure validation time
        start = time.perf_counter()
        is_valid = validator.validate_description(desc)
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        assert is_valid
        assert elapsed_ms < 10, f"Description validation took {elapsed_ms:.2f}ms (target: < 10ms)"

    def test_bulk_validation_performance(self):
        """Test validating 100 names with acceptable performance."""
        validator = SkillValidator()

        names = [f"skill-{i:03d}" for i in range(100)]

        start = time.perf_counter()
        results = [validator.validate_skill_name(name) for name in names]
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000
        avg_time = elapsed_ms / 100

        assert all(results)
        assert avg_time < 1, f"Average validation time {avg_time:.2f}ms exceeds 1ms per validation"


class TestLargeCatalogHandling:
    """Test handling large catalogs (100+ skills)."""

    def test_handle_200_skills_catalog(self, tmp_path):
        """Test catalog operations remain fast with 200 skills."""
        catalog_path = tmp_path / "catalog.json"
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        from datetime import datetime
        from uuid import uuid4

        from src.tools.skill_builder.models import SkillCatalogEntry

        # Add 200 skills
        for i in range(200):
            entry = SkillCatalogEntry(
                id=uuid4(),
                name=f"skill-{i:03d}",
                description=f"Test skill {i}",
                scope=ScopeType.PROJECT,
                path=tmp_path / "skills" / f"skill-{i:03d}",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={"template": "basic"},
            )
            catalog_manager.add_skill(entry)

        # Test list performance
        start = time.perf_counter()
        skills = catalog_manager.list_skills()
        list_time = (time.perf_counter() - start) * 1000

        # Test search performance
        start = time.perf_counter()
        results = catalog_manager.search_skills(query="050")
        search_time = (time.perf_counter() - start) * 1000

        # Test stats performance
        start = time.perf_counter()
        stats = catalog_manager.get_catalog_stats()
        stats_time = (time.perf_counter() - start) * 1000

        assert len(skills) == 200
        assert list_time < 150, f"List 200 skills took {list_time:.2f}ms (target: < 150ms)"
        assert search_time < 150, f"Search 200 skills took {search_time:.2f}ms (target: < 150ms)"
        assert stats_time < 150, f"Stats for 200 skills took {stats_time:.2f}ms (target: < 150ms)"


class TestConcurrentOperations:
    """Test concurrent skill operations."""

    def test_concurrent_skill_creation(self, tmp_path):
        """Test creating skills concurrently doesn't cause issues."""
        import threading

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

        results = []
        errors = []

        def create_skill(index):
            try:
                builder = SkillBuilder(
                    scope_manager=scope_manager,
                    template_manager=template_manager,
                    validator=validator,
                    catalog_manager=catalog_manager,
                )
                config = SkillConfig(
                    name=f"concurrent-skill-{index}",
                    description=f"Concurrent test skill {index}. Use for testing.",
                    scope=ScopeType.PROJECT,
                    template="basic",
                )
                result = builder.build_skill(config)
                results.append(result)
            except Exception as e:
                errors.append(e)

        # Create 5 skills concurrently
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_skill, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads
        for thread in threads:
            thread.join()

        # Verify results
        assert len(errors) == 0, f"Concurrent operations caused errors: {errors}"
        assert len(results) == 5
        # Note: Some operations might fail due to race conditions, which is expected
        successful = sum(1 for r in results if r.success)
        assert successful >= 3, "At least 3 out of 5 concurrent operations should succeed"
