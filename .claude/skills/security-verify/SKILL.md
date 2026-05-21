---
name: security-verify
description: Run security verification — SAST pattern scanning, DAST against a running app, OWASP Top 10 compliance, CVSS assessment, and adversarial code audit. Use before commit/push or when checking code for vulnerabilities. Trigger on "security scan", "is this vulnerable", "OWASP check", "security verify", "scan for vulnerabilities".
allowed-tools: Read, Bash, Grep, Glob
---

# Security Verify — Verification Workflows

Run security verification checks: pattern scanning, OWASP compliance, and vulnerability assessment.

## Usage

```
/security-verify              # Default: run scan mode
/security-verify scan [path]  # Pattern-based security scanning (SAST)
/security-verify dast <url>   # Dynamic testing against running app (DAST)
/security-verify owasp        # OWASP Top 10 compliance check
/security-verify assess       # Vulnerability CVSS scoring + remediation
/security-verify audit        # Adversarial logic-level code review (CWE + CVSS + exploit)
/security-verify full         # scan + audit combined (use for /health or manual deep check)
```

## Mode: scan

Run pattern-based security scanning against the codebase.

### What It Checks

1. **Secret Detection** — Hardcoded credentials, API keys, private keys
2. **SQL Injection** — String interpolation in queries, raw SQL
3. **XSS** — Disabled auto-escaping, innerHTML, unsafe template filters
4. **Command Injection** — Unsafe subprocess/exec patterns
5. **Insecure Deserialization** — Unsafe deserializers
6. **Weak Cryptography** — MD5, SHA1, weak random for security use
7. **Multi-Tenant Violations** — tenant_id from request, missing tenant filters
8. **Cookie Issues** — Missing \_\_Host- prefix, missing samesite

### Scan Execution

Run the scanner script against target path:

```bash
# Full scan — manual usage, scans entire directory
bash "$HOME/.claude/skills/security-verify/lib/scanner-runner.sh" "${TARGET_PATH:-.}"

# Staged-only scan — pre-commit context, scans only git-staged files
bash "$HOME/.claude/skills/security-verify/lib/scanner-runner.sh" --staged
```

Use `--staged` when invoked from `/pre-commit` to limit scope to the current commit's changes.
Full-path scanning is for standalone audits.

Review findings, assess severity, and provide fix recommendations.

### Dependency Audit

After pattern scan, check for known CVEs:

```bash
# Use filtered requirements file to audit only public packages.
if command -v uv &>/dev/null && ([ -f uv.lock ] || [ -f pyproject.toml ]); then
  if uv export --no-hashes --frozen > /tmp/raw-reqs.txt 2>/dev/null; then :; else
    uv run pip freeze > /tmp/raw-reqs.txt 2>/dev/null || true
  fi
  uv run --with pip-audit pip-audit -r /tmp/pip-audit-reqs.txt 2>/dev/null || true
elif command -v pip-audit &>/dev/null; then
  pip-audit --local 2>/dev/null || true
else
  echo "pip-audit not installed"
fi
npm audit --production 2>/dev/null || echo "No package.json"
```

### Report Format

Generate a markdown report with severity counts, findings with file:line references, and fix recommendations.

## Mode: dast

Dynamic Application Security Testing against a running application. Tests live HTTP endpoints rather than reading source files.

### Prerequisites

- Application must be running and accessible at the provided URL
- `curl` (always available, zero extra deps)
- `nuclei` (optional, for deeper template-based scanning): `brew install nuclei`
- `python3` (required if using `--nuclei`, for JSON parsing)

### What It Checks

**Tier 1 — curl-based (always runs):**

| #   | Category               | What it checks                                                                          | Severity      |
| --- | ---------------------- | --------------------------------------------------------------------------------------- | ------------- |
| 1   | HTTP Security Headers  | HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy | LOW–HIGH      |
| 2   | Cookie Security        | Secure, HttpOnly, SameSite flags                                                        | MEDIUM–HIGH   |
| 3   | CORS                   | Wildcard origins, evil origin reflection                                                | HIGH–CRITICAL |
| 4   | TLS/SSL                | Protocol version (≥TLS 1.2), cert expiry                                                | MEDIUM–HIGH   |
| 5   | Information Disclosure | Server version header, X-Powered-By, exposed paths (/.env, /.git, /debug, /admin)       | LOW–HIGH      |
| 6   | Open Redirects         | Redirect parameter injection test                                                       | HIGH          |
| 7   | HTTP Methods           | TRACE enabled, OPTIONS enumeration                                                      | LOW           |

