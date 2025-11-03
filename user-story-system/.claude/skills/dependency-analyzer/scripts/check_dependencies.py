#!/usr/bin/env python3
"""
Check and analyze story dependencies.

This script:
- Builds a dependency graph of all stories
- Detects circular dependencies
- Finds blocking chains
- Identifies stories with no dependencies (good candidates for immediate work)
- Generates Mermaid diagrams for visualization
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import yaml
import argparse
import networkx as nx
from networkx.algorithms.cycles import simple_cycles

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


def load_config() -> Dict:
    """Load configuration from YAML file."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def load_all_stories(config: Dict) -> Dict[str, Dict]:
    """
    Load all story YAML files.

    Args:
        config: Configuration dictionary

    Returns:
        Dict mapping story_id to story data
    """
    story_files = sorted(STORIES_YAML_DIR.glob("US-*.yaml"))

    stories = {}
    for story_file in story_files:
        try:
            with open(story_file, 'r') as f:
                story_data = yaml.safe_load(f)
                story_id = story_data.get('id', story_file.stem)
                stories[story_id] = story_data
                logger.debug(f"Loaded story: {story_id}")
        except Exception as e:
            logger.error(f"Error loading {story_file}: {e}")

    logger.info(f"Loaded {len(stories)} stories")
    return stories


