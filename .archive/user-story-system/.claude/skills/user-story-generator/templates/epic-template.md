# {{ id }}: {{ title }}

{{ description }}

---

## Business Context

**Objective:** {{ business.objective }}

**Value Proposition:** {{ business.value_proposition }}

{% if business.success_metrics %}
### Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
{% for metric in business.success_metrics %}
| {{ metric.metric }} | {{ metric.target }} | {{ metric.current if metric.current else "N/A" }} |
{% endfor %}
{% endif %}

{% if business.stakeholders %}
**Stakeholders:** {{ business.stakeholders | join(", ") }}
{% endif %}

{% if business.budget %}
**Budget:** {{ business.budget }}
{% endif %}

---

## Metadata

| Field | Value |
|-------|-------|
| **ID** | {{ id }} |
| **Status** | {{ metadata.status }} |
| **Priority** | {{ metadata.priority }} |
| **Created** | {{ metadata.created_date }} |
| **Updated** | {{ metadata.updated_date }} |
| **Author** | {{ metadata.author }} |
{% if metadata.target_date %}
| **Target Date** | {{ metadata.target_date }} |
{% endif %}
{% if metadata.actual_completion_date %}
| **Completed** | {{ metadata.actual_completion_date }} |
{% endif %}

---

## Scope

{% if scope.in_scope %}
### In Scope
{% for item in scope.in_scope %}
- {{ item }}
{% endfor %}
{% endif %}

{% if scope.out_of_scope %}
### Out of Scope
{% for item in scope.out_of_scope %}
- {{ item }}
{% endfor %}
{% endif %}

{% if scope.assumptions %}
### Assumptions
{% for assumption in scope.assumptions %}
- {{ assumption }}
{% endfor %}
{% endif %}

{% if scope.constraints %}
### Constraints
{% for constraint in scope.constraints %}
- {{ constraint }}
{% endfor %}
{% endif %}

---

## Stories

**Total Stories:** {{ stories.total_count }}
**Total Story Points:** {{ stories.total_story_points }}
**Completed Story Points:** {{ stories.completed_story_points }}
**Progress:** {{ progress.percentage_complete }}%

{% if stories.story_ids %}
### Story List

| ID | Status | Story Points |
|----|--------|--------------|
{% for story_id in stories.story_ids %}
| [{{ story_id }}](../stories/generated-docs/{{ story_id }}.md) | - | - |
{% endfor %}
{% endif %}

---

{% if timeline %}
## Timeline

{% if timeline.estimated_duration %}
**Estimated Duration:** {{ timeline.estimated_duration }}
{% endif %}

{% if timeline.start_date %}
**Start Date:** {{ timeline.start_date }}
{% endif %}

{% if timeline.end_date %}
**End Date:** {{ timeline.end_date }}
{% endif %}

{% if timeline.milestones %}
### Milestones

| Milestone | Date | Status |
|-----------|------|--------|
{% for milestone in timeline.milestones %}
| {{ milestone.name }} | {{ milestone.date }} | {{ milestone.status }} |
{% endfor %}
{% endif %}
{% endif %}

---

{% if dependencies and (dependencies.depends_on_epics or dependencies.blocks_epics or dependencies.external_dependencies) %}
## Dependencies

{% if dependencies.depends_on_epics %}
### Depends On
{% for epic_id in dependencies.depends_on_epics %}
- [{{ epic_id }}]({{ epic_id }}.md)
{% endfor %}
{% endif %}

{% if dependencies.blocks_epics %}
### Blocks
{% for epic_id in dependencies.blocks_epics %}
- [{{ epic_id }}]({{ epic_id }}.md)
{% endfor %}
{% endif %}

{% if dependencies.external_dependencies %}
### External Dependencies
{% for dep in dependencies.external_dependencies %}
- {{ dep }}
{% endfor %}
{% endif %}

---
{% endif %}

## Progress Tracking

| Status | Count |
|--------|-------|
| **Completed** | {{ progress.stories_completed }} |
| **In Progress** | {{ progress.stories_in_progress }} |
| **Blocked** | {{ progress.stories_blocked }} |
| **Not Started** | {{ progress.stories_not_started }} |

**Overall Progress:** {{ progress.percentage_complete }}%

```
Progress: [{% for i in range((progress.percentage_complete / 5) | int) %}█{% endfor %}{% for i in range(20 - (progress.percentage_complete / 5) | int) %}░{% endfor %}] {{ progress.percentage_complete }}%
```

---

{% if github and (github.milestone_url or github.project_url) %}
## GitHub

{% if github.milestone_url %}
- **Milestone:** [#{{ github.milestone_number }}]({{ github.milestone_url }})
{% endif %}
{% if github.project_url %}
- **Project:** [{{ github.project_url }}]({{ github.project_url }})
{% endif %}
{% if github.labels %}
- **Labels:** {{ github.labels | join(", ") }}
{% endif %}

---
{% endif %}

{% if notes %}
## Notes

{{ notes }}

---
{% endif %}

{% if updates %}
## Updates

{% for update in updates %}
### {{ update.date }} - {{ update.author }}
{{ update.update }}

{% endfor %}
---
{% endif %}

---

*Generated from [{{ id }}.yaml]({{ id }}.yaml)*
