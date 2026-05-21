"""
Validation logic for agent_builder tool.

This module provides security-first validation for agent names, descriptions,
model selection, and file paths. All validation methods return (bool, str) tuples
with validation status and error/success messages.

Security Focus:
- Path traversal prevention
- Input sanitization
- Model whitelist validation
- Length and format checks
"""

import re
from pathlib import Path
from typing import List, Optional, Tuple

from .models import ModelType


class AgentValidator:
    """
    Validator for agent configuration and security checks.

    Provides static methods for validating agent names, descriptions,
    models, template names, and file paths with security focus.
    """

    # Agent name pattern: lowercase, numbers, hyphens only
    AGENT_NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")

    # Template name pattern: lowercase, numbers, underscores, hyphens
    TEMPLATE_NAME_PATTERN = re.compile(r"^[a-z0-9_-]+$")

    # Valid Claude models (from ModelType enum)
    VALID_MODELS = {model.value for model in ModelType}

    @staticmethod
    def validate_agent_name(name: str) -> Tuple[bool, str]:
        """
        Validates agent name follows pattern: ^[a-z0-9-]{1,64}$

        Security: Prevents path traversal, special characters, and ensures
        the name is safe for filesystem operations.

        Args:
            name: Agent name to validate

        Returns:
            Tuple of (is_valid, message)
            - (True, "Valid agent name") if valid
            - (False, error_message) if invalid

        Examples:
            >>> AgentValidator.validate_agent_name("plan-agent")
            (True, "Valid agent name")
            >>> AgentValidator.validate_agent_name("Invalid Name")
            (False, "Name must contain only lowercase letters, numbers, and hyphens")
        """
        # Check empty or length
        if not name or len(name) < 1:
            return False, "Name cannot be empty"

        if len(name) > 64:
            return False, "Name must be 1-64 characters"

        # Security: Explicit path traversal check (BEFORE pattern check)
        if ".." in name or "/" in name or "\\" in name:
            return False, "Name cannot contain path separators or '..'"

        # Check pattern
        if not AgentValidator.AGENT_NAME_PATTERN.match(name):
            return False, "Name must contain only lowercase letters, numbers, and hyphens"

        # Security: Check for leading/trailing hyphens
        if name.startswith("-") or name.endswith("-"):
            return False, "Name cannot start or end with hyphen"

        # Security: Check for consecutive hyphens
        if "--" in name:
            return False, "Name cannot contain consecutive hyphens"

        return True, "Valid agent name"

    @staticmethod
    def validate_description(description: str) -> Tuple[bool, str]:
        """
        Validates description (max 1024 chars, must include usage context).

        The description should explain both what the agent does AND when
        Claude should use it. This is critical for agent discovery.

        Args:
            description: Agent description to validate

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> AgentValidator.validate_description("Strategic planning. Use when defining architecture.")
            (True, "Valid description")
            >>> AgentValidator.validate_description("A planning agent.")
            (False, "Description should include when to use this agent...")
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
                "Description should include when to use this agent "
                "(e.g., 'Use when...', 'for processing...', 'if working with...')"
            )

        return True, "Valid description"

    @staticmethod
    def validate_model(model: str) -> Tuple[bool, str]:
        """
        Validates model against whitelist of supported Claude models.

        Security: Prevents arbitrary model names and ensures only known
        Claude models are specified.

        Args:
            model: Model identifier to validate

        Returns:
            Tuple of (is_valid, message)

        Examples:
            >>> AgentValidator.validate_model("claude-3-5-sonnet-20241022")
            (True, "Valid model: claude-3-5-sonnet-20241022")
            >>> AgentValidator.validate_model("gpt-4")
            (False, "Invalid model. Must be one of: ...")
        """
        if not model:
            return False, "Model cannot be empty"

        if model not in AgentValidator.VALID_MODELS:
            valid_list = ", ".join(sorted(AgentValidator.VALID_MODELS))
            return False, f"Invalid model. Must be one of: {valid_list}"

        return True, f"Valid model: {model}"

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
            >>> AgentValidator.validate_template_name("basic")
            (True, "Valid template name")
            >>> AgentValidator.validate_template_name("../../../etc/passwd")
            (False, "Template name cannot contain path separators")
        """
        if not name:
            return False, "Template name cannot be empty"

        # Security: Prevent path traversal (check BEFORE pattern check)
        if ".." in name or "/" in name or "\\" in name:
            return False, "Template name cannot contain path separators"

        # Check pattern
        if not AgentValidator.TEMPLATE_NAME_PATTERN.match(name):
            return False, (
                "Template name must contain only lowercase letters, numbers, "
                "underscores, and hyphens"
            )

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
            >>> AgentValidator.validate_path_security(base / "agent", base)
            (True, "Path is secure")
            >>> AgentValidator.validate_path_security(Path("/etc/passwd"), base)
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
    def validate_frontmatter_keys(frontmatter: Optional[dict]) -> Tuple[bool, str]:
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
            >>> AgentValidator.sanitize_string("Hello\\nWorld")
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
            >>> AgentValidator.is_safe_filename("AGENT.md")
            (True, "Safe filename")
            >>> AgentValidator.is_safe_filename("../../../etc/passwd")
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
