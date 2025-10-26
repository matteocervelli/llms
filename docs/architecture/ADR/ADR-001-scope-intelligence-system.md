# ADR-001: Scope Intelligence System

**Status:** Accepted
**Date:** 2025-10-26
**Authors:** Matteo Cervelli
**Issue:** [#2](https://github.com/matteocervelli/llms/issues/2)

## Context

The LLM Configuration Management System needs to support multiple levels of configuration to accommodate different use cases:

1. **User-wide settings** that apply across all projects
2. **Project-specific settings** shared with the team
3. **Local overrides** not committed to version control

Claude Code already uses a `.claude/` directory structure, but lacks intelligent scope detection and precedence handling. Other tools (like Git, npm, ESLint) successfully implement hierarchical configuration systems that serve as proven patterns.

## Decision

We will implement a **three-tier scope intelligence system** with automatic detection and configuration precedence:

### Scope Tiers

1. **Global Scope** (`~/.claude/`)
   - User-wide, applies to all projects
   - Precedence: 3 (lowest)
   - Always available

2. **Project Scope** (`.claude/`)
   - Project-specific, team-shared
   - Precedence: 2 (medium)
   - Committed to version control

3. **Local Scope** (`.claude/settings.local.json`)
   - Project-local, not committed
   - Precedence: 1 (highest)
   - Gitignored

### Configuration Precedence

**Local > Project > Global**

Higher precedence scopes override lower precedence scopes, similar to CSS cascading or Git config hierarchy.

### Auto-Detection Logic

```
1. Check for Local scope (.claude/settings.local.json in project)
2. Check for Project scope (.claude/ in current or parent dirs)
3. Default to Global scope (~/.claude/)
```

### CLI Flag Support

Tools can accept explicit scope flags to override auto-detection:

- `--global`: Force global scope
- `--project`: Force project scope
- `--local`: Force local scope

## Rationale

### Why Three Tiers?

**Global Scope:**
- Needed for: User preferences, default templates, personal settings
- Example: Personal API keys, default editor preferences

**Project Scope:**
- Needed for: Team-shared configuration, project-specific skills/commands
- Example: Project agents, team workflows, project templates

**Local Scope:**
- Needed for: Developer-specific overrides, machine-specific config
- Example: Local API keys, development-only settings, personal aliases

### Why This Precedence Order?

**Local > Project > Global** follows the principle of **specificity over generality**:

- Local settings are most specific (this machine, this project)
- Project settings are medium specific (this project, all machines)
- Global settings are least specific (all projects, all machines)

This matches user expectations from other tools (Git, npm, etc.).

### Why Auto-Detection?

Auto-detection reduces cognitive load:
- Users don't need to specify scope for every command
- System intelligently chooses the most appropriate scope
- CLI flags available for explicit control when needed

## Implementation Details

### Core Components

1. **`ScopeType` Enum:** GLOBAL, PROJECT, LOCAL
2. **`ScopeConfig` Dataclass:** path, type, precedence, exists
3. **`ScopeManager` Class:** Detection, resolution, validation
4. **Custom Exceptions:** ScopeError, ScopeNotFoundError, InvalidScopeError, MultipleScopeFlagsError

### Project Root Detection

The system searches for project markers to identify project boundaries:
- `.git` directory (standard Git repository marker)
- `.claude` directory (Claude Code project marker)

This allows the system to work in both Git and non-Git projects.

### Security Considerations

1. **Path Traversal Prevention:**
   - All paths resolved using `Path.resolve()`
   - Validates paths stay within expected boundaries
   - Rejects malicious symlinks

2. **Sensitive Data Protection:**
   - Local scope designed for secrets (not committed)
   - Clear documentation on scope security implications
   - Warning system for sensitive data in committed scopes

3. **Input Validation:**
   - CLI flags validated against whitelist
   - Mutually exclusive flags enforced
   - Path sanitization for user inputs

### Performance Optimizations

1. **Caching:** Scope detection results cached with `@lru_cache`
2. **Lazy Loading:** Configs only loaded when needed
3. **Efficient Traversal:** Directory search stops at first project marker
4. **Target Performance:** < 10ms for scope detection

## Alternatives Considered

### Alternative 1: Two-Tier System (Global + Project)

**Pros:**
- Simpler implementation
- Fewer edge cases
- Easier to understand

**Cons:**
- No way to override project settings locally
- Developers forced to modify committed config for personal preferences
- Cannot handle machine-specific configuration

**Decision:** Rejected - Local scope is essential for developer productivity

### Alternative 2: Four-Tier System (Global + Org + Project + Local)

**Pros:**
- Organization-wide settings possible
- More granular control
- Supports enterprise use cases

**Cons:**
- Significantly more complex
- Unclear precedence rules
- Over-engineering for current use case

**Decision:** Rejected - Can be added later if needed (YAGNI principle)

### Alternative 3: Environment Variables Only

**Pros:**
- Standard approach
- Works everywhere
- No file management needed

**Cons:**
- Not discoverable
- Difficult to manage many settings
- No hierarchical organization
- Poor developer experience

**Decision:** Rejected - Files provide better organization and discoverability

### Alternative 4: Single Config with Profiles

**Pros:**
- Single source of truth
- Profile-based switching
- Familiar pattern (AWS profiles, etc.)

**Cons:**
- All settings in one file (large files)
- Profiles must be predefined
- Less flexible than hierarchical scopes
- Team config mixed with personal config

**Decision:** Rejected - Hierarchical scopes provide better separation

## Consequences

### Positive

1. **Developer Productivity:** Auto-detection reduces friction
2. **Team Collaboration:** Project scope enables shared configuration
3. **Security:** Local scope keeps secrets out of version control
4. **Flexibility:** CLI flags provide explicit control when needed
5. **Familiar Pattern:** Similar to Git config, npm config, etc.
6. **Future-Proof:** Extensible to multi-LLM support

### Negative

1. **Complexity:** Three scopes add mental overhead
2. **Documentation Burden:** Must explain scope system clearly
3. **Testing Overhead:** More edge cases to test
4. **Potential Confusion:** Users might not understand precedence

### Mitigation Strategies

1. **Comprehensive Documentation:** README, examples, API docs
2. **Clear Error Messages:** Explain scope issues with helpful hints
3. **Validation Tools:** Help users verify scope configuration
4. **Sensible Defaults:** Auto-detection handles 90% of cases

## Migration Strategy

### For New Users

No migration needed - system designed from scratch.

### For Existing Claude Code Users

If users already have `.claude/` directories:

1. Existing `.claude/` detected as Project scope automatically
2. No breaking changes to existing setups
3. Local scope opt-in (create `settings.local.json` if needed)
4. Global scope created on first use of global-scoped tools

## Future Considerations

### Multi-LLM Support

The scope system is designed to extend to other LLMs:

```
~/.llm/
  ├── .claude/    # Claude Code config
  ├── .codex/     # Codex config
  └── .opencode/  # OpenCode config
```

Current implementation uses `.claude/` but architecture supports future LLM directories.

### Configuration Merging

Future enhancement: Merge configurations across scopes with precedence:

```python
# Merge all scopes into single config
config = manager.merge_configs()
# { ...global, ...project, ...local }
```

### Encrypted Settings

Future enhancement: Support encrypted settings in Local scope:

```
.claude/settings.local.json.encrypted
```

### Remote Scope Sync

Future enhancement: Sync global scope across machines:

```
~/.claude/sync/
```

## References

- [Git Config](https://git-scm.com/docs/git-config) - Three-tier config hierarchy
- [npm Config](https://docs.npmjs.com/cli/v8/using-npm/config) - Cascading configuration
- [ESLint Config](https://eslint.org/docs/user-guide/configuring/) - Hierarchical configuration
- [Keep a Changelog](https://keepachangelog.com/) - Changelog format
- [Semantic Versioning](https://semver.org/) - Version numbering

## Approval

**Approved by:** Matteo Cervelli
**Date:** 2025-10-26
**Implementation Status:** Complete (Sprint 1, Issue #2)

---

## Revision History

- **2025-10-26:** Initial version (v1.0)
