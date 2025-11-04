---
description: Implement new feature from GitHub issue with full development workflow
argument-hint: <issue-number> [create-branch:true|false]
allowed-tools: gh, git
---

# Implement Feature from GitHub Issue

Implement feature from GitHub issue #$1 following the prompt @./.claude/prompts/feature-implementer-main.md prompt.

The main orchestrator guides six phases: Requirements Analysis → Design & Planning → User Approval → Implementation → Validation → Deployment.

Branch creation: ${2:-true}