# Code Review Checklist

This comprehensive checklist covers all aspects of code quality, testing, performance, security, and style for thorough code reviews.

---

## 1. CODE QUALITY

### File Organization (10 items)

- [ ] **File size ≤ 500 lines** - Large files should be split by responsibility
- [ ] **Single responsibility** - File has one clear purpose
- [ ] **Logical module structure** - Related functionality grouped together
- [ ] **Appropriate file location** - File in correct directory (src/, tests/, etc.)
- [ ] **Clear file naming** - Name reflects file purpose
- [ ] **No circular dependencies** - Imports don't create circular references
- [ ] **Proper __init__.py** - Package initialization files present (Python)
- [ ] **Directory structure follows conventions** - Matches project layout
- [ ] **No unused files** - No dead code files in repository
- [ ] **Version control appropriate** - No generated files or binaries in git

### Naming Conventions (15 items)

- [ ] **Variable names descriptive** - `user_count` not `uc`
- [ ] **Function names verb-noun pattern** - `get_user()`, `calculate_total()`
- [ ] **Class names PascalCase** - `UserManager`, `DataProcessor`
- [ ] **Constants UPPER_CASE** - `MAX_RETRIES`, `API_KEY`
- [ ] **Private members prefixed** - `_internal_method()`, `_private_var`
- [ ] **No single-letter names** - Except loop counters (`i`, `j`, `k`)
- [ ] **Boolean names are questions** - `is_valid`, `has_permission`, `can_access`
- [ ] **No abbreviations** - Unless widely recognized (HTTP, API, URL)
- [ ] **Consistent terminology** - Same concept uses same names throughout
- [ ] **No Hungarian notation** - Don't encode type in name (`strName`)
- [ ] **Context-appropriate names** - Name clarity within its scope
- [ ] **No misleading names** - Name accurately reflects purpose
- [ ] **Plural for collections** - `users` not `user` for lists
- [ ] **Specific over generic** - `user_repository` not `data_handler`
- [ ] **Module names lowercase** - `user_service.py` not `UserService.py`

### Type Hints (12 items)

- [ ] **All function parameters typed** - Every parameter has type annotation
- [ ] **All return types specified** - Functions have return type annotation
- [ ] **Complex types properly annotated** - Use `List[str]`, `Dict[str, int]`, etc.
- [ ] **Optional types used correctly** - `Optional[str]` for nullable values
- [ ] **Union types when appropriate** - `Union[str, int]` for multiple types
- [ ] **Generic types specified** - `List[User]` not just `List`
- [ ] **Type aliases for complex types** - Create alias for repeated complex types
- [ ] **Protocol/ABC for interfaces** - Use Protocol or ABC for interfaces
- [ ] **No bare `Any`** - Avoid `Any` unless absolutely necessary
- [ ] **Callable types specified** - `Callable[[int, str], bool]` for functions
- [ ] **TypeVar used correctly** - For generic functions and classes
- [ ] **Type hints not in docstrings** - Use annotations, not documentation

### Docstrings (15 items)

- [ ] **Google-style format** - Follows Google Python Style Guide
- [ ] **All public functions documented** - Every public function has docstring
- [ ] **All public classes documented** - Every public class has docstring
- [ ] **Clear purpose description** - First line summarizes purpose
- [ ] **Args section complete** - All parameters documented
- [ ] **Args include types** - Parameters show type information
- [ ] **Returns section present** - Return value documented
- [ ] **Returns includes type** - Return type specified
- [ ] **Raises section when applicable** - Exceptions documented
- [ ] **Examples when helpful** - Complex functions have usage examples
- [ ] **No outdated documentation** - Docstrings match current implementation
- [ ] **Concise yet clear** - Not too verbose, not too terse
- [ ] **No redundant information** - Don't repeat what's obvious from code
- [ ] **Module-level docstring** - Module purpose documented at top
- [ ] **Multi-line format correct** - Proper indentation and line breaks

### Error Handling (15 items)

