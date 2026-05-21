---
name: map-codebase
description: Analyze an existing codebase in parallel via 7 specialized mapper subagents. Outputs structured findings to docs/codebase/ for persistent cross-session context. Use when onboarding to a brownfield project or when reactive on-demand file reading is too slow.
allowed-tools: Read, Bash, Grep, Glob, Task, Write
---

# Map-Codebase Skill

## Purpose

When starting work on an **existing codebase**, Claude must discover its structure, patterns,
and risks reactively — reading files on demand, accumulating context piecemeal. This skill
runs a one-time parallel analysis and persists the results in `docs/codebase/` so every
future session loads structured context instead of starting blind.

**Not for:** greenfield projects you built from scratch (you already know the structure).

---

## Usage

```bash
/map-codebase                  # full analysis (all 7 mappers)
/map-codebase <area>           # single mapper focus (e.g. "security", "stack", "test")
/map-codebase --refresh        # force re-analysis, even if docs/codebase/ exists
```

Valid area names: `stack`, `architecture`, `conventions`, `security`, `test`, `dependency`, `concerns`

---

## Workflow

### Step 0: Cache Check

Before spawning any agents, check if a previous map exists:

```bash
ls docs/codebase/INDEX.md 2>/dev/null
```

**If INDEX.md exists AND `--refresh` was NOT passed:**

- Display the existing INDEX.md summary to the user
- Ask: "Map exists from <Generated date>. Refresh all, refresh a specific area, or use existing?"
- Proceed only if user asks to refresh

**If `--refresh` or no map exists:** proceed to Step 1.

---

### Step 1: Pre-Triage

Before spawning agents, do a 30-second orientation:

```bash
# Count files by extension to understand the dominant language
find . -type f -not -path './.git/*' -not -path './.claude/*' \
  | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20

# Check for common entry points
ls -1 {main.py,app.py,index.ts,index.js,main.go,Cargo.toml,pyproject.toml,package.json} 2>/dev/null

# Size check — warn if > 500 files
find . -type f -not -path './.git/*' | wc -l
```

If > 2000 files: warn the user that analysis will take longer and suggest a focused area.

---

### Step 2: Ensure Output Directory

```bash
mkdir -p docs/codebase
```

---

### Step 3: Spawn Parallel Mapper Agents

For a **full analysis**, launch all 7 Task agents simultaneously.
For a **focused area** (`/map-codebase security`), launch only that agent.

Each agent is:

- `type: Explore` (read-only, no code modifications)
- `model: haiku` (fast, sufficient for structured analysis)
- Writes its output to `docs/codebase/<name>.md`

---

#### Agent Prompts

**stack-mapper** → `docs/codebase/stack.md`

```
You are a stack-mapper agent. Analyze this codebase and produce a structured report
about its technology stack.

Find and report:
- Primary language(s) and version(s) (check .python-version, .nvmrc, go.mod, Cargo.toml, etc.)
- Frameworks in use (FastAPI, Django, Next.js, Express, etc.) with versions
- Runtime environment (Node, Python, Go, Rust, JVM)
- Package manager (pip, uv, npm, pnpm, yarn, cargo, go mod)
- Key configuration files and what they control
- Deployment artifacts (Dockerfile, docker-compose, Procfile, fly.toml, etc.)

Write output to docs/codebase/stack.md using this schema:

## Summary
- <3-5 bullet summary>

## Key Findings
<detailed findings>

## Risks / Concerns
<version mismatches, EOL runtimes, etc.>

## Files Analyzed
<list of key files read>

## Generated: <ISO datetime>
```

---

**architecture-mapper** → `docs/codebase/architecture.md`

```
You are an architecture-mapper agent. Analyze this codebase's structural design.

Find and report:
- Top-level directory structure and purpose of each major folder
- Architectural pattern in use (MVC, CQRS, hexagonal, monolith, microservices, etc.)
- Entry points (main files, CLI commands, API routers, event handlers)
- Module boundaries and how they communicate (imports, message queues, REST, etc.)
- Any clear layering violations or circular dependencies

Write output to docs/codebase/architecture.md using this schema:

## Summary
- <3-5 bullet summary>

## Directory Map
<annotated tree of top-level dirs>

## Architectural Pattern
<detected pattern + evidence>

## Entry Points
<list of entry files/functions>

## Key Findings
<inter-module communication, layering>

## Risks / Concerns
<boundary violations, coupling>

## Files Analyzed
<list>

## Generated: <ISO datetime>
```

