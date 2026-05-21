# User Guide Template

**Location**: `docs/guides/<feature-name>-guide.md`

Use this template for complex features that need detailed user documentation.

````markdown
# <Feature Name> User Guide

## Introduction

What is this feature and who is it for?

## Getting Started

### Prerequisites

- Requirement 1
- Requirement 2

### Installation

```bash
pip install required-package
```
````

### Basic Setup

```bash
llm-tool init feature-name
```

## Usage

### Basic Example

```python
# Simple example
from llms.feature import Feature

feature = Feature()
result = feature.process(data)
```

### Advanced Usage

#### Use Case 1: <Scenario>

[Step-by-step instructions]

#### Use Case 2: <Scenario>

[Step-by-step instructions]

## Configuration Options

| Option  | Type | Default   | Description  |
| ------- | ---- | --------- | ------------ |
| option1 | str  | "default" | What it does |

## Troubleshooting

### Common Issues

**Problem**: Error message or issue
**Solution**: How to fix it

## Best Practices

- Practice 1
- Practice 2

## Examples

### Example 1: <Scenario>

Full working example with explanation

### Example 2: <Scenario>

Another complete example

## FAQ

**Q: Question?**
A: Answer.

## References

- API Documentation: [link]
- Implementation: [link]

```

```
