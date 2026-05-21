# User Story System - Deployment Guide

This guide covers deploying the user story system globally to make it available across all your projects.

## Overview

The system consists of:
- **Scripts**: Python and shell scripts in `scripts/`
- **Skills**: Claude Code skills in `.claude/skills/`
- **Commands**: Slash commands in `.claude/commands/`
- **Agents**: Sub-agents in `.claude/agents/`
- **Config**: Configuration files in `config/`
- **Templates**: YAML and Markdown templates in `templates/`

## Deployment Strategy

### Option 1: Keep Local (Recommended for Testing)

Use the system within this project only:
```bash
# Already set up! Just use the commands:
/user-story-new
/user-story-refine
/user-story-sprint
```

**Pros:**
- No system-wide changes
- Easy to test and iterate
- Project-specific configuration

**Cons:**
- Only available in this project
- Need to copy to other projects

### Option 2: Global Deployment (Production Use)

Make the system available globally across all projects.

## Global Deployment Steps

### 1. Create Global Symlinks for Skills

```bash
# Create global skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Symlink each skill
ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/skills/user-story-generator ~/.claude/skills/user-story-generator

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/skills/story-validator ~/.claude/skills/story-validator

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/skills/technical-annotator ~/.claude/skills/technical-annotator

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/skills/dependency-analyzer ~/.claude/skills/dependency-analyzer

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/skills/sprint-planner ~/.claude/skills/sprint-planner
```

### 2. Create Global Symlinks for Commands

```bash
# Create global commands directory if it doesn't exist
mkdir -p ~/.claude/commands

# Symlink each command
ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/commands/user-story-new.md ~/.claude/commands/user-story-new.md

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/commands/user-story-refine.md ~/.claude/commands/user-story-refine.md

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/commands/user-story-annotate.md ~/.claude/commands/user-story-annotate.md

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/commands/user-story-deps.md ~/.claude/commands/user-story-deps.md

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/commands/user-story-sprint.md ~/.claude/commands/user-story-sprint.md
```

### 3. Create Global Symlinks for Agents

```bash
# Create global agents directory if it doesn't exist
mkdir -p ~/.claude/agents

# Symlink each agent
ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/agents/qa-validator-agent.md ~/.claude/agents/qa-validator-agent.md

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/agents/technical-annotator-agent.md ~/.claude/agents/technical-annotator-agent.md

ln -sf /Users/matteocervelli/dev/projects/llms/user-story-system/.claude/agents/story-orchestrator-agent.md ~/.claude/agents/story-orchestrator-agent.md
```

### 4. Add Scripts to PATH (Optional)

Make scripts globally accessible:

```bash
# Add to ~/.zshrc or ~/.bashrc
export PATH="/Users/matteocervelli/dev/projects/llms/user-story-system/scripts:$PATH"

# Then reload
source ~/.zshrc  # or source ~/.bashrc
```

Now you can run scripts from anywhere:
```bash
validate_story_invest.py --story-id US-0001
generate_story_from_yaml.py --all
```

### 5. Verification

Verify global deployment:

```bash
# Check skills
ls -la ~/.claude/skills/ | grep user-story

# Check commands
ls -la ~/.claude/commands/ | grep user-story

# Check agents
ls -la ~/.claude/agents/ | grep -E "(validator|annotator|orchestrator)"

# Test a command
cd ~/some-other-project
/user-story-new --help  # Should work!
```

## Automated Deployment Script

Save this as `scripts/deploy-global.sh`:

```bash
#!/usr/bin/env bash
# deploy-global.sh - Deploy user story system globally

set -euo pipefail

SYSTEM_DIR="/Users/matteocervelli/dev/projects/llms/user-story-system"
GLOBAL_CLAUDE="$HOME/.claude"

echo "🚀 Deploying User Story System globally..."

# Create directories
mkdir -p "$GLOBAL_CLAUDE/skills"
mkdir -p "$GLOBAL_CLAUDE/commands"
mkdir -p "$GLOBAL_CLAUDE/agents"

echo "📁 Created global directories"

# Symlink skills
echo "🔗 Symlinking skills..."
for skill in user-story-generator story-validator technical-annotator dependency-analyzer sprint-planner; do
    ln -sf "$SYSTEM_DIR/.claude/skills/$skill" "$GLOBAL_CLAUDE/skills/$skill"
    echo "  ✅ $skill"
done

# Symlink commands
echo "🔗 Symlinking commands..."
for cmd in user-story-new user-story-refine user-story-annotate user-story-deps user-story-sprint; do
    ln -sf "$SYSTEM_DIR/.claude/commands/$cmd.md" "$GLOBAL_CLAUDE/commands/$cmd.md"
    echo "  ✅ $cmd"
done

# Symlink agents
echo "🔗 Symlinking agents..."
for agent in qa-validator-agent technical-annotator-agent story-orchestrator-agent; do
    ln -sf "$SYSTEM_DIR/.claude/agents/$agent.md" "$GLOBAL_CLAUDE/agents/$agent.md"
    echo "  ✅ $agent"
done

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Verification:"
echo "  Skills: $(ls -1 $GLOBAL_CLAUDE/skills/ | grep user-story | wc -l) symlinks"
echo "  Commands: $(ls -1 $GLOBAL_CLAUDE/commands/ | grep user-story | wc -l) symlinks"
echo "  Agents: $(ls -1 $GLOBAL_CLAUDE/agents/ | grep -E '(validator|annotator|orchestrator)' | wc -l) symlinks"
echo ""
echo "🎯 Test it:"
echo "  cd ~/any-project"
echo "  /user-story-new"
```

