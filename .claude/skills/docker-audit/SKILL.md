---
name: docker-audit
description: Audit Dockerfiles and Compose files against the 10 common Docker mistakes — image security, build efficiency, runtime safety. Use when reviewing or hardening Docker configs. Trigger on "audit my Dockerfile", "check this Compose file", "Docker best practices", "is my container secure".
allowed-tools: Read, Bash, Grep, Glob
---

# Docker Audit Skill

## Purpose

Systematic audit of Docker configurations against the 10 most common Docker mistakes. Covers image security, build efficiency, runtime safety, and Compose best practices. Works with grep-based detection (no external tools required) plus optional deep scanning with hadolint, trivy, and dockle.

## Quick Start

```bash
/docker-audit [path]
```

## Discovery

Find all Docker files in scope:

```bash
find . -name "Dockerfile*" -o -name "compose*.yaml" -o -name "compose*.yml" -o -name "docker-compose*.yml" -o -name "docker-compose*.yaml" -o -name ".dockerignore" | head -50
```

## Audit Categories

### 1. Image Tags (Critical)

```bash
# Detect :latest or untagged images
grep -n "^FROM.*:latest" Dockerfile*
grep -n "^FROM [^ :]*$" Dockerfile*
grep -rn "image:.*:latest" compose*.yaml docker-compose*.yml 2>/dev/null
grep -rn "image: [^ :]*$" compose*.yaml docker-compose*.yml 2>/dev/null
```

**Pass**: All FROM/image directives use pinned version tags (e.g., `node:22.12-alpine`)
**Fail**: Any `:latest` or missing tag

### 2. Image Size (High)

```bash
# Check for bloated base images
grep -n "^FROM.*ubuntu\|^FROM.*debian\|^FROM.*centos\|^FROM.*fedora" Dockerfile*
```

**Pass**: Uses alpine, slim, or distroless variants
**Fail**: Full OS base images without justification

### 3. Build Cache Ordering (Medium)

```bash
# Check COPY order — dependency files should come before source
grep -n "^COPY\|^ADD" Dockerfile*
# Correct: COPY package*.json -> RUN npm install -> COPY . .
# Wrong: COPY . . -> RUN npm install
```

**Pass**: Dependency manifests (package.json, requirements.txt, go.mod, Gemfile) copied and installed before source code
**Fail**: `COPY . .` appears before dependency installation

### 4. Non-Root User (Critical)

```bash
# Check for USER directive
grep -n "^USER" Dockerfile*
# Check for user creation
grep -n "adduser\|useradd\|addgroup\|groupadd" Dockerfile*
```

**Pass**: USER directive present with non-root user
**Fail**: No USER directive (defaults to root)

### 5. Secrets in Build (Critical)

```bash
# Detect secrets in Dockerfiles
grep -in "ENV.*PASSWORD\|ENV.*SECRET\|ENV.*API_KEY\|ENV.*TOKEN\|ENV.*CREDENTIAL" Dockerfile*
grep -in "ARG.*PASSWORD\|ARG.*SECRET\|ARG.*API_KEY\|ARG.*TOKEN" Dockerfile*
# Check for COPY of secret files
grep -in "COPY.*\.env\|COPY.*credentials\|COPY.*\.pem\|COPY.*\.key\|COPY.*\.p12" Dockerfile*
```

**Pass**: No secrets in ENV/ARG/COPY directives
**Fail**: Secret-like values found in build context

### 6. Dockerignore (High)

```bash
# Check existence and content
ls .dockerignore 2>/dev/null
# Check for critical exclusions
grep -c ".git\|node_modules\|__pycache__\|\.env" .dockerignore 2>/dev/null
```

