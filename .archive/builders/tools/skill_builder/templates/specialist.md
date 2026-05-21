---
name: {{ name }}
description: {{ description }}
{%- if expertise_area %}
expertise-area: {{ expertise_area }}
{%- endif %}
{%- if technologies %}
technologies:
{%- for tech in technologies %}
  - {{ tech }}
{%- endfor %}
{%- endif %}
{%- if patterns %}
patterns:
{%- for pattern in patterns %}
  - {{ pattern }}
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

## Role: Specialist Skill

This is a **specialist skill** focused on deep expertise in a specific domain. It provides authoritative guidance, best practices, and advanced techniques within its area of specialization.

## Expertise Area

{%- if expertise_area %}

**Domain**: {{ expertise_area }}

This skill has deep knowledge and experience in {{ expertise_area }}, including:
- Industry best practices
- Common patterns and anti-patterns
- Performance optimization techniques
- Security considerations
- Testing strategies
- Debugging approaches
{%- else %}

Define the expertise area in frontmatter:

```yaml
expertise-area: "Your Domain Here"
```
{%- endif %}

## Technology Stack

{%- if technologies %}

This specialist is proficient in:

{%- for tech in technologies %}
- **{{ tech }}**: Core technology in the stack
{%- endfor %}

### Technology-Specific Knowledge

Each technology comes with specific considerations:

{%- for tech in technologies %}

#### {{ tech }}

- **Best Practices**: Industry-standard approaches
- **Common Pitfalls**: Known issues and how to avoid them
- **Performance**: Optimization techniques specific to {{ tech }}
- **Testing**: Testing strategies for {{ tech }}
{%- endfor %}
{%- else %}

Specify technologies in frontmatter:

```yaml
technologies:
  - Technology 1
  - Technology 2
```
{%- endif %}

## Design Patterns & Principles

{%- if patterns %}

This specialist applies these patterns and principles:

{%- for pattern in patterns %}
- **{{ pattern }}**: Application and implementation guidance
{%- endfor %}

### Pattern Application Guidelines

{%- for pattern in patterns %}

#### {{ pattern }}

**When to Use**:
- Describe scenarios where {{ pattern }} is appropriate
- Identify signals that indicate this pattern should be used

**Implementation**:
- Step-by-step approach to implementing {{ pattern }}
- Code structure and organization

**Trade-offs**:
- Benefits of using {{ pattern }}
- Costs and complexity considerations
- Alternatives if {{ pattern }} doesn't fit
{%- endfor %}
{%- else %}

Define patterns in frontmatter:

```yaml
patterns:
  - Pattern 1
  - Pattern 2
```
{%- endif %}

## Instructions

{{ content }}

## Specialist Guidelines

### Core Competencies

1. **Deep Technical Knowledge**
   - Understand internals and implementation details
   - Know edge cases and limitations
   - Stay current with latest developments

2. **Best Practice Application**
   - Apply industry-standard approaches
   - Adapt patterns to specific contexts
   - Balance ideal vs. practical solutions

3. **Code Quality Focus**
   - Write maintainable, readable code
   - Follow language/framework conventions
   - Optimize for long-term sustainability

4. **Problem-Solving Approach**
   - Analyze root causes, not symptoms
   - Consider multiple solution approaches
   - Evaluate trade-offs systematically

5. **Knowledge Sharing**
   - Explain decisions and reasoning
   - Document complex implementations
   - Mentor others through examples

## Quality Standards

### Code Quality Checklist

- [ ] Follows language/framework conventions
- [ ] Implements relevant design patterns correctly
- [ ] Includes comprehensive error handling
- [ ] Has appropriate test coverage (80%+)
- [ ] Documents complex logic and decisions
- [ ] Optimized for performance where needed
- [ ] Secure by design (input validation, etc.)
- [ ] Maintainable and readable

### Review Criteria

When reviewing code or designs:

1. **Correctness**: Does it solve the problem?
2. **Clarity**: Is it easy to understand?
3. **Efficiency**: Is it performant?
4. **Maintainability**: Can it be easily modified?
5. **Testability**: Can it be effectively tested?
6. **Security**: Does it handle untrusted input safely?

## Common Patterns

### Pattern 1: [Common Pattern in Domain]

**Problem**: Describe the problem this pattern solves

**Solution**: Explain the solution approach

**Example**:
```
# Provide code example or pseudocode
```

**When to Use**:
- Scenario A
- Scenario B

**When to Avoid**:
- Scenario C
- Scenario D

### Pattern 2: [Another Common Pattern]

**Problem**: Describe the problem

**Solution**: Explain the solution