- [ ] **Appropriate exception types** - Use specific exceptions, not generic
- [ ] **Custom exceptions when needed** - Create domain-specific exceptions
- [ ] **Error messages clear** - Messages explain what went wrong and why
- [ ] **No bare except** - Always specify exception type
- [ ] **No silent failures** - Don't catch and ignore without logging
- [ ] **Cleanup in finally** - Resources released in finally blocks
- [ ] **Context managers for resources** - Use `with` for file/connection handling
- [ ] **Fail fast** - Check preconditions early
- [ ] **Meaningful exception messages** - Include context (values, state)
- [ ] **Don't catch Exception broadly** - Catch specific exceptions only
- [ ] **Re-raise with context** - Use `raise ... from` to preserve stack trace
- [ ] **Validation at boundaries** - Validate inputs at public API boundaries
- [ ] **Error logging appropriate** - Errors logged with sufficient detail
- [ ] **No exception for control flow** - Don't use exceptions for normal flow
- [ ] **Graceful degradation** - System handles errors gracefully

### Function Design (15 items)

- [ ] **Single responsibility** - Function does one thing well
- [ ] **Function size ≤ 50 lines** - Large functions should be split
- [ ] **Low complexity** - Cyclomatic complexity ≤ 10
- [ ] **Few parameters (≤ 5)** - Use objects for many parameters
- [ ] **No side effects** - Pure functions preferred
- [ ] **Immutable by default** - Don't modify input parameters
- [ ] **Return early** - Avoid deep nesting with early returns
- [ ] **No flag parameters** - Split function instead of boolean flags
- [ ] **Consistent abstraction level** - All operations at same level
- [ ] **No hidden dependencies** - Dependencies explicit in parameters
- [ ] **Testable design** - Easy to write tests for function
- [ ] **No global state** - Don't rely on or modify globals
- [ ] **Idempotent when possible** - Same input = same output
- [ ] **Clear entry/exit points** - One entry, one exit (or early returns)
- [ ] **Async for I/O operations** - Use async/await for I/O-bound work

### Class Design (12 items)

- [ ] **Single responsibility** - Class has one reason to change
- [ ] **Small class size** - Class ≤ 300 lines
- [ ] **Composition over inheritance** - Favor composition
- [ ] **Dependency injection** - Dependencies passed in, not created
- [ ] **Interface segregation** - Small, focused interfaces
- [ ] **Liskov substitution** - Subtypes can replace base types
- [ ] **Immutable when possible** - Prefer immutable objects
- [ ] **No god objects** - No classes that do everything
- [ ] **Proper encapsulation** - Private members truly private
- [ ] **No static mutable state** - Class variables should be immutable
- [ ] **Factory methods when complex** - Use factories for complex creation
- [ ] **Clear constructor** - `__init__` does minimal work

### Code Structure (10 items)

- [ ] **No code duplication** - DRY principle followed
- [ ] **Max nesting depth 3** - Deeply nested code is refactored
- [ ] **No magic numbers** - Use named constants
- [ ] **Clear control flow** - Easy to follow logic
- [ ] **Proper indentation** - Consistent 4-space indentation (Python)
- [ ] **Blank lines appropriate** - Logical separation with blank lines
- [ ] **Import organization** - Grouped and sorted correctly
- [ ] **No commented-out code** - Remove dead code
- [ ] **TODOs have owners/dates** - `# TODO(username): description`
- [ ] **No print statements** - Use logging instead

---

## 2. TESTING

### Test Coverage (10 items)

- [ ] **80%+ code coverage** - Minimum coverage threshold met
- [ ] **All public functions tested** - Every public API has tests
- [ ] **Edge cases covered** - Boundary values tested
- [ ] **Error paths tested** - Exception handling tested
- [ ] **Happy path tested** - Normal execution tested
- [ ] **Integration points tested** - Interactions between modules tested
- [ ] **No untested complex logic** - Complex algorithms have tests
- [ ] **Critical paths well-tested** - Security/payment logic thoroughly tested
- [ ] **Mock external dependencies** - Network/DB calls mocked in unit tests
- [ ] **Coverage report generated** - Can verify coverage metrics

### Test Quality (15 items)

