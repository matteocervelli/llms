---
name: registry
description: Query, update, and audit the registry of all Claude Code components (skills, agents, rules, hooks, plugins) with PDCA lifecycle tracking. Use when listing/inspecting components, finding stale ones, or registering new ones. Trigger on "list skills", "component registry", "what skills exist", "stale skills", "/registry".
---

# Component Registry

PDCA lifecycle management for all Claude Code system components.

## Usage

```
/registry                        # Dashboard — counts + stale warnings
/registry list [type]            # List components (skills, agents, rules, hooks, plugins)
/registry check <name>           # Full detail for one component
/registry update                 # Scan filesystem, add new components, preserve manual fields
/registry scan                   # Integrity check (broken refs, orphans, missing frontmatter)
/registry stale [days]           # Components not tested in N days (default: 30)
/registry deprecate <name>       # Deprecate a skill: move to _archived/, update registry.yaml
```

## Data Store

`~/.claude/docs/development/registry.yaml` — single YAML file, version-controlled.

## Subcommand Details

### `/registry` (default) — Dashboard

Read `registry.yaml` and produce a summary:

```markdown
## Component Registry Dashboard

| Type    | Count | Act | Check | Do  | Plan | Stale (>30d) |
| ------- | ----- | --- | ----- | --- | ---- | ------------ |
| Skills  | 38    | 12  | 5     | 8   | 13   | 20           |
| Agents  | 2     | 0   | 1     | 1   | 0    | 2            |
| Rules   | 12    | 8   | 2     | 1   | 1    | 5            |
| Hooks   | 7     | 5   | 1     | 1   | 0    | 3            |
| Plugins | 7     | 4   | 2     | 1   | 0    | 2            |

**Warnings**: 32 components not tested in >30 days.
```

### `/registry list [type]` — List Components

List all components, optionally filtered by type.

Output format per component:

```
[pdca_status] name — why (last_manual_test)
```

Example:

```
Skills (38):
  [act]   security — Single entry point for security guidance (2026-02-14)
  [act]   review — Unified review dispatcher (2026-02-14)
  [plan]  analytics — DB query helper (never tested)
  ...

Deprecated (2):
  [deprecated] example-skill — Replaced by /unified (deprecated 2026-03-09, remove by 2026-06-07)
  [deprecated] old-helper — No longer needed (deprecated 2026-02-01, OVERDUE: was due 2026-05-02)
```

Deprecated entries always appear in a separate section at the bottom, never mixed with active components.

### `/registry check <name>` — Component Detail

Find component by name in any type section. Display all fields:

```markdown
## security (skill)

| Field            | Value                                                                      |
| ---------------- | -------------------------------------------------------------------------- |
| Category         | security                                                                   |
| Why              | Single entry point for stack-specific security guidance                    |
| Intended Impact  | Replace 11 fragmented SOPs with progressive disclosure                     |
| Actual Effect    | Works — tested on app-levero                                               |
| PDCA Status      | act                                                                        |
| Last Manual Test | 2026-02-14                                                                 |
| Depends On       | security-verify                                                            |
| Subcommands      | backend, frontend, database, infrastructure, operations, matrix, checklist |
```

### `/registry update` — Scan & Sync

1. Scan filesystem for all components:
   - `skills/*/SKILL.md` (excluding `_archived`) — parse YAML frontmatter
   - `agents/*.md` (excluding `_archived`) — parse YAML frontmatter
   - `rules/*.md` — parse YAML frontmatter
   - `hooks/handlers/*.py` — extract handler functions
   - `settings.json` → `enabledPlugins` — extract enabled plugins

2. For each component found:
   - If already in `registry.yaml`: preserve all manual fields (why, intended_impact, actual_effect, pdca_status, last_manual_test)
   - If new: add with `pdca_status: plan`, `last_manual_test: null`, other fields as "TBD"

3. Remove components from the active `skills:` section of `registry.yaml` that no longer exist on disk. Do NOT remove entries from the `deprecated:` section.

4. Write updated `registry.yaml`

### `/registry scan` — Integrity Check

Check for:

- **Orphaned skill dirs**: directories in `skills/` (excluding `_archived/`) without `SKILL.md`
- **Missing frontmatter**: SKILL.md files without `name:` in frontmatter
- **Broken skill refs**: skills that reference non-existent skills in their content
- **Agent skill refs**: agents listing skills that don't exist
- **Stale archived refs**: active files referencing `_archived/` paths
- **Registry drift**: components in active sections of registry.yaml that don't exist on disk
- **Overdue removals**: entries in `deprecated:` section where `removal_date < today`
  → Flag as `[ACTION REQUIRED] Remove <name> (was due YYYY-MM-DD)`
- **Upcoming expirations**: deprecated entries where `removal_date` is within 14 days
  → Flag as `[WARN] <name> removal in N days (YYYY-MM-DD)`
- **Archived dir drift**: directories in `skills/_archived/` that have no corresponding entry in the `deprecated:` section of registry.yaml — these were moved manually without going through `/registry deprecate`
- **DRY violations**: skill SKILL.md files that inline content already covered by a rule in `rules/`,
  without referencing the rule file. Run this check using the following Python snippet:

  ```python
  import re
  from pathlib import Path

  rules_dir = Path.home() / ".claude/rules"
  skills_dir = Path.home() / ".claude/skills"

  for skill_dir in sorted(skills_dir.iterdir()):
      if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
          continue
      skill_md = skill_dir / "SKILL.md"
      if not skill_md.exists():
          continue
      body = skill_md.read_text()
      for rule_file in sorted(rules_dir.glob("*.md")):
          m = re.search(r"^#+\s+(.+)", rule_file.read_text(), re.MULTILINE)
          if not m:
              continue
          phrase = m.group(1).strip().lower()
          if phrase not in body.lower() or rule_file.name in body:
              continue
          # Check proximity: if rule filename is within 40 lines, suppress
          lines = body.split("\n")
          for i, line in enumerate(lines):
              if phrase in line.lower():
                  window = "\n".join(lines[max(0, i - 40) : i + 40])
                  if rule_file.name not in window:
                      print(f"⚠ DRY: {skill_dir.name} inlines '{phrase}' without referencing {rule_file.name}")
                  break
  ```

  Flag as `⚠ DRY: <skill> inlines '<phrase>' without referencing rules/<file>.md`.
  Fix: replace inlined content with `See \`rules/<file>.md\``.

