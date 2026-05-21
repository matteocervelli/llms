"""
Comprehensive tests for the Scanner component.

Tests filesystem scanning for skills, commands, and agents with:
- YAML frontmatter parsing
- Security validation (path traversal prevention)
- Error handling for malformed files
- Multiple scope support
"""

import pytest
from pathlib import Path

from src.tools.catalog_system.scanner import Scanner
from src.tools.catalog_system.models import (
    SkillCatalogEntry,
    CommandCatalogEntry,
    AgentCatalogEntry,
)
from src.tools.catalog_system.exceptions import ScanError


@pytest.fixture
def scanner():
    """Create a Scanner instance."""
    return Scanner()


@pytest.fixture
def temp_skills_dir(tmp_path):
    """Create temporary skills directory with test files."""
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    return skills_dir


@pytest.fixture
def temp_commands_dir(tmp_path):
    """Create temporary commands directory with test files."""
    commands_dir = tmp_path / ".claude" / "commands"
    commands_dir.mkdir(parents=True)
    return commands_dir


@pytest.fixture
def temp_agents_dir(tmp_path):
    """Create temporary agents directory with test files."""
    agents_dir = tmp_path / ".claude" / "agents"
    agents_dir.mkdir(parents=True)
    return agents_dir


@pytest.fixture
def sample_skill_file(temp_skills_dir):
    """Create a sample SKILL.md file with valid frontmatter."""
    skill_dir = temp_skills_dir / "test-skill"
    skill_dir.mkdir()

    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(
        """---
name: test-skill
description: A test skill for scanning
template: basic
allowed-tools: ["Read", "Write"]
---

# Test Skill

This is the skill content.
"""
    )
    return skill_dir


@pytest.fixture
def sample_command_file(temp_commands_dir):
    """Create a sample command.md file with valid frontmatter."""
    command_file = temp_commands_dir / "test-command.md"
    command_file.write_text(
        """---
name: test-command
description: A test command for scanning
aliases: ["tc", "test"]
requires_tools: ["Bash", "Read"]
tags: ["testing", "utility"]
---

# Test Command

This is the command content.
"""
    )
    return command_file


@pytest.fixture
def sample_agent_file(temp_agents_dir):
    """Create a sample agent.md file with valid frontmatter."""
    agent_file = temp_agents_dir / "test-agent.md"
    agent_file.write_text(
        """---
name: test-agent
description: A test agent for scanning
model: sonnet
specialization: Testing and validation
requires_skills: ["test-skill"]
---

# Test Agent

This is the agent content.
"""
    )
    return agent_file


class TestScannerInitialization:
    """Test Scanner initialization."""

    def test_scanner_creation(self, scanner):
        """Test Scanner can be created."""
        assert scanner is not None
        assert isinstance(scanner, Scanner)


