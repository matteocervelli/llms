"""
Personal design system import logic.

Handles importing design systems from JSON/YAML files, validating schemas,
and saving them to the design-systems directory with metadata.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    yaml = None

from .validator import DesignTokenValidator

logger = logging.getLogger(__name__)


class PersonalDesignImporter:
    """Imports personal design systems and saves them to the catalog."""

    def __init__(self, output_dir: str | Path = "design-systems") -> None:
        """
        Initialize the importer.

        Args:
            output_dir: Base directory for design system storage
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.validator = DesignTokenValidator()

    def import_design(
        self,
        file_path: str | Path,
        system_name: Optional[str] = None,
        overwrite: bool = False,
    ) -> tuple[bool, str, Optional[Path]]:
        """
        Import a design system from a file.

        Args:
            file_path: Path to JSON or YAML design file
            system_name: Override system name from file (optional)
            overwrite: Whether to overwrite existing systems

        Returns:
            Tuple of (success, message, system_dir_path)
        """
        file_path = Path(file_path)

        # Validate file exists
        if not file_path.exists():
            return False, f"File not found: {file_path}", None

        # Load file
        try:
            data = self._load_file(file_path)
        except Exception as e:
            return False, f"Failed to load file: {e}", None

        # Override system name if provided
        if system_name:
            data["name"] = system_name

        # Validate schema
        is_valid, errors = self.validator.validate(data)
        if not is_valid:
            error_msg = "Validation failed:\n  - " + "\n  - ".join(errors)
            return False, error_msg, None

        # Save design system
        try:
            system_dir = self._save_design(data, overwrite)
            msg = f"Design system imported: {data['name']}"
            return True, msg, system_dir
        except Exception as e:
            return False, f"Failed to save design system: {e}", None

    def _load_file(self, file_path: Path) -> dict[str, Any]:
        """
        Load design system from JSON or YAML file.

        Args:
            file_path: Path to file

        Returns:
            Parsed design system data

        Raises:
            ValueError: If file format is unsupported
            json.JSONDecodeError: If JSON is invalid
            yaml.YAMLError: If YAML is invalid
        """
        suffix = file_path.suffix.lower()

        if suffix == ".json":
            with open(file_path) as f:
                return json.load(f)
        elif suffix in {".yaml", ".yml"}:
            if yaml is None:
                raise ImportError("PyYAML required for YAML support: pip install pyyaml")
            with open(file_path) as f:
                return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def _save_design(
        self,
        data: dict[str, Any],
        overwrite: bool = False,
    ) -> Path:
        """
        Save design system to disk.

        Args:
            data: Design system data
            overwrite: Whether to overwrite existing

        Returns:
            Path to system directory

        Raises:
            FileExistsError: If system exists and overwrite=False
        """
        system_name = self._normalize_name(data["name"])
        system_dir = self.output_dir / f"custom-{system_name}"

        # Check if exists
        if system_dir.exists() and not overwrite:
            raise FileExistsError(f"Design system already exists: {system_dir}")

        system_dir.mkdir(parents=True, exist_ok=True)

        # Prepare metadata
        metadata = {
            "name": data["name"],
            "version": data.get("version", "1.0.0"),
            "description": data.get("description", ""),
            "author": data.get("author", ""),
            "source_type": "personal_import",
            "imported_at": datetime.now().isoformat(),
        }

        # Save tokens
        tokens_file = system_dir / "tokens.json"
        with open(tokens_file, "w") as f:
            json.dump(data["tokens"], f, indent=2)

        # Save metadata
        metadata_file = system_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Saved design system to {system_dir}")
        return system_dir

    @staticmethod
    def _normalize_name(name: str) -> str:
        """
        Normalize system name for directory naming.

        Args:
            name: System name

        Returns:
            Normalized name (lowercase, dashes instead of spaces)
        """
        return name.lower().replace(" ", "-").replace("_", "-")
