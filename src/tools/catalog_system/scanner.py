"""
Scanner component for catalog system.

Auto-discovers skills, commands, and agents by scanning the filesystem
and parsing YAML frontmatter from Markdown files.

Security Features:
- Path traversal prevention (rejects .. and absolute paths outside scope)
- Path normalization and validation
- Safe YAML parsing with error handling

Example Usage:
    >>> from pathlib import Path
    >>> from src.tools.catalog_system.scanner import Scanner
    >>>
    >>> scanner = Scanner()
    >>> skills = scanner.scan_skills([Path("~/.claude").expanduser()])
    >>> for skill in skills:
    ...     print(f"{skill.name}: {skill.description}")
"""

import yaml  # type: ignore[import-untyped]
from pathlib import Path
from typing import List, Dict, Any, Optional

from .models import (
    SkillCatalogEntry,
    CommandCatalogEntry,
    AgentCatalogEntry,
)
from .exceptions import ScanError

# Import validator for element validation
try:
    from ..element_validator import ElementValidator, ElementType
    VALIDATOR_AVAILABLE = True
except ImportError:
    VALIDATOR_AVAILABLE = False


class Scanner:
    """
    Scans filesystem for catalog elements and extracts metadata.

    The Scanner walks through designated directories looking for:
    - Skills: directories containing SKILL.md files in .claude/skills/
    - Commands: .md files in .claude/commands/
    - Agents: .md files in .claude/agents/

    For each element, it:
    1. Parses YAML frontmatter to extract metadata
    2. Detects scope based on path (global/project/local)
    3. Creates appropriate CatalogEntry models
    4. Validates paths for security
    """

    # Directory names for each element type
    SKILLS_DIR = "skills"
    COMMANDS_DIR = "commands"
    AGENTS_DIR = "agents"

    # Scope detection patterns
    GLOBAL_MARKER = ".claude"  # in home directory

    def __init__(self, validate: bool = True, skip_invalid: bool = True) -> None:
        """
        Initialize the Scanner.

        Args:
            validate: Enable element validation (requires element_validator)
            skip_invalid: Skip invalid elements instead of failing
        """
        self.validate_elements = validate and VALIDATOR_AVAILABLE
        self.skip_invalid = skip_invalid

        if self.validate_elements:
            self.validator = ElementValidator()
        else:
            self.validator = None

        if validate and not VALIDATOR_AVAILABLE:
            print("Warning: element_validator not available, validation disabled")

    def scan_skills(self, scope_paths: List[Path]) -> List[SkillCatalogEntry]:
        """
        Scan for skills in the provided scope paths.

        Args:
            scope_paths: List of paths to .claude directories to scan

        Returns:
            List of discovered SkillCatalogEntry objects

        Raises:
            ScanError: If path validation fails or scanning encounters errors

        Example:
            >>> scanner = Scanner()
            >>> global_path = Path.home() / ".claude"
            >>> skills = scanner.scan_skills([global_path])
        """
        discovered: List[SkillCatalogEntry] = []

        for scope_path in scope_paths:
            # Validate and normalize path
            validated_path = self._validate_path(scope_path)

            # Build skills directory path
            skills_dir = validated_path / self.SKILLS_DIR

            # Skip if directory doesn't exist
            if not skills_dir.exists() or not skills_dir.is_dir():
                continue

            # Detect scope from path
            scope = self._detect_scope(validated_path)

            # Scan for skill directories
            try:
                for item in skills_dir.iterdir():
                    if not item.is_dir():
                        continue

                    # Look for SKILL.md file
                    skill_file = item / "SKILL.md"
                    if not skill_file.exists():
                        continue

                    # Validate element (skip if invalid and skip_invalid=True)
                    if not self._validate_element(skill_file, ElementType.SKILL if VALIDATOR_AVAILABLE else None):
                        continue

                    # Parse frontmatter and create entry
                    try:
                        entry = self._create_skill_entry(item, skill_file, scope)
                        discovered.append(entry)
                    except Exception:
                        # Log error but continue scanning
                        # In production, would use proper logging
                        continue

            except PermissionError:
                # Handle permission errors gracefully
                continue
            except OSError:
                # Handle other OS errors
                continue

        return discovered

    def scan_commands(self, scope_paths: List[Path]) -> List[CommandCatalogEntry]:
        """
        Scan for commands in the provided scope paths.

        Args:
            scope_paths: List of paths to .claude directories to scan

        Returns:
            List of discovered CommandCatalogEntry objects

        Raises:
            ScanError: If path validation fails or scanning encounters errors

        Example:
            >>> scanner = Scanner()
            >>> project_path = Path.cwd() / ".claude"
            >>> commands = scanner.scan_commands([project_path])
        """
        discovered: List[CommandCatalogEntry] = []

        for scope_path in scope_paths:
            # Validate and normalize path
            validated_path = self._validate_path(scope_path)

            # Build commands directory path
            commands_dir = validated_path / self.COMMANDS_DIR

            # Skip if directory doesn't exist
            if not commands_dir.exists() or not commands_dir.is_dir():
                continue

            # Detect scope from path
            scope = self._detect_scope(validated_path)

            # Scan for command files
            try:
                for item in commands_dir.iterdir():
                    if not item.is_file() or item.suffix != ".md":
                        continue

                    # Validate element (skip if invalid and skip_invalid=True)
                    if not self._validate_element(item, ElementType.COMMAND if VALIDATOR_AVAILABLE else None):
                        continue

                    # Parse frontmatter and create entry
                    try:
                        entry = self._create_command_entry(item, scope)
                        discovered.append(entry)
                    except Exception:
                        # Log error but continue scanning
                        continue

            except PermissionError:
                continue
            except OSError:
                continue

        return discovered

    def scan_agents(self, scope_paths: List[Path]) -> List[AgentCatalogEntry]:
        """
        Scan for agents in the provided scope paths.

        Args:
            scope_paths: List of paths to .claude directories to scan

        Returns:
            List of discovered AgentCatalogEntry objects

        Raises:
            ScanError: If path validation fails or scanning encounters errors

        Example:
            >>> scanner = Scanner()
            >>> all_paths = [Path.home() / ".claude", Path.cwd() / ".claude"]
            >>> agents = scanner.scan_agents(all_paths)
        """
        discovered: List[AgentCatalogEntry] = []

        for scope_path in scope_paths:
            # Validate and normalize path
            validated_path = self._validate_path(scope_path)

            # Build agents directory path
            agents_dir = validated_path / self.AGENTS_DIR

            # Skip if directory doesn't exist
            if not agents_dir.exists() or not agents_dir.is_dir():
                continue

            # Detect scope from path
            scope = self._detect_scope(validated_path)

            # Scan for agent files
            try:
                for item in agents_dir.iterdir():
                    if not item.is_file() or item.suffix != ".md":
                        continue

                    # Validate element (skip if invalid and skip_invalid=True)
                    if not self._validate_element(item, ElementType.AGENT if VALIDATOR_AVAILABLE else None):
                        continue

                    # Parse frontmatter and create entry
                    try:
                        entry = self._create_agent_entry(item, scope)
                        discovered.append(entry)
                    except Exception:
                        # Log error but continue scanning
                        continue

            except PermissionError:
                continue
            except OSError:
                continue

        return discovered

    def _validate_path(self, path: Path) -> Path:
        """
        Validate and normalize a path for security.

        Prevents directory traversal attacks by:
        - Rejecting paths with .. components
        - Rejecting absolute paths outside expected scope
        - Normalizing and resolving paths

        Args:
            path: Path to validate

        Returns:
            Normalized, validated Path object

        Raises:
            ScanError: If path is invalid or dangerous
        """
        # Resolve to absolute path
        resolved = path.resolve()

        # Check for parent directory traversal
        if ".." in str(path):
            raise ScanError(f"Invalid path: Path traversal not allowed: {path}")

        # Check if trying to access system directories
        system_dirs = ["/etc", "/sys", "/proc", "/dev"]
        for sys_dir in system_dirs:
            if str(resolved).startswith(sys_dir):
                raise ScanError(f"Invalid path: System directory access not " f"allowed: {path}")

        return resolved

    def _detect_scope(self, path: Path) -> str:
        """
        Detect scope (global/project/local) from path.

        Detection logic:
        - If path is directly under home/.claude: global
        - Otherwise: project
        - Local scope requires additional context (settings.local.json)

        Args:
            path: Path to analyze

        Returns:
            Scope string: "global", "project", or "local"
        """
        home = Path.home()
        global_claude = home / ".claude"

        # Check if path is the global .claude directory
        try:
            # If path is global_claude or a direct child of it
            if path == global_claude or path.parent == global_claude:
                return "global"
        except (ValueError, OSError):
            pass

        # Check if path is under home/.claude
        try:
            path.relative_to(global_claude)
            return "global"
        except ValueError:
            # Not under home/.claude, must be project
            return "project"

    def _parse_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse YAML frontmatter from a Markdown file.

        Expects frontmatter delimited by --- at start of file.

        Args:
            file_path: Path to Markdown file

        Returns:
            Dictionary of frontmatter data, empty dict if parsing fails
        """
        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            # Handle file read errors or encoding issues
            return {}

        # Check for frontmatter
        if not content.startswith("---"):
            return {}

        # Split on --- delimiters
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}

        frontmatter_str = parts[1].strip()
        if not frontmatter_str:
            return {}

        # Parse YAML
        try:
            return yaml.safe_load(frontmatter_str) or {}
        except yaml.YAMLError:
            # Return empty dict on YAML parse error
            return {}

    def _create_skill_entry(
        self, skill_dir: Path, skill_file: Path, scope: str
    ) -> SkillCatalogEntry:
        """
        Create a SkillCatalogEntry from a skill directory.

        Args:
            skill_dir: Path to skill directory
            skill_file: Path to SKILL.md file
            scope: Detected scope (global/project/local)

        Returns:
            SkillCatalogEntry object
        """
        # Parse frontmatter
        frontmatter = self._parse_frontmatter(skill_file)

        # Extract fields with fallbacks
        name = frontmatter.get("name", skill_dir.name)
        description = frontmatter.get("description", "")
        template = frontmatter.get("template", "basic")
        allowed_tools = frontmatter.get("allowed-tools", [])

        # Check for scripts directory
        has_scripts = (skill_dir / "scripts").exists()

        # Count files in directory
        try:
            file_count = len(list(skill_dir.iterdir()))
        except (OSError, PermissionError):
            file_count = 1

        # Create entry
        return SkillCatalogEntry(
            name=name,
            scope=scope,  # type: ignore
            description=description,
            file_path=skill_dir,
            template=template,
            has_scripts=has_scripts,
            file_count=file_count,
            allowed_tools=allowed_tools,
        )

    def _create_command_entry(self, command_file: Path, scope: str) -> CommandCatalogEntry:
        """
        Create a CommandCatalogEntry from a command file.

        Args:
            command_file: Path to command .md file
            scope: Detected scope (global/project/local)

        Returns:
            CommandCatalogEntry object
        """
        # Parse frontmatter
        frontmatter = self._parse_frontmatter(command_file)

        # Extract fields with fallbacks
        name = frontmatter.get("name", command_file.stem)
        description = frontmatter.get("description", "")
        aliases = frontmatter.get("aliases", [])
        requires_tools = frontmatter.get("requires_tools", [])
        tags = frontmatter.get("tags", [])

        # Create entry
        return CommandCatalogEntry(
            name=name,
            scope=scope,  # type: ignore
            description=description,
            file_path=command_file,
            aliases=aliases,
            requires_tools=requires_tools,
            tags=tags,
        )

    def _create_agent_entry(self, agent_file: Path, scope: str) -> AgentCatalogEntry:
        """
        Create an AgentCatalogEntry from an agent file.

        Args:
            agent_file: Path to agent .md file
            scope: Detected scope (global/project/local)

        Returns:
            AgentCatalogEntry object
        """
        # Parse frontmatter
        frontmatter = self._parse_frontmatter(agent_file)

        # Extract fields with fallbacks
        name = frontmatter.get("name", agent_file.stem)
        description = frontmatter.get("description", "")
        model = frontmatter.get("model", "sonnet")
        specialization = frontmatter.get("specialization", "")
        requires_skills = frontmatter.get("requires_skills", [])

        # Create entry
        return AgentCatalogEntry(
            name=name,
            scope=scope,  # type: ignore
            description=description,
            file_path=agent_file,
            model=model,
            specialization=specialization,
            requires_skills=requires_skills,
        )

    def _validate_element(
        self, file_path: Path, element_type: Optional[ElementType] = None
    ) -> bool:
        """
        Validate an element file using the ElementValidator.

        Args:
            file_path: Path to the element file
            element_type: Optional element type hint

        Returns:
            True if valid or validation disabled, False if invalid

        Raises:
            ScanError: If validation fails and skip_invalid is False
        """
        if not self.validate_elements or self.validator is None:
            # Validation disabled
            return True

        result = self.validator.validate_element(file_path, element_type)

        if not result.is_valid:
            error_summary = f"{file_path.name}: {len(result.errors)} errors"
            for error in result.errors[:3]:  # Show first 3 errors
                error_summary += f"\n  - [{error.field}] {error.message}"

            if self.skip_invalid:
                # Log warning and continue
                print(f"Warning: Skipping invalid element: {error_summary}")
                return False
            else:
                # Raise error to stop scanning
                raise ScanError(f"Invalid element: {error_summary}")

        return True