- [ ] **Clear test names** - `test_function_condition_expected` pattern
- [ ] **Arrange-Act-Assert** - Tests follow AAA pattern
- [ ] **One assertion per test** - Or multiple related assertions
- [ ] **Independent tests** - Tests don't depend on each other
- [ ] **Repeatable tests** - Same result every run
- [ ] **Fast tests** - Unit tests run quickly (< 100ms each)
- [ ] **Proper fixtures** - Setup/teardown handled correctly
- [ ] **Meaningful assertions** - Assertions verify specific behavior
- [ ] **No flaky tests** - Tests don't randomly fail
- [ ] **Test data realistic** - Test data matches real-world scenarios
- [ ] **Cleanup after tests** - Resources cleaned up properly
- [ ] **Test isolation** - Tests don't affect each other
- [ ] **Error messages helpful** - Test failures clearly indicate problem
- [ ] **Parametrized where appropriate** - Use parametrize for similar tests
- [ ] **Test documentation** - Complex tests have docstrings

### Test Organization (8 items)

- [ ] **One test file per source file** - `test_module.py` for `module.py`
- [ ] **Test classes for grouping** - Related tests in classes
- [ ] **Test files in tests/ directory** - Proper test directory structure
- [ ] **Test discovery works** - pytest/unittest can find tests
- [ ] **Fixtures in conftest.py** - Shared fixtures properly located
- [ ] **Integration tests separate** - In tests/integration/ directory
- [ ] **Test helpers separate** - Test utilities in proper location
- [ ] **No business logic in tests** - Tests don't duplicate business logic

---

## 3. PERFORMANCE

### Algorithm Efficiency (10 items)

- [ ] **Optimal complexity** - Best known algorithm for problem
- [ ] **No unnecessary loops** - Loops not nested when avoidable
- [ ] **Efficient data structures** - Right structure for use case
- [ ] **No repeated calculations** - Cache expensive operations
- [ ] **Early termination** - Stop when result found
- [ ] **Batch operations** - Process items in batches
- [ ] **Parallel processing** - Use multiprocessing/threading when appropriate
- [ ] **Lazy evaluation** - Compute only when needed
- [ ] **Streaming for large data** - Don't load everything into memory
- [ ] **No premature optimization** - Optimize bottlenecks only

### Memory Usage (10 items)

- [ ] **No memory leaks** - Resources properly released
- [ ] **Generators for large data** - Use generators instead of lists
- [ ] **Proper resource cleanup** - Files/connections closed
- [ ] **No unnecessary copies** - Avoid copying large objects
- [ ] **Weak references when appropriate** - For caches or observers
- [ ] **Memory profiling done** - For memory-intensive operations
- [ ] **No global caches** - Or caches have size limits
- [ ] **Efficient string operations** - Use join(), not concatenation in loops
- [ ] **Database connections managed** - Connection pooling used
- [ ] **No circular references** - Avoid reference cycles

### I/O Optimization (10 items)

- [ ] **Async for I/O operations** - Use async/await for I/O
- [ ] **Batch database queries** - Reduce round trips
- [ ] **Query optimization** - Proper indexes, avoid N+1 queries
- [ ] **File operations buffered** - Use buffering for file I/O
- [ ] **Caching implemented** - Cache expensive operations
- [ ] **Rate limiting** - Don't overwhelm external services
- [ ] **Connection pooling** - Reuse connections
- [ ] **Lazy loading** - Load data only when needed
- [ ] **Pagination for large results** - Don't return huge result sets
- [ ] **CDN for static assets** - Offload static file serving

---

## 4. SECURITY

### Input Validation (15 items)

- [ ] **All inputs validated** - Every external input checked
- [ ] **Type checking** - Input types verified
- [ ] **Range checking** - Numeric inputs within bounds
- [ ] **Length checking** - String lengths validated
- [ ] **Format validation** - Formats (email, URL) validated
- [ ] **Whitelist over blacklist** - Allow known good, not block known bad
- [ ] **Sanitization applied** - Dangerous characters removed/escaped
- [ ] **No trust in client data** - Server validates everything
- [ ] **File upload validation** - File types, sizes validated
- [ ] **Path traversal prevention** - No access outside allowed directories
- [ ] **Command injection prevention** - No unsanitized input to shell
- [ ] **Regular expression DoS prevention** - No catastrophic backtracking
- [ ] **Integer overflow prevention** - Check for overflow in calculations
- [ ] **Null byte injection prevention** - No null bytes in strings
- [ ] **Encoding issues handled** - Proper character encoding

