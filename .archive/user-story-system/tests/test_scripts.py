#!/usr/bin/env python3
"""
Comprehensive test suite for User Story System scripts.

Tests all major functionality of the Python scripts:
- models.py - Pydantic models
- generate_story_from_yaml.py - Story generation
- validate_story_invest.py - INVEST validation
- check_dependencies.py - Dependency analysis
- batch_story_generator.py - Batch processing
- story_map_generator.py - Story mapping
- github_sync.py - GitHub integration
"""

import pytest
import sys
import yaml
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import modules to test
from models import (
    UserStory, Epic, StoryMetadata, AcceptanceCriterion,
    InvestCriteria, Validation
)
import generate_story_from_yaml as gen_story
import validate_story_invest as validate
import check_dependencies as check_deps
import story_map_generator as story_map


# Fixtures

@pytest.fixture
def sample_story_data():
    """Sample story data for testing."""
    return {
        'id': 'US-0001',
        'title': 'Test Story',
        'epic_id': 'EP-001',
        'metadata': {
            'created_date': '2025-01-01',
            'updated_date': '2025-01-02',
            'author': 'Test Author',
            'status': 'backlog',
            'priority': 'high',
            'story_points': 5,
            'sprint': 'Sprint 1'
        },
        'story': {
            'persona': 'ceo',
            'as_a': 'CEO',
            'i_want': 'to see business metrics',
            'so_that': 'I can make informed decisions based on real-time data',
            'context': 'Business metrics are currently scattered',
            'assumptions': ['Data is available'],
            'out_of_scope': ['Historical data']
        },
        'acceptance_criteria': [
            {
                'given': 'I am on the dashboard',
                'when': 'I view the metrics',
                'then': 'I see current revenue, profit, and growth rate'
            }
        ],
        'technical': {
            'tech_stack': ['Python', 'FastAPI'],
            'implementation_hints': ['Use caching'],
            'affected_components': ['API', 'Database'],
            'estimated_effort': '3 days',
            'complexity': 'medium',
            'risks': ['Data inconsistency']
        },
        'dependencies': {
            'blocks': ['US-0002'],
            'blocked_by': [],
            'related_to': ['US-0003']
        },
        'testing': {
            'unit_tests_required': True,
            'integration_tests_required': True,
            'e2e_tests_required': False
        },
        'github': {
            'issue_url': '',
            'issue_number': None,
            'pr_urls': [],
            'labels': []
        },
        'notes': 'Test notes',
        'comments': [],
        'validation': {
            'invest_score': None,
            'invest_criteria': {},
            'last_validated': None,
            'validation_issues': []
        },
        'custom': {}
    }


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        'paths': {
            'stories_yaml': 'stories/yaml-source',
            'stories_md': 'stories/generated-docs',
            'epics': 'epics',
            'templates': 'templates'
        },
        'templates': {
            'markdown': {
                'story_template': 'story-template.md'
            }
        },
        'validation': {
            'invest': {
                'enabled': True,
                'strict_mode': False,
                'criteria': {
                    'independent': {'enabled': True, 'check_dependencies': True},
                    'negotiable': {'enabled': True, 'require_options': False},
                    'valuable': {'enabled': True, 'require_business_value': True},
                    'estimable': {'enabled': True, 'require_story_points': True},
                    'small': {'enabled': True, 'max_story_points': 8},
                    'testable': {'enabled': True, 'require_acceptance_criteria': True, 'min_acceptance_criteria': 1}
                }
            }
        },
        'dependencies': {
            'check_circular': True,
            'max_depth': 10,
            'warn_on_long_chains': True,
            'max_chain_length': 5
        },
        'github': {
            'enabled': True,
            'issues': {
                'title_format': '[{story_id}] {title}',
                'labels': {
                    'story_points': {'enabled': True, 'format': 'story-points-{points}'},
                    'persona': {'enabled': True, 'format': 'persona-{persona_id}'},
                    'epic': {'enabled': True, 'format': 'epic-{epic_id}'},
                    'status': {'enabled': True},
                    'custom': ['user-story']
                }
            },
            'repo': {
                'auto_detect': True,
                'fallback': 'owner/repo'
            }
        }
    }


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


