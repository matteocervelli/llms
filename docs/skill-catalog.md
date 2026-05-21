# Skill Catalog

39 skills organized by domain. Invoke with `/skill-name` in Claude Code or Codex.


## SDLC Pipeline

| Skill             | Trigger                                                            | Description                                                                 |
| ----------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| `/discovery`      | "is this worth building", "validate this idea"                     | Phase 0 gate — problem framing, competitive analysis, feasibility, go/no-go |
| `/story`          | "write user stories", "break this into stories", "plan the sprint" | Feature idea → INVEST-compliant stories, epics, PRPs, sprint plans          |
| `/story-verify`   | "validate the stories", "INVEST check", "are these stories ready"  | INVEST scoring, story-to-test coverage, development readiness               |
| `/spec`           | "write a spec", "spec before coding"                               | Durable feature spec before touching code. Pipelines into `/implementation` |
| `/design`         | "design the architecture", "design the API", "data model"          | Component architecture, REST API contracts, Pydantic schemas                |
| `/implementation` | "implement this", "build it"                                       | Spec-driven implementation — TDD waves, map patching, review                |
| `/fix`            | "fix this bug", "fix issue #N"                                     | Bug fix with minimal ceremony. Optional GitHub issue linkage                |
| `/quick`          | "quick fix", "small change"                                        | Zero-ceremony atomic task for tiny fixes (minutes, not hours)               |
| `/diagnose`       | "investigate this bug", "unknown root cause"                       | Root cause investigation via subagent + companion solver                    |


## Quality & Security

| Skill                 | Trigger                                                                  | Description                                                            |
| --------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| `/code-review`        | "review this code", "code review", "is this well-written"                | Claude-native code quality review — no external AI                     |
| `/pre-commit`         | "validate before commit", "ready to commit", "run all checks"            | Full gate: quality, tests, coverage, security scan, companion review   |
| `/quality-check`      | "lint", "type-check", "quality check", "run the linters"                 | Multi-language formatting, linting, type-checking, complexity analysis |
| `/security`           | "how do I secure this", "security best practices", "is this secure"      | Stack-specific security implementation guidance                        |
| `/security-verify`    | "security scan", "OWASP check", "scan for vulnerabilities"               | SAST, DAST, OWASP Top 10, CVSS, adversarial audit                      |
| `/supply-chain-audit` | "supply chain audit", "check for compromised packages"                   | Forensic scan for npm/PyPI supply-chain compromise                     |
| `/docker-audit`       | "audit my Dockerfile", "Docker best practices", "is my container secure" | Dockerfile and Compose audit against 10 common mistakes                |
| `/test-scaffold`      | "scaffold tests", "generate test file", "write test boilerplate"         | Unit test files with structure, fixtures, mocking (pytest / Jest)      |


## Git / PR / Release

| Skill         | Trigger                                                   | Description                                                            |
| ------------- | --------------------------------------------------------- | ---------------------------------------------------------------------- |
| `/ship`       | "ship it", "commit and push"                              | Final-mile orchestrator — commit → push → PR creation                  |
| `/pr-creator` | "create a PR", "open a pull request"                      | Comprehensive PR with description, test plan, proper git workflow      |
| `/pr-fix`     | "fix this PR", "triage the PR"                            | Triage, fix, and pre-flight a PR before merge                          |
| `/pr-merge`   | "merge the PR", "is this ready to merge"                  | Safe merge with CI/CD, review, conflict validation                     |
| `/release`    | "cut a release", "bump the version", "generate changelog" | Version planning, changelog generation, release verification           |
| `/deploy`     | "deploy", "roll out", "canary", "feature flag"            | Post-merge deployment — canary/blue-green, smoke tests, rollback       |
| `/progress`   | "where was I", "what's next", "progress"                  | Situational awareness — fresh git/PR snapshot + next action suggestion |


## Docs & Ops

| Skill                    | Trigger                                                            | Description                                                              |
| ------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `/docs`                  | "write docs", "documentation site", "user guide"                   | Build and publish project docs — Starlight/Astro or markdown             |
| `/documentation-updater` | "update the docs", "sync docs after feature"                       | Update implementation docs, user guides, API docs, architecture diagrams |
| `/deps`                  | "outdated dependencies", "dependency audit", "should I upgrade"    | Dependency freshness audit, CVE scanning, PASS/WARN/FAIL gate            |
| `/health`                | "project health", "audit the project", "health check"              | Holistic audit across endpoints, versions, docs, security, quality, CI   |
| `/ops`                   | "add logging", "metrics", "dashboard", "alerting", "observability" | Structured logging, RED metrics, Prometheus, Grafana, SLO alerting       |
| `/techdebt`              | "find tech debt", "dead code", "duplicated code", "code hygiene"   | Dead code, duplications, TODOs, oversized functions                      |
| `/website-health`        | "audit my website", "site health", "check SEO"                     | Live website audit — SEO, performance, links, privacy, a11y, security    |


## Meta / Tooling

| Skill                | Trigger                                                               | Description                                                              |
| -------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `/map-codebase`      | "map the codebase", "understand this repo"                            | Parallel codebase analysis via 7 mapper subagents                        |
| `/skillify`          | "make this a skill", "convert this to a skill"                        | Convert a working solution into a permanent, tested, registered skill    |
| `/registry`          | "list skills", "component registry", "what skills exist"              | Query, update, and audit the skill/agent/hook registry                   |
| `/review`            | "get a second opinion", "companion review", "review my changes"       | Dispatch to external companion AIs (Codex, Gemini, Claude)               |
| `/project-create`    | "create a new project", "initialize a project", "bootstrap a project" | New project with full setup — repo structure, docs, quality tools, CI/CD |
| `/analytics`         | "query the database", "SQL", "show me data from"                      | SQL queries against psql, BigQuery, or MySQL from terminal               |
| `/frontend`          | "build a component", "E2E test", "accessibility audit", "a11y"        | UI design, components, Playwright E2E, WCAG a11y, visual review          |
| `/claude-code-guide` | "how do I use Claude Code", "Claude Code docs"                        | Fetch Claude Code documentation and help with configuration              |
