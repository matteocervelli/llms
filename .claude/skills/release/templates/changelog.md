# CHANGELOG Generator

## Purpose

Systematic guidance for generating CHANGELOG entries following conventional commits format and semantic versioning principles.

## When to Use

- After feature implementation
- Need to document changes
- Determining version increments
- Creating release notes

## Templates

| Template               | Purpose                   |
| ---------------------- | ------------------------- |
| `changelog-format.md`  | Standard CHANGELOG format |
| `changelog-entries.md` | Real-world entry examples |

## Workflow

### 1. Analyze Changes

```bash
# View commits since last release
git log --oneline main..HEAD

# View files changed
git diff --stat main..HEAD
```

Identify:

- New features
- Bug fixes
- Breaking changes
- Security fixes
- Deprecations

### 2. Determine Change Type

| Type              | Description     | Version |
| ----------------- | --------------- | ------- |
| `feat`            | New feature     | MINOR   |
| `fix`             | Bug fix         | PATCH   |
| `BREAKING CHANGE` | Breaking change | MAJOR   |
| `docs`            | Documentation   | PATCH   |
| `perf`            | Performance     | PATCH   |

### 3. Calculate Version

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes (2.0.0)
MINOR: New features (1.3.0)
PATCH: Bug fixes (1.2.4)
```

### 4. Generate Entry

Use `changelog-format.md`:

```markdown
## [1.3.0] - 2024-01-15

### Added

- User authentication with JWT tokens (#123)

### Fixed

- Memory leak in cache manager (#124)

### Security

- Rate limiting for login attempts (#125)
```

### 5. Update CHANGELOG.md

Edit CHANGELOG.md to promote the `[Unreleased]` section to a versioned release entry:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added

- ...

### Fixed

- ...
```

Add a comparison link at the bottom:

```markdown
[1.3.0]: https://github.com/owner/repo/compare/v1.2.0...v1.3.0
```

### 5b. Date Freshness Check

Extract the date from the newly created CHANGELOG section and verify it matches today:

```bash
# Extract date from the newest version header (first non-Unreleased entry)
ENTRY_DATE=$(grep -m1 '^## \[[0-9]' CHANGELOG.md | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
TODAY=$(date +%Y-%m-%d)

if [[ -z "$ENTRY_DATE" ]]; then
  echo "WARN: Could not extract date from CHANGELOG header"
elif [[ "$ENTRY_DATE" != "$TODAY" ]]; then
  echo "⚠ WARN: CHANGELOG date is $ENTRY_DATE but today is $TODAY"
  # Check if release.yml will auto-publish this on tag push
  if [ -f ".forgejo/workflows/release.yml" ]; then
    echo "  .forgejo/workflows/release.yml is present — stale date will be published automatically on tag push."
  fi
  echo "  Update the date before tagging."
fi
```

If the dates differ, prompt the user to confirm or update the date before proceeding with the version bump.

### 6. Apply Version Bump

After the CHANGELOG entry is confirmed, propagate the version to all project files.

#### 6.1 Detect version files

```bash
for f in pyproject.toml package.json setup.cfg Cargo.toml; do [ -f "$f" ] && echo "$f"; done
```

If the loop prints nothing: note "No version files detected in repo root — skipping propagation."
If one or more files are printed: proceed with the relevant steps below.

**Python (uv) lockfile**: If `pyproject.toml` exists, also check for `uv.lock` — `uv` automatically
updates it to reflect the new version string. It must be committed alongside `pyproject.toml`.

```bash
# Check if uv.lock exists (may be nested, e.g. backend/uv.lock)
find . -name "uv.lock" -not -path "*/node_modules/*" 2>/dev/null
```

#### 6.2 Update `pyproject.toml` (Python projects)

Locate the `version` field under `[project]`:

```bash
grep -n 'version' pyproject.toml
```

Edit `pyproject.toml` — replace only the `version = "..."` line under `[project]`:

```toml
[project]
version = "X.Y.Z"
```

Also check `src/__init__.py` or the package's `__version__` if present:

```bash
grep -rn '__version__' src/ 2>/dev/null | head -5
```

If found, update with the same version string.

#### 6.3 Update `package.json` (Node projects)

```bash
# In-place version update using jq (preferred)
TMP=$(mktemp) && jq --arg v "X.Y.Z" '.version = $v' package.json > "$TMP" && mv "$TMP" package.json
```

If `jq` is unavailable, edit `package.json` directly — replace only the top-level `"version"` field.

#### 6.4 Update `setup.cfg` (legacy Python)

```bash
grep -n 'version' setup.cfg
```

Edit `setup.cfg` — replace the `version = X.Y.Z` line under `[metadata]`.

#### 6.5 Update `Cargo.toml` (Rust projects)

Edit `Cargo.toml` — replace the `version = "X.Y.Z"` line under `[package]`.

#### 6.6 Update README version badge (if present)

```bash
grep -n 'version' README.md | grep -i 'badge\|shield\|img.shields' | head -5
```

If a version badge is found (e.g., `![version](https://img.shields.io/badge/version-X.Y.Z-...)`),
edit README.md to replace the old version string in the badge URL with the new version.

#### 6.7 Propose commit (user confirms before executing)

Stage only the files that were actually modified in steps 5–6.2:

```bash
# Stage each file only if it exists and was modified
git diff --name-only | grep -E 'CHANGELOG\.md|pyproject\.toml|package\.json|setup\.cfg|Cargo\.toml|README\.md|__init__\.py|uv\.lock' | xargs git add
git diff --cached --stat
```

Note: this covers root-level version files only. For monorepos with nested packages,
manually stage any additional modified files shown by `git status --short`.

**Python (uv) projects**: `uv.lock` will be modified by the version bump and MUST be included.
Always run `git status --short` after staging to catch any `uv.lock` files in subdirectories
(e.g. `backend/uv.lock`) that the grep above may miss.

Show the staged diff summary to the user, then propose:

```bash
git commit -m "chore: bump version to X.Y.Z"
```

**Wait for explicit user confirmation before running the commit.**

## Entry Categories

| Category        | Use For                |
| --------------- | ---------------------- |
| **Added**       | New features           |
| **Changed**     | Existing functionality |
| **Fixed**       | Bug fixes              |
| **Deprecated**  | Future removal         |
| **Removed**     | Deleted features       |
| **Security**    | Security fixes         |
| **Performance** | Speed improvements     |

## Writing Guidelines

**DO:**

- Start with verb: "Add", "Fix", "Update"
- Include issue reference (#123)
- Be specific and clear
- Write from user perspective

**DON'T:**

- Use vague descriptions
- Skip references
- Hide breaking changes

### Good Example

```markdown
### Added

- User authentication system with JWT and OAuth support (#123)
  - Supports email/password and social login
  - Includes session management
```

### Bad Example

```markdown
### Added

- Auth stuff
```

## Breaking Changes

Mark clearly with **BREAKING**:

```markdown
### Changed

- **BREAKING**: Auth API requires Bearer token header (#126)
  - **Before**: `GET /api?token=xxx`
  - **After**: `GET /api` with `Authorization: Bearer xxx`
  - **Migration**: Update clients to use header
```

## Quality Checklist

- [ ] Version follows semver
- [ ] Date in YYYY-MM-DD
- [ ] All changes categorized
- [ ] Issue references included
- [ ] Breaking changes marked
- [ ] User perspective maintained
- [ ] Comparison links updated
- [ ] Version files updated (`pyproject.toml` / `package.json` / `Cargo.toml` / README badge)
- [ ] Date matches intended release date (not a stale draft date)
