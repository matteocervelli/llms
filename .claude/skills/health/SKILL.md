---
name: health
description: Holistic project audit across endpoints, versions, docs, security, quality, CI, and library dimensions. Use when checking overall project health or running a periodic cross-cutting audit. Trigger on "project health", "audit the project", "health check", "is this project in good shape".
allowed-tools: Read, Bash, Grep, Glob
---

# /health — Project Health Audit

Orchestrates a cross-cutting audit across all project dimensions. Designed to run periodically via
the native `/loop` bundled skill.

**Architecture — hybrid orchestrator:**

- **Native checks** (no dedicated sub-skill exists for these): `endpoints`, `versions`, `docs`
- **Pure delegation** (sub-skill owns the logic): `security` → `/security-verify scan`, `quality` → `/quality-check`, `library` → `/library`, `releases` → `/release verify tags`, `ci` → `/ci-setup audit`, `website` → `/website-health`

## Quick Start

```
/health                    # auto-detect project, show summary
/health full               # comprehensive audit across all dimensions
/health endpoints          # check routes vs docs
/health versions           # version string consistency
/health docs               # CLAUDE.md + README staleness + license check
/health roadmap            # bidirectional sync: ROADMAP.md ↔ GitHub Issues ↔ CHANGELOG
/health license            # check LICENSE file; advisor mode if missing
/health security           # delegate to /security-verify scan
/health quality            # delegate to /quality-check + tests + coverage
/health techdebt           # delegate to /techdebt (duplicates, dead code, TODOs, oversized functions)
/health deps               # delegate to /deps scan (outdated deps, CVEs, decision coverage)
/health hygiene            # filesystem lint: gitignore gaps, orphans, structure drift, root clutter
/health library            # delegate to /library scan + sync + drift + new
/health releases           # delegate to /release verify tags
/health ci                 # delegate to /ci-setup audit (Forgejo workflow drift, conditional)
/health agents             # review unreviewed agent-created issues (ai-suggested label)
/health agents triage      # interactive triage: dismiss, promote, or skip each signal
/health docker             # delegate to /docker-audit (if Dockerfile* or compose.yaml detected)
/health website            # delegate to /website-health (if website project detected)
/health branches           # stale branch audit — local, GitHub, Forgejo
/health issues             # open GitHub BACKLOG issues for findings
```

## Loop Integration

```
/loop 1h /health full      # hourly comprehensive audit
/loop 1d /health security  # daily security check
/loop 1d /health library   # daily library drift check
```

Uses the native Claude Code `/loop` bundled skill (CronCreate under the hood).
Tasks are session-scoped and auto-expire after 3 days.

---

## Subcommand: `/health` (summary)

Auto-detect project type and print a one-line status per dimension.

**Steps:**

1. Detect project type: check for `pyproject.toml` (Python), `package.json` (Node), `Cargo.toml` (Rust), MCP server markers (`server.py`, `mcp.json`)
2. Run each dimension sequentially (each sub-check runs to completion; delegated checks like security/library may take 30-300s)
3. Print consolidated summary with overall gate

**Output:**

```
## Health Summary — <project-name> — <date>

Endpoints  [PASS]  14 routes, all documented
Versions   [WARN]  pyproject.toml (0.3.1) ≠ README badge (0.3.0)
Docs       [PASS]  CLAUDE.md current, README current
Security   [PASS]  No critical/high findings
Quality    [PASS]  0 lint errors, 45/45 tests, 87% coverage
Tech Debt  [PASS]  0 critical findings
Hygiene    [WARN]  .coverage not in .gitignore; 2 unexpected top-level dirs
Releases   [PASS]  3 tags, all match CHANGELOG + GH/FJ releases + artifacts (pypi: 3/3)
Agents     [WARN]  12 unreviewed signals across 3 repos — run /health agents triage
Branches   [WARN]  3 local merged, 1 remote stale on Forgejo (if git repo)
Docker     [WARN]  Non-root USER missing in Dockerfile (if Docker files detected)
Website    [PASS]  7/7 dimensions pass (if website project detected)

Overall: WARN — 3 FIX-NOW (apply immediately) · 2 TRACK (open issues)
```

---

## Subcommand: `/health endpoints`

Compare implemented routes vs what is documented in README or API docs.

**Detection patterns:**

| Stack           | Pattern                                                            |
| --------------- | ------------------------------------------------------------------ |
| FastAPI         | `@router.(get\|post\|put\|delete\|patch)`, `@app.(get\|post\|...)` |
| Click CLI       | `@click.command`, `@cli.command`, `@<group>.command`               |
| MCP             | `@mcp.tool`, `@server.tool`, `@server.list_tools`                  |
| Express/Next.js | `app.(get\|post\|...)`, `router.(get\|...)`, `pages/api/**` glob   |

**Steps:**

1. Grep codebase for route/command decorators → build implemented set
2. Parse README "API Reference", "Commands", or "Endpoints" section → build documented set
3. Diff: implemented ∩ documented = OK; implemented \ documented = undocumented; documented \ implemented = dead docs

**Gate:**

- `PASS`: all implemented routes documented
- `WARN`: undocumented routes exist (non-security-critical)
- `FAIL`: undocumented route with auth/data-mutation pattern (POST/PUT/DELETE without docs)

---

## Subcommand: `/health versions`

Cross-check all version strings across manifest files and README.

**Version file detection** (reuses `/release changelog` Step 6 patterns):

| File          | Path                                                              |
| ------------- | ----------------------------------------------------------------- |
| Python        | `pyproject.toml` → `[project] version` or `[tool.poetry] version` |
| Node          | `package.json` → `.version`                                       |
| Rust          | `Cargo.toml` → `[package] version`                                |
| Legacy Python | `setup.cfg` → `version =`                                         |
| README badge  | `shields.io/badge/version-X.Y.Z` or similar                       |

**Steps:**

1. Find all version files via glob
2. Extract version string from each
3. Compare — flag any that differ
4. Output version matrix table

**Gate:**

