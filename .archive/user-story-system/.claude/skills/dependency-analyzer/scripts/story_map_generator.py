#!/usr/bin/env python3
"""
Generate story maps for visualization.

A story map organizes stories by epic and priority, providing
a visual overview of the product backlog. Supports multiple
output formats: Markdown table and Mermaid diagram.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
import yaml
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Base paths - calculate from script location
SKILL_DIR = Path(__file__).parent.parent  # parent of scripts/ directory
PROJECT_ROOT = SKILL_DIR.parent.parent.parent  # 3 levels up to project root

# Config paths (uses config from user-story-generator)
USER_STORY_GENERATOR_SKILL = SKILL_DIR.parent / "user-story-generator"
CONFIG_PATH = USER_STORY_GENERATOR_SKILL / "config" / "automation-config.yaml"

# Project-wide paths
STORIES_YAML_DIR = PROJECT_ROOT / "stories" / "yaml-source"
EPICS_DIR = PROJECT_ROOT / "epics"


def load_config() -> Dict:
    """Load configuration from YAML file."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def load_all_stories(config: Dict) -> List[Dict]:
    """Load all story YAML files."""
    story_files = sorted(STORIES_YAML_DIR.glob("US-*.yaml"))

    stories = []
    for story_file in story_files:
        try:
            with open(story_file, 'r') as f:
                story_data = yaml.safe_load(f)
                stories.append(story_data)
        except Exception as e:
            logger.error(f"Error loading {story_file}: {e}")

    logger.info(f"Loaded {len(stories)} stories")
    return stories


def load_all_epics(config: Dict) -> Dict[str, Dict]:
    """Load all epic YAML files."""
    epic_files = sorted(EPICS_DIR.glob("EP-*.yaml"))

    epics = {}
    for epic_file in epic_files:
        try:
            with open(epic_file, 'r') as f:
                epic_data = yaml.safe_load(f)
                epic_id = epic_data.get('id', epic_file.stem)
                epics[epic_id] = epic_data
        except Exception as e:
            logger.error(f"Error loading {epic_file}: {e}")

    logger.info(f"Loaded {len(epics)} epics")
    return epics