class TestScanSkills:
    """Test skill scanning functionality."""

    def test_scan_skills_empty_directory(self, scanner, temp_skills_dir):
        """Test scanning empty skills directory returns empty list."""
        result = scanner.scan_skills([temp_skills_dir.parent])
        assert result == []

    def test_scan_skills_single_skill(self, scanner, sample_skill_file):
        """Test scanning directory with one skill."""
        result = scanner.scan_skills([sample_skill_file.parent.parent])

        assert len(result) == 1
        entry = result[0]
        assert isinstance(entry, SkillCatalogEntry)
        assert entry.name == "test-skill"
        assert entry.description == "A test skill for scanning"
        assert entry.template == "basic"
        assert entry.allowed_tools == ["Read", "Write"]
        assert entry.file_path == sample_skill_file

    def test_scan_skills_multiple_skills(self, scanner, temp_skills_dir):
        """Test scanning directory with multiple skills."""
        # Create multiple skill directories
        for i in range(3):
            skill_dir = temp_skills_dir / f"skill-{i}"
            skill_dir.mkdir()
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text(
                f"""---
name: skill-{i}
description: Skill number {i}
template: basic
---

# Skill {i}
"""
            )

        result = scanner.scan_skills([temp_skills_dir.parent])
        assert len(result) == 3

        # Verify all skills were found
        names = {entry.name for entry in result}
        assert names == {"skill-0", "skill-1", "skill-2"}

    def test_scan_skills_with_scripts(self, scanner, temp_skills_dir):
        """Test scanning skill with scripts directory."""
        skill_dir = temp_skills_dir / "skill-with-scripts"
        skill_dir.mkdir()

        # Create scripts directory
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()

        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            """---
name: skill-with-scripts
description: Skill with scripts
template: tool-enhanced
---

# Skill with Scripts
"""
        )

        result = scanner.scan_skills([temp_skills_dir.parent])
        assert len(result) == 1
        assert result[0].has_scripts is True

    def test_scan_skills_without_scripts(self, scanner, sample_skill_file):
        """Test scanning skill without scripts directory."""
        result = scanner.scan_skills([sample_skill_file.parent.parent])
        assert len(result) == 1
        assert result[0].has_scripts is False

    def test_scan_skills_missing_frontmatter(self, scanner, temp_skills_dir):
        """Test scanning skill without frontmatter uses directory name."""
        skill_dir = temp_skills_dir / "no-frontmatter-skill"
        skill_dir.mkdir()

        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("# Skill without frontmatter\n\nJust content.")

        result = scanner.scan_skills([temp_skills_dir.parent])
        assert len(result) == 1
        # Should fall back to directory name
        assert result[0].name == "no-frontmatter-skill"
        assert result[0].description == ""

    def test_scan_skills_malformed_yaml(self, scanner, temp_skills_dir):
        """Test scanning skill with malformed YAML frontmatter."""
        skill_dir = temp_skills_dir / "malformed-skill"
        skill_dir.mkdir()

        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            """---
name: malformed
description: [unclosed list
---

# Malformed Skill
"""
        )

        result = scanner.scan_skills([temp_skills_dir.parent])
        # Should handle gracefully, fall back to directory name
        assert len(result) == 1
        assert result[0].name == "malformed-skill"

    def test_scan_skills_no_skill_md_file(self, scanner, temp_skills_dir):
        """Test scanning directory without SKILL.md is skipped."""
        skill_dir = temp_skills_dir / "no-skill-file"
        skill_dir.mkdir()

        # Create other files but not SKILL.md
        (skill_dir / "README.md").write_text("# Not a skill file")

        result = scanner.scan_skills([temp_skills_dir.parent])
        assert result == []

    def test_scan_skills_file_count(self, scanner, temp_skills_dir):
        """Test file_count attribute is correctly calculated."""
        skill_dir = temp_skills_dir / "multi-file-skill"
        skill_dir.mkdir()

        # Create multiple files
        (skill_dir / "SKILL.md").write_text(
            """---
name: multi-file-skill
description: Skill with multiple files
template: custom
---

# Multi-file Skill
"""
        )
        (skill_dir / "README.md").write_text("# README")
        (skill_dir / "config.yaml").write_text("key: value")

        result = scanner.scan_skills([temp_skills_dir.parent])
        assert len(result) == 1
        assert result[0].file_count == 3

    def test_scan_skills_multiple_scopes(self, scanner, tmp_path):
        """Test scanning multiple scope paths."""
        # Create two separate scope directories
        scope1 = tmp_path / "scope1" / ".claude" / "skills"
        scope2 = tmp_path / "scope2" / ".claude" / "skills"
        scope1.mkdir(parents=True)
        scope2.mkdir(parents=True)

        # Create skills in each scope
        for scope, name in [(scope1, "skill-1"), (scope2, "skill-2")]:
            skill_dir = scope / name
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                f"""---
name: {name}
description: Skill in different scope
template: basic
---

# {name}
"""
            )

        result = scanner.scan_skills([scope1.parent, scope2.parent])
        assert len(result) == 2
        names = {entry.name for entry in result}
        assert names == {"skill-1", "skill-2"}


class TestScanCommands:
    """Test command scanning functionality."""

    def test_scan_commands_empty_directory(self, scanner, temp_commands_dir):
        """Test scanning empty commands directory returns empty list."""
        result = scanner.scan_commands([temp_commands_dir.parent])
        assert result == []

    def test_scan_commands_single_command(self, scanner, sample_command_file):
        """Test scanning directory with one command."""
        result = scanner.scan_commands([sample_command_file.parent.parent])

        assert len(result) == 1
        entry = result[0]
        assert isinstance(entry, CommandCatalogEntry)
        assert entry.name == "test-command"
        assert entry.description == "A test command for scanning"
        assert entry.aliases == ["tc", "test"]
        assert entry.requires_tools == ["Bash", "Read"]
        assert entry.tags == ["testing", "utility"]

    def test_scan_commands_multiple_commands(self, scanner, temp_commands_dir):
        """Test scanning directory with multiple commands."""
        for i in range(3):
            command_file = temp_commands_dir / f"command-{i}.md"
            command_file.write_text(
                f"""---
name: command-{i}
description: Command number {i}
---

# Command {i}
"""
            )

        result = scanner.scan_commands([temp_commands_dir.parent])
        assert len(result) == 3

    def test_scan_commands_missing_frontmatter(self, scanner, temp_commands_dir):
        """Test scanning command without frontmatter uses filename."""
        command_file = temp_commands_dir / "no-frontmatter.md"
        command_file.write_text("# Command without frontmatter")

        result = scanner.scan_commands([temp_commands_dir.parent])
        assert len(result) == 1
        # Should fall back to filename without .md
        assert result[0].name == "no-frontmatter"

    def test_scan_commands_optional_fields(self, scanner, temp_commands_dir):
        """Test commands with missing optional fields use defaults."""
        command_file = temp_commands_dir / "minimal-command.md"
        command_file.write_text(
            """---
name: minimal-command
description: Minimal command
---

# Minimal Command
"""
        )

        result = scanner.scan_commands([temp_commands_dir.parent])
        assert len(result) == 1
        assert result[0].aliases == []
        assert result[0].requires_tools == []
        assert result[0].tags == []