- `PASS`: all versions match
- `WARN`: README badge differs (cosmetic)
- `FAIL`: any two production manifests disagree (pyproject.toml, package.json, Cargo.toml, setup.cfg — README badge excluded from FAIL since it's cosmetic)
  Note: normalize ranges (`^1.2` → `1.2.x`) before comparing; VCS/path deps are flagged as WARN with a note to pin

---

## Subcommand: `/health docs`

Check required documentation exists at the root, is in the right location, and is not stale.
Also audits user-facing docs via `/docs audit` (dual mode: Starlight for apps, markdown for libs/services).

**Delegates to:**

- `/docs audit` — user-facing docs (dual mode auto-detected from repo):
  - **App mode** (`app-*`): `site/` present? Starlight pages stale? links rotti? language parity IT↔EN?
- `/documentation-updater` — checklist completeness (only when all required files exist)
- `/registry stale 30` — stale `act`-status skills (>30 days); `plan`/`do`/`check` with null dates are excluded (not yet in validation phase)

### Step 0 — Existence check

Required root-level docs and their init path when missing:

| File            | Severity if missing | Init suggestion                               |
| --------------- | ------------------- | --------------------------------------------- |
| `CLAUDE.md`     | `FAIL`              | `/claude-md-management:claude-md-improver`    |
| `README.md`     | `FAIL`              | `/documentation-updater`                      |
| `LICENSE`       | `WARN`              | `/health license` (advisor mode)              |
| `ROADMAP.md`    | `WARN`              | `/documentation-updater` (architecture docs)  |
| `TECH-STACK.md` | `WARN`              | `/documentation-updater` (configuration docs) |

For each missing file: report the finding, state the severity, and offer the init command.

**LICENSE note:** If `LICENSE` is missing, note it as WARN and print: "Run `/health license` to get an interactive advisor that will recommend the right license based on your project type."

### Step 1 — Location check

Search for required docs in non-root locations and flag misplaced copies:

```bash
for f in CLAUDE.md README.md ROADMAP.md TECH-STACK.md; do
  # Check root
  root_present=$([ -f "$f" ] && echo "yes" || echo "no")
  # Find any copies elsewhere (exclude .git, node_modules, .venv)
  elsewhere=$(find . -name "$f" \
    -not -path "./.git/*" \
    -not -path "./node_modules/*" \
    -not -path "./.venv/*" \
    -not -path "./.archive/*" \
    -not -maxdepth 1 2>/dev/null)
  # If found in subdir but not at root → WARN: propose move
  # If found in subdir AND at root → INFO: note the duplicate
done
```

Report as `WARN` with the path and suggest: "Move to project root and update any links."

### Step 2 — Staleness check

Only runs for files confirmed present at root. Uses Unix timestamps to avoid sign-flip bug when file is absent.

```bash
# Last CLAUDE.md/README change vs last code change — use Unix timestamps for arithmetic
DOC_TS=$(git log -1 --format="%ct" -- CLAUDE.md README.md ROADMAP.md TECH-STACK.md 2>/dev/null || echo 0)
CODE_TS=$(git log -1 --format="%ct" -- src/ app/ lib/ 2>/dev/null || echo 0)
DIFF_DAYS=$(( (CODE_TS - DOC_TS) / 86400 ))
# Positive DIFF_DAYS = code newer than docs (stale)
# Only evaluate if DOC_TS > 0 (files exist in git history)
```

**Gate:**

- `PASS`: all required files present at root AND `DIFF_DAYS` < 7
- `WARN`: `ROADMAP.md` or `TECH-STACK.md` missing OR any misplaced doc OR `DIFF_DAYS` ≥ 14
- `FAIL`: `CLAUDE.md` or `README.md` missing OR `DIFF_DAYS` ≥ 28 OR registry has >5 stale `act`-status skills (exclude `plan`/`do`/`check` with null `last_manual_test` — expected pre-validation)

### Step 2.5 — Instruction file structure check

Runs after staleness check. Checks CLAUDE.md, AGENTS.md, or both (whichever are present).

**a) Line count**

```bash
for f in CLAUDE.md AGENTS.md; do
  [ -f "$f" ] && wc -l < "$f" || echo 0
done
```

- `PASS`: ≤150 lines each
- `WARN`: 151–250 lines → "Consider extracting coding patterns to `.claude/rules/`"
- `FAIL`: >250 lines → "Instruction file bloated — split into root + rules or per-package files"

Line count FAIL escalates the overall Docs gate to FAIL.

**b) Monorepo without per-package instruction files**

```bash
# Detect monorepo
is_monorepo=$([ -f pnpm-workspace.yaml ] || [ -f turbo.json ] || [ -f lerna.json ] && echo yes || echo no)
# Count packages with their own CLAUDE.md
pkg_count=$(find apps packages libs -maxdepth 2 -name "CLAUDE.md" -o -name "AGENTS.md" 2>/dev/null | wc -l)
# Count total packages
total_pkgs=$(find apps packages libs -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l)
```

- `WARN` if monorepo detected AND `pkg_count < total_pkgs / 2`
- Message: "Monorepo detected — consider per-package CLAUDE.md for packages missing one"

Monorepo check is WARN-only (advisory).

**c) Dual-file alignment**

If both `CLAUDE.md` and `AGENTS.md` exist:

```bash
# Extract ## section headers from both files
claude_headers=$(grep "^## " CLAUDE.md 2>/dev/null | sort)
agents_headers=$(grep "^## " AGENTS.md 2>/dev/null | sort)
overlap=$(comm -12 <(echo "$claude_headers") <(echo "$agents_headers") | wc -l)
total=$(echo "$claude_headers" "$agents_headers" | sort -u | wc -l)
```

- `WARN` if overlap/total > 0.30 (>30% section headers shared)
- `INFO` always: "Both CLAUDE.md and AGENTS.md present — CLAUDE.md = architecture/context, AGENTS.md = build/style"

### Step 3 — User-facing docs audit (dual mode)

Delegates to `/docs audit` which auto-detects mode from repo:

**App mode** (`app-*` repos):

- Checks `site/` exists with `astro.config.mjs`
- Reads `site/docs-registry.yaml` → counts pages by status
- Verifies staleness: code newer than docs by >30 days?
- Checks language parity: IT vs EN page count
- Checks for broken internal links


- Checks `docs/user-guide/` exists
- Reads `docs/docs-registry.yaml` if present
- Verifies staleness: code changes vs `docs/user-guide/` last update
- Reports missing essential docs (getting-started, api-reference for services)

**Gate (combined with Steps 0–2.5):**

- `PASS`: Steps 0–2.5 pass AND `/docs audit` returns PASS
- `WARN`: Steps 0–2.5 pass but `/docs audit` returns WARN (stale pages, missing EN, etc.)
- `FAIL`: Steps 0–2.5 fail OR `/docs audit` returns FAIL (required pages missing, site/ absent for app)


---

## Subcommand: `/health security`

Delegates to `/security-verify scan` (fast SAST) and `/security-verify audit` (adversarial logic review).

```
Step 1: Invoke /security-verify scan    → pattern-based SAST (seconds)
Step 2: Invoke /security-verify audit   → adversarial logic review (minutes, spawns subagent)
```

Output of each step is shown. Gate:

- `PASS`: scan clean AND audit finds no HIGH/CRITICAL
- `WARN`: scan clean but audit finds MEDIUM findings
- `FAIL`: scan finds critical/high OR audit finds HIGH/CRITICAL

When invoked from `/health full`, both steps run. When invoked from `/loop 1d /health security`, both steps run. `scan` alone is the pre-commit gate (not this subcommand).

---

## Subcommand: `/health library`

Delegates entirely to `/library`. Runs four sub-checks in sequence:

```
Invoke: /library sync   → version matrix (current project vs local source)
Invoke: /library drift  → duplication findings
Invoke: /library scan   → extraction candidates
Invoke: /library new    → repeated pattern proposals (≥3x)
```

Summarizes findings into single `Library [PASS|WARN|FAIL]` line for the health report.


---

## Subcommand: `/health releases`

Verify release integrity — tag↔changelog↔GitHub-release consistency.

Always derive owner and repo from the Forgejo push remote:

```bash
FJ_OWNER=$(echo "$FORGEJO_REMOTE" | sed 's|.*:\(.*\)/.*\.git|\1|')
FJ_REPO=$(basename "$FORGEJO_REMOTE" .git)
```


**Delegates to:** `/release verify tags`

```
Invoke: /release verify tags
```

Output is passed through verbatim. Gate inherits from `/release verify`:

- `PASS`: all tags ↔ sections match, GH/FJ releases present, all expected artifacts published
- `WARN`: missing GH or Forgejo release for a tag, OR expected artifact MISSING (publish workflow exists but package absent)
- `FAIL`: tag without section OR section without tag

---

## Subcommand: `/health ci`



**Delegates to:** `/ci-setup audit`

```
Invoke: /ci-setup audit
```

Detection check:

```bash
```

Output is collapsed into a single gate line for the consolidated report:

