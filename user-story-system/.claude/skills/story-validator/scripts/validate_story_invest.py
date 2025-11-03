#!/usr/bin/env python3
"""
Validate user stories against INVEST criteria.

INVEST stands for:
- Independent: Story should be self-contained
- Negotiable: Details can be discussed
- Valuable: Delivers business value
- Estimable: Can be estimated
- Small: Can be completed in one sprint
- Testable: Has clear acceptance criteria

This script validates stories and provides actionable feedback.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import yaml
import argparse

# Add user-story-generator scripts to path for models import
USER_STORY_GENERATOR_SCRIPTS = Path(__file__).parent.parent.parent / "user-story-generator" / "scripts"
sys.path.insert(0, str(USER_STORY_GENERATOR_SCRIPTS))
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

# Config paths within skill (validator uses config from user-story-generator)
USER_STORY_GENERATOR_SKILL = SKILL_DIR.parent / "user-story-generator"
CONFIG_PATH = USER_STORY_GENERATOR_SKILL / "config" / "automation-config.yaml"

# Project-wide paths
STORIES_YAML_DIR = PROJECT_ROOT / "stories" / "yaml-source"


def load_config() -> Dict:
    """Load configuration from YAML file."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def load_story(story_id: str, config: Dict) -> Dict:
    """Load story YAML file."""
    story_path = STORIES_YAML_DIR / f"{story_id}.yaml"

    if not story_path.exists():
        raise FileNotFoundError(f"Story file not found: {story_path}")

    with open(story_path, 'r') as f:
        return yaml.safe_load(f)


def check_independent(story_data: Dict, config: Dict) -> Tuple[bool, List[str]]:
    """
    Check if story is independent.

    A story is independent if:
    - It has minimal blocking dependencies
    - It can be developed without waiting for other stories

    Args:
        story_data: Story data dictionary
        config: Configuration dictionary

    Returns:
        Tuple of (passed, issues)
    """
    issues = []
    dependencies = story_data.get('dependencies', {})
    blocked_by = dependencies.get('blocked_by', [])

    if not config['validation']['invest']['criteria']['independent']['enabled']:
        return True, []

    if blocked_by:
        issues.append(
            f"Story is blocked by {len(blocked_by)} other stories: "
            f"{', '.join(blocked_by)}. Consider reducing dependencies."
        )
        return False, issues

    return True, []


def check_negotiable(story_data: Dict, config: Dict) -> Tuple[bool, List[str]]:
    """
    Check if story is negotiable.

    A story is negotiable if:
    - It doesn't contain overly specific implementation details
    - It focuses on the "what" not the "how"
    - It allows for discussion and options

    Args:
        story_data: Story data dictionary
        config: Configuration dictionary

    Returns:
        Tuple of (passed, issues)
    """
    issues = []

    if not config['validation']['invest']['criteria']['negotiable']['enabled']:
        return True, []

    # Check for rigid language in the "i_want" field
    story_content = story_data.get('story', {})
    i_want = story_content.get('i_want', '').lower()

    rigid_phrases = [
        'must use', 'must implement', 'using exactly',
        'specifically with', 'only with', 'implemented as'
    ]

    found_rigid = [phrase for phrase in rigid_phrases if phrase in i_want]

    if found_rigid:
        issues.append(
            f"Story contains rigid requirements: {', '.join(found_rigid)}. "
            "Consider making the story more flexible to allow for discussion."
        )
        return False, issues

    return True, []


def check_valuable(story_data: Dict, config: Dict) -> Tuple[bool, List[str]]:
    """
    Check if story delivers value.

    A story is valuable if:
    - It has a clear "so that" benefit
    - The benefit is specific and measurable
    - It delivers value to a user or business

    Args:
        story_data: Story data dictionary
        config: Configuration dictionary

    Returns:
        Tuple of (passed, issues)
    """
    issues = []

    if not config['validation']['invest']['criteria']['valuable']['enabled']:
        return True, []

    story_content = story_data.get('story', {})
    so_that = story_content.get('so_that', '').strip()

    if not so_that:
        issues.append(
            "Story is missing 'so_that' benefit. "
            "Add a clear explanation of the value this story delivers."
        )
        return False, issues

    # Check if the benefit is too vague
    vague_phrases = [
        'to improve', 'to enhance', 'to make better',
        'for future use', 'for flexibility'
    ]

    if any(phrase in so_that.lower() for phrase in vague_phrases):
        if len(so_that) < 50:  # Short and vague
            issues.append(
                "Story benefit is vague. Be specific about "
                "what improvement or value is being delivered."
            )
            return False, issues

    return True, []


