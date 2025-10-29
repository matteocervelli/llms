# Migration Guide: v1 to v2 Architecture

**Version**: 1.0.0
**Date**: 2025-10-29
**Status**: Production Ready

## Overview

This guide helps you migrate from the v1 monolithic feature implementation approach to the v2 multi-agent architecture. The v2 architecture represents a significant advancement with 14 specialized agents, 37 production skills, and automated quality gates.

## What Changed

### Architecture Transformation

**v1 Architecture** (Monolithic):
```
/feature-implement command (187 lines)
└── All logic inline
    ├── Requirements analysis
    ├── Design & planning
    ├── Implementation
    ├── Testing
    └── Documentation
```

**v2 Architecture** (Multi-Agent):
```
/feature-implement command (15 lines)
└── @feature-implementer agent
    ├── Phase 1: @analysis-specialist
    ├── Phase 2: @design-orchestrator
    │   ├── @architecture-designer
    │   ├── @documentation-researcher
    │   └── @dependency-manager
    ├── Phase 3: User Approval
    ├── Phase 4: Implementation (main agent)
    ├── Phase 5: @validation-orchestrator
    │   ├── @unit-test-specialist
    │   ├── @integration-test-specialist
    │   ├── @test-runner-specialist
    │   ├── @code-quality-specialist
    │   ├── @security-specialist
    │   └── @e2e-accessibility-specialist
    └── Phase 6: @deployment-specialist
```

### Key Differences

| Aspect | v1 | v2 |
|--------|----|----|
| **Command Size** | 187 lines | 15 lines (92% reduction) |
| **Token Cost** | ~124,000 tokens upfront | ~300 tokens (99.76% reduction) |
| **Architecture** | Monolithic single command | Multi-agent orchestration |
| **Context Loading** | All at once | Progressive disclosure |
| **Agents** | 0 | 14 specialized agents |
| **Skills** | 0 | 37 production skills |
| **Hooks** | None | 2 (pre-commit, post-implementation) |
| **Quality Gates** | Manual | Automated |
| **Workflow Phases** | Ad-hoc | 6 structured phases |
| **Validation** | Manual | Recursive automated |
| **Documentation** | Basic | Comprehensive (analysis, PRP, reports) |

## Breaking Changes

### 1. Command Invocation

**v1**:
```bash
/feature-implement 123
```

**v2**:
```bash
@feature-implementer implement issue #123
```

The v1 slash command is now a thin wrapper that invokes the v2 agent.

### 2. Workflow Structure

**v1**: Linear execution with all logic in one command
**v2**: 6-phase orchestrated workflow with user approval checkpoint

### 3. Output Documents

**v1**: Minimal documentation
- Basic implementation notes

**v2**: Structured documentation
- `docs/implementation/analysis/analysis.md` (Phase 1)
- `docs/implementation/prp/prp.md` (Phase 2)
- Test reports (Phase 5)
- Security scan reports (Phase 5)
- Validation reports (Phase 5)
- Updated documentation (Phase 6)

### 4. Quality Enforcement

**v1**: Optional manual checks
**v2**: Mandatory automated quality gates via hooks

### 5. Model Selection

**v1**: Single model (typically Sonnet)
**v2**: Multi-model optimization
- Haiku: Fast, cost-effective tasks (analysis, testing, deployment)
- Sonnet: Balanced reasoning (orchestration, security)
- Opus: Deep reasoning (architecture design)

## Migration Steps

### Step 1: Update Your Workflow

**Before (v1)**:
```bash
# Old command
/feature-implement 123

# Everything happens in one shot
# No intermediate approval
# Manual quality checks
```

**After (v2)**:
```bash
# New agent invocation
@feature-implementer implement issue #123

# Phase 1: Analysis (automatic)
# Phase 2: Design (automatic with 3 parallel sub-agents)
# Phase 3: Approval (WAIT FOR USER)
# Phase 4: Implementation (automatic)
# Phase 5: Validation (automatic with 6 sequential specialists)
# Phase 6: Deployment (automatic)
```

### Step 2: Understand the Approval Checkpoint

In v2, you **MUST** explicitly approve the design before implementation proceeds.

**What to Review in Phase 3**:
- `docs/implementation/analysis/analysis.md` - Requirements and security assessment
- `docs/implementation/prp/prp.md` - Architecture, data models, APIs, dependencies

**How to Approve**:
```
Reviewer: "The design looks good, please proceed with implementation"
```

**How to Request Changes**:
```
Reviewer: "Please revise the API to use REST instead of GraphQL"
```

The agent will cycle back to Phase 2, regenerate the design, and present again for approval.

### Step 3: Leverage Automated Quality Gates

v2 enforces quality automatically via hooks:

**Pre-commit Hook** (automatic):
- Runs before every `git commit`
- Executes: Black → Flake8 → Mypy → Pytest
- **Blocks commit** if checks fail

**Post-implementation Hook** (automatic):
- Triggers when implementation completes
- Auto-launches validation workflow
- Recursive validation until all checks pass