**Tier 2 — nuclei (when installed):**

| #   | Category     | What it checks                                                   |
| --- | ------------ | ---------------------------------------------------------------- |
| 8   | CVE patterns | Known vulnerability templates for http/, ssl/, misconfiguration/ |
| 9   | Auth bypass  | Default credentials, auth misconfiguration templates             |

### DAST Execution

```bash
# Tier 1 only (curl-based, zero deps)
bash "$HOME/.claude/skills/security-verify/lib/dast-runner.sh" "http://localhost:8000"

# Tier 1 + Tier 2 (requires nuclei installed)
bash "$HOME/.claude/skills/security-verify/lib/dast-runner.sh" "http://localhost:8000" --nuclei

# Custom per-check timeout (default: 5s)
bash "$HOME/.claude/skills/security-verify/lib/dast-runner.sh" "http://localhost:8000" --timeout 3
```

### Report Format — Active vs Potential

Findings are labelled to distinguish confidence level:

- **`ACTIVE`** — Confirmed by server response. Remediate now. (e.g., server returned missing CSP header)
- **`POTENTIAL`** — Suspicious behavior requiring manual verification. (e.g., redirect parameter exists but may validate destinations)

Exit codes: `0` = no critical/high findings, `1` = critical/high found, `2` = URL unreachable.

### DAST vs SAST

|            | SAST (`scan`)             | DAST (`dast`)             |
| ---------- | ------------------------- | ------------------------- |
| Input      | Source files              | Running server            |
| Finds      | Potential vulnerabilities | Active misconfigurations  |
| Deps       | None (bash grep)          | curl + optional nuclei    |
| When       | Any time                  | App must be running       |
| Pre-commit | Yes (default)             | Optional (`--dast <url>`) |

## Mode: owasp

Systematic OWASP Top 10 2021 compliance verification.

### Categories

| ID  | Category                  | Key Checks                                            |
| --- | ------------------------- | ----------------------------------------------------- |
| A01 | Broken Access Control     | Authorization on every endpoint, no IDOR, CORS config |
| A02 | Cryptographic Failures    | TLS 1.2+, Argon2/bcrypt hashing, no weak algorithms   |
| A03 | Injection                 | Parameterized SQL, safe subprocess usage              |
| A04 | Insecure Design           | Rate limiting, account lockout, threat model          |
| A05 | Security Misconfiguration | Debug off, security headers, no defaults              |
| A06 | Vulnerable Components     | No critical CVEs, deps up to date                     |
| A07 | Auth Failures             | Strong passwords, session timeout, MFA                |
| A08 | Integrity Failures        | Safe deserialization, yaml.safe_load                  |
| A09 | Logging Failures          | Auth events logged, no PII in logs                    |
| A10 | SSRF                      | URL validation, private IPs blocked                   |

### Verification Process

For each category:

1. Run automated checks (grep patterns per category)
2. Review findings
3. Mark Pass/Partial/Fail with evidence
4. Generate compliance report

## Mode: assess

Deep vulnerability analysis with CVSS scoring and remediation strategies.

### Assessment Workflow

1. **Classify** vulnerability type (injection, auth, data exposure, XSS, etc.)
2. **Evaluate exploitability** (Easy/Medium/Hard based on attack vector, complexity, privileges)
3. **Assess impact** (Confidentiality/Integrity/Availability: None/Low/High)
4. **Calculate CVSS v3.1 score** using base metrics
5. **Prioritize** using risk matrix (severity x exploitability -> P0-P3)
6. **Recommend remediation** with code examples

### CVSS Score Ranges

| Score    | Severity |
| -------- | -------- |
| 0.0      | None     |
| 0.1-3.9  | Low      |
| 4.0-6.9  | Medium   |
| 7.0-8.9  | High     |
| 9.0-10.0 | Critical |

### Priority SLAs

| Priority | SLA      | Criteria                     |
| -------- | -------- | ---------------------------- |
| P0       | 24 hours | Critical+Easy or High+Easy   |
| P1       | 7 days   | Critical+Hard or High+Medium |
| P2       | 30 days  | Medium or High+Hard          |
| P3       | 90 days  | Low severity                 |

## Mode: audit

Adversarial logic-level code review. Reads code deeply to find vulnerabilities that grep-based SAST misses — auth bypass, IDOR, race conditions, session fixation, missing ownership checks.