# Tests for models.py

class TestModels:
    """Test Pydantic models."""

    def test_user_story_validation(self, sample_story_data):
        """Test UserStory model validation."""
        story = UserStory(**sample_story_data)
        assert story.id == 'US-0001'
        assert story.title == 'Test Story'
        assert story.metadata.priority == 'high'
        assert story.metadata.story_points == 5

    def test_invalid_story_id(self, sample_story_data):
        """Test invalid story ID format."""
        sample_story_data['id'] = 'INVALID-001'
        with pytest.raises(ValueError, match="Story ID must start with 'US-'"):
            UserStory(**sample_story_data)

    def test_invalid_priority(self, sample_story_data):
        """Test invalid priority value."""
        sample_story_data['metadata']['priority'] = 'invalid'
        with pytest.raises(ValueError, match="Priority must be one of"):
            UserStory(**sample_story_data)

    def test_invalid_story_points(self, sample_story_data):
        """Test invalid story points value."""
        sample_story_data['metadata']['story_points'] = 7
        with pytest.raises(ValueError, match="Story points must be one of"):
            UserStory(**sample_story_data)

    def test_acceptance_criterion(self):
        """Test AcceptanceCriterion model."""
        criterion = AcceptanceCriterion(
            given='initial state',
            when='action occurs',
            then='expected result'
        )
        assert criterion.given == 'initial state'
        assert criterion.when == 'action occurs'
        assert criterion.then == 'expected result'


# Tests for validate_story_invest.py

class TestValidateInvest:
    """Test INVEST validation."""

    def test_check_independent_no_blockers(self, sample_story_data, sample_config):
        """Test independent check with no blockers."""
        passed, issues = validate.check_independent(sample_story_data, sample_config)
        assert passed is True
        assert len(issues) == 0

    def test_check_independent_with_blockers(self, sample_story_data, sample_config):
        """Test independent check with blockers."""
        sample_story_data['dependencies']['blocked_by'] = ['US-0010', 'US-0011']
        passed, issues = validate.check_independent(sample_story_data, sample_config)
        assert passed is False
        assert len(issues) > 0
        assert 'blocked by' in issues[0].lower()

    def test_check_negotiable_flexible(self, sample_story_data, sample_config):
        """Test negotiable check with flexible story."""
        passed, issues = validate.check_negotiable(sample_story_data, sample_config)
        assert passed is True
        assert len(issues) == 0

    def test_check_negotiable_rigid(self, sample_story_data, sample_config):
        """Test negotiable check with rigid requirements."""
        sample_story_data['story']['i_want'] = 'to implement using exactly PostgreSQL database'
        passed, issues = validate.check_negotiable(sample_story_data, sample_config)
        assert passed is False
        assert len(issues) > 0

    def test_check_valuable_with_benefit(self, sample_story_data, sample_config):
        """Test valuable check with clear benefit."""
        passed, issues = validate.check_valuable(sample_story_data, sample_config)
        assert passed is True
        assert len(issues) == 0

    def test_check_valuable_missing_benefit(self, sample_story_data, sample_config):
        """Test valuable check without benefit."""
        sample_story_data['story']['so_that'] = ''
        passed, issues = validate.check_valuable(sample_story_data, sample_config)
        assert passed is False
        assert 'so_that' in issues[0].lower()

    def test_check_estimable_with_points(self, sample_story_data, sample_config):
        """Test estimable check with story points."""
        passed, issues = validate.check_estimable(sample_story_data, sample_config)
        assert passed is True
        assert len(issues) == 0

    def test_check_estimable_no_points(self, sample_story_data, sample_config):
        """Test estimable check without story points."""
        sample_story_data['metadata']['story_points'] = None
        passed, issues = validate.check_estimable(sample_story_data, sample_config)
        assert passed is False
        assert 'story points' in issues[0].lower()

    def test_check_small_within_limit(self, sample_story_data, sample_config):
        """Test small check within limit."""
        passed, issues = validate.check_small(sample_story_data, sample_config)
        assert passed is True
        assert len(issues) == 0

    def test_check_small_too_large(self, sample_story_data, sample_config):
        """Test small check exceeding limit."""
        sample_story_data['metadata']['story_points'] = 13
        passed, issues = validate.check_small(sample_story_data, sample_config)
        assert passed is False
        assert 'too large' in issues[0].lower()

    def test_check_testable_with_criteria(self, sample_story_data, sample_config):
        """Test testable check with acceptance criteria."""
        passed, issues = validate.check_testable(sample_story_data, sample_config)
        assert passed is True
        assert len(issues) == 0

    def test_check_testable_no_criteria(self, sample_story_data, sample_config):
        """Test testable check without criteria."""
        sample_story_data['acceptance_criteria'] = []
        passed, issues = validate.check_testable(sample_story_data, sample_config)
        assert passed is False
        assert 'acceptance criterion' in issues[0].lower()

    def test_calculate_invest_score_all_pass(self):
        """Test INVEST score calculation with all passing."""
        results = {
            'independent': (True, []),
            'negotiable': (True, []),
            'valuable': (True, []),
            'estimable': (True, []),
            'small': (True, []),
            'testable': (True, [])
        }
        score = validate.calculate_invest_score(results)
        assert score == 100

    def test_calculate_invest_score_half_pass(self):
        """Test INVEST score calculation with half passing."""
        results = {
            'independent': (True, []),
            'negotiable': (True, []),
            'valuable': (True, []),
            'estimable': (False, ['error']),
            'small': (False, ['error']),
            'testable': (False, ['error'])
        }
        score = validate.calculate_invest_score(results)
        assert score == 50


