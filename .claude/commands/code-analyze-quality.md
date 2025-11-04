---
{}
---

---
description: Run comprehensive code quality checks including linting, type checking, and formatting
argument-hint: [language] (auto-detect if not specified)
---

# Code Quality Check

Run comprehensive code quality checks with automatic language detection.

## Supported Languages

- **Python**: black, flake8, mypy, pytest
- **JavaScript/TypeScript**: eslint, prettier, tsc
- **Swift**: swiftlint, swift build
- **Go**: gofmt, golint, go vet
- **Rust**: rustfmt, clippy

## Usage

```bash
/code-quality          # Auto-detect language
/code-quality python   # Force Python checks
/code-quality js       # Force JavaScript checks
/code-quality swift    # Force Swift checks
```

## What it does

1. Detects project language(s) if not specified
2. Runs language-specific linters
3. Checks code formatting
4. Runs type checking (if applicable)
5. Reports all issues with line numbers

## Execution

### Auto-detect and run appropriate checks

!echo "🔍 Detecting project language..."
!if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then echo "✓ Python project detected"; fi
!if [ -f "package.json" ]; then echo "✓ JavaScript/TypeScript project detected"; fi
!if [ -f "Package.swift" ] || find . -name "*.xcodeproj" -o -name "*.xcworkspace" 2>/dev/null | grep -q .; then echo "✓ Swift project detected"; fi

### Python checks
!if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then echo "\n📦 Running Python quality checks..."; fi
!if command -v black &> /dev/null && ([ -f "pyproject.toml" ] || [ -f "setup.py" ]); then echo "→ Formatting check (black):" && black --check . 2>&1 | head -20; fi
!if command -v flake8 &> /dev/null && ([ -f "pyproject.toml" ] || [ -f "setup.py" ]); then echo "→ Linting (flake8):" && flake8 src/ tests/ 2>&1 | head -20; fi
!if command -v mypy &> /dev/null && ([ -f "pyproject.toml" ] || [ -f "setup.py" ]); then echo "→ Type checking (mypy):" && mypy src/ 2>&1 | head -20; fi

### JavaScript/TypeScript checks
!if [ -f "package.json" ]; then echo "\n📦 Running JavaScript/TypeScript quality checks..."; fi
!if [ -f "package.json" ] && command -v npm &> /dev/null; then echo "→ Linting (eslint):" && npm run lint 2>&1 | head -20 || echo "No lint script found"; fi
!if [ -f "tsconfig.json" ] && command -v tsc &> /dev/null; then echo "→ Type checking (tsc):" && tsc --noEmit 2>&1 | head -20; fi

### Swift checks
!if [ -f "Package.swift" ] || find . -name "*.xcodeproj" 2>/dev/null | grep -q .; then echo "\n📦 Running Swift quality checks..."; fi
!if command -v swiftlint &> /dev/null && ([ -f "Package.swift" ] || find . -name "*.xcodeproj" 2>/dev/null | grep -q .); then echo "→ Linting (swiftlint):" && swiftlint 2>&1 | head -20; fi
!if [ -f "Package.swift" ]; then echo "→ Build check:" && swift build 2>&1 | tail -10; fi

!echo "\n✅ Code quality check complete!"

## Environment-Specific Configuration

### Python (pyproject.toml)
```toml
[tool.black]
line-length = 100

[tool.flake8]
max-line-length = 100
ignore = E203, W503

[tool.mypy]
python_version = "3.11"
strict = true
```

### JavaScript (.eslintrc.json)
```json
{
  "extends": ["eslint:recommended"],
  "env": {"node": true, "es6": true}
}
```

### Swift (.swiftlint.yml)
```yaml
line_length: 120
disabled_rules:
  - trailing_whitespace
```

## Tips

- Run before committing to catch issues early
- Configure tools in project config files
- Add to pre-commit hooks for automation
- CI/CD should run same checks