```
CI  [PASS]  4 workflows match template · secrets: REGISTRY_TOKEN ✓ PYPI_TOKEN ✓
CI  [WARN]  missing release.yml · REGISTRY_TOKEN absent
CI  [FAIL]  legacy unified pattern detected · REGISTRY_TOKEN missing
```

Gate thresholds:

- `PASS`: all expected workflows present, all match templates, REGISTRY_TOKEN provisioned
- `WARN`: minor drift (e.g., missing `release.yml` but quality workflows present) OR REGISTRY_TOKEN missing
- `FAIL`: legacy patterns (`old-unified-pattern`, `legacy-setup-deps`), missing security workflow, OR REGISTRY_TOKEN missing

Run `/ci-setup fix` to apply any fixes surfaced by this check.

---

## Subcommand: `/health quality`

Periodic code quality snapshot — lint, tests, coverage.

**Delegates to:**

- `/quality-check` — linting, formatting, type checking
- Test runner (auto-detected: `pytest` / `npm test` / `cargo test`)
- Coverage tool (auto-detected: `pytest --cov` / `npm test --coverage`)

**Steps:**

1. Detect project type (Python/Node/Rust) from manifest files
2. Run lint + format check (`ruff` / `eslint` / `clippy`)
3. Run fast test suite (`-m "not integration and not e2e"`) — full suite is CI's domain
4. Measure coverage (informational only locally; threshold enforced on CI)

**Gate:**

- `PASS`: 0 lint errors, all fast tests pass
- `WARN`: 1-5 lint errors OR fast tests partially failing
- `FAIL`: fast tests failing OR > 5 lint errors

**Note:** This is a periodic health snapshot. For commit-adjacent validation, use `/pre-commit` which also includes security scanning and changelog updates. Coverage >= 80% is a CI gate, not a local health gate.

---

## Subcommand: `/health techdebt`

Delegates entirely to `/techdebt`. Scans for accumulated technical debt across the codebase.

```
Invoke: /techdebt
```

**Checks delegated:**

- Duplicated code blocks (≥10 identical lines across files)
- Dead code (unused functions, unreachable branches, commented-out blocks)
- TODOs / FIXMEs / HACKs left in code
- Oversized functions (>50 lines) and files (>500 lines per code-quality.md)

Output is passed through verbatim. Gate derived from finding counts:

- `PASS`: 0 critical findings (no duplicates >20 lines, no dead code, ≤3 TODOs)
- `WARN`: 1-5 duplicate blocks OR 1-10 TODOs OR 1-3 oversized functions
- `FAIL`: >5 duplicate blocks OR >10 TODOs OR >3 oversized functions OR dead code in critical paths
- `SKIP`: No source files detected (config-only or docs-only repo)

**Note:** Tech debt TRACK findings open with `--milestone TECH-DEBT` (not BACKLOG) via `/health issues`.

---

## Subcommand: `/health deps`

Delegates entirely to `/deps scan`. Audits dependency freshness, security posture, and
decision coverage — how many outdated deps have a recorded update/defer/skip rationale.

```
Invoke: /deps scan
```

**What it checks:**

- Outdated packages (Python, Node.js, Rust, Go) — classified by semver bump severity
- CVEs and EOL packages via `pip audit` / `npm audit` / `cargo audit`
- Active decisions in Atrium — marks assessed deps, flags overdue deferred decisions

Output gate derived from `/deps scan` results:

- `PASS`: 0 critical (CVE/EOL) · 0 unassessed HIGH · all deferred decisions within review date
- `WARN`: 0 critical · unassessed HIGH/MEDIUM exist · OR ≥1 decision due within 7 days
- `FAIL`: Any CRITICAL (CVE/EOL) · OR any overdue deferred decision
- `SKIP`: No manifest files found (config-only or docs-only repo)

**Atrium offline:** Gate still works (local scan only). Decision coverage shows as `n/a`.

**Note:** When FAIL on a TRACK finding (CVE, overdue decision), open issue with `--milestone TECH-DEBT`. Patch/minor updates are FIX-NOW — bump and test inline.
Run `/deps decide` after the audit to record decisions for unassessed findings.

---

## Subcommand: `/health hygiene`

Filesystem lint — catches structural rot, gitignore gaps, orphaned artifacts, and directory drift.
This is a **native check** (no delegation — uses Glob, Grep, Bash directly).

### Check A — Gitignore hygiene

**A1 — Untracked files matching known noise patterns per detected stack:**

```bash
git ls-files --others --exclude-standard
```

Cross-reference against known noise patterns:

| Stack       | Patterns that should be in .gitignore                                            |
| ----------- | -------------------------------------------------------------------------------- |
| All         | `.DS_Store`, `Thumbs.db`, `*.swp`, `*~`, `.env`, `.env.local`, `.env.*.local`    |
| Python      | `__pycache__/`, `*.pyc`, `.venv/`, `*.egg-info/`, `dist/`, `build/`, `.coverage` |
| Node        | `node_modules/`, `.next/`, `.nuxt/`, `.output/`, `dist/`                         |
| Rust        | `target/`                                                                        |
| IDE         | `.idea/`, `.vscode/` (except shared settings), `*.code-workspace`                |
| Testing     | `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `coverage/`, `htmlcov/`        |
| Claude Code | `projects/`, `plans/`, `tasks/`, `debug/`, `history.jsonl`, `memory-index.db*`   |

Report each match with the suggested `.gitignore` line to add.

**A2 — Tracked files that match .gitignore patterns (`git rm --cached` candidates):**

```bash
git ls-files -i --exclude-standard 2>/dev/null
```

Each result is a FAIL finding with the fix command: `git rm --cached <file>`.

**A3 — Missing gitignore entries for detected stack:**

Detect stack from manifest files (`pyproject.toml` → Python, `package.json` → Node, `Cargo.toml` → Rust).
Compare required patterns (table above) against actual `.gitignore` content. Report missing as WARN.

### Check B — Orphaned and stale files

**B1 — Backup/temp files tracked:**

```bash
git ls-files | grep -E '\.(bak|tmp|orig|swp|swo)$|~$'
```

**B2 — Zero-byte tracked files** (exclude `.gitkeep`, `__init__.py`, `py.typed`):

```bash
git ls-files | while read f; do [ -f "$f" ] && [ ! -s "$f" ] && echo "$f"; done
```

**B3 — OS artifacts in tracked files:**

```bash
git ls-files | grep -E '\.DS_Store$|Thumbs\.db$|desktop\.ini$'
```

### Check C — Directory structure audit

**C1 — Parse expected structure from README tree block:**

```bash
grep -n "^├──\|^└──\|^│" README.md 2>/dev/null
```

If a tree block exists: extract directory names → build expected set.
If no tree block: skip C2 (no reference to compare against).

**C2 — Compare actual vs expected top-level dirs:**

```bash
ls -d */ 2>/dev/null | sed 's|/$||'
```

- `EXPECTED + PRESENT` → OK
- `EXPECTED + MISSING` → WARN
- `PRESENT + NOT EXPECTED` → INFO (undocumented, not necessarily wrong)

**C3 — Misplaced files:**

| Signal                                  | Check                            |
| --------------------------------------- | -------------------------------- |
| `*.py` at root when `src/` exists       | Python file may belong in `src/` |
| `*.test.*` at root when `tests/` exists | Test file may belong in `tests/` |

Root-level config files (`setup.py`, `conftest.py`, `Makefile`, `pyproject.toml`) are excluded.

### Check D — Large and binary files

**D1 — Large tracked files:**

```bash
git ls-files | while read f; do
  [ -f "$f" ] && size=$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f" 2>/dev/null)
  [ "$size" -gt 1048576 ] && echo "$f ($((size / 1048576))MB)"