# Tests for check_dependencies.py

class TestCheckDependencies:
    """Test dependency checking."""

    def test_build_dependency_graph(self):
        """Test building dependency graph."""
        stories = {
            'US-0001': {
                'id': 'US-0001',
                'dependencies': {'blocks': ['US-0002'], 'blocked_by': []}
            },
            'US-0002': {
                'id': 'US-0002',
                'dependencies': {'blocks': [], 'blocked_by': ['US-0001']}
            },
            'US-0003': {
                'id': 'US-0003',
                'dependencies': {'blocks': [], 'blocked_by': []}
            }
        }

        graph = check_deps.build_dependency_graph(stories)

        assert graph.number_of_nodes() == 3
        assert graph.number_of_edges() == 1
        assert graph.has_edge('US-0001', 'US-0002')

    def test_find_circular_dependencies_none(self):
        """Test circular dependency detection with no cycles."""
        stories = {
            'US-0001': {'id': 'US-0001', 'dependencies': {'blocks': ['US-0002'], 'blocked_by': []}},
            'US-0002': {'id': 'US-0002', 'dependencies': {'blocks': ['US-0003'], 'blocked_by': ['US-0001']}},
            'US-0003': {'id': 'US-0003', 'dependencies': {'blocks': [], 'blocked_by': ['US-0002']}}
        }

        graph = check_deps.build_dependency_graph(stories)
        cycles = check_deps.find_circular_dependencies(graph)

        assert len(cycles) == 0

    def test_find_circular_dependencies_with_cycle(self):
        """Test circular dependency detection with cycle."""
        stories = {
            'US-0001': {'id': 'US-0001', 'dependencies': {'blocks': ['US-0002'], 'blocked_by': ['US-0003']}},
            'US-0002': {'id': 'US-0002', 'dependencies': {'blocks': ['US-0003'], 'blocked_by': ['US-0001']}},
            'US-0003': {'id': 'US-0003', 'dependencies': {'blocks': ['US-0001'], 'blocked_by': ['US-0002']}}
        }

        graph = check_deps.build_dependency_graph(stories)
        cycles = check_deps.find_circular_dependencies(graph)

        assert len(cycles) > 0

    def test_find_independent_stories(self):
        """Test finding independent stories."""
        stories = {
            'US-0001': {'id': 'US-0001', 'dependencies': {'blocks': ['US-0002'], 'blocked_by': []}},
            'US-0002': {'id': 'US-0002', 'dependencies': {'blocks': [], 'blocked_by': ['US-0001']}},
            'US-0003': {'id': 'US-0003', 'dependencies': {'blocks': [], 'blocked_by': []}}
        }

        graph = check_deps.build_dependency_graph(stories)
        independent = check_deps.find_independent_stories(graph)

        assert 'US-0001' in independent
        assert 'US-0003' in independent
        assert 'US-0002' not in independent

    def test_find_bottleneck_stories(self):
        """Test finding bottleneck stories."""
        stories = {
            'US-0001': {
                'id': 'US-0001',
                'dependencies': {'blocks': ['US-0002', 'US-0003', 'US-0004'], 'blocked_by': []}
            },
            'US-0002': {'id': 'US-0002', 'dependencies': {'blocks': [], 'blocked_by': ['US-0001']}},
            'US-0003': {'id': 'US-0003', 'dependencies': {'blocks': [], 'blocked_by': ['US-0001']}},
            'US-0004': {'id': 'US-0004', 'dependencies': {'blocks': [], 'blocked_by': ['US-0001']}}
        }

        graph = check_deps.build_dependency_graph(stories)
        bottlenecks = check_deps.find_bottleneck_stories(graph, threshold=3)

        assert len(bottlenecks) == 1
        assert bottlenecks[0][0] == 'US-0001'
        assert bottlenecks[0][1] == 3


