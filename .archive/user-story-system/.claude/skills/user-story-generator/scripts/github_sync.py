#!/usr/bin/env python3
"""
GitHub integration for user stories.

Provides bi-directional synchronization between user story YAML files
and GitHub issues, with support for labels, milestones, and metadata.

Commands:
  create - Create GitHub issue from story
  update - Update existing GitHub issue
  sync   - Bi-directional sync between story and issue
  bulk   - Process multiple stories
"""

import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import yaml
import argparse
from github import Github, GithubException

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

# Config paths within skill
CONFIG_PATH = SKILL_DIR / "config" / "automation-config.yaml"
STATUSES_PATH = SKILL_DIR / "config" / "story-statuses.yaml"

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


def save_story(story_id: str, story_data: Dict, config: Dict) -> None:
    """Save story YAML file atomically."""
    story_path = STORIES_YAML_DIR / f"{story_id}.yaml"

    temp_path = story_path.with_suffix('.tmp')

    try:
        with open(temp_path, 'w') as f:
            yaml.dump(story_data, f, default_flow_style=False, sort_keys=False)

        temp_path.rename(story_path)
        logger.debug(f"Saved story {story_id}")

    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise


def get_github_token() -> str:
    """
    Get GitHub token from environment or gh CLI.

    Returns:
        GitHub personal access token

    Raises:
        RuntimeError: If token cannot be obtained
    """
    # Try gh CLI first
    try:
        result = subprocess.run(
            ['gh', 'auth', 'token'],
            capture_output=True,
            text=True,
            check=True
        )
        token = result.stdout.strip()
        if token:
            logger.debug("Got GitHub token from gh CLI")
            return token
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("gh CLI not available or not authenticated")

    raise RuntimeError(
        "GitHub token not found. Run 'gh auth login' to authenticate."
    )


def detect_github_repo(config: Dict) -> str:
    """
    Detect GitHub repository from git remote.

    Args:
        config: Configuration dictionary

    Returns:
        Repository in "owner/repo" format

    Raises:
        RuntimeError: If repository cannot be detected
    """
    github_config = config.get('github', {}).get('repo', {})

    # Check manual fallback first
    if github_config.get('fallback'):
        return github_config['fallback']

    # Try to detect from git remote
    if not github_config.get('auto_detect', True):
        raise RuntimeError("GitHub repo auto-detection disabled and no fallback set")

    try:
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            check=True,
            cwd=PROJECT_ROOT
        )

        remote_url = result.stdout.strip()

        # Parse owner/repo from URL
        # Format: git@github.com:owner/repo.git or https://github.com/owner/repo.git
        if 'github.com' in remote_url:
            parts = remote_url.split('github.com')[-1]
            parts = parts.strip(':/')
            repo = parts.replace('.git', '')
            logger.info(f"Detected GitHub repo: {repo}")
            return repo

        raise RuntimeError(f"Could not parse GitHub repo from: {remote_url}")

    except subprocess.CalledProcessError:
        raise RuntimeError("Not a git repository or no remote 'origin'")


def format_issue_title(story_id: str, title: str, config: Dict) -> str:
    """Format issue title according to configuration."""
    title_format = config['github']['issues']['title_format']
    return title_format.format(story_id=story_id, title=title)


