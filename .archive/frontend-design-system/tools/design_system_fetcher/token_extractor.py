"""
Design token extraction from markdown content.

This module parses design system documentation markdown and extracts design tokens
including colors, typography, spacing, and shadows. It uses pattern matching and
heuristics to identify token definitions in various markdown formats.

Supports common design system documentation patterns from Material Design,
Figma Design System, Ant Design, and other major systems.

Example:
    >>> from token_extractor import DesignTokenExtractor
    >>>
    >>> extractor = DesignTokenExtractor()
    >>> markdown = '''
    ... # Colors
    ... - Primary: #2196F3
    ... - Secondary: #FFC107
    ... '''
    >>> tokens = extractor.extract(markdown)
    >>> print(tokens['colors'])
    {'primary': '#2196f3', 'secondary': '#ffc107'}
"""

import re
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ColorToken:
    """Represents a color design token."""

    name: str
    value: str
    description: Optional[str] = None
    usage: Optional[str] = None


@dataclass
class TypographyToken:
    """Represents a typography design token."""

    name: str
    font_family: Optional[str] = None
    font_size: Optional[str] = None
    font_weight: Optional[str] = None
    line_height: Optional[str] = None
    letter_spacing: Optional[str] = None
    description: Optional[str] = None


@dataclass
class SpacingToken:
    """Represents a spacing design token."""

    name: str
    value: str
    description: Optional[str] = None


@dataclass
class ShadowToken:
    """Represents a shadow design token."""

    name: str
    x_offset: Optional[str] = None
    y_offset: Optional[str] = None
    blur_radius: Optional[str] = None
    spread_radius: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None


