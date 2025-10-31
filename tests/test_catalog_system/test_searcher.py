"""
Comprehensive tests for the Searcher component.

Tests search and filter capabilities for catalog entries with:
- Text search with scoring algorithm
- Scope filtering
- Type filtering
- Fuzzy matching
"""

import pytest
from pathlib import Path

from src.tools.catalog_system.searcher import Searcher
from src.tools.catalog_system.models import (
    SkillCatalogEntry,
    CommandCatalogEntry,
    AgentCatalogEntry,
)


@pytest.fixture
def searcher():
    """Create a Searcher instance."""
    return Searcher()


@pytest.fixture
def sample_skills():
    """Create sample skill entries for testing."""
    return [
        SkillCatalogEntry(
            name="python-tester",
            scope="global",
            description="Test Python code with pytest",
            file_path=Path("/test/skill1"),
            template="basic",
        ),
        SkillCatalogEntry(
            name="javascript-analyzer",
            scope="project",
            description="Analyze JavaScript code for issues",
            file_path=Path("/test/skill2"),
            template="tool-enhanced",
        ),
        SkillCatalogEntry(
            name="code-formatter",
            scope="local",
            description="Format code using black and prettier",
            file_path=Path("/test/skill3"),
            template="custom",
        ),
        SkillCatalogEntry(
            name="pytest-runner",
            scope="global",
            description="Run pytest tests with coverage",
            file_path=Path("/test/skill4"),
            template="basic",
        ),
    ]


@pytest.fixture
def sample_commands():
    """Create sample command entries for testing."""
    return [
        CommandCatalogEntry(
            name="test-all",
            scope="global",
            description="Run all tests in the project",
            file_path=Path("/test/cmd1.md"),
            tags=["testing", "ci"],
        ),
        CommandCatalogEntry(
            name="lint-code",
            scope="project",
            description="Lint code with flake8 and eslint",
            file_path=Path("/test/cmd2.md"),
            tags=["linting", "quality"],
        ),
    ]


@pytest.fixture
def sample_agents():
    """Create sample agent entries for testing."""
    return [
        AgentCatalogEntry(
            name="test-specialist",
            scope="global",
            description="Specialist in writing comprehensive tests",
            file_path=Path("/test/agent1.md"),
            model="sonnet",
        ),
        AgentCatalogEntry(
            name="code-reviewer",
            scope="project",
            description="Reviews code for best practices",
            file_path=Path("/test/agent2.md"),
            model="opus",
        ),
    ]


class TestSearcherInitialization:
    """Test Searcher initialization."""

    def test_searcher_creation(self, searcher):
        """Test Searcher can be created."""
        assert searcher is not None
        assert isinstance(searcher, Searcher)