def generate_issue_body(story_data: Dict, config: Dict) -> str:
    """
    Generate GitHub issue body from story data.

    Args:
        story_data: Story data dictionary
        config: Configuration dictionary

    Returns:
        Formatted issue body
    """
    story = story_data.get('story', {})
    metadata = story_data.get('metadata', {})
    acceptance_criteria = story_data.get('acceptance_criteria', [])

    lines = [
        "## User Story",
        "",
        f"**As a** {story.get('as_a', '')}",
        f"**I want** {story.get('i_want', '')}",
        f"**So that** {story.get('so_that', '')}",
        ""
    ]

    if story.get('context'):
        lines.extend([
            "## Context",
            "",
            story['context'],
            ""
        ])

    # Acceptance criteria as checklist
    if acceptance_criteria:
        lines.extend([
            "## Acceptance Criteria",
            ""
        ])

        for i, criterion in enumerate(acceptance_criteria, 1):
            lines.append(f"### {i}. {criterion.get('given', 'Criterion')}")
            lines.append(f"- [ ] **Given:** {criterion.get('given', '')}")
            lines.append(f"- [ ] **When:** {criterion.get('when', '')}")
            lines.append(f"- [ ] **Then:** {criterion.get('then', '')}")
            lines.append("")

    # Metadata table
    lines.extend([
        "## Metadata",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| Story Points | {metadata.get('story_points', 'Not estimated')} |",
        f"| Priority | {metadata.get('priority', 'medium')} |",
        f"| Sprint | {metadata.get('sprint', 'Not assigned')} |",
        ""
    ])

    return "\n".join(lines)


def generate_labels(story_data: Dict, config: Dict) -> List[str]:
    """
    Generate GitHub labels from story data.

    Args:
        story_data: Story data dictionary
        config: Configuration dictionary

    Returns:
        List of label names
    """
    labels = []
    labels_config = config['github']['issues']['labels']
    metadata = story_data.get('metadata', {})

    # Story points label
    if labels_config.get('story_points', {}).get('enabled'):
        points = metadata.get('story_points')
        if points:
            label_format = labels_config['story_points']['format']
            labels.append(label_format.format(points=points))

    # Persona label
    if labels_config.get('persona', {}).get('enabled'):
        persona = story_data.get('story', {}).get('persona')
        if persona:
            label_format = labels_config['persona']['format']
            labels.append(label_format.format(persona_id=persona))

    # Epic label
    if labels_config.get('epic', {}).get('enabled'):
        epic_id = story_data.get('epic_id')
        if epic_id:
            label_format = labels_config['epic']['format']
            labels.append(label_format.format(epic_id=epic_id))

    # Status label (from story-statuses.yaml)
    if labels_config.get('status', {}).get('enabled'):
        status = metadata.get('status', 'draft')
        # Load status configuration
        if STATUSES_PATH.exists():
            with open(STATUSES_PATH, 'r') as f:
                status_config = yaml.safe_load(f)
                status_info = status_config.get('statuses', {}).get(status, {})
                status_labels = status_info.get('github_labels', [])
                labels.extend(status_labels)

    # Custom labels
    custom_labels = labels_config.get('custom', [])
    labels.extend(custom_labels)

    # Additional labels from story
    github_labels = story_data.get('github', {}).get('labels', [])
    labels.extend(github_labels)

    return list(set(labels))  # Remove duplicates


def create_github_issue(
    story_id: str,
    story_data: Dict,
    config: Dict,
    github_client: Github
) -> Tuple[int, str]:
    """
    Create GitHub issue from story.

    Args:
        story_id: Story ID
        story_data: Story data
        config: Configuration
        github_client: PyGithub client

    Returns:
        Tuple of (issue_number, issue_url)
    """
    repo_name = detect_github_repo(config)
    repo = github_client.get_repo(repo_name)

    # Format title and body
    title = format_issue_title(story_id, story_data.get('title', ''), config)
    body = generate_issue_body(story_data, config)
    labels = generate_labels(story_data, config)

    # Create issue
    issue = repo.create_issue(
        title=title,
        body=body,
        labels=labels
    )

    logger.info(f"Created issue #{issue.number}: {issue.html_url}")

    return issue.number, issue.html_url