def check_estimable(story_data: Dict, config: Dict) -> Tuple[bool, List[str]]:
    """
    Check if story is estimable.

    A story is estimable if:
    - It has story points assigned
    - It has clear acceptance criteria
    - The scope is well-defined

    Args:
        story_data: Story data dictionary
        config: Configuration dictionary

    Returns:
        Tuple of (passed, issues)
    """
    issues = []

    if not config['validation']['invest']['criteria']['estimable']['enabled']:
        return True, []

    metadata = story_data.get('metadata', {})
    story_points = metadata.get('story_points')

    if story_points is None:
        issues.append(
            "Story has no story points. Estimate the effort required "
            "using Fibonacci sequence (1, 2, 3, 5, 8, 13)."
        )
        return False, issues

    # Check if acceptance criteria exist
    acceptance_criteria = story_data.get('acceptance_criteria', [])
    if not acceptance_criteria or len(acceptance_criteria) == 0:
        issues.append(
            "Story lacks acceptance criteria, making it hard to estimate. "
            "Add clear Given/When/Then criteria."
        )
        return False, issues

    return True, []


def check_small(story_data: Dict, config: Dict) -> Tuple[bool, List[str]]:
    """
    Check if story is small enough.

    A story is small if:
    - Story points are within acceptable range
    - It can be completed within one sprint

    Args:
        story_data: Story data dictionary
        config: Configuration dictionary

    Returns:
        Tuple of (passed, issues)
    """
    issues = []

    if not config['validation']['invest']['criteria']['small']['enabled']:
        return True, []

    metadata = story_data.get('metadata', {})
    story_points = metadata.get('story_points')
    max_points = config['validation']['invest']['criteria']['small']['max_story_points']

    if story_points is None:
        # Can't check size without points
        return True, []

    if story_points > max_points:
        issues.append(
            f"Story is too large ({story_points} points > {max_points} max). "
            "Consider breaking it down into smaller stories."
        )
        return False, issues

    return True, []


def check_testable(story_data: Dict, config: Dict) -> Tuple[bool, List[str]]:
    """
    Check if story is testable.

    A story is testable if:
    - It has acceptance criteria
    - Criteria use Given/When/Then format
    - Criteria are specific and verifiable

    Args:
        story_data: Story data dictionary
        config: Configuration dictionary

    Returns:
        Tuple of (passed, issues)
    """
    issues = []

    if not config['validation']['invest']['criteria']['testable']['enabled']:
        return True, []

    acceptance_criteria = story_data.get('acceptance_criteria', [])
    min_criteria = config['validation']['invest']['criteria']['testable']['min_acceptance_criteria']

    if not acceptance_criteria or len(acceptance_criteria) < min_criteria:
        issues.append(
            f"Story needs at least {min_criteria} acceptance criterion. "
            "Add clear Given/When/Then criteria that can be tested."
        )
        return False, issues

    # Check format of acceptance criteria
    for i, criterion in enumerate(acceptance_criteria, 1):
        given = criterion.get('given', '').strip()
        when = criterion.get('when', '').strip()
        then = criterion.get('then', '').strip()

        if not given or not when or not then:
            issues.append(
                f"Acceptance criterion #{i} is incomplete. "
                "Ensure all criteria have Given, When, and Then parts."
            )
            return False, issues

    return True, []


def calculate_invest_score(results: Dict[str, Tuple[bool, List[str]]]) -> int:
    """
    Calculate overall INVEST score.

    Args:
        results: Dictionary of criterion name to (passed, issues) tuple

    Returns:
        int: Score from 0-100
    """
    passed_count = sum(1 for passed, _ in results.values() if passed)
    total_count = len(results)

    if total_count == 0:
        return 0

    return int((passed_count / total_count) * 100)


