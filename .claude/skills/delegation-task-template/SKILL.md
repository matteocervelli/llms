---
name: delegation-task-template
description: Create structured delegation tasks with context, definition of done, checklists, due dates, and all necessary components for effective task delegation
allowed-tools:
  - Read
  - Write
  - Edit
  - TodoWrite
---

# Delegation Task Template

Create comprehensive, well-structured delegation tasks that provide clear context, expectations, and success criteria for effective task assignment and completion.

## Purpose

This skill helps you create professional delegation tasks that include:
- Clear task title and description
- Context and background information
- Definition of Done (DoD)
- Acceptance criteria
- Step-by-step checklists
- Due dates and priorities
- Assignee information
- Dependencies and blockers
- Success metrics

## When to Use This Skill

Use this skill when you need to:
- Delegate work to team members
- Create task tickets in project management tools
- Define work items for contractors or external contributors
- Document requirements for feature implementation
- Create standardized work templates for repetitive tasks
- Integrate task delegation into Claude SDK applications

## Instructions

When asked to create a delegation task, follow these steps:

### 1. Gather Information

First, collect the following information from the user (ask if not provided):
- Task name/title
- Brief description
- Who is this task for (assignee)
- Due date
- Priority level (Low, Medium, High, Critical)
- Any dependencies or blockers

### 2. Create the Task Document

Generate a comprehensive task document with the following structure:

```markdown
# [TASK TITLE]

**Status**: 🟡 Not Started
**Assignee**: [Name/Email]
**Due Date**: [YYYY-MM-DD]
**Priority**: [Low/Medium/High/Critical]
**Created**: [Current Date]

---

## 📋 Task Summary

[Brief 2-3 sentence summary of what needs to be done and why]

---

## 🎯 Context & Background

[Detailed context explaining:]
- Why this task is needed
- Business/technical justification
- How it fits into larger project goals
- Any relevant history or previous attempts
- Links to related documents, designs, or discussions

---

## ✅ Definition of Done (DoD)

The task is considered complete when:

- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Specific deliverable 3]
- [ ] All acceptance criteria met
- [ ] Documentation updated
- [ ] Tests written and passing
- [ ] Code reviewed and approved (if applicable)
- [ ] Changes deployed/merged (if applicable)

---

## 🎨 Acceptance Criteria

1. **Criterion 1**: [Specific, measurable requirement]
   - Verification: [How to verify this is met]

2. **Criterion 2**: [Specific, measurable requirement]
   - Verification: [How to verify this is met]

3. **Criterion 3**: [Specific, measurable requirement]
   - Verification: [How to verify this is met]

---

## 📝 Implementation Checklist

### Phase 1: Planning & Setup
- [ ] Review task requirements and context
- [ ] Identify any questions or clarifications needed
- [ ] Set up development environment (if applicable)
- [ ] Review related documentation
- [ ] Estimate effort and timeline

### Phase 2: Execution
- [ ] [Step 1: Specific action to take]
- [ ] [Step 2: Specific action to take]
- [ ] [Step 3: Specific action to take]
- [ ] [Step 4: Specific action to take]

### Phase 3: Quality Assurance
- [ ] Self-review completed work
- [ ] Run tests (unit, integration, e2e)
- [ ] Check for edge cases
- [ ] Verify all acceptance criteria
- [ ] Update documentation

### Phase 4: Delivery
- [ ] Submit for review
- [ ] Address feedback
- [ ] Final verification
- [ ] Mark task as complete

---

## 🔗 Dependencies

**Blocked By**:
- [ ] [Task/requirement that must be completed first]
- [ ] [External dependency or approval needed]

**Blocks**:
- [ ] [Task that depends on this task]

---

## 📚 Resources

**Documentation**:
- [Link to relevant documentation]
- [Link to design specs]
- [Link to API documentation]

**Related Tasks**:
- [Link to related task 1]
- [Link to related task 2]

**Reference Materials**:
- [Link to tutorials or examples]
- [Link to technical specifications]

---

## 📊 Success Metrics

**Quantitative**:
- [Metric 1: e.g., "Response time < 200ms"]
- [Metric 2: e.g., "Test coverage > 80%"]
- [Metric 3: e.g., "Zero critical bugs"]

**Qualitative**:
- [Metric 1: e.g., "Code is maintainable and follows style guide"]
- [Metric 2: e.g., "Documentation is clear and comprehensive"]

---

## 🚨 Important Notes

- [Any critical warnings or cautions]
- [Known limitations or constraints]
- [Security considerations]
- [Performance requirements]

---

## 💬 Questions & Clarifications

If you have any questions or need clarification:
1. Check the context and resources sections above
2. Review related documentation
3. Contact [stakeholder name/email]
4. Post in [relevant Slack/Teams channel]

---

## 📅 Timeline

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Planning Complete | [Date] | 🟡 Pending |
| Phase 1 Complete | [Date] | 🟡 Pending |
| Phase 2 Complete | [Date] | 🟡 Pending |
| Review Complete | [Date] | 🟡 Pending |
| Final Delivery | [Date] | 🟡 Pending |

---

## 🔄 Progress Updates

### [Date] - Initial Assignment
- Task created and assigned to [assignee]
- Initial review scheduled for [date]

### [Date] - Update 1
- [Progress note]

### [Date] - Update 2
- [Progress note]

---

*Task created with delegation-task-template skill*
*Last updated: [Current Date]*
```

