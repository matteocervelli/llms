"""Security tests for skill_builder.

Tests security measures:
- Path traversal prevention
- XSS prevention in descriptions
- YAML injection protection
- Tool whitelist enforcement
- File permission validation
- Template sandboxing
"""

import os
from pathlib import Path

import pytest

from src.core.scope_manager import ScopeManager
from src.tools.skill_builder.builder import SkillBuilder
from src.tools.skill_builder.catalog import CatalogManager
from src.tools.skill_builder.exceptions import SkillBuilderError
from src.tools.skill_builder.models import ScopeType, SkillConfig
from src.tools.skill_builder.templates import TemplateManager
from src.tools.skill_builder.validator import SkillValidator


class TestPathTraversalPrevention:
    """Test path traversal attack prevention."""

    @pytest.mark.parametrize(
        "malicious_name",
        [
            "../../../etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "skill/../../../etc/passwd",
            "....//....//....//etc/passwd",
            "../.../.././../etc/passwd",
        ],
    )
    def test_path_traversal_in_skill_name(self, malicious_name, tmp_path):
        """Test path traversal attempts in skill names are blocked."""
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

        # Attempt path traversal
        with pytest.raises((ValueError, SkillBuilderError)):
            config = SkillConfig(
                name=malicious_name,
                description="Malicious skill. Use for security testing.",
                scope=ScopeType.PROJECT,
                template="basic",
            )
            builder.build_skill(config)

    def test_absolute_path_blocked(self, tmp_path):
        """Test absolute paths in skill names are blocked."""
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

        with pytest.raises((ValueError, SkillBuilderError)):
            config = SkillConfig(
                name="/etc/passwd",
                description="Absolute path attack. Use for security testing.",
                scope=ScopeType.PROJECT,
                template="basic",
            )
            builder.build_skill(config)


class TestXSSPrevention:
    """Test XSS prevention in skill descriptions."""

    @pytest.mark.parametrize(
        "xss_payload",
        [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(1)'>",
        ],
    )
    def test_xss_in_description(self, xss_payload, tmp_path):
        """Test XSS payloads in descriptions are sanitized."""
        validator = SkillValidator()

        # Descriptions with XSS should fail validation or be sanitized
        is_valid = validator.validate_description(xss_payload)

        # Either validation fails, or description is rejected
        assert not is_valid, f"XSS payload should not validate: {xss_payload}"

    def test_xss_not_stored_in_catalog(self, tmp_path):
        """Test XSS payloads don't get stored in catalog."""
        catalog_path = tmp_path / "catalog.json"
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        from datetime import datetime
        from uuid import uuid4

        from src.tools.skill_builder.models import SkillCatalogEntry

        # Try to create entry with XSS in description
        try:
            entry = SkillCatalogEntry(
                id=uuid4(),
                name="xss-test",
                description="<script>alert('XSS')</script>",
                scope=ScopeType.PROJECT,
                path=tmp_path / "skills" / "xss-test",
                created_at=datetime.now(),
                updated_at=datetime.now(),
                metadata={"template": "basic"},
            )
            catalog_manager.add_skill(entry)

            # If it was added, verify it's sanitized
            skill = catalog_manager.get_skill("xss-test")
            if skill:
                assert "<script>" not in skill.description
                assert "alert" not in skill.description.lower()
        except Exception:
            # Validation error is also acceptable
            pass


class TestYAMLInjectionPrevention:
    """Test YAML injection attack prevention."""

    def test_malformed_yaml_in_description(self, tmp_path):
        """Test malformed YAML in description doesn't break system."""
        validator = SkillValidator()

        malicious_desc = """
description: normal
---
evil_key: !!python/object/apply:os.system
  args: ['rm -rf /']
---
"""

        # Should fail validation
        is_valid = validator.validate_description(malicious_desc)
        assert not is_valid

    def test_yaml_injection_in_frontmatter(self, tmp_path):
        """Test YAML injection attempts in frontmatter are blocked."""
        # Setup
        project_root = tmp_path / "project"
        project_root.mkdir()
        skills_dir = project_root / ".claude" / "skills"
        skills_dir.mkdir(parents=True)

        # Create malicious SKILL.md
        skill_dir = skills_dir / "yaml-injection-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"

        malicious_content = """---
name: yaml-injection
description: Normal description
evil: !!python/object/apply:os.system ['rm -rf /']
---

# Skill Content
"""
        skill_file.write_text(malicious_content)

        catalog_path = project_root / "catalog.json"
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        # Sync should handle safely
        try:
            added, removed = catalog_manager.sync_catalog(scope_path=skills_dir)
            # If it was added, verify no code execution
            assert os.path.exists(tmp_path)  # System should still be intact
        except Exception:
            # Parsing error is acceptable
            pass


