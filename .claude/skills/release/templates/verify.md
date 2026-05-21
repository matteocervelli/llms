# Release Integrity Verification

Verifies bidirectional consistency between commits, CHANGELOG, tags, and GitHub releases.

## Quick Start

```
/release verify              # auto-detect: `commits` if unreleased work, `tags` if clean main
/release verify commits      # every significant commit since last tag has a changelog entry
/release verify tags         # bidirectional tag↔changelog↔GitHub-release consistency
/release verify history      # full past-release integrity (tags, manifests, GH releases)
```

## Auto-Detection

When invoked without a subcommand:

```bash
LAST_TAG=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null)
UNRELEASED=$(git log --no-merges --oneline "${LAST_TAG:-$(git rev-list --max-parents=0 HEAD)}..HEAD" | wc -l)

if [[ "$UNRELEASED" -gt 0 ]]; then
  # Unreleased work exists → run `commits`
else
  # Clean state → run `tags`
fi
```

---

## Subcommand: `commits`

Verify that every significant commit since the last tag has a matching CHANGELOG entry.

### Algorithm

**1. Establish baseline:**

```bash
LAST_TAG=$(git describe --tags --abbrev=0 --match "v*" 2>/dev/null)
if [[ -z "$LAST_TAG" ]]; then
  LAST_TAG=$(git rev-list --max-parents=0 HEAD)
  echo "No version tags found — using root commit as baseline"
fi

COMMIT_COUNT=$(git log --no-merges --oneline "$LAST_TAG"..HEAD | wc -l)
if [[ "$COMMIT_COUNT" -gt 100 ]]; then
  echo "WARN: $COMMIT_COUNT commits since last tag — consider running /release plan first"
fi
```

**2. List commits:**

```bash
git log --no-merges --oneline "$LAST_TAG"..HEAD
```

**3. Parse [Unreleased] section from CHANGELOG.md:**

Extract content between `## [Unreleased]` and the next `## [` header.

**4. Match commits to changelog entries:**

Priority order for matching:

1. **Issue/PR ref match** `(#N)` — most reliable, check both commit message and changelog entry
2. **Text similarity** — match first 5 words after conventional commit prefix against changelog entry text → classify as `UNCERTAIN`

**5. Classify commits:**

**Significant** (require changelog entry):

- `feat:`, `fix:`, `perf:`, `security:`, `refactor:`, `docs:` prefixes

**Exempt** (no entry expected):

- `chore:`, `style:`, `test:`, `ci:`, `build:` prefixes
- Merge commits
- `chore: bump version` pattern

**6. Check for unreviewed agent signals:**

```bash
gh issue list -R "$REPO" --label ai-suggested --state open --json number --jq 'length'
```

If count > 0: add WARN finding `"N unreviewed ai-suggested issues in this repo"`.

**7. Gate:**

| Result | Condition                                                         |
| ------ | ----------------------------------------------------------------- |
| `PASS` | 0 unmatched significant commits AND 0 open `ai-suggested` issues  |
| `WARN` | 1–3 unmatched significant commits OR ≥1 open `ai-suggested` issue |
| `FAIL` | >3 unmatched significant commits                                  |

`UNCERTAIN` matches do not count toward FAIL.
Agent signals count as WARN only — they never block a release, they are a nudge to triage.

### Graceful Degradation

- No `CHANGELOG.md` → report `SKIPPED` (not FAIL)
- `gh` unavailable → skip GitHub-specific checks, report as `SKIPPED`

### Output Format

```
## Release Verify — Commits
- Last tag: v1.2.0
- Commits since: 15 (12 significant, 3 exempt)

### Matched (10)
- abc1234 feat: add search (#42) → Added: search feature (#42)
- def5678 fix: null check (#43) → Fixed: null pointer (#43)

### Unmatched (2) — WARN
- ghi9012 feat: new endpoint — no changelog entry found
- jkl3456 fix: edge case — no changelog entry found

### Uncertain (1)
- mno7890 refactor: auth module → Changed: refactor authentication (similarity match)

### Exempt (3)
- pqr1234 chore: update deps
- stu5678 test: add coverage
- vwx9012 ci: fix pipeline

Gate: WARN (2 unmatched)
→ Add missing entries to [Unreleased] or run /release changelog
```

---

## Subcommand: `tags`

Bidirectional consistency between git tags, CHANGELOG sections, and GitHub releases.

### Algorithm

**1. Collect tags and changelog sections:**

```bash
# All version tags
git tag -l 'v*' --sort=-v:refname

# CHANGELOG version headers
grep -n '^## \[' CHANGELOG.md | grep -v 'Unreleased'
```