done
```

- > 1MB: INFO | >10MB: WARN | >50MB: FAIL

**D2 — Binary files without LFS:**

Check tracked binaries (MIME type `application/`, `image/`, `audio/`, `video/`) against `.gitattributes`.
If `.gitattributes` has no LFS rule for the file type: WARN (small binaries in `docs/` <100KB excluded).

### Check E — Root-level clutter

**E1 — Root file count:**

```bash
git ls-files --full-name | grep -cv '/'
```

- ≤15: PASS | 16-25: INFO | >25: WARN

**E2 — Nested .git directories** (accidental submodules):

```bash
find . -name ".git" -type d -not -path "./.git" 2>/dev/null
```

If found: WARN — "nested .git detected; verify with `git submodule status`."

**E3 — Orphaned lock files** (lock without corresponding manifest):

```bash
[ -f "package-lock.json" ] && [ ! -f "package.json" ] && echo "package-lock.json"
[ -f "poetry.lock" ] && [ ! -f "pyproject.toml" ] && echo "poetry.lock"
[ -f "uv.lock" ] && [ ! -f "pyproject.toml" ] && echo "uv.lock"
[ -f "Cargo.lock" ] && [ ! -f "Cargo.toml" ] && echo "Cargo.lock"
```

### Check F — Stash audit

```bash
git stash list
```

If the stash is empty: PASS (no output).

For each stash entry, capture:

- **Index** (`stash@{N}`)
- **Branch** it was stashed from (from the `WIP on <branch>` part)
- **Message** (commit description)
- **Age** — compute from reflog: `git log -g --format="%ci" stash@{N} | head -1`

**Age classification:**

| Age       | Severity |
| --------- | -------- |
| <7 days   | INFO     |
| 7–30 days | WARN     |
| >30 days  | WARN     |

**Output (when stash non-empty):**

```
**Stash:**
- ⚠ stash@{0}: "WIP on main: fix auth" — 12 days old
- ⚠ stash@{1}: "WIP on feature/x: draft" — 45 days old
```

Any stash entry triggers at minimum WARN — a non-empty stash means forgotten work. List the `git stash show stash@{N}` command next to each entry so the user can see what's in it.

### Gate

- `PASS`: 0 WARN/FAIL findings
- `WARN`: tracked OS artifacts, missing gitignore for stack, >25 root files, >10MB file, binary without LFS, OR any stash entry
- `FAIL`: tracked file matching .gitignore, >50MB file, orphaned lock file, nested .git (non-submodule)
- `SKIP`: Not a git repository

### Output format

```
### Hygiene [PASS|WARN|FAIL]

**Gitignore:**
- ✓ .gitignore covers detected stack (Python)
- ⚠ Missing entry: `.coverage` (Python testing artifact)
- ✗ Tracked file matches .gitignore: `.DS_Store` → run: git rm --cached .DS_Store

**Orphaned files:**
- ✓ No backup/temp files tracked
- ✓ No OS artifacts tracked

**Structure:**
- ✓ 6/6 expected directories present (per README tree)
- ℹ Unexpected top-level: `commands/`, `shared/` (not in README tree — may be intentional)

**Large files:**
- ✓ No files >1MB tracked

**Root cleanliness:**
- ✓ 12 root-level files (clean)
- ✓ No nested .git directories
- ✓ No orphaned lock files

**Stash:**
- ✓ Stash is empty
```

**Note:** Hygiene TRACK findings (orphaned lock files, nested .git) open with `--milestone TECH-DEBT`. FIX-NOW hygiene items (.gitignore gaps, tracked artifacts) are fixed inline — no issue needed.

---

## Subcommand: `/health issues`

Open GitHub issues **only for TRACK findings** — findings that cannot be resolved immediately
(structural work, investigation required, multi-session effort, or delegated sub-skills).

**Never open issues for FIX-NOW findings.** Those must be fixed in-place first.

**For each TRACK finding:**

1. Format as `[BACKLOG] [P2] #NEW <finding summary>` per github-workflow.md convention
   (permanent milestones like BACKLOG, TECH-DEBT, BUG have no order suffix;
   sprint/version milestones use `|ORDER`, e.g. `[SPRINT-1|03]`)
2. Propose `gh issue create` command with `--milestone BACKLOG`, `--label enhancement`
3. Ask user to confirm **all at once** — one Y/n for the full batch, not per-finding

**Shell safety — titles with metacharacters:** Issue titles may contain `|` (from
`[MILESTONE|ORDER]` convention on sprint/version milestones). Always use **single quotes**
for `--title` values to prevent shell interpretation of `|`, `$`, backticks, and other
metacharacters. If the title itself contains a single quote, escape it as `'\''`.

**Example:**

```bash
gh issue create \
  --title '[BACKLOG] [P2] Undocumented POST /upload route' \
  --body "Found by /health endpoints on 2026-03-28. Needs API docs update." \
  --label "enhancement" \
  --milestone "BACKLOG"
```

---

## Subcommand: `/health agents`

Native check — no delegation. Scans all repos with GitHub remotes for open issues labeled `ai-suggested` (auto-created by the session analyzer nightly job).

**Steps:**

1. Discover repos: for each directory in `~/dev/*/` plus `~/.claude`, run:

   ```bash
   git -C <dir> remote get-url origin 2>/dev/null
   ```

   Extract `owner/repo` slugs via regex. Deduplicate.

2. For each repo with a GitHub remote, run:

   ```bash
   gh issue list -R owner/repo --label ai-suggested --state open \
     --json number,title,labels,createdAt \
     --jq '.[] | {number, title, createdAt, kind: ([.labels[].name] | map(select(. == "bug" or . == "tech-debt" or . == "enhancement")) | first)}'
   ```

3. Group by repo, then by kind (`bug`, `tech-debt`, `enhancement`).

4. Compute age of oldest issue per repo.

5. Print summary table:

   ```
   ### Agents [PASS|WARN|FAIL]

   | Repo                   | Bugs | Tech-Debt | Enhancements | Total | Oldest |
   |------------------------|------|-----------|--------------|-------|--------|
   | claude-dotfiles        | 8    | 2         | 1            | 11    | 5d ago |

   Total: 15 unreviewed signals across 2 repos — run `/health agents triage` to review
   ```

6. If WARN/FAIL: suggest `/health agents triage`.

**Gate:**

- `PASS`: 0 open `ai-suggested` issues
- `WARN`: 1–15 open issues across all repos
- `FAIL`: >15 open issues OR any issue older than 14 days
- `SKIP`: No GitHub remote in current repo (still runs globally from project scan)

---

## Subcommand: `/health agents triage`

Interactive triage mode. Works across all repos, not just the current one.

**Steps:**

1. Run the same repo discovery and issue query as `/health agents`.
2. For each repo with open issues, print the issue list grouped by kind.
3. For each issue (or allow batch selection), present 3 actions:
   - **Dismiss** — close as not actionable:
     ```bash
     gh issue close N -R owner/repo --comment "Dismissed during /health agents triage — not actionable or already fixed."
     ```
   - **Promote** — make it a human-owned issue (ask for target milestone: BACKLOG, BUG, SPRINT-N):
     ```bash
     gh issue edit N -R owner/repo \
       --remove-label ai-suggested \
       --milestone <chosen-milestone>
     ```
   - **Skip** — leave as-is for next triage session.

4. After all repos are processed, print updated counts.

