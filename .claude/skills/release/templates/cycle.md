# Release Full — Orchestrator

Orchestrates the full pre-release sequence: scope the version, audit health, fix blockers, write docs for the new version, then tag and ship.

**Assumes code is done.** This skill is not for implementing features — call it when the work is in main/branch and you need to close out a release.

## When to Use

- Milestone is complete (or nearly complete) and you're ready to ship
- You want a structured gate before tagging
- Docs have drifted and need updating for the release
- "Let's release what we have"

## Phase Order

Phases run **sequentially**. Order is non-negotiable:

```
Phase 1: /release plan  → scope the version, create milestone
Phase 2: /health full   → audit, classify: blocker vs track
Phase 3: fix blockers   → auto-fix trivial, pause on ambiguous
Phase 4: /docs full     → docs written for the new version
Phase 5: tag + ship     → changelog, pre-commit, tag, push, verify
```

Why this order: docs must reference the version being released (Phase 1 determines it). Health must run before docs so FIX-NOW items don't invalidate the docs just written. `/pre-commit` runs twice — after Phase 3 and after Phase 4 — to ensure both fixes and docs are clean.

---

## Phase 1: Release Plan

**Delegate to `/release plan`.** When it completes, extract and record:

- `VERSION_TARGET` — the version we're shipping (e.g., `0.5.0`)
- `MILESTONE_NAME` — the GitHub milestone (e.g., `v0.5.0`)
- `FLOW_TYPE` — `trunk-based` or `release-branch` (depends on `staging.yml` presence)
- `UNRELEASED_FEATURES` — list of features from CHANGELOG [Unreleased] that will become this version

If `/release plan` finds a **version gap** (pyproject.toml version ≠ last git tag, or CHANGELOG section exists without a tag), surface this explicitly before proceeding:

```
VERSION GAP DETECTED
=====================
pyproject.toml:  0.4.0
Last git tag:    v0.3.1
CHANGELOG:       [0.4.0] section exists (dated YYYY-MM-DD), no tag

Options:
A) Tag v0.4.0 retroactively at the commit that matches [0.4.0] scope,
   then plan vX.Y.Z for [Unreleased]
B) Skip retroactive tag; fold [0.4.0] into [Unreleased] and release as vX.Y.Z

Recommendation: Option A (preserves historical record, cleaner CHANGELOG)
```

Ask user to choose before continuing.

**Phase 1 output for handoff:**

```
VERSION_TARGET: X.Y.Z
MILESTONE_NAME: vX.Y.Z
FLOW_TYPE: trunk-based | release-branch
UNRELEASED_FEATURES: [list from CHANGELOG]
RETROACTIVE_TAG: vA.B.C at SHA (if version gap — may be null)
```

---

## Phase 2: Health Audit

**Delegate to `/health full`.**

Run all dimensions. Internally `/health full` already parallelizes across dimensions (endpoints, versions, docs, security, quality, techdebt, hygiene, releases, ci, docker, branches).

After the audit report, **classify every finding**:

### BLOCKER — must fix before tagging

- Version string inconsistency (pyproject.toml ≠ README badge ≠ planned tag)
- Failing tests
- Critical/high security findings (bandit, pip-audit)
- Missing LICENSE file (decision required)
- Broken CI workflow that would fail on tag push

### FIX-NOW — fix before docs (auto-fixable)

- `ruff format` violations → `ruff format .`
- gitignore gaps for common artifacts (`.coverage`, `__pycache__`, `.mypy_cache`, `*.egg-info`)
- Stale merged local branches
- pyproject.toml version bump to `VERSION_TARGET`
- README version badge mismatch → update to `VERSION_TARGET`

### TRACK — create GitHub issue, do not block release

- Missing test coverage threshold configuration
- Security tools not in CI (bandit, pip-audit)
- Architectural tech debt
- Missing tests for non-critical paths
- `WARN`-level findings with no immediate impact

**Phase 2 output for handoff:**