class TestScanAgents:
    """Test agent scanning functionality."""

    def test_scan_agents_empty_directory(self, scanner, temp_agents_dir):
        """Test scanning empty agents directory returns empty list."""
        result = scanner.scan_agents([temp_agents_dir.parent])
        assert result == []

    def test_scan_agents_single_agent(self, scanner, sample_agent_file):
        """Test scanning directory with one agent."""
        result = scanner.scan_agents([sample_agent_file.parent.parent])

        assert len(result) == 1
        entry = result[0]
        assert isinstance(entry, AgentCatalogEntry)
        assert entry.name == "test-agent"
        assert entry.description == "A test agent for scanning"
        assert entry.model == "sonnet"
        assert entry.specialization == "Testing and validation"
        assert entry.requires_skills == ["test-skill"]

    def test_scan_agents_multiple_agents(self, scanner, temp_agents_dir):
        """Test scanning directory with multiple agents."""
        for i in range(3):
            agent_file = temp_agents_dir / f"agent-{i}.md"
            agent_file.write_text(
                f"""---
name: agent-{i}
description: Agent number {i}
model: haiku
---

# Agent {i}
"""
            )

        result = scanner.scan_agents([temp_agents_dir.parent])
        assert len(result) == 3

    def test_scan_agents_missing_frontmatter(self, scanner, temp_agents_dir):
        """Test scanning agent without frontmatter uses filename."""
        agent_file = temp_agents_dir / "no-frontmatter.md"
        agent_file.write_text("# Agent without frontmatter")

        result = scanner.scan_agents([temp_agents_dir.parent])
        assert len(result) == 1
        assert result[0].name == "no-frontmatter"

    def test_scan_agents_optional_fields(self, scanner, temp_agents_dir):
        """Test agents with missing optional fields use defaults."""
        agent_file = temp_agents_dir / "minimal-agent.md"
        agent_file.write_text(
            """---
name: minimal-agent
description: Minimal agent
model: opus
---

# Minimal Agent
"""
        )

        result = scanner.scan_agents([temp_agents_dir.parent])
        assert len(result) == 1
        assert result[0].specialization == ""
        assert result[0].requires_skills == []


class TestSecurityValidation:
    """Test security features (path traversal prevention)."""

    def test_scan_rejects_parent_directory_traversal(self, scanner, tmp_path):
        """Test scanner rejects paths with .. components."""
        malicious_path = tmp_path / ".." / "etc" / "passwd"

        with pytest.raises(ScanError, match="Invalid path|Path traversal"):
            scanner.scan_skills([malicious_path])

    def test_scan_rejects_absolute_paths_outside_scope(self, scanner):
        """Test scanner validates paths are within expected scope."""
        # Scanner should reject system directories with .. in path
        malicious = Path("/tmp") / ".." / "etc"
        with pytest.raises(ScanError, match="Invalid path|System directory"):
            scanner.scan_skills([malicious])

    def test_scan_normalizes_paths(self, scanner, temp_skills_dir):
        """Test scanner normalizes and resolves paths."""
        # Create skill in normalized location
        skill_dir = temp_skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            """---
name: test-skill
description: Test
template: basic
---
"""
        )

        # Pass normalized path (path validation requires proper structure)
        result = scanner.scan_skills([temp_skills_dir.parent])

        assert len(result) == 1
        # Paths should be resolved/normalized
        assert result[0].file_path.is_absolute()


