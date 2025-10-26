"""
Validation and sanitization for command builder.

Provides comprehensive validation for command names, bash commands, file references,
and other inputs with security-first design to prevent path traversal, command injection,
and other vulnerabilities.
"""

import re
from pathlib import Path
from typing import List, Tuple

from .exceptions import SecurityError, ValidationError

# Dangerous bash commands/patterns that should trigger warnings
DANGEROUS_COMMANDS = [
    "rm -rf",
    "rm -fr",
    "dd if=",
    "mkfs",
    ":(){ :|:& };:",  # Fork bomb
    "> /dev/",
    "chmod -R 777",
    "chmod 777",
    "curl",  # Can be dangerous if downloading and executing
    "wget",  # Can be dangerous if downloading and executing
]

# Safe bash commands that are commonly used
SAFE_COMMANDS = [
    "git",
    "npm",
    "yarn",
    "pnpm",
    "python",
    "python3",
    "pip",
    "uv",
    "pytest",
    "node",
    "echo",
    "cat",
    "ls",
    "grep",
    "find",
    "sed",
    "awk",
    "docker",
    "kubectl",
    "make",
    "cargo",
    "go",
    "rustc",
    "gcc",
    "clang",
]


class Validator:
    """Validator for command builder inputs with security-first design."""

    @staticmethod
    def validate_command_name(name: str) -> Tuple[bool, str]:
        """
        Validate command name follows slug format and security requirements.

        Args:
            name: Command name to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name:
            return (False, "Command name cannot be empty")

        if len(name) < 2:
            return (False, "Command name must be at least 2 characters")

        if len(name) > 50:
            return (False, "Command name must be at most 50 characters")

        # Must start and end with alphanumeric
        if not name[0].isalnum() or not name[-1].isalnum():
            return (False, "Command name must start and end with alphanumeric character")

        # Only lowercase alphanumeric and hyphens
        pattern = r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$"
        if not re.match(pattern, name):
            return (False, "Command name must be lowercase alphanumeric with hyphens (slug format)")

        # No consecutive hyphens
        if "--" in name:
            return (False, "Command name cannot contain consecutive hyphens")

        # Reserved names
        reserved = ["help", "version", "list", "edit", "delete", "create", "generate", "validate"]
        if name in reserved:
            return (False, f"Command name '{name}' is reserved")

        return (True, "")

    @staticmethod
    def validate_bash_command(command: str) -> Tuple[bool, str, List[str]]:
        """
        Validate bash command for safety.

        Args:
            command: Bash command to validate

        Returns:
            Tuple of (is_safe, error_or_warning, warnings_list)
        """
        if not command or not command.strip():
            return (False, "Bash command cannot be empty", [])

        command_lower = command.lower()
        warnings = []

        # Check for dangerous patterns
        for dangerous in DANGEROUS_COMMANDS:
            if dangerous in command_lower:
                return (
                    False,
                    f"Dangerous command detected: '{dangerous}'. This command is not allowed.",
                    [],
                )

        # Check for potentially unsafe patterns
        if any(char in command for char in ["$(", "`", "&", "|", ";"]):
            warnings.append("Command contains shell operators ($(, `, &, |, ;). Use with caution.")

        # Check if redirecting to system files
        if ">" in command or ">>" in command:
            if any(sys_path in command for sys_path in ["/etc/", "/sys/", "/proc/", "/dev/"]):
                return (
                    False,
                    "Cannot redirect output to system directories",
                    [],
                )
            warnings.append("Command redirects output. Ensure the target path is safe.")

        # Check if command starts with a safe command
        first_word = command.strip().split()[0] if command.strip().split() else ""
        if first_word and first_word not in SAFE_COMMANDS and not any(
            first_word.startswith(safe) for safe in SAFE_COMMANDS
        ):
            warnings.append(
                f"Command '{first_word}' is not in the safe commands list. Review carefully."
            )

        return (True, "", warnings)

    @staticmethod
    def validate_file_reference(file_ref: str, project_root: Path) -> Tuple[bool, str]:
        """
        Validate file reference for security (no path traversal).

        Args:
            file_ref: File reference path
            project_root: Project root directory

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_ref or not file_ref.strip():
            return (False, "File reference cannot be empty")

        # Remove @ prefix if present
        clean_ref = file_ref.lstrip("@").strip()

        # Check for path traversal attempts
        if ".." in clean_ref:
            return (False, "Path traversal detected (..). File references must be within project.")

        # Check for absolute paths
        if clean_ref.startswith("/") or (len(clean_ref) > 1 and clean_ref[1] == ":"):
            return (False, "Absolute paths not allowed. Use relative paths from project root.")

        try:
            # Resolve path and check it's within project
            full_path = (project_root / clean_ref).resolve()
            if not str(full_path).startswith(str(project_root.resolve())):
                return (False, "File reference must be within project directory")
        except Exception as e:
            return (False, f"Invalid file path: {e}")

        return (True, "")

    @staticmethod
    def validate_template_name(template: str) -> Tuple[bool, str]:
        """
        Validate template name for security (no path traversal).

        Args:
            template: Template name

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not template or not template.strip():
            return (False, "Template name cannot be empty")

        # Check for path separators
        if "/" in template or "\\" in template:
            return (False, "Template name cannot contain path separators")

        # Check for path traversal
        if ".." in template:
            return (False, "Path traversal detected in template name")

        # Must be alphanumeric with hyphens/underscores
        if not re.match(r"^[a-zA-Z0-9_-]+$", template):
            return (False, "Template name must be alphanumeric with hyphens/underscores")

        return (True, "")

    @staticmethod
    def sanitize_yaml_value(value: any) -> any:
        """
        Sanitize YAML value for safe frontmatter generation.

        Args:
            value: Value to sanitize

        Returns:
            Sanitized value
        """
        if isinstance(value, str):
            # Remove control characters
            sanitized = "".join(char for char in value if ord(char) >= 32 or char in "\n\r\t")
            return sanitized.strip()
        elif isinstance(value, (list, tuple)):
            return [Validator.sanitize_yaml_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: Validator.sanitize_yaml_value(v) for k, v in value.items()}
        else:
            return value

    @staticmethod
    def validate_scope_path(scope_path: Path) -> Tuple[bool, str]:
        """
        Validate scope path exists and is a directory.

        Args:
            scope_path: Path to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not scope_path.exists():
            return (False, f"Scope path does not exist: {scope_path}")

        if not scope_path.is_dir():
            return (False, f"Scope path is not a directory: {scope_path}")

        # Check write permissions
        test_file = scope_path / ".test_write"
        try:
            test_file.touch()
            test_file.unlink()
        except Exception as e:
            return (False, f"No write permission in scope path: {e}")

        return (True, "")