```
HEALTH_PASS: true | false
BLOCKERS: [list of items that block tagging]
FIX_NOW: [list of auto-fixable items]
TRACK: [list of items to create issues for]
```

---

## Phase 3: Fix Blockers

### Auto-fix (no user prompt)

Run these in parallel subagents when independent:

```bash
# Format
uv run ruff format .

# gitignore audit — add missing entries
grep -q "^\.coverage$" .gitignore || echo ".coverage" >> .gitignore
grep -q "^\.mypy_cache" .gitignore || echo ".mypy_cache/" >> .gitignore
grep -q "^__pycache__" .gitignore || echo "__pycache__/" >> .gitignore

# Stale local branches (merged)
git branch --merged main | grep -vE "^\*|main$" | xargs -r git branch -d

# Version bump pyproject.toml to VERSION_TARGET
# (use Edit tool — do NOT sed)

# README badge version update
# (use Edit tool on README.md)
```

### Pause for user decision

For each BLOCKER that isn't auto-fixable, present clearly:

```
BLOCKER: Missing LICENSE file
---------------------------------
No LICENSE file detected at project root.
Options:
  A) MIT
  B) Apache 2.0
  C) Proprietary (UNLICENSED in pyproject.toml)
  D) Skip — create GitHub issue and defer

What should we do?
```

For security findings:

```
BLOCKER: bandit found N HIGH severity issues
---------------------------------
[description of each finding with file:line]

Options:
  A) Fix now (I'll implement the fixes)
  B) Add nosec comments with justification
  C) Create GitHub issues, defer, and continue release
  D) Stop release cycle — scope too large
```

Do NOT proceed to Phase 4 until all BLOCKERs are resolved or explicitly deferred.

After all fixes: run `/pre-commit` **(first run)**. Fix any failures before continuing.

### TRACK items

For each TRACK item, create a GitHub issue:

```bash
gh issue create \
  --title "[TECH-DEBT|XX] [P3] fix: <finding title>" \
  --body "<health audit finding details>" \
  --milestone "TECH-DEBT" \
  --label "enhancement"
```

### Release Readiness Ceremony

**Mandatory gate before Phase 4.** Always display this summary, even when all findings are clean.
Do not skip it. This is the moment the user sees the full unresolved picture before committing to docs and tagging.

Print a structured report in this format:

```
╔══════════════════════════════════════════════════════╗
║   RELEASE READINESS — vVERSION_TARGET                ║
╚══════════════════════════════════════════════════════╝

✅ FIXED (N items)
  • ruff format violations — fixed inline
  • pyproject.toml bumped to VERSION_TARGET
  • stale branches deleted: feature/foo, feature/bar

⚠️  DEFERRED BLOCKERS (N items) — release will proceed with these open
  • [#42] Missing LICENSE file — deferred by user (create after release)
  • [#43] bandit HIGH: subprocess shell=True — deferred (fix in v0.6.0)

📋 TRACKED AS ISSUES (N items)
  • [#44] No coverage threshold configured (TECH-DEBT, P3)
  • [#45] bandit and pip-audit not in CI (TECH-DEBT, P3)
  • [#46] Missing tests for social_verification edge cases (TECH-DEBT, P3)

🔴 UNRESOLVED / NEEDS ACTION (N items)
  • CRITICAL: 2 failing tests — must fix before proceeding
    → Proposed action: run `uv run pytest -x` to locate, then /fix
  • HIGH: pip-audit found 1 known CVE in dependency X==1.2.3
    → Proposed action: `uv add X>=1.2.4` or defer with issue
  • WARN: README endpoints table has N undocumented routes
    → Proposed action: Phase 4 (/docs) will address this

─────────────────────────────────────────────────────
Proceed to Phase 4 (docs)?  [Y = proceed / N = stop here]
```

Rules:

