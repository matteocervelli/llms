# CHANGELOG Format Template

Standard format for CHANGELOG.md following Keep a Changelog conventions.

---

## File Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.0] - 2024-01-15

### Added

- User authentication system with JWT tokens (#123)
- Password reset functionality (#125)
- Email verification for new accounts (#126)

### Changed

- Updated user profile API to include avatar URL (#127)
- Improved error messages for validation failures (#128)

### Fixed

- Memory leak in cache manager (#124)
- Race condition in concurrent requests (#129)

### Security

- Implemented rate limiting for login attempts (#130)
- Added CSRF protection for all forms (#131)

### Performance

- Optimized database queries with proper indexing (#132)
- Reduced API response time by 40% (#133)

### Deprecated

- `/api/v1/users` endpoint (use `/api/v2/users`) (#134)

### Removed

- Legacy authentication method (#135)

## [1.2.3] - 2024-01-01

### Fixed

- Critical bug in payment processing (#120)

[Unreleased]: https://github.com/user/repo/compare/v1.3.0...HEAD
[1.3.0]: https://github.com/user/repo/compare/v1.2.3...v1.3.0
[1.2.3]: https://github.com/user/repo/compare/v1.2.2...v1.2.3
```

---

## Entry Categories

| Category        | Use For                           | Example                        |
| --------------- | --------------------------------- | ------------------------------ |
| **Added**       | New features, new capabilities    | "User authentication system"   |
| **Changed**     | Changes in existing functionality | "Updated API response format"  |
| **Fixed**       | Bug fixes                         | "Memory leak in cache manager" |
| **Deprecated**  | Features marked for removal       | "Legacy API endpoints"         |
| **Removed**     | Removed features                  | "Support for IE 11"            |
| **Security**    | Security improvements/fixes       | "Rate limiting for login"      |
| **Performance** | Performance improvements          | "Optimized database queries"   |

---

## Writing Guidelines

### Good Entry Examples

```markdown
### Added

- User authentication system with JWT tokens and refresh token support (#123)
  - Supports email/password and OAuth providers
  - Includes session management and logout functionality

### Changed

- **BREAKING**: Authentication API now requires `Authorization` header instead of query parameter (#126)
- Database schema updated to support user roles (#127)

### Fixed

- Memory leak in cache manager causing high RAM usage (#124)

### Security

- Implemented rate limiting (100 req/min per IP) to prevent brute force attacks (#130)
- Updated dependencies to fix security vulnerabilities (CVE-2024-1234) (#132)
```

### Bad Entry Examples

```markdown
### Added

- Authentication stuff
- Password thing

### Changed

- Auth API changed
```

---

## Semantic Versioning Quick Reference

| Change Type     | Version Impact | Example       |
| --------------- | -------------- | ------------- |
| Breaking change | MAJOR (X.0.0)  | 1.2.3 → 2.0.0 |
| New feature     | MINOR (0.X.0)  | 1.2.3 → 1.3.0 |
| Bug fix         | PATCH (0.0.X)  | 1.2.3 → 1.2.4 |

---

## Conventional Commit Types

| Type              | Description      | Version Impact |
| ----------------- | ---------------- | -------------- |
| `feat`            | New feature      | MINOR          |
| `fix`             | Bug fix          | PATCH          |
| `docs`            | Documentation    | PATCH          |
| `style`           | Code style       | PATCH          |
| `refactor`        | Code refactoring | PATCH          |
| `perf`            | Performance      | PATCH          |
| `test`            | Tests            | PATCH          |
| `chore`           | Maintenance      | PATCH          |
| `BREAKING CHANGE` | Breaking change  | MAJOR          |
