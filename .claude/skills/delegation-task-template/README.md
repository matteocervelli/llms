# Delegation Task Template Skill

A comprehensive Claude Code skill for creating well-structured delegation tasks with all necessary components for effective task assignment and completion.

## Overview

This skill helps you create professional delegation tasks that include:
- Clear context and background
- Definition of Done (DoD)
- Acceptance criteria
- Implementation checklists
- Due dates and priorities
- Dependencies and resources
- Success metrics
- Progress tracking

## Quick Start

### Using with Claude Code

Simply ask Claude to create a delegation task:

```
"Create a delegation task for implementing a dark mode feature"
```

Claude will use this skill to generate a comprehensive task document with all the necessary sections.

### Using with Claude SDK

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

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
        """
    }]
)

task_content = response.content[0].text
print(task_content)
```

## Features

### Complete Task Structure
- **Task Summary**: Brief overview
- **Context & Background**: Why this task matters
- **Definition of Done**: Clear completion criteria
- **Acceptance Criteria**: Specific, measurable requirements
- **Implementation Checklist**: Step-by-step execution plan
- **Dependencies**: Blockers and relationships
- **Resources**: Documentation and references
- **Success Metrics**: How to measure success
- **Timeline**: Milestones and deadlines
- **Progress Updates**: Track work as it happens

### Multiple Output Formats
- Markdown (default)
- JSON (for programmatic use)
- GitHub Issues
- Notion database entries

### Flexible Usage
- Team delegation
- Personal task planning
- Client deliverables
- Feature specifications
- Bug fix documentation
- Project management integration

## Use Cases

### 1. Team Delegation
Delegate work to team members with clear expectations:
- Full context and background
- Detailed checklists
- Resources and documentation
- Success criteria

### 2. Client Projects
Create deliverable specifications for contractors:
- Professional format
- Clear acceptance criteria
- Timeline with milestones
- Quality standards

### 3. Feature Development
Document feature requirements:
- Technical context
- Implementation steps
- Testing requirements
- Success metrics

### 4. Bug Fixes
Structure bug fix work:
- Issue reproduction
- Root cause analysis
- Fix verification
- Regression prevention

### 5. Documentation Tasks
Plan documentation work:
- Scope and coverage
- Quality standards
- Review process
- Publishing workflow

## Examples

### Example 1: Feature Development

**Input**:
```
Create a delegation task for implementing user authentication with OAuth2
```

**Output**: Complete task document with:
- OAuth2 flow explanation
- Security considerations
- 20+ step checklist
- Testing requirements
- Performance metrics

### Example 2: Bug Fix

**Input**:
```
Create a task to fix the payment timeout issue for the checkout process
```

**Output**: Structured bug fix task with:
- Issue description
- Impact analysis
- Debugging steps
- Fix verification
- Monitoring requirements

### Example 3: SDK Integration

**Input** (via Claude SDK):
```python
{
  "title": "Migrate database to PostgreSQL",
  "assignee": "database-team@company.com",
  "due_date": "2025-12-01",
  "priority": "high",
  "context": "Current MySQL setup can't handle our scale"
}
```

**Output**: JSON-formatted task ready for import into your task management system

## Integration

### Claude Code
This skill is automatically available when placed in `.claude/skills/` directory.

### Claude SDK
Use in your applications:
- Chatbots with task management
- Project management tools
- Documentation generators
- Team collaboration apps
- Automation workflows

### CI/CD Integration
Generate tasks from:
- Pull request templates
- Issue templates
- Release planning
- Sprint automation

## Best Practices

### 1. Provide Context
Always explain WHY a task is needed, not just WHAT needs to be done.

### 2. Be Specific
Use concrete, measurable acceptance criteria:
- ✅ "Response time < 200ms"
- ❌ "Make it fast"

### 3. Break It Down
Complex tasks need detailed checklists with 15-20 specific steps.

### 4. Include Resources
Link to all relevant documentation, examples, and tools upfront.

### 5. Define Success
Include both quantitative metrics and qualitative standards.

## File Structure

```
delegation-task-template/
├── SKILL.md          # Main skill instructions
├── README.md         # This file
└── examples/         # Example delegation tasks
    ├── feature-example.md
    ├── bugfix-example.md
    └── documentation-example.md
```

## Configuration

### Customization

You can customize the task template by editing `SKILL.md`:

1. Adjust sections to match your workflow
2. Add company-specific fields
3. Modify checklist phases
4. Change output format defaults

### Global vs Project Scope

- **Global** (`~/.claude/skills/`): Available across all projects
- **Project** (`.claude/skills/`): Specific to current project
- **Local** (`.claude/skills/`, uncommitted): Personal customizations

## Tips for Effective Delegation

1. **Start with Why**: Context helps assignees make better decisions
2. **Trust but Verify**: Clear checkpoints without micromanagement
3. **Enable Questions**: Make it easy to ask for clarification
4. **Provide Learning**: Include resources for skill development
5. **Celebrate Success**: Recognition in task completion workflow

## Troubleshooting

### Issue: Generated tasks are too generic

**Solution**: Provide more specific context in your request:
- Technical details
- Business requirements
- Known constraints
- Similar past work

### Issue: Checklists are too short

**Solution**: Ask for more detailed breakdown:
- "Create a detailed checklist with 20+ steps"
- "Break down each phase into specific actions"

### Issue: Need different format

**Solution**: Specify output format:
- "Generate as JSON"
- "Format as GitHub issue"
- "Create Notion database entry"

## Version History

### v1.0.0 (2025-10-30)
- Initial release
- Complete task template structure
- Multiple output formats
- Claude SDK integration examples
- Comprehensive documentation

## Contributing

To improve this skill:

1. Fork the repository
2. Create feature branch
3. Update `SKILL.md` with improvements
4. Add examples to demonstrate changes
5. Submit pull request

## License

MIT License - Use freely in your projects

## Support

- **GitHub Issues**: [matteocervelli/llms/issues](https://github.com/matteocervelli/llms/issues)
- **Documentation**: See `SKILL.md` for detailed instructions
- **Examples**: Check `examples/` directory

## Related Skills

- **project-planning**: Break down projects into tasks
- **requirements-gathering**: Collect detailed requirements
- **documentation-writer**: Create supporting docs
- **pr-review**: Review completed deliverables

---

**Created with**: skill_builder tool
**Version**: 1.0.0
**Last Updated**: 2025-10-30
**Maintainer**: Matteo Cervelli
