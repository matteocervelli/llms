# Documentation Sources

## Overview

This resource provides a curated list of official documentation sources for popular libraries and frameworks. Use these authoritative sources when fetching documentation via context7-mcp or fetch-mcp.

---

## Python Libraries

### Web Frameworks

**FastAPI**
- Official Docs: https://fastapi.tiangolo.com/
- GitHub: https://github.com/tiangolo/fastapi
- Context7 ID: `/tiangolo/fastapi`
- API Reference: https://fastapi.tiangolo.com/reference/
- Tutorial: https://fastapi.tiangolo.com/tutorial/
- Changelog: https://github.com/tiangolo/fastapi/blob/master/CHANGELOG.md

**Django**
- Official Docs: https://docs.djangoproject.com/
- GitHub: https://github.com/django/django
- Context7 ID: `/django/django`
- API Reference: https://docs.djangoproject.com/en/stable/ref/
- Tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/
- Release Notes: https://docs.djangoproject.com/en/stable/releases/

**Flask**
- Official Docs: https://flask.palletsprojects.com/
- GitHub: https://github.com/pallets/flask
- Context7 ID: `/pallets/flask`
- API Reference: https://flask.palletsprojects.com/en/stable/api/
- Quick Start: https://flask.palletsprojects.com/en/stable/quickstart/
- Changelog: https://flask.palletsprojects.com/en/stable/changes/

### Data Validation

**Pydantic**
- Official Docs: https://docs.pydantic.dev/
- GitHub: https://github.com/pydantic/pydantic
- Context7 ID: `/pydantic/pydantic`
- API Reference: https://docs.pydantic.dev/latest/api/
- Migration Guide (v1 to v2): https://docs.pydantic.dev/latest/migration/
- Examples: https://docs.pydantic.dev/latest/examples/

### Testing

**Pytest**
- Official Docs: https://docs.pytest.org/
- GitHub: https://github.com/pytest-dev/pytest
- Context7 ID: `/pytest-dev/pytest`
- API Reference: https://docs.pytest.org/en/stable/reference/reference.html
- How-to Guides: https://docs.pytest.org/en/stable/how-to/index.html
- Changelog: https://docs.pytest.org/en/stable/changelog.html

**Pytest-Asyncio**
- Official Docs: https://pytest-asyncio.readthedocs.io/
- GitHub: https://github.com/pytest-dev/pytest-asyncio
- Usage Guide: https://pytest-asyncio.readthedocs.io/en/latest/how-to.html

### Async Libraries

**HTTPX**
- Official Docs: https://www.python-httpx.org/
- GitHub: https://github.com/encode/httpx
- Context7 ID: `/encode/httpx`
- Quick Start: https://www.python-httpx.org/quickstart/
- API Reference: https://www.python-httpx.org/api/

**Asyncio**
- Official Docs: https://docs.python.org/3/library/asyncio.html
- Tutorial: https://docs.python.org/3/library/asyncio-task.html
- API Reference: https://docs.python.org/3/library/asyncio-api-index.html

### Database Libraries

**SQLAlchemy**
- Official Docs: https://docs.sqlalchemy.org/
- GitHub: https://github.com/sqlalchemy/sqlalchemy
- Context7 ID: `/sqlalchemy/sqlalchemy`
- ORM Tutorial: https://docs.sqlalchemy.org/en/stable/orm/tutorial.html
- API Reference: https://docs.sqlalchemy.org/en/stable/core/api_basics.html

**Alembic**
- Official Docs: https://alembic.sqlalchemy.org/
- GitHub: https://github.com/sqlalchemy/alembic
- Tutorial: https://alembic.sqlalchemy.org/en/latest/tutorial.html

---

## TypeScript/JavaScript Libraries

### React

**React**
- Official Docs: https://react.dev/
- GitHub: https://github.com/facebook/react
- Context7 ID: `/facebook/react`
- Quick Start: https://react.dev/learn
- API Reference: https://react.dev/reference/react
- Hooks: https://react.dev/reference/react/hooks

**Next.js**
- Official Docs: https://nextjs.org/docs
- GitHub: https://github.com/vercel/next.js
- Context7 ID: `/vercel/next.js`
- Getting Started: https://nextjs.org/docs/getting-started
- API Reference: https://nextjs.org/docs/api-reference

### Testing

**Jest**
- Official Docs: https://jestjs.io/
- GitHub: https://github.com/jestjs/jest
- Context7 ID: `/jestjs/jest`
- Getting Started: https://jestjs.io/docs/getting-started
- API Reference: https://jestjs.io/docs/api

**Playwright**
- Official Docs: https://playwright.dev/
- GitHub: https://github.com/microsoft/playwright
- Context7 ID: `/microsoft/playwright`
- Quick Start: https://playwright.dev/docs/intro
- API Reference: https://playwright.dev/docs/api/class-playwright

---

## Rust Libraries

