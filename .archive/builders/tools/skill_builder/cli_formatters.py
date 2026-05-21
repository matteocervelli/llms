"""
CLI formatting functions for Skill Builder.

Provides formatting utilities for displaying skill information in the CLI.
"""

from .models import SkillCatalogEntry, ScopeType


def format_scope_badge(scope: ScopeType) -> str:
    """Format scope with emoji badge."""
    badges = {
        ScopeType.GLOBAL: "🌐",
        ScopeType.PROJECT: "📁",
        ScopeType.LOCAL: "🔒",
    }
    return f"{badges.get(scope, '❓')} {scope.value}"


def format_skill_entry(entry: SkillCatalogEntry, show_path: bool = False) -> str:
    """Format skill catalog entry for display."""
    lines = []

    # Name and scope
    scope_badge = format_scope_badge(entry.scope)
    lines.append(f"  {entry.name} ({scope_badge})")

    # Description
    if entry.description:
        lines.append(f"    {entry.description}")

    # Metadata
    meta_parts = []
    if entry.metadata:
        if entry.metadata.get("template"):
            meta_parts.append(f"template:{entry.metadata['template']}")
        if entry.metadata.get("has_scripts"):
            meta_parts.append("scripts")
        if entry.metadata.get("allowed_tools"):
            tool_count = len(entry.metadata["allowed_tools"])
            meta_parts.append(f"{tool_count} tools")

    if meta_parts:
        lines.append(f"    💡 {', '.join(meta_parts)}")

    # Path (optional)
    if show_path and entry.path:
        lines.append(f"    📂 {entry.path}")

    return "\n".join(lines)