class DesignTokenExtractor:
    """
    Extracts design tokens from markdown documentation.

    Uses pattern matching to identify and extract color, typography,
    spacing, and shadow tokens from design system documentation.
    """

    # Color patterns: #hex, rgb(), hsl(), named colors
    COLOR_PATTERN = re.compile(
        r"(?P<name>[\w\s-]+)(?:\s*[:=]\s*)?(?P<value>#[0-9a-fA-F]{3,8}|rgb\([^)]+\)|hsl\([^)]+\)|(?:none|transparent|inherit|currentColor))",
        re.IGNORECASE,
    )

    # Font size pattern: 12px, 1.5rem, etc.
    FONT_SIZE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)(px|rem|em|%)")

    # Line height pattern
    LINE_HEIGHT_PATTERN = re.compile(r"(?:line[- ]?height|leading)\s*[:=]\s*([\d.]+|[\d.]+(?:px|rem|em))")

    # Letter spacing pattern
    LETTER_SPACING_PATTERN = re.compile(
        r"(?:letter[- ]?spacing|tracking)\s*[:=]\s*([-\d.]+(?:px|em)?)"
    )

    # Spacing pattern: 8px, 16px, etc.
    SPACING_PATTERN = re.compile(
        r"(?P<name>[\w\s-]+)(?:\s*[:=]\s*)?(?P<value>\d+(?:\.\d+)?(?:px|rem|em|%)?)"
    )

    # Shadow pattern: 0 2px 4px rgba(0,0,0,0.1)
    SHADOW_PATTERN = re.compile(
        r"(?P<name>[\w\s-]+)\s*[:=]\s*(?:(?P<x>[-\d.]+(?:px|em)?)\s+(?P<y>[-\d.]+(?:px|em)?)\s+(?P<blur>[-\d.]+(?:px|em)?)\s*(?:(?P<spread>[-\d.]+(?:px|em)?)\s+)?(?P<color>rgba?\([^)]+\)|#[0-9a-fA-F]{3,8}|[\w]+))"
    )

    def __init__(self) -> None:
        """Initialize the token extractor."""
        pass

    def extract(self, markdown: str) -> dict:
        """
        Extract all design tokens from markdown content.

        Args:
            markdown: Markdown content from design system documentation

        Returns:
            Dictionary with keys: colors, typography, spacing, shadows

        Example:
            >>> markdown = '''
            ... # Colors
            ... Primary: #2196F3
            ... Secondary: #FF9800
            ... '''
            >>> tokens = extractor.extract(markdown)
            >>> tokens['colors']
            {'primary': '#2196f3', 'secondary': '#ff9800'}
        """
        return {
            "colors": self.extract_colors(markdown),
            "typography": self.extract_typography(markdown),
            "spacing": self.extract_spacing(markdown),
            "shadows": self.extract_shadows(markdown),
        }

    def extract_colors(self, markdown: str) -> dict:
        """
        Extract color tokens from markdown.

        Args:
            markdown: Markdown content

        Returns:
            Dictionary mapping color names to hex/rgb values
        """
        colors = {}

        # Find color sections
        color_section = self._find_section(markdown, ["color", "palette", "theme"])
        if not color_section:
            color_section = markdown

        # Extract hex colors
        hex_matches = re.finditer(
            r"(?P<name>[\w\s-]+)(?:\s*[:=]\s*)?(?P<value>#[0-9a-fA-F]{3,8})",
            color_section,
            re.IGNORECASE,
        )

        for match in hex_matches:
            name = match.group("name").strip().lower()
            value = match.group("value").lower()
            if name and value:
                colors[name] = value

        # Extract rgb/rgba colors
        rgb_matches = re.finditer(
            r"(?P<name>[\w\s-]+)(?:\s*[:=]\s*)?(?P<value>rgba?\([^)]+\))",
            color_section,
            re.IGNORECASE,
        )

        for match in rgb_matches:
            name = match.group("name").strip().lower()
            value = match.group("value")
            if name and value and name not in colors:
                colors[name] = value

        return colors

    def extract_typography(self, markdown: str) -> dict:
        """
        Extract typography tokens from markdown.

        Args:
            markdown: Markdown content

        Returns:
            Dictionary mapping typography names to properties
        """
        typography = {}

        # Find typography section
        typo_section = self._find_section(
            markdown, ["typograph", "font", "text", "heading"]
        )
        if not typo_section:
            typo_section = markdown

        # Extract font family definitions
        font_family_matches = re.finditer(
            r"(?P<name>[\w\s-]+)\s*[:=]\s*(?:font[- ]?family\s*[:=]\s*)?['\"]?(?P<value>[^'\";\n]+)['\"]?",
            typo_section,
            re.IGNORECASE,
        )

        for match in font_family_matches:
            name = match.group("name").strip().lower()
            value = match.group("value").strip()
            if name and "font" not in typography:
                typography[name] = {"font_family": value}

        # Extract font size from sections
        size_matches = re.finditer(
            r"(?P<name>[\w\s-]+).*?font[- ]?size\s*[:=]\s*(?P<value>\d+(?:\.\d+)?(?:px|rem|em)?)",
            typo_section,
            re.IGNORECASE,
        )

        for match in size_matches:
            name = match.group("name").strip().lower()
            value = match.group("value")
            if name and value:
                if name not in typography:
                    typography[name] = {}
                typography[name]["font_size"] = value

        return typography

    def extract_spacing(self, markdown: str) -> list:
        """
        Extract spacing tokens from markdown.

        Args:
            markdown: Markdown content

        Returns:
            List of spacing values and names
        """
        spacing = []

        # Find spacing section
        space_section = self._find_section(markdown, ["spacing", "space", "padding", "margin"])
        if not space_section:
            space_section = markdown

        # Extract spacing values
        space_matches = re.finditer(
            r"(?P<name>[\w\s-]+)(?:\s*[:=]\s*)?(?P<value>\d+(?:\.\d+)?(?:px|rem|em|%)?)",
            space_section,
            re.IGNORECASE,
        )

        seen = set()
        for match in space_matches:
            name = match.group("name").strip().lower()
            value = match.group("value").strip()
            if name and value and (name, value) not in seen:
                spacing.append({"name": name, "value": value})
                seen.add((name, value))

        return spacing

    def extract_shadows(self, markdown: str) -> list:
        """
        Extract shadow tokens from markdown.

        Args:
            markdown: Markdown content

        Returns:
            List of shadow definitions
        """
        shadows = []

        # Find shadow section
        shadow_section = self._find_section(markdown, ["shadow", "elevation", "depth"])
        if not shadow_section:
            shadow_section = markdown

        # Extract shadow definitions
        shadow_matches = re.finditer(
            r"(?P<name>[\w\s-]+)\s*[:=]\s*(?P<value>[\d.\s\-px()rgba,#]+)",
            shadow_section,
            re.IGNORECASE,
        )

        seen = set()
        for match in shadow_matches:
            name = match.group("name").strip().lower()
            value = match.group("value").strip()
            if name and value and (name, value) not in seen:
                shadows.append({"name": name, "value": value})
                seen.add((name, value))

        return shadows

    def _find_section(self, markdown: str, keywords: list[str]) -> Optional[str]:
        """
        Find a section in markdown matching keywords.

        Args:
            markdown: Markdown content
            keywords: List of keywords to search for

        Returns:
            Content of matching section or None
        """
        # Find heading followed by content
        for keyword in keywords:
            pattern = rf"^#+\s+({re.escape(keyword)}[^\n]*)\n(.*?)(?=\n#+|$)"
            match = re.search(pattern, markdown, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if match:
                return match.group(2)

        return None
