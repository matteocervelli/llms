# Plan Sprint with Capacity Management

Plan a sprint by selecting stories based on capacity, dependencies, and priority.

## Usage

```
/user-story-sprint <capacity>
/user-story-sprint <capacity> --buffer <percentage>
```

## Examples

```
/user-story-sprint 40
/user-story-sprint 40 --buffer 20
/user-story-sprint 50 --dry-run
```

## What it does

1. **Load Backlog** - Loads stories with status "backlog" or "ready"
2. **Check Dependencies** - Verifies dependency readiness
3. **Sort by Priority** - Orders stories (critical → high → medium → low)
4. **Calculate Capacity** - Applies buffer for unknowns
5. **Fit Stories** - Selects stories up to capacity
6. **Validate Plan** - Checks feasibility
7. **Update Status** - Moves stories to sprint
8. **Create Milestone** - Creates GitHub milestone (if enabled)

## Result

- Sprint plan with selected stories
- Capacity breakdown (used/available/buffer)
- Dependency validation
- Story status updates (backlog → ready)
- GitHub milestone creation (if enabled)

---

Activate the **sprint-planner** skill to plan a sprint with capacity management.

Use the `sprint-planner` skill located in `.claude/skills/sprint-planner/SKILL.md`.

## Parameters

- **capacity**: Sprint capacity in story points (required)
- **--buffer**: Buffer percentage (default: 20%)
- **--dry-run**: Show plan without making changes
- **--sprint-name**: Custom sprint name (default: auto-generated)

## Sprint Planning Process

### 1. Capacity Calculation

```
Total Capacity: 40 points
Buffer (20%): 8 points
Available for Stories: 32 points
```

The buffer reserves capacity for:
- Bug fixes
- Support requests
- Technical debt
- Unknown complexity

### 2. Story Selection Criteria

Stories must meet ALL criteria:
- ✅ Status is "backlog" or "ready"
- ✅ All blocking dependencies are "done"
- ✅ Story points are estimated
- ✅ Acceptance criteria exist
- ✅ INVEST validation passed

### 3. Priority Sorting

Stories are sorted:
1. **Critical** - Must be in sprint
2. **High** - Important features
3. **Medium** - Standard priority
4. **Low** - Nice-to-have

Within same priority, sorted by:
- Dependency readiness
- Story points (smaller first)
- Created date (older first)

### 4. Capacity Fitting

Algorithm:
```
1. Start with highest priority stories
2. Add stories while total ≤ available capacity
3. Skip stories if dependencies not met
4. Continue until capacity full or no more stories
```

### 5. Validation Checks

- **Capacity Check**: Total ≤ available capacity
- **Dependency Check**: All blockers are done
- **Balance Check**: Mix of small and medium stories
- **Risk Check**: No single story >40% of capacity

## Sprint Plan Report

```
📊 Sprint Plan: Sprint 5 (March 2025)

💪 Capacity
- Total: 40 points
- Buffer (20%): 8 points
- Available: 32 points
- Used: 30 points
- Remaining: 2 points

📝 Selected Stories (7)

1. US-0012: User authentication (5 pts) [High]
   Dependencies: None ✅

2. US-0015: Dashboard layout (3 pts) [High]
   Dependencies: Blocked by US-0012 ✅

3. US-0018: Data visualization (5 pts) [Medium]
   Dependencies: Blocked by US-0015 ✅

4. US-0021: Export to PDF (3 pts) [Medium]
   Dependencies: Blocked by US-0015 ✅

5. US-0024: User profile page (5 pts) [Medium]
   Dependencies: Blocked by US-0012 ✅

6. US-0027: Search functionality (5 pts) [Medium]
   Dependencies: None ✅

7. US-0030: Email notifications (4 pts) [Low]
   Dependencies: Blocked by US-0012 ✅

✅ All dependencies satisfied
✅ Good story size balance
⚠️  2 points remaining (consider adding US-0031: 2pts)

📌 Not Selected
- US-0033: Advanced analytics (8 pts) - Blocked by incomplete dependencies
- US-0036: Mobile app (13 pts) - Too large, should be split
- US-0039: Integration testing (5 pts) - Capacity limit reached

🎯 Next Steps
1. Review and confirm sprint plan
2. Move stories to sprint (updates status)
3. Create GitHub milestone
4. Start development!
```

## Workflow

The skill will:
1. Accept sprint capacity (story points)
2. Load all backlog/ready stories
3. Check dependency readiness for each story
4. Run dependency analyzer to verify no circular deps
5. Filter stories ready to start (dependencies met)
6. Sort by priority (critical → high → medium → low)
7. Calculate available capacity (total - buffer)
8. Fit stories to capacity using greedy algorithm
9. Validate sprint plan (capacity, balance, dependencies)
10. Present sprint plan for review
11. Ask for confirmation
12. Update story status (backlog → ready or in_progress)
13. Update sprint field in YAML
14. Regenerate Markdown documentation
15. Create GitHub milestone (if enabled)
16. Present final summary

## Configuration

From `.claude/skills/user-story-generator/config/automation-config.yaml`:

```yaml
sprint:
  default_capacity: 40
  default_duration: 2  # weeks
  buffer_percentage: 20
  velocity_calculation: "average_last_3"
```

## GitHub Integration

If GitHub integration is enabled:

1. **Create Milestone**: Creates or updates sprint milestone
2. **Assign Issues**: Assigns story issues to milestone
3. **Update Labels**: Adds "sprint-X" label
4. **Set Due Date**: Sets milestone due date based on duration

## File References

- Skill: `.claude/skills/sprint-planner/SKILL.md`
- Script: `.claude/skills/dependency-analyzer/scripts/check_dependencies.py`
- Scripts: `.claude/skills/user-story-generator/scripts/generate_story_from_yaml.py`, `.claude/skills/sprint-planner/scripts/github_sync.py`
- Stories: `stories/yaml-source/US-*.yaml`
- Config: `.claude/skills/user-story-generator/config/automation-config.yaml`

## Best Practices

### Capacity Guidelines
- **Small Team (2-3)**: 20-30 points
- **Medium Team (4-6)**: 40-60 points
- **Large Team (7+)**: 70-100 points

### Buffer Guidelines
- **Stable team, known tech**: 15-20% buffer
- **New team or tech**: 25-30% buffer
- **High uncertainty**: 30-40% buffer

### Story Balance
- Mix of small (1-3) and medium (5) stories
- Avoid too many large (8) stories
- No stories >8 points (split them)

### Dependency Management
- Start with independent stories
- Ensure blocking stories are done
- Check for hidden dependencies

## Related Commands

- `/user-story-deps` - Analyze dependencies first
- `/user-story-refine` - Ensure stories are validated
- `/user-story-new` - Create stories for backlog
- `/user-story-annotate` - Add technical context
