"""
Skill builder core logic.

Handles skill directory generation, including template rendering, SKILL.md creation,
and directory management with proper permissions and scope handling.

This module provides the SkillBuilder class which creates skill directories
(not single files) with SKILL.md inside. Skills can have additional files
like scripts/, docs/, etc. based on the template used.

Security Focus:
- Path traversal prevention
- Secure file permissions (755 for directories, 644 for files)
- Input validation through SkillConfig and SkillValidator
- Scope-based path resolution

Performance Target:
- < 50ms skill creation time
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from uuid import uuid4

from src.core.scope_manager import ScopeManager
from src.tools.skill_builder.exceptions import (
    SkillBuilderError,
    SkillExistsError,
    TemplateError,
)
from src.tools.skill_builder.models import SkillCatalogEntry, SkillConfig, ScopeType
from src.tools.skill_builder.templates import TemplateManager
from src.tools.skill_builder.validator import SkillValidator

# Import TYPE_CHECKING to avoid circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.tools.skill_builder.catalog import CatalogManager


class SkillBuilder:
    """
    Builds Claude Code skill directories from configuration.

    The SkillBuilder creates skill directories (not single files) with SKILL.md
    as the main skill file. Additional files may be created based on the template.

    Attributes:
        scope_manager: ScopeManager for path resolution
        template_manager: TemplateManager for SKILL.md generation
        catalog_manager: Optional CatalogManager for tracking skills
    """

    # File permissions constants
    DIR_PERMISSIONS = 0o755  # rwxr-xr-x
    FILE_PERMISSIONS = 0o644  # rw-r--r--

    def __init__(
        self,
        scope_manager: Optional[ScopeManager] = None,
        template_manager: Optional[TemplateManager] = None,
        catalog_manager: Optional["CatalogManager"] = None,
    ):
        """
        Initialize skill builder.

        Args:
            scope_manager: ScopeManager instance (creates default if not provided)
            template_manager: TemplateManager instance (creates default if not provided)
            catalog_manager: Optional CatalogManager for tracking skills (optional)

        Examples:
            >>> builder = SkillBuilder()  # Uses defaults, no catalog
            >>> builder = SkillBuilder(scope_manager=custom_scope_mgr)
            >>> builder = SkillBuilder(catalog_manager=catalog_mgr)  # With catalog tracking
        """
        self.scope_manager = scope_manager or ScopeManager()
        self.template_manager = template_manager or TemplateManager()
        self.catalog_manager = catalog_manager

    def get_scope_path(
        self, scope: ScopeType, project_root: Optional[Path] = None
    ) -> Path:
        """
        Get the skills directory path for a given scope.

        Creates the directory with proper permissions if it doesn't exist.

        Args:
            scope: Scope type (GLOBAL, PROJECT, or LOCAL)
            project_root: Project root directory (for PROJECT/LOCAL scopes)

        Returns:
            Path to skills directory

        Raises:
            SkillBuilderError: If scope path cannot be determined

        Examples:
            >>> builder = SkillBuilder()
            >>> path = builder.get_scope_path(ScopeType.GLOBAL)
            >>> print(path)
            PosixPath('/home/user/.claude/skills')
        """
        if scope == ScopeType.GLOBAL:
            # Global scope: ~/.claude/skills/
            global_path = Path.home() / ".claude" / "skills"
            global_path.mkdir(parents=True, exist_ok=True)
            # Set permissions
            os.chmod(global_path, self.DIR_PERMISSIONS)
            return global_path

        elif scope == ScopeType.PROJECT:
            # Project scope: <project>/.claude/skills/
            if project_root is None:
                project_root = Path.cwd()

            project_path = project_root / ".claude" / "skills"
            project_path.mkdir(parents=True, exist_ok=True)
            # Set permissions
            os.chmod(project_path, self.DIR_PERMISSIONS)
            return project_path

        elif scope == ScopeType.LOCAL:
            # Local scope: <project>/.claude/skills/ (same directory as project)
            # Note: Local skills are tracked separately in catalog but use same directory
            if project_root is None:
                project_root = Path.cwd()

            local_path = project_root / ".claude" / "skills"
            local_path.mkdir(parents=True, exist_ok=True)
            # Set permissions
            os.chmod(local_path, self.DIR_PERMISSIONS)
            return local_path

        else:
            raise SkillBuilderError(f"Unknown scope type: {scope}")

    def build_skill(
        self,
        config: SkillConfig,
        project_root: Optional[Path] = None,
        dry_run: bool = False,
    ) -> Tuple[Path, str]:
        """
        Build a skill directory from configuration.

        Creates a skill directory with SKILL.md file. Additional files may be
        created based on the template (e.g., scripts/ directory).

        Args:
            config: Skill configuration (validated SkillConfig instance)
            project_root: Project root directory (required for PROJECT/LOCAL scopes)
            dry_run: If True, validates but doesn't create files

        Returns:
            Tuple of (skill_directory_path, skill_md_content)

        Raises:
            SkillExistsError: If skill already exists in the scope
            SkillBuilderError: If skill cannot be built
            TemplateError: If template rendering fails

        Performance:
            Target: < 50ms for skill creation

        Examples:
            >>> config = SkillConfig(
            ...     name="pdf-processor",
            ...     description="Extract text from PDFs. Use when working with PDF files.",
            ...     scope=ScopeType.PROJECT,
            ...     template="basic"
            ... )
            >>> builder = SkillBuilder()
            >>> skill_path, content = builder.build_skill(config, dry_run=False)
            >>> print(f"Created: {skill_path}")
            Created: /project/.claude/skills/pdf-processor
        """
        # Get scope path
        try:
            scope_path = self.get_scope_path(config.scope, project_root)
        except Exception as e:
            raise SkillBuilderError(f"Failed to determine scope path: {str(e)}")

        # Build skill directory path
        skill_dir = scope_path / config.name

        # Security: Validate path is within scope directory
        is_valid, error = SkillValidator.validate_path_security(skill_dir, scope_path)
        if not is_valid:
            raise SkillBuilderError(f"Path security validation failed: {error}")

        # Check if skill already exists
        if skill_dir.exists() and not dry_run:
            raise SkillExistsError(
                f"Skill '{config.name}' already exists in {config.scope.value} scope at {skill_dir}. "
                "Delete it first or use update_skill() to modify it."
            )

        # Prepare template variables
        template_vars = {
            "name": config.name,
            "description": config.description,
            "allowed_tools": config.allowed_tools or [],
            "content": config.content or "",
            "frontmatter": config.frontmatter,
        }

        # Render template
        try:
            skill_content = self.template_manager.render(config.template, template_vars)
        except TemplateError as e:
            raise e
        except Exception as e:
            raise SkillBuilderError(f"Failed to render template '{config.template}': {str(e)}")

        # Dry run: return without creating files
        if dry_run:
            return (skill_dir, skill_content)

        # Create skill directory
        try:
            skill_dir.mkdir(parents=True, exist_ok=False)
            os.chmod(skill_dir, self.DIR_PERMISSIONS)
        except FileExistsError:
            raise SkillExistsError(
                f"Skill directory already exists: {skill_dir}. "
                "This shouldn't happen - check for race conditions."
            )
        except Exception as e:
            raise SkillBuilderError(f"Failed to create skill directory: {str(e)}")

        # Write SKILL.md file
        skill_file = skill_dir / "SKILL.md"
        try:
            skill_file.write_text(skill_content, encoding="utf-8")
            os.chmod(skill_file, self.FILE_PERMISSIONS)
        except Exception as e:
            # Cleanup: Remove directory if file write fails
            try:
                shutil.rmtree(skill_dir)
            except Exception:
                pass  # Best effort cleanup
            raise SkillBuilderError(f"Failed to write SKILL.md: {str(e)}")

        # Add to catalog if manager is provided
        if self.catalog_manager:
            try:
                entry = SkillCatalogEntry(
                    id=uuid4(),
                    name=config.name,
                    description=config.description,
                    scope=config.scope,
                    path=skill_dir,
                    metadata={
                        "template": config.template,
                        "has_scripts": (skill_dir / "scripts").exists(),
                        "file_count": len(list(skill_dir.iterdir())),
                        "allowed_tools": config.allowed_tools or [],
                    },
                )
                self.catalog_manager.add_skill(entry)
            except Exception as e:
                # Log warning but don't fail the skill creation
                # The skill was created successfully, catalog update is optional
                import warnings
                warnings.warn(f"Failed to add skill to catalog: {str(e)}")

        return (skill_dir, skill_content)

    def update_skill(
        self,
        skill_path: Path,
        config: SkillConfig,
    ) -> Tuple[Path, str]:
        """
        Update an existing skill's SKILL.md file.

        Re-renders the template with new configuration and updates SKILL.md.
        The skill directory and other files remain unchanged.

        Args:
            skill_path: Path to existing skill directory
            config: New skill configuration

        Returns:
            Tuple of (skill_directory_path, new_skill_md_content)

        Raises:
            SkillBuilderError: If skill cannot be updated

        Examples:
            >>> config = SkillConfig(
            ...     name="pdf-processor",
            ...     description="Updated description. Use when processing PDFs.",
            ...     scope=ScopeType.PROJECT,
            ...     template="with_tools",
            ...     allowed_tools=["Read", "Bash"]
            ... )
            >>> builder = SkillBuilder()
            >>> skill_path, content = builder.update_skill(
            ...     Path(".claude/skills/pdf-processor"),
            ...     config
            ... )
        """
        # Validate skill_path exists
        if not skill_path.exists():
            raise SkillBuilderError(f"Skill directory not found: {skill_path}")

        if not skill_path.is_dir():
            raise SkillBuilderError(f"Path is not a directory: {skill_path}")

        # Security: Validate path is within allowed scope
        # Get parent directory (should be skills/)
        scope_dir = skill_path.parent
        is_valid, error = SkillValidator.validate_path_security(skill_path, scope_dir)
        if not is_valid:
            raise SkillBuilderError(f"Path security validation failed: {error}")

        # Prepare template variables
        template_vars = {
            "name": config.name,
            "description": config.description,
            "allowed_tools": config.allowed_tools or [],
            "content": config.content or "",
            "frontmatter": config.frontmatter,
        }

        # Render new template
        try:
            skill_content = self.template_manager.render(config.template, template_vars)
        except TemplateError as e:
            raise e
        except Exception as e:
            raise SkillBuilderError(f"Failed to render template '{config.template}': {str(e)}")

        # Write updated SKILL.md
        skill_file = skill_path / "SKILL.md"
        try:
            skill_file.write_text(skill_content, encoding="utf-8")
            os.chmod(skill_file, self.FILE_PERMISSIONS)
        except Exception as e:
            raise SkillBuilderError(f"Failed to update SKILL.md: {str(e)}")

        # Update catalog timestamp if manager is provided
        if self.catalog_manager:
            try:
                # Find skill by name and scope
                skill = self.catalog_manager.get_skill(name=config.name, scope=config.scope)
                if skill:
                    self.catalog_manager.update_skill(
                        skill.id,
                        description=config.description,
                        updated_at=datetime.now(),
                        metadata={
                            "template": config.template,
                            "has_scripts": (skill_path / "scripts").exists(),
                            "file_count": len(list(skill_path.iterdir())),
                            "allowed_tools": config.allowed_tools or [],
                        },
                    )
            except Exception as e:
                # Log warning but don't fail the update
                import warnings
                warnings.warn(f"Failed to update skill in catalog: {str(e)}")

        return (skill_path, skill_content)

    def delete_skill(self, skill_path: Path) -> bool:
        """
        Delete a skill directory and all its contents.

        Removes the entire skill directory tree including SKILL.md and any
        additional files (scripts/, docs/, etc.).

        Args:
            skill_path: Path to skill directory to delete

        Returns:
            True if deleted successfully, False if directory doesn't exist

        Raises:
            SkillBuilderError: If skill cannot be deleted

        Security:
            Validates path is within an allowed scope directory before deletion.

        Examples:
            >>> builder = SkillBuilder()
            >>> success = builder.delete_skill(Path(".claude/skills/old-skill"))
            >>> print(f"Deleted: {success}")
            Deleted: True
        """
        # Check if path exists
        if not skill_path.exists():
            return False

        if not skill_path.is_dir():
            raise SkillBuilderError(f"Path is not a directory: {skill_path}")

        # Security: Validate path is within allowed scope
        # Get parent directory (should be skills/)
        scope_dir = skill_path.parent
        is_valid, error = SkillValidator.validate_path_security(skill_path, scope_dir)
        if not is_valid:
            raise SkillBuilderError(f"Path security validation failed: {error}")

        # Additional security: Verify parent directory is named "skills"
        if scope_dir.name != "skills":
            raise SkillBuilderError(
                f"Invalid skill path: parent directory must be 'skills', got '{scope_dir.name}'"
            )

        # Find and remove from catalog first (before deletion)
        skill_name = skill_path.name
        if self.catalog_manager:
            try:
                # Try all scopes to find the skill
                for scope in [ScopeType.GLOBAL, ScopeType.PROJECT, ScopeType.LOCAL]:
                    skill = self.catalog_manager.get_skill(name=skill_name, scope=scope)
                    if skill:
                        self.catalog_manager.remove_skill(skill.id)
                        break
            except Exception as e:
                # Log warning but don't fail the deletion
                import warnings
                warnings.warn(f"Failed to remove skill from catalog: {str(e)}")

        # Delete directory tree
        try:
            shutil.rmtree(skill_path)
            return True
        except Exception as e:
            raise SkillBuilderError(f"Failed to delete skill directory: {str(e)}")

    def validate_skill_directory(self, skill_path: Path) -> Tuple[bool, str]:
        """
        Validate an existing skill directory structure.

        Checks that:
        - Path exists and is a directory
        - Path is within an allowed scope
        - SKILL.md file exists
        - SKILL.md has valid frontmatter

        Args:
            skill_path: Path to skill directory

        Returns:
            Tuple of (is_valid, error_message)
            - (True, "") if valid
            - (False, error_message) if invalid

        Examples:
            >>> builder = SkillBuilder()
            >>> is_valid, msg = builder.validate_skill_directory(
            ...     Path(".claude/skills/pdf-processor")
            ... )
            >>> print(f"Valid: {is_valid}")
            Valid: True
        """
        # Check if path exists
        if not skill_path.exists():
            return (False, f"Skill directory not found: {skill_path}")

        if not skill_path.is_dir():
            return (False, f"Path is not a directory: {skill_path}")

        # Security: Validate path is within allowed scope
        scope_dir = skill_path.parent
        is_valid, error = SkillValidator.validate_path_security(skill_path, scope_dir)
        if not is_valid:
            return (False, f"Path security validation failed: {error}")

        # Check SKILL.md exists
        skill_file = skill_path / "SKILL.md"
        if not skill_file.exists():
            return (False, f"SKILL.md not found in {skill_path}")

        if not skill_file.is_file():
            return (False, f"SKILL.md is not a file: {skill_file}")

        # Validate SKILL.md content
        try:
            content = skill_file.read_text(encoding="utf-8")
        except Exception as e:
            return (False, f"Failed to read SKILL.md: {str(e)}")

        if not content.strip():
            return (False, "SKILL.md is empty")

        # Basic validation: should have frontmatter
        if not content.startswith("---"):
            return (False, "SKILL.md must start with YAML frontmatter (---)")

        return (True, "")
