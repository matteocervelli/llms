---
paths:
  - "**/*.html"
  - "**/*.jinja2"
  - "**/*.j2"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/*.vue"
  - "**/*.svelte"
---

# Frontend Verification

After implementing ANY frontend/UI/UX change, proactively verify it works using `playwright-cli`. Don't wait to be asked.

## Tool Selection

| Need                        | playwright-cli (primary)                      | attach --cdp=chrome (reuse user's Chrome)   |
| --------------------------- | --------------------------------------------- | ------------------------------------------- |
| Quick visual check          | `playwright-cli screenshot`                   | `attach --cdp=chrome` then screenshot       |
| Click through a flow        | `playwright-cli click/fill/type` with refs    | Same after attach                           |
| Read console errors         | `playwright-cli console`                      | Same after attach                           |
| Read network traffic        | `playwright-cli requests` + `request <N>`     | Same after attach                           |
| Responsive check            | `playwright-cli resize` at multiple viewports | N/A (attached session uses Chrome viewport) |
| Record interaction          | `playwright-cli video-start/video-stop`       | Same after attach                           |
| Mark element visually       | `playwright-cli highlight e5`                 | Same after attach                           |
| UI review / design feedback | `playwright-cli show --annotate`              | Same after attach                           |
| Write E2E tests             | `/frontend e2e` (Playwright test runner)      | —                                           |
| Thorough testing            | `browser-tester` agent (discovery + fix)      | —                                           |

## Quick verification workflow

```bash
# 1. Check dev server
curl -s -o /dev/null -w "%{http_code}" http://localhost:<port>

# 2. Open and inspect
playwright-cli open http://localhost:<port>
playwright-cli snapshot                    # get element refs

# 3. Interact if needed
playwright-cli fill <ref> "test data"
playwright-cli click <ref>

# 4. Check for errors
playwright-cli console
playwright-cli requests          # numbered list; use `playwright-cli request <N>` for details

# 5. Screenshot and close
playwright-cli screenshot
playwright-cli close
```

Screenshots save to `.playwright-cli/` (gitignored globally).

## Browser

Default: `--browser=chromium` (ARM Linux + macOS compatible).
Do NOT use `--browser=chrome` — no ARM Ubuntu binary.

## Pre-flight

Before any browser interaction, verify the dev server is running:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:<port>
```

## Authentication — CRITICAL

**NEVER change, reset, or "fix" passwords when a login fails during verification.**

When playwright-cli hits a login wall:

1. Check `.claude/playwright-creds.json` in the project root for saved credentials
2. If not found, **ASK the user** for the credentials before proceeding
3. If login still fails with known credentials, report the failure and stop — do NOT attempt to fix the DB, change password hashes, or modify any user records

Changing passwords without being asked is a destructive action that breaks other users' sessions and wastes debugging time. The correct response to a 401 is to ask, not to act.
