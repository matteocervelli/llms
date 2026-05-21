---
name: project-create
description: Initialize a new project with full setup — repo structure, docs, quality tools, and CI/CD. Use when starting a brand-new project from scratch. Trigger on "create a new project", "initialize a project", "set up a new repo", "bootstrap a project".
---

# Project Create Skill

## Purpose

Initialize new projects with complete setup, documentation structure, quality tools, and CI/CD pipeline.

## Usage

```bash
/project-create <project-name>
```

## Repository Setup

```bash
# Create project structure
mkdir -p <project-name>/{docs/{architecture,guides,implementation,PRD},src,tests,.github/workflows}
cd <project-name>

# Initialize Git and GitHub
git init
gh repo create <project-name> --private --description="[Project description]"
git remote add origin https://github.com/$(gh api user --jq .login)/<project-name>.git
```

## Core Documentation

### 1. Planning (`docs/PLANNING.md`)

- **Goals & Objectives**: Primary/secondary goals with success metrics
- **Use Cases**: 4+ core use cases with inputs/outputs
- **Technical Assumptions**: Infrastructure, data volume, integrations
- **Security Requirements**: Authentication, data protection, compliance needs

### 2. Roadmap (`docs/ROADMAP.md`)

- **Phases**: MVP -> Enhancement -> Advanced -> Scale
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
touch .env.example .env .gitignore
echo "# Environment variables
.env
.env.local

# Dependencies
node_modules/
__pycache__/

# Build outputs
dist/
build/
*.log" > .gitignore
```

## Quality & Security Setup

### Node.js/TypeScript

```bash
npm init -y
# Add scripts: lint, test, typecheck, build, dev
# Setup: ESLint, Prettier, TypeScript, Jest
```

### Python

```bash
touch requirements.txt pyproject.toml
# Setup: ruff, mypy, pytest
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
git add .
git commit -m "feat: initial project setup

Project: <project-name>
- Complete documentation structure (PLANNING, ROADMAP, ARCHITECTURE)
- Development environment configuration
- CI/CD pipeline with security scanning
- Quality tools setup (linting, testing, type checking)
- Security-by-design foundation"

git push -u origin main
```

## Branch Protection & Team Setup

```bash
# Configure branch protection
gh api repos/:owner/:repo/branches/main/protection --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci"]}'

# Setup project board if complex project
gh project create --title "<project-name> Development" --body "Project tracking"
```

## Next Steps Checklist

After kickoff completion:

- [ ] Configure environment variables in .env
- [ ] Setup monitoring/observability tools (Grafana, Sentry)
- [ ] Create first GitHub Issue for initial feature
- [ ] Run `npm run dev` or equivalent to verify setup
- [ ] Document team access and onboarding procedures

## Tips

- Activate Plan Mode (Shift+Tab twice) before running for safer planning
- Use consistent naming conventions from the start
- Set up quality tools before writing code
- Document decisions early with ADRs
- Configure CI/CD before first PR

## Related Skills

- `/implementation` - Implement features after setup
- `/infrastructure-setup` - Production infrastructure
- `/gh-milestone-create` - Create milestones for planning
