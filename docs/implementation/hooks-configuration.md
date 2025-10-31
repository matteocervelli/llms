# Claude Code Hooks Configuration

## Overview

This document explains the hook configuration for this project and how hooks work with Claude Code's agent architecture.

## Current Hook Setup

### Pre-Commit Hook (Active)

**File**: `.claude/hooks/pre-commit.py`
**Type**: PreToolUse hook
**Triggers on**: `git commit` commands via Bash tool

**Purpose**: Runs automated quality checks before commits and provides feedback to Claude without blocking the commit.

**Behavior**:
- Runs pytest, black, mypy, and flake8 on staged Python files
- **Exit code 0**: Always allows commit to proceed
- **Feedback**: Prints quality check results to stderr for Claude to see
- **Claude's decision**: Claude sees issues and can decide to fix them before committing

**Configuration** (in `.claude/settings.json`):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/pre-commit.py",
            "timeout": 180
          }
        ]
      }
    ]
  }
}
```

### Post-Implementation Hook (Removed)

**Previously**: `.claude/hooks/post-implementation.py`
**Status**: ❌ Removed

**Why removed**:
1. **Conflicted with Feature-Implementer v2**: Phase 5 already handles validation
2. **Conflicted with agents**: Triggered inappropriately when agents finished work
3. **Too aggressive**: Simple keyword matching caused false triggers
4. **Redundant**: Pre-commit hook + explicit validation in workflows is sufficient

## Hook Architecture

### Hook Types in Claude Code

1. **PreToolUse**: Runs before tool execution (can validate, modify, or block)
2. **PostToolUse**: Runs after tool execution
3. **Stop**: Runs when Claude finishes responding
4. **SubagentStop**: Runs when a subagent finishes
5. **UserPromptSubmit**: Runs when user submits a prompt
6. **SessionStart/SessionEnd**: Runs at session boundaries

### Exit Codes

**PreToolUse hooks**:
- `0`: Success, allow tool to proceed
- `2`: Blocking error, prevent tool execution and feed stderr to Claude
- Other: Non-blocking error, show stderr to user

**Stop hooks**:
- `0`: Success, allow stopping
- `2`: Blocking error, prevent stopping and feed stderr to Claude
- Other: Non-blocking error, show stderr to user

### JSON Output Format

Hooks can return structured JSON for advanced control:

**PreToolUse**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow" | "deny" | "ask",
    "permissionDecisionReason": "explanation",
    "updatedInput": {
      "field_to_modify": "new value"
    }
  }
}
```

**Stop**:
```json
{
  "decision": "block" | undefined,
  "reason": "Explanation (required when decision is 'block')"
}
```

## Integration with Agents

### Pre-Commit Hook vs code-quality-specialist Agent

**Key Distinction**:

| Aspect | Pre-Commit Hook | code-quality-specialist Agent |
|--------|----------------|------------------------------|
| **When** | Before git commits | During Phase 5 validation |
| **Purpose** | Quick quality gate | Comprehensive validation |
| **Blocking** | No (exit 0) | Yes (via recursive communication) |
| **Scope** | Staged files only | Entire codebase |
| **Invocation** | Automatic | Explicit (Feature-Implementer Phase 5) |
| **Output** | Feedback to Claude | Detailed validation report |

**These do NOT conflict** - they serve different purposes:
- Hook = fast feedback loop on commits
- Agent = thorough validation during feature implementation

### Feature-Implementer v2 Workflow

The Feature-Implementer v2 workflow (`.claude/prompts/feature-implementer-main.md`) has **Phase 5: Validation** which explicitly invokes validation agents:

1. `@unit-test-specialist`
2. `@integration-test-specialist`
3. `@test-runner-specialist`
4. **`@code-quality-specialist`** ← This agent runs quality checks
5. `@security-specialist`
6. `@e2e-accessibility-specialist` (frontend only)

**No Stop hook needed** - validation is orchestrated explicitly in the workflow.

## Workflow Examples

### Commit Workflow with Pre-Commit Hook

1. Claude runs `git commit`
2. PreToolUse hook triggers
3. Hook runs pytest, black, mypy, flake8
4. Hook prints results to stderr (exit 0)
5. Claude sees results:
   - **If issues found**: Claude fixes them, stages changes, retries commit
   - **If no issues**: Commit proceeds successfully

