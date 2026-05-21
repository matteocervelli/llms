#!/usr/bin/env python3
"""
Generate Markdown documentation from YAML story files.

This script loads user story YAML files and renders them to Markdown
using Jinja2 templates. It supports both single story generation and
batch processing of all stories.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from models import UserStory

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

# Config and template paths within skill
CONFIG_PATH = SKILL_DIR / "config" / "automation-config.yaml"
TEMPLATES_DIR = SKILL_DIR / "templates"

# Project-wide paths
STORIES_YAML_DIR = PROJECT_ROOT / "stories" / "yaml-source"
STORIES_MD_DIR = PROJECT_ROOT / "stories" / "generated-docs"


def load_config() -> Dict:
    """
    Load configuration from YAML file.

    Returns:
        Dict: Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")

    try:
        with open(CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)
        logger.debug(f"Loaded configuration from {CONFIG_PATH}")
        return config
    except yaml.YAMLError as e:
        logger.error(f"Error parsing config file: {e}")
        raise


def load_story_yaml(story_path: Path) -> Dict:
    """
    Load and validate a YAML story file.

    Args:
        story_path: Path to the YAML story file

    Returns:
        Dict: Story data dictionary

    Raises:
        FileNotFoundError: If story file doesn't exist
        yaml.YAMLError: If YAML is invalid
        ValueError: If story data is invalid
    """
    if not story_path.exists():
        raise FileNotFoundError(f"Story file not found: {story_path}")

    try:
        with open(story_path, 'r') as f:
            story_data = yaml.safe_load(f)

        # Validate using Pydantic model
        try:
            UserStory(**story_data)
        except Exception as e:
            logger.warning(f"Story validation warning for {story_path.name}: {e}")

        logger.debug(f"Loaded story from {story_path}")
        return story_data

    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {story_path}: {e}")
        raise


def render_story_markdown(story_data: Dict, template_path: Path) -> str:
    """
    Render story data to Markdown using Jinja2 template.

    Args:
        story_data: Story data dictionary
        template_path: Path to Jinja2 template file

    Returns:
        str: Rendered Markdown content

    Raises:
        TemplateNotFound: If template file doesn't exist
        Exception: If rendering fails
    """
    try:
        env = Environment(
            loader=FileSystemLoader(template_path.parent),
            trim_blocks=True,
            lstrip_blocks=True
        )
        template = env.get_template(template_path.name)

        rendered = template.render(**story_data)
        logger.debug(f"Rendered template {template_path.name}")
        return rendered

    except TemplateNotFound:
        logger.error(f"Template not found: {template_path}")
        raise
    except Exception as e:
        logger.error(f"Error rendering template: {e}")
        raise


def write_markdown_atomic(content: str, output_path: Path) -> None:
    """
    Write Markdown content to file atomically.

    Uses atomic write pattern: write to temp file, then rename.
    This prevents corruption if process is interrupted.

    Args:
        content: Markdown content to write
        output_path: Destination file path

    Raises:
        IOError: If write fails
    """
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write to temporary file
    temp_path = output_path.with_suffix('.tmp')

    try:
        with open(temp_path, 'w') as f:
            f.write(content)

        # Atomic rename
        temp_path.rename(output_path)
        logger.info(f"Written: {output_path}")

    except Exception as e:
        # Clean up temp file on error
        if temp_path.exists():
            temp_path.unlink()
        logger.error(f"Error writing file {output_path}: {e}")
        raise


def generate_story(story_id: str, config: Dict) -> bool:
    """
    Generate Markdown documentation for a single story.

    Args:
        story_id: Story ID (e.g., "US-0001")
        config: Configuration dictionary

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Build paths using project root
        story_yaml_path = STORIES_YAML_DIR / f"{story_id}.yaml"
        story_md_path = STORIES_MD_DIR / f"{story_id}.md"

        # Load story
        logger.info(f"Processing story: {story_id}")
        story_data = load_story_yaml(story_yaml_path)

        # Render template
        template_name = config['templates']['markdown']['story_template']
        template_path = TEMPLATES_DIR / template_name
        markdown_content = render_story_markdown(story_data, template_path)

        # Write output
        write_markdown_atomic(markdown_content, story_md_path)

        return True

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return False
    except Exception as e:
        logger.error(f"Error generating story {story_id}: {e}")
        return False


def generate_all_stories(config: Dict) -> tuple[int, int]:
    """
    Generate Markdown documentation for all stories.

    Args:
        config: Configuration dictionary

    Returns:
        tuple: (success_count, total_count)
    """
    # Find all YAML story files using project root path
    story_files = sorted(STORIES_YAML_DIR.glob("US-*.yaml"))

    if not story_files:
        logger.warning(f"No story files found in {STORIES_YAML_DIR}")
        return 0, 0

    logger.info(f"Found {len(story_files)} story files")

    success_count = 0
    for story_file in story_files:
        story_id = story_file.stem
        if generate_story(story_id, config):
            success_count += 1

    return success_count, len(story_files)


def main() -> int:
    """
    Main entry point with argument parsing.

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description='Generate Markdown documentation from YAML story files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate single story
  %(prog)s --story-id US-0001

  # Generate all stories
  %(prog)s --all

  # Enable debug logging
  %(prog)s --all --verbose
        """
    )

    # Arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--story-id',
        type=str,
        help='Generate single story by ID (e.g., US-0001)'
    )
    group.add_argument(
        '--all',
        action='store_true',
        help='Generate all stories'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose debug logging'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Load configuration
        config = load_config()

        # Generate stories
        if args.story_id:
            success = generate_story(args.story_id, config)
            if success:
                logger.info(f"Successfully generated {args.story_id}")
                return 0
            else:
                logger.error(f"Failed to generate {args.story_id}")
                return 1

        elif args.all:
            success_count, total_count = generate_all_stories(config)
            logger.info(f"Generated {success_count}/{total_count} stories")

            if success_count == total_count:
                return 0
            elif success_count > 0:
                logger.warning(f"Some stories failed: {total_count - success_count} errors")
                return 1
            else:
                logger.error("All stories failed to generate")
                return 1

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
