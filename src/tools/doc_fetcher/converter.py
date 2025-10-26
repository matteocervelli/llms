"""
HTML to Markdown Converter

Converts HTML documentation to clean Markdown format with:
- HTML sanitization (security)
- Metadata extraction (title, description)
- Code block preservation
- Link and image handling
- Structural cleaning (navigation, footers)
"""

import logging
import re
from typing import Optional

from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md

from .exceptions import ConversionError

# Configure logging
logger = logging.getLogger(__name__)


class DocumentConverter:
    """
    Converts HTML documentation to Markdown.

    Features:
        - HTML sanitization to prevent XSS
        - Metadata extraction (title, description)
        - Structural cleaning (remove navigation, footers, ads)
        - Code block preservation
        - Link and image handling
        - Whitespace normalization
    """

    # Tags to remove (navigation, ads, tracking)
    REMOVE_TAGS = [
        "nav",
        "footer",
        "header",
        "aside",
        "script",
        "style",
        "noscript",
        "iframe",
        "form",
    ]

    # Classes/IDs that indicate non-content sections
    REMOVE_CLASSES = [
        "nav",
        "navigation",
        "sidebar",
        "footer",
        "header",
        "ad",
        "advertisement",
        "cookie",
        "banner",
        "social",
        "share",
        "comment",
        "related",
    ]

    # Attributes to remove for security (XSS prevention)
    REMOVE_ATTRS = ["onclick", "onload", "onerror", "onmouseover", "onfocus"]

    def __init__(self) -> None:
        """Initialize DocumentConverter."""
        logger.info("Initialized DocumentConverter")

    def _clean_html(self, html: str) -> BeautifulSoup:
        """
        Clean and sanitize HTML.

        Args:
            html: Raw HTML content

        Returns:
            BeautifulSoup object with cleaned HTML
        """
        soup = BeautifulSoup(html, "html.parser")

        # Remove dangerous tags
        for tag_name in self.REMOVE_TAGS:
            for tag in soup.find_all(tag_name):
                tag.decompose()

        # Remove elements with non-content classes/IDs
        for class_name in self.REMOVE_CLASSES:
            # Remove by class
            for tag in soup.find_all(class_=re.compile(class_name, re.I)):
                tag.decompose()
            # Remove by ID
            for tag in soup.find_all(id=re.compile(class_name, re.I)):
                tag.decompose()

        # Remove dangerous attributes (XSS prevention)
        for tag in soup.find_all():
            for attr in self.REMOVE_ATTRS:
                if attr in tag.attrs:
                    del tag.attrs[attr]

        return soup

    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> dict[str, Optional[str]]:
        """
        Extract metadata from HTML.

        Args:
            soup: BeautifulSoup object
            url: Source URL

        Returns:
            Dictionary with title and description
        """
        metadata: dict[str, Optional[str]] = {
            "title": None,
            "description": None,
        }

        # Extract title
        title_tag = soup.find("title")
        if title_tag:
            metadata["title"] = title_tag.get_text().strip()
        else:
            # Try h1 as fallback
            h1_tag = soup.find("h1")
            if h1_tag:
                metadata["title"] = h1_tag.get_text().strip()

        # Extract description from meta tags
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and isinstance(meta_desc, Tag):
            content = meta_desc.get("content")
            if content:
                metadata["description"] = str(content).strip()
        else:
            # Try Open Graph description
            og_desc = soup.find("meta", attrs={"property": "og:description"})
            if og_desc and isinstance(og_desc, Tag):
                content = og_desc.get("content")
                if content:
                    metadata["description"] = str(content).strip()

        logger.debug(f"Extracted metadata for {url}: {metadata}")
        return metadata

    def _find_main_content(self, soup: BeautifulSoup) -> Optional[Tag]:
        """
        Find main content area in HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            Main content tag or None
        """
        # Try common main content tags/selectors
        main_selectors = [
            {"name": "main"},
            {"name": "article"},
            {"class_": re.compile(r"(main|content|article|documentation|docs)", re.I)},
            {"id": re.compile(r"(main|content|article|documentation|docs)", re.I)},
            {"role": "main"},
        ]

        for selector in main_selectors:
            main = soup.find(**selector)  # type: ignore
            if main and isinstance(main, Tag):
                logger.debug(f"Found main content with selector: {selector}")
                return main

        # Fallback to body
        body = soup.find("body")
        if body and isinstance(body, Tag):
            return body

        return None

    def _normalize_whitespace(self, markdown: str) -> str:
        """
        Normalize whitespace in Markdown.

        Args:
            markdown: Raw markdown text

        Returns:
            Cleaned markdown with normalized whitespace
        """
        # Remove excessive blank lines (more than 2 consecutive)
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in markdown.split("\n")]
        markdown = "\n".join(lines)

        # Ensure single newline at end
        markdown = markdown.strip() + "\n"

        return markdown

    def convert(self, html: str, url: str) -> tuple[str, dict[str, Optional[str]]]:
        """
        Convert HTML to Markdown.

        Args:
            html: HTML content to convert
            url: Source URL (for error reporting and metadata)

        Returns:
            Tuple of (markdown_content, metadata)

        Raises:
            ConversionError: If conversion fails
        """
        try:
            logger.info(f"Converting HTML to Markdown for {url}")

            # Clean HTML
            soup = self._clean_html(html)

            # Extract metadata
            metadata = self._extract_metadata(soup, url)

            # Find main content
            main_content = self._find_main_content(soup)
            if not main_content:
                raise ConversionError(url, "Could not find main content area")

            # Convert to Markdown
            markdown = md(
                str(main_content),
                heading_style="ATX",  # Use # style headings
                bullets="-",  # Use - for bullets
                code_language_callback=lambda el: el.get("class", [""])[0].replace("language-", ""),
                strip=["script", "style"],
            )

            # Normalize whitespace
            markdown = self._normalize_whitespace(markdown)

            # Add metadata header
            if metadata["title"]:
                header = f"# {metadata['title']}\n\n"
                if metadata["description"]:
                    header += f"> {metadata['description']}\n\n"
                header += f"**Source**: {url}\n\n---\n\n"
                markdown = header + markdown

            logger.info(f"Successfully converted {url} to Markdown ({len(markdown)} characters)")
            return markdown, metadata

        except Exception as e:
            logger.error(f"Failed to convert {url}: {e}")
            raise ConversionError(url, str(e)) from e
