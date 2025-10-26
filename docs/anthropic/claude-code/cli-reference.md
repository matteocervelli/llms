Agent Skills are now available! [Learn more about extending Claude's capabilities with Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview).
[Claude Docs home page![light logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/light.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=c877c45432515ee69194cb19e9f983a2)![dark logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/dark.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=f5bb877be0cb3cba86cf6d7c88185216)](https://docs.claude.com/)
![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)
English
Search...
⌘K
  * [Support](https://support.claude.com/)


Search...
Navigation
Reference
CLI reference
[Home](https://docs.claude.com/en/home)[Developer Guide](https://docs.claude.com/en/docs/intro)[API Reference](https://docs.claude.com/en/api/overview)[Claude Code](https://docs.claude.com/en/docs/claude-code/overview)[Model Context Protocol (MCP)](https://docs.claude.com/en/docs/mcp)[Resources](https://docs.claude.com/en/resources/overview)[Release Notes](https://docs.claude.com/en/release-notes/overview)
##### Getting started
  * [Overview](https://docs.claude.com/en/docs/claude-code/overview)
  * [Quickstart](https://docs.claude.com/en/docs/claude-code/quickstart)
  * [Common workflows](https://docs.claude.com/en/docs/claude-code/common-workflows)
  * [Claude Code on the web](https://docs.claude.com/en/docs/claude-code/claude-code-on-the-web)


##### Build with Claude Code
  * [Subagents](https://docs.claude.com/en/docs/claude-code/sub-agents)
  * [Plugins](https://docs.claude.com/en/docs/claude-code/plugins)
  * [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills)
  * [Output styles](https://docs.claude.com/en/docs/claude-code/output-styles)
  * [Hooks](https://docs.claude.com/en/docs/claude-code/hooks-guide)
  * [Headless mode](https://docs.claude.com/en/docs/claude-code/headless)
  * [GitHub Actions](https://docs.claude.com/en/docs/claude-code/github-actions)
  * [GitLab CI/CD](https://docs.claude.com/en/docs/claude-code/gitlab-ci-cd)
  * [Model Context Protocol (MCP)](https://docs.claude.com/en/docs/claude-code/mcp)
  * [Troubleshooting](https://docs.claude.com/en/docs/claude-code/troubleshooting)


##### Claude Agent SDK
  * [Migrate to Claude Agent SDK](https://docs.claude.com/en/docs/claude-code/sdk/migration-guide)


##### Deployment
  * [Overview](https://docs.claude.com/en/docs/claude-code/third-party-integrations)
  * [Amazon Bedrock](https://docs.claude.com/en/docs/claude-code/amazon-bedrock)
  * [Google Vertex AI](https://docs.claude.com/en/docs/claude-code/google-vertex-ai)
  * [Network configuration](https://docs.claude.com/en/docs/claude-code/network-config)
  * [LLM gateway](https://docs.claude.com/en/docs/claude-code/llm-gateway)
  * [Development containers](https://docs.claude.com/en/docs/claude-code/devcontainer)
  * [Sandboxing](https://docs.claude.com/en/docs/claude-code/sandboxing)


##### Administration
  * [Advanced installation](https://docs.claude.com/en/docs/claude-code/setup)
  * [Identity and Access Management](https://docs.claude.com/en/docs/claude-code/iam)
  * [Security](https://docs.claude.com/en/docs/claude-code/security)
  * [Data usage](https://docs.claude.com/en/docs/claude-code/data-usage)
  * [Monitoring](https://docs.claude.com/en/docs/claude-code/monitoring-usage)
  * [Costs](https://docs.claude.com/en/docs/claude-code/costs)
  * [Analytics](https://docs.claude.com/en/docs/claude-code/analytics)
  * [Plugin marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)


##### Configuration
  * [Settings](https://docs.claude.com/en/docs/claude-code/settings)
  * [Visual Studio Code](https://docs.claude.com/en/docs/claude-code/vs-code)
  * [JetBrains IDEs](https://docs.claude.com/en/docs/claude-code/jetbrains)
  * [Terminal configuration](https://docs.claude.com/en/docs/claude-code/terminal-config)
  * [Model configuration](https://docs.claude.com/en/docs/claude-code/model-config)
  * [Memory management](https://docs.claude.com/en/docs/claude-code/memory)
  * [Status line configuration](https://docs.claude.com/en/docs/claude-code/statusline)


##### Reference
  * [CLI reference](https://docs.claude.com/en/docs/claude-code/cli-reference)
  * [Interactive mode](https://docs.claude.com/en/docs/claude-code/interactive-mode)
  * [Slash commands](https://docs.claude.com/en/docs/claude-code/slash-commands)
  * [Checkpointing](https://docs.claude.com/en/docs/claude-code/checkpointing)
  * [Hooks reference](https://docs.claude.com/en/docs/claude-code/hooks)
  * [Plugins reference](https://docs.claude.com/en/docs/claude-code/plugins-reference)


##### Resources
  * [Legal and compliance](https://docs.claude.com/en/docs/claude-code/legal-and-compliance)


On this page
  * [CLI commands](https://docs.claude.com/en/docs/claude-code/cli-reference#cli-commands)
  * [CLI flags](https://docs.claude.com/en/docs/claude-code/cli-reference#cli-flags)
  * [Agents flag format](https://docs.claude.com/en/docs/claude-code/cli-reference#agents-flag-format)
  * [See also](https://docs.claude.com/en/docs/claude-code/cli-reference#see-also)


Reference
# CLI reference
Copy page
Complete reference for Claude Code command-line interface, including commands and flags.
Copy page
## 
[​](https://docs.claude.com/en/docs/claude-code/cli-reference#cli-commands)
CLI commands
Command | Description | Example  
---|---|---  
`claude` | Start interactive REPL | `claude`  
`claude "query"` | Start REPL with initial prompt | `claude "explain this project"`  
`claude -p "query"` | Query via SDK, then exit | `claude -p "explain this function"`  
`cat file | claude -p "query"` | Process piped content | `cat logs.txt | claude -p "explain"`  
`claude -c` | Continue most recent conversation | `claude -c`  
`claude -c -p "query"` | Continue via SDK | `claude -c -p "Check for type errors"`  
`claude -r "<session-id>" "query"` | Resume session by ID | `claude -r "abc123" "Finish this PR"`  
`claude update` | Update to latest version | `claude update`  
`claude mcp` | Configure Model Context Protocol (MCP) servers | See the [Claude Code MCP documentation](https://docs.claude.com/en/docs/claude-code/mcp).  
## 
[​](https://docs.claude.com/en/docs/claude-code/cli-reference#cli-flags)
CLI flags
Customize Claude Code’s behavior with these command-line flags: Flag | Description | Example  
---|---|---  
`--add-dir` | Add additional working directories for Claude to access (validates each path exists as a directory) | `claude --add-dir ../apps ../lib`  
`--agents` | Define custom [subagents](https://docs.claude.com/en/docs/claude-code/sub-agents) dynamically via JSON (see below for format) | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'`  
`--allowedTools` | A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](https://docs.claude.com/en/docs/claude-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Read"`  
`--disallowedTools` | A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](https://docs.claude.com/en/docs/claude-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`  
`--print`, `-p` | Print response without interactive mode (see [SDK documentation](https://docs.claude.com/en/docs/claude-code/sdk) for programmatic usage details) | `claude -p "query"`  
`--append-system-prompt` | Append to system prompt (only with `--print`) | `claude --append-system-prompt "Custom instruction"`  
`--output-format` | Specify output format for print mode (options: `text`, `json`, `stream-json`) | `claude -p "query" --output-format json`  
`--input-format` | Specify input format for print mode (options: `text`, `stream-json`) | `claude -p --output-format json --input-format stream-json`  
`--include-partial-messages` | Include partial streaming events in output (requires `--print` and `--output-format=stream-json`) | `claude -p --output-format stream-json --include-partial-messages "query"`  
`--verbose` | Enable verbose logging, shows full turn-by-turn output (helpful for debugging in both print and interactive modes) | `claude --verbose`  
`--max-turns` | Limit the number of agentic turns in non-interactive mode | `claude -p --max-turns 3 "query"`  
`--model` | Sets the model for the current session with an alias for the latest model (`sonnet` or `opus`) or a model’s full name | `claude --model claude-sonnet-4-5-20250929`  
`--permission-mode` | Begin in a specified [permission mode](https://docs.claude.com/en/docs/claude-code/iam#permission-modes) | `claude --permission-mode plan`  
`--permission-prompt-tool` | Specify an MCP tool to handle permission prompts in non-interactive mode | `claude -p --permission-prompt-tool mcp_auth_tool "query"`  
`--resume` | Resume a specific session by ID, or by choosing in interactive mode | `claude --resume abc123 "query"`  
`--continue` | Load the most recent conversation in the current directory | `claude --continue`  
`--dangerously-skip-permissions` | Skip permission prompts (use with caution) | `claude --dangerously-skip-permissions`  
The `--output-format json` flag is particularly useful for scripting and automation, allowing you to parse Claude’s responses programmatically.
### 
[​](https://docs.claude.com/en/docs/claude-code/cli-reference#agents-flag-format)
Agents flag format
The `--agents` flag accepts a JSON object that defines one or more custom subagents. Each subagent requires a unique name (as the key) and a definition object with the following fields: Field | Required | Description  
---|---|---  
`description` | Yes | Natural language description of when the subagent should be invoked  
`prompt` | Yes | The system prompt that guides the subagent’s behavior  
`tools` | No | Array of specific tools the subagent can use (e.g., `["Read", "Edit", "Bash"]`). If omitted, inherits all tools  
`model` | No | Model alias to use: `sonnet`, `opus`, or `haiku`. If omitted, uses the default subagent model  
Example:
Copy
```
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'

```

For more details on creating and using subagents, see the [subagents documentation](https://docs.claude.com/en/docs/claude-code/sub-agents). For detailed information about print mode (`-p`) including output formats, streaming, verbose logging, and programmatic usage, see the [SDK documentation](https://docs.claude.com/en/docs/claude-code/sdk).
## 
[​](https://docs.claude.com/en/docs/claude-code/cli-reference#see-also)
See also
  * [Interactive mode](https://docs.claude.com/en/docs/claude-code/interactive-mode) - Shortcuts, input modes, and interactive features
  * [Slash commands](https://docs.claude.com/en/docs/claude-code/slash-commands) - Interactive session commands
  * [Quickstart guide](https://docs.claude.com/en/docs/claude-code/quickstart) - Getting started with Claude Code
  * [Common workflows](https://docs.claude.com/en/docs/claude-code/common-workflows) - Advanced workflows and patterns
  * [Settings](https://docs.claude.com/en/docs/claude-code/settings) - Configuration options
  * [SDK documentation](https://docs.claude.com/en/docs/claude-code/sdk) - Programmatic usage and integrations


Was this page helpful?
YesNo
[Status line configuration](https://docs.claude.com/en/docs/claude-code/statusline)[Interactive mode](https://docs.claude.com/en/docs/claude-code/interactive-mode)
Assistant
Responses are generated using AI and may contain mistakes.
[Claude Docs home page![light logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/light.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=c877c45432515ee69194cb19e9f983a2)![dark logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/dark.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=f5bb877be0cb3cba86cf6d7c88185216)](https://docs.claude.com/)
Company
Help and security
[Support center](https://support.claude.com/)
Learn
[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)
Terms and policies
