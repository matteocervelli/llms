---
name: story
description: Turn a feature idea into INVEST-compliant user stories, epics, PRPs/PRDs, and sprint plans. Use when breaking down a feature for implementation or planning a sprint. Trigger on "write user stories", "break this into stories", "create a PRP", "plan the sprint", "story".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
---

# Story Pipeline — Planning, Generation & Sprint Management

Unified workflow from feature idea to ready-to-implement stories. Replaces user-story-generator, story-validator, sprint-planner, and technical-annotator.

> **TDD note:** Do NOT use `/story tests`. Use `/implementation` directly — it has TDD built-in
> and generates tests from acceptance criteria with full codebase context. `/story tests` is
> archived: it produces generic stubs that conflict with implementation-generated tests.

## Usage

```
/story                          # Auto-detect project, suggest next action
/story create                   # Feature description -> INVEST-compliant user stories
/story create --epic            # Feature too large for stories -> create EP-XXXX epic
/story create --prd             # Feature description -> PRD (aggregated stories)
/story decompose <EP-XXXX>      # Decompose an epic into child US-XXXX stories
/story prp <story-ids>          # Generate PRP from stories (invokes /prp-generator)
/story plan                     # Sprint/milestone planning from backlog
/story update                   # Create new stories from change request
/story sync                     # Push stories/epics to GitHub issues via gh CLI
```

## Language

**Always write in English.** All story/epic YAML content, GitHub issue titles and bodies, acceptance criteria, and documentation must be in English. No exceptions — do not detect or adapt to project language.

## Epic vs Story — quando usare quale

| Usa `--epic` quando...                        | Usa `create` (storia) quando...          |
| --------------------------------------------- | ---------------------------------------- |
| La feature richiede >3 storie figlie          | La feature si implementa in 1-2 sessioni |
| Stima > 8 story points                        | Stima ≤ 8 story points                   |
| Coinvolge nuovo modello dati + UI + notifiche | Tocca un'area già strutturata            |
| È un deliverable di bando o milestone         | È un task di refinement                  |

**Regola pratica:** se mentre scrivi le acceptance criteria ti vengono 6+ punti, è un'epica.

## Workflow

### Step 1: Determine Mode

Parse `$ARGUMENTS` for explicit subcommand. If no arguments, detect project context:

```bash
PROJECT_INFO=$(bash "$HOME/.claude/skills/story/lib/project-detector.sh")
```

With no arguments:

- If project has story YAML files -> show backlog summary, suggest validate/plan/implementation
- If project has PRPs but no stories -> suggest `/story create` for next PRP
- If new project -> suggest `/story create` to start

### Step 2: Route to Subcommand

---

## Subcommand: `create`

Interactive feature-to-stories workflow.

### Phase 0: Epic check (NUOVO)

**Prima di generare storie**, valuta se la feature è troppo grande:

- Stimi >8 punti totali? → `--epic` obbligatorio
- Richiede >3 sotto-funzionalità distinte? → `--epic` obbligatorio
- Nuovo modello dati + UI + notifiche + auth? → quasi certamente `--epic`

Se l'utente non ha passato `--epic` ma la feature lo richiede, **proponi di creare un'epica invece**. Non generare storie impossibili da stimare.

### Phase 1: Feature Extraction

Ask the user these questions in English. Skip if answers are obvious from context.

1. **What** does this feature do? (one sentence)
2. **Who** benefits? (persona: operator, fatturatore, client-pmi, employee-pmi, admin…)
3. **Why** does it matter? (business value, pain it resolves)
4. **What** does success look like? (measurable outcome)
5. **What** constraints exist? (technical, time, dependencies on existing system)

Always add: **Current system state (AS-IS)** — what already exists, what is missing. Without this, context is insufficient for implementation.

### Phase 1b: Epic Mode (`--epic`)

Quando `--epic` è passato, genera un'epica EP-XXXX invece di storie:

