---
paths:
  - "**/*.py"
  - "**/*.ts"
  - "**/*.tsx"
  - "**/*.js"
  - "**/*.jsx"
  - "**/*.go"
  - "**/*.rs"
  - "**/*.rb"
---

# Anti-Slop — AI Code Quality Patterns to Avoid

Flag these patterns during `/review` and `/quality-check`. They are common in
AI-generated code and indicate over-engineering, defensive noise, or lazy output.

## Structural Anti-Patterns

**Unnecessary wrapper class** — a class with one method that does nothing but call another function:

```python
# Bad
class FileReader:
    def read(self, path): return open(path).read()

# Good
def read_file(path): return open(path).read()
```

**Single-use abstraction** — factory/strategy/builder for exactly one implementation. Three similar
lines is better than a premature abstraction.

**Redundant return await** — `return await` is identical to `return` in an async function
that doesn't need the await for cleanup:

```python
# Bad (unless caller needs cleanup behavior)
async def fetch(): return await http.get(url)
# Good
async def fetch(): return http.get(url)
```

## Error Handling Anti-Patterns

**Bare exception with pass** — silently swallows all errors, makes debugging impossible:

```python
# Bad
try:
    do_thing()
except Exception:
    pass

# Good: log, re-raise, or handle specifically
except ValueError as e:
    logger.warning("Expected value error: %s", e)
```

**Catch-all error handler** — catches Exception where only 1-2 specific types are possible.

## Comment Anti-Patterns

**Comment restates the code** — reader can see what the code does; comment only needed for WHY:

```python
# Bad: "increment the counter"
counter += 1

# Bad: "return the result"
return result

# Good: explains non-obvious constraint
# Cap at 100 to match API rate limit (confirmed with vendor 2026-04)
MAX_RETRIES = 100
```

**Multi-paragraph docstring for simple function** — one line max unless the function has
non-obvious behavior, side effects, or required contract.

## Import Anti-Patterns

**Unused import kept "for safety"** — dead code that confuses grep and increases bundle size.
Delete it. If it was needed, git history has it.

**Star imports** — `from module import *` pollutes namespace and breaks linters.

## When to Flag vs When to Skip

Flag: pattern appears in code YOU (Claude) just wrote or modified.
Skip: pre-existing code in files you didn't touch this session — treat as tech debt,
not a blocker. Open a `/techdebt` note instead.
