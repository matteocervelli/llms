# Claude Code Hooks

This directory contains custom hooks for Claude Code that enhance the development workflow with automatic quality checks and validation triggers.

## Hooks Overview

### Pre-Commit Hook (`pre-commit.py`)

**Purpose**: Enforce code quality standards before allowing git commits

**Triggers**: `PreToolUse` event for Bash commands containing `git commit`

**Quality Checks**:
1. **Black** - Code formatting validation
2. **Flake8** - Linting and style checking (max line length: 100)
3. **Mypy** - Static type checking
4. **Pytest** - Test suite execution

**Behavior**:
- ✅ **Blocking**: Exit code 2 prevents commits when checks fail
- ⚡ **Fast skip**: Only runs for Python projects (checks for `src/` or `tests/`)
- ⏱️ **Timeout**: 180 seconds (configurable in settings.json)
- 📋 **Detailed output**: Shows specific errors for each failed check

**Example Output**:
```
🔍 Running pre-commit quality checks...

  ✓ Checking code formatting (black)...
  ✓ Running linter (flake8)...
  ✓ Type checking (mypy)...
  ✓ Running tests (pytest)...

✅ All pre-commit checks passed!
```

### Post-Implementation Hook (`post-implementation.py`)

**Purpose**: Automatically trigger validation workflow after implementation completes

**Triggers**: `Stop` event (when main Claude agent finishes responding)

**Smart Detection**: Analyzes transcript for implementation completion markers:
- "implementation complete"
- "implementation phase complete"
- "all tests pass"
- "tests passing"
- "ready for validation"

**Behavior**:
- 🎯 **Smart trigger**: Only activates when implementation is detected
- 🔄 **Loop prevention**: Checks `stop_hook_active` to avoid infinite loops
- 📝 **Validation prompt**: Returns comprehensive validation checklist
- ⏱️ **Timeout**: 60 seconds (lightweight detection)

**Example Output**:
```
🎯 Implementation complete! Triggering validation workflow...
```

Returns validation prompt covering:
1. Code quality checks (black, mypy, flake8)
2. Test coverage (>= 80% target)
3. Performance validation
4. Security assessment
5. Acceptance criteria review
6. Validation report generation

## Configuration

Hooks are configured in `.claude/settings.json`:

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
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post-implementation.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

## Testing

### Test Pre-Commit Hook

```bash
# Simulate a git commit command
echo '{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m \"test\"",
    "description": "Test commit"
  },
  "cwd": "/home/user/llms"
}' | python3 .claude/hooks/pre-commit.py

echo "Exit code: $?"
```

**Expected Results**:
- Exit code 0: All checks passed
- Exit code 2: Checks failed (commit blocked)
- Detailed error messages for each failed check

### Test Post-Implementation Hook

```bash
# Create test transcript with completion marker
cat > /tmp/test-transcript.jsonl <<EOF
{"role": "assistant", "content": "Implementation phase complete. All tests passing."}
EOF

# Simulate Stop event
echo '{
  "hook_event_name": "Stop",
  "transcript_path": "/tmp/test-transcript.jsonl",
  "cwd": "/home/user/llms",
  "stop_hook_active": false
}' | python3 .claude/hooks/post-implementation.py
```

**Expected Results**:
- JSON output with `"decision": "block"`
- Comprehensive validation prompt in `reason` field
- Exit code 0 (successful detection)

## Customization

### Adjust Pre-Commit Quality Standards

Edit `pre-commit.py`:

```python
# Customize flake8 max line length
run_command(
    ["flake8", "src/", "tests/", "--max-line-length=120"],  # Changed from 100
    project_dir
)

# Skip specific checks
run_command(
    ["flake8", "src/", "tests/", "--extend-ignore=E203,W503,E501"],
    project_dir
)
```

### Customize Post-Implementation Detection

Edit `post-implementation.py`:

```python
# Add more completion markers
completion_markers = [
    "implementation complete",
    "feature complete",
    "ready to validate",
    # Add your custom markers here
]
```

### Adjust Timeouts

Edit `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "...",
        "timeout": 300  // 5 minutes for large test suites
      }]
    }]
  }
}
```

## Debugging

### Enable Debug Output

Run Claude Code with debug flag:
```bash
claude --debug
```

Check hook execution in output:
```
[DEBUG] Executing hooks for PreToolUse:Bash
[DEBUG] Hook command completed with status 2
```

### View Hook Logs

Pre-commit hook outputs to stderr:
```bash
# Capture hook output
python3 .claude/hooks/pre-commit.py < test-input.json 2>&1 | tee hook-output.log
```

### Common Issues

**Issue**: Hook doesn't trigger
- **Solution**: Verify hooks are registered with `/hooks` command in Claude Code
- **Solution**: Check settings.json syntax is valid JSON

**Issue**: Hook times out
- **Solution**: Increase timeout in settings.json
- **Solution**: Optimize quality checks (skip slow tests)

**Issue**: Hook blocks valid commits
- **Solution**: Fix quality issues reported in error output
- **Solution**: Temporarily disable hook in `.claude/settings.local.json`

## Disable Hooks

### Temporarily Disable (Local)

Create `.claude/settings.local.json`:
```json
{
  "hooks": {}
}
```

### Disable Specific Hook

Edit `.claude/settings.json` and remove the hook configuration.

## Security

### Pre-Commit Hook Security
- ✅ JSON input validation
- ✅ No shell injection (uses subprocess with list arguments)
- ✅ Timeout protection (180 seconds)
- ✅ Project type validation (only runs for Python projects)

### Post-Implementation Hook Security
- ✅ Safe transcript reading (no code execution)
- ✅ Infinite loop prevention (`stop_hook_active` check)
- ✅ JSON output validation
- ✅ No sensitive data exposure

## Integration with Feature-Implementer v2

These hooks enhance the Feature-Implementer v2 workflow:

```
Phase 1: Requirements Analysis
    ↓
Phase 2: Architecture Design
    ↓
Phase 3: Implementation
    ↓ [Pre-commit hook validates before each commit]
    ↓
Implementation Complete
    ↓ [Post-implementation hook automatically triggers]
    ↓
Phase 4: Validation ← Automatic transition
    ↓
Phase 5: Deployment
```

## Learn More

- **Claude Code Hooks Reference**: https://docs.claude.com/en/docs/claude-code/hooks
- **Hooks Guide**: https://docs.claude.com/en/docs/claude-code/hooks-guide
- **Implementation Documentation**: `docs/implementation/issue-52-hooks-implementation.md`

---

**Created**: 2025-10-29
**Issue**: #52
**Branch**: claude/implement-issue-52-011CUbwNA4AnKdDuacscniGH