- Leggi `templates/epic-yaml.md` per lo schema
- Incrementa `.epic_counter` (separato da `.story_counter`)
- Compila obbligatoriamente: `context`, `problem`, `personas`, `goal`, `success_metrics`, `current_state`, `sub_stories`, `technical_dependencies`
- Il campo `sub_stories` è una lista di titoli delle storie figlie — verranno create da `/story decompose`
- File: `stories/yaml-source/EP-XXXX.yaml`
- GitHub issue body: includi il blocco `> Questa è un'epica — va decomposta prima dell'implementazione` in cima, poi tutte le sezioni in italiano con sub_stories come checklist

### Phase 2: Story Decomposition

From the feature, generate 2-6 user stories following INVEST criteria:

- Each story gets an ID: `US-XXXX` (increment from `.story_counter` in project root, create if absent)
- Format: Read `templates/story-yaml.md` for the YAML schema
- Each story MUST have at least 2 acceptance criteria in Given/When/Then format
- Story points: Fibonacci (1, 2, 3, 5, 8). If >8, split the story
- **Include `context` field** with: da dove viene questa storia (epica parent, bando, discovery), riferimenti a documenti, stato AS-IS del sistema. Senza contesto il YAML è inutile.
- Se la storia ha un'epica parent, imposta `parent_epic: EP-XXXX` e aggiorna `child_stories` nell'epica

### Phase 3: Quick Validation

For each generated story, check INVEST inline (no external scripts):

| Criterion   | Pass if...                             |
| ----------- | -------------------------------------- |
| Independent | No circular deps, minimal blocking     |
| Negotiable  | Describes outcome, not implementation  |
| Valuable    | Has clear "so that" benefit            |
| Estimable   | Has story points + acceptance criteria |
| Small       | <=8 points                             |
| Testable    | Has Given/When/Then criteria           |

Fix any failures before presenting to user.

### Phase 4: Write Story Files

- YAML source: `stories/yaml-source/US-XXXX.yaml`
- Markdown doc: `stories/generated-docs/US-XXXX.md`

Create `stories/` directories if they don't exist in the project.

### Phase 5: Present Summary

Show table of generated stories with: ID, title, points, persona, acceptance criteria count.
Ask user to approve, modify, or regenerate.

### PRD Mode (`--prd`)

When `--prd` flag is present, wrap stories into a Product Requirements Document:

- Read `templates/prd.md` for the PRD format
- PRD aggregates related stories into a product-level document
- Includes: executive summary, user personas, story map, success metrics, timeline
- Save to: `docs/development/prds/PRD-XXXX.md`

---

## Subcommand: `decompose`

Decompone un'epica EP-XXXX nelle sue storie figlie US-XXXX.

### Process

1. Leggi `stories/yaml-source/EP-XXXX.yaml` (ID passato come argomento)
2. Per ogni voce in `sub_stories`, genera una storia US-XXXX:
   - Imposta `parent_epic: EP-XXXX`
   - Imposta `blocked_by` in base alle dipendenze logiche tra le storie figlie
   - Copia `context` dall'epica e aggiungi la specifica della singola storia
   - Compila `acceptance_criteria` (Given/When/Then) specifici per questa storia
   - Stima `story_points` (Fibonacci 1-8)
3. Scrivi i file `stories/yaml-source/US-XXXX.yaml`
4. Aggiorna il campo `child_stories` nell'epica con i nuovi ID
5. Aggiorna il campo `status` dell'epica a `decomposed`
6. Presenta la tabella delle storie figlie generate con ID, titolo, punti, dipendenze
7. Chiedi conferma prima di creare le GitHub issue
8. Dopo aver creato le issue figlie, **chiudi l'issue epica** su GitHub:
   ```bash
   gh issue comment <epic_issue_number> --body "Decomposed into: US-XXXX #NNN, US-XXXX #NNN, ..."
   gh issue close <epic_issue_number> --reason "not planned"
   ```
   Rationale: l'epica è un contenitore di planning, non un work item. Una volta decomposta,
   il lavoro reale vive nelle storie figlie. L'issue epica rimane visibile (non cancellata)
   con il commento che linka le figlie.