**2. Bidirectional check:**

- Every `v*` tag has a matching `## [X.Y.Z]` section in CHANGELOG
- Every `## [X.Y.Z]` section has a matching `v*` tag

**3. GitHub release per tag:**

```bash
# Check each tag has a GitHub release
gh release view vX.Y.Z --json tagName,name,body 2>/dev/null
```

**3b. Forgejo release per tag (if Forgejo remote exists):**

```bash
# Guard: skip if no Forgejo push remote

  # Fetch all Forgejo releases and collect tag names

  # Detect .forgejo/workflows/release.yml presence
  RELEASE_YML=$([ -f ".forgejo/workflows/release.yml" ] && echo "present" || echo "absent")

  # For each tag, check if a Forgejo release exists
  for TAG in $(git tag -l 'v*' --sort=-v:refname); do
      echo "FJ: $TAG ✓"
    else
      echo "FJ: $TAG MISSING (release.yml: $RELEASE_YML)"
    fi
  done
fi
```

**3c. Artifact publication check (if publish workflows exist):**

**3c-preamble: Detect expected artifacts (once, before per-tag loop)**

Scan `.forgejo/workflows/*.yml` for publish indicators. Detection is workflow-driven — a project marker alone (e.g., `pyproject.toml`) is not enough; there must be a workflow that actually publishes.

| Indicator in workflow YAML                                         | Artifact type       | Package name source                                                         |
| ------------------------------------------------------------------ | ------------------- | --------------------------------------------------------------------------- |
| `uv publish` or `UV_PUBLISH_URL`                                   | `forgejo-pypi`      | `pyproject.toml [project].name`                                             |
| `pnpm publish` or `npm publish`                                    | `forgejo-npm`       | `package.json .name` (root if not `private: true`; scan sub-dirs otherwise) |
| `twine upload` targeting `upload.pypi.org`                         | `public-pypi`       | same as forgejo-pypi                                                        |
| `publishConfig` → `registry.npmjs.org`                             | `public-npm`        | same as forgejo-npm                                                         |
| `docker/login-action` without registry (defaults to Docker Hub)    | `public-docker`     | `images:` field in workflow                                                 |
| `gh release upload` or `softprops/action-gh-release` with `files:` | `gh-release-assets` | filename pattern from workflow                                              |

```bash
EXPECTED_ARTIFACTS=()
PKG_NAME=""
NPM_NAMES=()
CONTAINER_NAME=""

if ls .forgejo/workflows/*.yml 2>/dev/null | xargs grep -l 'uv publish\|UV_PUBLISH_URL' >/dev/null 2>&1; then
  PKG_NAME=$(python3 -c "
import tomllib
with open('pyproject.toml', 'rb') as f:
    print(tomllib.load(f)['project']['name'])
" 2>/dev/null)
  [[ -n "$PKG_NAME" ]] && EXPECTED_ARTIFACTS+=("forgejo-pypi:$PKG_NAME")
fi

if ls .forgejo/workflows/*.yml 2>/dev/null | xargs grep -l 'pnpm publish\|npm publish' >/dev/null 2>&1; then
  ROOT_PRIVATE=$(python3 -c "import json; d=json.load(open('package.json')); print(str(d.get('private',False)).lower())" 2>/dev/null)
  if [[ "$ROOT_PRIVATE" == "true" ]]; then
    for pkg_json in */package.json; do
      pkg_name=$(python3 -c "import json; d=json.load(open('$pkg_json')); print(d['name'])" 2>/dev/null)
      [[ -n "$pkg_name" ]] && NPM_NAMES+=("$pkg_name") && EXPECTED_ARTIFACTS+=("forgejo-npm:$pkg_name")
    done
  else
    pkg_name=$(python3 -c "import json; d=json.load(open('package.json')); print(d['name'])" 2>/dev/null)
    [[ -n "$pkg_name" ]] && NPM_NAMES+=("$pkg_name") && EXPECTED_ARTIFACTS+=("forgejo-npm:$pkg_name")
  fi
fi

if ls .forgejo/workflows/*.yml 2>/dev/null | xargs grep -l 'docker/build-push-action' 2>/dev/null | xargs grep -l 'push: true' >/dev/null 2>&1; then
  REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
  EXPECTED_ARTIFACTS+=("forgejo-container:$CONTAINER_NAME")
fi

if ls .forgejo/workflows/*.yml 2>/dev/null | xargs grep -l 'upload.pypi.org' >/dev/null 2>&1; then
  [[ -n "$PKG_NAME" ]] && EXPECTED_ARTIFACTS+=("public-pypi:$PKG_NAME")
fi

if ls .forgejo/workflows/*.yml 2>/dev/null | xargs grep -l 'registry.npmjs.org' >/dev/null 2>&1; then
  for n in "${NPM_NAMES[@]}"; do EXPECTED_ARTIFACTS+=("public-npm:$n"); done
fi

if ls .forgejo/workflows/*.yml 2>/dev/null | xargs grep -l 'gh release upload\|softprops/action-gh-release' 2>/dev/null | xargs grep -l 'files:' >/dev/null 2>&1; then
  EXPECTED_ARTIFACTS+=("gh-release-assets")
fi

if [[ ${#EXPECTED_ARTIFACTS[@]} -eq 0 ]]; then
  echo "Artifacts: SKIP (no publish workflows detected)"
fi
```

