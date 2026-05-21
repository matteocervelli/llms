---
name: deps
description: Audit dependency freshness — scan outdated deps and CVEs, classify severity, record update/defer/skip decisions in Atrium, gate PASS/WARN/FAIL. Use when checking for outdated packages or deciding whether to upgrade. Trigger on "outdated dependencies", "dependency audit", "are my deps up to date", "should I upgrade".
allowed-tools: Read, Bash, Grep, Glob
---

# /deps — Dependency Health & Decision Tracker

Scans project dependencies for outdated versions and CVEs, classifies severity, and records
human decisions (update / defer / skip) in Atrium so the reasoning survives across sessions.

**Data flow:** `/deps scan` both reads AND writes to Atrium:

- Reads: existing decisions to mark assessed deps
- Writes: fresh outdated findings via `POST /api/dev-projects/sync` (keeps Atrium current
  between scheduled audit runs)

**Graceful degradation:** When Atrium is unreachable, scan/classify still works locally.
Decision storage and decision-coverage checks are silently skipped with a note.

## Quick Start

```
/deps                        # summary: outdated deps + decision status for current project
/deps scan                   # full scan → PASS/WARN/FAIL gate (used by /health deps)
/deps decide                 # interactive: assess each unassessed finding, record to Atrium
/deps status                 # fetch current snapshot from Atrium (deps + active decisions)
/deps history                # fetch version changelog from Atrium (newest first)
```

Invoked by: `/health deps` as part of the full project health audit.

---

## Atrium URL Resolution

All subcommands that talk to Atrium resolve the base URL in this order:

```bash
```

---

## Subcommand: `/deps` (summary)

Show dependency status for the current project — outdated count by severity, decision coverage.

**Steps:**

1. Detect project slug from current directory (last segment of `pwd`).
3. If Atrium unreachable: fall through to local scan mode (show outdated only, no decisions).
4. If Atrium available: show dep table with decision column.

**Output:**

```
## Dependency Status — <project> — <date>

  next                 14.2.0 → 15.0.0   [HIGH]     DEFERRED until 2026-04-27
  fastapi              0.109.0 → 0.115.0  [MEDIUM]   unassessed
  httpx                0.27.0 → 0.28.0    [LOW]      unassessed

Summary: 1 CRITICAL · 0 HIGH unassessed · 2 MEDIUM unassessed
Run `/deps decide` to record decisions. Run `/deps scan` for full gate.
```

---

## Subcommand: `/deps scan`

Full dependency scan producing a `Deps [PASS|WARN|FAIL]` gate. Used by `/health deps`.

### Step 1 — Detect ecosystems

Scan the current directory for manifest files:

```bash
HAS_PYTHON=false; HAS_NODE=false; HAS_RUST=false; HAS_GO=false
[ -f pyproject.toml ] || [ -f requirements.txt ] || [ -f setup.py ] && HAS_PYTHON=true
[ -f package.json ] && HAS_NODE=true
[ -f Cargo.toml ] && HAS_RUST=true
[ -f go.mod ] && HAS_GO=true
```

If no manifests found: output `Deps [SKIP] — no manifest files found`, stop.

### Step 2 — Collect outdated packages

Run package manager outdated commands. Parse into a unified list of findings.

**Each finding has:** `package`, `ecosystem`, `current_version`, `available_version`

**Python:**

```bash
# uv preferred; fallback to pip
if command -v uv &>/dev/null; then
  uv pip list --outdated --format json 2>/dev/null
else
  pip list --outdated --format json 2>/dev/null
fi
```

Parse: `jq '.[] | {package: .name, ecosystem: "python", current_version: .version, available_version: .latest_version}'`

**Node.js:**

```bash
npm outdated --json 2>/dev/null || true
# npm outdated exits non-zero when outdated deps exist — `|| true` prevents abort
```

Parse: `jq 'to_entries[] | {package: .key, ecosystem: "npm", current_version: .value.current, available_version: .value.latest}'`

**Rust (if cargo-outdated installed):**