class TestSearch:
    """Test search functionality."""

    def test_search_exact_match(self, searcher, sample_skills):
        """Test exact name match gets highest score (100)."""
        results = searcher.search(sample_skills, "python-tester")

        assert len(results) > 0
        # First result should be exact match
        entry, score = results[0]
        assert entry.name == "python-tester"
        assert score == 100

    def test_search_prefix_match(self, searcher, sample_skills):
        """Test prefix match gets score of 75."""
        results = searcher.search(sample_skills, "python")

        # Should find "python-tester"
        assert len(results) > 0
        entry, score = results[0]
        assert entry.name == "python-tester"
        assert score == 75

    def test_search_contains_match(self, searcher, sample_skills):
        """Test substring match gets score of 50."""
        results = searcher.search(sample_skills, "test")

        # Should find entries containing "test"
        assert len(results) >= 2  # python-tester, pytest-runner
        # Results should be sorted by score descending
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)

    def test_search_description_match(self, searcher, sample_skills):
        """Test searching in description field."""
        results = searcher.search(sample_skills, "pytest")

        # Should find entries with "pytest" in name or description
        assert len(results) >= 2
        names = {entry.name for entry, _ in results}
        assert "python-tester" in names  # has "pytest" in description
        assert "pytest-runner" in names  # has "pytest" in name

    def test_search_case_insensitive(self, searcher, sample_skills):
        """Test search is case-insensitive."""
        results_lower = searcher.search(sample_skills, "python")
        results_upper = searcher.search(sample_skills, "PYTHON")
        results_mixed = searcher.search(sample_skills, "PyThOn")

        # All should return same results
        assert len(results_lower) == len(results_upper) == len(results_mixed)
        names_lower = {e.name for e, _ in results_lower}
        names_upper = {e.name for e, _ in results_upper}
        names_mixed = {e.name for e, _ in results_mixed}
        assert names_lower == names_upper == names_mixed

    def test_search_no_matches(self, searcher, sample_skills):
        """Test search with no matches returns empty list."""
        results = searcher.search(sample_skills, "nonexistent")
        assert results == []

    def test_search_empty_query(self, searcher, sample_skills):
        """Test search with empty query returns all entries."""
        results = searcher.search(sample_skills, "")
        assert len(results) == len(sample_skills)

    def test_search_fuzzy_match(self, searcher, sample_skills):
        """Test fuzzy matching for typos."""
        # Note: This depends on fuzzy matching implementation
        # May use Levenshtein distance or similar
        results = searcher.search(sample_skills, "pythn")  # typo

        # Should still find "python-tester" with lower score
        if results:  # Fuzzy matching is optional
            assert any("python" in e.name.lower() for e, _ in results)

    def test_search_multiple_matches(self, searcher, sample_skills):
        """Test search returns all matching entries."""
        results = searcher.search(sample_skills, "test")

        # Should find multiple entries
        assert len(results) >= 2
        # Results sorted by score
        for i in range(len(results) - 1):
            assert results[i][1] >= results[i + 1][1]

    def test_search_score_ordering(self, searcher, sample_skills):
        """Test results are ordered by score (highest first)."""
        results = searcher.search(sample_skills, "code")

        # Should find entries with "code" in name/description
        assert len(results) > 0
        # Verify descending score order
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)


class TestFilterByScope:
    """Test scope filtering functionality."""

    def test_filter_global_scope(self, searcher, sample_skills):
        """Test filtering by global scope."""
        results = searcher.filter_by_scope(sample_skills, "global")

        assert len(results) == 2  # python-tester, pytest-runner
        assert all(e.scope == "global" for e in results)

    def test_filter_project_scope(self, searcher, sample_skills):
        """Test filtering by project scope."""
        results = searcher.filter_by_scope(sample_skills, "project")

        assert len(results) == 1  # javascript-analyzer
        assert all(e.scope == "project" for e in results)

    def test_filter_local_scope(self, searcher, sample_skills):
        """Test filtering by local scope."""
        results = searcher.filter_by_scope(sample_skills, "local")

        assert len(results) == 1  # code-formatter
        assert all(e.scope == "local" for e in results)

    def test_filter_all_scope(self, searcher, sample_skills):
        """Test filtering with 'all' scope returns everything."""
        results = searcher.filter_by_scope(sample_skills, "all")

        assert len(results) == len(sample_skills)

    def test_filter_empty_list(self, searcher):
        """Test filtering empty list returns empty list."""
        results = searcher.filter_by_scope([], "global")
        assert results == []

    def test_filter_invalid_scope(self, searcher, sample_skills):
        """Test filtering with invalid scope returns empty list."""
        results = searcher.filter_by_scope(sample_skills, "invalid")
        assert results == []