**Key invariant:** promoting removes the `ai-suggested` label → the issue becomes human-owned and exits the agents check. Dismissing closes it. Both actions reduce the count.

---

## Subcommand: `/health branches`

Stale branch audit across local, GitHub, and Forgejo remotes. Native check — no delegation.

**Steps:**

### Step 1 — Fetch and collect branch data

```bash
# Refresh remote refs (prune deleted remote-tracking branches)
git fetch --prune origin

# Local branches merged into main
git branch --merged main | grep -v '^\*\s*main$'

# Local branches NOT merged, sorted by last commit date
git for-each-ref --sort=committerdate refs/heads/ \
  --format='%(committerdate:iso8601) %(refname:short) %(objectname:short)'

# Remote tracking branches (all remotes)
git for-each-ref --sort=committerdate refs/remotes/ \
  --format='%(committerdate:iso8601) %(refname:short)'
```

### Step 2 — Forgejo remote branches via API


```bash
fj branch list "$OWNER/$REPO"
# Raw output if needed: fj --json branch list "$OWNER/$REPO" | python3 -c "
import json, sys, datetime
now = datetime.datetime.now(datetime.timezone.utc)
for b in json.load(sys.stdin):
    name = b['name']
    if name in ('main', 'master'): continue
    ts = b['commit']['timestamp']
    dt = datetime.datetime.fromisoformat(ts.replace('Z','+00:00'))
    age_days = (now - dt).days
    print(f'{age_days:4d}d  {name}')
"
```

### Step 3 — GitHub remote branches via gh CLI

If `gh auth status` succeeds AND repo has a GitHub remote:

```bash
gh api repos/{owner}/{repo}/branches --paginate \
  --jq '.[] | select(.name | test("^(main|master)$") | not) |
        [.name, .commit.commit.committer.date] | @tsv'
```

Correlate with open PRs: branches with an open PR are **not stale** regardless of age.

```bash
gh pr list --state open --json headRefName --jq '.[].headRefName'
```

### Step 4 — Classify findings

| Category                      | Condition                                   | Severity                 |
| ----------------------------- | ------------------------------------------- | ------------------------ |
| Local merged                  | Branch already merged into main             | FIX-NOW (safe to delete) |
| Local stale                   | Unmerged, no commit in >30 days, no open PR | WARN                     |
| Local stale                   | Unmerged, no commit in >60 days, no open PR | FAIL                     |
| Remote stale (GitHub/Forgejo) | No commit in >30 days, no open PR           | WARN                     |
| Remote stale (GitHub/Forgejo) | No commit in >60 days, no open PR           | FAIL                     |

Branches with an associated open PR on either forge are **excluded** from stale classification.
Branch `main` and `master` are always excluded.

### Step 5 — Suggest cleanup commands

For each FIX-NOW finding, print the exact delete command (do NOT run it — user confirms):

```bash
# Local merged branch
git branch -d <branch-name>

# Remote branch on GitHub
git push origin --delete <branch-name>

# Remote branch on Forgejo (via API — no direct git push since Forgejo is push-only remote)
fj branch delete {owner}/{repo} {branch}
```

**Gate:**

- `PASS`: No stale branches anywhere
- `WARN`: ≥1 local merged branch OR ≥1 remote stale >30 days
- `FAIL`: ≥1 branch stale >60 days on any remote
- `SKIP`: Not a git repo, or bare repo with no branches

---

## Subcommand: `/health website`

Conditional dimension — only runs if the project is a website. Also user-invokable directly: `/health website`.

**Detection** (check in order, use first match):

| Stack           | Marker                                                                           | baseURL extraction                          |
| --------------- | -------------------------------------------------------------------------------- | ------------------------------------------- |
| Astro Starlight | `astro.config.mjs` or `astro.config.ts` + `@astrojs/starlight` in `package.json` | `site:` field in astro config or `SITE` env |
| Astro           | `astro.config.mjs` or `astro.config.ts`                                          | `site:` field in astro config or `SITE` env |
| Hugo            | `hugo.toml` or `config.toml` with `baseURL`                                      | `baseURL` value                             |
| Netlify         | `netlify.toml`                                                                   | from underlying framework config            |
| Next.js         | `next.config.js` or `next.config.ts`                                             | `NEXT_PUBLIC_SITE_URL` env or localhost     |
| Gatsby          | `gatsby-config.js` with `siteMetadata.siteUrl`                                   | `siteUrl` value                             |
| Generic         | `package.json` with `homepage`                                                   | `homepage` value                            |

**Astro Starlight note:** When detected, pass `--stack astro-starlight` to `/website-health` so it can apply docs-site specific checks (sidebar nav, search index, versioned docs, translation completeness).

If no marker found: skip dimension (report `[SKIP] No website project detected`).

**Delegates to:** `/website-health <baseURL>` — invokes the quick summary mode (all 7 dimensions, L1 depth).

**Output normalization:** Extract the overall gate (PASS/WARN/FAIL) and one-line status from `/website-health` output. Collapse into the standard health report format:

```
Website  [PASS|WARN|FAIL]  <one-line summary from /website-health>
```

**Gate:**

- Inherits from `/website-health` overall gate (PASS/WARN/FAIL)

---

## Subcommand: `/health docker`

Conditional check — **delegates to `/docker-audit`**. Skipped if no Docker files are detected.

**Detection:**

```bash
# Check for any Docker-related files
find . -maxdepth 3 \
  \( -name "Dockerfile" -o -name "Dockerfile.*" -o \
     -name "compose.yaml" -o -name "compose.yml" -o \
     -name "docker-compose.yml" -o -name "docker-compose.yaml" \) \
  -not -path "./.git/*" \
  -not -path "./node_modules/*" \
  | head -10
```

If no files found: report `[SKIP] No Docker files detected` — stop here.

**Delegates to:** `/docker-audit [path]` — runs the full 10-category audit plus Compose checklist.

**Output normalization:** Extract the overall score and CRITICAL/HIGH/MEDIUM/LOW counts from `/docker-audit` output. Collapse into standard health format:

```
Docker  [PASS|WARN|FAIL]  <N> files · <score>/10 categories · <k> critical, <n> high findings
```

**Gate:**

- `PASS`: 0 critical, 0 high findings
- `WARN`: any HIGH finding (non-root user, no HEALTHCHECK, `:latest` tag, no `.dockerignore`)
- `FAIL`: any CRITICAL finding (secrets in Dockerfile ENV/ARG/COPY, root user with privileged port exposure)
- `SKIP`: no Docker files found

---

## Subcommand: `/health roadmap`

Bidirectional sync between `ROADMAP.md`, GitHub Issues, and `CHANGELOG.md`.
Ensures roadmap items have corresponding issues and issues are reflected in the roadmap.

**Prerequisites:** GitHub CLI authenticated (`gh auth status`). Roadmap check is skipped (SKIP) if no GitHub remote is detected.

### Step 1 — Parse ROADMAP.md

If `ROADMAP.md` is absent: report `[SKIP]` with note "run /documentation-updater to create ROADMAP.md first."

Parse sections looking for:

- Version headings: `## v1.2.0`, `## Unreleased`, `## Planned`, `## In Progress`, `## Released`
- Feature lines: any `- `, `* ` bullet OR item with `#N` issue reference
- Extract: (item text, version/section, issue ref if present)

```bash
# Extract headings and items from ROADMAP.md
grep -n "^#\|^- \|^* " ROADMAP.md
```

### Step 2 — Fetch GitHub Issues and Milestones

