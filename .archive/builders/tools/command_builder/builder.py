"""
Command builder core logic.

Handles command file generation, including template rendering, frontmatter creation,
and file writing with proper path management based on scope.
"""

from pathlib import Path
from typing import Optional, Tuple

from .exceptions import CommandBuilderError, CommandExistsError
from .models import CommandConfig, ScopeType
from .templates import TemplateManager
from .validator import Validator


class CommandBuilder:
    """Builds Claude Code slash command files from configuration."""

    def __init__(self, template_manager: Optional[TemplateManager] = None):
        """
        Initialize command builder.

        Args:
            template_manager: Template manager (creates default if not provided)
        """
        self.template_manager = template_manager or TemplateManager()

    def get_scope_path(self, scope: ScopeType, project_root: Optional[Path] = None) -> Path:
        """
        Get the directory path for a given scope.

        Args:
            scope: Scope type (global/project/local)
            project_root: Project root directory (for project/local scopes)

        Returns:
            Path to scope directory

        Raises:
            CommandBuilderError: If scope path cannot be determined
        """
        if scope == ScopeType.GLOBAL:
            # Global scope: ~/.claude/commands/
            global_path = Path.home() / ".claude" / "commands"
            global_path.mkdir(parents=True, exist_ok=True)
            return global_path

        elif scope == ScopeType.PROJECT:
            # Project scope: <project>/.claude/commands/
            if project_root is None:
                project_root = Path.cwd()
            project_path = project_root / ".claude" / "commands"
            project_path.mkdir(parents=True, exist_ok=True)
            return project_path

        elif scope == ScopeType.LOCAL:
            # Local scope: <project>/.claude/commands/ (same as project for files)
            # Note: Local commands are tracked separately in catalog but use same directory
            if project_root is None:
                project_root = Path.cwd()
            local_path = project_root / ".claude" / "commands"
            local_path.mkdir(parents=True, exist_ok=True)
            return local_path

        else:
            raise CommandBuilderError(f"Unknown scope type: {scope}")

    def build_command(
        self,
        config: CommandConfig,
        project_root: Optional[Path] = None,
        overwrite: bool = False,
    ) -> Tuple[Path, str]:
        """
        Build a command file from configuration.

        Args:
            config: Command configuration
            project_root: Project root directory
            overwrite: Whether to overwrite existing command

        Returns:
            Tuple of (command_file_path, rendered_content)

        Raises:
            CommandExistsError: If command already exists and overwrite=False
            CommandBuilderError: If command cannot be built
        """
        # Get scope path
        scope_path = self.get_scope_path(config.scope, project_root)

        # Validate scope path
        is_valid, error = Validator.validate_scope_path(scope_path)
        if not is_valid:
            raise CommandBuilderError(f"Invalid scope path: {error}")

        # Build command file path
        command_file = scope_path / f"{config.name}.md"

        # Check if command already exists
        if command_file.exists() and not overwrite:
            raise CommandExistsError(
                f"Command '{config.name}' already exists at {command_file}. "
                "Use overwrite=True to replace it."
            )

        # Validate file references if present
        if config.file_references and project_root:
            for file_ref in config.file_references:
                is_valid, error = Validator.validate_file_reference(file_ref, project_root)
                if not is_valid:
                    raise CommandBuilderError(f"Invalid file reference '{file_ref}': {error}")

        # Validate bash commands if present
        warnings = []
        if config.bash_commands:
            for cmd in config.bash_commands:
                is_safe, error, cmd_warnings = Validator.validate_bash_command(cmd)
                if not is_safe:
                    raise CommandBuilderError(f"Unsafe bash command '{cmd}': {error}")
                warnings.extend(cmd_warnings)

        # Render template
        try:
            content = self.template_manager.render_template(config.template, config)
        except Exception as e:
            raise CommandBuilderError(f"Failed to render template: {e}")

        # Write command file
        try:
            command_file.write_text(content)
        except Exception as e:
            raise CommandBuilderError(f"Failed to write command file: {e}")

        return (command_file, content)

    def update_command(
        self,
        command_path: Path,
        config: CommandConfig,
    ) -> Tuple[Path, str]:
        """
        Update an existing command file.

        Args:
            command_path: Path to existing command file
            config: New command configuration

        Returns:
            Tuple of (command_file_path, rendered_content)

        Raises:
            CommandBuilderError: If command cannot be updated
        """
        if not command_path.exists():
            raise CommandBuilderError(f"Command file not found: {command_path}")

        # Render new template
        try:
            content = self.template_manager.render_template(config.template, config)
        except Exception as e:
            raise CommandBuilderError(f"Failed to render template: {e}")

        # Write updated command file
        try:
            command_path.write_text(content)
        except Exception as e:
            raise CommandBuilderError(f"Failed to update command file: {e}")

        return (command_path, content)

    def delete_command(self, command_path: Path) -> bool:
        """
        Delete a command file.

        Args:
            command_path: Path to command file

        Returns:
            True if deleted successfully

        Raises:
            CommandBuilderError: If command cannot be deleted
        """
        if not command_path.exists():
            return False

        try:
            command_path.unlink()
            return True
        except Exception as e:
            raise CommandBuilderError(f"Failed to delete command file: {e}")

    def validate_command_file(self, command_path: Path) -> Tuple[bool, str]:
        """
        Validate an existing command file.

        Args:
            command_path: Path to command file

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not command_path.exists():
            return (False, f"Command file not found: {command_path}")

        if not command_path.is_file():
            return (False, f"Path is not a file: {command_path}")

        if command_path.suffix != ".md":
            return (False, f"Command file must have .md extension: {command_path}")

        try:
            content = command_path.read_text()
            if not content.strip():
                return (False, "Command file is empty")

            # Basic validation: should have frontmatter
            if not content.startswith("---"):
                return (False, "Command file must start with YAML frontmatter (---)")

            return (True, "")

        except Exception as e:
            return (False, f"Failed to read command file: {e}")
