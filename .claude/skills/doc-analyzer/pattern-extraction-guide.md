# Pattern Extraction Guide

## Overview

This guide provides techniques for extracting code patterns, usage examples, and integration strategies from library and framework documentation. Use these methods to transform raw documentation into actionable implementation guidance.

---

## Pattern Recognition Techniques

### 1. Keyword-Based Detection

**Method:** Identify sections containing specific keywords related to patterns.

```python
def detect_pattern_section(section: dict, keywords: list) -> bool:
    """
    Detect if section contains pattern-related keywords.
    """
    text = f"{section['title']} {section['content']}".lower()
    return any(keyword.lower() in text for keyword in keywords)

# Pattern type keywords
PATTERN_KEYWORDS = {
    "initialization": ["setup", "initialize", "config", "getting started", "__init__"],
    "usage": ["example", "usage", "how to", "tutorial", "guide"],
    "integration": ["integrate", "combination", "together", "with", "plugin"],
    "testing": ["test", "testing", "unittest", "pytest", "mock"],
    "error_handling": ["error", "exception", "handle", "try", "catch"]
}
```

### 2. Code Block Analysis

**Method:** Extract and analyze code blocks from documentation.

```python
import re

def extract_code_blocks(content: str, language: str = None) -> list:
    """
    Extract code blocks from markdown content.
    """
    # Regex for fenced code blocks
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)

    code_blocks = []
    for lang, code in matches:
        if language is None or lang == language:
            code_blocks.append({
                "language": lang or "unknown",
                "code": code.strip(),
                "lines": len(code.strip().split("\n"))
            })

    return code_blocks

def categorize_code_block(code: str, language: str) -> str:
    """
    Categorize code block by type.
    """
    # Initialization patterns
    if re.search(r"(app|client|connection)\s*=", code):
        return "initialization"

    # Function/class definitions
    if re.search(r"^(def|class|async def)", code, re.MULTILINE):
        return "definition"

    # Usage examples
    if re.search(r"@|\.get\(|\.post\(|\.put\(", code):
        return "usage"

    # Test patterns
    if re.search(r"test_|assert|mock", code):
        return "testing"

    return "generic"
```

### 3. Structural Analysis

**Method:** Analyze documentation structure to identify pattern locations.

```python
def analyze_documentation_structure(docs: dict) -> dict:
    """
    Analyze documentation structure for pattern indicators.
    """
    structure = {
        "quick_start": find_sections(docs, ["quick start", "getting started"]),
        "tutorials": find_sections(docs, ["tutorial", "guide", "walkthrough"]),
        "examples": find_sections(docs, ["example", "sample"]),
        "api_reference": find_sections(docs, ["api", "reference", "documentation"]),
        "best_practices": find_sections(docs, ["best practice", "guidelines"]),
        "migration": find_sections(docs, ["migration", "upgrading", "changelog"])
    }

    return structure
```

---

## Pattern Extraction Methods

### Initialization Patterns

**Goal:** Extract setup and configuration patterns.

```python
def extract_initialization_patterns(docs: dict) -> list:
    """
    Extract initialization patterns from documentation.
    """
    patterns = []

    # Find setup sections
    setup_sections = find_sections(docs, ["setup", "initialize", "config"])

    for section in setup_sections:
        code_blocks = extract_code_blocks(section["content"])

        for code in code_blocks:
            patterns.append({
                "type": "initialization",
                "title": section["title"],
                "code": code["code"],
                "language": code["language"],
                "prerequisites": extract_prerequisites(section),
                "complexity": assess_complexity(code)
            })

    return patterns

def extract_prerequisites(section: dict) -> list:
    """
    Extract prerequisites from section content.
    """
    prereq_indicators = ["require", "need", "must have", "prerequisite", "install"]
    prerequisites = []

    for line in section["content"].split("\n"):
        if any(indicator in line.lower() for indicator in prereq_indicators):
            prerequisites.append(line.strip())

    return prerequisites
```

### Usage Patterns

**Goal:** Extract common usage examples and patterns.

```python
def extract_usage_patterns(docs: dict, api_element: str = None) -> list:
    """
    Extract usage patterns, optionally filtered by API element.
    """
    patterns = []

    # Find example/usage sections
    usage_sections = find_sections(docs, ["example", "usage", "how to"])

    for section in usage_sections:
        code_blocks = extract_code_blocks(section["content"])

        for code in code_blocks:
            # Filter by API element if specified
            if api_element and api_element not in code["code"]:
                continue

            patterns.append({
                "type": "usage",
                "api_element": identify_api_element(code["code"]),
                "use_case": infer_use_case(section["title"], code["code"]),
                "code": code["code"],
                "language": code["language"],
                "complexity": assess_complexity(code),
                "runnable": validate_runnability(code)
            })

    return patterns

def identify_api_element(code: str) -> str:
    """
    Identify primary API element in code.
    """
    # Look for decorators
    decorator_match = re.search(r"@(\w+\.\w+)", code)
    if decorator_match:
        return decorator_match.group(1)

    # Look for class/function definitions
    def_match = re.search(r"(class|def)\s+(\w+)", code)
    if def_match:
        return def_match.group(2)

    return "unknown"
```