**3c-fetch: Batch fetch published versions (one call per artifact type)**

Version normalization: strip `v` prefix for PyPI/npm (`v1.2.0` → `1.2.0`). Container images may use both the semver tag and the commit SHA — check both.

```bash

if [[ -n "$PKG_NAME" ]] && echo "${EXPECTED_ARTIFACTS[*]}" | grep -q "forgejo-pypi"; then
  PYPI_VERSIONS=$(echo "$PYPI_RAW" | \
    python3 -c "import json,sys; [print(p['version']) for p in json.load(sys.stdin)]" 2>/dev/null)
  PYPI_FIRST_PUBLISH=$(echo "$PYPI_RAW" | python3 -c "
import json, sys
pkgs = json.load(sys.stdin)
if pkgs:
    dates = [p['created'] for p in pkgs if 'created' in p]
    print(min(dates) if dates else '')
" 2>/dev/null)
fi

for npm_name in "${NPM_NAMES[@]}"; do
    python3 -c "import json,sys; [print(p['version']) for p in json.load(sys.stdin)]" 2>/dev/null || true)
  eval "NPM_VERSIONS_${npm_name//[^a-zA-Z0-9]/_}='$npm_versions'"
done

if [[ -n "$CONTAINER_NAME" ]] && echo "${EXPECTED_ARTIFACTS[*]}" | grep -q "forgejo-container"; then
    python3 -c "import json,sys; [print(p['version']) for p in json.load(sys.stdin)]" 2>/dev/null || true)
fi

if echo "${EXPECTED_ARTIFACTS[*]}" | grep -q "public-pypi"; then
  PUBLIC_PYPI_VERSIONS=$(curl -s "https://pypi.org/pypi/${PKG_NAME}/json" | \
    python3 -c "import json,sys; print('\n'.join(json.load(sys.stdin).get('releases',{}).keys()))" 2>/dev/null)
fi
```

**3c-verify: Per-tag artifact status (inside existing tag loop)**

```bash
VERSION="${TAG#v}"
TAG_SHA=$(git rev-parse --short=12 "$TAG" 2>/dev/null)

ARTIFACT_STATUS=()

if echo "${EXPECTED_ARTIFACTS[*]}" | grep -q "forgejo-pypi"; then
    ARTIFACT_STATUS+=("pypi:SKIP(no-auth)")
  elif echo "$PYPI_VERSIONS" | grep -qx "$VERSION"; then
    ARTIFACT_STATUS+=("pypi:OK")
  else
    TAG_DATE=$(git log -1 --format="%cI" "$TAG" 2>/dev/null)
    if [[ -n "$PYPI_FIRST_PUBLISH" && -n "$TAG_DATE" ]] && \
       python3 -c "import sys; sys.exit(0 if '$TAG_DATE' < '$PYPI_FIRST_PUBLISH' else 1)" 2>/dev/null; then
      ARTIFACT_STATUS+=("pypi:SKIP(pre-registry)")
    else
      ARTIFACT_STATUS+=("pypi:MISSING")
    fi
  fi
fi

if echo "${EXPECTED_ARTIFACTS[*]}" | grep -q "forgejo-container"; then
  if echo "$CONTAINER_VERSIONS" | grep -qx "$VERSION" || echo "$CONTAINER_VERSIONS" | grep -qx "$TAG_SHA"; then
    ARTIFACT_STATUS+=("container:OK")
  elif echo "$CONTAINER_VERSIONS" | grep -q "."; then
    ARTIFACT_STATUS+=("container:SKIP(SHA-tagged)")
  else
    ARTIFACT_STATUS+=("container:MISSING")
  fi
fi

if echo "${EXPECTED_ARTIFACTS[*]}" | grep -q "public-pypi"; then
  if echo "$PUBLIC_PYPI_VERSIONS" | grep -qx "$VERSION"; then
    ARTIFACT_STATUS+=("pypi.org:OK")
  else
    ARTIFACT_STATUS+=("pypi.org:MISSING")
  fi
fi

if echo "${EXPECTED_ARTIFACTS[*]}" | grep -q "gh-release-assets"; then
  ASSET_COUNT=$(gh release view "$TAG" --json assets --jq '.assets | length' 2>/dev/null || echo "0")
  if [[ "$ASSET_COUNT" -gt 0 ]]; then
    ARTIFACT_STATUS+=("gh-assets:${ASSET_COUNT}files")
  else
    ARTIFACT_STATUS+=("gh-assets:MISSING")
  fi
fi
```

