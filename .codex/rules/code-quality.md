# Code Quality Rules

## File Organization

- 500 line max per file (split by responsibility)
- Single Responsibility: one clear purpose per file
- Dependency Injection: service params, not global imports
- Interface First: contracts before implementations

## Naming

- Self-documenting names > comments
- Verbs for functions, nouns for data
- Short, single-purpose functions

## Simplicity

- Simple things must be simple to accomplish
- Fight complexity at every decision point
- 3 similar lines > 1 premature helper
- Can't explain simply? Redesign

## Comments

- Purpose: WHY, not WHAT
- Design: 10-line design comment at top of non-trivial files
- Why-comments: freeze hidden reasoning