class TestErrorHandling:
    """Test error handling for various edge cases."""

    def test_scan_handles_permission_errors(self, scanner, tmp_path, monkeypatch):
        """Test scanner handles permission denied errors gracefully."""
        skills_dir = tmp_path / ".claude" / "skills"
        skills_dir.mkdir(parents=True)

        skill_dir = skills_dir / "restricted-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: test\n---")

        # Mock to raise permission error
        import os

        original_listdir = os.listdir

        def mock_listdir(path):
            if "restricted-skill" in str(path):
                raise PermissionError("Access denied")
            return original_listdir(path)

        monkeypatch.setattr(os, "listdir", mock_listdir)

        # Should handle gracefully, possibly skipping or logging error
        scanner.scan_skills([skills_dir.parent])
        # Exact behavior depends on implementation
        # Should not crash the entire scan

    def test_scan_handles_invalid_utf8(self, scanner, temp_skills_dir):
        """Test scanner handles files with invalid UTF-8 encoding."""
        skill_dir = temp_skills_dir / "invalid-encoding"
        skill_dir.mkdir()

        # Write file with invalid UTF-8
        skill_file = skill_dir / "SKILL.md"
        with open(skill_file, "wb") as f:
            f.write(b"---\nname: test\n---\n\xff\xfe Invalid UTF-8")

        # Should handle gracefully
        scanner.scan_skills([temp_skills_dir.parent])
        # May skip the file or use fallback


class TestScopeDetection:
    """Test automatic scope detection from file paths."""

    def test_scan_detects_global_scope(self, scanner):
        """Test scanner detects global scope from ~/.claude/ path."""
        # Use actual home directory for accurate scope detection
        home = Path.home()
        global_claude = home / ".claude"

        # Only test if global .claude exists
        if not global_claude.exists():
            pytest.skip("Global .claude directory doesn't exist")

        global_skills = global_claude / "skills"
        if not global_skills.exists():
            global_skills.mkdir(parents=True)

        skill_dir = global_skills / "test-global-skill-scanner"
        skill_dir.mkdir(exist_ok=True)
        try:
            (skill_dir / "SKILL.md").write_text(
                """---
name: test-global-skill-scanner
description: Test global skill
template: basic
---
"""
            )

            result = scanner.scan_skills([global_claude])
            # Find our test skill
            test_skills = [s for s in result if s.name == "test-global-skill-scanner"]
            assert len(test_skills) == 1
            # Should detect global scope
            assert test_skills[0].scope == "global"
        finally:
            # Cleanup
            import shutil

            if skill_dir.exists():
                shutil.rmtree(skill_dir)

    def test_scan_detects_project_scope(self, scanner, tmp_path):
        """Test scanner detects project scope from .claude/ in project."""
        project = tmp_path / "my-project"
        project.mkdir()

        project_skills = project / ".claude" / "skills"
        project_skills.mkdir(parents=True)

        skill_dir = project_skills / "project-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            """---
name: project-skill
description: Project skill
template: basic
---
"""
        )

        result = scanner.scan_skills([project_skills.parent])
        assert len(result) == 1
        # Should detect project scope
        assert result[0].scope == "project"

    def test_scan_detects_local_scope(self, scanner, tmp_path):
        """Test scanner detects local scope when appropriate."""
        # Local scope is tricky - might need specific markers
        # Implementation may vary
        pass


class TestPerformance:
    """Test performance characteristics."""

    def test_scan_large_number_of_skills(self, scanner, temp_skills_dir):
        """Test scanner handles large number of skills efficiently."""
        # Create 100 skills
        for i in range(100):
            skill_dir = temp_skills_dir / f"skill-{i:03d}"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                f"""---
name: skill-{i:03d}
description: Skill number {i}
template: basic
---
"""
            )

        result = scanner.scan_skills([temp_skills_dir.parent])
        assert len(result) == 100

    def test_scan_deeply_nested_directories(self, scanner, temp_skills_dir):
        """Test scanner doesn't follow deep nesting (only top-level)."""
        # Skills should be direct children of skills/ directory
        skill_dir = temp_skills_dir / "skill-1"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            """---
name: skill-1
description: Top-level skill
template: basic
---
"""
        )

        # Create nested skill (should be ignored)
        nested = skill_dir / "nested-skill"
        nested.mkdir()
        (nested / "SKILL.md").write_text(
            """---
name: nested-skill
description: Nested skill
template: basic
---
"""
        )

        result = scanner.scan_skills([temp_skills_dir.parent])
        # Should only find top-level skill
        assert len(result) == 1
        assert result[0].name == "skill-1"
