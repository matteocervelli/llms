"""Core validation logic for Claude Code elements."""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

from .schemas import (
    ElementType,
    SCHEMA_MAP,
    FieldSchema,
    AgentSchema,
    SkillSchema,
    CommandSchema,
)


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"  # "error", "warning", "info"
    suggested_fix: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class ValidationResult:
    """Result of validating an element."""

    is_valid: bool
    element_type: Optional[ElementType] = None
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    frontmatter: Optional[Dict[str, Any]] = None
    content: Optional[str] = None
    file_path: Optional[Path] = None

    def add_error(
        self,
        field: str,
        message: str,
        suggested_fix: Optional[str] = None,
        line_number: Optional[int] = None,
    ):
        """Add an error to the result."""
        self.errors.append(
            ValidationError(
                field=field,
                message=message,
                severity="error",
                suggested_fix=suggested_fix,
                line_number=line_number,
            )
        )
        self.is_valid = False

    def add_warning(
        self,
        field: str,
        message: str,
        suggested_fix: Optional[str] = None,
        line_number: Optional[int] = None,
    ):
        """Add a warning to the result."""
        self.warnings.append(
            ValidationError(
                field=field,
                message=message,
                severity="warning",
                suggested_fix=suggested_fix,
                line_number=line_number,
            )
        )

    def get_summary(self) -> str:
        """Get a summary of the validation result."""
        if self.is_valid:
            status = "✅ Valid"
        else:
            status = f"❌ Invalid ({len(self.errors)} errors)"

        if self.warnings:
            status += f", {len(self.warnings)} warnings"

        return status


