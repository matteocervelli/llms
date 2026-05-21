---
name: {{ name }}
description: {{ description }}
{%- if sub_skills %}
sub-skills:
{%- for skill in sub_skills %}
  - {{ skill }}
{%- endfor %}
{%- endif %}
{%- if allowed_tools %}
allowed-tools:
{%- for tool in allowed_tools %}
  - {{ tool }}
{%- endfor %}
{%- endif %}
{%- if frontmatter %}
{%- for key, value in frontmatter.items() %}
{{ key }}: {{ value }}
{%- endfor %}
{%- endif %}
---

# {{ name }}

{{ description }}

## Role: Orchestrator Skill

This is an **orchestrator skill** that coordinates multiple sub-skills to accomplish complex tasks. It breaks down high-level goals into manageable steps and delegates to specialized skills.

## Sub-Skills

{%- if sub_skills %}

This orchestrator delegates to the following sub-skills:

{%- for skill in sub_skills %}
- **{{ skill }}**: Specialized skill for specific task
{%- endfor %}
{%- else %}

No sub-skills configured. Add sub-skills in the frontmatter:

```yaml
sub-skills:
  - skill-name-1
  - skill-name-2
```
{%- endif %}

## Instructions

{{ content }}

## Workflow

{%- if workflow %}

{{ workflow }}
{%- else %}

### Standard Orchestration Pattern

1. **Analyze**: Break down the complex task into subtasks
2. **Plan**: Determine which sub-skills to use and in what order
3. **Coordinate**: Invoke sub-skills with appropriate context
4. **Integrate**: Combine results from multiple sub-skills
5. **Validate**: Ensure final output meets requirements
6. **Report**: Provide comprehensive summary of work done
{%- endif %}

## Orchestration Principles

### 1. Task Decomposition

Break complex tasks into:
- **Independent subtasks**: Can run in parallel
- **Dependent subtasks**: Must run sequentially
- **Optional subtasks**: Run conditionally based on results

### 2. Context Management

- **Context Passing**: Pass relevant context to each sub-skill
- **State Tracking**: Maintain state across sub-skill invocations
- **Result Aggregation**: Collect and synthesize results

### 3. Error Handling

- **Graceful Degradation**: Handle sub-skill failures gracefully
- **Fallback Strategies**: Provide alternatives when sub-skills fail
- **Error Propagation**: Report errors with context

### 4. Progress Tracking

- Track completion status of each subtask
- Provide progress updates for long-running operations
- Maintain audit trail of delegations

## Decision Framework

Use this decision tree to delegate tasks:

```
Task Analysis
├─ Simple & Direct → Use specialized sub-skill
├─ Multi-step Process → Use workflow pattern
├─ Parallel Work Possible → Coordinate multiple sub-skills
└─ Unknown Complexity → Start with analysis sub-skill
```

## Examples

### Example 1: Feature Implementation

```
Task: Implement new feature

Orchestration:
1. Invoke `requirement-analyzer` → Extract requirements
2. Invoke `architecture-designer` → Design solution
3. Invoke `code-implementer` → Write code
4. Invoke `test-generator` → Create tests
5. Invoke `code-reviewer` → Review quality
6. Integrate all outputs → Complete feature
```

### Example 2: Bug Fix

```
Task: Fix production bug

Orchestration:
1. Invoke `issue-analyzer` → Understand bug
2. Invoke `code-searcher` → Find relevant code
3. Invoke `root-cause-analyzer` → Identify cause
4. Invoke `fix-implementer` → Implement fix
5. Invoke `test-generator` → Add regression tests
6. Validate fix → Ensure bug resolved
```

### Example 3: Code Refactoring

```
Task: Refactor legacy module

Orchestration:
1. Invoke `code-analyzer` → Understand current code
2. Invoke `dependency-mapper` → Map dependencies
3. Invoke `refactoring-planner` → Plan changes
4. Invoke `code-implementer` → Execute refactoring
5. Invoke `test-validator` → Ensure tests pass
6. Review changes → Confirm improvements
```

## Best Practices

### Do's
- ✅ Break tasks into logical subtasks
- ✅ Pass clear context to each sub-skill
- ✅ Validate sub-skill outputs before proceeding
- ✅ Maintain consistent state across delegations
- ✅ Provide comprehensive final reports
- ✅ Handle errors gracefully with fallbacks

### Don'ts
- ❌ Create circular dependencies between sub-skills
- ❌ Pass excessive context (keep it relevant)
- ❌ Ignore sub-skill errors
- ❌ Over-complicate simple tasks
- ❌ Lose track of overall goal during delegation

## Sub-Skill Communication

### Invoking Sub-Skills

When delegating to a sub-skill:

1. **Prepare Context**: Extract relevant information
2. **Set Expectations**: Define what you need from the sub-skill
3. **Invoke**: Trigger the sub-skill
4. **Validate Output**: Ensure results meet requirements
5. **Integrate**: Incorporate into overall workflow

### Example Invocation Pattern

```
# Invoke requirement-analyzer
Context: Feature request from user
Expected Output: Structured requirements list
Validation: Must include acceptance criteria

# Invoke architecture-designer
Context: Requirements from previous step
Expected Output: System architecture design
Validation: Must include data flow diagrams
```

## Performance Optimization

- **Parallel Execution**: Run independent sub-skills concurrently
- **Caching**: Reuse results from repeated sub-skill calls
- **Early Exit**: Stop orchestration if critical step fails
- **Progressive Disclosure**: Only invoke sub-skills when needed

## Monitoring & Debugging

### Execution Trace

Track orchestration flow:
```
[Orchestrator: {{ name }}]
  ├─ [Sub-skill: skill-1] Status: Success
  ├─ [Sub-skill: skill-2] Status: Success
  ├─ [Sub-skill: skill-3] Status: Failed → Fallback
  └─ [Integration] Status: Complete
```

### Metrics to Track

- Sub-skill invocation count
- Success/failure rates
- Total execution time
- Context size passed
- Result quality score

## Troubleshooting

**Sub-skill not available**
- Verify sub-skill exists in catalog
- Check sub-skill activation conditions
- Ensure sub-skill is in correct scope

**Context overflow**
- Reduce context size passed to sub-skills
- Summarize information before passing
- Split into multiple smaller invocations

**Inconsistent results**
- Validate sub-skill outputs rigorously
- Add intermediate validation steps
- Review sub-skill configurations

**Orchestration too complex**
- Simplify workflow by combining steps
- Create intermediate orchestrator for subsections
- Review if task should be simpler

## Advanced Patterns

### Sequential Pipeline
```
Input → Skill-1 → Skill-2 → Skill-3 → Output
```

### Parallel Fan-Out
```
        ┌─ Skill-1 ─┐
Input ──┼─ Skill-2 ──┼→ Aggregator → Output
        └─ Skill-3 ─┘
```

### Conditional Branching
```
Input → Analysis
         ├─ If Condition-A → Skill-1 → Output
         ├─ If Condition-B → Skill-2 → Output
         └─ Else → Skill-3 → Output
```

### Iterative Refinement
```
Input → Initial-Skill → Validator
                ↓         ↑
                └─ Refiner (loop until valid)
```

## Related Skills

List related orchestrator and sub-skills:

- Parent orchestrator (if this is a sub-orchestrator)
- Sibling orchestrators with similar capabilities
- All sub-skills referenced in this orchestrator

---

*Generated with skill_builder tool*