### 3. Save the Task Document

Use the **Write** tool to save the task document:
- Default filename: `TASK-[task-name]-[date].md`
- Location: Current directory or user-specified path
- Format: Markdown (.md)

### 4. Optional: Create Related Files

Based on the task type, you may also create:
- **scripts/**: Helper scripts for the task
- **docs/**: Additional documentation
- **templates/**: Code templates or boilerplates
- **tests/**: Test specifications

### 5. Optional: GitHub Integration

If the user wants to create a GitHub issue, provide the content formatted for GitHub:
- Use GitHub-flavored markdown
- Include labels (enhancement, bug, documentation, etc.)
- Add milestone and project information
- Suggest assignees

## Tool Usage Guidelines

### Read
- **Use for**: Reading existing task templates, project documentation, or related files
- **Example**: `Read previous delegation tasks to maintain consistency`

### Write
- **Use for**: Creating new delegation task documents, checklists, or supporting files
- **Example**: `Write the main task document to TASK-feature-xyz-2025-10-30.md`

### Edit
- **Use for**: Updating existing tasks, adding progress notes, or refining requirements
- **Example**: `Edit task document to add new acceptance criteria`

### TodoWrite
- **Use for**: Breaking down the delegation task into trackable todos for immediate execution
- **Example**: `Create todos for gathering requirements, drafting task, and saving document`

## Examples

### Example 1: Feature Development Task

**User Request**: "Create a delegation task for implementing user authentication"

**Generated Task**:
- Title: "Implement User Authentication System"
- Context: OAuth2 integration, JWT tokens, role-based access
- DoD: Login/logout working, tests passing, docs updated
- Checklist: 15+ specific steps
- Due date: 2 weeks
- Success metrics: < 500ms response time, 90%+ test coverage

### Example 2: Bug Fix Task

**User Request**: "Create a task to fix the payment processing timeout issue"

**Generated Task**:
- Title: "Fix Payment Processing Timeout (Issue #234)"
- Context: Users reporting timeouts after 30 seconds, impacts checkout
- DoD: Timeout resolved, no errors in logs, monitoring alerts cleared
- Checklist: Reproduce bug, identify root cause, implement fix, test, deploy
- Priority: Critical
- Success metrics: 0 timeout errors, < 5s processing time

### Example 3: Documentation Task

**User Request**: "Create a task for writing API documentation"

**Generated Task**:
- Title: "Write Comprehensive API Documentation"
- Context: New API endpoints need documentation for external developers
- DoD: All endpoints documented, examples provided, published to docs site
- Checklist: List endpoints, write descriptions, add examples, review, publish
- Resources: OpenAPI spec, Postman collection, existing docs

### Example 4: Team Delegation

**User Request**: "Create a task for Sarah to migrate the database schema"

**Generated Task**:
- Title: "Migrate Database Schema to v2.0"
- Assignee: Sarah Johnson (sarah@company.com)
- Context: New schema required for multi-tenancy feature
- DoD: Migration script tested, data integrity verified, rollback plan ready
- Dependencies: Design approval from architecture team
- Timeline: 5-day timeline with milestones

## Best Practices

### Task Creation
- **Be Specific**: Avoid vague requirements; use concrete, measurable criteria
- **Provide Context**: Explain the "why" not just the "what"
- **Break It Down**: Complex tasks need detailed step-by-step checklists
- **Set Realistic Deadlines**: Consider complexity and dependencies
- **Define Success**: Include both quantitative and qualitative metrics

### Communication
- **Clear Language**: Use simple, direct language; avoid jargon unless necessary
- **Visual Clarity**: Use emojis, headers, and formatting for readability
- **Complete Information**: Include all resources, links, and contacts upfront
- **Update Regularly**: Keep progress notes current for transparency

### Collaboration
- **Identify Dependencies**: Call out blockers and dependencies explicitly
- **Provide Resources**: Link to all relevant documentation and references
- **Enable Questions**: Make it easy for assignees to ask for clarification
- **Track Progress**: Use status indicators and timeline updates

### Quality Assurance
- **Review Criteria**: Ensure acceptance criteria are verifiable
- **Test Requirements**: Include testing expectations in the checklist
- **Documentation**: Require documentation updates as part of DoD
- **Feedback Loop**: Plan for review and iteration

## Integration with Claude SDK

This skill can be integrated into applications using the Claude SDK:

```python
# Example: Using this skill in a Claude SDK application

from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Request task creation
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=4000,
    messages=[{
        "role": "user",
        "content": """Use the delegation-task-template skill to create a task for:
        - Title: Implement dark mode feature
        - Assignee: John Doe
        - Due date: 2025-11-15
        - Priority: Medium
        - Context: Users requesting dark mode for better UX
        """
    }]
)

# The response will contain a complete delegation task document
task_content = response.content[0].text

# Save to your task management system
save_to_project_management_tool(task_content)
```

## Output Formats

This skill can generate tasks in multiple formats:

### Markdown (Default)
- Portable, readable, version-controllable
- Works with GitHub, GitLab, Notion, etc.

### JSON (Programmatic)
```json
{
  "title": "Task Title",
  "assignee": "Name",
  "due_date": "2025-11-15",
  "priority": "high",
  "context": "...",
  "definition_of_done": [...],
  "acceptance_criteria": [...],
  "checklist": [...]
}
```

### GitHub Issue Template
- Formatted for GitHub issues
- Includes labels, milestones, projects

### Notion Database Entry
- Formatted for Notion import
- Properties and relations included

## Error Handling

### Common Issues

**Missing Information**:
- Ask user for required fields (title, assignee, due date)
- Provide sensible defaults where appropriate
- Suggest common priorities and timelines

**Unclear Requirements**:
- Ask clarifying questions before generating task
- Provide examples of well-defined vs. vague requirements
- Iterate on task definition with user feedback

**Integration Failures**:
- Provide task content even if external system integration fails
- Offer alternative formats (copy-paste, download, etc.)
- Log errors for debugging

## Tips for Effective Delegation

1. **Set Clear Expectations**: Don't assume knowledge; be explicit
2. **Provide Autonomy**: Give the "what" and "why", let them decide "how"
3. **Include Learning Resources**: Help assignees learn, don't just instruct
4. **Build in Checkpoints**: Regular check-ins prevent late surprises
5. **Celebrate Success**: Include recognition in task completion workflow

## Related Skills

- **project-planning**: For breaking down large projects into tasks
- **requirements-gathering**: For collecting detailed requirements
- **documentation-writer**: For creating supporting documentation
- **pr-review**: For reviewing completed task deliverables

---

*Generated with skill_builder tool*
*Version: 1.0.0*
*Last updated: 2025-10-30*
