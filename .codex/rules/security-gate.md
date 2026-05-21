# Security Gate — Universal Scanning Independent of CI

Applies to every project regardless of whether CI is configured.

## Mandatory: Before git commit or git push

Always run `/security-verify scan` before suggesting `git commit` or `git push`.
Do not skip this even if:

- The project has no CI configured
- The repo has no `.github/workflows/`
- The user says it's a small/quick change

If the user has already run `/security-verify scan` in the current session and no new files were
changed since then, the scan is considered fresh — no need to re-run.

## Mandatory: After gh pr create

Immediately after a successful `gh pr create`, run `/security-verify scan` against the branch.
This is the post-PR gate that replaces CI-based scanning when CI is absent.

## Why `git commit --no-verify` / `-n` is blocked

The `--no-verify` flag (short: `-n`) bypasses git pre-commit hooks, which is the same mechanism
that enforces the security gate. Both forms are STRICTLY blocked by the PreToolUse hook (bash.py).

If a user needs to commit quickly (emergency hotfix), the minimum acceptable path is:

1. Run `/security-verify scan` — takes ~30s
2. If scan passes, commit normally
3. If scan finds critical issues, address them first or document them as known tech debt

## Scope

Cross-repo, cross-stack. This rule applies when working with any codebase, not just projects
with an explicit security configuration.

## Exception: Config-Only Repos

Repos containing exclusively markdown, YAML, and text files (no executable code, no secrets,
no dependencies) may skip the scan with an explicit acknowledgment in the session.

Qualifies if ALL of the following are true:

- No `.py`, `.js`, `.ts`, `.sh`, `.rb`, `.go`, `.rs` files changed
- No `.env`, credentials, or secrets files changed
- Repo is a personal config/dotfiles repo (not a service or library)

In this case, note "config-only repo, scan skipped" before committing.

## JS Dependency Audit Threshold (S-3)

Hard gate: `pnpm audit --audit-level=critical` — blocks on CRITICAL only.
Informational: `pnpm audit --audit-level=high || true` — surfaces HIGH vulns without blocking.

**Rationale:** JS ecosystems produce HIGH-severity findings in transitive/dev deps (ReDoS in build
tools, prototype pollution in bundlers) that are not exploitable in the runtime path. Gating on
HIGH creates constant noise and "|| true" workarounds that erode trust in the gate. CRITICAL vulns
in JS are rare, typically RCE/SSRF in runtime code, and genuinely actionable.

Python uses `pip-audit` with no severity threshold argument (all vulns surfaced + gated) — different
ecosystem, more conservative CVE scoring, smaller dep trees.
