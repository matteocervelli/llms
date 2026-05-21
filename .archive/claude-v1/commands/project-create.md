---
description: Initialize new project with complete setup and documentation
allowed-tools: gh, git, filesystem
---

# Project Kickoff: $ARGUMENTS

**💡 Tip:** For safer planning, activate Plan Mode (press Shift+Tab twice) before running this command to review the project structure before creation.

## Repository Setup

```bash
# Create project structure
!mkdir -p $ARGUMENTS/{docs/{architecture,guides,implementation,PRD},src,tests,.github/workflows}
!cd $ARGUMENTS

# Initialize Git and GitHub
!git init
!gh repo create $ARGUMENTS --private --description="[Project description]"
!git remote add origin https://github.com/$(gh api user --jq .login)/$ARGUMENTS.git
```

## Core Documentation

Create essential planning documents:

### 1. Planning (`docs/PLANNING.md`)

- **Goals & Objectives**: Primary/secondary goals with success metrics
- **Use Cases**: 4+ core use cases with inputs/outputs
- **Technical Assumptions**: Infrastructure, data volume, integrations
- **Security Requirements**: Authentication, data protection, compliance needs

### 2. Roadmap (`docs/ROADMAP.md`)

- **Phases**: MVP → Enhancement → Advanced → Scale
- **Timeline**: Milestone dates and deliverables
- **Security & Privacy**: GDPR, data protection strategy
- **Success Criteria**: Measurable acceptance criteria

### 3. Architecture (`docs/architecture/ARCHITECTURE.md`)

- **Pattern**: MVC/Microservices/JAMstack decision
- **Components**: System diagram and data flow
- **Security Architecture**: Auth flow, data protection
- **Performance Strategy**: Caching, scaling, optimization

### 4. Tech Stack (`docs/architecture/TECH-STACK.md`)

- **Backend/Frontend/Database**: Technology choices with rationale
- **DevOps Tools**: CI/CD, monitoring, deployment
- **Security Tools**: SAST/DAST, dependency scanning
- **Development Workflow**: Commands and setup instructions

## Environment Configuration

```bash
# Create environment files
!touch .env.example .env .gitignore
!echo "# Environment variables\n.env\n.env.local\n\n# Dependencies\nnode_modules/\n__pycache__/\n\n# Build outputs\ndist/\nbuild/\n*.log" > .gitignore
```

## Quality & Security Setup

Initialize based on tech stack:

**Node.js/TypeScript:**

```bash
!npm init -y
# Add scripts: lint, test, typecheck, build, dev
# Setup: ESLint, Prettier, TypeScript, Jest
```

**Python:**

```bash
!touch requirements.txt pyproject.toml
# Setup: Black, isort, flake8, mypy, pytest
```

Configure pre-commit hooks and security scanning tools.

## CI/CD Pipeline

Create `.github/workflows/ci.yml`:

- **Quality Gates**: Linting, type checking, testing
- **Security Scans**: Dependency vulnerabilities, SAST
- **Build Verification**: Successful compilation/build
- **Deployment**: Staging/production pipeline

## Documentation Templates

Setup documentation structure:

- **ADR Template**: `docs/architecture/ADR/adr-template.md`
- **Sequence Diagrams**: `docs/architecture/sequence-diagrams/`
- **Implementation Logs**: `docs/implementation/`
- **User Guides**: `docs/guides/`

## Initial Commit

```bash
!git add .
!git commit -m "feat: initial project setup

Project: $ARGUMENTS
- Complete documentation structure (PLANNING, ROADMAP, ARCHITECTURE)
- Development environment configuration
- CI/CD pipeline with security scanning
- Quality tools setup (linting, testing, type checking)
- Security-by-design foundation

Setup includes:
- Tech stack documented and configured
- Security tools and workflows
- Performance monitoring preparation
- Documentation templates"

!git push -u origin main
```

## Branch Protection & Team Setup

```bash
# Configure branch protection
!gh api repos/:owner/:repo/branches/main/protection --method PUT --field required_status_checks='{"strict":true,"contexts":["ci"]}'

# Setup project board if complex project
!gh project create --title "$ARGUMENTS Development" --body "Project tracking for $ARGUMENTS"
```

## Next Steps Checklist

After kickoff completion:

- [ ] Configure environment variables in .env
- [ ] Setup monitoring/observability tools (Grafana, Sentry)
- [ ] Create first GitHub Issue for initial feature
- [ ] Run `npm run dev` or equivalent to verify setup
- [ ] Document team access and onboarding procedures