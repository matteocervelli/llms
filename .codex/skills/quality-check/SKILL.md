---
name: quality-check
description: Multi-language code quality validation (Python, JS/TS, Shell, SQL) — formatting, linting, type-checking, complexity analysis with auto language detection. Use when checking code quality or running linters. Trigger on "lint", "type-check", "quality check", "run the linters", "check code quality".
allowed-tools: Read, Bash, Grep, Glob
---

# Quality Check Skill

## Purpose

Unified code quality validation across Python, JavaScript/TypeScript, Shell, and SQL. Runs formatting checks, linting, type checking, and complexity analysis.

## Quick Start

```bash
# Auto-detect language and run appropriate checks
/quality-check [path]
```

## Language Detection

The skill auto-detects language based on file extensions:

- `.py` -> Python tools
- `.js`, `.ts`, `.tsx`, `.jsx` -> JavaScript/TypeScript tools
- `.sh`, `.bash` -> Shell tools
- `.sql` -> SQL validation

## Tool Matrix

| Language | Formatter   | Linter     | Type Check  | Complexity        |
| -------- | ----------- | ---------- | ----------- | ----------------- |
| Python   | ruff format | ruff check | mypy        | radon cc          |
| JS/TS    | prettier    | eslint     | tsc         | eslint complexity |
| Shell    | shfmt       | shellcheck | -           | -                 |
| SQL      | -           | sqlfluff   | -           | -                 |
| Swift    | -           | swiftlint  | swift build | -                 |
| Go       | gofmt       | golint     | go vet      | -                 |
| Rust     | rustfmt     | clippy     | -           | -                 |

## Commands by Language

### Python

```bash
# Format check (replaces black + isort)
ruff format --check src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Complexity (functions with cc > 10)
radon cc src/ -nc
```

### JavaScript/TypeScript

```bash
# Format check
npx prettier --check "src/**/*.{ts,tsx,js,jsx}"

# Lint
npx eslint "src/**/*.{ts,tsx}"

# Type check
npx tsc --noEmit

# Dependency audit
npm audit --production
```

### Shell

```bash
# Lint
shellcheck scripts/*.sh

# Format check (if shfmt installed)
shfmt -d scripts/*.sh
```

### SQL

```bash
# Lint (if sqlfluff installed)
sqlfluff lint queries/
```

### Swift

```bash
# Lint
swiftlint

# Build check (type checking)
swift build
```

### Go

```bash
# Format check
gofmt -d .

# Lint
golint ./...

# Vet (static analysis)
go vet ./...
```

### Rust

```bash
# Format check
cargo fmt --check

# Lint
cargo clippy -- -D warnings
```

## Quality Standards

### All Languages

| Metric        | Threshold         |
| ------------- | ----------------- |
| File size     | < 500 lines       |
| Function size | < 50 lines        |
| Complexity    | < 10 per function |
| Nesting depth | < 4 levels        |

### Python-Specific

- Type hints on all functions
- Google-style docstrings on public API
- No bare `except:` clauses
- No mutable default arguments

### TypeScript-Specific

- Strict mode enabled
- Explicit return types
- No `any` types (except justified)
- No unused variables

## Output Format

```markdown
# Quality Report

**Status**: PASS/FAIL
**Files Checked**: N
**Language**: Python/TypeScript/Mixed

## Results

| Check      | Status | Issues           |
| ---------- | ------ | ---------------- |
| Format     | PASS   | 0                |
| Lint       | PASS   | 0                |
| Types      | PASS   | 0                |
| Complexity | WARN   | 2 functions > 10 |

## Issues Found

### Critical

[None or list]

### Warnings

- `src/utils.py:45` - complexity 12 (function `process_data`)

## Auto-fix Available

Run: `ruff format src/ && ruff check --fix src/`
```

## Integration

This skill is called by `/pre-commit` as part of the full validation suite.

## Troubleshooting

### Tool Not Found

```bash
# Python
pip install ruff mypy radon

# JS/TS
npm install -D prettier eslint typescript

# Shell
brew install shellcheck shfmt  # macOS
apt install shellcheck shfmt   # Ubuntu
```

### Too Many Errors

Focus on one category at a time:

1. Fix formatting first (auto-fixable)
2. Then linting (many auto-fixable)
3. Then type errors (manual)
4. Complexity last (refactoring)