**What This Means**:
- No more manual quality checks
- Consistent code quality
- Test coverage ≥80% enforced
- Security scanning automatic

### Step 4: Adopt Progressive Disclosure

v2 uses **progressive disclosure** - context loads only when needed:

**v1**: All prompt text (124,000 tokens) loaded upfront
**v2**: Only active agent prompt loaded (~300 tokens)

**What This Means**:
- Faster response times
- Lower token costs (99.76% reduction)
- Better context utilization
- Cleaner conversation history

**How It Works**:
- Skills auto-activate based on task descriptions
- Agents load only when invoked
- Context released after phase completes

### Step 5: Update Documentation Expectations

v2 produces comprehensive structured documentation:

**Analysis Document** (`docs/implementation/analysis/analysis.md`):
- Requirements extraction
- Security assessment (OWASP, data privacy)
- Tech stack evaluation
- Dependencies identified

**PRP Document** (`docs/implementation/prp/prp.md`):
- Problem statement
- Requirements detailed
- Architecture plan
- Component design
- Data models
- API contracts
- Dependency analysis

**Validation Reports** (Phase 5 outputs):
- Test execution results
- Coverage analysis (≥80% required)
- Code quality checks (Black, Flake8, Mypy)
- Security scan (OWASP Top 10)
- E2E test results (frontend)
- Accessibility audit (WCAG 2.1 AA, frontend)

### Step 6: Configure Hooks (If Not Already Done)

Hooks are auto-configured in issue #52, but verify:

**Check hooks exist**:
```bash
ls -la .claude/hooks/
# Should see: pre-commit.py, post-implementation.py
```

**Check settings.json**:
```bash
cat .claude/settings.json
```

Should contain:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre-commit.py", "timeout": 180}]
    }],
    "Stop": [{
      "hooks": [{"type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post-implementation.py", "timeout": 60}]
    }]
  }
}
```

**If missing**: See [issue #52 documentation](../implementation/issue-52-hooks-implementation.md)

## Common Migration Scenarios

### Scenario 1: Simple Feature Implementation

**v1**:
```bash
/feature-implement 123
# Wait for completion
# Manually run tests
# Manually commit
```

**v2**:
```bash
@feature-implementer implement issue #123
# Phase 1-2: Automatic analysis and design
# Phase 3: Review and approve design
# Phase 4-6: Automatic implementation, validation, deployment
# Pre-commit hook runs on git commit (automatic)
```

### Scenario 2: Feature with Security Requirements

**v1**:
```bash
/feature-implement 456
# Implementation happens
# Manual security review needed
# Manual OWASP checks
```

**v2**:
```bash
@feature-implementer implement issue #456
# Phase 1: Automatic security assessment (OWASP, data privacy)
# Phase 2: Security considerations in architecture
# Phase 5: Automatic security scanning (OWASP Top 10)
# Security requirements enforced throughout
```

### Scenario 3: Frontend Feature with Accessibility

**v1**:
```bash
/feature-implement 789
# Implementation happens
# Manual E2E testing
# Manual accessibility checks
```

**v2**:
```bash
@feature-implementer implement issue #789
# Phase 5: Automatic E2E testing (Playwright)
# Phase 5: Automatic WCAG 2.1 AA compliance check
# E2E specialist only activates for frontend features
```

### Scenario 4: Feature Needing Latest Library Docs

**v1**:
```bash
/feature-implement 101
# Implementation with potentially outdated docs
# Manual doc lookup if needed
```

**v2**:
```bash
@feature-implementer implement issue #101
# Phase 2: @documentation-researcher sub-agent
# Auto-fetches latest library docs via context7-mcp
# Design based on current best practices
```

## Backward Compatibility

### What's Preserved

✅ **Project structure**: No changes required
✅ **Git workflow**: Commits, PRs work the same
✅ **Test framework**: pytest, jest, etc. unchanged
✅ **Code standards**: Same quality requirements
✅ **GitHub integration**: Issues, PRs, labels work the same

### What's Not Compatible

❌ **v1 slash command syntax**: Use `@feature-implementer` instead
❌ **Manual quality workflow**: Hooks now enforce automatically
❌ **Ad-hoc implementation**: Must follow 6-phase workflow
❌ **Skip approval**: Phase 3 approval required before implementation

## Rollback Strategy

If you need to temporarily use v1 behavior:

### Option 1: Use Legacy Command

The v1 command is archived as `/feature-implement-legacy`:

```bash
/feature-implement-legacy 123 false
```

**Note**: Legacy command lacks:
- Multi-agent orchestration
- Progressive disclosure
- Automated quality gates
- Structured documentation
- Recursive validation

### Option 2: Disable Hooks Temporarily

```bash
# Temporarily disable hooks
mv .claude/settings.json .claude/settings.json.backup
echo '{"hooks": {}}' > .claude/settings.json

# Use v2 without quality gates
@feature-implementer implement issue #123