- If **UNRESOLVED / NEEDS ACTION** contains any CRITICAL items: the user must explicitly confirm `Y` to proceed.
- If only WARN/INFO items remain: still display them, but default recommendation is to proceed.
- Items in ✅ FIXED are purely informational.
- Items in 📋 TRACKED have GitHub issue numbers already created — no further action needed.
- Items in ⚠️ DEFERRED have issue numbers and explicit user consent to defer.
- The 🔴 section must include a concrete **Proposed action** for each item.

**Phase 3 output for handoff:**

```
FIXES_APPLIED: [list]
BLOCKERS_RESOLVED: [list]
BLOCKERS_DEFERRED: [list with issue numbers]
ISSUES_CREATED: [list of issue numbers]
UNRESOLVED_CRITICAL: [list — empty = safe to proceed]
PRE_COMMIT_PASS: true | false
CEREMONY_APPROVED: true | false
```

---

## Phase 4: Docs (Version-Aware)

**Delegate to `/docs full`**, but pass version context.

Before invoking `/docs full`, set context:

```
Preparing docs for release VERSION_TARGET.
Features being released:
UNRELEASED_FEATURES (from Phase 1)

Docs must:
- Reference version VERSION_TARGET where versions appear
- Cover all features in UNRELEASED_FEATURES
- Not document unreleased/speculative features
```

`/docs full` internally runs: scaffold → features extraction → audit → create missing → review-drafts.

Review-drafts agents are instructed to verify content against:

1. The features in UNRELEASED_FEATURES (not all historical features)
2. The actual source code in the current branch
3. The version number `VERSION_TARGET`

After `/docs full` completes: run `/pre-commit` **(second run)**. Fix any failures before continuing.

**Phase 4 output for handoff:**

```
DOCS_CREATED: [list of new pages]
DOCS_UPDATED: [list of updated pages]
PRE_COMMIT_PASS: true | false
```

---

## Phase 5: Tag + Ship

### Step 5a: Retroactive tag (if RETROACTIVE_TAG set from Phase 1)

```bash
# Find the commit that matches the retroactive version content
git log --oneline  # identify SHA

git tag vA.B.C <SHA>
git push origin vA.B.C  # pushes to both remotes (dual-remote policy)
```

Verify `release.yml` fires on Forgejo for the retroactive tag if present.

### Step 5b: Finalize changelog

Run `/release changelog` (or `/release verify commits`):

```
[UNRELEASED] → [VERSION_TARGET] - YYYY-MM-DD
```

### Step 5c: Regenerate lockfile (Python projects only)

After bumping `version =` in `pyproject.toml`, always regenerate the lockfile:

```bash
# Python (uv) — standard
uv lock
git add uv.lock
git commit -m "chore: update uv.lock for vVERSION_TARGET"
```

`data-upload-time`. uv 0.11.7+ rejects packages without publish dates during
re-resolution. Use per-package override instead of bare `uv lock`:

```bash
uv lock \
```