Run it:
```bash
chmod +x scripts/deploy-global.sh
./scripts/deploy-global.sh
```

## Project-Specific Setup

When using the system in a new project:

### 1. Create User Story Directories

```bash
mkdir -p stories/{yaml-source,generated-docs,backlog}
mkdir -p epics
```

### 2. Copy Configuration (Optional)

If you want project-specific configuration:

```bash
mkdir -p config
cp /Users/matteocervelli/dev/projects/llms/user-story-system/config/automation-config.yaml config/
cp /Users/matteocervelli/dev/projects/llms/user-story-system/config/personas.yaml config/
```

Edit config files for project-specific settings.

### 3. Copy Templates (Optional)

If you want custom templates:

```bash
mkdir -p templates
cp /Users/matteocervelli/dev/projects/llms/user-story-system/templates/* templates/
```

### 4. Initialize Counters

```bash
echo "1" > .story_counter
echo "1" > .epic_counter
```

### 5. Configure GitHub Integration

Edit `config/automation-config.yaml`:

```yaml
github:
  enabled: true
  auto_sync: true
  repo:
    auto_detect: true  # Or set manually: "owner/repo"
```

## Usage Across Projects

After global deployment:

```bash
# In any project
cd ~/my-project

# Create story structure (one-time)
mkdir -p stories/{yaml-source,generated-docs,backlog} epics

# Use commands immediately
/user-story-new "Add payment processing"
/user-story-refine backlog
/user-story-sprint 40
```

## Uninstalling

To remove global deployment:

```bash
# Remove symlinks
rm ~/.claude/skills/user-story-*
rm ~/.claude/skills/story-*
rm ~/.claude/skills/dependency-*
rm ~/.claude/skills/sprint-*
rm ~/.claude/commands/user-story-*
rm ~/.claude/agents/qa-validator-agent.md
rm ~/.claude/agents/technical-annotator-agent.md
rm ~/.claude/agents/story-orchestrator-agent.md

# Remove from PATH (edit ~/.zshrc or ~/.bashrc)
# Remove the export PATH line
```

## Updating the System

After making changes to the system:

1. Changes are automatically reflected (symlinks!)
2. No need to re-deploy
3. Test in the source project first
4. Changes apply globally once tested

## Backup Considerations

The system files are in:
- `/Users/matteocervelli/dev/projects/llms/user-story-system/`

Include this in your backup strategy:
- Git commit changes regularly
- Push to remote repository
- Back up configuration files

## Troubleshooting

### Commands Not Found

```bash
# Check symlinks
ls -la ~/.claude/commands/ | grep user-story

# If missing, re-run deployment script
./scripts/deploy-global.sh
```

### Scripts Not Executable

```bash
chmod +x /Users/matteocervelli/dev/projects/llms/user-story-system/scripts/*.py
chmod +x /Users/matteocervelli/dev/projects/llms/user-story-system/scripts/*.sh
```

### Python Dependencies Missing

```bash
cd /Users/matteocervelli/dev/projects/llms/user-story-system
pip install -r requirements.txt
```

### GitHub Integration Not Working

```bash
# Check GitHub CLI
gh auth status

# Login if needed
gh auth login

# Check repo detection
cd your-project
gh repo view
```

## Best Practices

### 1. Version Control

- Commit the system to git
- Tag releases (v1.0.0, v1.1.0, etc.)
- Document breaking changes

### 2. Project Organization

- Keep story files in `stories/` directory
- Use consistent naming (US-0001, EP-001)
- Commit story files to project repository

### 3. Configuration Management

- Use global config for defaults
- Override with project-specific config when needed
- Document custom personas

### 4. Team Collaboration

- Share story files via git
- Use GitHub issues for tracking
- Review stories in PRs

## Next Steps

After deployment:

1. **Test the System**: Create a few test stories
2. **Customize Config**: Adjust personas and settings
3. **Train Team**: Share user guide with team
4. **Integrate with Workflow**: Make stories part of planning process
5. **Iterate**: Gather feedback and improve

## Support

For issues or questions:
1. Check documentation in `docs/`
2. Review examples in `docs/examples/`
3. Run tests: `pytest tests/`
4. Check logs: `user-story-system.log`

---

**Deployment Status**: Ready for Production ✅