Output: list of issues found, or "No integrity issues detected."

### `/registry routing-check` — Routing Eval + DRY Audit

Run the routing eval framework against all skill fixtures, then check for DRY violations.

**Step 1 — Fixture coverage (structural, $0):**

```bash
cd ~/.claude/routing-eval
uv run python -m framework.runner --report-dir results/
```

Reports:

- Skills with no fixture file in `routing-eval/fixtures/claude/` → unreachable (no test)
- Skills failing Layer A (keyword match misses or wrong skill matched)
- Ambiguous pairs (two skills competing for the same trigger phrases)
- Pass rate per skill and overall

**Step 2 — Usage analytics (from SQLite, $0):**

Parse `tags` and `analysis_text` fields to identify which skills were invoked.
Cross-reference with the registry to surface:

```
72 skill registrate | 25 usate (30gg) | 47 mai invocate
```

Flag skills not invoked in 60+ days as candidates for archival.

**Step 3 — DRY audit (grep-based, $0):**

For each `rules/*.md`, extract key phrases (first `##` heading + 3 most distinctive terms).
For each `skills/*/SKILL.md`, check if those phrases appear inline without a reference to the rule file.
Suppress if the rule filename appears within 40 lines of the inline content.

Output format:

```
⚠ DRY: skill "deploy" contains 12 lines about security scanning but does not reference rules/security-gate.md
⚠ DRY: skill "implementation" inlines TDD steps without referencing rules/tdd.md
```

**Step 4 — 6-check summary (like GBrain check-resolvable):**

| Check               | What                                            | Pass condition |
| ------------------- | ----------------------------------------------- | -------------- |
| 1 Reachability      | Every skill has a fixture file                  | 0 missing      |
| 2 File existence    | Every fixture references a real SKILL.md        | 0 broken       |
| 3 MECE overlap      | No two skills dominate the same trigger         | 0 collisions   |
| 4 MECE gap          | No fixture left unmatched by any skill          | 0 gaps         |
| 5 DRY violations    | No inlined rule content                         | 0 violations   |
| 6 Frontmatter audit | All SKILL.md have name + description ≤200 chars | 0 malformed    |

Output: `PASS (6/6)` or `FAIL (4/6) — see details above`.

### `/registry stale [days]` — Stale Components

Filter `registry.yaml` for components where `last_manual_test` is null or older than N days (default: 30).

Output: sorted list, oldest first, with component name, type, and last test date.

### `/registry deprecate <name> [--grace-days N]` — Deprecate a Skill

Formal sunsetting process for a skill. Default grace period: 90 days.

**Workflow:**

1. Validate `<name>` exists in the active `skills:` section of registry.yaml and is not already deprecated
2. Ask for `deprecation_reason` if not supplied as `--reason "string"`
3. Move `skills/<name>/` directory to `skills/_archived/<name>/`
4. Prepend standard deprecation banner to `skills/_archived/<name>/SKILL.md`:
   ```markdown
   > **DEPRECATED**: <deprecation_reason>. Will be removed on <removal_date>.
   ```
5. Remove `<name>` from active `skills:` section in registry.yaml
6. Add entry to `deprecated:` section:
   ```yaml
   <name>:
     type: skill
     deprecation_date: <today>
     removal_date: <today + grace_days>
     deprecation_reason: "<reason>"
   ```
7. Print summary and suggest CHANGELOG entry:
   ```
   chore(registry): deprecate <name> — <reason>
   ```

**Example:**

```
/registry deprecate prp-generator --reason "Merged into /story prp subcommand" --grace-days 60
```

---

## PDCA Status Meanings

| Status       | Meaning                                                                   |
| ------------ | ------------------------------------------------------------------------- |
| `plan`       | Component exists but hasn't been validated. Needs review.                 |
| `do`         | Being actively developed or modified.                                     |
| `check`      | Implementation done, needs testing/validation.                            |
| `act`        | Tested, validated, working in production. Monitoring.                     |
| `deprecated` | Replaced or obsolete. Moved to `_archived/`. Grace period before removal. |

## Lifecycle

```
plan → do → check → act ─┬→ deprecated → [removed from registry]
                          └→ (stays active, re-enters plan if issue found)

Deprecated lifecycle:
  /registry deprecate <name>
    → skill dir moves to skills/_archived/<name>/
    → deprecation_date set, removal_date = deprecation_date + grace_days
    → /registry scan flags [WARN] when within 14 days
    → /registry scan flags [ACTION REQUIRED] when past removal_date
```

## Workflow

Typical PDCA cycle for a component:

1. Create/modify component → set `pdca_status: do`
2. Implementation complete → set `pdca_status: check`
3. Manual test passes → set `pdca_status: act`, update `last_manual_test`
4. Issue found → set `pdca_status: plan`, document issue in `actual_effect`
5. Component replaced/obsolete → run `/registry deprecate <name>`