### GitHub issue per storie figlie

Usa il titolo formato: `[MILESTONE|NN] [PP] US-XXXX feat: titolo`
Nel body: includi link all'epica parent (`Part of EP-XXXX #NNN`) e i criteri Given/When/Then.

---

## Subcommand: `prp`

Bridge stories to PRP generation.

### Process

1. Load story YAML files from `$ARGUMENTS`
2. Read `templates/prp-bridge.md` for mapping rules
3. Compose PRP input:
   - Stories -> Requirements section (acceptance criteria become requirements)
   - Story points -> Complexity assessment
   - Personas -> User context
   - Dependencies -> Architecture constraints
4. Invoke `/prp-generator` skill with composed input
5. PRP saved to project's PRP directory (detected by project-detector.sh)

---

## Subcommand: `plan`

Sprint/milestone planning from story backlog.

### Process

1. Scan `stories/yaml-source/` for stories with status: `backlog` or `ready`
2. Show eligible stories sorted by priority (critical > high > medium > low), then by points
3. Ask for sprint parameters:
   - Capacity (story points, default: 40)
   - Duration (default: 2 weeks)
   - Buffer % (default: 20%)
4. Greedy-fit stories into capacity (priority order, skip if story exceeds remaining)
5. Check dependency constraints (blocked_by must be in same or earlier sprint)
6. Present sprint plan using `templates/sprint-report.md` format
7. On approval:
   - Update story YAML status -> `sprint: "Sprint YYYY-NN"`
   - Optionally create GitHub milestone via `gh api`

---

## Subcommand: `update`

Create new stories from a change request or user feedback.

### Process

1. Ask user: what changed? (new requirement, bug found, scope change, feedback)
2. Load existing stories from `stories/yaml-source/`
3. Generate new stories or modify existing ones
4. Validate INVEST inline
5. Write updated YAML + Markdown

---

## Subcommand: `sync`

Push stories and epics to GitHub issues.

### Process

1. Load all YAML files from `stories/yaml-source/` (both EP-XXXX and US-XXXX)
2. For each file without `github_issue`:
   - Epic: `gh issue create --title "[MILESTONE|NN] [P0] EP-XXXX epica: titolo" --body <body con header epica + sub_stories checklist>`
   - Story: `gh issue create --title "[MILESTONE|NN] [PP] US-XXXX feat: titolo" --body <body con AC Given/When/Then + link parent epic>`
3. Update YAML with `github_issue: <number>`
4. For files with existing issues, update body if content changed
5. For stories with `parent_epic`: add comment linking to parent issue

---

## Template Locations

| Template          | Purpose                        | File                         |
| ----------------- | ------------------------------ | ---------------------------- |
| Epic YAML format  | Schema per file epica EP-XXXX  | `templates/epic-yaml.md`     |
| Story YAML format | Schema per file storia US-XXXX | `templates/story-yaml.md`    |
| PRP bridge        | Story -> PRP section mapping   | `templates/prp-bridge.md`    |
| PRD format        | Product requirements document  | `templates/prd.md`           |
| Sprint report     | Sprint plan output             | `templates/sprint-report.md` |
| GitHub issue      | Issue body template            | `templates/github-issue.md`  |
| GitHub issue      | Issue body template            | `templates/github-issue.md`  |

## Progressive Disclosure

1. **Start lean** — show story summaries, not full YAML dumps
2. **Read templates on demand** — use Read tool, don't memorize content
3. **User drives depth** — "show details", "show YAML", "show criteria" trigger deeper output
4. **One subcommand at a time** — don't chain create+tests+prp unless user asks for full pipeline
