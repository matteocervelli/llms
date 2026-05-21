# {{ title }}

## User Story

**As a** {{ story.as_a }}
**I want** {{ story.i_want }}
**So that** {{ story.so_that }}

{% if story.context %}
## Context
{{ story.context }}
{% endif %}

## Acceptance Criteria

{% for criterion in acceptance_criteria %}
### {{ loop.index }}. {{ criterion.given }}

- [ ] **Given:** {{ criterion.given }}
- [ ] **When:** {{ criterion.when }}
- [ ] **Then:** {{ criterion.then }}

{% endfor %}

{% if technical and (technical.tech_stack or technical.implementation_hints) %}
## Technical Notes

{% if technical.tech_stack %}
**Tech Stack:** {{ technical.tech_stack | join(", ") }}
{% endif %}

{% if technical.implementation_hints %}
### Implementation Hints
{% for hint in technical.implementation_hints %}
- {{ hint }}
{% endfor %}
{% endif %}

{% if technical.complexity %}
**Complexity:** {{ technical.complexity }}
{% endif %}

{% if technical.estimated_effort %}
**Estimated Effort:** {{ technical.estimated_effort }}
{% endif %}
{% endif %}

{% if dependencies and (dependencies.blocks or dependencies.blocked_by) %}
## Dependencies

{% if dependencies.blocked_by %}
**Blocked By:**
{% for dep in dependencies.blocked_by %}
- {{ dep }}
{% endfor %}
{% endif %}

{% if dependencies.blocks %}
**Blocks:**
{% for dep in dependencies.blocks %}
- {{ dep }}
{% endfor %}
{% endif %}
{% endif %}

{% if testing and testing.test_scenarios %}
## Testing

{% for scenario in testing.test_scenarios %}
- [ ] {{ scenario }}
{% endfor %}
{% endif %}

---

**Story ID:** {{ id }}
**Story Points:** {{ metadata.story_points if metadata.story_points else "Not estimated" }}
**Priority:** {{ metadata.priority }}
{% if epic_id %}
**Epic:** {{ epic_id }}
{% endif %}

---

*This issue was automatically generated from user story [{{ id }}]({{ story_file_url }})*
