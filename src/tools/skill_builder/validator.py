"""
Validation logic for skill_builder tool.

This module provides security-first validation for skill names, descriptions,
allowed tools, and file paths. All validation methods return (bool, str) tuples
with validation status and error/success messages.

Security Focus:
- Path traversal prevention
- Input sanitization
- Whitelist validation for tools
- Length and format checks
"""

import re
from pathlib import Path
from typing import List, Optional, Tuple


class SkillValidator:
    """
    Validator for skill configuration and security checks.

    Provides static methods for validating skill names, descriptions,
    allowed tools, template names, and file paths with security focus.
    """

    # Claude Code available tools (whitelist)
    # Source: Claude Code documentation
    ALLOWED_TOOLS = {
        "Read",
        "Write",
        "Edit",
        "Bash",
        "Grep",
        "Glob",
        "Task",
        "WebFetch",
        "WebSearch",
        "TodoWrite",
        "Skill",
        "SlashCommand",
        "NotebookEdit",
        "BashOutput",
        "KillShell",
        "ListMcpResourcesTool",
        "ReadMcpResourceTool",
    }

    # Skill name pattern: lowercase, numbers, hyphens only
    SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")

    # Template name pattern: lowercase, numbers, underscores, hyphens
    TEMPLATE_NAME_PATTERN = re.compile(r"^[a-z0-9_-]+$")

    @staticmethod
    def validate_skill_name(name: str) -> Tuple[bool, str]:
        """
        Validates skill name follows pattern: ^[a-z0-9-]{1,64}$

        Security: Prevents path traversal, special characters, and ensures
        the name is safe for filesystem operations.

        Args:
            name: Skill name to validate

        Returns:
            Tuple of (is_valid, message)
            - (True, "Valid skill name") if valid
            - (False, error_message) if invalid

        Examples:
            >>> SkillValidator.validate_skill_name("pdf-processor")
            (True, "Valid skill name")
            >>> SkillValidator.validate_skill_name("Invalid Name")
            (False, "Name must contain only lowercase letters, numbers, and hyphens")
        """
        # Check empty or length
        if not name or len(name) < 1:
            return False, "Name cannot be empty"

        if len(name) > 64:
            return False, "Name must be 1-64 characters"

        # Check pattern
        if not SkillValidator.SKILL_NAME_PATTERN.match(name):
            return False, ("Name must contain only lowercase letters, numbers, and hyphens")

        # Security: Check for leading/trailing hyphens
        if name.startswith("-") or name.endswith("-"):
            return False, "Name cannot start or end with hyphen"

        # Security: Check for consecutive hyphens
        if "--" in name:
            return False, "Name cannot contain consecutive hyphens"

        # Security: Explicit path traversal check
        if ".." in name or "/" in name or "\\" in name:
            return False, "Name cannot contain path separators or '..')"

        return True, "Valid skill name"

    @staticmethod
    def validate_description(description: str) -> Tuple[bool, str]:
        """
        Validates description (max 1024 chars, must include usage context).

        The description should explain both what the skill does AND when
        Claude should use it. This is critical for skill discovery.

        Args:
            description: Skill description to validate

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> SkillValidator.validate_description("Process PDFs. Use when working with PDF files.")
            (True, "Valid description")
            >>> SkillValidator.validate_description("Process PDFs.")
            (False, "Description should include when to use this skill...")
        """
        # Check empty
        if not description or len(description.strip()) == 0:
            return False, "Description cannot be empty"

        # Check length
        if len(description) > 1024:
            return False, "Description must be 1024 characters or less"

        # Check for usage context keywords
        usage_keywords = ["when", "use", "for", "during", "if", "while"]
        has_usage_context = any(keyword in description.lower() for keyword in usage_keywords)

        if not has_usage_context:
            return False, (
                "Description should include when to use this skill "
                "(e.g., 'Use when...', 'for processing...', 'if working with...')"
            )

        return True, "Valid description"

    @staticmethod
    def validate_allowed_tools(tools: Optional[List[str]]) -> Tuple[bool, str]:
        """
        Validates allowed-tools against whitelist.

        Security: Prevents arbitrary tool names and ensures only known
        Claude Code tools are specified.

        Args:
            tools: Optional list of tool names

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> SkillValidator.validate_allowed_tools(["Read", "Grep"])
            (True, "Valid tools: Read, Grep")
            >>> SkillValidator.validate_allowed_tools(["InvalidTool"])
            (False, "Invalid tools: InvalidTool")
        """
        if tools is None:
            return True, "No tools specified (all allowed)"

        if not isinstance(tools, list):
            return False, "Allowed tools must be a list"

        if len(tools) == 0:
            return True, "Empty tools list (all allowed)"

        # Check for invalid tools
        invalid_tools = [t for t in tools if t not in SkillValidator.ALLOWED_TOOLS]

        if invalid_tools:
            return False, f"Invalid tools: {', '.join(invalid_tools)}"

        return True, f"Valid tools: {', '.join(tools)}"

    @staticmethod
    def validate_template_name(name: str) -> Tuple[bool, str]:
        """
        Validates template name (alphanumeric, underscores, hyphens only).

        Security: Prevents path traversal and ensures template name is
        safe for filesystem operations.

        Args:
            name: Template name to validate

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> SkillValidator.validate_template_name("basic")
            (True, "Valid template name")
            >>> SkillValidator.validate_template_name("../../../etc/passwd")
            (False, "Template name cannot contain path separators")
        """
        if not name:
            return False, "Template name cannot be empty"

        # Check pattern
        if not SkillValidator.TEMPLATE_NAME_PATTERN.match(name):
            return False, (
                "Template name must contain only lowercase letters, numbers, "
                "underscores, and hyphens"
            )

        # Security: Prevent path traversal
        if ".." in name or "/" in name or "\\" in name:
            return False, "Template name cannot contain path separators"

        return True, "Valid template name"

    @staticmethod
    def validate_path_security(path: Path, base_dir: Path) -> Tuple[bool, str]:
        """
        Ensures path is within base directory.

        Security: Prevents path traversal attacks by verifying the resolved
        path is relative to the base directory.

        Args:
            path: Path to validate
            base_dir: Base directory that path must be within

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> base = Path("/safe/dir")
            >>> SkillValidator.validate_path_security(base / "skill", base)
            (True, "Path is secure")
            >>> SkillValidator.validate_path_security(Path("/etc/passwd"), base)
            (False, "Path is outside allowed directory")
        """
        try:
            resolved_path = path.resolve()
            resolved_base = base_dir.resolve()

            # Check if path is relative to base
            if not resolved_path.is_relative_to(resolved_base):
                return False, "Path is outside allowed directory"

            return True, "Path is secure"

        except Exception as e:
            return False, f"Path validation error: {str(e)}"

    @staticmethod
    def validate_frontmatter_keys(frontmatter: dict) -> Tuple[bool, str]:
        """
        Validates frontmatter keys are safe.

        Security: Ensures frontmatter keys don't contain special characters
        that could cause YAML parsing issues.

        Args:
            frontmatter: Dictionary of frontmatter keys/values

        Returns:
            Tuple of (is_valid, message)
        """
        if not frontmatter:
            return True, "No frontmatter to validate"

        # Pattern for safe keys: alphanumeric, underscores, hyphens
        safe_key_pattern = re.compile(r"^[a-zA-Z0-9_-]+$")

        invalid_keys = [key for key in frontmatter.keys() if not safe_key_pattern.match(str(key))]

        if invalid_keys:
            return False, f"Invalid frontmatter keys: {', '.join(invalid_keys)}"

        return True, "Valid frontmatter keys"

    @staticmethod
    def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
        """
        Sanitizes a string by removing/escaping dangerous characters.

        Args:
            value: String to sanitize
            max_length: Optional maximum length

        Returns:
            Sanitized string

        Examples:
            >>> SkillValidator.sanitize_string("Hello\\nWorld")
            'Hello World'
        """
        if not value:
            return ""

        # Remove control characters except whitespace
        sanitized = "".join(char if char.isprintable() or char.isspace() else "" for char in value)

        # Normalize whitespace
        sanitized = " ".join(sanitized.split())

        # Trim to max length if specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized

    @staticmethod
    def is_safe_filename(filename: str) -> Tuple[bool, str]:
        """
        Checks if filename is safe for filesystem operations.

        Security: Prevents special characters, path traversal, and reserved names.

        Args:
            filename: Filename to check

        Returns:
            Tuple of (is_safe, message)

        Examples:
            >>> SkillValidator.is_safe_filename("SKILL.md")
            (True, "Safe filename")
            >>> SkillValidator.is_safe_filename("../../../etc/passwd")
            (False, "Filename contains path traversal")
        """
        if not filename:
            return False, "Filename cannot be empty"

        # Check for path traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            return False, "Filename contains path traversal"

        # Check for reserved names (Windows)
        reserved_names = {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        }

        name_without_ext = filename.split(".")[0].upper()
        if name_without_ext in reserved_names:
            return False, f"Filename '{filename}' is a reserved name"

        # Check for special characters (allow alphanumeric, hyphen, underscore, dot)
        if not re.match(r"^[a-zA-Z0-9._-]+$", filename):
            return False, "Filename contains invalid characters"

        return True, "Safe filename"
