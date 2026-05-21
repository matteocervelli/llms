# User Story Workflow System

A comprehensive system for creating, managing, and tracking user stories with automated validation, GitHub integration, and sprint planning capabilities.

## Overview

This system provides a complete workflow for product teams to:

- **Extract features** from requirements through interactive Q&A
- **Generate user stories** following INVEST criteria
- **Validate automatically** using sub-agents
- **Track dependencies** and prevent circular dependencies
- **Plan sprints** with capacity management
- **Sync with GitHub** for issue tracking
- **Generate documentation** in both YAML and Markdown formats

## Architecture

```
user-story-system/
├── stories/                 # Story files
│   ├── yaml-source/         # Source YAML files
│   ├── generated-docs/      # Generated Markdown docs
│   └── backlog/             # Backlog stories
├── epics/                   # Epic files
├── .claude/                 # Claude Code integration
│   ├── skills/              # Self-contained workflow skills
│   │   ├── user-story-generator/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/     # Generation and GitHub scripts
│   │   │   ├── config/      # Automation config, personas
│   │   │   └── templates/   # YAML and Markdown templates
│   │   ├── story-validator/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/     # INVEST validation script
│   │   │   └── config/      # Story statuses config
│   │   ├── technical-annotator/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/     # Technical annotation
│   │   ├── dependency-analyzer/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/     # Dependency checking, story maps
│   │   └── sprint-planner/
│   │       ├── SKILL.md
│   │       └── scripts/     # Sprint management, GitHub sync
│   ├── commands/            # Slash commands
│   │   ├── user-story-new.md
│   │   ├── user-story-refine.md
│   │   ├── user-story-annotate.md
│   │   ├── user-story-deps.md
│   │   └── user-story-sprint.md
│   └── agents/              # Sub-agents
│       ├── qa-validator-agent.md
│       ├── technical-annotator-agent.md
│       └── story-orchestrator-agent.md
├── tests/                   # Test suite
├── docs/                    # Documentation and examples
└── README.md
```

### Key Design Principles

- **Self-contained Skills**: Each skill has its own scripts, config, and templates
- **No External Dependencies**: Skills don't depend on root-level directories
- **Claude Code Compliant**: Follows official skill structure guidelines
- **Easy Deployment**: Skills can be symlinked or copied to global ~/.claude/

## Features

### 1. Interactive Feature Extraction
- Guided Q&A to extract feature details
- User confirmation before story generation
- Persona selection from pre-defined personas
- Context preservation across iterations

### 2. Automated Story Generation
- Decompose features into 2-8 user stories
- Follow "As a [persona], I want [goal], So that [benefit]" format
- Generate Given/When/Then acceptance criteria
- Assign story points using Fibonacci sequence

### 3. INVEST Validation
- **I**ndependent - Stories can be developed separately
- **N**egotiable - Open to discussion and changes
- **V**aluable - Delivers business value
- **E**stimable - Can be estimated
- **S**mall - Fits within a sprint
- **T**estable - Has clear acceptance criteria

### 4. Technical Annotation
- Automatic tech stack identification
- Implementation hints for developers
- Effort estimation
- Risk identification
- Component mapping

### 5. Dependency Management
- Track story dependencies (blocks, blocked_by, related_to)
- Detect circular dependencies
- Generate dependency graphs
- Visualize with Mermaid diagrams

### 6. Sprint Planning
- Load backlog stories
- Fit stories to sprint capacity
- Check dependency readiness
- Generate sprint plans
- Move stories to sprint folders

### 7. GitHub Integration
- Auto-create GitHub issues from stories
- Sync story status with issue status
- Map story points to labels
- Create milestones for sprints
- Bi-directional synchronization
- Link PRs to stories

### 8. File Management
- YAML as source of truth
- Markdown for human-readable docs
- Automatic regeneration on changes
- Version control friendly

## Personas

The system includes pre-configured personas for Italian SME business context:

- **CEO** - Chief Executive Officer
- **Business Owner** - Family business owner
- **General Manager** - Operations leader
- **CFO** - Chief Financial Officer
- **Sales Manager** - Sales team leader
- **New Owner (Succession)** - Next generation taking over
- **End User** - Generic feature user