### Authentication & Authorization (15 items)

- [ ] **Strong authentication** - Proper authentication mechanism
- [ ] **Password hashing** - bcrypt/scrypt/Argon2, not MD5/SHA1
- [ ] **Passwords not in code** - Credentials from environment/secrets
- [ ] **Session management secure** - Secure session tokens
- [ ] **Token validation** - JWT/API tokens properly validated
- [ ] **Authorization checks** - Verify permissions for every action
- [ ] **Principle of least privilege** - Minimal permissions granted
- [ ] **No hardcoded credentials** - No passwords in code
- [ ] **Multi-factor authentication** - MFA for sensitive operations
- [ ] **Account lockout** - Limit login attempts
- [ ] **Session timeout** - Sessions expire appropriately
- [ ] **Logout functionality** - Proper session cleanup on logout
- [ ] **CSRF protection** - CSRF tokens for state-changing operations
- [ ] **API key rotation** - API keys can be rotated
- [ ] **OAuth/OIDC properly implemented** - If using OAuth

### Data Protection (15 items)

- [ ] **No secrets in code** - API keys, passwords in environment
- [ ] **No secrets in logs** - Sensitive data not logged
- [ ] **Sensitive data encrypted** - Encryption at rest and in transit
- [ ] **HTTPS enforced** - No HTTP for sensitive data
- [ ] **SQL parameterized** - No string concatenation for queries
- [ ] **Prepared statements used** - For database queries
- [ ] **ORM used correctly** - ORM prevents injection
- [ ] **Output encoding** - HTML output encoded
- [ ] **No sensitive data in URLs** - Tokens/passwords not in query params
- [ ] **Secure cookie flags** - HttpOnly, Secure, SameSite
- [ ] **No PII in logs** - Personal information not logged
- [ ] **Data retention policy** - Sensitive data deleted when no longer needed
- [ ] **Encryption keys managed** - Keys stored securely
- [ ] **TLS certificates valid** - Certificates not expired or self-signed
- [ ] **Database encryption** - Sensitive fields encrypted

### OWASP Top 10 (20 items)

#### A01: Broken Access Control
- [ ] **Authorization for every action** - Every operation checks permissions
- [ ] **No horizontal privilege escalation** - Users can't access others' data
- [ ] **No vertical privilege escalation** - Users can't elevate privileges
- [ ] **CORS properly configured** - CORS headers restrictive

#### A02: Cryptographic Failures
- [ ] **Strong encryption** - Use modern algorithms (AES-256, RSA-2048+)
- [ ] **No weak hashing** - No MD5/SHA1 for security
- [ ] **Keys properly generated** - Cryptographically secure random
- [ ] **Encryption at rest** - Sensitive data encrypted in storage

#### A03: Injection
- [ ] **No SQL injection** - Parameterized queries only
- [ ] **No command injection** - No user input to shell commands
- [ ] **No code injection** - No eval() with user input
- [ ] **No LDAP injection** - LDAP queries properly escaped

#### A04: Insecure Design
- [ ] **Threat modeling done** - Security considered in design
- [ ] **Security requirements defined** - Security goals explicit
- [ ] **Secure by default** - Default configuration is secure

#### A05: Security Misconfiguration
- [ ] **No default credentials** - Default passwords changed
- [ ] **Error messages not verbose** - Don't leak implementation details
- [ ] **Unnecessary features disabled** - Minimal attack surface
- [ ] **Security headers set** - CSP, X-Frame-Options, etc.

#### A06: Vulnerable Components
- [ ] **Dependencies up to date** - Regular dependency updates
- [ ] **No known vulnerabilities** - Dependencies scanned for CVEs

#### A07: Authentication Failures
- [ ] **Covered in Authentication section above**

#### A08: Data Integrity Failures
- [ ] **Digital signatures used** - For critical data
- [ ] **Integrity checks** - Verify data hasn't been tampered with

---

## 5. STYLE

### PEP 8 Compliance (Python) (15 items)