def group_stories_by_epic(stories: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group stories by epic.

    Args:
        stories: List of story data dictionaries

    Returns:
        Dict mapping epic_id to list of stories
    """
    grouped = defaultdict(list)

    for story in stories:
        epic_id = story.get('epic_id', 'No Epic')
        grouped[epic_id].append(story)

    return dict(grouped)


def get_priority_color(priority: str) -> str:
    """
    Get color for priority level.

    Args:
        priority: Priority level (low, medium, high, critical)

    Returns:
        Color name or hex code
    """
    colors = {
        'critical': '#FF0000',
        'high': '#FFA500',
        'medium': '#FFFF00',
        'low': '#90EE90'
    }
    return colors.get(priority, '#CCCCCC')


def get_status_emoji(status: str) -> str:
    """Get emoji for status."""
    emojis = {
        'draft': '📝',
        'backlog': '📋',
        'ready': '✅',
        'in_progress': '🔄',
        'blocked': '🚫',
        'in_review': '👀',
        'done': '✔️',
        'discarded': '❌'
    }
    return emojis.get(status, '❓')


def generate_markdown_table(
    stories: List[Dict],
    epics: Dict[str, Dict],
    epic_filter: Optional[str] = None
) -> str:
    """
    Generate Markdown table story map.

    Args:
        stories: List of story data
        epics: Dict of epic data
        epic_filter: Optional epic ID to filter by

    Returns:
        Markdown table as string
    """
    # Group by epic
    grouped = group_stories_by_epic(stories)

    # Filter if requested
    if epic_filter:
        if epic_filter in grouped:
            grouped = {epic_filter: grouped[epic_filter]}
        else:
            logger.warning(f"Epic {epic_filter} not found")
            return f"# Story Map\n\nNo stories found for epic {epic_filter}"

    lines = [
        "# Story Map",
        "",
        "## Overview",
        "",
        f"Total Stories: {len(stories)}",
        f"Total Epics: {len(grouped)}",
        ""
    ]

    # Generate table for each epic
    for epic_id, epic_stories in sorted(grouped.items()):
        # Epic header
        epic_title = epics.get(epic_id, {}).get('title', 'Unknown Epic')
        lines.append(f"## {epic_id}: {epic_title}")
        lines.append("")

        # Sort stories by priority and status
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_stories = sorted(
            epic_stories,
            key=lambda s: (
                priority_order.get(s.get('metadata', {}).get('priority', 'medium'), 2),
                s.get('id', '')
            )
        )

        # Table header
        lines.append("| ID | Title | Status | Priority | Points | Sprint |")
        lines.append("|---|---|---|---|---|---|")

        # Table rows
        for story in sorted_stories:
            story_id = story.get('id', 'Unknown')
            title = story.get('title', 'No title')
            metadata = story.get('metadata', {})
            status = metadata.get('status', 'draft')
            priority = metadata.get('priority', 'medium')
            points = metadata.get('story_points', '-')
            sprint = metadata.get('sprint', '-')

            status_emoji = get_status_emoji(status)

            lines.append(
                f"| {story_id} | {title} | {status_emoji} {status} | "
                f"{priority} | {points} | {sprint} |"
            )

        lines.append("")

        # Epic summary
        total_points = sum(
            s.get('metadata', {}).get('story_points', 0) or 0
            for s in epic_stories
        )
        done_stories = [
            s for s in epic_stories
            if s.get('metadata', {}).get('status') == 'done'
        ]
        done_points = sum(
            s.get('metadata', {}).get('story_points', 0) or 0
            for s in done_stories
        )

        lines.append(f"**Epic Summary:**")
        lines.append(f"- Stories: {len(epic_stories)}")
        lines.append(f"- Total Points: {total_points}")
        lines.append(f"- Completed: {len(done_stories)} stories ({done_points} points)")
        lines.append("")

    return "\n".join(lines)


def generate_mermaid_diagram(
    stories: List[Dict],
    epics: Dict[str, Dict],
    epic_filter: Optional[str] = None
) -> str:
    """
    Generate Mermaid diagram story map.

    Args:
        stories: List of story data
        epics: Dict of epic data
        epic_filter: Optional epic ID to filter by

    Returns:
        Mermaid diagram as string
    """
    # Group by epic
    grouped = group_stories_by_epic(stories)

    # Filter if requested
    if epic_filter:
        if epic_filter in grouped:
            grouped = {epic_filter: grouped[epic_filter]}
        else:
            logger.warning(f"Epic {epic_filter} not found")
            return "graph TD\n    NoStories[No stories found]"

    lines = ["graph TD"]

    # Create epic nodes and story nodes
    for epic_id, epic_stories in sorted(grouped.items()):
        epic_title = epics.get(epic_id, {}).get('title', 'Unknown Epic')

        # Epic node
        epic_node = epic_id.replace('-', '_')
        lines.append(f"    {epic_node}[\"{epic_id}: {epic_title}\"]")

        # Story nodes
        for story in epic_stories:
            story_id = story.get('id', 'Unknown')
            title = story.get('title', 'No title')[:30]  # Truncate long titles
            metadata = story.get('metadata', {})
            priority = metadata.get('priority', 'medium')
            status = metadata.get('status', 'draft')

            story_node = story_id.replace('-', '_')

            # Create story node with truncated title
            lines.append(f"    {story_node}[\"{story_id}: {title}...\"]")

            # Link epic to story
            lines.append(f"    {epic_node} --> {story_node}")

            # Color by priority
            color = get_priority_color(priority)
            lines.append(f"    style {story_node} fill:{color}")

        # Style epic node
        lines.append(f"    style {epic_node} fill:#E0E0E0,stroke:#333,stroke-width:2px")

    return "\n".join(lines)


def main() -> int:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Generate story maps for visualization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Output Formats:
  md       - Markdown table with epic grouping
  mermaid  - Mermaid diagram with color coding by priority

Examples:
  # Generate Markdown table
  %(prog)s --format md

  # Generate Mermaid diagram
  %(prog)s --format mermaid

  # Filter by epic
  %(prog)s --format md --epic EP-001

  # Save to file
  %(prog)s --format md --output story-map.md
        """
    )

    parser.add_argument(
        '--format',
        choices=['md', 'mermaid'],
        default='md',
        help='Output format (default: md)'
    )

    parser.add_argument(
        '--epic',
        type=str,
        help='Filter by epic ID (e.g., EP-001)'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (prints to stdout if not specified)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose debug logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Load configuration
        config = load_config()

        # Load data
        stories = load_all_stories(config)
        epics = load_all_epics(config)

        if not stories:
            logger.error("No stories found")
            return 1

        # Generate map
        if args.format == 'md':
            output = generate_markdown_table(stories, epics, args.epic)
        else:
            output = generate_mermaid_diagram(stories, epics, args.epic)

        # Write output
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w') as f:
                f.write(output)

            logger.info(f"Story map written to {output_path}")
        else:
            print(output)

        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
