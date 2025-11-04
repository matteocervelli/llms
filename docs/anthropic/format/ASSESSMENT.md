# YAML Directives Usage Assessment

## Summary

Analysis of YAML frontmatter directives used across our Claude Code elements compared to official documentation.

**Analysis Date**: 2025-11-04
**Files Analyzed**: 112 total (15 agents, 84 skills, 13 commands)

---

## AGENTS (Sub-agents)

### Officially Documented Fields

| Field | Usage | Status |
|-------|-------|--------|
| `name` | 15/15 files (100%) | ✅ Required - all files compliant |
| `description` | 15/15 files (100%) | ✅ Required - all files compliant |
| `tools` | 13/15 files (87%) | ✅ Optional - properly used |
| `model` | 13/15 files (87%) | ✅ Optional - properly used |

### Undocumented Fields

| Field | Usage | Colors Used | Recommendation |
|-------|-------|-------------|----------------|
| `color` | 7/15 files (47%) | cyan, green, purple, red, yellow | **KEEP** - You confirmed this is valid for distinguishing agents |

**Files using `color`**:
- code-quality-specialist.md
- deployment-specialist.md
- e2e-accessibility-specialist.md
- integration-test-specialist.md
- security-specialist.md
- test-runner-specialist.md
- unit-test-specialist.md

**Decision Needed**: ✅ Already confirmed - `color` is valid but undocumented

---

## SKILLS

### Officially Documented Fields

| Field | Usage | Status |
|-------|-------|--------|
| `name` | 84/84 files (100%) | ✅ Required - all files compliant |
| `description` | 84/84 files (100%) | ✅ Required - all files compliant |
| `allowed-tools` | 39/84 files (46%) | ✅ Optional - properly used |

### Undocumented Fields

⚠️ **Parsing Issues Detected**

The following "fields" appear to be markdown content mistakenly detected as YAML:
- `- **Issue 1**:` (2 files)
- `- **Issue 2**:` (2 files)
- `- **Operation failed**:` (1 file)
- `- **Permission denied**:` (1 file)
- `- **Tool not available**:` (1 file)
- `Common issues and solutions:` (2 files)
- `Common tool-related errors and solutions:` (1 file)
- `List related skills that might be useful:` (2 files)
- `Provide examples of when this skill should be used:` (3 files)

**Decision Needed**:
- ❓ **Investigate**: Some skill files may have malformed YAML frontmatter (content bleeding into frontmatter)
- ❓ **Action**: Identify and fix files with improperly closed frontmatter delimiters

---

## COMMANDS (Slash Commands)

### Officially Documented Fields

| Field | Usage | Status |
|-------|-------|--------|
| `description` | 11/13 files (85%) | ✅ Optional - recommended for tool access |
| `allowed-tools` | 7/13 files (54%) | ✅ Optional - properly used |
| `argument-hint` | 6/13 files (46%) | ✅ Optional - properly used |
| `model` | 0/13 files (0%) | ⚠️ Optional - not currently used |
| `disable-model-invocation` | 0/13 files (0%) | ⚠️ Optional - not currently used |

### Undocumented Fields

None detected.

**Decision Needed**: None - all commands use only documented fields.

---

## Recommendations

### 1. Agent `color` Field ✅
**Status**: Keep
**Reason**: User confirmed this is a valid undocumented field for distinguishing agents
**Action**: Update validator to allow `color` field for agents

### 2. Skills YAML Parsing Issues ❌
**Status**: Fix required
**Reason**: Content appearing as YAML fields indicates malformed frontmatter
**Action**:
1. Identify skill files with parsing issues
2. Verify frontmatter closing delimiter (`---`) is present
3. Fix files with content bleeding into YAML section

### 3. Command Fields
**Status**: No action needed
**Reason**: All commands use only documented fields
**Action**: None

---

## Validator Updates Required

### Current Behavior
The validator warns about unknown fields, causing validation errors for the `color` field.

### Recommended Changes

1. **Add `color` to agent schema as optional**:
   ```python
   # In schemas.py - AgentSchema
   OPTIONAL_FIELDS = [
       FieldSchema(name="tools", required=False, field_type=str),
       FieldSchema(name="model", required=False, field_type=str, pattern=r"^(sonnet|opus|haiku|inherit)$"),
       FieldSchema(name="color", required=False, field_type=str, pattern=r"^(cyan|green|purple|red|yellow)$"),
   ]
   ```

2. **Remove warning for unknown fields** (or make it configurable):
   ```python
   # In validator.py - remove or make optional
   # Lines 330-335 that add warnings for unknown fields
   ```

3. **Fix skills with malformed frontmatter**:
   - Run validator to identify files
   - Manually inspect and fix YAML delimiters
   - Re-validate

---

## Next Steps

1. ✅ User decision on `color` field → **APPROVED**
2. ⏳ Identify skill files with YAML parsing issues
3. ⏳ Update validator to accept `color` field
4. ⏳ Fix malformed skill files
5. ⏳ Re-run validation workflow

---

## Official Documentation References

- **Agents**: https://docs.claude.com/en/docs/claude-code/sub-agents
- **Skills**: https://docs.claude.com/en/docs/claude-code/skills
- **Commands**: https://docs.claude.com/en/docs/claude-code/slash-commands
- **Hooks**: https://docs.claude.com/en/docs/claude-code/hooks