def update_github_issue(
    issue_number: int,
    story_data: Dict,
    config: Dict,
    github_client: Github
) -> str:
    """
    Update existing GitHub issue.

    Args:
        issue_number: GitHub issue number
        story_data: Story data
        config: Configuration
        github_client: PyGithub client

    Returns:
        Issue URL
    """
    repo_name = detect_github_repo(config)
    repo = github_client.get_repo(repo_name)
    issue = repo.get_issue(issue_number)

    # Update title, body, labels
    story_id = story_data.get('id', '')
    title = format_issue_title(story_id, story_data.get('title', ''), config)
    body = generate_issue_body(story_data, config)
    labels = generate_labels(story_data, config)

    issue.edit(title=title, body=body, labels=labels)

    # Update state based on story status
    metadata = story_data.get('metadata', {})
    status = metadata.get('status', 'draft')

    if STATUSES_PATH.exists():
        with open(STATUSES_PATH, 'r') as f:
            status_config = yaml.safe_load(f)
            status_info = status_config.get('statuses', {}).get(status, {})
            github_state = status_info.get('github_state')

            if github_state == 'closed' and issue.state == 'open':
                issue.edit(state='closed')
                logger.info(f"Closed issue #{issue_number}")
            elif github_state == 'open' and issue.state == 'closed':
                issue.edit(state='open')
                logger.info(f"Reopened issue #{issue_number}")

    logger.info(f"Updated issue #{issue_number}: {issue.html_url}")

    return issue.html_url


def sync_story_to_github(
    story_id: str,
    config: Dict,
    github_client: Github
) -> None:
    """
    Sync story to GitHub (create or update).

    Args:
        story_id: Story ID
        config: Configuration
        github_client: PyGithub client
    """
    story_data = load_story(story_id, config)
    github_info = story_data.get('github', {})
    issue_number = github_info.get('issue_number')

    if issue_number:
        # Update existing issue
        issue_url = update_github_issue(issue_number, story_data, config, github_client)
    else:
        # Create new issue
        issue_number, issue_url = create_github_issue(
            story_id, story_data, config, github_client
        )

        # Update story with GitHub info
        if 'github' not in story_data:
            story_data['github'] = {}

        story_data['github']['issue_number'] = issue_number
        story_data['github']['issue_url'] = issue_url

        save_story(story_id, story_data, config)


def main() -> int:
    """Main entry point with subcommands."""
    parser = argparse.ArgumentParser(
        description='GitHub integration for user stories',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create GitHub issue from story')
    create_parser.add_argument('story_id', help='Story ID (e.g., US-0001)')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update existing GitHub issue')
    update_parser.add_argument('story_id', help='Story ID (e.g., US-0001)')

    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync story with GitHub')
    sync_parser.add_argument('story_id', help='Story ID (e.g., US-0001)')

    # Bulk command
    bulk_parser = subparsers.add_parser('bulk', help='Process multiple stories')
    bulk_parser.add_argument(
        '--all',
        action='store_true',
        help='Process all stories'
    )
    bulk_parser.add_argument(
        '--story-ids',
        help='Comma-separated story IDs'
    )

    # Global options
    parser.add_argument('--verbose', action='store_true', help='Verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return 1

    try:
        # Load configuration
        config = load_config()

        # Get GitHub client
        token = get_github_token()
        github_client = Github(token)

        # Execute command
        if args.command == 'create':
            sync_story_to_github(args.story_id, config, github_client)
            logger.info(f"✓ Created GitHub issue for {args.story_id}")

        elif args.command == 'update':
            sync_story_to_github(args.story_id, config, github_client)
            logger.info(f"✓ Updated GitHub issue for {args.story_id}")

        elif args.command == 'sync':
            sync_story_to_github(args.story_id, config, github_client)
            logger.info(f"✓ Synced {args.story_id} with GitHub")

        elif args.command == 'bulk':
            if args.all:
                story_files = sorted(STORIES_YAML_DIR.glob("US-*.yaml"))
                story_ids = [f.stem for f in story_files]
            else:
                story_ids = [sid.strip() for sid in args.story_ids.split(',')]

            for story_id in story_ids:
                try:
                    sync_story_to_github(story_id, config, github_client)
                    logger.info(f"✓ Synced {story_id}")
                except Exception as e:
                    logger.error(f"✗ Failed {story_id}: {e}")

        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
