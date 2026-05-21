"""
Integration tests for LLM adapter with ScopeManager.

This test suite verifies that the LLM adapter integrates correctly with the
ScopeManager system, testing real-world workflows with temporary file systems.

Test Coverage:
    - Integration with ScopeManager scope detection
    - End-to-end skill/command/agent creation across all scopes
    - Multi-scope workflows (global, project, local)
    - Real filesystem operations with temp directories

Run tests:
    pytest tests/test_adapter_integration.py -v
    pytest tests/test_adapter_integration.py --cov
"""

import pytest
from pathlib import Path

from src.core.llm_adapter import ClaudeAdapter
from src.core.scope_manager import ScopeManager, ScopeType
from src.core.adapter_models import ElementType


class TestScopeManagerIntegration:
    """Test suite for ScopeManager integration."""

    def test_create_skill_with_auto_detected_scope(self, tmp_path):
        """Test skill creation with auto-detected scope."""
        # Set up project structure
        project_root = tmp_path / "project"
        project_root.mkdir()
        (project_root / ".git").mkdir()
        claude_dir = project_root / ".claude"
        claude_dir.mkdir()

        # Use ScopeManager to detect scope
        manager = ScopeManager(cwd=project_root)
        scope_config = manager.get_effective_scope()

        # Create adapter and skill
        adapter = ClaudeAdapter(scope_config)
        result = adapter.create_skill(
            name="auto-detected",
            description="Skill with auto-detected scope",
            content="Implementation",
        )

        assert result.success is True
        assert result.path.exists()
        assert scope_config.type == ScopeType.PROJECT

    def test_create_skill_with_global_flag(self, tmp_path):
        """Test skill creation with explicit global flag."""
        # Set up global directory
        global_dir = tmp_path / ".claude"
        global_dir.mkdir()

        # Override home directory for testing
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(Path, "home", lambda: tmp_path)

            manager = ScopeManager()
            scope_config = manager.get_effective_scope("--global")

            adapter = ClaudeAdapter(scope_config)
            result = adapter.create_skill(
                name="global-skill",
                description="Global scope skill",
                content="Implementation",
            )

            assert result.success is True
            assert scope_config.type == ScopeType.GLOBAL
            assert "global-skill.md" in str(result.path)

    def test_create_skill_with_project_flag(self, tmp_path):
        """Test skill creation with explicit project flag."""
        # Set up project structure
        project_root = tmp_path / "project"
        project_root.mkdir()
        (project_root / ".git").mkdir()
        claude_dir = project_root / ".claude"
        claude_dir.mkdir()

        manager = ScopeManager(cwd=project_root)
        scope_config = manager.get_effective_scope("--project")

        adapter = ClaudeAdapter(scope_config)
        result = adapter.create_skill(
            name="project-skill",
            description="Project scope skill",
            content="Implementation",
        )

        assert result.success is True
        assert scope_config.type == ScopeType.PROJECT
        assert "project-skill.md" in str(result.path)
        assert str(project_root) in str(result.path)


class TestEndToEndWorkflows:
    """Test suite for end-to-end workflows."""

    @pytest.fixture
    def project_setup(self, tmp_path):
        """Fixture providing a complete project setup."""
        # Create project structure
        project_root = tmp_path / "test-project"
        project_root.mkdir()
        (project_root / ".git").mkdir()
        claude_dir = project_root / ".claude"
        claude_dir.mkdir()

        return {
            "root": project_root,
            "claude_dir": claude_dir,
        }

    def test_create_multiple_skills_same_scope(self, project_setup):
        """Test creating multiple skills in the same scope."""
        manager = ScopeManager(cwd=project_setup["root"])
        scope_config = manager.get_effective_scope()
        adapter = ClaudeAdapter(scope_config)

        # Create multiple skills
        skill_names = ["skill1", "skill2", "skill3"]
        results = []

        for name in skill_names:
            result = adapter.create_skill(
                name=name,
                description=f"Test skill {name}",
                content=f"Implementation for {name}",
            )
            results.append(result)

        # Verify all created successfully
        assert all(r.success for r in results)
        assert len(results) == 3

        # Verify all files exist
        skills_dir = project_setup["claude_dir"] / "skills"
        assert skills_dir.exists()
        assert len(list(skills_dir.glob("*.md"))) == 3

    def test_create_skill_command_agent_same_scope(self, project_setup):
        """Test creating skill, command, and agent in the same scope."""
        manager = ScopeManager(cwd=project_setup["root"])
        scope_config = manager.get_effective_scope()
        adapter = ClaudeAdapter(scope_config)

        # Create one of each element type
        skill_result = adapter.create_skill(
            name="test-skill",
            description="Test skill",
            content="Skill implementation",
        )

        command_result = adapter.create_command(
            name="test-command",
            description="Test command",
            content="Command implementation",
        )

        agent_result = adapter.create_agent(
            name="test-agent",
            description="Test agent",
            content="Agent implementation",
        )

        # Verify all created successfully
        assert skill_result.success is True
        assert command_result.success is True
        assert agent_result.success is True

        # Verify correct directories were created
        assert (project_setup["claude_dir"] / "skills" / "test-skill.md").exists()
        assert (project_setup["claude_dir"] / "commands" / "test-command.md").exists()
        assert (project_setup["claude_dir"] / "agents" / "test-agent.md").exists()

    def test_cross_scope_workflow(self, tmp_path):
        """Test creating elements across different scopes."""
        # Set up global and project scopes
        global_dir = tmp_path / ".claude"
        global_dir.mkdir()

        project_root = tmp_path / "project"
        project_root.mkdir()
        (project_root / ".git").mkdir()
        project_claude = project_root / ".claude"
        project_claude.mkdir()

        # Override home directory
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(Path, "home", lambda: tmp_path)

            # Create global skill
            global_manager = ScopeManager()
            global_scope = global_manager.get_effective_scope("--global")
            global_adapter = ClaudeAdapter(global_scope)

            global_result = global_adapter.create_skill(
                name="global-skill",
                description="Global skill",
                content="Global implementation",
            )

            # Create project skill
            project_manager = ScopeManager(cwd=project_root)
            project_scope = project_manager.get_effective_scope("--project")
            project_adapter = ClaudeAdapter(project_scope)

            project_result = project_adapter.create_skill(
                name="project-skill",
                description="Project skill",
                content="Project implementation",
            )

            # Verify both created successfully
            assert global_result.success is True
            assert project_result.success is True

            # Verify they're in different locations
            assert str(global_dir) in str(global_result.path)
            assert str(project_claude) in str(project_result.path)
            assert global_result.path != project_result.path