### Integration Patterns

**Goal:** Extract patterns for integrating multiple libraries.

```python
def extract_integration_patterns(docs: dict, libraries: list) -> list:
    """
    Extract integration patterns between libraries.
    """
    patterns = []

    # Find integration sections
    integration_sections = find_sections(docs, ["integrate", "combination", "together"])

    for section in integration_sections:
        # Identify libraries mentioned
        mentioned_libs = [lib for lib in libraries if lib.lower() in section["content"].lower()]

        if mentioned_libs:
            code_blocks = extract_code_blocks(section["content"])

            for code in code_blocks:
                patterns.append({
                    "type": "integration",
                    "libraries": mentioned_libs,
                    "pattern": section["title"],
                    "code": code["code"],
                    "compatibility": extract_compatibility(section),
                    "configuration_needed": requires_configuration(code)
                })

    return patterns
```

---

## Pattern Validation

### Code Example Validation

**Goal:** Validate that code examples are complete and runnable.

```python
def validate_runnability(code: dict) -> bool:
    """
    Validate if code example is runnable.
    """
    code_str = code["code"]

    # Check for incomplete code indicators
    if "..." in code_str or "# ..." in code_str:
        return False

    # Check for required imports
    if uses_external_library(code_str) and not has_imports(code_str):
        return False

    # Check for syntax errors (basic)
    try:
        compile(code_str, "<string>", "exec")
        return True
    except SyntaxError:
        return False

def extract_dependencies(code: dict) -> list:
    """
    Extract dependencies from code example.
    """
    dependencies = []

    # Extract from imports
    import_pattern = r"(?:from|import)\s+(\w+)"
    matches = re.findall(import_pattern, code["code"])

    for module in matches:
        if module not in ["os", "sys", "re", "json"]:  # Skip stdlib
            dependencies.append(module)

    return list(set(dependencies))
```

### Pattern Complexity Assessment

**Goal:** Assess complexity of code patterns.

```python
def assess_complexity(code: dict) -> str:
    """
    Assess complexity of code pattern.
    """
    code_str = code["code"]
    lines = code_str.strip().split("\n")

    # Simple heuristics
    line_count = len(lines)
    has_classes = "class " in code_str
    has_async = "async " in code_str
    import_count = code_str.count("import ")
    decorator_count = code_str.count("@")

    # Complexity scoring
    score = 0
    score += min(line_count // 10, 3)  # Lines (0-3 points)
    score += 2 if has_classes else 0
    score += 1 if has_async else 0
    score += min(import_count // 3, 2)
    score += min(decorator_count // 2, 1)

    if score <= 2:
        return "simple"
    elif score <= 5:
        return "intermediate"
    else:
        return "advanced"
```

---

## Pattern Categorization

### By Complexity

```python
def categorize_by_complexity(patterns: list) -> dict:
    """
    Categorize patterns by complexity level.
    """
    categorized = {
        "simple": [],
        "intermediate": [],
        "advanced": []
    }

    for pattern in patterns:
        complexity = pattern.get("complexity", "intermediate")
        categorized[complexity].append(pattern)

    return categorized
```

### By Feature

```python
def categorize_by_feature(patterns: list) -> dict:
    """
    Categorize patterns by feature/API element.
    """
    categorized = {}

    for pattern in patterns:
        feature = pattern.get("api_element", "general")

        if feature not in categorized:
            categorized[feature] = []

        categorized[feature].append(pattern)

    return categorized
```

### By Use Case

```python
def infer_use_case(title: str, code: str) -> str:
    """
    Infer use case from title and code.
    """
    title_lower = title.lower()
    code_lower = code.lower()

    # Common use cases
    use_cases = {
        "authentication": ["auth", "login", "token", "jwt", "oauth"],
        "database": ["database", "query", "sql", "db", "model"],
        "api_endpoint": ["endpoint", "route", "@app", "get", "post"],
        "validation": ["validate", "pydantic", "schema", "validator"],
        "testing": ["test", "mock", "assert", "pytest"],
        "error_handling": ["error", "exception", "try", "catch"],
        "async_operations": ["async", "await", "asyncio"],
        "file_operations": ["file", "read", "write", "open"],
    }

    for use_case, keywords in use_cases.items():
        if any(kw in title_lower or kw in code_lower for kw in keywords):
            return use_case

    return "general"
```

---

## Best Practices

### 1. Focus on Relevance
- Extract patterns relevant to feature requirements
- Prioritize commonly used patterns
- Filter by complexity appropriate to feature
- Avoid extracting every possible pattern

### 2. Validate Examples
- Check code syntax
- Verify dependencies
- Test runnability when possible
- Document prerequisites

### 3. Maintain Context
- Include surrounding explanation
- Note version information
- Document source URL
- Preserve rationale

### 4. Systematic Organization
- Use consistent categorization
- Tag with metadata (complexity, use case)
- Link related patterns
- Create pattern hierarchies

### 5. Quality Over Quantity
- Prefer complete, working examples
- Avoid code fragments
- Include only tested patterns
- Document known limitations

---

**Version:** 2.0.0
**Last Updated:** 2025-10-29
**Maintainer:** Documentation Researcher Agent
