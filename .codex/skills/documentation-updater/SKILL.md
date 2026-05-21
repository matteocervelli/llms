---
name: documentation-updater
description:
  Update all project documentation including implementation docs, user
  guides, API docs, and architecture diagrams. Use when finalizing features to ensure
  comprehensive documentation.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Documentation Updater Skill

## Purpose

Systematic guidance for updating all types of project documentation when finalizing feature implementations.

## When to Use

- After feature implementation and validation are complete
- Need to document implementation details
- Creating or updating user guides
- Updating API documentation
- Adding architecture diagrams
- Documenting configuration changes

## Templates

All templates are located in `templates/`:

| Template                 | Location               | Purpose                         |
| ------------------------ | ---------------------- | ------------------------------- |
| `implementation-docs.md` | `docs/implementation/` | How the feature was implemented |
| `user-guide.md`          | `docs/guides/`         | End-user documentation          |
| `api-docs.md`            | `docs/api/`            | REST API and Python docstrings  |
| `architecture-docs.md`   | `docs/architecture/`   | Design decisions and diagrams   |
| `configuration-docs.md`  | Various                | Config, env vars, TECH-STACK    |

## Documentation Update Workflow

### 1. Implementation Documentation

**When**: Always required for every feature

**Actions**:

1. Create doc using `templates/implementation-docs.md`
2. Document solution approach and architecture
3. Include security measures and performance optimizations
4. List dependencies and configuration requirements

### 2. User-Facing Documentation

**When**: Feature changes user interaction

**README Updates** - Check if updates needed for:

- Installation steps
- New CLI commands
- Configuration changes
- New user-facing features

**User Guides** - Create for complex features using `templates/user-guide.md`

### 3. API Documentation

**When**: REST APIs or public Python APIs added/changed

**REST APIs** - Use `templates/api-docs.md` for:

- Endpoint documentation with examples
- Request/response formats
- Error codes and rate limiting

**Python APIs** - Update docstrings with:

- Args, Returns, Raises
- Examples
- See Also references

### 4. Architecture Documentation

**When**: Complex features with multiple components or significant design decisions

**Use** `templates/architecture-docs.md` for:

- System diagrams
- Component responsibilities
- Design decision records
- Data flow documentation

### 5. Configuration Documentation

**Update these files**:

- `.env.example` - Add new environment variables
- `docs/guides/configuration.md` - Document config options
- `TECH-STACK.md` - Document new dependencies

Use `templates/configuration-docs.md` for formats.

## Documentation Checklist

### Implementation Documentation

- [ ] Implementation doc created in `docs/implementation/`
- [ ] Solution approach documented
- [ ] Architecture and components described
- [ ] Security measures documented
- [ ] Testing coverage detailed
- [ ] Dependencies documented

### User Documentation

- [ ] README.md updated (if applicable)
- [ ] User guide created (for complex features)
- [ ] Usage examples provided
- [ ] Troubleshooting section added

### API Documentation

- [ ] API endpoints documented
- [ ] Request/response formats shown
- [ ] Error codes documented
- [ ] Python API docstrings complete

### Architecture Documentation

- [ ] Architecture doc created (if complex feature)
- [ ] System diagrams included
- [ ] Design decisions documented

### Configuration Documentation

- [ ] .env.example updated
- [ ] Configuration guide updated
- [ ] TECH-STACK.md updated (if dependencies added)

### Quality Checks

- [ ] All links tested and working
- [ ] Code examples tested
- [ ] Markdown properly formatted
- [ ] Version numbers consistent

## Best Practices

### Writing Style

- Clear, concise language
- Present tense, active voice
- Define technical terms on first use

### Code Examples

- Test all code examples
- Include imports and setup
- Show expected output

### Organization

- Logical structure with consistent headings
- Cross-reference related docs
- Table of contents for long docs

## Common Documentation Patterns

### Feature Introduction

```markdown
## <Feature Name>

<One-line description>

### Overview

<What it does and why>

### Quick Start

<Minimal example>

### Learn More

- [User Guide](link)
- [API Documentation](link)
```

### Troubleshooting Pattern

```markdown
### Common Issues

#### Issue: <Error message>

**Symptoms**: What the user sees
**Cause**: Why this happens
**Solution**: Steps to fix
**Prevention**: How to avoid
```

## Integration with Deployment Flow

**Input**: Completed, validated feature implementation
**Process**: Systematic documentation of all aspects
**Output**: Comprehensive documentation across all types
**Next Step**: Changelog generation

---

**Version**: 1.0.0
