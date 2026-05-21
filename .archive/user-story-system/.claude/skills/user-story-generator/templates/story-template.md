# {{ id }}: {{ title }}

{% if epic_id %}
**Epic:** [{{ epic_id }}](../epics/{{ epic_id }}.md)
{% endif %}

---

## Story

**As a** {{ story.as_a }}
**I want** {{ story.i_want }}
**So that** {{ story.so_that }}

{% if story.context %}
### Context
{{ story.context }}
{% endif %}

---

## Metadata

| Field | Value |
|-------|-------|
| **ID** | {{ id }} |
| **Status** | {{ metadata.status }} |
| **Priority** | {{ metadata.priority }} |
| **Story Points** | {{ metadata.story_points if metadata.story_points else "Not estimated" }} |
| **Sprint** | {{ metadata.sprint if metadata.sprint else "Not assigned" }} |
| **Created** | {{ metadata.created_date }} |
| **Updated** | {{ metadata.updated_date }} |
| **Author** | {{ metadata.author }} |

---

## Acceptance Criteria

{% for criterion in acceptance_criteria %}
### {{ loop.index }}. {{ criterion.given }}

- **Given:** {{ criterion.given }}
- **When:** {{ criterion.when }}
- **Then:** {{ criterion.then }}

{% endfor %}

---

{% if technical and (technical.tech_stack or technical.implementation_hints) %}
## Technical Notes

{% if technical.tech_stack %}
### Tech Stack
{% for tech in technical.tech_stack %}
- {{ tech }}
{% endfor %}
{% endif %}

{% if technical.implementation_hints %}
### Implementation Hints
{% for hint in technical.implementation_hints %}
- {{ hint }}
{% endfor %}
{% endif %}

{% if technical.affected_components %}
### Affected Components
{% for component in technical.affected_components %}
- {{ component }}
{% endfor %}
{% endif %}

{% if technical.estimated_effort %}
**Estimated Effort:** {{ technical.estimated_effort }}
{% endif %}

{% if technical.complexity %}
**Complexity:** {{ technical.complexity }}
{% endif %}

{% if technical.risks %}
### Risks
{% for risk in technical.risks %}
- {{ risk }}
{% endfor %}
{% endif %}

---
{% endif %}

{% if dependencies and (dependencies.blocks or dependencies.blocked_by or dependencies.related_to) %}
## Dependencies

{% if dependencies.blocked_by %}
### Blocked By
{% for dep in dependencies.blocked_by %}
- [{{ dep }}]({{ dep }}.md)
{% endfor %}
{% endif %}

{% if dependencies.blocks %}
### Blocks
{% for dep in dependencies.blocks %}
- [{{ dep }}]({{ dep }}.md)
{% endfor %}
{% endif %}

{% if dependencies.related_to %}
### Related Stories
{% for dep in dependencies.related_to %}
- [{{ dep }}]({{ dep }}.md)
{% endfor %}
{% endif %}

{% if dependencies.requires_data %}
### Data Dependencies
{% for dep in dependencies.requires_data %}
- {{ dep }}
{% endfor %}
{% endif %}

{% if dependencies.requires_infrastructure %}
### Infrastructure Dependencies
{% for dep in dependencies.requires_infrastructure %}
- {{ dep }}
{% endfor %}
{% endif %}

---
{% endif %}

{% if testing and (testing.test_scenarios or testing.test_data_needed) %}
## Testing

{% if testing.test_scenarios %}
### Test Scenarios
{% for scenario in testing.test_scenarios %}
- {{ scenario }}
{% endfor %}
{% endif %}

{% if testing.test_data_needed %}
### Test Data Required
{% for data in testing.test_data_needed %}
- {{ data }}
{% endfor %}
{% endif %}

**Unit Tests Required:** {{ "Yes" if testing.unit_tests_required else "No" }}
**Integration Tests Required:** {{ "Yes" if testing.integration_tests_required else "No" }}
**E2E Tests Required:** {{ "Yes" if testing.e2e_tests_required else "No" }}

---
{% endif %}

{% if story.assumptions %}
## Assumptions
{% for assumption in story.assumptions %}
- {{ assumption }}
{% endfor %}

---
{% endif %}

{% if story.out_of_scope %}
## Out of Scope
{% for item in story.out_of_scope %}
- {{ item }}
{% endfor %}

---
{% endif %}

{% if github and github.issue_url %}
## GitHub

- **Issue:** [#{{ github.issue_number }}]({{ github.issue_url }})
{% if github.pr_urls %}
- **Pull Requests:**
{% for pr_url in github.pr_urls %}
  - [{{ pr_url }}]({{ pr_url }})
{% endfor %}
{% endif %}
{% if github.labels %}
- **Labels:** {{ github.labels | join(", ") }}
{% endif %}

---
{% endif %}

{% if validation and validation.invest_score %}
## Validation

**INVEST Score:** {{ validation.invest_score }}/100

| Criterion | Status |
|-----------|--------|
| Independent | {{ "✅" if validation.invest_criteria.independent else "❌" }} |
| Negotiable | {{ "✅" if validation.invest_criteria.negotiable else "❌" }} |
| Valuable | {{ "✅" if validation.invest_criteria.valuable else "❌" }} |
| Estimable | {{ "✅" if validation.invest_criteria.estimable else "❌" }} |
| Small | {{ "✅" if validation.invest_criteria.small else "❌" }} |
| Testable | {{ "✅" if validation.invest_criteria.testable else "❌" }} |

{% if validation.validation_issues %}
### Issues Found
{% for issue in validation.validation_issues %}
- {{ issue }}
{% endfor %}
{% endif %}

**Last Validated:** {{ validation.last_validated }}

---
{% endif %}

{% if notes %}
## Notes

{{ notes }}

---
{% endif %}

{% if comments %}
## Comments

{% for comment in comments %}
### {{ comment.timestamp }} - {{ comment.author }}
{{ comment.comment }}

{% endfor %}
---
{% endif %}

---

*Generated from [{{ id }}.yaml](../yaml-source/{{ id }}.yaml)*
