---
name: design
description: Design component architecture, REST API contracts, and data models (Pydantic schemas) before implementation. Use when planning how to build a feature, defining endpoints, or modeling data. Trigger on "design the architecture", "design the API", "data model", "how should I structure this feature".
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Design — Architecture, API & Data Models

Unified design guidance for feature implementation. Auto-detects context from project files or accepts explicit mode.

## Usage

```
/design                    # Auto-detect from project, show summary
/design architecture       # Component architecture, SOLID, patterns
/design api                # REST API design, auth, rate limiting
/design data               # Pydantic schemas, validators, relationships
/design full               # All three in sequence (architecture → data → API)
```

## Workflow

### Step 1: Determine Mode

Parse `$ARGUMENTS` for explicit mode. If no arguments provided, detect context:

```bash
DETECTED=$(bash "$HOME/.claude/skills/design/lib/design-detector.sh")
```

Map detection results to recommended mode:

- `pydantic,fastapi` → suggest `api` + `data`
- `pydantic` only → suggest `data`
- `fastapi` or `flask` or `django` → suggest `api`
- Generic Python/Node → suggest `architecture`
- Unknown → show all summaries, let user choose

### Step 2: Show Relevant Guidance

Based on detected or explicit mode, use **progressive disclosure**:

**Level 1 — Summary** (default, ~15 lines):
Read and present the summary template for the chosen domain:

- `templates/architecture/summary.md`
- `templates/api/summary.md`
- `templates/data/summary.md`

**Level 2 — Patterns** (on request for more detail, ~50 lines):
Read the patterns template with decision guidance and examples:

- `templates/architecture/patterns.md`
- `templates/api/patterns.md`
- `templates/data/patterns.md`

**Level 3 — Full Reference** (on request for complete SOP):
Read the deep reference documents on demand:

- `reference/architecture-patterns.md` + `reference/component-design-guide.md`
- `reference/api-design-guide.md` + `reference/function-design-patterns.md`
- `reference/data-model-guide.md` + `reference/pydantic-patterns.md`

### Step 3: Handle Multiple Domains

If context suggests multiple domains (e.g., new feature with API + data):

- Show summary for each detected domain
- Let user choose which to dive deeper into
- Or use `/design full` for the complete sequence

### Step 4: No Context Detected

If detection returns "unknown" and no explicit mode:

- Show all three summaries as overview
- List available modes for user to choose

## `/design full` Sequence

When running the full design workflow:

1. **Architecture first**: Component boundaries, layers, patterns, DI
2. **Data models second**: Pydantic schemas based on architecture components
3. **API contracts third**: Endpoints and schemas using data models

Output uses `templates/architecture-doc.md` as the final document template.

## Output

Write documents to `docs/architecture/` in the project root:

| Subcommand             | Output Path                                   |
| ---------------------- | --------------------------------------------- |
| `/design architecture` | `docs/architecture/architecture-{feature}.md` |
| `/design api`          | `docs/architecture/api-{feature}.md`          |
| `/design data`         | `docs/architecture/data-{feature}.md`         |
| `/design full`         | `docs/architecture/{feature}.md` (combined)   |

Use `templates/architecture-doc.md` as the document template with sections:

- Overview, Architecture Pattern, Component Design, Data Model, API Specification
- Data Flows, Module Structure, Error Handling, Configuration
- Testing Strategy, Security Considerations, Performance Considerations

Create `docs/architecture/` if it doesn't exist.

## Integration

**Invoked by**: User directly (`/design`), `/story prp` workflow (design phase)
**Invokes**: Nothing directly — produces architecture docs consumed by `prp-generator`
**Connected skills**:

- `/story create` → requirements → `/design` → architecture doc → `/story prp` → PRP
- `/implementation` consumes design output

## Progressive Disclosure Rules

- **Never** load reference/ docs unless user explicitly asks for full SOP or L3 detail
- **Default** to L1 summary — enough to orient and decide
- **L2 patterns** when user asks "how", "what pattern", "show me examples"
- **L3 full** when user asks for "complete guide", "full reference", or specific deep topic