### Feature Implementation with Validation

1. User runs `/feature-implement <issue-number>`
2. Phases 1-3: Analysis, Design, User Approval
3. **Phase 4**: Claude implements code with TDD
4. **Phase 5**: Validation orchestrator invokes `@code-quality-specialist`
   - Agent runs comprehensive quality checks
   - If issues found: Recursive communication to fix
   - If passing: Proceed to Phase 6
5. **Phase 6**: Deployment (commit, push, PR)

**Pre-commit hook runs during Phase 6 commit** - provides final quality gate.

## Best Practices

### When to Use Hooks vs Agents

**Use Hooks for**:
- ✅ Automated quality gates (pre-commit checks)
- ✅ Fast feedback loops
- ✅ Preventing accidental mistakes (committing secrets, etc.)
- ✅ Consistent enforcement across all commits

**Use Agents for**:
- ✅ Comprehensive validation
- ✅ Multi-step workflows (Feature-Implementer)
- ✅ Detailed reporting
- ✅ Flexible, context-aware decisions

### Hook Design Guidelines

1. **Exit with 0 for feedback, not blocking**: Let Claude decide next steps
2. **Avoid Stop hooks**: They're hard to control and cause confusion
3. **Keep hooks fast**: < 3 minutes total execution time
4. **Provide actionable feedback**: Tell Claude what to fix and how
5. **Don't overlap with agents**: Hooks and agents should complement, not duplicate

## Troubleshooting

### Hook Blocks Commits

**Symptom**: Git commits are blocked even when trying to commit
**Cause**: Hook exits with code 2
**Solution**: Change hook to exit with code 0 and provide feedback instead

### Hook Triggers Inappropriately

**Symptom**: Stop hook triggers when it shouldn't
**Cause**: Transcript analysis has false positives
**Solution**: Remove Stop hook, use explicit workflow orchestration instead

### Hook Conflicts with Agent

**Symptom**: Both hook and agent try to validate the same thing
**Cause**: Overlapping responsibilities
**Solution**: Define clear boundaries (hooks = fast gates, agents = comprehensive validation)

## Global vs Project Hooks

### Global Hooks (`~/.claude/hooks/`)

**Current Setup**:
- `pre-commit.py`: Runs for all projects with Python files

**Best for**:
- Universal quality standards
- Cross-project consistency
- Personal development preferences

### Project Hooks (`.claude/hooks/`)

**Current Setup**:
- `pre-commit.py`: Project-specific pre-commit checks

**Best for**:
- Project-specific requirements
- Team-shared standards
- Specialized workflows

**Priority**: Project hooks override global hooks when both exist.

## Configuration Files

### Project Settings

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/pre-commit.py",
            "timeout": 180
          }
        ]
      }
    ]
  }
}
```

### Global Settings

**File**: `~/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre-commit.py",
            "timeout": 180
          }
        ]
      }
    ]
  }
}
```

**Note**: Global hook references project-specific hook using `$CLAUDE_PROJECT_DIR` environment variable.

## Changes Made (2025-10-31)

### Summary

Fixed hook conflicts and blocking behavior to work seamlessly with agent architecture.

### Changes

1. **Modified `pre-commit.py`**:
   - Changed exit code from 2 to 0
   - Now provides feedback instead of blocking commits
   - Claude can see issues and decide whether to fix or proceed

2. **Removed Stop hooks**:
   - Deleted `.claude/hooks/post-implementation.py` (project)
   - Deleted `~/.claude/hooks/post-implementation.py` (global)
   - Removed Stop hook configuration from both settings files

3. **Kept `code-quality-specialist` agent**:
   - Agent is correctly used in Feature-Implementer Phase 5
   - No conflict with pre-commit hook (different purposes)

### Result

- ✅ Pre-commit hook provides feedback without blocking
- ✅ No Stop hook interference with workflow
- ✅ Agents work independently without hook conflicts
- ✅ Claude maintains decision-making control
- ✅ Quality checks still enforced via hook + agents

## References

- [Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks)
- [Claude Code Hooks Guide](https://docs.claude.com/en/docs/claude-code/hooks-guide)
- Feature-Implementer v2 Prompt: `.claude/prompts/feature-implementer-main.md`
- Code Quality Specialist Agent: `.claude/agents/code-quality-specialist.md`