**Tokio**
- Official Docs: https://tokio.rs/
- GitHub: https://github.com/tokio-rs/tokio
- Context7 ID: `/tokio-rs/tokio`
- Tutorial: https://tokio.rs/tokio/tutorial
- API Reference: https://docs.rs/tokio/

**Axum**
- Official Docs: https://docs.rs/axum/
- GitHub: https://github.com/tokio-rs/axum
- Examples: https://github.com/tokio-rs/axum/tree/main/examples

**Serde**
- Official Docs: https://serde.rs/
- GitHub: https://github.com/serde-rs/serde
- Context7 ID: `/serde-rs/serde`
- Data Formats: https://serde.rs/#data-formats

---

## Source Selection Guidelines

### When to Use Context7-MCP

Use context7 for:
- Comprehensive API references
- Deep documentation retrieval
- Semantic search across documentation
- Version-specific documentation
- Library-specific patterns and conventions

**Advantages:**
- Semantic search capabilities
- Structured documentation retrieval
- Version awareness
- High-quality extraction

**Limitations:**
- May not cover all libraries
- Token limits apply
- Requires library ID resolution

### When to Use Fetch-MCP

Use fetch for:
- Official quick start guides
- GitHub READMEs and examples
- Migration guides and changelogs
- Community tutorials (verified sources)
- Documentation pages not in context7

**Advantages:**
- Access any publicly available URL
- Flexible prompt-based extraction
- Latest content from official sources
- No library ID required

**Limitations:**
- Less structured than context7
- Depends on prompt quality
- May include irrelevant content
- No semantic search

### Hybrid Approach (Recommended)

For comprehensive documentation:
1. **Context7:** Primary documentation and API reference
2. **Fetch (Official Docs):** Quick start and getting started guides
3. **Fetch (GitHub):** Latest examples and README
4. **Fetch (Changelog):** Version migration information

---

## Source Verification

### Official Documentation Checklist

✅ **Verify URL is official:**
- Check domain matches project website
- Verify SSL certificate
- Cross-reference with GitHub repository

✅ **Check documentation currency:**
- Look for version number
- Check last updated date
- Verify it matches required version

✅ **Validate content quality:**
- Official sources only
- No third-party tutorials (unless verified)
- Complete and comprehensive
- Code examples are runnable

---

## Common Documentation Patterns

### Official Documentation Structure

Most official documentation follows this pattern:
```
/docs/
├── index.html or README.md    # Overview and introduction
├── getting-started/            # Quick start guides
├── tutorial/                   # Step-by-step tutorials
├── guides/                     # How-to guides
├── api-reference/              # Comprehensive API docs
├── examples/                   # Code examples
└── changelog/ or CHANGELOG.md  # Version history
```

### GitHub Repository Structure

Most GitHub repositories follow this pattern:
```
/
├── README.md                   # Overview, features, quick start
├── CHANGELOG.md or CHANGES.md  # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── docs/                       # Additional documentation
├── examples/                   # Example code
└── src/ or lib/                # Source code
```

---

## Version-Specific Documentation

### Fetching Specific Versions

**Context7 (if supported):**
```python
# Version-specific library ID
library_id = "/tiangolo/fastapi/v0.100.0"
```

**Fetch-MCP (version in URL):**
```python
# Django version 4.2 docs
url = "https://docs.djangoproject.com/en/4.2/"

# React version 18.x docs
url = "https://react.dev/"  # Latest
url = "https://17.reactjs.org/"  # React 17
```

### Version Detection

When version is not specified:
1. Fetch current/latest version from main docs
2. Check changelog for breaking changes
3. Document version compatibility notes
4. Provide migration guidance if upgrading

---

## Documentation URL Templates

### Python Package Documentation

**PyPI Package:**
```
https://pypi.org/project/{package_name}/
```

**Read the Docs:**
```
https://{project_name}.readthedocs.io/en/latest/
https://{project_name}.readthedocs.io/en/stable/
https://{project_name}.readthedocs.io/en/v{version}/
```

### JavaScript/TypeScript Package Documentation

**npm Package:**
```
https://www.npmjs.com/package/{package_name}
```

**Official Docs:**
```
https://{project_name}.dev/docs
https://docs.{project_name}.com/
https://{project_name}.org/docs/
```

### Rust Crate Documentation

**docs.rs:**
```
https://docs.rs/{crate_name}/
https://docs.rs/{crate_name}/{version}/
```

**Crates.io:**
```
https://crates.io/crates/{crate_name}
```

---

## Error Handling

### Documentation Not Found

If documentation cannot be fetched:

1. **Try Alternative Sources:**
   - Official website → GitHub → Package registry

2. **Search Context7:**
   - Try alternate library names
   - Check for org/project format variations

3. **Manual Verification:**
   - Search engine for official docs
   - Check GitHub repository for docs link
   - Verify domain authenticity

4. **Report to User:**
   - Document attempted sources
   - Suggest manual documentation review
   - Continue with available sources

---

**Version:** 2.0.0
**Last Updated:** 2025-10-29
**Maintainer:** Documentation Researcher Agent
