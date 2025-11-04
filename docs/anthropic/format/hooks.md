# Hooks Format Guide

## Configuration Format

Hooks use **JSON configuration** in `settings.json`, **not YAML frontmatter**.

## Basic Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

## Matcher Patterns

- **Exact match**: `"Write"`
- **Regex**: `"Edit|Write"` or `"Notebook.*"`
- **Wildcard**: `"*"` (matches all tools)
- **No matcher**: Omit for events without tool matching

## Hook Types

### Command Hook

```json
{
  "type": "command",
  "command": "bash-command",
  "timeout": 30
}
```

### Prompt Hook

```json
{
  "type": "prompt",
  "prompt": "Your prompt with $ARGUMENTS placeholder",
  "timeout": 30
}
```

## Supported Events

- **PreToolUse** - Before tool execution
- **PostToolUse** - After tool execution
- **UserPromptSubmit** - When user submits prompt
- **Stop** - Main conversation stops
- **SubagentStop** - Sub-agent stops
- **PreCompact** - Before conversation compaction
- **SessionStart** - Session begins
- **SessionEnd** - Session ends
- **Notification** - Notification events

## Example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "black $FILE_PATH",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Official Documentation

https://docs.claude.com/en/docs/claude-code/hooks
