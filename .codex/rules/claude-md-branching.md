---
paths:
  - "**/CLAUDE.md"
  - "**/README.md"
---

# CLAUDE.md Branching Policy

CLAUDE.md and root README.md are release-branch responsibilities.
Feature branches must not modify them — doing so creates merge conflicts between parallel features and races on the behavioral contract.

## Rule

| Branch type | CLAUDE.md | README.md (root) | skills/\*/SKILL.md |
| ----------- | --------- | ---------------- | ------------------ |
| `feature/*` | **No**    | **No**           | Yes                |
| `fix/*`     | **No**    | **No**           | Yes                |
| `chore/*`   | **No**    | **No**           | Yes                |
| `release/*` | Yes       | Yes              | Yes                |
| `v*`        | Yes       | Yes              | Yes                |
| `docs/*`    | Yes       | Yes              | Yes                |
| `main`      | Yes       | Yes              | Yes                |

## Rationale

Feature branches serialize into a release branch where doc changes are
aggregated once. Editing CLAUDE.md on a feature branch means every
parallel feature competes to own the same file — last writer wins.

**Edge case — direct main commits**: Hotfixes, health audits, and version bumps
committed directly to `main` (no branch) are allowed to touch CLAUDE.md and README.md.
No parallel branch conflict is possible in this case.

## Enforcement

This is **observational**, not a hard hook block.
`/pr-merge` Step 5 detects violations post-merge and flags them.
If a feature branch modified CLAUDE.md, Step 5 proposes a corrective
commit directly on main to restore policy compliance.
