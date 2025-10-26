Agent Skills are now available! [Learn more about extending Claude's capabilities with Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview).
[Claude Docs home page![light logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/light.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=c877c45432515ee69194cb19e9f983a2)![dark logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/dark.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=f5bb877be0cb3cba86cf6d7c88185216)](https://docs.claude.com/)
![US](https://d3gk2c5xim1je2.cloudfront.net/flags/US.svg)
English
Search...
⌘K
  * [Support](https://support.claude.com/)


Search...
Navigation
Configuration
Manage Claude's memory
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
  * [Determine memory type](https://docs.claude.com/en/docs/claude-code/memory#determine-memory-type)
  * [CLAUDE.md imports](https://docs.claude.com/en/docs/claude-code/memory#claude-md-imports)
  * [How Claude looks up memories](https://docs.claude.com/en/docs/claude-code/memory#how-claude-looks-up-memories)
  * [Quickly add memories with the # shortcut](https://docs.claude.com/en/docs/claude-code/memory#quickly-add-memories-with-the-%23-shortcut)
  * [Directly edit memories with /memory](https://docs.claude.com/en/docs/claude-code/memory#directly-edit-memories-with-%2Fmemory)
  * [Set up project memory](https://docs.claude.com/en/docs/claude-code/memory#set-up-project-memory)
  * [Organization-level memory management](https://docs.claude.com/en/docs/claude-code/memory#organization-level-memory-management)
  * [Memory best practices](https://docs.claude.com/en/docs/claude-code/memory#memory-best-practices)


Configuration
# Manage Claude's memory
Copy page
Learn how to manage Claude Code’s memory across sessions with different memory locations and best practices.
Copy page
Claude Code can remember your preferences across sessions, like style guidelines and common commands in your workflow.
## 
[​](https://docs.claude.com/en/docs/claude-code/memory#determine-memory-type)
Determine memory type
Claude Code offers four memory locations in a hierarchical structure, each serving a different purpose: Memory Type | Location | Purpose | Use Case Examples | Shared With  
---|---|---|---|---  
**Enterprise policy** | macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`  
Linux: `/etc/claude-code/CLAUDE.md`  
Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md` | Organization-wide instructions managed by IT/DevOps | Company coding standards, security policies, compliance requirements | All users in organization  
**Project memory** |  `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared instructions for the project | Project architecture, coding standards, common workflows | Team members via source control  
**User memory** | `~/.claude/CLAUDE.md` | Personal preferences for all projects | Code styling preferences, personal tooling shortcuts | Just you (all projects)  
**Project memory (local)** | `./CLAUDE.local.md` | Personal project-specific preferences |  _(Deprecated, see below)_ Your sandbox URLs, preferred test data | Just you (current project)  
All memory files are automatically loaded into Claude Code’s context when launched. Files higher in the hierarchy take precedence and are loaded first, providing a foundation that more specific memories build upon.
## 
[​](https://docs.claude.com/en/docs/claude-code/memory#claude-md-imports)
CLAUDE.md imports
CLAUDE.md files can import additional files using `@path/to/import` syntax. The following example imports 3 files:
Copy
```
See @README for project overview and @package.json for available npm commands for this project.
# Additional Instructions
- git workflow @docs/git-instructions.md

```

Both relative and absolute paths are allowed. In particular, importing files in user’s home dir is a convenient way for your team members to provide individual instructions that are not checked into the repository. Previously CLAUDE.local.md served a similar purpose, but is now deprecated in favor of imports since they work better across multiple git worktrees.
Copy
```
# Individual Preferences
- @~/.claude/my-project-instructions.md

```

To avoid potential collisions, imports are not evaluated inside markdown code spans and code blocks.
Copy
```
This code span will not be treated as an import: `@anthropic-ai/claude-code`

```

Imported files can recursively import additional files, with a max-depth of 5 hops. You can see what memory files are loaded by running `/memory` command.
## 
[​](https://docs.claude.com/en/docs/claude-code/memory#how-claude-looks-up-memories)
How Claude looks up memories
Claude Code reads memories recursively: starting in the cwd, Claude Code recurses up to (but not including) the root directory _/_ and reads any CLAUDE.md or CLAUDE.local.md files it finds. This is especially convenient when working in large repositories where you run Claude Code in _foo/bar/_ , and have memories in both _foo/CLAUDE.md_ and _foo/bar/CLAUDE.md_. Claude will also discover CLAUDE.md nested in subtrees under your current working directory. Instead of loading them at launch, they are only included when Claude reads files in those subtrees.
## 
[​](https://docs.claude.com/en/docs/claude-code/memory#quickly-add-memories-with-the-%23-shortcut)
Quickly add memories with the `#` shortcut
The fastest way to add a memory is to start your input with the `#` character:
Copy
```
# Always use descriptive variable names

```

You’ll be prompted to select which memory file to store this in.
## 
[​](https://docs.claude.com/en/docs/claude-code/memory#directly-edit-memories-with-%2Fmemory)
Directly edit memories with `/memory`
Use the `/memory` slash command during a session to open any memory file in your system editor for more extensive additions or organization.
## 
[​](https://docs.claude.com/en/docs/claude-code/memory#set-up-project-memory)
Set up project memory
Suppose you want to set up a CLAUDE.md file to store important project information, conventions, and frequently used commands. Project memory can be stored in either `./CLAUDE.md` or `./.claude/CLAUDE.md`. Bootstrap a CLAUDE.md for your codebase with the following command:
Copy
```
> /init 

```

Tips:
  * Include frequently used commands (build, test, lint) to avoid repeated searches
  * Document code style preferences and naming conventions
  * Add important architectural patterns specific to your project
  * CLAUDE.md memories can be used for both instructions shared with your team and for your individual preferences.


## 
[​](https://docs.claude.com/en/docs/claude-code/memory#organization-level-memory-management)
Organization-level memory management
Enterprise organizations can deploy centrally managed CLAUDE.md files that apply to all users. To set up organization-level memory management:
  1. Create the enterprise memory file in the appropriate location for your operating system:


  * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
  * Linux/WSL: `/etc/claude-code/CLAUDE.md`
  * Windows: `C:\ProgramData\ClaudeCode\CLAUDE.md`


  1. Deploy via your configuration management system (MDM, Group Policy, Ansible, etc.) to ensure consistent distribution across all developer machines.


## 
[​](https://docs.claude.com/en/docs/claude-code/memory#memory-best-practices)
Memory best practices
  * **Be specific** : “Use 2-space indentation” is better than “Format code properly”.
  * **Use structure to organize** : Format each individual memory as a bullet point and group related memories under descriptive markdown headings.
  * **Review periodically** : Update memories as your project evolves to ensure Claude is always using the most up to date information and context.


Was this page helpful?
YesNo
[Model configuration](https://docs.claude.com/en/docs/claude-code/model-config)[Status line configuration](https://docs.claude.com/en/docs/claude-code/statusline)
Assistant
Responses are generated using AI and may contain mistakes.
[Claude Docs home page![light logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/light.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=c877c45432515ee69194cb19e9f983a2)![dark logo](https://mintcdn.com/anthropic-claude-docs/DcI2Ybid7ZEnFaf0/logo/dark.svg?fit=max&auto=format&n=DcI2Ybid7ZEnFaf0&q=85&s=f5bb877be0cb3cba86cf6d7c88185216)](https://docs.claude.com/)
Company
Help and security
[Support center](https://support.claude.com/)
Learn
[MCP connectors](https://claude.com/partners/mcp)[Customer stories](https://www.claude.com/customers)[Powered by Claude](https://claude.com/partners/powered-by-claude)[Service partners](https://claude.com/partners/services)[Startups program](https://claude.com/programs/startups)
Terms and policies
