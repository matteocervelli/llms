#!/usr/bin/env bash
# Tech debt scanner — multi-language, graceful skip on missing tools
# Usage: scan.sh [path] [--duplicates|--todos|--dead-code]
# Outputs labeled sections for each check category.

set -euo pipefail

SCAN_PATH="${1:-.}"
FILTER="${2:-}"

has() { command -v "$1" &>/dev/null; }
section() { echo; echo "=== $1 ==="; }

detect_langs() {
  local path="$1"
  HAVE_PYTHON=false; HAVE_JS=false
  find "$path" -name "*.py" -not -path "*/node_modules/*" -not -path "*/.venv/*" \
    -not -path "*/__pycache__/*" 2>/dev/null | head -1 | grep -q . && HAVE_PYTHON=true
  find "$path" \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" \) \
    -not -path "*/node_modules/*" -not -path "*/dist/*" 2>/dev/null | head -1 | grep -q . && HAVE_JS=true
}

scan_todos() {
  section "TODOs / FIXMEs / HACKs"
  grep -rn "TODO\|FIXME\|HACK\|XXX\|TEMP\|DEPRECATED" "$SCAN_PATH" \
    --include="*.py" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.sh" \
    --exclude-dir=".venv" --exclude-dir="node_modules" --exclude-dir="dist" \
    --exclude-dir=".next" --exclude-dir="__pycache__" --exclude-dir=".git" \
    2>/dev/null || echo "(none found)"
}

scan_large_files() {
  section "Oversized files (>500 lines)"
  find "$SCAN_PATH" \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.tsx" \) \
    -not -path "*/node_modules/*" -not -path "*/.venv/*" 2>/dev/null \
    | xargs wc -l 2>/dev/null \
    | awk '$1 > 500 && $2 != "total"' \
    | sort -rn || echo "(none)"
}

scan_duplicates() {
  section "Duplicated code"
  if $HAVE_PYTHON && has pylint; then
    echo "[Python — pylint]"
    pylint --disable=all --enable=duplicate-code "$SCAN_PATH" 2>/dev/null \
      | grep -v "^$\|^-\|Your code" || echo "(no duplicates or pylint unavailable)"
  fi
  if $HAVE_JS && has npx; then
    echo "[JS/TS — jscpd]"
    npx --yes jscpd "$SCAN_PATH" --min-lines 10 --reporters console \
      --ignore "node_modules,dist,.next" 2>/dev/null || echo "(jscpd unavailable)"
  fi
}

scan_dead_code() {
  section "Dead code"
  if $HAVE_PYTHON && has vulture; then
    echo "[Python — vulture]"
    vulture "$SCAN_PATH" --min-confidence 80 2>/dev/null || echo "(vulture unavailable)"
  fi
  if $HAVE_JS && has npx; then
    echo "[TS — ts-prune]"
    npx --yes ts-prune 2>/dev/null || echo "(ts-prune unavailable)"
  fi
}

scan_complexity() {
  section "Complexity hotspots (CC > 10)"
  if $HAVE_PYTHON && has radon; then
    echo "[Python — radon cc]"
    radon cc "$SCAN_PATH" -nc --min C 2>/dev/null || echo "(radon unavailable)"
    echo
    echo "[Python — oversized functions (radon raw)]"
    radon raw "$SCAN_PATH" -s 2>/dev/null \
      | grep -E "LOC: [5-9][0-9]|LOC: [1-9][0-9]{2}" || echo "(none or radon unavailable)"
  fi
  if $HAVE_JS && has npx; then
    echo "[JS/TS — eslint complexity]"
    npx eslint "$SCAN_PATH" --rule 'complexity: [warn, 10]' \
      --rule 'max-lines-per-function: [warn, 50]' 2>/dev/null \
      | head -40 || echo "(eslint unavailable)"
  fi
}

scan_circular() {
  section "Circular imports"
  if $HAVE_PYTHON && has pycycle; then
    echo "[Python — pycycle]"
    pycycle --here 2>/dev/null || echo "(pycycle unavailable)"
  fi
  if $HAVE_JS && has npx; then
    echo "[TS — madge]"
    npx --yes madge --circular "$SCAN_PATH" 2>/dev/null || echo "(madge unavailable)"
  fi
}

# --- main ---
detect_langs "$SCAN_PATH"
echo "Scanning: $SCAN_PATH  (python=$HAVE_PYTHON  js/ts=$HAVE_JS)"

case "$FILTER" in
  --todos)     scan_todos ;;
  --dead-code) scan_dead_code ;;
  --duplicates) scan_duplicates ;;
  *)
    scan_todos
    scan_large_files
    scan_duplicates
    scan_dead_code
    scan_complexity
    scan_circular
    ;;
esac
