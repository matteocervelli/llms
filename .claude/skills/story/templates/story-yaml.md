# Story YAML Schema

Use this format for all story YAML files saved to `stories/yaml-source/US-XXXX.yaml`.

```yaml
id: US-XXXX
title: "Short imperative title (e.g., View financial dashboard)"
status: backlog # backlog | ready | sprint | done
priority: medium # critical | high | medium | low
story_points: 3 # Fibonacci: 1, 2, 3, 5, 8

# User story format
as_a: "end-user" # persona identifier
i_want: "to view my financial health score on the dashboard"
so_that: "I can quickly understand my company's financial position"

# Acceptance criteria — MUST use Given/When/Then
acceptance_criteria:
  - given: "I am logged in as a CEO"
    when: "I navigate to the dashboard"
    then: "I see a health score between 0-100 with color indicator"
  - given: "financial data has been analyzed"
    when: "I view the dashboard"
    then: "I see all 4 KPI pillars with individual scores"

# Dependencies (optional)
blocked_by: [] # list of US-XXXX ids that must complete first
blocks: [] # list of US-XXXX ids waiting on this

# Sprint tracking (set by /story plan)
sprint: null # "Sprint 2026-01" when assigned
sprint_start: null # ISO date
sprint_end: null # ISO date

# GitHub integration (set by /story sync)
github_issue: null # issue number when synced

# Metadata
created: "2026-02-11"
updated: "2026-02-11"
persona: "ceo" # lowercase persona key
epic: null # EP-XXX if part of an epic
tags: [] # free-form labels
```

## Story ID Convention

- Format: `US-XXXX` (zero-padded 4 digits)
- Counter: `.story_counter` file in project root
- Increment counter after each story creation

## INVEST Quick Reference

| Criterion   | Requirement                                    |
| ----------- | ---------------------------------------------- |
| Independent | No circular deps                               |
| Negotiable  | "i_want" describes outcome, not implementation |
| Valuable    | "so_that" has clear benefit                    |
| Estimable   | Has story_points + >=2 acceptance_criteria     |
| Small       | story_points <= 8                              |
| Testable    | Each criterion has given/when/then             |
