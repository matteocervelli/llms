---
name: skillify
description: Convert a working prototype or ad-hoc solution into a permanent, tested, registered skill. Run after something works and you want it to stick.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Skillify

Converts a working solution into a permanent skill with routing tests, registry
entry, and DRY compliance. The complement of `/hookify` (which blocks failures)
— this crystallises successes.

## Usage

```
/skillify <name>              # Full 8-step pipeline for a new skill
/skillify <name> --check      # Audit an existing skill (steps 3-8 only)
/skillify <name> --step 3     # Run a single step
```

## When to use

- You just solved something ad-hoc and want it reusable
- A workaround worked 3+ times → time to make it a skill
- `/memory extract` surfaces a recurring pattern worth formalising
- After `/quick` or a raw session where something clicked

## 8-Step Pipeline

Run steps in order. Stop and report if any step fails — do not skip.

---

### Step 1 — SKILL.md contract

If `~/.claude/skills/<name>/SKILL.md` does not exist, create it.

Required frontmatter:

```yaml
---
name: <name>
description: "<one sentence, < 200 chars, no quotes inside>"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob # trim to what's needed
---
```

If it exists, validate:

- `name:` matches directory name
- `description:` present and < 200 characters
- `allowed-tools:` present

**Verify**: parse frontmatter with Python — must not raise `yaml.YAMLError`.

```bash
python3 -c "
import yaml, sys
fm = open('$HOME/.claude/skills/<name>/SKILL.md').read()
end = fm.find('---', 3)
d = yaml.safe_load(fm[3:end])
assert 'name' in d and 'description' in d, 'missing fields'
assert len(d['description']) < 200, f'description too long: {len(d[\"description\"])}'
print('OK:', d['name'], '-', d['description'][:60])
"
```

---

### Step 2 — Deterministic extraction

Read the SKILL.md body. Identify logic that is:

- Computing / parsing / transforming data (same input → same output)
- Making API calls and parsing structured responses
- Searching files or running commands and collecting results

If found: create `~/.claude/skills/<name>/scripts/<name>.py` (or `.sh`) and
replace the prose description with a `Run:` block that calls the script.

If not found: note "prompt-only skill — no script needed" and continue.

See `rules/skill-architecture.md` for the deterministic-vs-latent decision table.

**Verify**: if a script was created, it runs without error on sample input.

---

### Step 3 — Routing test

Create `~/.claude/routing-eval/fixtures/claude/<name>.jsonl` with:

- 5+ positive triggers (natural language, NOT copies of the description)
- 3+ negative triggers (`"expected_skill": null, "should_match": false`)
- Mix Italian and English inputs

Then run Layer A check:

```bash
cd ~/.claude/routing-eval
uv run python -m framework.runner --skill <name> --verbose
```

**Verify**: 0 FAIL results. AMBIGUOUS is acceptable (Layer B resolves at runtime).
If the skill collides with an existing skill, revise the description to disambiguate.

---

### Step 4 — Functional test

**Script-backed skill**: create `~/.claude/skills/<name>/tests/test_<name>.py`
with at least one test for happy path and one for error handling. Run with:

```bash
cd ~/.claude/skills/<name> && uv run pytest tests/ -q
```

**Prompt-only skill**: invoke the skill with a known input and verify the output
matches the expected structure (sections present, no empty output, no error).
Document the test case in a `## Smoke Test` section of SKILL.md.

**Verify**: test passes.

---

### Step 5 — DRY check

Scan the SKILL.md body for content that duplicates existing rules:

```bash
python3 - <<'EOF'
import re
from pathlib import Path

skill_md = Path.home() / ".claude/skills/<name>/SKILL.md"
rules_dir = Path.home() / ".claude/rules"
body = skill_md.read_text()

violations = []
for rule_file in sorted(rules_dir.glob("*.md")):
    # Extract first heading as key phrase
    m = re.search(r'^#+\s+(.+)', rule_file.read_text(), re.MULTILINE)
    if not m:
        continue
    phrase = m.group(1).strip().lower()
    # Check if phrase appears in body without a reference to the rule file
    if phrase in body.lower() and rule_file.name not in body:
        # Suppress if rule filename mentioned within 40 lines of the phrase
        lines = body.split('\n')
        for i, line in enumerate(lines):
            if phrase in line.lower():
                window = '\n'.join(lines[max(0,i-40):i+40])
                if rule_file.name not in window:
                    violations.append(f"{rule_file.name}: '{phrase}' inlined without reference")
                    break

if violations:
    for v in violations: print("⚠ DRY:", v)
else:
    print("OK: no DRY violations")
EOF
```

If violations found: replace inlined content with a one-liner reference:
`See \`rules/<rule-file>.md\``.

**Verify**: script outputs "OK: no DRY violations".

---

### Step 6 — Registry entry

Update `~/.claude/docs/development/registry.yaml`:

```yaml
skills:
  <name>:
    category: <appropriate category>
    why: "<why this skill exists>"
    intended_impact: "<what it should do>"
    actual_effect: "New — not yet tested in production"
    pdca_status: check
    last_manual_test: "<today YYYY-MM-DD>"
    depends_on: []
    subcommands: []
```

Use `/registry update` to auto-add, then manually fill `why` and `intended_impact`.

**Verify**: `grep -A5 "^  <name>:" ~/.claude/docs/development/registry.yaml` shows the entry.

---

### Step 7 — Smoke test

Invoke the skill with a real input and observe the output:

```
/skillify <name> --step 7
→ invoke: /<name> <real-world input>
→ verify: output is non-empty, no errors, matches expected structure
```

Document the result in the registry `actual_effect` field.

**Verify**: skill completes without error on a real input.

---

### Step 8 — Convention reference

Check that the SKILL.md references the relevant rules for its domain:

| Skill type             | Required rule references                |
| ---------------------- | --------------------------------------- |
| Any code-writing skill | `rules/tdd.md`, `rules/code-quality.md` |
| Security-adjacent      | `rules/security-gate.md`                |
| Memory/knowledge       | `rules/memory-system.md`                |
| Deployment/infra       | `rules/cicd-split.md`                   |
| Script-backed          | `rules/skill-architecture.md`           |

If a relevant rule is not referenced: add a one-liner to the SKILL.md.

**Verify**: grep confirms rule references present.

---

## Cross-sistema: Codex port

After all 8 steps pass, port to Codex:

```bash
# Copy SKILL.md (adapt paths if needed)
mkdir -p ~/.codex/skills/<name>
cp ~/.claude/skills/<name>/SKILL.md ~/.codex/skills/<name>/SKILL.md

# Copy fixtures
cp ~/.claude/routing-eval/fixtures/claude/<name>.jsonl \
   ~/.claude/routing-eval/fixtures/codex/<name>.jsonl

# Update Codex registry
# Add entry to ~/.codex/docs/system-registry.yaml
```

## Completion report

After all 8 steps:

```
✓ Step 1: SKILL.md valid (name, description < 200 chars)
✓ Step 2: [script created | prompt-only]
✓ Step 3: routing.jsonl — Layer A pass rate X/Y
✓ Step 4: [N tests passing | smoke test documented]
✓ Step 5: no DRY violations
✓ Step 6: registry entry — pdca_status: check
✓ Step 7: smoke test passed
✓ Step 8: rule references confirmed

Skill <name> is permanent. Run /registry routing-check to verify global routing.
```