# Re-enable hooks
mv .claude/settings.json.backup .claude/settings.json
```

### Option 3: Manual Implementation

Implement manually without the agent:

```bash
# Analyze issue yourself
# Design architecture yourself
# Implement code
# Run tests manually: pytest
# Run quality checks manually: black, flake8, mypy
# Commit (pre-commit hook still runs if enabled)
```

## Troubleshooting

### Issue: Agent doesn't respond

**Symptom**: `@feature-implementer` does nothing

**Solution**:
1. Check agent file exists: `ls .claude/agents/feature-implementer.md`
2. Verify syntax: `@feature-implementer implement issue #123`
3. Check no typos in agent name

### Issue: Skills not activating

**Symptom**: Agent doesn't load expected skills

**Solution**:
1. Check skill directories exist: `ls .claude/skills/`
2. Verify each has `SKILL.md`: `find .claude/skills -name "SKILL.md"`
3. Describe task clearly to trigger skill activation

### Issue: Hooks not running

**Symptom**: Pre-commit doesn't run, or post-implementation doesn't trigger validation

**Solution**:
1. Check hooks exist: `ls .claude/hooks/*.py`
2. Verify settings.json: `cat .claude/settings.json`
3. Check hook permissions: `ls -la .claude/hooks/*.py` (should be executable)
4. Make executable: `chmod +x .claude/hooks/*.py`

### Issue: Approval checkpoint skipped

**Symptom**: Implementation starts without user approval

**Solution**:
- This shouldn't happen - agent waits for explicit approval
- If it does, report as a bug
- Use plan mode to review design before execution

### Issue: Validation fails repeatedly

**Symptom**: Phase 5 validation keeps failing and retrying

**Solution**:
1. Review validation reports in terminal output
2. Fix identified issues (test failures, linting, security)
3. Recursive validation will continue until all checks pass
4. If stuck, manually fix issues and ask agent to re-validate

### Issue: Token costs higher than expected

**Symptom**: Using more tokens than v1

**Solution**:
- Progressive disclosure should reduce costs 99.76%
- If costs are high, check:
  - Are you loading unnecessary context?
  - Are skills being re-activated multiple times?
  - Is validation failing and retrying excessively?

## FAQ

### Q: Do I need to migrate existing features?

**A**: No. v2 is for **new feature implementation**. Existing features work as-is. Only use v2 for new GitHub issues.

### Q: Can I use v2 for bug fixes?

**A**: Yes, but consider `/issue-fix` command instead, which is optimized for bug fixes. v2 is designed for new features.

### Q: How long does v2 take vs v1?

**A**: v2 typically takes 10-20% longer due to structured phases, but produces:
- Better architecture
- Comprehensive tests
- Security validation
- Complete documentation
- Higher quality code

The time investment pays off in reduced technical debt.

### Q: Can I skip phases?

**A**: No. All phases are required for quality. However:
- Phase 3 (Approval) is quick if design is good
- Phase 5 (Validation) is automatic
- Phase 6 (Deployment) is automatic

### Q: What if my project doesn't have frontend?

**A**: The E2E/Accessibility specialist only activates for frontend features. It's automatically skipped for backend-only projects.

### Q: Can I customize the workflow?

**A**: Yes. You can:
- Modify agent prompts in `.claude/agents/`
- Adjust skill guidance in `.claude/skills/`
- Configure hooks in `.claude/hooks/`
- Set quality standards in validation skills

See [User Guide](../guides/feature-implementer-v2-guide.md) for customization details.

### Q: How do I know which phase I'm in?

**A**: The agent clearly announces each phase:
```
Phase 1: Requirements Analysis
Phase 2: Architecture & Design
Phase 3: User Approval
Phase 4: Implementation
Phase 5: Validation
Phase 6: Deployment
```

### Q: Can I use v2 with other LLMs (Codex, OpenCode)?

**A**: Not yet. v2 is Claude Code-specific. Multi-LLM support planned for Sprint 5+.

### Q: Is v2 production-ready?

**A**: Yes! v1.0.0 release (2025-10-29) marks production readiness:
- All 14 agents verified
- All 37 skills tested
- Hooks validated
- Complete workflow tested
- Comprehensive documentation

## Resources

- **User Guide**: [docs/guides/feature-implementer-v2-guide.md](../guides/feature-implementer-v2-guide.md)
- **Architecture**: [docs/architecture/feature-implementer-v2.md](feature-implementer-v2.md)
- **Skills Mapping**: [docs/architecture/skills-mapping.md](skills-mapping.md)
- **Implementation Plan**: [docs/architecture/implementation-plan.md](implementation-plan.md)
- **CHANGELOG**: [CHANGELOG.md](../../CHANGELOG.md)

## Support

For issues, questions, or feedback:
- **GitHub Issues**: https://github.com/matteocervelli/llms/issues
- **GitHub Discussions**: https://github.com/matteocervelli/llms/discussions

---

**Prepared by**: Feature-Implementer v2 Architecture Team
**Last Updated**: 2025-10-29
**Version**: 1.0.0
