---
name: story-verify
description: Validate user stories — INVEST scoring, story-to-test coverage mapping, PRP completeness, and development-readiness assessment. Use after writing stories and before starting implementation. Trigger on "validate the stories", "are these stories ready", "INVEST check", "story coverage", "is this ready to build".
allowed-tools: Read, Grep, Glob, Bash
---

# Story Verification

Validate stories, check test coverage gaps, verify PRP completeness, and assess development readiness.

## Usage

```
/story-verify                       # Auto: validate all stories in project
/story-verify invest <id|all>       # INVEST criteria scoring
/story-verify coverage              # Map stories -> tests, show gaps
/story-verify prp                   # Check PRP completeness against stories
/story-verify ready <id>            # Development readiness assessment
```

## Workflow

### Step 1: Determine Mode

Parse `$ARGUMENTS` for explicit subcommand. If no arguments, run `invest all` as default.

Detect project context:

```bash
PROJECT_INFO=$(bash "$HOME/.claude/skills/story/lib/project-detector.sh")
```

### Step 2: Route to Subcommand

---

## Subcommand: `invest`

INVEST criteria validation — no Python scripts, pure template-based inline logic.

### Process

1. Load story YAML from `stories/yaml-source/US-XXXX.yaml` (or all if "all")
2. Read `templates/invest-checklist.md` for scoring rules
3. Score each criterion (0-100):

| Criterion       | Score 100                                  | Score 50                             | Score 0                          |
| --------------- | ------------------------------------------ | ------------------------------------ | -------------------------------- |
| **Independent** | No blocked_by, or only 1 external dep      | 2-3 dependencies                     | Circular deps or >3 blockers     |
| **Negotiable**  | "i_want" describes outcome/behavior        | Mentions specific tech but flexible  | Prescribes exact implementation  |
| **Valuable**    | Clear "so_that" with measurable benefit    | Vague benefit ("improve experience") | Missing "so_that" entirely       |
| **Estimable**   | Has story_points + >=3 acceptance_criteria | Has points OR criteria, not both     | Missing both points and criteria |
| **Small**       | 1-5 story points                           | 6-8 story points                     | >8 points (must split)           |
| **Testable**    | All criteria have given/when/then          | Some criteria missing parts          | No given/when/then at all        |

4. **Overall score** = average of 6 criteria
5. **Pass**: overall >= 70 AND all criteria >= 50

### Output

```
Story US-XXXX: "View financial dashboard"
  I: 100  N: 100  V: 75  E: 100  S: 100  T: 100
  Overall: 96 — PASS

  Issues:
  - [Medium] Valuable: "so_that" could be more specific about measurable outcome
```

### Auto-Fix Suggestions

| Issue                               | Fix                                                             |
| ----------------------------------- | --------------------------------------------------------------- |
| Missing "so_that"                   | Suggest based on persona goals and feature context              |
| Vague benefit                       | Add measurable outcome (number, percentage, time saved)         |
| Missing story points                | Estimate from acceptance criteria count (1 criterion ≈ 1 point) |
| Too few criteria                    | Suggest additional Given/When/Then from feature scope           |
| Implementation language in "i_want" | Rewrite to describe behavior, not code                          |
| >8 points                           | Suggest story splitting strategy                                |

---

## Subcommand: `coverage`

Map stories to test files and identify untested acceptance criteria.

### Process

1. Load all story YAML files
2. For each story, search test directory for matching test file:
   - Pattern: `test_US_XXXX*` (pytest) or `US_XXXX*.test.*` (jest)
3. For each acceptance criterion in the story:
   - Search test files for matching test function (by criterion slug or docstring)
4. Build coverage matrix

### Output

Read `templates/coverage-matrix.md` for output format.

```
Story Coverage Matrix
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

US-0001: View dashboard          [2/3 criteria covered]
  ✓ health score displayed       → test_dashboard_shows_health_score
  ✓ KPI pillars visible          → test_dashboard_shows_kpi_pillars
  ✗ color indicator correct      → NO TEST

US-0002: Upload document         [0/2 criteria covered]
  ✗ PDF accepted                 → NO TEST
  ✗ error on invalid file        → NO TEST

Summary: 2/5 criteria covered (40%)
Gap: 3 criteria need test stubs — run `/story tests US-0001 US-0002`
```

---

## Subcommand: `prp`

Check PRP completeness against its source stories.

### Process

1. Scan PRP directory (detected by project-detector.sh) for PRP files
2. For each PRP, extract referenced stories (look for US-XXXX patterns)
3. Cross-reference with story YAML files:
   - Are all referenced stories defined?
   - Do all stories have sufficient acceptance criteria?
   - Are story dependencies resolvable?
4. Check PRP sections against PRP completeness checklist:
   - Header with metadata
   - Executive summary
   - Requirements reference
   - Architecture design
   - Implementation plan (phased)
   - Testing strategy
   - Success criteria

### Output

```
PRP-012: Financial Data Display
  Stories referenced: US-0010, US-0011, US-0012, US-0013
  ✓ All stories defined in YAML
  ✓ All stories have acceptance criteria
  ✗ US-0011 blocked_by US-0009 (not in scope — risk)
  ✓ PRP has all required sections
  ✗ Testing strategy missing E2E test plan
```

---

## Subcommand: `ready`

Full readiness assessment for a story before implementation starts.

### Process

1. Run `invest` validation (must pass)
2. Check dependencies: all `blocked_by` stories must be status `done`
3. Check test stubs exist (from `/story tests`)
4. Check PRP exists for the story's feature area
5. Check technical context (has enough detail for implementation)

### Output

Read `templates/readiness-checklist.md` for format.

```
US-0012: Display financial data tables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✓ INVEST validation: PASS (score: 92)
  ✓ Dependencies: US-0011 (done), US-0009 (done)
  ✗ Test stubs: NOT FOUND — run `/story tests US-0012`
  ✓ PRP: PRP-012 covers this story
  ✓ Technical context: FastAPI route + Jinja2 template

  Verdict: ALMOST READY — generate test stubs first
```

---

## Template Locations

| Template            | Purpose                      | File                               |
| ------------------- | ---------------------------- | ---------------------------------- |
| INVEST checklist    | Scoring rules and thresholds | `templates/invest-checklist.md`    |
| Coverage matrix     | Story-to-test mapping format | `templates/coverage-matrix.md`     |
| Readiness checklist | Dev readiness criteria       | `templates/readiness-checklist.md` |
