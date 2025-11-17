"""
Design token schema validation.

Validates design system files against the expected schema to ensure
all required fields and proper structure before import.
"""

from typing import Any, Optional


class DesignTokenValidator:
    """Validates design token schemas."""

    # Required top-level fields
    REQUIRED_FIELDS = {"name", "tokens"}

    # Required token categories
    REQUIRED_TOKEN_CATEGORIES = {"colors", "typography", "spacing", "shadows"}

    # Optional top-level fields
    OPTIONAL_FIELDS = {"version", "description", "author", "license"}

    @classmethod
    def validate(cls, data: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Validate design system data against schema.

        Args:
            data: Design system dictionary to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors: list[str] = []

        # Check required top-level fields
        for field in cls.REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"Missing required field: '{field}'")

        if errors:
            return False, errors

        # Validate name
        if not isinstance(data.get("name"), str) or not data["name"].strip():
            errors.append("'name' must be a non-empty string")

        # Validate tokens structure
        tokens = data.get("tokens", {})
        if not isinstance(tokens, dict):
            errors.append("'tokens' must be a dictionary")
            return False, errors

        # Check token categories exist
        for category in cls.REQUIRED_TOKEN_CATEGORIES:
            if category not in tokens:
                errors.append(f"Missing required token category: '{category}'")

        # Validate token category structures
        colors = tokens.get("colors", {})
        if not isinstance(colors, dict):
            errors.append("'tokens.colors' must be a dictionary")

        typography = tokens.get("typography", {})
        if not isinstance(typography, dict):
            errors.append("'tokens.typography' must be a dictionary")

        spacing = tokens.get("spacing", [])
        if not isinstance(spacing, (list, dict)):
            errors.append("'tokens.spacing' must be a list or dictionary")

        shadows = tokens.get("shadows", [])
        if not isinstance(shadows, (list, dict)):
            errors.append("'tokens.shadows' must be a list or dictionary")

        # Validate optional fields if present
        if "version" in data and not isinstance(data["version"], str):
            errors.append("'version' must be a string if provided")

        if "description" in data and not isinstance(data["description"], str):
            errors.append("'description' must be a string if provided")

        return len(errors) == 0, errors

    @classmethod
    def get_schema(cls) -> dict[str, Any]:
        """
        Get the expected schema for design systems.

        Returns:
            Dictionary describing the schema
        """
        return {
            "name": "Design System Schema",
            "required": list(cls.REQUIRED_FIELDS),
            "optional": list(cls.OPTIONAL_FIELDS),
            "token_categories": list(cls.REQUIRED_TOKEN_CATEGORIES),
            "example": {
                "name": "My Custom Design",
                "version": "1.0.0",
                "description": "My custom design system",
                "tokens": {
                    "colors": {
                        "primary": "#007AFF",
                        "secondary": "#5AC8FA",
                    },
                    "typography": {
                        "heading": {
                            "font": "Helvetica",
                            "size": "32px",
                            "weight": "bold",
                        },
                        "body": {
                            "font": "Helvetica",
                            "size": "16px",
                            "weight": "regular",
                        },
                    },
                    "spacing": [4, 8, 16, 24, 32, 48, 64],
                    "shadows": [
                        {"blur": 2, "offset": 1, "color": "rgba(0,0,0,0.1)"},
                        {"blur": 8, "offset": 4, "color": "rgba(0,0,0,0.15)"},
                    ],
                },
            },
        }