---

**conventions-mapper** → `docs/codebase/conventions.md`

```
You are a conventions-mapper agent. Analyze coding conventions and style patterns.

Find and report:
- Naming style for files, classes, functions, variables (snake_case, camelCase, PascalCase)
- File organization pattern (feature-based, layer-based, etc.)
- Import style (absolute vs relative, aliased, barrel exports)
- Recurring structural patterns (factory, repository, service, handler, etc.)
- Docstring / comment style
- Error handling style (exceptions, Result types, error codes)
- Any style config files (eslint, ruff, flake8, etc.)

Sample 10-15 representative files across the codebase. Do not read every file.

Write output to docs/codebase/conventions.md using this schema:

## Summary
- <3-5 bullet summary>

## Naming Conventions
<findings>

## File Organization
<findings>

## Recurring Patterns
<list of patterns with example file paths>

## Style Config
<linter/formatter config findings>

## Key Findings
<anything non-obvious>

## Risks / Concerns
<inconsistencies, mixed styles>

## Files Analyzed
<list>

## Generated: <ISO datetime>
```

---

**security-mapper** → `docs/codebase/security.md`

```
You are a security-mapper agent. Analyze the codebase's security surface.

Find and report:
- Authentication mechanism (JWT, session cookies, OAuth, API keys, none)
- Authorization model (RBAC, ABAC, middleware-based, none)
- Input validation approach (Pydantic, Zod, manual, none)
- Secrets handling (env vars, vaults, hardcoded strings — flag any hardcoded secrets)
- SQL/NoSQL query construction (ORM, parameterized, raw strings — flag raw string concat)
- External API calls and whether responses are validated
- File upload handling (if any)
- CORS and CSP configuration (if applicable)

DO NOT modify any files. Flag concerns, do not fix them.

Write output to docs/codebase/security.md using this schema:

## Summary
- <3-5 bullet summary>

## Auth & Authorization
<findings>

## Input Validation
<findings>

## Secrets Handling
<findings>

## Query Construction
<findings>

## Key Findings
<anything non-obvious>

## Risks / Concerns
<ranked by severity: HIGH / MEDIUM / LOW>

## Files Analyzed
<list>

## Generated: <ISO datetime>
```

---

**test-mapper** → `docs/codebase/test.md`

```
You are a test-mapper agent. Analyze the codebase's test coverage and strategy.

Find and report:
- Test framework(s) in use (pytest, jest, vitest, go test, etc.)
- Test directory structure and naming conventions
- Types of tests present (unit, integration, e2e, snapshot)
- Approximate test-to-source file ratio
- CI configuration (GitHub Actions, CircleCI, etc.) and what it runs
- Coverage reporting setup (if any)
- Mocking strategy (mocks, fakes, stubs, real dependencies)
- Any obvious gaps (untested modules, no integration tests, etc.)

Write output to docs/codebase/test.md using this schema:

## Summary
- <3-5 bullet summary>

## Test Framework
<findings>

## Coverage Estimate
<findings>

## CI Configuration
<findings>

## Key Findings
<gaps, patterns>

## Risks / Concerns
<untested critical paths, flaky test patterns>

## Files Analyzed
<list>

## Generated: <ISO datetime>
```

---

**dependency-mapper** → `docs/codebase/dependency.md`

