# Sprint Report Template

## Sprint {sprint_name}

**Duration**: {start_date} → {end_date}
**Capacity**: {capacity} story points (buffer: {buffer}%)
**Utilization**: {used}/{available} points ({utilization}%)

### Selected Stories

| Priority   | ID      | Title   | Points   | Persona   | Deps                   |
| ---------- | ------- | ------- | -------- | --------- | ---------------------- |
| {priority} | US-XXXX | {title} | {points} | {persona} | {blocked_by or "none"} |

### Capacity Analysis

- **Available**: {capacity} points
- **Buffer**: {buffer_points} points ({buffer}%)
- **Allocated**: {allocated} points
- **Remaining**: {remaining} points

### Dependency Check

{For each story with blocked_by}

- US-XXXX depends on US-YYYY — {status: in this sprint / already done / NOT in sprint (risk!)}

### Risk Assessment

- **Overcommitment**: {capacity utilization > 85%? warn}
- **Dependency gaps**: {blocked_by stories not in sprint? warn}
- **Large stories**: {any story > 5 points? suggest splitting}

### GitHub Milestone

```bash
gh api repos/:owner/:repo/milestones --method POST \
  -f title="{sprint_name}" \
  -f description="Sprint {sprint_name}: {story_count} stories, {total_points} points" \
  -f due_on="{end_date}T23:59:59Z"
```
