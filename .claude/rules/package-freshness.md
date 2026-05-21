---
name: package-freshness
description: Warn before adding Python/JS packages published less than 7 days ago — behavioral guardrail against supply chain attacks targeting new releases.
metadata:
  type: feedback
paths:
  - "pyproject.toml"
  - "package.json"
  - "pnpm-lock.yaml"
  - "uv.lock"
  - "requirements*.txt"
---

Before adding any NEW package (one not already in the lockfile), check its publish date.

**Why:** Supply chain attacks often target the first days after a package is published or after a maintainer account is compromised. A 7-day window catches most fast-moving attacks while being invisible for normal workflows (most packages are weeks/months old).

**How to apply:**

1. When the user asks to `uv add <pkg>`, `pnpm add <pkg>`, or similar:
   - Check PyPI: `curl -s https://pypi.org/pypi/<pkg>/json | python3 -c "import json,sys; d=json.load(sys.stdin); print(list(d['releases'].keys())[-1], list(d['releases'].values())[-1][0]['upload_time'] if d['releases'].values() else 'unknown')"`
   - Check npm: `curl -s https://registry.npmjs.org/<pkg>/latest | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('time',{}).get(d.get('version',''),'unknown'))"`
2. If published < 7 days ago: **warn** before proceeding. Say: "⚠️ `<pkg>` was published N days ago (on DATE). New packages carry elevated supply chain risk. Proceed?"
3. If published ≥ 7 days ago: proceed silently — no friction.

**This is a warning, not a block.** The user decides. If they say yes, proceed.

**Scope:** new deps only. If the package is already in the lockfile at any version, no check needed.
