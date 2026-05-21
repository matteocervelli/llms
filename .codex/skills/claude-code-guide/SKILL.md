---
name: claude-code-guide
description: "Fetch Claude Code documentation and help update configuration. Use /claude-code-guide <topic> where topic is: memory, skills, hooks, agents, settings, mcp, plugins, cli, overview, all"
---

## Purpose

Fetch the latest Claude Code documentation from code.claude.com and help update your configuration files based on current best practices.

## Usage

/claude-code-guide <topic>

## Topics

| Topic      | Description             | Doc URLs                       | Config Files                       |
| ---------- | ----------------------- | ------------------------------ | ---------------------------------- |
| `memory`   | CLAUDE.md configuration | /memory, /best-practices       | CLAUDE.md, CLAUDE.local.md         |
| `skills`   | Skills system           | /skills                        | .claude/skills/\*.md               |
| `hooks`    | Hooks configuration     | /hooks, /hooks-guide           | .claude/hooks/, settings.json      |
| `agents`   | Custom subagents        | /sub-agents                    | .claude/agents/\*.md               |
| `settings` | Settings.json config    | /settings                      | settings.json, settings.local.json |
| `mcp`      | MCP servers             | /mcp                           | settings.json mcpServers           |
| `plugins`  | Plugin system           | /plugins, /plugin-marketplaces | plugins/                           |
| `cli`      | CLI reference           | /cli-reference                 | N/A (reference)                    |
| `overview` | Features overview       | /features-overview             | N/A (reference)                    |
| `all`      | Full documentation      | All above                      | All config files                   |

---

## Embedded Best Practices

### Memory (CLAUDE.md)

**File Locations & Precedence (highest to lowest):**

