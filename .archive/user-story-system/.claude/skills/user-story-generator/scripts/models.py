#!/usr/bin/env python3
"""
Pydantic models for User Story System.

This module defines the data models for user stories and epics,
providing validation and type safety across all scripts.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, field_validator


class StoryMetadata(BaseModel):
    """Metadata for a user story."""
    created_date: str
    updated_date: str
    author: str
    status: str = "draft"
    priority: str = "medium"
    story_points: Optional[int] = None
    sprint: Optional[str] = None

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v: str) -> str:
        """Validate priority is one of the allowed values."""
        allowed = ['low', 'medium', 'high', 'critical']
        if v not in allowed:
            raise ValueError(f"Priority must be one of {allowed}")
        return v

    @field_validator('story_points')
    @classmethod
    def validate_story_points(cls, v: Optional[int]) -> Optional[int]:
        """Validate story points are in Fibonacci sequence."""
        if v is None:
            return v
        allowed = [1, 2, 3, 5, 8, 13]
        if v not in allowed:
            raise ValueError(f"Story points must be one of {allowed}")
        return v


class StoryContent(BaseModel):
    """Main story content following As a/I want/So that format."""
    persona: str
    as_a: str
    i_want: str
    so_that: str
    context: str = ""
    assumptions: List[str] = Field(default_factory=list)
    out_of_scope: List[str] = Field(default_factory=list)


class AcceptanceCriterion(BaseModel):
    """Single acceptance criterion in Given/When/Then format."""
    given: str
    when: str
    then: str


class TechnicalNotes(BaseModel):
    """Technical annotations for a story."""
    tech_stack: List[str] = Field(default_factory=list)
    implementation_hints: List[str] = Field(default_factory=list)
    affected_components: List[str] = Field(default_factory=list)
    estimated_effort: str = ""
    complexity: str = ""
    risks: List[str] = Field(default_factory=list)


class Dependencies(BaseModel):
    """Story dependencies."""
    blocks: List[str] = Field(default_factory=list)
    blocked_by: List[str] = Field(default_factory=list)
    related_to: List[str] = Field(default_factory=list)
    requires_data: List[str] = Field(default_factory=list)
    requires_infrastructure: List[str] = Field(default_factory=list)


class Testing(BaseModel):
    """Testing requirements for a story."""
    unit_tests_required: bool = True
    integration_tests_required: bool = False
    e2e_tests_required: bool = False
    test_scenarios: List[str] = Field(default_factory=list)
    test_data_needed: List[str] = Field(default_factory=list)


class GitHubIntegration(BaseModel):
    """GitHub integration data."""
    issue_url: str = ""
    issue_number: Optional[int] = None
    pr_urls: List[str] = Field(default_factory=list)
    labels: List[str] = Field(default_factory=list)


class Comment(BaseModel):
    """Comment on a story."""
    timestamp: str
    author: str
    comment: str


class InvestCriteria(BaseModel):
    """INVEST criteria validation results."""
    independent: Optional[bool] = None
    negotiable: Optional[bool] = None
    valuable: Optional[bool] = None
    estimable: Optional[bool] = None
    small: Optional[bool] = None
    testable: Optional[bool] = None


class Validation(BaseModel):
    """Validation results for a story."""
    invest_score: Optional[int] = None
    invest_criteria: InvestCriteria = Field(default_factory=InvestCriteria)
    last_validated: Optional[str] = None
    validation_issues: List[str] = Field(default_factory=list)


class UserStory(BaseModel):
    """Complete user story model."""
    id: str
    title: str
    epic_id: str = ""
    metadata: StoryMetadata
    story: StoryContent
    acceptance_criteria: List[AcceptanceCriterion]
    technical: TechnicalNotes = Field(default_factory=TechnicalNotes)
    dependencies: Dependencies = Field(default_factory=Dependencies)
    testing: Testing = Field(default_factory=Testing)
    github: GitHubIntegration = Field(default_factory=GitHubIntegration)
    notes: str = ""
    comments: List[Comment] = Field(default_factory=list)
    validation: Validation = Field(default_factory=Validation)
    custom: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate story ID format."""
        if not v.startswith('US-'):
            raise ValueError("Story ID must start with 'US-'")
        return v


class EpicMetadata(BaseModel):
    """Metadata for an epic."""
    created_date: str
    updated_date: str
    author: str
    status: str = "planning"
    priority: str = "medium"
    target_date: Optional[str] = None
    actual_completion_date: Optional[str] = None


class BusinessContext(BaseModel):
    """Business context for an epic."""
    objective: str
    value_proposition: str
    success_metrics: List[Dict[str, str]] = Field(default_factory=list)
    stakeholders: List[str] = Field(default_factory=list)
    budget: Optional[float] = None


class EpicScope(BaseModel):
    """Scope definition for an epic."""
    in_scope: List[str] = Field(default_factory=list)
    out_of_scope: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)


class EpicStories(BaseModel):
    """Story tracking for an epic."""
    total_count: int = 0
    story_ids: List[str] = Field(default_factory=list)
    total_story_points: int = 0
    completed_story_points: int = 0


class EpicDependencies(BaseModel):
    """Epic dependencies."""
    depends_on_epics: List[str] = Field(default_factory=list)
    blocks_epics: List[str] = Field(default_factory=list)
    external_dependencies: List[str] = Field(default_factory=list)


class Milestone(BaseModel):
    """Milestone in epic timeline."""
    name: str
    date: str
    status: str


class Timeline(BaseModel):
    """Timeline for an epic."""
    estimated_duration: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    milestones: List[Milestone] = Field(default_factory=list)


class EpicGitHub(BaseModel):
    """GitHub integration for epics."""
    milestone_url: str = ""
    milestone_number: Optional[int] = None
    project_url: str = ""
    labels: List[str] = Field(default_factory=list)


class Progress(BaseModel):
    """Progress tracking for an epic."""
    percentage_complete: int = 0
    stories_completed: int = 0
    stories_in_progress: int = 0
    stories_blocked: int = 0
    stories_not_started: int = 0


class Update(BaseModel):
    """Status update for an epic."""
    date: str
    author: str
    update: str


class Epic(BaseModel):
    """Complete epic model."""
    id: str
    title: str
    description: str
    metadata: EpicMetadata
    business: BusinessContext = Field(default_factory=BusinessContext)
    scope: EpicScope = Field(default_factory=EpicScope)
    stories: EpicStories = Field(default_factory=EpicStories)
    dependencies: EpicDependencies = Field(default_factory=EpicDependencies)
    timeline: Timeline = Field(default_factory=Timeline)
    github: EpicGitHub = Field(default_factory=EpicGitHub)
    progress: Progress = Field(default_factory=Progress)
    notes: str = ""
    updates: List[Update] = Field(default_factory=list)
    custom: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate epic ID format."""
        if not v.startswith('EP-'):
            raise ValueError("Epic ID must start with 'EP-'")
        return v
