---
description: Implement new feature from GitHub issue with full development workflow
argument-hint: <issue-number> [create-branch:true|false]
allowed-tools: [gh, git]
---

# Implement Feature from GitHub Issue

Implement feature from GitHub issue #$1 using the @feature-implementer agent.

The agent orchestrates five phases: Requirements Analysis → Architecture Design → Implementation → Validation → Deployment.

Branch creation: ${2:-true}