See `config/personas.yaml` for full persona definitions.

## Story Statuses

Stories progress through these statuses:

1. **Draft** - Being written
2. **Backlog** - Ready but not prioritized
3. **Ready** - Refined and ready for development
4. **In Progress** - Actively being developed
5. **Blocked** - Blocked by dependencies
6. **In Review** - Under review
7. **Done** - Complete and accepted
8. **Discarded** - No longer needed

## Commands

### `/user-story-new`
Create a new user story from a feature description

```bash
/user-story-new "Feature: Dashboard analytics for CEO"
```

### `/user-story-refine`
Refine existing stories or entire backlog

```bash
/user-story-refine US-0001
/user-story-refine backlog
```

### `/user-story-sprint`
Plan a sprint with capacity

```bash
/user-story-sprint 40  # 40 story points capacity
```

### `/user-story-validate`
Validate story structure and INVEST criteria

```bash
/user-story-validate US-0001
```

### `/user-story-deps`
Analyze story dependencies and generate visualizations

```bash
/user-story-deps
/user-story-deps US-0001
/user-story-deps --diagram
```

### `/user-story-annotate`
Add technical context to stories

```bash
/user-story-annotate US-0001
/user-story-annotate --all
```

## Skills

Each skill is self-contained with its own scripts, config, and templates:

### `user-story-generator`
**Location**: `.claude/skills/user-story-generator/`
- Main orchestrator for story creation workflow
- Includes generation, GitHub sync, and batch processing scripts
- Contains automation config, personas, and all templates

### `story-validator`
**Location**: `.claude/skills/story-validator/`
- Validates stories against INVEST criteria
- Includes validation script and story statuses config

### `technical-annotator`
**Location**: `.claude/skills/technical-annotator/`
- Adds technical notes and implementation hints
- Context-aware tech stack identification

### `dependency-analyzer`
**Location**: `.claude/skills/dependency-analyzer/`
- Analyzes and visualizes story dependencies
- Includes dependency checking and story mapping scripts

### `sprint-planner`
**Location**: `.claude/skills/sprint-planner/`
- Plans sprints with capacity management
- Includes sprint management and GitHub sync scripts

## Agents

Silent sub-agents for automated processing:

### `qa-validator-agent`
Validates stories against INVEST criteria without user interaction

### `technical-annotator-agent`
Adds technical context silently during story creation

### `story-orchestrator-agent`
Coordinates the overall workflow between skills and agents

## Configuration

Configuration files are organized within skills for self-containment:

### System Configuration
**Location**: `.claude/skills/user-story-generator/config/automation-config.yaml`

Configure:
- File paths and naming conventions
- Story ID format and counters
- INVEST validation settings
- Dependency checking rules
- Sprint planning defaults
- GitHub integration settings
- Template rendering options
- Sub-agent configuration

### Personas
**Location**: `.claude/skills/user-story-generator/config/personas.yaml`

Customize:
- Add custom personas for your team/clients
- Modify persona goals and pain points
- Update persona context
- Define persona selection rules

### Story Statuses
**Location**: `.claude/skills/story-validator/config/story-statuses.yaml`

Configure:
- Add custom statuses for your workflow
- Define status transitions
- Configure GitHub label mapping
- Set default status

## Workflow Example

### 1. Create a New Story

```bash
/user-story-new
```

System will:
- Ask questions about the feature
- Extract details to JSON
- Request user confirmation
- Generate 2-8 user stories
- Run silent validation
- Add technical annotations
- Create YAML and Markdown files
- Create GitHub issue (if enabled)

### 2. Refine Stories

```bash
/user-story-refine backlog
```

System will:
- Load all backlog stories
- Validate against INVEST
- Present issues found
- Suggest fixes
- Regenerate files

### 3. Plan Sprint

```bash
/user-story-sprint 40
```

System will:
- Load ready stories
- Check dependencies
- Fit to 40 points capacity
- Consider 20% buffer
- Move stories to sprint
- Create GitHub milestone

