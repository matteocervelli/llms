"""
Design System Fetcher - Tool for extracting design tokens from design system documentation.

This module provides functionality to fetch design system documentation from URLs,
extract design tokens (colors, typography, spacing, shadows), and save them with
metadata for later reference and analysis.

Main Components:
    - fetcher: Core fetching logic using DocumentationCrawler
    - token_extractor: Extract design tokens from markdown content
    - storage: Save tokens and metadata to disk
"""

from .fetcher import DesignSystemFetcher
from .token_extractor import DesignTokenExtractor

__all__ = ["DesignSystemFetcher", "DesignTokenExtractor"]