```bash
if command -v cargo-outdated &>/dev/null; then
  cargo outdated --format json 2>/dev/null
fi
```

Parse the `dependencies` array. If `cargo-outdated` not installed: note "install cargo-outdated for Rust dep checking" and skip.

**Go:**

```bash
if [ "$HAS_GO" = "true" ]; then
  go list -m -u -json all 2>/dev/null | jq -s '.[] | select(.Update != null) |
    {package: .Path, ecosystem: "go", current_version: .Version, available_version: .Update.Version}'
fi
```

### Step 3 — Run security audits

**Python:**

```bash
pip audit --format json 2>/dev/null
```

Parse: extract packages with `vulns` list non-empty. Each vuln has `id` (CVE/GHSA), `fix_versions`.

**Node.js:**

```bash
npm audit --json 2>/dev/null || true
```

Parse: `jq '.vulnerabilities | to_entries[] | {package: .key, severity: .value.severity, cves: [.value.via[] | select(type=="object") | .cve // .url]}'`

**Rust (if cargo-audit installed):**

```bash
if command -v cargo-audit &>/dev/null; then
  cargo audit --json 2>/dev/null
fi
```

### Step 4 — Classify severity

For each finding, assign severity:

| Severity   | Condition                                                                                  |
| ---------- | ------------------------------------------------------------------------------------------ |
| `critical` | Has CVE IDs OR package is EOL (detected by pip-audit `fix_versions` empty)                 |
| `high`     | Major version bump: `available_version` major > `current_version` major (semver X changed) |
| `medium`   | Minor version bump: major same, minor changed                                              |
| `low`      | Patch only: major.minor same, patch changed                                                |

**Semver parsing (bash):**

```bash
major() { echo "$1" | cut -d. -f1 | tr -dc '0-9'; }
minor() { echo "$1" | cut -d. -f2 | tr -dc '0-9'; }
```

Security audit findings always override to `critical` regardless of version bump type.

Merge: if a package appears in both outdated and audit lists, take the higher severity and
union the CVE IDs.

### Step 5 — Fetch decisions from Atrium

```bash
SLUG=$(basename "$(pwd)")

DECISIONS=$(curl -sf --max-time 5 \
```

If `DECISIONS` is empty: mark all findings as `unassessed`, skip coverage check.

For each finding:

- If an active decision exists for `(package, ecosystem)`: mark as `assessed`, show decision + review_at.
- Check `GET /{slug}/dep-decisions/overdue` — any overdue decisions escalate to `critical`.

### Step 6 — Push fresh findings to Atrium

Construct a `POST /api/dev-projects/sync` payload from the scan results. This keeps Atrium
current between scheduled audit runs.

```bash
# Build deps array as JSON
DEPS_JSON=$(jq -n \
  --argjson findings "$FINDINGS_JSON" \
  '$findings | map({
    package: .package,
    ecosystem: .ecosystem,
    current_version: .current_version,
    available_version: .available_version,
    severity: .severity,
    cve_ids: (.cve_ids // []),
    is_dev_dep: false
  })')

SYNC_PAYLOAD=$(jq -n \
  --arg name "$SLUG" \
  --arg slug "$SLUG" \
  --arg path "$(pwd)" \
  --argjson deps "$DEPS_JSON" \
  '{projects: [{name: $name, slug: $slug, path: $path, deps: $deps}]}')

  -H "Content-Type: application/json" \
  -d "$SYNC_PAYLOAD" >/dev/null 2>&1 || true
```

Skip silently if Atrium unreachable.

### Step 7 — Gate and output

**Gate logic:**

| Gate   | Condition                                                                             |
| ------ | ------------------------------------------------------------------------------------- |
| `PASS` | 0 critical findings AND 0 unassessed high findings AND 0 overdue decisions            |
| `WARN` | 0 critical BUT unassessed high/medium findings exist OR ≥1 decision due within 7 days |
| `FAIL` | Any critical (CVE or EOL) OR any overdue deferred decision                            |
| `SKIP` | No manifest files found                                                               |

**Output format** (matches `/health` report style):