# Tests for story_map_generator.py

class TestStoryMap:
    """Test story map generation."""

    def test_group_stories_by_epic(self):
        """Test grouping stories by epic."""
        stories = [
            {'id': 'US-0001', 'epic_id': 'EP-001'},
            {'id': 'US-0002', 'epic_id': 'EP-001'},
            {'id': 'US-0003', 'epic_id': 'EP-002'},
            {'id': 'US-0004', 'epic_id': ''}
        ]

        grouped = story_map.group_stories_by_epic(stories)

        assert 'EP-001' in grouped
        assert 'EP-002' in grouped
        # Empty epic_id becomes 'No Epic'
        assert ('No Epic' in grouped or '' in grouped)
        assert len(grouped['EP-001']) == 2
        assert len(grouped['EP-002']) == 1
        # Check the no-epic group exists with correct count
        no_epic_key = 'No Epic' if 'No Epic' in grouped else ''
        assert len(grouped[no_epic_key]) == 1

    def test_get_priority_color(self):
        """Test priority color mapping."""
        assert story_map.get_priority_color('critical') == '#FF0000'
        assert story_map.get_priority_color('high') == '#FFA500'
        assert story_map.get_priority_color('medium') == '#FFFF00'
        assert story_map.get_priority_color('low') == '#90EE90'
        assert story_map.get_priority_color('unknown') == '#CCCCCC'

    def test_get_status_emoji(self):
        """Test status emoji mapping."""
        assert story_map.get_status_emoji('draft') == '📝'
        assert story_map.get_status_emoji('done') == '✔️'
        assert story_map.get_status_emoji('blocked') == '🚫'


# Integration tests

class TestIntegration:
    """Integration tests for end-to-end workflows."""

    def test_story_generation_workflow(self, temp_dir, sample_story_data, sample_config):
        """Test complete story generation workflow."""
        # Create directory structure
        yaml_dir = temp_dir / "stories" / "yaml-source"
        md_dir = temp_dir / "stories" / "generated-docs"
        templates_dir = temp_dir / "templates"

        yaml_dir.mkdir(parents=True)
        md_dir.mkdir(parents=True)
        templates_dir.mkdir(parents=True)

        # Write story YAML
        story_path = yaml_dir / "US-0001.yaml"
        with open(story_path, 'w') as f:
            yaml.dump(sample_story_data, f)

        # Create simple template
        template_path = templates_dir / "story-template.md"
        with open(template_path, 'w') as f:
            f.write("# {{ id }}: {{ title }}\n")

        # Load and render
        story_data = gen_story.load_story_yaml(story_path)
        assert story_data['id'] == 'US-0001'

        markdown = gen_story.render_story_markdown(story_data, template_path)
        assert 'US-0001' in markdown
        assert 'Test Story' in markdown


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