**Run as a focused subagent** (spawn fresh context to avoid polluting the main conversation with large finding sets). When invoked, spawn an Agent with `subagent_type: general-purpose`, `model: sonnet`, and pass the target scope.

### Mindset

Assume the code is hostile until proven otherwise. Find vulnerabilities a real attacker would exploit. "If you can't write the exploit scenario in one sentence, downgrade severity."



- Injection: trace user-controlled input → all SQL sinks (raw `text()`, `op.execute()`, f-strings in queries). Alembic rule: each `op.execute()` must be a single statement — two statements separated by `;` fail on asyncpg.
- Auth: check every route for `Depends(get_current_user)` or equivalent. Routes missing auth on sensitive operations (write, delete, admin functions) are CRITICAL.
- IDOR: for every endpoint accepting an object ID (company_id, person_id, job_id), verify ownership check: does the handler confirm the object belongs to the authenticated user/tenant?
- Race conditions: check background job handlers and Celery tasks for TOCTOU patterns on shared resources.

**General checks (adapt to target):**

- Sensitive data exposure: PII in logs, cleartext credentials in source, debug endpoints accessible in prod
- Input validation: Pydantic model field constraints present at API boundaries (length, range, format)
- CSRF: state-changing endpoints behind Traefik — session cookie `SameSite` set?
- Insecure deserialization: no `yaml.load()` without `Loader=yaml.SafeLoader`; no unsafe deserialization of untrusted binary data
- Security misconfiguration: debug mode off, `ALLOWED_HOSTS` not `*`, verbose error messages suppressed

### Report Format

Each finding must include:

- **ID**: `SEC-NNN` (sequential)
- **CWE**: `CWE-XXX — Name` (e.g., `CWE-89 — SQL Injection`)
- **Severity**: `CRITICAL / HIGH / MEDIUM / LOW` with CVSS-ish reasoning
- **Location**: `file.py:line`
- **Exploit scenario**: one sentence describing the attack
- **Fix**: concrete code-level remediation

### When to use

- Manual deep audit before major releases
- After `/health security` (scan passes but audit finds logic flaws)
- When security-sensitive PR touches auth, session, IDOR-prone endpoints

**NOT for pre-commit** — use `scan` there. `audit` takes minutes; `scan` takes seconds.

## Mode: full

Runs `scan` + `audit` sequentially. Use for `/health full` or when you want complete security coverage in one command.

```
1. Run scan (SAST grep patterns + dependency audit)
2. Run audit (adversarial logic-level review)
3. Merge findings into unified report ordered by severity
```

## Workflow Integration

Recommended security workflow:

1. **Implement** → `/security [mode]` — get implementation guidance
2. **Scan** → `/security-verify scan` — SAST: fast grep-based check (seconds, runs in pre-commit)
3. **Audit** → `/security-verify audit` — adversarial logic review (minutes, run manually or via /health)
4. **Dynamic** → `/security-verify dast <url>` — DAST: test running app (staging/local)
5. **Comply** → `/security-verify owasp` — verify OWASP Top 10 compliance
6. **Assess** → `/security-verify assess` — CVSS score and prioritize findings
7. **Full** → `/security-verify full` — scan + audit combined (use for /health full)

`/security-verify scan` is called by `/pre-commit` automatically. `/security-verify dast` is optional — use `--dast <url>` with `/pre-commit` when a local dev server is running. `/security-verify audit` and `full` are called by `/health security` and `/health full`.

## Gotchas

- Bandit requires Python ≤3.13 — Python 3.14 removed `.s`/`.n` AST attributes; bandit ≤1.8.x crashes on every file and silently reports 0 findings. Use `python3.13 -m bandit` (bandit 1.9.4 installed there).
- `scanner-runner.sh --staged` requires bash 4+ (`mapfile`); macOS ships bash 3.2 — use full scan mode instead of `--staged` on macOS.
- False positives in `projects/` (JSONL session transcripts), `.archive/`, and `.venv/` — assess as FP, do not report as real issues.
- JS dependency audit gates on CRITICAL only (`pnpm audit --audit-level=critical`); HIGH vulns in transitive/dev deps (ReDoS in build tools, prototype pollution in bundlers) are noise, not runtime-exploitable — surface them informationally but do not block.
- Python `pip-audit` runs with no severity threshold (all vulns surfaced + gated) — different ecosystem from JS, more conservative CVE scoring, smaller dep trees.
