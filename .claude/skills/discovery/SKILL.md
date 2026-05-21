---
name: discovery
description: Phase 0 validation gate — problem framing, competitive analysis, feasibility, and a go/no-go checkpoint before committing to a feature. Use when evaluating whether an idea is worth building, before /story or /design. Trigger on "is this worth building", "validate this idea", "discovery", "should we build".
allowed-tools: Read, Write, Grep, Glob
---

# Discovery — Phase 0 Validation Gate

Structured Discovery & Validation before committing to a feature. Prevents building unvalidated ideas by gating entry into the story and design pipeline with four sequential modes.

## Usage

```
/discovery                   # Show overview of all 4 modes
/discovery problem           # Problem framing: who has it, how urgent, what evidence
/discovery competitive       # Competitive landscape: what exists, differentiators, moat
/discovery feasibility       # Feasibility: technical, economic, time constraints
/discovery checkpoint        # Go/no-go gate: 5-criteria verdict before /story create
```

## Workflow

### Step 1: Determine Mode

Parse `$ARGUMENTS` for explicit mode. If no arguments provided, show overview:

```
no args         → read templates/overview.md
problem         → read templates/problem/summary.md
competitive     → read templates/competitive/summary.md
feasibility     → read templates/feasibility/summary.md
checkpoint      → read templates/checkpoint/summary.md
<anything else> → show usage error + list valid modes + read templates/overview.md
```

### Step 2: Present Guidance (Progressive Disclosure)

**Level 1 — Summary** (default, ~20 lines):
Read and present the summary template. This is the entry point — frames the questions to answer.

**Level 2 — Patterns** (on request, ~60 lines):
When the user asks for more depth, "show me patterns", "how do I score this", or "give me examples" — read the patterns template.

**Level 3 — Full Analysis** (on request):
No template — dive into specific questions with the user based on context provided.

### Step 3: Run Modes Sequentially

Recommended sequence: `problem` → `competitive` → `feasibility` → `checkpoint`

Each mode builds on the previous:

- **problem** → frames who, what, and why
- **competitive** → validates market gap
- **feasibility** → validates buildability
- **checkpoint** → synthesizes all three into a go/no-go verdict

You can run individual modes out of order when the user has already done partial research.

### Step 4: Checkpoint Verdict

After the `checkpoint` mode:

- **Go** → "Run `/story create` to define the feature scope."
- **Conditional go** → Flag caveats, suggest mitigations, then allow forward.
- **No-go** → Explain which criteria failed, suggest what needs to change before re-evaluating.

## Template Locations

### Summary Templates (~20 lines each — L1 default)

| Mode          | File                                                          |
| ------------- | ------------------------------------------------------------- |
| overview      | `~/.claude/skills/discovery/templates/overview.md`            |
| `problem`     | `~/.claude/skills/discovery/templates/problem/summary.md`     |
| `competitive` | `~/.claude/skills/discovery/templates/competitive/summary.md` |
| `feasibility` | `~/.claude/skills/discovery/templates/feasibility/summary.md` |
| `checkpoint`  | `~/.claude/skills/discovery/templates/checkpoint/summary.md`  |

### Patterns Templates (~60 lines each — L2 on request)

| Mode          | File                                                           |
| ------------- | -------------------------------------------------------------- |
| `problem`     | `~/.claude/skills/discovery/templates/problem/patterns.md`     |
| `competitive` | `~/.claude/skills/discovery/templates/competitive/patterns.md` |
| `feasibility` | `~/.claude/skills/discovery/templates/feasibility/patterns.md` |
| `checkpoint`  | `~/.claude/skills/discovery/templates/checkpoint/patterns.md`  |

## Progressive Disclosure Rules

1. **Always start at L1** — never present all 4 modes' full patterns at once
2. **Read templates on demand** — use the Read tool; don't memorize template content
3. **User drives depth** — "show me how to score", "give me the rubric", "examples?" triggers L2
4. **Don't hard-block the user** — if they skip modes, accept partial input but flag explicitly which criteria are scored on assumptions rather than evidence
5. **Checkpoint is the exit gate** — nothing moves to `/story create` without a checkpoint verdict

## Integration

**Position in pipeline**: Phase 0 → before everything else

```
/discovery (Phase 0)
  → /story create (Phase 1 — only after checkpoint go)
    → /design (Phase 2)
      → /implementation (Phase 3)
```

**Invoked by**: User directly (`/discovery`)
**Invokes**: Nothing — produces validated problem definition consumed by `/story create`
**Connected skills**:

- `/story create` — next step after checkpoint go
- `/design` — invoked by user after `/story prp` generates a PRP; uses the validated problem scope from discovery
- `/product-assess` — deeper product assessment for complex ideas (optional, before `/discovery checkpoint`)

## Examples

**Full sequence on a new idea**:

> User: `/discovery problem` → frames who/urgency/evidence
> User: `/discovery competitive` → maps alternatives
> User: `/discovery feasibility` → checks buildability
> User: `/discovery checkpoint` → verdict: Go
> → "Great, run `/story create` to define the feature."

**Skipping straight to checkpoint**:

> User: `/discovery checkpoint`
> → Present checkpoint summary, fill criteria based on what user already knows
> → Flag any missing evidence as risks

**L2 escalation**:

> User: `/discovery problem`
> → Show problem/summary.md
> User: "show me how to score urgency"
> → Read and show problem/patterns.md (pain-point scoring section)