def build_dependency_graph(stories: Dict[str, Dict]) -> nx.DiGraph:
    """
    Build directed dependency graph.

    In this graph:
    - Nodes are story IDs
    - Edge A -> B means "A blocks B" or "B is blocked by A"

    Args:
        stories: Dictionary of story data

    Returns:
        NetworkX directed graph
    """
    graph = nx.DiGraph()

    # Add all story nodes
    for story_id in stories.keys():
        graph.add_node(story_id)

    # Add dependency edges
    for story_id, story_data in stories.items():
        dependencies = story_data.get('dependencies', {})

        # If this story is blocked by others, add edges FROM blockers TO this story
        blocked_by = dependencies.get('blocked_by', [])
        for blocker in blocked_by:
            if blocker in stories:
                graph.add_edge(blocker, story_id, type='blocks')
                logger.debug(f"Dependency: {blocker} -> {story_id}")
            else:
                logger.warning(f"Story {story_id} references non-existent blocker: {blocker}")

        # If this story blocks others, add edges FROM this story TO blocked stories
        blocks = dependencies.get('blocks', [])
        for blocked in blocks:
            if blocked in stories:
                graph.add_edge(story_id, blocked, type='blocks')
                logger.debug(f"Dependency: {story_id} -> {blocked}")

    logger.info(f"Built graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    return graph


def find_circular_dependencies(graph: nx.DiGraph) -> List[List[str]]:
    """
    Find circular dependencies in the graph.

    Args:
        graph: Dependency graph

    Returns:
        List of cycles (each cycle is a list of story IDs)
    """
    try:
        cycles = list(simple_cycles(graph))
        if cycles:
            logger.warning(f"Found {len(cycles)} circular dependencies")
        else:
            logger.info("No circular dependencies found")
        return cycles
    except Exception as e:
        logger.error(f"Error detecting cycles: {e}")
        return []


def find_blocking_chains(graph: nx.DiGraph, max_length: int = 5) -> List[List[str]]:
    """
    Find long blocking chains.

    A blocking chain is a sequence of stories where each blocks the next.

    Args:
        graph: Dependency graph
        max_length: Warn about chains longer than this

    Returns:
        List of chains that exceed max_length
    """
    long_chains = []

    # Find all root nodes (no predecessors)
    root_nodes = [n for n in graph.nodes() if graph.in_degree(n) == 0]

    for root in root_nodes:
        # Find all simple paths from this root
        for target in graph.nodes():
            if root != target:
                try:
                    paths = list(nx.all_simple_paths(graph, root, target))
                    for path in paths:
                        if len(path) > max_length:
                            long_chains.append(path)
                except nx.NetworkXNoPath:
                    continue

    if long_chains:
        logger.warning(f"Found {len(long_chains)} chains longer than {max_length}")

    return long_chains


def find_independent_stories(graph: nx.DiGraph) -> List[str]:
    """
    Find stories with no dependencies (good candidates for immediate work).

    Args:
        graph: Dependency graph

    Returns:
        List of story IDs with no blockers
    """
    independent = [n for n in graph.nodes() if graph.in_degree(n) == 0]
    logger.info(f"Found {len(independent)} independent stories")
    return independent


def find_bottleneck_stories(graph: nx.DiGraph, threshold: int = 3) -> List[Tuple[str, int]]:
    """
    Find stories that block many other stories (bottlenecks).

    Args:
        graph: Dependency graph
        threshold: Consider stories blocking >= this many as bottlenecks

    Returns:
        List of (story_id, blocked_count) tuples
    """
    bottlenecks = []

    for node in graph.nodes():
        blocked_count = graph.out_degree(node)
        if blocked_count >= threshold:
            bottlenecks.append((node, blocked_count))

    bottlenecks.sort(key=lambda x: x[1], reverse=True)

    if bottlenecks:
        logger.warning(f"Found {len(bottlenecks)} bottleneck stories")

    return bottlenecks


def generate_mermaid_diagram(graph: nx.DiGraph, output_path: Optional[Path] = None) -> str:
    """
    Generate Mermaid diagram of dependency graph.

    Args:
        graph: Dependency graph
        output_path: Optional path to save diagram

    Returns:
        Mermaid diagram as string
    """
    lines = ["graph TD"]

    # Add all edges
    for source, target in graph.edges():
        lines.append(f"    {source} --> {target}")

    # Highlight independent stories (no incoming edges)
    independent = [n for n in graph.nodes() if graph.in_degree(n) == 0]
    for story_id in independent:
        lines.append(f"    style {story_id} fill:#90EE90")

    # Highlight bottlenecks (many outgoing edges)
    bottlenecks = [n for n in graph.nodes() if graph.out_degree(n) >= 3]
    for story_id in bottlenecks:
        lines.append(f"    style {story_id} fill:#FFB6C1")

    diagram = "\n".join(lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(diagram)
        logger.info(f"Saved Mermaid diagram to {output_path}")

    return diagram


def analyze_dependencies(
    story_id: Optional[str],
    config: Dict
) -> Dict:
    """
    Analyze dependencies for all stories or a specific story.

    Args:
        story_id: Optional story ID to focus analysis on
        config: Configuration dictionary

    Returns:
        Dict: Analysis report
    """
    # Load all stories
    stories = load_all_stories(config)

    if not stories:
        return {
            'error': 'No stories found',
            'stories_count': 0
        }

    # Build dependency graph
    graph = build_dependency_graph(stories)

    # Analyze
    circular_deps = find_circular_dependencies(graph)
    max_chain_length = config['dependencies']['max_chain_length']
    blocking_chains = find_blocking_chains(graph, max_chain_length)
    independent = find_independent_stories(graph)
    bottlenecks = find_bottleneck_stories(graph)

    # Build report
    report = {
        'stories_count': len(stories),
        'dependencies_count': graph.number_of_edges(),
        'circular_dependencies': [
            {'cycle': cycle, 'length': len(cycle)}
            for cycle in circular_deps
        ],
        'long_blocking_chains': [
            {'chain': chain, 'length': len(chain)}
            for chain in blocking_chains
        ],
        'independent_stories': independent,
        'bottleneck_stories': [
            {'story_id': sid, 'blocks_count': count}
            for sid, count in bottlenecks
        ],
        'has_issues': len(circular_deps) > 0 or len(blocking_chains) > 0,
    }

    # If analyzing specific story, add focused info
    if story_id and story_id in stories:
        report['focus_story'] = {
            'id': story_id,
            'blocks': list(graph.successors(story_id)),
            'blocked_by': list(graph.predecessors(story_id)),
            'is_independent': graph.in_degree(story_id) == 0,
            'is_bottleneck': graph.out_degree(story_id) >= 3,
        }

    return report


def main() -> int:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description='Check and analyze story dependencies',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all dependencies
  %(prog)s

  # Analyze specific story
  %(prog)s --story-id US-0001

  # Generate Mermaid diagram
  %(prog)s --output-diagram dependencies.mmd

  # Output as JSON
  %(prog)s --output json
        """
    )

    parser.add_argument(
        '--story-id',
        type=str,
        help='Focus analysis on specific story ID'
    )

    parser.add_argument(
        '--output-diagram',
        type=str,
        help='Output path for Mermaid diagram'
    )

    parser.add_argument(
        '--output',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
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

        # Analyze
        report = analyze_dependencies(args.story_id, config)

        # Generate diagram if requested
        if args.output_diagram:
            stories = load_all_stories(config)
            graph = build_dependency_graph(stories)
            diagram_path = Path(args.output_diagram)
            generate_mermaid_diagram(graph, diagram_path)

        # Output results
        if args.output == 'json':
            print(json.dumps(report, indent=2))
        else:
            # Text output
            print("\nDependency Analysis Report")
            print("=" * 60)

            if 'error' in report:
                print(f"\nError: {report['error']}")
                return 1

            print(f"\nStories: {report['stories_count']}")
            print(f"Dependencies: {report['dependencies_count']}")

            # Circular dependencies
            if report['circular_dependencies']:
                print(f"\n⚠ Circular Dependencies: {len(report['circular_dependencies'])}")
                for i, cycle_info in enumerate(report['circular_dependencies'], 1):
                    cycle = cycle_info['cycle']
                    print(f"  {i}. {' -> '.join(cycle + [cycle[0]])}")
            else:
                print("\n✓ No circular dependencies")

            # Long chains
            if report['long_blocking_chains']:
                print(f"\n⚠ Long Blocking Chains: {len(report['long_blocking_chains'])}")
                for i, chain_info in enumerate(report['long_blocking_chains'], 1):
                    chain = chain_info['chain']
                    print(f"  {i}. {' -> '.join(chain)} (length: {chain_info['length']})")
            else:
                print("\n✓ No long blocking chains")

            # Independent stories
            if report['independent_stories']:
                print(f"\n✓ Independent Stories (ready to start): {len(report['independent_stories'])}")
                for story_id in report['independent_stories'][:5]:
                    print(f"  - {story_id}")
                if len(report['independent_stories']) > 5:
                    print(f"  ... and {len(report['independent_stories']) - 5} more")

            # Bottlenecks
            if report['bottleneck_stories']:
                print(f"\n⚠ Bottleneck Stories (blocking many): {len(report['bottleneck_stories'])}")
                for bottleneck in report['bottleneck_stories'][:5]:
                    print(f"  - {bottleneck['story_id']} (blocks {bottleneck['blocks_count']} stories)")

            # Focus story info
            if 'focus_story' in report:
                focus = report['focus_story']
                print(f"\nFocus Story: {focus['id']}")
                print(f"  Blocks: {focus['blocks'] if focus['blocks'] else 'none'}")
                print(f"  Blocked by: {focus['blocked_by'] if focus['blocked_by'] else 'none'}")
                print(f"  Independent: {focus['is_independent']}")
                print(f"  Bottleneck: {focus['is_bottleneck']}")

            # Summary
            print("\nSummary:")
            if report['has_issues']:
                print("  ⚠ Issues found - review circular dependencies and long chains")
                return 1
            else:
                print("  ✓ No critical dependency issues")
                return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