```bash
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)

# Existing milestones (open + closed)
gh api "repos/$REPO/milestones?state=all&per_page=100" \
  --jq '.[] | {number: .number, title: .title, state: .state, open_issues: .open_issues, closed_issues: .closed_issues}'

# Open issues with milestones
gh api "repos/$REPO/issues?state=open&per_page=100" \
  --jq '.[] | select(.pull_request == null) | {number: .number, title: .title, milestone: .milestone.title, labels: [.labels[].name]}'

# Recently closed issues (last 90 days — may already be shipped)
gh api "repos/$REPO/issues?state=closed&per_page=50" \
  --jq '.[] | select(.pull_request == null) | {number: .number, title: .title, closed_at: .closed_at}'
```

Build a **milestone map**: `{ roadmap_section_title → github_milestone_number_or_null }` by matching ROADMAP.md section headings (`## v1.2.0`, `## Q2 2026`, etc.) against existing GitHub milestone titles (case-insensitive, strip `##` prefix and trim).

For each section heading in ROADMAP.md that is NOT in BACKLOG/BUG/TECH-DEBT/Unreleased/Released **and** matches a versioning/sprint pattern (`vX.Y.Z`, `SPRINT-N`, `QN YYYY`, or `SPRINT-N-feature`): note whether the milestone exists in GitHub or is `MISSING`.

Skip sections that do not match these patterns (e.g., `## Ideas for v2`, `## Parking Lot`, `## In Progress`) — these are informational headings, not actionable milestones.

### Step 3 — Map roadmap items → issues

For each roadmap item:

1. Check if it contains an explicit `#N` reference → verify that issue exists
2. If no explicit ref: fuzzy-match title against open issues (≥60% word overlap)
3. Classify as:
   - `LINKED` — has verified issue reference
   - `FUZZY_MATCH` — probable match found (show candidate)
   - `ORPHANED` — no issue found

### Step 4 — Find orphaned roadmap items → create milestones + issues + write back

#### Step 4a — Create missing milestones

For each ROADMAP.md section that has `MISSING` milestone in GitHub (from Step 2 milestone map), print the proposed creation:

```
⚠ ROADMAP section has no GitHub Milestone:
  Section: ## v1.3.0
  Action:  gh api repos/$REPO/milestones --method POST -f title="v1.3.0"
```

After listing all missing milestones, ask **once**: "Create all N milestones on GitHub? [Y/n]"

**If confirmed:** run each `gh api` call and update the milestone map with the newly created milestone numbers. Report:

```
✓ Created milestone "v1.3.0" (#5 on GitHub)
```

**Priority inference for issues:** determine milestone from the roadmap section the item belongs to:

- Section `## v1.X.Y` or `## SPRINT-N` → use that milestone title
- Section `## Planned` or `## In Progress` (no version) → use `BACKLOG`
- Section `## Unreleased` → use `BACKLOG`

#### Step 4b — Create issues for orphaned items

For each `ORPHANED` item in "Planned", "In Progress", or versioned sections, print the proposed command using the **correct milestone** (not hardcoded BACKLOG):

```
⚠ ROADMAP item has no GitHub Issue:
  Section: ## v1.3.0  →  milestone: v1.3.0
  Item:    "Add multi-tenant support"
  Action:  gh issue create \
             --title '[v1.3.0|05] [P2] Add multi-tenant support' \
             --body "From ROADMAP.md ## v1.3.0. No existing issue found." \
             --label "enhancement" \
             --milestone "v1.3.0"
```

Title prefix follows `[MILESTONE|ORDER]` convention from `github-workflow.md`.
**Shell safety:** Always use **single quotes** for `--title` values — titles with `|` (e.g.
`[v1.3.0|05]`) will break the shell if double-quoted or unquoted.

After listing all orphaned items, ask **once**: "Create all N issues and update ROADMAP.md? [Y/n]"

**If confirmed (Y or Enter):**

1. For each orphaned item, run the `gh issue create` command and capture the returned issue URL/number:

   ```bash
   ISSUE_URL=$(gh issue create \
     --title '[v1.3.0|05] [P2] Add multi-tenant support' \
     --body "From ROADMAP.md ## v1.3.0. No existing issue found." \
     --label "enhancement" --milestone "v1.3.0")
   ISSUE_NUM=$(echo "$ISSUE_URL" | grep -o '[0-9]*$')
   ```

2. Immediately update `ROADMAP.md` — append `#N` to the matching item line:

   ```
   Before: - Add multi-tenant support
   After:  - Add multi-tenant support #42
   ```

   Use direct file edit, matching the exact item text.

3. Report each update:
   ```
   ✓ Created #42 "Add multi-tenant support" (milestone: v1.3.0) → ROADMAP.md updated
   ```

**If skipped (n):** list the commands for manual execution and note that ROADMAP.md was not updated.

### Step 5 — Find GitHub Issues not in roadmap → write back

For each open issue with a milestone (excluding BACKLOG/BUG/TECH-DEBT):

1. Check if it appears in ROADMAP.md (by `#N` ref or fuzzy title match)
2. If not present: flag as `MISSING_FROM_ROADMAP`

```
⚠ Issue not reflected in ROADMAP.md:
  #42 "OAuth2 integration" (milestone: v1.2.0)
  Suggest adding to ROADMAP.md under ## v1.2.0
```

List all missing items with proposed markdown snippet for ROADMAP.md.

After listing, ask **once**: "Add all N missing issues to ROADMAP.md? [Y/n]"

**If confirmed (Y or Enter):**

For each `MISSING_FROM_ROADMAP` issue, insert a new bullet under the matching version/milestone section in ROADMAP.md:

```
- <issue title> #N
```

If the section doesn't exist yet, create it (e.g., `## v1.2.0`) immediately before the first lower version or at the end of the planned area.

Report:

```
✓ Added #42 "OAuth2 integration" under ## v1.2.0 in ROADMAP.md
```

**If skipped (n):** print the snippets for manual insertion.

**After all write-backs (Steps 4 and 5):** if ROADMAP.md was modified, note that the file should be committed — suggest `/ship` or a quick `git add ROADMAP.md`.

### Step 6 — CHANGELOG reconciliation

Cross-check `CHANGELOG.md [Unreleased]` against ROADMAP.md "Planned" items:

1. Items that appear in CHANGELOG [Unreleased] AND in ROADMAP Planned → flag as `SHIPPED_BUT_PLANNED`
   - These should move from "Planned" to "Released" (or be removed from Planned)
2. Items in CHANGELOG released sections (tagged versions) that still appear in ROADMAP Planned → same flag

```
⚠ SHIPPED items still listed as Planned in ROADMAP.md:
  "Add structured logging" — in CHANGELOG v1.1.0 but still in ROADMAP ## Planned
  Suggest: move to ## Released or remove from Planned.
```

### Step 7 — Next version proposal

Based on milestone completion state:

```bash
# Get milestone progress
gh api "repos/$REPO/milestones" \
  --jq '.[] | select(.state=="open") | "\(.title): \(.closed_issues)/\(.open_issues + .closed_issues) closed (\((.closed_issues * 100 / (.open_issues + .closed_issues + 0.001)) | floor)%)"'
```

For any milestone ≥80% closed: propose adding/updating a version section in ROADMAP.md with the remaining open issues.
For milestones ≥95% closed: suggest bumping to "In Progress" or flagging for imminent release via `/release plan`.

**Gate:**

