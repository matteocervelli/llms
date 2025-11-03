---
description: Comprehensive product assessment using interactive or transcript analysis
argument-hint: [--interactive | --analyze <transcript-file>]
allowed-tools: [filesystem, context]
---

# Product Assessment

Conduct comprehensive product assessment using the @~/.claude/prompts/product-assessor.md prompt.

## Modes

**Interactive Mode** (recommended):
```bash
/product-assess --interactive
```
Guides you through structured product assessment questions one by one.

**Transcript Analysis Mode**:
```bash
/product-assess --analyze path/to/transcript.md
```
Extracts product insights from existing transcript or conversation file.

## Output

Generates assessment report with:
- Market fit analysis
- Value proposition clarity
- Target customer validation
- Competitive positioning
- Product-market readiness
- Recommendations
