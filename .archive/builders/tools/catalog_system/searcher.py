"""
Searcher component for catalog system.

Provides search and filter capabilities for catalog entries with:
- Text-based search across name and description
- Scoring algorithm (exact=100, prefix=75, contains=50, fuzzy=25)
- Scope filtering (global/project/local)
- Type filtering (skill/command/agent)

Example Usage:
    >>> from src.tools.catalog_system.searcher import Searcher
    >>> from src.tools.catalog_system.models import SkillCatalogEntry
    >>>
    >>> searcher = Searcher()
    >>> results = searcher.search(entries, "python")
    >>> for entry, score in results:
    ...     print(f"{entry.name} (score: {score})")
"""

from typing import List, Tuple
from .models import (
    CatalogEntry,
    SkillCatalogEntry,
    CommandCatalogEntry,
    AgentCatalogEntry,
)


class Searcher:
    """
    Provides search and filter operations for catalog entries.

    The Searcher implements a weighted scoring system:
    - Exact match: 100 points
    - Prefix match: 75 points
    - Contains match: 50 points
    - Fuzzy match: 25 points (optional, for typo tolerance)

    Searches are case-insensitive and search both name and description fields.
    """

    # Scoring constants
    SCORE_EXACT = 100
    SCORE_PREFIX = 75
    SCORE_CONTAINS = 50
    SCORE_FUZZY = 25

    def __init__(self) -> None:
        """Initialize the Searcher."""
        pass

    def search(
        self,
        entries: List[CatalogEntry],
        query: str,
    ) -> List[Tuple[CatalogEntry, int]]:
        """
        Search catalog entries by query string with scoring.

        Searches both name and description fields. Returns results sorted by
        score (highest first).

        Args:
            entries: List of catalog entries to search
            query: Search query string (case-insensitive)

        Returns:
            List of (entry, score) tuples sorted by score descending

        Example:
            >>> searcher = Searcher()
            >>> results = searcher.search(skills, "python")
            >>> for entry, score in results:
            ...     print(f"{entry.name}: {score}")
            python-tester: 100
            pytest-runner: 50
        """
        if not query:
            # Empty query returns all entries with neutral score
            return [(entry, 50) for entry in entries]

        query_lower = query.lower().strip()
        scored_results: List[Tuple[CatalogEntry, int]] = []

        for entry in entries:
            score = self._calculate_score(entry, query_lower)
            if score > 0:
                scored_results.append((entry, score))

        # Sort by score descending, then by name ascending for ties
        scored_results.sort(key=lambda x: (-x[1], x[0].name))

        return scored_results

    def filter_by_scope(
        self,
        entries: List[CatalogEntry],
        scope: str,
    ) -> List[CatalogEntry]:
        """
        Filter catalog entries by scope.

        Args:
            entries: List of catalog entries to filter
            scope: Scope to filter by ("global", "project", "local", or "all")

        Returns:
            List of entries matching the scope

        Example:
            >>> searcher = Searcher()
            >>> global_skills = searcher.filter_by_scope(all_skills, "global")
        """
        if scope == "all":
            return entries

        # Validate scope
        valid_scopes = {"global", "project", "local"}
        if scope not in valid_scopes:
            return []

        return [entry for entry in entries if entry.scope == scope]

    def filter_by_type(
        self,
        entries: List[CatalogEntry],
        entry_type: str,
    ) -> List[CatalogEntry]:
        """
        Filter catalog entries by type.

        Args:
            entries: List of catalog entries to filter
            entry_type: Type to filter by
                       ("skill", "command", "agent", or "all")

        Returns:
            List of entries matching the type

        Example:
            >>> searcher = Searcher()
            >>> skills = searcher.filter_by_type(all_entries, "skill")
        """
        if entry_type == "all":
            return entries

        # Map type strings to entry classes
        type_map = {
            "skill": SkillCatalogEntry,
            "command": CommandCatalogEntry,
            "agent": AgentCatalogEntry,
        }

        entry_class = type_map.get(entry_type)
        if not entry_class:
            return []

        return [entry for entry in entries if isinstance(entry, entry_class)]

    def _calculate_score(self, entry: CatalogEntry, query_lower: str) -> int:
        """
        Calculate relevance score for an entry against a query.

        Scoring algorithm:
        - Exact match in name: 100
        - Prefix match in name: 75
        - Contains match in name: 50
        - Exact match in description: 75
        - Contains match in description: 50
        - Fuzzy match: 25 (basic implementation)

        Args:
            entry: Catalog entry to score
            query_lower: Lowercase query string

        Returns:
            Score (0-100), higher is better match
        """
        name_lower = entry.name.lower()
        desc_lower = entry.description.lower()

        # Exact match in name (highest priority)
        if name_lower == query_lower:
            return self.SCORE_EXACT

        # Prefix match in name
        if name_lower.startswith(query_lower):
            return self.SCORE_PREFIX

        # Contains match in name
        if query_lower in name_lower:
            return self.SCORE_CONTAINS

        # Exact match in description
        if desc_lower == query_lower:
            return self.SCORE_PREFIX

        # Contains match in description
        if query_lower in desc_lower:
            return self.SCORE_CONTAINS

        # Fuzzy match (basic: check if most characters present)
        if self._fuzzy_match(name_lower, query_lower):
            return self.SCORE_FUZZY

        if self._fuzzy_match(desc_lower, query_lower):
            return self.SCORE_FUZZY

        # No match
        return 0

    def _fuzzy_match(self, text: str, query: str) -> bool:
        """
        Basic fuzzy matching - checks if most query characters
        appear in text.

        This is a simple implementation. For production, consider using
        a library like python-Levenshtein or difflib for better fuzzy
        matching.

        Args:
            text: Text to search in
            query: Query to fuzzy match

        Returns:
            True if fuzzy match found, False otherwise
        """
        if not query or not text:
            return False

        # Count how many query characters appear in text (in order)
        text_idx = 0
        matched = 0

        for char in query:
            # Find next occurrence of this character in text
            idx = text.find(char, text_idx)
            if idx != -1:
                matched += 1
                text_idx = idx + 1

        # Consider it a fuzzy match if 70% of characters matched
        threshold = len(query) * 0.7
        return matched >= threshold
