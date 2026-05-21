---
name: techdebt
description: Detect technical debt — duplicated code, dead code, TODOs, and oversized functions across the codebase. Use at the end of a session or when auditing code hygiene. Trigger on "find tech debt", "any dead code", "duplicated code", "code hygiene", "techdebt".
allowed-tools: Read, Bash, Grep, Glob
---

# Tech Debt Finder

## Purpose

Surface technical debt patterns before they accumulate: duplicates, dead code, complexity hotspots, TODOs, oversized files.

## Quick Start

```bash
/techdebt              # scan current directory
/techdebt src/         # scan specific path
/techdebt --duplicates # only duplicate check
/techdebt --todos      # only TODO/FIXME markers
/techdebt --dead-code  # only dead code
```

## How to Run

Execute the scan script — it auto-detects Python/JS/TS and skips missing tools:

```bash
bash $CLAUDE_SKILL_DIR/scripts/scan.sh [path] [filter-flag]
```

Then **interpret and report** the output using the Output Format below. The script
handles tool invocation; your job is to classify findings by severity and suggest fixes.

## Output Format

Produce a `# Tech Debt Report` with:
1. **Summary table** — category, count, severity (Low / Medium / High)
2. **Details per category** — file, line, symbol, suggestion
3. **Quick Fixes** — any automatable repairs (`ruff --fix`, `eslint --fix`)
4. **Recommended Actions** — prioritized: Immediate / This week / Backlog

Severity thresholds: duplicates (Low ≤2, Medium 3-5, High >5), dead code (Low ≤5, High >10),
large functions (Medium >75 lines, High >100), large files (High >1000 lines), complexity CC >10 (Medium).

## Tool Reference

Tools the script uses (installed = runs; missing = skipped with note):

| Check            | Python           | JS/TS        |
| ---------------- | ---------------- | ------------ |
| Duplicates       | pylint           | jscpd        |
| Dead code        | vulture          | ts-prune     |
| Complexity/size  | radon            | eslint       |
| Circular imports | pycycle          | madge        |
| TODOs            | grep (no dep)    | grep (no dep)|

Install missing tools: `uv add --dev vulture radon pylint` / `npm install -D jscpd ts-prune madge`

## Gotchas

- `.venv`, `node_modules`, `dist`, `__pycache__` are auto-excluded by the scan script
- `pylint --enable=duplicate-code` is slow on large codebases; warn if scanning >500 files
- `ts-prune` only works from the project root (needs `tsconfig.json`); run from a sub-path → 0 findings
- `radon cc` = per-function cyclomatic complexity; `radon raw` = per-file LOC — different output formats
- Deprecated registry dependency check requires `~/.claude/docs/development/registry.yaml`; skip silently if absent