def validate_story(story_id: str, config: Dict, strict: bool = False) -> Dict:
    """
    Validate a story against INVEST criteria.

    Args:
        story_id: Story ID to validate
        config: Configuration dictionary
        strict: If True, require all criteria to pass

    Returns:
        Dict: Validation report
    """
    logger.info(f"Validating story: {story_id}")

    try:
        # Load story
        story_data = load_story(story_id, config)

        # Run all checks
        results = {
            'independent': check_independent(story_data, config),
            'negotiable': check_negotiable(story_data, config),
            'valuable': check_valuable(story_data, config),
            'estimable': check_estimable(story_data, config),
            'small': check_small(story_data, config),
            'testable': check_testable(story_data, config)
        }

        # Calculate score
        invest_score = calculate_invest_score(results)

        # Collect all issues
        all_issues = []
        criteria_status = {}

        for criterion, (passed, issues) in results.items():
            criteria_status[criterion] = passed
            all_issues.extend(issues)

        # Build report
        report = {
            'story_id': story_id,
            'invest_score': invest_score,
            'criteria': criteria_status,
            'passed': invest_score == 100 or (not strict and invest_score >= 50),
            'issues': all_issues,
            'timestamp': datetime.now().isoformat()
        }

        # Log results
        if report['passed']:
            logger.info(f"✓ Story {story_id} passed validation (score: {invest_score}/100)")
        else:
            logger.warning(f"✗ Story {story_id} failed validation (score: {invest_score}/100)")
            for issue in all_issues:
                logger.warning(f"  - {issue}")

        return report

    except FileNotFoundError as e:
        logger.error(f"Story not found: {e}")
        return {
            'story_id': story_id,
            'error': str(e),
            'passed': False
        }
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return {
            'story_id': story_id,
            'error': str(e),
            'passed': False
        }


def save_validation_to_story(story_id: str, report: Dict, config: Dict) -> None:
    """
    Save validation results back to story YAML file.

    Args:
        story_id: Story ID
        report: Validation report
        config: Configuration dictionary
    """
    story_path = STORIES_YAML_DIR / f"{story_id}.yaml"

    try:
        # Load existing story
        with open(story_path, 'r') as f:
            story_data = yaml.safe_load(f)

        # Update validation section
        if 'validation' not in story_data:
            story_data['validation'] = {}

        story_data['validation']['invest_score'] = report['invest_score']
        story_data['validation']['invest_criteria'] = report['criteria']
        story_data['validation']['last_validated'] = report['timestamp']
        story_data['validation']['validation_issues'] = report['issues']

        # Write back atomically
        temp_path = story_path.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)

        temp_path.rename(story_path)
        logger.info(f"Updated validation results in {story_id}.yaml")

    except Exception as e:
        logger.error(f"Failed to save validation results: {e}")


def main() -> int:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Validate user stories against INVEST criteria',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
INVEST Criteria:
  Independent - Story is self-contained with minimal dependencies
  Negotiable  - Details can be discussed, focuses on "what" not "how"
  Valuable    - Delivers clear business or user value
  Estimable   - Can be estimated with story points
  Small       - Can be completed within one sprint
  Testable    - Has clear, verifiable acceptance criteria

Examples:
  # Validate single story
  %(prog)s --story-id US-0001

  # Strict validation (all criteria must pass)
  %(prog)s --story-id US-0001 --strict

  # Output as JSON
  %(prog)s --story-id US-0001 --output json

  # Save results back to YAML
  %(prog)s --story-id US-0001 --save
        """
    )

    parser.add_argument(
        '--story-id',
        type=str,
        required=True,
        help='Story ID to validate (e.g., US-0001)'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Require all criteria to pass (default: 50%% threshold)'
    )

    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--save',
        action='store_true',
        help='Save validation results back to story YAML'
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

        # Validate story
        report = validate_story(args.story_id, config, args.strict)

        # Output results
        if args.output == 'json':
            print(json.dumps(report, indent=2))
        else:
            # Text output
            print(f"\nValidation Report: {report['story_id']}")
            print("=" * 60)

            if 'error' in report:
                print(f"\nError: {report['error']}")
                return 1

            print(f"\nINVEST Score: {report['invest_score']}/100")
            print(f"Status: {'PASSED' if report['passed'] else 'FAILED'}")

            print("\nCriteria:")
            for criterion, passed in report['criteria'].items():
                status = "✓" if passed else "✗"
                print(f"  {status} {criterion.capitalize()}")

            if report['issues']:
                print("\nIssues Found:")
                for issue in report['issues']:
                    print(f"  - {issue}")

            print(f"\nValidated: {report['timestamp']}")

        # Save results if requested
        if args.save and 'error' not in report:
            save_validation_to_story(args.story_id, report, config)

        return 0 if report['passed'] else 1

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