### 4. Sync with GitHub

```bash
/user-story-github sync US-0001
```

System will:
- Create or update GitHub issue
- Sync status and labels
- Add story points label
- Link to milestone
- Update story with issue URL

## Testing

Run the test suite:

```bash
# All tests
pytest tests/

# Specific test
pytest tests/test_scripts.py

# With coverage
pytest --cov=scripts tests/
```

## Development

### Adding Custom Personas

Edit `config/personas.yaml`:

```yaml
personas:
  my_persona:
    id: "my_persona"
    name: "My Custom Persona"
    description: "Description here"
    context: "Context here"
    goals:
      - "Goal 1"
      - "Goal 2"
    pain_points:
      - "Pain point 1"
    typical_scenarios:
      - "Scenario 1"
```

### Customizing Templates

Templates use Jinja2 syntax. Edit files in `templates/` to customize:

- Story YAML structure
- Markdown formatting
- GitHub issue format
- Epic structure

### Extending Scripts

Scripts are in `scripts/` directory. Follow these guidelines:

- Use type hints
- Add docstrings
- Include error handling
- Write unit tests
- Follow 500-line limit

## GitHub Integration

### Setup

1. Configure GitHub CLI:
   ```bash
   gh auth login
   ```

2. Enable in config:
   ```yaml
   github:
     enabled: true
     auto_sync: true
   ```

3. Set repository:
   ```yaml
   github:
     repo:
       auto_detect: true  # Or set manually
       fallback: "owner/repo"
   ```

### Features

- **Auto-create issues** - Creates GitHub issue on story creation
- **Status sync** - Syncs story status with issue state
- **Label management** - Maps story points and status to labels
- **Milestone tracking** - Creates milestones for sprints
- **Bi-directional sync** - Updates flow both ways
- **Bulk operations** - Create/update multiple issues

### Labels

The system automatically manages these labels:

- `story-points-{N}` - Story point estimation
- `persona-{id}` - User persona
- `epic-{id}` - Epic linkage
- Status labels from `config/story-statuses.yaml`
- `user-story` - Always added

## Best Practices

### Writing Good Stories

1. **Focus on user value** - Always explain "so that" benefit
2. **Keep it small** - Maximum 8 story points
3. **Make it testable** - Clear acceptance criteria
4. **Be specific** - Avoid vague terms like "better" or "improved"
5. **Consider dependencies** - Identify blocking stories early

### Managing Backlogs

1. **Regular refinement** - Run `/user-story-refine backlog` weekly
2. **Prioritize ruthlessly** - Not everything needs high priority
3. **Break down large stories** - Split stories > 8 points
4. **Remove stale stories** - Discard stories no longer needed
5. **Track dependencies** - Use dependency analyzer regularly

### Sprint Planning

1. **Use velocity** - Base capacity on team velocity
2. **Include buffer** - Reserve 20% for unknowns
3. **Check dependencies** - Ensure prerequisite stories are done
4. **Balance work** - Mix quick wins with complex stories
5. **Review capacity** - Adjust based on team availability

## Troubleshooting

### Story Not Generating

- Check feature description clarity
- Verify persona exists in `config/personas.yaml`
- Review validation errors in logs
- Ensure templates are valid

### GitHub Sync Failing

- Verify `gh` CLI authentication
- Check repository permissions
- Validate issue template syntax
- Review GitHub API rate limits

### Dependency Errors

- Run `/user-story-validate` to check
- Use `check_dependencies.py` script
- Review dependency graph visualization
- Check for circular dependencies

### Validation Failing

- Review INVEST criteria in config
- Check story structure in YAML
- Verify acceptance criteria format
- Disable strict mode if needed

## Support

For issues, questions, or contributions:

1. Check documentation in `docs/`
2. Review examples in `docs/examples/`
3. Run validation scripts
4. Check logs in `user-story-system.log`

## License

Part of the LLM Configuration Management System project.

---

**Version:** 1.0.0
**Created:** 2025-11-03
**Author:** Matteo Cervelli / Claude Code