**Pass**: `.dockerignore` exists and excludes .git, node_modules/**pycache**, .env, logs
**Fail**: Missing or incomplete .dockerignore

### 7. Health Checks (High)

```bash
# Dockerfile HEALTHCHECK
grep -n "HEALTHCHECK" Dockerfile*
# Compose healthcheck
grep -A3 "healthcheck:" compose*.yaml docker-compose*.yml 2>/dev/null
```

**Pass**: HEALTHCHECK in Dockerfile or healthcheck in Compose for all services
**Fail**: No health check defined

### 8. Multi-Stage Builds (Medium)

```bash
# Count FROM directives (multi-stage = 2+)
grep -c "^FROM" Dockerfile*
# Check for AS aliases
grep -n "^FROM.*AS\|^FROM.*as" Dockerfile*
```

**Pass**: Production Dockerfile uses multi-stage (2+ FROM with AS alias)
**Fail**: Single FROM for production images

### 9. Layer Efficiency (Medium)

```bash
# Count separate RUN commands (flag if >5)
grep -c "^RUN" Dockerfile*
# Check for cleanup in same layer as install
grep -n "rm -rf.*apt\|rm -rf.*cache\|rm -rf.*tmp\|rm -rf.*lists" Dockerfile*
# Detect split update/install (bad pattern)
grep -c "apt-get update" Dockerfile*
grep -c "apt-get install" Dockerfile*
```

**Pass**: RUN commands combined where logical, cleanup in same layer as install
**Fail**: Many separate RUN commands, no cleanup, split update/install

### 10. Base Image Currency (Medium)

```bash
# Extract base images for scanning
grep "^FROM" Dockerfile* | awk -F'FROM ' '{print $2}' | awk '{print $1}'

# Trivy scan (if available)
trivy image --severity HIGH,CRITICAL <image>

# Docker Scout (if available)
docker scout cves <image>
```

**Pass**: No critical/high CVEs in base images
**Fail**: Outdated base images with known vulnerabilities

## Compose-Specific Checks

```bash
# File naming — modern convention is compose.yaml
ls compose.yaml compose.override.yaml 2>/dev/null
ls docker-compose.yml docker-compose.yaml 2>/dev/null

# Resource limits
grep -A5 "deploy:" compose*.yaml docker-compose*.yml 2>/dev/null | grep "limits"
grep "mem_limit\|cpus:" compose*.yaml docker-compose*.yml 2>/dev/null

# Named volumes vs bind mounts
grep "\\./" compose*.yaml docker-compose*.yml 2>/dev/null  # bind mounts (flag for prod)

# Deprecated CLI usage
grep "docker-compose" Makefile* scripts/*.sh 2>/dev/null  # should be docker compose

# Override structure
ls compose.override.yaml compose.prod.yaml compose.staging.yaml 2>/dev/null

# Verify merge output
docker compose config 2>/dev/null
```

### Compose Checklist

- [ ] Uses `compose.yaml` naming (not `docker-compose.yml`)
- [ ] Override files for dev (`compose.override.yaml`) and prod (`compose.prod.yaml`)
- [ ] `docker compose config` produces valid merged output
- [ ] Image versions pinned in all compose files
- [ ] Resource limits set for all services
- [ ] Named volumes for persistent data (no bind mounts in prod)
- [ ] Healthcheck defined for each service
- [ ] No use of deprecated `docker-compose` CLI in scripts

## External Tools

Run when available. Fall back to grep-based checks otherwise.

```bash
# Hadolint — Dockerfile linter (primary tool)
hadolint Dockerfile
hadolint --format json Dockerfile

# Trivy — vulnerability + misconfiguration scanner
trivy config Dockerfile
trivy image <built-image>

# Docker Scout — CVE scanning
docker scout cves <image>
docker scout recommendations <image>

# Dockle — container image linter
dockle <image>
```

## Audit Report Format

```markdown
# Docker Audit Report

**Date**: YYYY-MM-DD
**Scope**: [path]
**Files Scanned**: [list]

## Summary

| Severity | Count |
| -------- | ----- |
| Critical | 0     |
| High     | 0     |
| Medium   | 0     |
| Low      | 0     |

## Overall Score

[X/10 categories pass] — PASS / NEEDS WORK / FAIL

## Findings

### [Category] — [PASS/FAIL] (Severity)

- **File**: Dockerfile:14
- **Issue**: [description]
- **Fix**: [specific remediation]

## Dockerfile Checklist

- [ ] Image tags pinned (no :latest)
- [ ] Minimal base image (alpine/slim/distroless)
- [ ] Build cache optimized (deps before source)
- [ ] Non-root USER directive
- [ ] No secrets in Dockerfile/args
- [ ] .dockerignore exists and aggressive
- [ ] HEALTHCHECK defined
- [ ] Multi-stage build for production
- [ ] Layers combined and cleaned
- [ ] Base images scanned and current

## Compose Checklist

- [ ] Uses compose.yaml naming convention
- [ ] Override files for dev/prod separation
- [ ] Image versions pinned
- [ ] Resource limits set
- [ ] Named volumes (no bind mounts in prod)
- [ ] Healthcheck per service
- [ ] No deprecated docker-compose CLI usage

## Recommendations

### Immediate (Critical/High)

1. [action items]

### Short-Term (Medium)

1. [action items]

### Ongoing

1. [action items]
```

## Integration

- `/security-scan` — covers application code; `/docker-audit` covers container config
- `/infrastructure-setup` — creates Docker files; `/docker-audit` validates them
- `rules/docker.md` — always-on guardrails; this skill is the deep audit

## Tool Installation

```bash
# Hadolint (macOS)
brew install hadolint

# Trivy (macOS)
brew install trivy

# Dockle
brew install goodwithtech/r/dockle

# Docker Scout (built into Docker Desktop 4.17+)
docker scout version
```
