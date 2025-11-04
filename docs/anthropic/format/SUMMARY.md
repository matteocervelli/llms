# YAML Format Validation - Summary

**Date**: 2025-11-04

## What We Did

### 1. Created Format Guides

Created concise, official documentation-based guides in `docs/anthropic/format/`:

- **agents.md** - Sub-agents YAML format specification
- **skills.md** - Skills YAML format specification
- **commands.md** - Slash commands YAML format specification
- **hooks.md** - Hooks JSON configuration (not YAML)
- **prompts.md** - Status (not a supported element type)

### 2. Analyzed Undocumented Directives

**Assessment Results** (`ASSESSMENT.md`):

- **Agents**: Found `color` field (cyan, green, purple, red, yellow)
  - Used in 7/15 agent files
  - **Decision**: APPROVED - Valid but undocumented field for distinguishing agents
  - **Action**: Added to validator schema

- **Skills**: Found 3 files with malformed YAML frontmatter
  - Missing newline before closing `---` delimiter
  - **Action**: Fixed all 3 files

- **Commands**: All using only documented fields ✅

### 3. Updated Validator

**Changes to `src/tools/element_validator/`**:

1. **Added `color` field support** (`schemas.py`):
   - Added to `AgentSchema.OPTIONAL_FIELDS`
   - Pattern: `^(cyan|green|purple|red|yellow)$`

2. **Removed PROMPT element type** (not supported in Claude Code):
   - Removed from `ElementType` enum
   - Removed `PromptSchema` class
   - Updated imports in `validator.py`

3. **Improved file filtering** (`validator.py`):
   - Only validate files in `/agents/`, `/skills/`, `/commands/` directories
   - For skills, only validate `SKILL.md` files
   - Skip README, LICENSE, CHANGELOG, etc.

### 4. Fixed Malformed Files

**Fixed 3 skill files**:
- `.claude/skills/permission-test-skill/SKILL.md`
- `.claude/skills/whitelist-bypass-skill/SKILL.md`
- `.claude/skills/file-permission-test/SKILL.md`

**Issue**: Missing newline before `---` closing delimiter
**Fix**: Added proper line break

### 5. Validation Results

**Project (.claude/)**:
- 72 files validated
- ✅ 72 valid (100%)
- ❌ 0 invalid

**Global (~/.claude/)**:
- 77 files validated
- ✅ 76 valid (98.7%)
- ❌ 1 invalid (issue.md - missing frontmatter)
- ⚠️ 2 warnings (catalog commands with `arguments` field)

## Validation Workflow

Use these make commands:

```bash
make validate           # Validate all elements
make validate-fix       # Auto-fix validation errors
make catalog-sync       # Regenerate catalog manifests
make validate-and-sync  # Complete workflow (validate → fix → catalog)
```

## Supported YAML Directives

### Agents (Sub-agents)

**Required**:
- `name` - Lowercase letters, numbers, hyphens
- `description` - Natural language description

**Optional**:
- `tools` - Comma-separated tool names
- `model` - sonnet | opus | haiku | inherit
- `color` - cyan | green | purple | red | yellow (undocumented)

### Skills

**Required**:
- `name` - Lowercase letters, numbers, hyphens (max 64 chars)
- `description` - Max 1024 characters

**Optional**:
- `allowed-tools` - Comma-separated tool names

### Commands

**All Optional**:
- `description` - Brief description
- `allowed-tools` - Comma-separated tool names
- `argument-hint` - Expected arguments
- `model` - sonnet | opus | haiku
- `disable-model-invocation` - Boolean

## Files Changed

### Created
- `docs/anthropic/format/agents.md`
- `docs/anthropic/format/skills.md`
- `docs/anthropic/format/commands.md`
- `docs/anthropic/format/hooks.md`
- `docs/anthropic/format/prompts.md`
- `docs/anthropic/format/ASSESSMENT.md`
- `docs/anthropic/format/SUMMARY.md` (this file)

### Modified
- `src/tools/element_validator/schemas.py`
  - Added `color` field to AgentSchema
  - Removed PromptSchema and ElementType.PROMPT

- `src/tools/element_validator/validator.py`
  - Removed PromptSchema import
  - Removed ElementType.PROMPT detection
  - Improved file filtering to skip non-element files
  - Added logic to only validate SKILL.md in skills directories

- `.claude/skills/permission-test-skill/SKILL.md`
- `.claude/skills/whitelist-bypass-skill/SKILL.md`
- `.claude/skills/file-permission-test/SKILL.md`

## Next Steps

1. ✅ All validation passing for project elements
2. ⏳ Fix global `issue.md` command (missing frontmatter)
3. ⏳ Review warnings for `arguments` field in catalog commands
4. ✅ Documentation complete and up-to-date

## Official Documentation References

- **Sub-agents**: https://docs.claude.com/en/docs/claude-code/sub-agents
- **Skills**: https://docs.claude.com/en/docs/claude-code/skills
- **Commands**: https://docs.claude.com/en/docs/claude-code/slash-commands
- **Hooks**: https://docs.claude.com/en/docs/claude-code/hooks