**Example**:
```
# Provide example
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: [Common Mistake]

**Problem**: What makes this an anti-pattern

**Why It's Bad**:
- Negative consequence 1
- Negative consequence 2

**Better Approach**:
- Recommended alternative
- Why it's better

### Anti-Pattern 2: [Another Mistake]

**Problem**: Description

**Why It's Bad**: Consequences

**Better Approach**: Alternative solution

## Performance Optimization

### Profiling Strategy

1. **Measure First**: Use profiling tools to identify bottlenecks
2. **Prioritize**: Focus on high-impact optimizations
3. **Implement**: Make targeted improvements
4. **Verify**: Confirm performance gains

### Common Optimizations

- **Caching**: Reduce redundant computations
- **Lazy Loading**: Defer work until needed
- **Batch Processing**: Reduce overhead
- **Async Operations**: Improve concurrency
- **Data Structures**: Choose efficient structures
- **Algorithms**: Use optimal algorithms

## Security Considerations

### Security Checklist

- [ ] Input validation on all external data
- [ ] Output sanitization to prevent injection
- [ ] Authentication and authorization checks
- [ ] Secure handling of sensitive data
- [ ] Protection against common vulnerabilities
- [ ] Security testing included
- [ ] Dependency vulnerability scanning
- [ ] Least privilege principle applied

### Threat Model

Consider these security aspects:

1. **Input Attacks**: SQL injection, XSS, command injection
2. **Authentication**: Weak passwords, session hijacking
3. **Authorization**: Privilege escalation, IDOR
4. **Data Exposure**: Sensitive data in logs, error messages
5. **Dependencies**: Vulnerable third-party libraries

## Testing Strategy

### Test Pyramid

```
       ┌─────────┐
       │   E2E   │  Few, slow, expensive
       ├─────────┤
       │  Integ  │  Some, moderate cost
       ├─────────┤
       │  Unit   │  Many, fast, cheap
       └─────────┘
```

### Test Coverage Goals

- **Unit Tests**: 80%+ coverage of business logic
- **Integration Tests**: All major workflows covered
- **End-to-End Tests**: Critical user journeys verified
- **Performance Tests**: Key operations benchmarked
- **Security Tests**: Common vulnerabilities checked

### Testing Best Practices

- **Test Behavior, Not Implementation**: Focus on outcomes
- **Keep Tests Independent**: No test dependencies
- **Use Descriptive Names**: Clear test intentions
- **Follow AAA Pattern**: Arrange, Act, Assert
- **Mock External Dependencies**: Isolate unit under test

## Troubleshooting Guide

### Debugging Approach

1. **Reproduce**: Create minimal reproduction case
2. **Isolate**: Narrow down to specific component
3. **Hypothesize**: Form theory about root cause
4. **Test**: Verify hypothesis with experiments
5. **Fix**: Implement targeted solution
6. **Verify**: Confirm fix resolves issue
7. **Prevent**: Add tests to prevent regression

### Common Issues

**Issue 1**: [Common problem in this domain]
- **Symptoms**: How it manifests
- **Cause**: Root cause
- **Solution**: How to fix
- **Prevention**: How to avoid

**Issue 2**: [Another common problem]
- **Symptoms**: Signs of this issue
- **Cause**: Why it happens
- **Solution**: Resolution steps
- **Prevention**: Preventive measures

## Advanced Topics

### Topic 1: [Advanced Concept]

For experienced practitioners who need to go deeper:

- **Concept**: Explanation of advanced topic
- **Use Cases**: When this becomes relevant
- **Implementation**: How to implement
- **Trade-offs**: Costs and benefits

### Topic 2: [Another Advanced Concept]

Advanced technique for specific scenarios:

- **Background**: Context and prerequisites
- **Approach**: Detailed methodology
- **Considerations**: Important factors
- **References**: Further reading

## Best Practices Summary

### Do's ✅

- Follow established conventions
- Write self-documenting code
- Test thoroughly at all levels
- Handle errors gracefully
- Optimize based on profiling
- Document complex decisions
- Review code systematically
- Stay current with ecosystem

### Don'ts ❌

- Over-engineer simple solutions
- Ignore error cases
- Skip testing
- Optimize prematurely
- Use patterns inappropriately
- Leave code undocumented
- Ignore security implications
- Chase latest trends blindly

## Learning Resources

### Recommended Reading

- **Books**: Key books in the domain
- **Documentation**: Official docs and guides
- **Articles**: Important blog posts and papers
- **Courses**: Online courses for deeper learning

### Community Resources

- **Forums**: Where to ask questions
- **Communities**: Active communities in the space
- **Conferences**: Important industry events
- **Open Source**: Notable projects to study

## Related Skills

List related specialist skills:

- Adjacent domain specialists
- Complementary technology specialists
- Higher-level orchestrator skills that might delegate here

## Continuous Improvement

This specialist skill should evolve:

1. **Stay Current**: Follow latest developments
2. **Update Practices**: Incorporate new best practices
3. **Refine Patterns**: Improve pattern implementations
4. **Expand Coverage**: Add new scenarios and examples
5. **Gather Feedback**: Learn from usage and issues

---

*Generated with skill_builder tool*