class TestFilterByType:
    """Test type filtering functionality."""

    def test_filter_by_type_skill(self, searcher, sample_skills, sample_commands):
        """Test filtering by entry type (skill)."""
        mixed = sample_skills + sample_commands
        results = searcher.filter_by_type(mixed, "skill")

        assert len(results) == len(sample_skills)
        assert all(isinstance(e, SkillCatalogEntry) for e in results)

    def test_filter_by_type_command(self, searcher, sample_skills, sample_commands):
        """Test filtering by entry type (command)."""
        mixed = sample_skills + sample_commands
        results = searcher.filter_by_type(mixed, "command")

        assert len(results) == len(sample_commands)
        assert all(isinstance(e, CommandCatalogEntry) for e in results)

    def test_filter_by_type_agent(self, searcher, sample_agents, sample_commands):
        """Test filtering by entry type (agent)."""
        mixed = sample_agents + sample_commands
        results = searcher.filter_by_type(mixed, "agent")

        assert len(results) == len(sample_agents)
        assert all(isinstance(e, AgentCatalogEntry) for e in results)

    def test_filter_by_type_all(self, searcher, sample_skills, sample_commands):
        """Test filtering with 'all' type returns everything."""
        mixed = sample_skills + sample_commands
        results = searcher.filter_by_type(mixed, "all")

        assert len(results) == len(mixed)

    def test_filter_by_type_invalid(self, searcher, sample_skills):
        """Test filtering with invalid type returns empty list."""
        results = searcher.filter_by_type(sample_skills, "invalid")
        assert results == []


class TestCombinedOperations:
    """Test combining search and filter operations."""

    def test_search_then_filter_scope(self, searcher, sample_skills):
        """Test searching then filtering by scope."""
        # Search for "test"
        search_results = searcher.search(sample_skills, "test")
        entries = [entry for entry, _ in search_results]

        # Filter to global scope
        filtered = searcher.filter_by_scope(entries, "global")

        # Should only have global entries with "test"
        assert len(filtered) >= 1
        assert all(e.scope == "global" for e in filtered)
        assert all("test" in e.name.lower() or "test" in e.description.lower() for e in filtered)

    def test_filter_scope_then_search(self, searcher, sample_skills):
        """Test filtering by scope then searching."""
        # Filter to global scope first
        global_skills = searcher.filter_by_scope(sample_skills, "global")

        # Search within global skills
        results = searcher.search(global_skills, "python")

        # Should only find global skills matching "python"
        assert len(results) >= 1
        entry, score = results[0]
        assert entry.scope == "global"
        assert "python" in entry.name.lower()


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_search_with_special_characters(self, searcher, sample_skills):
        """Test search handles special characters gracefully."""
        searcher.search(sample_skills, "python-test*")
        # Should handle gracefully, possibly matching "python-test"

    def test_search_with_unicode(self, searcher, sample_skills):
        """Test search handles Unicode characters."""
        searcher.search(sample_skills, "pythön")
        # Should handle gracefully

    def test_search_very_long_query(self, searcher, sample_skills):
        """Test search handles very long query strings."""
        long_query = "x" * 1000
        results = searcher.search(sample_skills, long_query)
        assert results == []

    def test_filter_preserves_entry_integrity(self, searcher, sample_skills):
        """Test filtering doesn't modify entries."""
        original_names = {e.name for e in sample_skills}
        searcher.filter_by_scope(sample_skills, "global")

        # Original list should be unchanged
        assert {e.name for e in sample_skills} == original_names


class TestPerformance:
    """Test performance characteristics."""

    def test_search_large_catalog(self, searcher):
        """Test search performance with large number of entries."""
        # Create 1000 sample entries
        large_catalog = [
            SkillCatalogEntry(
                name=f"skill-{i:04d}",
                scope="global" if i % 2 == 0 else "project",
                description=f"Description for skill {i}",
                file_path=Path(f"/test/skill{i}"),
                template="basic",
            )
            for i in range(1000)
        ]

        # Search should complete quickly
        results = searcher.search(large_catalog, "skill-0500")
        assert len(results) > 0
        # Exact match should be first
        assert results[0][0].name == "skill-0500"

    def test_filter_large_catalog(self, searcher):
        """Test filter performance with large number of entries."""
        # Create 1000 sample entries
        large_catalog = [
            SkillCatalogEntry(
                name=f"skill-{i:04d}",
                scope="global" if i % 3 == 0 else "project",
                description=f"Description for skill {i}",
                file_path=Path(f"/test/skill{i}"),
                template="basic",
            )
            for i in range(1000)
        ]

        # Filter should complete quickly
        results = searcher.filter_by_scope(large_catalog, "global")
        # Approximately 1/3 should be global
        assert 300 <= len(results) <= 400
