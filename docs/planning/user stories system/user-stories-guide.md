# User Stories Guide

## Core Function

User stories capture **what a user wants to accomplish and why** — not how the system will do it. They're communication tools that align your team around user value before you design technical solutions.

## Essential Components

A complete user story contains:

1. **Who** - The user type/persona
2. **What** - The capability they need
3. **Why** - The value/outcome they're seeking
4. **Acceptance criteria** - How you'll know it's done right

## The Standard Template

```
As a [user type],
I want to [action/capability],
So that [benefit/value].
```

**Acceptance Criteria:**
- Given [context/precondition]
- When [action]
- Then [expected outcome]

## What Makes a Good Story

Use the **INVEST** framework:

- **I**ndependent - Can be built separately
- **N**egotiable - Details can be discussed
- **V**aluable - Delivers clear user benefit
- **E**stimable - Team can size the effort
- **S**mall - Completable in one sprint
- **T**estable - Clear pass/fail criteria

## Examples for Your Context

**Bad (technical focus):**
"Implement OAuth2 authentication system"

**Good (user-centric):**
```
As a CEO consulting client,
I want to log in securely with my existing Google account,
So that I can access my diagnostic dashboard without managing another password.

Acceptance Criteria:
- Given I'm on the login page
- When I click "Continue with Google"
- Then I'm authenticated and redirected to my dashboard
- And my session persists for 30 days
```

**Another example:**
```
As a business owner using ScalabilityScore,
I want to see my constraint analysis in a visual priority matrix,
So that I can quickly identify which bottlenecks to address first.

Acceptance Criteria:
- Given I've completed the assessment
- When I view results
- Then constraints are plotted by impact vs. effort
- And I can filter by category (people/process/systems)
- And each item is clickable for detailed recommendations
```

## Key Guardrails

- **No solution prescription** - "I want a dropdown" ❌ vs "I want to filter results" ✓
- **Real user language** - Not internal jargon
- **One clear job-to-be-done** - If you need "and" twice, split it
- **Measurable value** - The "so that" must be verifiable

This keeps you focused on **user outcomes** while leaving technical implementation flexible.