Also add to `pyproject.toml` so the setting is recorded (CI reads it via `uv sync --locked`
which doesn't re-resolve and is unaffected, but the record helps with future maintenance):

```toml
[tool.uv.exclude-newer-package]
```

**Why:** `uv.lock` contains the project's own version entry. A stale lockfile causes
`uv sync --locked` to fail in CI — uv falls back to dependency resolution, hits private
indexes, and fails with 401 Unauthorized even when credentials are correct.

Skip if no `uv.lock` / `poetry.lock` / `package-lock.json` is present.

### Step 5d: Final pre-commit

Run `/pre-commit` **(third run — final gate)**. Must pass cleanly.

### Step 5f: Tag and push

```bash
git tag vVERSION_TARGET
git push origin main        # both remotes (GitHub fetch + Forgejo push)
git push origin vVERSION_TARGET  # tag to both remotes
```

Verify `release.yml` fires on Forgejo (auto-creates release from CHANGELOG).

If `GH_PAT` secret is configured, GitHub release is mirrored automatically.

### Step 5g: Verify and close

```bash
# Verify tag pushed to both remotes
git ls-remote --tags origin | grep vVERSION_TARGET
git ls-remote --tags forgejo | grep vVERSION_TARGET 2>/dev/null || true

# Close milestone
gh api "repos/:owner/:repo/milestones" \
  --jq '.[] | select(.title=="MILESTONE_NAME") | .number' | \
  xargs -I {} gh api "repos/:owner/:repo/milestones/{}" \
  --method PATCH -f state=closed
```

Run `/release verify tags` to confirm everything is consistent.

### Step 5h: CI Build Gate

After pushing the tag, **wait for CI to complete and verify the build succeeded**. Do not proceed to Step 5i until the build workflow passes.

```bash
# Check recent runs for the tag commit — look for build workflow
fj ci runs {repo} 5          # confirm release.yml + build.yml triggered
fj ci tasks {repo} --limit 20  # check all job statuses

# Gate: all jobs for the tag SHA must be success or skip — no failure
```

**Classify failures:**

- `release.yml` / `create-release` failed → BLOCKER: Forgejo release not created. Re-trigger:
  `fj ci trigger {repo} release.yml main`
- `build.yml` / `Build and push` failed with **registry 5xx** → transient; re-trigger:
  `fj ci trigger {repo} build.yml main`
- `build.yml` failed with **compilation / install error** → BLOCKER: image not updated in registry.
  Investigate and fix before deploying. Do NOT proceed to Step 5i.
- `ci.yml` tests/lint failed → code issue merged to main; open a hotfix issue.

**This check is mandatory.** A build failure means the new image is not in the registry — deploying will pull the previous version silently.

### Step 5i: Deploy Prompt

After CI gate passes, ask the user:

```
╔══════════════════════════════════════════════════════╗
║   RELEASE COMPLETE — vVERSION_TARGET                 ║
║   CI: all green ✓                                    ║
╚══════════════════════════════════════════════════════╝

Deploy to production now?
  Y — trigger deploy workflow  (fj ci trigger {repo} deploy.yml main)
  N — skip (deploy manually later via /deploy)
```

If **Y**: run `fj ci trigger {repo} deploy.yml main` and invoke `/deploy verify` to run the post-deploy smoke test checklist.

If **N**: remind the user that `/deploy` is the next step and that the new image is ready in the registry.

**Phase 5 output:**

```
TAG: vVERSION_TARGET
MILESTONE_CLOSED: true | false
RELEASE_VERIFY: PASS | WARN | FAIL
CI_BUILD_GATE: PASS | FAIL | RETRIED
DEPLOY_TRIGGERED: true | false
```

---

## Error Handling

| Condition                                                | Action                                                                                          |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Phase 1 discovers no unreleased work                     | Abort: "Nothing to release — CHANGELOG [Unreleased] is empty and no milestone has open issues." |
| Phase 2 BLOCKER cannot be auto-fixed and user defers all | Continue with deferred list, note in release summary                                            |
| Phase 3 `/pre-commit` fails after 2 attempts             | Pause and present failure to user — do not proceed to Phase 4                                   |
| Phase 4 `/docs full` produces empty output               | Warn: "No docs were generated — verify docs/ structure and CHANGELOG entries"                   |
| Phase 5 build fails (registry 5xx)                       | Re-trigger `build.yml` once. If fails again, investigate registry health.                       |
| Phase 5 build fails (code/install error)                 | Do NOT deploy. Open hotfix issue. Fix on main, push, re-tag if needed.                          |

---

## Re-run Rules

The skill is designed to be **idempotent within a session**:

- Phases 1-3 can be re-run if something changes (new commit, user changes a blocker decision)
- Phase 4 re-runs safely (docs overwrite drafts with verified content)
- Phase 5 STOPS if the tag already exists — do not re-push

---

## Related Skills

- `/release plan` — Phase 1 (version scoping)
- `/health` — Phase 2 (project audit)
- `/docs` — Phase 4 (documentation pipeline)
- `/pre-commit` — validation gate between phases
- `/release verify` — post-tag consistency check
- `/release changelog` — Phase 5 changelog finalization
- `/ship` — commit + push + PR (used within phases when branching)