1. **Managed policy**: `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) - org-wide
2. **Project memory**: `./CLAUDE.md` or `./.claude/CLAUDE.md` - team-shared
3. **Project rules**: `./.claude/rules/*.md` - modular topic-specific rules
4. **User memory**: `~/.claude/CLAUDE.md` - personal across all projects
5. **Project local**: `./CLAUDE.local.md` - personal project-specific (gitignored)

**Best Practices:**

- Be specific: "Use 2-space indentation" beats "Format code properly"
- Use structure: Format memories as bullet points under descriptive markdown headings
- Review periodically: Update as project evolves
- Use imports: `@path/to/file` syntax to include other files
- Path-specific rules: Use YAML frontmatter with `paths` field for conditional rules

**Example CLAUDE.md:**

```markdown
# Project Standards

- Use TypeScript strict mode
- Follow ESLint airbnb config
- Write tests for all new functions

# Commands

- Build: `npm run build`
- Test: `npm test`
- Lint: `npm run lint`

# Architecture

- React components in src/components/
- API routes in src/api/
- Shared utilities in src/utils/
```

**Modular Rules (.claude/rules/):**

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All endpoints must include input validation
- Use standard error response format
- Include OpenAPI documentation comments
```

---

### Skills

**Location:** `.claude/skills/<skill-name>/SKILL.md`

**Frontmatter Fields:**
| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name (defaults to directory name) |
| `description` | Recommended | When to use this skill |
| `argument-hint` | No | Hint for arguments, e.g., `[filename]` |
| `disable-model-invocation` | No | `true` = only user can invoke |
| `user-invocable` | No | `false` = only Claude can invoke |
| `allowed-tools` | No | Restrict tools available |
| `model` | No | Model override |
| `context` | No | `fork` = run in subagent |
| `agent` | No | Subagent type when `context: fork` |

**Example Skill:**

```yaml
---
name: code-review
description: Reviews code for quality and best practices. Use after code changes.
allowed-tools: Read, Grep, Glob
---

When reviewing code:
1. Check for code clarity and readability
2. Look for potential bugs
3. Verify error handling
4. Check test coverage
5. Note security concerns

Provide feedback organized by priority:
- Critical (must fix)
- Warnings (should fix)
- Suggestions (consider)
```

**Supporting Files:** Skills can include additional files (templates, scripts, examples) referenced from SKILL.md.

**String Substitutions:**

- `$ARGUMENTS` - User-provided arguments
- `${CLAUDE_SESSION_ID}` - Current session ID

---

### Hooks

**Configuration Location:** `settings.json` under `hooks` key

**Available Hook Events:**
| Event | When | Matcher |
|-------|------|---------|
| `SessionStart` | Session begins | startup, resume, clear, compact |
| `UserPromptSubmit` | User submits prompt | - |
| `PreToolUse` | Before tool execution | Tool name |
| `PermissionRequest` | Permission dialog | Tool name |
| `PostToolUse` | After tool succeeds | Tool name |
| `PostToolUseFailure` | After tool fails | Tool name |
| `SubagentStart` | Subagent spawns | Agent type |
| `SubagentStop` | Subagent finishes | Agent type |
| `Stop` | Claude finishes | - |
| `PreCompact` | Before compaction | manual, auto |
| `SessionEnd` | Session terminates | - |

**Hook Configuration Structure:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Exit Codes:**

- `0`: Success (stdout shown in verbose mode)
- `2`: Blocking error (stderr fed back to Claude)
- Other: Non-blocking error

**Environment Variables:**

- `CLAUDE_PROJECT_DIR`: Project root path
- `CLAUDE_ENV_FILE`: (SessionStart only) File for persisting env vars

---

### Agents (Subagents)

**Location:** `.claude/agents/<agent-name>.md` or `~/.claude/agents/`

**Built-in Agents:**

- `Explore`: Fast, read-only, uses Haiku
- `Plan`: Research for plan mode, inherits model
- `general-purpose`: Full tools, complex tasks

**Frontmatter Fields:**
| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier |
| `description` | Yes | When to delegate |
| `tools` | No | Allowed tools (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | No | Skills to preload |
| `hooks` | No | Lifecycle hooks |

**Example Agent:**

```yaml
---
name: code-reviewer
description: Expert code review. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer ensuring high standards.

When invoked:
1. Run git diff to see changes
2. Focus on modified files
3. Review for quality, security, performance

Provide feedback by priority:
- Critical (must fix)
- Warnings (should fix)
- Suggestions (consider)
```

---

### Settings

**File Locations (precedence highest to lowest):**

1. **Managed**: System-level `managed-settings.json`
2. **CLI arguments**: Session overrides
3. **Local project**: `.claude/settings.local.json`
4. **Project**: `.claude/settings.json`
5. **User**: `~/.claude/settings.json`

**Key Settings:**
| Key | Description |
|-----|-------------|
| `permissions` | Allow/deny/ask rules for tools |
| `hooks` | Hook configurations |
| `env` | Environment variables |
| `model` | Default model override |
| `attribution` | Git commit/PR attribution |
| `mcpServers` | MCP server configurations |
| `enabledPlugins` | Plugin enable/disable |

**Permissions Example:**

```json
{
  "permissions": {
    "allow": ["Bash(npm run lint)", "Bash(npm run test:*)"],
    "deny": ["Bash(curl:*)", "Read(./.env)"],
    "additionalDirectories": ["../docs/"]
  }
}
```

---

### MCP Servers

**Adding Servers:**

```bash
# HTTP transport (recommended for remote)
claude mcp add --transport http <name> <url>

# SSE transport (deprecated)
claude mcp add --transport sse <name> <url>

# Stdio transport (local)
claude mcp add --transport stdio <name> -- <command> [args...]
```

**Scopes:**

- `local` (default): Current project, private
- `project`: Shared via `.mcp.json`
- `user`: All your projects

**Example .mcp.json:**

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "db": {
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${DB_URL}"]
    }
  }
}
```

**Commands:**

- `claude mcp list` - List servers
- `claude mcp get <name>` - Get details
- `claude mcp remove <name>` - Remove server
- `/mcp` - Check status (in Claude Code)

---

### Plugins

**Plugin Structure:**

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # Required manifest
├── skills/              # Skills with SKILL.md
├── agents/              # Agent definitions
├── hooks/
│   └── hooks.json       # Hook configs
└── .mcp.json            # MCP servers
```

**plugin.json Manifest:**

```json
{
  "name": "my-plugin",
  "description": "Plugin description",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
```

**Testing Plugins:**

```bash
claude --plugin-dir ./my-plugin
```

**Installing from Marketplace:**

```
/plugin install <plugin-name>@<marketplace>
```

---

## Workflow

### Step 1: Fetch Fresh Documentation

For the requested topic, fetch from https://code.claude.com/docs/en/<topic>:

**For memory:**

- WebFetch https://code.claude.com/docs/en/memory
- WebFetch https://code.claude.com/docs/en/best-practices

**For skills:**

- WebFetch https://code.claude.com/docs/en/skills

**For hooks:**

- WebFetch https://code.claude.com/docs/en/hooks
- WebFetch https://code.claude.com/docs/en/hooks-guide

**For agents:**

- WebFetch https://code.claude.com/docs/en/sub-agents

**For settings:**

- WebFetch https://code.claude.com/docs/en/settings

**For mcp:**

- WebFetch https://code.claude.com/docs/en/mcp

**For plugins:**

- WebFetch https://code.claude.com/docs/en/plugins
- WebFetch https://code.claude.com/docs/en/plugin-marketplaces

**For cli:**

- WebFetch https://code.claude.com/docs/en/cli-reference

**For overview:**

- WebFetch https://code.claude.com/docs/en/features-overview

### Step 2: Read Current Configuration

**For memory:**

- Read ~/.claude/CLAUDE.md
- Read ./CLAUDE.md
- Read ./CLAUDE.local.md
- Glob .claude/rules/\*.md

**For skills:**

- Glob .claude/skills/\*/SKILL.md
- Read each skill file

**For hooks:**

- Read ~/.claude/settings.json (hooks section)
- Read .claude/settings.json
- Read .claude/settings.local.json

**For agents:**

- Glob ~/.claude/agents/\*.md
- Glob .claude/agents/\*.md

**For settings:**

- Read ~/.claude/settings.json
- Read .claude/settings.json
- Read .claude/settings.local.json

**For mcp:**

- Read settings.json mcpServers section
- Read .mcp.json

**For plugins:**

- Read .claude/plugins/ directory

### Step 3: Compare & Recommend

- Identify differences from documentation best practices
- Note deprecated patterns
- Suggest improvements
- Highlight missing recommended configurations

### Step 4: Apply Updates

Ask user which recommendations to apply, then:

- Edit existing config files
- Create new config files if needed
- Validate changes

## Notes

- Documentation is fetched fresh each time for up-to-date guidance
- No changes made without user approval
- Respects existing patterns while suggesting improvements