class TestRealFilesystemOperations:
    """Test suite for real filesystem operations."""

    def test_file_persistence(self, tmp_path):
        """Test that created files persist correctly."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        scope_config = ScopeManager(cwd=tmp_path).get_effective_scope()
        adapter = ClaudeAdapter(scope_config)

        # Create skill
        result = adapter.create_skill(
            name="persistent",
            description="Test persistence",
            content="Content that should persist",
        )

        # Read file directly from filesystem
        file_path = result.path
        assert file_path.exists()

        content = file_path.read_text(encoding="utf-8")
        assert "# persistent" in content
        assert "Test persistence" in content
        assert "Content that should persist" in content

    def test_file_overwrite_preserves_no_other_files(self, tmp_path):
        """Test that overwriting a file doesn't affect other files."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        scope_config = ScopeManager(cwd=tmp_path).get_effective_scope()
        adapter = ClaudeAdapter(scope_config)

        # Create two skills
        adapter.create_skill(name="skill1", description="Skill 1", content="Content 1")
        adapter.create_skill(name="skill2", description="Skill 2", content="Content 2")

        # Overwrite first skill
        adapter.create_skill(
            name="skill1",
            description="Updated Skill 1",
            content="Updated Content 1",
            overwrite=True,
        )

        # Verify skill2 is unchanged
        skill2_path = claude_dir / "skills" / "skill2.md"
        skill2_content = skill2_path.read_text()
        assert "Skill 2" in skill2_content
        assert "Content 2" in skill2_content

        # Verify skill1 was updated
        skill1_path = claude_dir / "skills" / "skill1.md"
        skill1_content = skill1_path.read_text()
        assert "Updated Skill 1" in skill1_content
        assert "Updated Content 1" in skill1_content

    def test_directory_structure_created_correctly(self, tmp_path):
        """Test that directory structure is created correctly."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        scope_config = ScopeManager(cwd=tmp_path).get_effective_scope()
        adapter = ClaudeAdapter(scope_config)

        # Create one of each type
        adapter.create_skill(name="s1", description="S", content="C")
        adapter.create_command(name="c1", description="C", content="C")
        adapter.create_agent(name="a1", description="A", content="C")

        # Verify directory structure
        assert (claude_dir / "skills").is_dir()
        assert (claude_dir / "commands").is_dir()
        assert (claude_dir / "agents").is_dir()

        # Verify each has one file
        assert len(list((claude_dir / "skills").glob("*.md"))) == 1
        assert len(list((claude_dir / "commands").glob("*.md"))) == 1
        assert len(list((claude_dir / "agents").glob("*.md"))) == 1


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""

    def test_create_with_very_long_content(self, tmp_path):
        """Test creating elements with very long content."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        scope_config = ScopeManager(cwd=tmp_path).get_effective_scope()
        adapter = ClaudeAdapter(scope_config)

        # Create skill with long content
        long_content = "A" * 10000
        result = adapter.create_skill(
            name="long-content",
            description="Skill with long content",
            content=long_content,
        )

        assert result.success is True
        assert result.path.exists()

        # Verify content was written
        saved_content = result.path.read_text()
        assert len(saved_content) > 10000

    def test_create_with_unicode_content(self, tmp_path):
        """Test creating elements with Unicode content."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        scope_config = ScopeManager(cwd=tmp_path).get_effective_scope()
        adapter = ClaudeAdapter(scope_config)

        # Create skill with Unicode characters
        unicode_content = "Testing Unicode: 你好世界 🚀 café"
        result = adapter.create_skill(
            name="unicode-test",
            description="Unicode description: 日本語",
            content=unicode_content,
        )

        assert result.success is True

        # Verify Unicode was preserved
        saved_content = result.path.read_text(encoding="utf-8")
        assert "你好世界" in saved_content
        assert "🚀" in saved_content
        assert "café" in saved_content
        assert "日本語" in saved_content

    def test_create_with_newlines_in_description(self, tmp_path):
        """Test creating elements with newlines in description."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()

        scope_config = ScopeManager(cwd=tmp_path).get_effective_scope()
        adapter = ClaudeAdapter(scope_config)

        description_with_newlines = "Line 1\nLine 2\nLine 3"
        result = adapter.create_skill(
            name="multiline",
            description=description_with_newlines,
            content="Content",
        )

        assert result.success is True
        saved_content = result.path.read_text()
        assert "Line 1" in saved_content
        assert "Line 2" in saved_content
        assert "Line 3" in saved_content