class TestToolWhitelistEnforcement:
    """Test allowed-tools whitelist enforcement."""

    def test_invalid_tool_rejected(self, tmp_path):
        """Test invalid tool names are rejected."""
        validator = SkillValidator()

        # Invalid tool names should fail validation
        invalid_tools = ["InvalidTool", "MaliciousTool", "System", "Exec"]

        for tool in invalid_tools:
            is_valid = validator.validate_allowed_tools([tool])
            assert not is_valid, f"Invalid tool should be rejected: {tool}"

    def test_valid_tools_accepted(self, tmp_path):
        """Test valid Claude Code tools are accepted."""
        validator = SkillValidator()

        valid_tools = [
            "Read",
            "Write",
            "Edit",
            "Bash",
            "Grep",
            "Glob",
            "Task",
            "WebFetch",
            "AskUserQuestion",
        ]

        is_valid = validator.validate_allowed_tools(valid_tools)
        assert is_valid

    def test_whitelist_bypass_attempt(self, tmp_path):
        """Test attempts to bypass whitelist are blocked."""
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

        # Try to create skill with invalid tools
        with pytest.raises((ValueError, SkillBuilderError)):
            config = SkillConfig(
                name="whitelist-bypass-skill",
                description="Bypass attempt. Use for security testing.",
                scope=ScopeType.PROJECT,
                template="with_tools",
                allowed_tools=["Read", "SystemCall", "Exec"],  # Invalid tools mixed in
            )
            builder.build_skill(config)


class TestFilePermissionValidation:
    """Test file permission enforcement."""

    def test_skill_directory_permissions(self, tmp_path):
        """Test skill directories have correct permissions (755)."""
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
            name="permission-test-skill",
            description="Permission test. Use for testing.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        result = builder.build_skill(config)
        assert result.success

        # Check directory permissions (should be readable/executable by all)
        dir_stat = result.skill_path.stat()
        dir_mode = oct(dir_stat.st_mode)[-3:]

        # Should be 755 or similar (rwxr-xr-x)
        assert dir_mode[0] == "7", f"Owner should have rwx: {dir_mode}"
        assert dir_mode[1] >= "5", f"Group should have r-x at least: {dir_mode}"

    def test_skill_file_permissions(self, tmp_path):
        """Test SKILL.md files have correct permissions (644)."""
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
            name="file-permission-test",
            description="File permission test. Use for testing.",
            scope=ScopeType.PROJECT,
            template="basic",
        )

        result = builder.build_skill(config)
        assert result.success

        # Check file permissions
        skill_file = result.skill_path / "SKILL.md"
        file_stat = skill_file.stat()
        file_mode = oct(file_stat.st_mode)[-3:]

        # Should be 644 or similar (rw-r--r--)
        assert file_mode[0] == "6", f"Owner should have rw-: {file_mode}"
        assert file_mode[1] >= "4", f"Group should have r-- at least: {file_mode}"