class ElementValidator:
    """Validator for Claude Code elements."""

    def __init__(self):
        """Initialize the validator."""
        pass

    def detect_element_type(self, file_path: Path) -> Optional[ElementType]:
        """Detect the element type from file path or content."""
        path_str = str(file_path)

        # Check parent directory names
        if "/agents/" in path_str or file_path.parent.name == "agents":
            return ElementType.AGENT
        elif "/skills/" in path_str or file_path.parent.name == "skills":
            return ElementType.SKILL
        elif "/commands/" in path_str or file_path.parent.name == "commands":
            return ElementType.COMMAND

        # Check file name patterns
        if "agent" in file_path.stem.lower():
            return ElementType.AGENT
        elif file_path.stem == "SKILL":
            return ElementType.SKILL

        return None

    def parse_frontmatter(
        self, content: str
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str], List[ValidationError]]:
        """
        Parse YAML frontmatter from markdown content.

        Returns:
            Tuple of (frontmatter_dict, content_after_frontmatter, errors)
        """
        errors = []

        # Check for frontmatter delimiters
        if not content.strip().startswith("---"):
            errors.append(
                ValidationError(
                    field="frontmatter",
                    message="Missing opening frontmatter delimiter (---)",
                    suggested_fix="Add '---' at the start of the file",
                    line_number=1,
                )
            )
            return None, content, errors

        # Split by frontmatter delimiters
        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append(
                ValidationError(
                    field="frontmatter",
                    message="Missing closing frontmatter delimiter (---)",
                    suggested_fix="Add '---' after the YAML frontmatter",
                )
            )
            return None, content, errors

        frontmatter_str = parts[1].strip()
        content_after = parts[2].strip()

        # Parse YAML
        try:
            frontmatter = yaml.safe_load(frontmatter_str)
            if not isinstance(frontmatter, dict):
                errors.append(
                    ValidationError(
                        field="frontmatter",
                        message=f"Frontmatter must be a YAML dict, got {type(frontmatter).__name__}",
                    )
                )
                return None, content_after, errors
        except yaml.YAMLError as e:
            errors.append(
                ValidationError(
                    field="frontmatter",
                    message=f"Invalid YAML: {str(e)}",
                    suggested_fix="Fix YAML syntax errors",
                )
            )
            return None, content_after, errors

        return frontmatter, content_after, errors

    def validate_field(
        self, field_name: str, field_value: Any, field_schema: FieldSchema
    ) -> List[ValidationError]:
        """Validate a single field against its schema."""
        errors = []

        # Check type
        if not isinstance(field_value, field_schema.field_type):
            errors.append(
                ValidationError(
                    field=field_name,
                    message=f"Expected {field_schema.field_type.__name__}, got {type(field_value).__name__}",
                    suggested_fix=f"Convert to {field_schema.field_type.__name__}",
                )
            )
            return errors

        # For string fields, perform additional checks
        if field_schema.field_type == str:
            value_str = str(field_value).strip()

            # Check empty
            if not value_str:
                errors.append(
                    ValidationError(
                        field=field_name,
                        message="Field cannot be empty",
                        suggested_fix=f"Provide a {field_schema.description}",
                    )
                )
                return errors

            # Check max length
            if field_schema.max_length and len(value_str) > field_schema.max_length:
                errors.append(
                    ValidationError(
                        field=field_name,
                        message=f"Exceeds max length of {field_schema.max_length} characters (current: {len(value_str)})",
                        suggested_fix=f"Shorten to {field_schema.max_length} characters or less",
                    )
                )

            # Check pattern
            if field_schema.pattern:
                if not re.match(field_schema.pattern, value_str):
                    errors.append(
                        ValidationError(
                            field=field_name,
                            message=f"Does not match required pattern: {field_schema.pattern}",
                            suggested_fix=field_schema.description,
                        )
                    )

        # Custom validator
        if field_schema.validator:
            try:
                field_schema.validator(field_value)
            except ValueError as e:
                errors.append(
                    ValidationError(field=field_name, message=str(e))
                )

        return errors

    def validate_element(
        self, file_path: Path, element_type: Optional[ElementType] = None
    ) -> ValidationResult:
        """
        Validate a Claude Code element file.

        Args:
            file_path: Path to the element file
            element_type: Optional element type (auto-detected if not provided)

        Returns:
            ValidationResult with errors, warnings, and suggestions
        """
        result = ValidationResult(is_valid=True, file_path=file_path)

        # Check file exists
        if not file_path.exists():
            result.add_error("file", f"File not found: {file_path}")
            return result

        # Read file content
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error("file", f"Failed to read file: {str(e)}")
            return result

        # Detect element type if not provided
        if element_type is None:
            element_type = self.detect_element_type(file_path)
            if element_type is None:
                result.add_error(
                    "file",
                    "Could not detect element type from file path",
                    suggested_fix="Place file in agents/, skills/, commands/, or prompts/ directory",
                )
                return result

        result.element_type = element_type

        # Get schema for this element type
        schema_class = SCHEMA_MAP.get(element_type)
        if not schema_class:
            result.add_error("file", f"Unknown element type: {element_type}")
            return result

        # Parse frontmatter
        frontmatter, content_after, parse_errors = self.parse_frontmatter(content)
        result.frontmatter = frontmatter
        result.content = content_after

        for error in parse_errors:
            result.errors.append(error)
            result.is_valid = False

        if frontmatter is None:
            return result

        # Get all fields for this schema
        all_fields = schema_class.get_all_fields()
        required_fields = schema_class.get_required_field_names()

        # Check required fields
        for field_name in required_fields:
            if field_name not in frontmatter:
                field_schema = all_fields[field_name]
                result.add_error(
                    field_name,
                    f"Required field '{field_name}' is missing",
                    suggested_fix=f"Add '{field_name}: {field_schema.description}'",
                )

        # Validate present fields
        for field_name, field_value in frontmatter.items():
            if field_name in all_fields:
                field_schema = all_fields[field_name]
                field_errors = self.validate_field(
                    field_name, field_value, field_schema
                )
                for error in field_errors:
                    result.errors.append(error)
                    result.is_valid = False
            else:
                # Unknown field - warning, not error
                result.add_warning(
                    field_name,
                    f"Unknown field '{field_name}' for {element_type.value}",
                    suggested_fix=f"Remove this field or check spelling",
                )

        # Check content exists
        if not content_after or not content_after.strip():
            result.add_warning(
                "content",
                "Element has no content after frontmatter",
                suggested_fix=f"Add {element_type.value} instructions or description",
            )

        return result

    def validate_directory(
        self, directory: Path, recursive: bool = True
    ) -> Dict[Path, ValidationResult]:
        """
        Validate all elements in a directory.

        Args:
            directory: Directory to validate
            recursive: Whether to search subdirectories

        Returns:
            Dictionary mapping file paths to validation results
        """
        results = {}

        # Find all markdown files with specific filtering
        if recursive:
            pattern = "**/*.md"
        else:
            pattern = "*.md"

        for file_path in directory.glob(pattern):
            # Skip non-element files
            if file_path.name.lower() in [
                "readme.md", "changelog.md", "license.md", "history.md",
                "security.md", "api.md", "third_party_notices.md", "claude.md"
            ]:
                continue

            # Only validate files in proper element directories
            path_str = str(file_path)
            in_agents = "/agents/" in path_str
            in_skills = "/skills/" in path_str
            in_commands = "/commands/" in path_str

            # Skip if not in a known element directory
            if not (in_agents or in_skills or in_commands):
                continue

            # For skills, only validate SKILL.md files
            if in_skills and file_path.name != "SKILL.md":
                continue

            result = self.validate_element(file_path)
            results[file_path] = result

        return results

    def auto_fix(self, file_path: Path, result: ValidationResult) -> bool:
        """
        Attempt to automatically fix validation errors.

        Args:
            file_path: Path to the file
            result: ValidationResult with errors

        Returns:
            True if fixes were applied, False otherwise
        """
        if result.is_valid:
            return False

        # Handle missing frontmatter entirely
        if result.frontmatter is None:
            # Create new frontmatter with required fields
            schema_class = SCHEMA_MAP.get(result.element_type)
            if not schema_class:
                return False

            # Generate default name from filename
            default_name = file_path.stem.lower()
            default_name = re.sub(r"[^a-z0-9-]", "-", default_name)
            default_name = re.sub(r"-+", "-", default_name)
            default_name = default_name.strip("-")

            # Create minimal valid frontmatter
            fixed_frontmatter = {}
            for field in schema_class.REQUIRED_FIELDS:
                if field.name == "name":
                    fixed_frontmatter["name"] = default_name
                elif field.name == "description":
                    fixed_frontmatter["description"] = f"TODO: {field.description}"
                else:
                    fixed_frontmatter[field.name] = f"TODO: {field.description}"

            # Reconstruct file with new frontmatter
            original_content = file_path.read_text(encoding="utf-8")
            new_content = "---\n"
            new_content += yaml.dump(fixed_frontmatter, default_flow_style=False, sort_keys=False)
            new_content += "---\n\n"
            new_content += original_content

            # Write back
            try:
                file_path.write_text(new_content, encoding="utf-8")
                return True
            except Exception as e:
                print(f"Failed to write fixes: {str(e)}")
                return False

        # Apply fixes to existing frontmatter
        fixed_frontmatter = dict(result.frontmatter)
        fixes_applied = False

        for error in result.errors:
            # Fix type mismatches (e.g., list to string conversion)
            if "Expected str, got" in error.message and error.field in fixed_frontmatter:
                field_value = fixed_frontmatter[error.field]
                if isinstance(field_value, list):
                    # Convert list to comma-separated string
                    fixed_frontmatter[error.field] = ", ".join(str(item) for item in field_value)
                    fixes_applied = True
                elif not isinstance(field_value, str):
                    # Convert other types to string
                    fixed_frontmatter[error.field] = str(field_value)
                    fixes_applied = True

            # Fix missing required fields
            if "missing" in error.message.lower() and error.field:
                schema_class = SCHEMA_MAP[result.element_type]
                all_fields = schema_class.get_all_fields()

                if error.field in all_fields:
                    field_schema = all_fields[error.field]
                    # Add placeholder value
                    if field_schema.field_type == str:
                        if field_schema.name == "name":
                            # Generate from filename
                            default_name = file_path.stem.lower()
                            default_name = re.sub(r"[^a-z0-9-]", "-", default_name)
                            default_name = re.sub(r"-+", "-", default_name)
                            default_name = default_name.strip("-")
                            fixed_frontmatter[error.field] = default_name
                        else:
                            fixed_frontmatter[error.field] = f"TODO: {field_schema.description}"
                        fixes_applied = True

            # Fix pattern mismatches for name fields
            if error.field == "name" and "pattern" in error.message.lower():
                if "name" in fixed_frontmatter:
                    # Convert to lowercase and replace invalid characters
                    fixed_name = re.sub(
                        r"[^a-z0-9-]", "-", fixed_frontmatter["name"].lower()
                    )
                    fixed_name = re.sub(r"-+", "-", fixed_name)  # Remove duplicate hyphens
                    fixed_name = fixed_name.strip("-")  # Remove leading/trailing hyphens
                    fixed_frontmatter["name"] = fixed_name
                    fixes_applied = True

        if not fixes_applied:
            return False

        # Reconstruct file content
        new_content = "---\n"
        new_content += yaml.dump(fixed_frontmatter, default_flow_style=False, sort_keys=False)
        new_content += "---\n\n"
        if result.content:
            new_content += result.content

        # Write back
        try:
            file_path.write_text(new_content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"Failed to write fixes: {str(e)}")
            return False