```
### Deps [PASS|WARN|FAIL]

Scanned: python (pyproject.toml), npm (package.json)
Date: YYYY-MM-DD

| Package  | Ecosystem | Current  | Available | Severity | Decision          |
|----------|-----------|----------|-----------|----------|-------------------|
| next     | npm       | 14.2.0   | 15.0.0    | HIGH     | DEFERRED 2026-04-27 |
| fastapi  | python    | 0.109.0  | 0.115.0   | MEDIUM   | unassessed        |
| httpx    | python    | 0.27.0   | 0.28.0    | LOW      | unassessed        |

- ✗ 0 CRITICAL
- ⚠ 1 unassessed HIGH
- ⚠ 2 unassessed MEDIUM
- ✓ 1 DEFERRED (within review date)
```

Summary line for `/health` report: `Deps  [WARN]  0 critical · 1 unassessed HIGH · 2 unassessed MEDIUM`

---

## Subcommand: `/deps decide`

Interactive decision workflow. For each unassessed finding (sorted by severity desc), present
options and record the decision in Atrium.

**Steps:**

1. Run `/deps scan` to get current findings.
2. Filter to unassessed only.
3. For each finding (CRITICAL first, then HIGH, MEDIUM, LOW):

```
─────────────────────────────────────────────────
Package:   next  (npm)
Current:   14.2.0  →  Available: 15.0.0
Severity:  HIGH (major version bump)
CVEs:      none
─────────────────────────────────────────────────

Decision:
  [u] update   — will update now (no Atrium record needed)
  [d] defer    — not now, but schedule review
  [s] skip     — permanently skip this version jump

Choice:
```

4. **For `update`:** Record nothing in Atrium (dep will disappear after update+rescan).
   Print: `→ Marked for update. Run update commands after this session.`

5. **For `defer`:**
   - Prompt: `Rationale (why not now)?`
   - Prompt: `Review in how many days? [30]`

6. **For `skip`:**
   - Prompt: `Rationale (why skip this version permanently)?`
   - POST with `review_at: null`

7. After all findings processed, print summary:

```
Decisions recorded: 2 deferred · 1 to update · 1 skipped
Run `/deps scan` to verify gate status.
```

**Atrium unavailable:** If `POST` fails, print the decision in a copyable format and suggest
recording manually later.

---

## Subcommand: `/deps status`

Fetch the current dep snapshot + active decisions from Atrium.

```bash
SLUG=$(basename "$(pwd)")
echo ""
echo "Active decisions:"
  jq '.[] | "\(.package) [\(.ecosystem)]: \(.decision) — \(.rationale) (review: \(.review_at // "never"))"'
```

If project not found in Atrium (404): print "Project '${SLUG}' not yet registered in Atrium.
Run `/deps scan` to register and populate."

---

## Subcommand: `/deps history`

Fetch dep version changelog from Atrium — when did versions change and what CVEs were present.

```bash
SLUG=$(basename "$(pwd)")
  jq '.[] | "\(.detected_at[:10]) \(.package) [\(.ecosystem)]: \(.from_version // "new") → \(.to_version)  severity=\(.severity)"'
```

---

## Decision Recording Format

When recording to Atrium (`POST /api/dev-projects/{slug}/dep-decisions`):

```json
{
  "package": "next",
  "ecosystem": "npm",
  "current_version": "14.2.0",
  "available_version": "15.0.0",
  "decision": "defer",
  "rationale": "Breaking changes in App Router, assess after migration guide",
  "review_at": "2026-04-27T00:00:00Z",
  "decided_by": "matteo",
  "session_id": null
}
```

`decided_by` is optional — use `whoami` output if available.

---

## Thresholds

| Gate | Condition                                                                    |
| ---- | ---------------------------------------------------------------------------- |
| PASS | 0 critical · 0 unassessed HIGH · all decisions within review date            |
| WARN | 0 critical · unassessed HIGH/MEDIUM exist · OR ≥1 decision due within 7 days |
| FAIL | Any CRITICAL (CVE/EOL) · OR any overdue deferred decision                    |
| SKIP | No manifest files found                                                      |