- `PASS`: all roadmap items linked to issues AND no CHANGELOG reconciliation issues
- `WARN`: ≥1 orphaned roadmap items OR ≥1 missing-from-roadmap issues OR ≥1 SHIPPED_BUT_PLANNED items
- `FAIL`: ROADMAP.md present but >50% of Planned items are orphaned (roadmap is effectively disconnected from issues)
- `SKIP`: ROADMAP.md absent OR no GitHub remote

---

## Subcommand: `/health license`

Audit the `LICENSE` file at project root. If absent, run interactive advisor to recommend the right license.

### Step 1 — Detection

```bash
# Check for common license file names (case-insensitive)
ls LICENSE LICENSE.md LICENSE.txt COPYING COPYING.md 2>/dev/null | head -1
```

If found: parse and identify the license type (MIT, Apache-2.0, GPL-3.0, etc.) and report `[PASS]`.

**Parse logic:**

- Check first line or SPDX header for identifier: `SPDX-License-Identifier: MIT`
- Fallback: keyword match on first 5 lines ("MIT License", "Apache License", "GNU GENERAL PUBLIC LICENSE", etc.)
- If unrecognizable: report `[WARN] License file present but type unknown — verify SPDX identifier`

**Apache 2.0 — NOTICE file check:**

Apache 2.0 does not embed the copyright holder inside `LICENSE` (it's a generic text). The owner is declared in a separate `NOTICE` file. When Apache 2.0 is detected:

```bash
ls NOTICE 2>/dev/null || echo "missing"
```

- `NOTICE` present with copyright line → `PASS`
- `NOTICE` absent → `WARN: Apache-2.0 detected but no NOTICE file found — add NOTICE with "Copyright <year> <holder>"`

Suggest creating: `echo "Copyright $(date +%Y) $(git config user.name)" > NOTICE`

### Step 2 — Advisor mode (LICENSE absent)

Ask 5 questions to recommend the best license. Present as a numbered menu each time.

**Q1 — Project type:**

```
1. Open source library (others will import/depend on it)
2. Open source application (end users run it)
3. Internal / proprietary (not publicly distributed)
4. Commercial SaaS (hosted service, not distributed)
```

**Q2 — Copyleft preference:**

```
1. Permissive — anyone can use, including in proprietary products (MIT, Apache, BSD)
2. Weak copyleft — modifications must stay open, but linking is fine (LGPL, MPL)
3. Strong copyleft — derivative works must also be open source (GPL, AGPL)
4. Network copyleft — copyleft applies even to SaaS use (AGPL)
```

**Q3 — Patent clause:**

```
1. Yes — include explicit patent grant (Apache-2.0, GPL-3.0)
2. No — no explicit patents (MIT, BSD)
3. Don't know — recommend based on other answers
```

**Q4 — Attribution requirement:**

```
1. Must preserve copyright notice and attribution (all major licenses do this)
2. Cannot use my name/brand in derived products (BSD 3-Clause, Apache)
3. Minimal — just keep the license text (MIT)
```

**Q5 — Compatibility requirements:**

```
1. Must be compatible with GPL (MIT, Apache-2.0, LGPL)
2. Must be compatible with Apache-2.0 (MIT, BSD, Apache)
3. No specific compatibility requirement
```

### Step 3 — License recommendation matrix

Based on answers, output one of:

| Scenario                          | Recommended                        | Why                                                             |
| --------------------------------- | ---------------------------------- | --------------------------------------------------------------- |
| Library, permissive, patent grant | **Apache-2.0**                     | Permissive + patent protection, industry standard for libraries |
| Library, permissive, minimal      | **MIT**                            | Simplest, most permissive, widely understood                    |
| Library, weak copyleft            | **MPL-2.0**                        | File-level copyleft, allows proprietary linking                 |
| App, strong copyleft              | **GPL-3.0**                        | Forces derivative works open, patent grant                      |
| App/SaaS, network copyleft        | **AGPL-3.0**                       | Closes SaaS loophole, requires source even for hosted use       |
| Internal/proprietary              | **All Rights Reserved**            | No distribution rights, explicit copyright notice only          |
| Commercial SaaS w/ open core      | **Apache-2.0 + commercial addons** | Open core model                                                 |
| BSD variant needed                | **BSD-3-Clause**                   | MIT-like + no-endorsement clause                                |

After recommendation, offer to:

1. Fetch the full license text and write `LICENSE` file (with current year + copyright holder)
2. Show the SPDX identifier to add to `pyproject.toml` / `package.json`

```bash
# Detect copyright holder from git config
git config user.name
git config user.email
```

**Gate:**

- `PASS`: LICENSE file present and type identified
- `WARN`: LICENSE file present but type unrecognizable
- `FAIL`: No LICENSE file AND this is a public repository (`gh repo view --json isPrivate --jq '.isPrivate'` = false)
- `INFO` (not gated): No LICENSE file on a private repo (common for proprietary/internal work) — still suggest running advisor

---

## Fix-vs-Issue Decision Matrix

Apply this matrix during `/health full` step 16 triage. Every WARN/FAIL finding is either
`FIX-NOW` (apply immediately in this session) or `TRACK` (open a GitHub issue for future work).

**FIX-NOW criteria:** single-file change, no design decisions required, reversible, takes < 5 min.
**TRACK criteria:** investigation needed, multi-file structural work, external dependencies, or
requires a design decision before acting.

| Dimension | Finding                                                 | Class   | How to fix                                    |
| --------- | ------------------------------------------------------- | ------- | --------------------------------------------- |
| Versions  | README badge mismatch                                   | FIX-NOW | Update badge string in README                 |
| Versions  | Cross-manifest mismatch (single bump)                   | FIX-NOW | Bump the lagging file                         |
| Versions  | Cross-manifest mismatch (breaking change)               | TRACK   | Requires version strategy                     |
| Hygiene   | Artifact not in .gitignore (.coverage, .DS_Store, etc.) | FIX-NOW | Append to .gitignore                          |
| Hygiene   | Tracked file that matches .gitignore                    | FIX-NOW | `git rm --cached <file>`                      |
| Hygiene   | Root clutter (>25 files, unexpected dirs)               | FIX-NOW | Move or delete offenders                      |
| Hygiene   | Orphaned lock file                                      | TRACK   | Needs investigation                           |
| Hygiene   | Non-empty stash (<7 days)                               | FIX-NOW | Review with `git stash show` and pop or drop  |
| Hygiene   | Non-empty stash (≥7 days old)                           | TRACK   | Old stash likely forgotten — review and clear |
| Docs      | ROADMAP.md missing                                      | FIX-NOW | Create skeleton file                          |
| Docs      | TECH-STACK.md missing                                   | FIX-NOW | Create skeleton file                          |
| Docs      | LICENSE missing (private repo)                          | FIX-NOW | Add standard LICENSE                          |
| Docs      | Stale docs (code updated, docs not)                     | TRACK   | Requires actual writing                       |
| Docs      | CLAUDE.md / README missing                              | TRACK   | Requires content decisions                    |
| Endpoints | Undocumented non-mutating route                         | TRACK   | Add docs                                      |
| Endpoints | Undocumented POST/PUT/DELETE                            | TRACK   | High priority — add docs                      |
| Security  | Any CRITICAL/HIGH finding                               | TRACK   | Investigate before touching                   |
| Security  | LOW/INFO false positive (e.g., B101 in tests)           | FIX-NOW | Add `# nosec` annotation                      |
| Quality   | Lint errors (auto-fixable, e.g. `ruff --fix`)           | FIX-NOW | Run the linter's auto-fix                     |
| Quality   | Tests failing                                           | TRACK   | Needs root cause investigation                |
| Quality   | Coverage below threshold                                | TRACK   | Needs test writing                            |
| Tech Debt | TODOs / FIXMEs                                          | TRACK   | Can't resolve in health run                   |
| Tech Debt | Oversized functions                                     | TRACK   | Refactor work                                 |
| Deps      | Patch/minor update available                            | FIX-NOW | Bump version, run tests                       |
| Deps      | CRITICAL/HIGH CVE                                       | TRACK   | Needs investigation                           |
| Library   | Extraction candidate                                    | TRACK   | Design decision required                      |
| Roadmap   | Released section not updated (version missing)          | FIX-NOW | Add entry to `## Released` section in ROADMAP |
| Releases  | Missing GH release for a tag                            | FIX-NOW | `gh release create <tag>`                     |
| Releases  | Missing Forgejo release for a tag                       | FIX-NOW | Create via Forgejo API                        |
| Releases  | Artifact MISSING (publish workflow exists, no package)  | FIX-NOW | Re-run publish workflow or push manually      |
| Releases  | Artifact SKIP(pre-registry) (tag predates first pub)    | TRACK   | Decide whether to backfill or document gap    |
| Releases  | Tag↔changelog mismatch                                  | TRACK   | Requires changelog work                       |
| CI        | Missing security/release workflow                       | FIX-NOW | `/ci-setup fix` copies from template          |
| CI        | Minor template drift (whitespace, comments)             | FIX-NOW | `/ci-setup fix` re-copies file                |
| CI        | Legacy unified pattern (quality+tests in one file)      | TRACK   | May have intentional customizations           |
| CI        | GH_PAT missing                                          | TRACK   | Manual web UI action — WAF blocks API         |
| Branches  | Local merged branch                                     | FIX-NOW | `git branch -d <name>`                        |
| Branches  | Remote stale >30 days, no open PR                       | FIX-NOW | Delete via `git push --delete` or Forgejo API |
| Branches  | Remote stale >60 days, no open PR                       | TRACK   | Confirm intent before deleting                |

**When in doubt:** if you can write the fix in this response without asking a question, it's FIX-NOW.
If you'd need to ask "what should this say?" or "is this intentional?", it's TRACK.

---

## Subcommand: `/health full`

Runs all checks in sequence, then triages findings via the Fix-vs-Issue Decision Matrix.

**Execution order:**

1. `/health endpoints`
2. `/health versions`
3. `/health docs` (includes LICENSE existence check — WARN if absent)
4. `/health license` (advisor mode — only if LICENSE absent from Step 3; otherwise PASS)
5. `/health roadmap` (bidirectional sync — SKIP if no GitHub remote or ROADMAP.md absent)
6. `/health security`
7. `/health quality`
8. `/health techdebt` (SKIP on config-only or docs-only repos)
9. `/health deps` (SKIP if no manifest files found)
10. `/health hygiene` (filesystem lint — SKIP if not a git repo)
11. `/health library`
12. `/health releases`
14. `/health docker` (conditional — only if `Dockerfile*`, `compose.yaml`, or `docker-compose*.yml` found)
15. `/health website` (conditional — only if website project detected)
16. `/health agents` (cross-repo scan for unreviewed `ai-suggested` issues)
17. `/health branches` (stale branch audit — local, GitHub, Forgejo — SKIP if not a git repo)
18. Print consolidated report with Overall gate
19. Triage all WARN/FAIL findings using the **Fix-vs-Issue Decision Matrix** below:
    - Collect all FIX-NOW findings → print list → ask once: "Apply all N fixes now? [Y/n]"
    - If yes: apply fixes on a `fix/health-audit-<date>` branch (see post-audit commit protocol)
    - Collect remaining TRACK findings → ask once: "Open GitHub issues for these M findings? [Y/n]"
    - Do NOT default to issue creation for FIX-NOW findings. Fix them.

**Post-audit commit protocol:**

Any fixes applied during or after the audit (doc creation, file moves, version bumps, etc.) MUST be committed via a branch, not directly to main:

```bash
git checkout -b fix/health-audit-<date>   # e.g. fix/health-audit-2026-03-14
# apply fixes...
/pre-commit    # full validation pipeline
/ship          # commit + push + PR creation
```

Always suggest this branch+PR flow before touching any files. Never commit health fixes directly to main.
Exception: if already on a feature/fix branch, continue on that branch.

---

## Output Format

All subcommands use this uniform structure:

```
## Health Report — <project> — <date>

### <Dimension> [PASS|WARN|FAIL]
- ✓ <passing finding>
- ⚠ <warning finding>
- ✗ <failing finding>
```

**Overall gate:** FAIL if any dimension is FAIL. WARN if any is WARN. PASS only if all pass.

---

## Thresholds

| Dimension | WARN threshold                                                                                                     | FAIL threshold                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Endpoints | any undocumented non-mutating                                                                                      | any undocumented POST/PUT/DELETE                                                                                        |
| Versions  | README badge differs                                                                                               | cross-manifest mismatch                                                                                                 |
| Docs      | ROADMAP/TECH-STACK/LICENSE missing OR misplaced doc OR >2 weeks stale                                              | CLAUDE.md/README missing OR >4 weeks stale OR >5 stale `act`-status registry skills (null `plan`/`do`/`check` excluded) |
| License   | LICENSE present but type unrecognizable                                                                            | LICENSE absent on a public repo                                                                                         |
| Roadmap   | ≥1 orphaned roadmap item OR ≥1 issue missing from roadmap OR ≥1 SHIPPED_BUT_PLANNED item                           | >50% of Planned items are orphaned (roadmap disconnected from issues)                                                   |
| Security  | (inherits from /security-verify)                                                                                   | (inherits from /security-verify)                                                                                        |
| Quality   | 1-5 lint errors OR coverage 60-79%                                                                                 | tests failing OR coverage < 60% OR > 5 lint errors                                                                      |
| Tech Debt | 1-5 duplicate blocks OR 1-10 TODOs OR 1-3 oversized functions                                                      | >5 duplicates OR >10 TODOs OR dead code in critical paths                                                               |
| Deps      | unassessed HIGH/MEDIUM deps exist OR ≥1 deferred decision due within 7 days                                        | any CRITICAL dep (CVE/EOL) OR any overdue deferred decision                                                             |
| Hygiene   | tracked OS artifacts, missing gitignore for stack, >25 root files, >10MB file, binary without LFS, any stash entry | tracked file matching .gitignore, >50MB file, orphaned lock file, nested .git (non-submodule)                           |
| Releases  | missing GH release for a tag                                                                                       | tag↔changelog section mismatch                                                                                          |
| CI        | minor drift (missing `release.yml`) OR `REGISTRY_TOKEN` missing                                                    | legacy patterns (`old-unified-pattern`, `legacy-setup-deps`) OR missing security workflow OR `REGISTRY_TOKEN` missing   |
| Docker    | any HIGH finding (non-root USER, no HEALTHCHECK, no .dockerignore, `:latest` tag)                                  | any CRITICAL finding (secrets in Dockerfile/ARG/ENV, root user with privileged ports)                                   |
| Website   | (inherits from /website-health)                                                                                    | (inherits from /website-health)                                                                                         |
| Agents    | 1–15 open `ai-suggested` issues across all repos                                                                   | >15 open issues OR any `ai-suggested` issue older than 14 days                                                          |
| Branches  | ≥1 local merged branch OR ≥1 remote stale >30 days (no open PR)                                                    | ≥1 branch stale >60 days on any remote (local or GitHub or Forgejo)                                                     |
