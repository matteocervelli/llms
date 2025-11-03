#!/usr/bin/env python3
"""
Batch process story generation with parallel execution.

This script generates Markdown documentation for multiple stories
in parallel, providing progress tracking and error reporting.
"""

import sys
import logging
from pathlib import Path
from typing import List, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import yaml
import argparse
from tqdm import tqdm

# Import from generate_story_from_yaml
from generate_story_from_yaml import generate_story, load_config

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

# Project-wide paths
STORIES_YAML_DIR = PROJECT_ROOT / "stories" / "yaml-source"


def get_all_story_ids(config: dict) -> List[str]:
    """
    Get all story IDs from YAML directory.

    Args:
        config: Configuration dictionary

    Returns:
        List of story IDs
    """
    story_files = sorted(STORIES_YAML_DIR.glob("US-*.yaml"))

    story_ids = [f.stem for f in story_files]
    logger.info(f"Found {len(story_ids)} stories")

    return story_ids


def parse_story_ids(story_ids_str: str) -> List[str]:
    """
    Parse comma-separated story IDs.

    Args:
        story_ids_str: Comma-separated story IDs

    Returns:
        List of story IDs
    """
    return [sid.strip() for sid in story_ids_str.split(',') if sid.strip()]


def process_story_wrapper(args: Tuple[str, dict]) -> Tuple[str, bool, str]:
    """
    Wrapper function for parallel processing.

    Args:
        args: Tuple of (story_id, config)

    Returns:
        Tuple of (story_id, success, error_message)
    """
    story_id, config = args

    try:
        success = generate_story(story_id, config)
        return (story_id, success, "")
    except Exception as e:
        return (story_id, False, str(e))


def batch_generate_sequential(story_ids: List[str], config: dict) -> Tuple[int, int, List[str]]:
    """
    Generate stories sequentially with progress bar.

    Args:
        story_ids: List of story IDs to process
        config: Configuration dictionary

    Returns:
        Tuple of (success_count, total_count, failed_ids)
    """
    success_count = 0
    failed_ids = []

    with tqdm(total=len(story_ids), desc="Generating stories", unit="story") as pbar:
        for story_id in story_ids:
            try:
                success = generate_story(story_id, config)
                if success:
                    success_count += 1
                else:
                    failed_ids.append(story_id)
            except Exception as e:
                logger.error(f"Error processing {story_id}: {e}")
                failed_ids.append(story_id)

            pbar.update(1)

    return success_count, len(story_ids), failed_ids


def batch_generate_parallel(
    story_ids: List[str],
    config: dict,
    max_workers: int = 4
) -> Tuple[int, int, List[str]]:
    """
    Generate stories in parallel with progress bar.

    Args:
        story_ids: List of story IDs to process
        config: Configuration dictionary
        max_workers: Maximum number of parallel workers

    Returns:
        Tuple of (success_count, total_count, failed_ids)
    """
    success_count = 0
    failed_ids = []

    # Prepare arguments for parallel processing
    args_list = [(story_id, config) for story_id in story_ids]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(process_story_wrapper, args): args[0]
            for args in args_list
        }

        # Process results with progress bar
        with tqdm(total=len(story_ids), desc="Generating stories", unit="story") as pbar:
            for future in as_completed(futures):
                story_id = futures[future]
                try:
                    sid, success, error = future.result()

                    if success:
                        success_count += 1
                    else:
                        failed_ids.append(sid)
                        if error:
                            logger.error(f"Failed {sid}: {error}")

                except Exception as e:
                    logger.error(f"Error processing {story_id}: {e}")
                    failed_ids.append(story_id)

                pbar.update(1)

    return success_count, len(story_ids), failed_ids


def main() -> int:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Batch generate Markdown documentation from YAML story files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all stories in parallel
  %(prog)s --all

  # Generate specific stories
  %(prog)s --story-ids US-0001,US-0002,US-0003

  # Sequential processing (no parallel)
  %(prog)s --all --no-parallel

  # Control number of parallel workers
  %(prog)s --all --workers 8

  # Quiet mode (minimal output)
  %(prog)s --all --quiet
        """
    )

    # Story selection
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--all',
        action='store_true',
        help='Process all stories'
    )
    group.add_argument(
        '--story-ids',
        type=str,
        help='Comma-separated list of story IDs (e.g., US-0001,US-0002)'
    )

    # Processing options
    parser.add_argument(
        '--no-parallel',
        action='store_true',
        help='Disable parallel processing (sequential)'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of parallel workers (default: 4)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output (errors only)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose debug logging'
    )

    args = parser.parse_args()

    # Set logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Load configuration
        config = load_config()

        # Get story IDs
        if args.all:
            story_ids = get_all_story_ids(config)
        else:
            story_ids = parse_story_ids(args.story_ids)

        if not story_ids:
            logger.error("No stories to process")
            return 1

        logger.info(f"Processing {len(story_ids)} stories")

        # Generate stories
        if args.no_parallel:
            success_count, total_count, failed_ids = batch_generate_sequential(
                story_ids, config
            )
        else:
            success_count, total_count, failed_ids = batch_generate_parallel(
                story_ids, config, args.workers
            )

        # Report results
        print(f"\n{'='*60}")
        print(f"Batch Generation Complete")
        print(f"{'='*60}")
        print(f"Total: {total_count}")
        print(f"Success: {success_count}")
        print(f"Failed: {len(failed_ids)}")

        if failed_ids:
            print(f"\nFailed Stories:")
            for story_id in failed_ids:
                print(f"  - {story_id}")
            return 1

        print("\n✓ All stories generated successfully")
        return 0

    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
