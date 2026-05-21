# CHANGELOG Entry Examples

Real-world examples of well-formatted CHANGELOG entries.

---

## Example 1: New Feature (MINOR)

**Scenario**: Added user authentication system
**Change Type**: `feat`
**Version**: 1.0.0 → 1.1.0

```markdown
## [1.1.0] - 2024-01-15

### Added

- User authentication system with email/password and OAuth support (#123)
  - JWT-based authentication with refresh tokens
  - Session management with configurable timeout
  - Password reset flow with email verification
- User profile management interface (#125)
- Role-based access control (RBAC) system (#126)

### Security

- Implemented bcrypt password hashing (#124)
- Added rate limiting for login attempts (5 per minute) (#127)
- CSRF protection for all authenticated endpoints (#128)

[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
```

---

## Example 2: Bug Fix (PATCH)

**Scenario**: Fixed memory leak
**Change Type**: `fix`
**Version**: 1.1.0 → 1.1.1

```markdown
## [1.1.1] - 2024-01-16

### Fixed

- Memory leak in cache manager causing gradual RAM increase (#129)
- Race condition in concurrent file uploads (#130)
- Incorrect timezone handling in date filters (#131)

[1.1.1]: https://github.com/user/repo/compare/v1.1.0...v1.1.1
```

---

## Example 3: Breaking Change (MAJOR)

**Scenario**: Changed authentication API
**Change Type**: `BREAKING CHANGE`
**Version**: 1.1.1 → 2.0.0

```markdown
## [2.0.0] - 2024-01-20

### Changed

- **BREAKING**: Authentication API now requires Bearer token in Authorization header (#132)
  - **Before**: `GET /api/resource?token=xxx`
  - **After**: `GET /api/resource` with `Authorization: Bearer xxx` header
  - **Migration**: Update all API clients to send token in header
  - Query parameter authentication removed in this version

- **BREAKING**: User model now requires email verification (#133)
  - All existing users marked as verified
  - New registrations require email confirmation
  - **Migration**: No action needed for existing users

### Added

- Improved token security with short-lived access tokens (#134)
- Automatic token refresh mechanism (#135)

### Deprecated

- `/auth/login-legacy` endpoint (use `/auth/login`) (#136)
  - Will be removed in v3.0.0

[2.0.0]: https://github.com/user/repo/compare/v1.1.1...v2.0.0
```

---

## Example 4: Security Update

**Scenario**: Security vulnerability fix
**Change Type**: `security`
**Version**: 2.0.0 → 2.0.1

```markdown
## [2.0.1] - 2024-01-21

### Security

- Fixed XSS vulnerability in comment system (CVE-2024-1234) (#137)
  - Input sanitization now applied to all user-generated content
  - Affected versions: 1.0.0 - 2.0.0
  - **Upgrade immediately**
- Updated dependencies to patch security vulnerabilities (#138)
  - lodash: 4.17.20 → 4.17.21 (prototype pollution)
  - axios: 0.21.1 → 0.21.4 (SSRF vulnerability)

### Fixed

- Prevented potential SQL injection in search endpoint (#139)

[2.0.1]: https://github.com/user/repo/compare/v2.0.0...v2.0.1
```

---

## Example 5: Performance Improvement

**Scenario**: Database optimization
**Change Type**: `perf`
**Version**: 2.0.1 → 2.0.2

```markdown
## [2.0.2] - 2024-01-22

### Performance

- Reduced page load time by 40% through lazy loading (#140)
- Optimized database queries for reports (#141)
  - Added composite indexes on frequently queried columns
  - Query time reduced from 2.5s to 0.3s
- Implemented Redis caching for API responses (#142)
  - Cache hit rate: ~85% for common requests
  - Average response time: 500ms → 50ms

### Changed

- Pagination now defaults to 50 items (was 100) (#143)

[2.0.2]: https://github.com/user/repo/compare/v2.0.1...v2.0.2
```

---

## Example 6: Documentation and Maintenance

**Scenario**: Documentation updates and dependency maintenance
**Change Type**: `docs`, `chore`
**Version**: 2.0.2 → 2.0.3

```markdown
## [2.0.3] - 2024-01-23

### Changed

- Updated README with new API examples (#144)
- Improved error messages for validation failures (#145)
- Enhanced logging for debugging (#146)

### Fixed

- Typo in configuration documentation (#147)
- Incorrect code example in API docs (#148)

[2.0.3]: https://github.com/user/repo/compare/v2.0.2...v2.0.3
```

---

## Example 7: Feature Deprecation

**Scenario**: Deprecating old API
**Change Type**: `deprecated`
**Version**: 2.0.3 → 2.1.0

```markdown
## [2.1.0] - 2024-01-25

### Added

- New v2 API with improved response format (#149)
- GraphQL endpoint for flexible queries (#150)

### Deprecated

- REST API v1 endpoints (#151)
  - `/api/v1/users` → use `/api/v2/users`
  - `/api/v1/products` → use `/api/v2/products`
  - **Removal scheduled**: v3.0.0 (Q2 2024)
  - **Migration guide**: See docs/migration-v2.md

- `GET /api/items?format=xml` parameter (#152)
  - XML format will be removed in v3.0.0
  - Use JSON format instead

[2.1.0]: https://github.com/user/repo/compare/v2.0.3...v2.1.0
```

---

## Quality Checklist

Before finalizing CHANGELOG entry:

- [ ] Version number follows semantic versioning
- [ ] Date is in YYYY-MM-DD format
- [ ] All changes categorized correctly
- [ ] Each entry has issue/PR reference (#number)
- [ ] Entries written from user perspective
- [ ] Breaking changes clearly marked with **BREAKING**
- [ ] Security fixes highlighted
- [ ] Migration instructions for breaking changes
- [ ] Comparison links updated at bottom
- [ ] No typos or grammar errors