If no publish workflows exist, omit the `Artifacts` column entirely from the output.
Token missing or API error → classify as `SKIP(auth)` or `ERROR` — does not affect gate.

> **Future artifact types** (add when relevant):
> `forgejo-cargo`, `forgejo-go`, `forgejo-helm`, `public-npm`, `public-docker`.

---

**4. Date consistency:**

Compare tag date vs CHANGELOG section date (7-day tolerance):

```bash
git log -1 --format="%ci" vX.Y.Z
```

**5. Comparison links audit:**

Check that CHANGELOG has comparison links at the bottom for each version:

```
[X.Y.Z]: https://github.com/owner/repo/compare/vX.Y-1.Z...vX.Y.Z
```

**6. Gate:**

| Result | Condition                                                                              |
| ------ | -------------------------------------------------------------------------------------- |
| `PASS` | All tags ↔ sections match, GH/FJ releases present, all expected artifacts published    |
| `WARN` | GH **or** Forgejo release missing for a tag **OR** expected artifact MISSING for a tag |
| `FAIL` | Tag without section OR section without tag                                             |

Artifact MISSING → WARN (not FAIL).

### Output Format

**With publish workflows detected:**

```
## Release Verify — Tags

| Version | Tag | CHANGELOG | GH Release | FJ Release | Artifacts | Date Match |
|---|---|---|---|---|---|---|
| 1.2.0 | v1.2.0 | ## [1.2.0] | Yes | Yes | pypi OK | Yes (same day) |
| 1.1.0 | v1.1.0 | ## [1.1.0] | Missing | Yes | pypi OK | Yes |
| 1.0.0 | v1.0.0 | ## [1.0.0] | Yes | Missing | pypi MISSING | WARN (8 days) |

Comparison links: 2/3 present (missing: v1.0.0)

Gate: WARN (1 missing GH release, 1 missing FJ release, 1 missing pypi artifact, 1 missing comparison link)
```

**Without publish workflows:**

```
## Release Verify — Tags

| Version | Tag | CHANGELOG | GH Release | FJ Release | Date Match |
|---|---|---|---|---|---|
| 1.2.0 | v1.2.0 | ## [1.2.0] | Yes | Yes | Yes (same day) |

Artifacts: SKIP (no publish workflows detected)
Comparison links: 1/1 present

Gate: PASS
```

---

## Subcommand: `history`

Full past-release integrity — extends `tags` with deeper checks per release.

### Additional Checks Per Release

```bash
# Tag type (annotated vs lightweight)
git cat-file -t vX.Y.Z 2>/dev/null  # "tag" = annotated, "commit" = lightweight

# Tag ancestry (is it on main?)
git merge-base --is-ancestor vX.Y.Z main && echo "on main" || echo "NOT on main"

# Manifest version at tag
git show vX.Y.Z:pyproject.toml 2>/dev/null | grep 'version'
git show vX.Y.Z:package.json 2>/dev/null | grep '"version"'

# GH release body non-empty
gh release view vX.Y.Z --json body --jq '.body | length' 2>/dev/null
```

### Output Format

```
## Release Verify — History

| Version | Annotated | On Main | Manifest | GH Body |
|---|---|---|---|---|
| 1.2.0 | Yes | Yes | 1.2.0 | 245 chars |
| 1.1.0 | No (lightweight) | Yes | 1.1.0 | Empty |
| 1.0.0 | Yes | Yes | 0.9.0 (MISMATCH) | 189 chars |

Gate: FAIL (v1.0.0 manifest version mismatch)
```

---

## Integration Points

- **`/health releases`** — delegates to `/release verify tags`
- **`/pr-creator` Step 1.5** — delegates to `/release verify commits`
- **`/pr-merge` Step 6** — references for post-merge readiness
- **`/progress`** — release state informs routing suggestions

## Related Skills

- `/release changelog` — fix missing entries found by `commits`
- `/release plan` — scope a version when too many unreleased commits
- `/health full` — includes `releases` dimension
- `/pr-merge` — Step 6 guides next steps based on release state