- [ ] **Line length ≤ 88 characters** - Black formatter default
- [ ] **Indentation: 4 spaces** - No tabs
- [ ] **Blank lines appropriate** - 2 before top-level, 1 before methods
- [ ] **Whitespace around operators** - `x = 1` not `x=1`
- [ ] **No trailing whitespace** - Lines don't end with spaces
- [ ] **Imports on separate lines** - One import per line
- [ ] **Imports grouped** - stdlib, third-party, local
- [ ] **Imports alphabetically sorted** - Within each group
- [ ] **No wildcard imports** - Avoid `from module import *`
- [ ] **Absolute imports preferred** - Over relative imports
- [ ] **Line continuation correct** - Proper alignment for multi-line
- [ ] **String quotes consistent** - Double quotes or single quotes
- [ ] **Docstring quotes** - Triple double-quotes for docstrings
- [ ] **Naming follows PEP 8** - See naming section above
- [ ] **No space before colon** - `def func():` not `def func() :`

### Import Organization (8 items)

- [ ] **Imports grouped correctly** - Three groups: stdlib, third-party, local
- [ ] **Blank line between groups** - Separate groups with blank line
- [ ] **Alphabetically sorted** - Within each group
- [ ] **No unused imports** - Remove imports not used
- [ ] **Absolute imports preferred** - `from package.module import X`
- [ ] **No circular imports** - Resolve circular dependencies
- [ ] **Import modules, not names** - `import os` not `from os import path`
- [ ] **Type hints imported separately** - In `if TYPE_CHECKING:` block

### Code Formatting (12 items)

- [ ] **Black-formatted** - Code passes Black formatter
- [ ] **Consistent style** - Same patterns throughout
- [ ] **Readable layout** - Code easy to read
- [ ] **Appropriate comments** - Comments explain "why", not "what"
- [ ] **No commented-out code** - Remove old code
- [ ] **Function spacing** - Blank line between functions
- [ ] **Class spacing** - Two blank lines before classes
- [ ] **Method spacing** - One blank line between methods
- [ ] **Expression spacing** - Space after commas: `[1, 2, 3]`
- [ ] **No unnecessary parentheses** - `return x` not `return (x)`
- [ ] **Multiline formatting** - Consistent multiline style
- [ ] **String formatting consistent** - f-strings, format(), or % (choose one)

### Documentation (10 items)

- [ ] **README exists** - Project has README
- [ ] **API documented** - Public API has documentation
- [ ] **User guide exists** - For user-facing features
- [ ] **Architecture documented** - High-level design explained
- [ ] **Examples provided** - Common usage examples
- [ ] **Changelog maintained** - CHANGELOG.md updated
- [ ] **Dependencies documented** - README lists requirements
- [ ] **Setup instructions clear** - README has setup steps
- [ ] **No outdated docs** - Documentation matches code
- [ ] **Links working** - No broken documentation links

---

## 6. PROJECT-SPECIFIC

### Project Standards (10 items)

- [ ] **500-line file limit** - As per project standards
- [ ] **Type hints required** - All functions have type annotations
- [ ] **Google-style docstrings** - As per project standards
- [ ] **Single responsibility** - Classes and functions focused
- [ ] **Dependency injection** - Dependencies passed as parameters
- [ ] **80%+ test coverage** - Meets project requirement
- [ ] **Clean architecture** - Layers properly separated
- [ ] **No globals** - Global state avoided
- [ ] **Immutability preferred** - Objects immutable when possible
- [ ] **Interface-first design** - Interfaces defined before implementation

---

## TOTAL CHECKLIST ITEMS: 316

**Categories:**
- Code Quality: 104 items
- Testing: 33 items
- Performance: 30 items
- Security: 65 items
- Style: 45 items
- Project-Specific: 10 items

**Priority Levels:**
- ⭐⭐⭐⭐⭐ Critical (Security, Core Quality): ~150 items
- ⭐⭐⭐⭐ Important (Testing, Error Handling): ~100 items
- ⭐⭐⭐ Moderate (Performance, Style): ~66 items

---

## How to Use This Checklist

1. **Select Relevant Items:** Not all items apply to every file
2. **Prioritize:** Focus on critical security and quality items first
3. **Context Matters:** Consider project stage and requirements
4. **Be Pragmatic:** Balance perfection with delivery
5. **Learn and Improve:** Use checklist to improve code quality over time