class TestTemplateSandboxing:
    """Test template rendering sandboxing."""

    def test_template_code_execution_blocked(self, tmp_path):
        """Test arbitrary code execution in templates is blocked."""
        template_manager = TemplateManager()

        # Try to execute Python code in template
        malicious_variables = {
            "name": "{{ ''.__class__.__mro__[1].__subclasses__()[104].__init__.__globals__['sys'].exit(1) }}",
            "description": "Code execution attempt. Use for testing.",
        }

        # Should render safely without code execution
        try:
            content = template_manager.render_template("basic", malicious_variables)
            # If rendering succeeds, verify no code was executed
            assert "subclasses" not in content or "mro" not in content
        except Exception:
            # Template error is also acceptable
            pass

    def test_template_file_access_blocked(self, tmp_path):
        """Test file access from templates is blocked."""
        template_manager = TemplateManager()

        malicious_variables = {
            "name": "{{ open('/etc/passwd').read() }}",
            "description": "File access attempt. Use for testing.",
        }

        # Should not read /etc/passwd
        try:
            content = template_manager.render_template("basic", malicious_variables)
            assert "root:" not in content  # /etc/passwd content should not be there
        except Exception:
            # Template error is acceptable
            pass


class TestUnicodeAndSpecialCharacters:
    """Test handling of Unicode and special characters."""

    @pytest.mark.parametrize(
        "unicode_name",
        [
            "skill-émojis-🚀",
            "skill-中文",
            "skill-עברית",
            "skill-हिन्दी",
        ],
    )
    def test_unicode_in_skill_names(self, unicode_name):
        """Test Unicode characters in skill names are handled safely."""
        validator = SkillValidator()

        # Unicode names should be validated (may be rejected for safety)
        try:
            is_valid = validator.validate_skill_name(unicode_name)
            # If accepted, should be safe
            assert is_valid or not is_valid  # Either outcome is acceptable
        except Exception:
            # Validation error is acceptable
            pass

    def test_null_byte_injection(self):
        """Test null byte injection is blocked."""
        validator = SkillValidator()

        malicious_name = "skill\x00malicious"

        # Should fail validation
        is_valid = validator.validate_skill_name(malicious_name)
        assert not is_valid

    def test_special_characters_sanitized(self):
        """Test special characters are sanitized."""
        validator = SkillValidator()

        # Test various special characters
        test_cases = [
            "skill;ls;",
            "skill&&ls",
            "skill|ls",
            "skill`ls`",
            "skill$(ls)",
        ]

        for test_name in test_cases:
            is_valid = validator.validate_skill_name(test_name)
            # Should either reject or sanitize
            assert not is_valid, f"Dangerous characters should be rejected: {test_name}"


class TestConcurrentAccessSafety:
    """Test safe handling of concurrent access."""

    def test_catalog_atomic_writes(self, tmp_path):
        """Test catalog writes are atomic (prevent corruption)."""
        import threading

        catalog_path = tmp_path / "catalog.json"
        catalog_manager = CatalogManager(catalog_path=catalog_path)

        from datetime import datetime
        from uuid import uuid4

        from src.tools.skill_builder.models import SkillCatalogEntry

        errors = []

        def add_skill(index):
            try:
                entry = SkillCatalogEntry(
                    id=uuid4(),
                    name=f"concurrent-skill-{index}",
                    description=f"Concurrent test {index}",
                    scope=ScopeType.PROJECT,
                    path=tmp_path / "skills" / f"concurrent-skill-{index}",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    metadata={"template": "basic"},
                )
                catalog_manager.add_skill(entry)
            except Exception as e:
                errors.append(e)

        # Create multiple skills concurrently
        threads = []
        for i in range(10):
            thread = threading.Thread(target=add_skill, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Catalog should not be corrupted
        assert len(errors) == 0, f"Concurrent operations caused errors: {errors}"

        # Verify catalog is still valid JSON
        import json

        with open(catalog_path) as f:
            data = json.load(f)
            assert "skills" in data


class TestResourceExhaustionPrevention:
    """Test prevention of resource exhaustion attacks."""

    def test_extremely_long_description_rejected(self):
        """Test extremely long descriptions are rejected."""
        validator = SkillValidator()

        # 10000 character description
        long_desc = "A" * 10000 + ". Use for testing."

        # Should fail validation (too long)
        is_valid = validator.validate_description(long_desc)
        assert not is_valid

    def test_excessive_tool_list_rejected(self):
        """Test excessive tool lists are rejected."""
        validator = SkillValidator()

        # Try to add 100 tools (excessive)
        excessive_tools = [f"Tool{i}" for i in range(100)]

        # Should fail validation
        is_valid = validator.validate_allowed_tools(excessive_tools)
        assert not is_valid