```
You are a dependency-mapper agent. Analyze direct and notable transitive dependencies.

Find and report:
- All direct dependencies from manifest files (pyproject.toml, package.json, go.mod, Cargo.toml)
- Whether versions are pinned, ranged, or unpinned
- Any obviously outdated major versions (e.g. Python 2, React 16, Django 2)
- Any dependencies with known CVE patterns in their name (e.g. old cryptography, xml2, etc.)
- Duplicate dependencies serving the same purpose (e.g. two HTTP clients)
- Dev vs prod dependency separation

Do NOT run any package manager commands. Read manifest files only.

Write output to docs/codebase/dependency.md using this schema:

## Summary
- <3-5 bullet summary>

## Direct Dependencies
<categorized list: web, db, auth, infra, dev, etc.>

## Version Pinning
<findings>

## Notable Risks
<outdated, suspicious, duplicated deps>

## Key Findings
<anything non-obvious>

## Risks / Concerns
<ranked>

## Files Analyzed
<list>

## Generated: <ISO datetime>
```

---

**concerns-mapper** → `docs/codebase/concerns.md`

```
You are a concerns-mapper agent. Surface technical debt, code health signals, and
maintenance concerns.

Find and report:
- TODO/FIXME/HACK/XXX/NOSONAR count and distribution (grep, do not read every file)
- Largest files by line count (top 10 — flag any > 500 lines)
- Duplicated logic (similar function names, copy-paste blocks across files)
- Dead code signals (commented-out code blocks, unused imports in sampled files)
- Missing error handling (bare except, swallowed errors in sampled files)
- Deprecated patterns for the detected stack
- Any .old, .bak, _v2, or archived files left in the tree

Write output to docs/codebase/concerns.md using this schema:

## Summary
- <3-5 bullet summary>

## TODO/FIXME Count
<totals + hotspot files>

## Oversized Files
<top 10 by line count>

## Duplication Signals
<findings>

## Dead Code Signals
<findings>

## Key Findings
<anything non-obvious>

## Risks / Concerns
<ranked>

## Files Analyzed
<list>

## Generated: <ISO datetime>
```

---

### Step 4: Aggregate into INDEX.md

After all agents complete, synthesize findings into `docs/codebase/INDEX.md`:

```markdown
# Codebase Map — <project name>

**Generated:** <ISO datetime>
**Mappers run:** stack | architecture | conventions | security | test | dependency | concerns

## Stack Snapshot

<1-2 lines from stack.md summary>

## Architecture Snapshot

<1-2 lines from architecture.md summary>

## Test Health

<1-2 lines from test.md summary>

## Top 3 Cross-Cutting Concerns

1. <highest priority concern from any mapper>
2. <second>
3. <third>

## Security Flags

<any HIGH-severity items from security.md — or "None flagged">

## Quick-Start Recommendations

For the next session working in this codebase:

- Start by reading: <2-3 key files identified by architecture-mapper>
- Watch out for: <top concern>
- Run before committing: <test/lint commands from test-mapper>

## Refresh

Run `/map-codebase --refresh` to re-analyze.
Individual mappers: `/map-codebase <area>`
```

---

### Step 5: Report to User

Present a brief summary:

```
Codebase map complete. Wrote 7 mapper files + INDEX.md to docs/codebase/

Stack: <1-line>
Architecture: <1-line>
Top concern: <1-line>

Future sessions will auto-load this map at startup (if SessionStart hook is configured).
Run /map-codebase --refresh to update.
```

---

## Output Structure

```
docs/codebase/
├── INDEX.md           ← session-injectable summary
├── stack.md
├── architecture.md
├── conventions.md
├── security.md
├── test.md
├── dependency.md
└── concerns.md
```

All files are committed to the repo (project-shared, cross-session).

---

## SessionStart Integration

If `hooks/handlers/session.py` is configured to inject this map, it will:

- Check for `docs/codebase/INDEX.md` in `cwd`
- Inject the "Top 3 Cross-Cutting Concerns" and "Stack Snapshot" sections (≤10 lines)
- Append: `Codebase map available. Run /map-codebase --refresh to update.`

This is passive — no injection if the file is absent.

---

## Related Skills

- `/diagnose` — investigate bugs with unknown root cause (uses subagent pattern this skill mirrors)
- `/security-verify scan` — deep security scanning after security-mapper flags concerns
- `/health` — ongoing project audit (runs periodically; map-codebase is a one-time onboarding step)
- `/implementation` — once map is loaded, implementation has structured context about conventions
