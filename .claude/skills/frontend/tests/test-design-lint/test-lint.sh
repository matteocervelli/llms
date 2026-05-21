#!/usr/bin/env bash
# test-lint.sh — Test runner for design-lint.sh.
# WHY: The lint script is deterministic; its correctness must be verified mechanically,
# not by reading it. These tests catch regressions when rules or patterns change.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LINT="$SCRIPT_DIR/../../scripts/design-lint.sh"
FIXTURES="$SCRIPT_DIR/fixtures"
PASS=0
FAIL=0

pass() { echo "PASS: $1"; PASS=$(( PASS + 1 )); }
fail() { echo "FAIL: $1"; FAIL=$(( FAIL + 1 )); }

assert_exit() {
  local desc="$1" expected="$2"; shift 2
  local actual=0
  "$@" &>/dev/null || actual=$?
  [[ "$actual" -eq "$expected" ]] && pass "$desc" || fail "$desc (got exit $actual, want $expected)"
}

assert_contains() {
  local desc="$1" pattern="$2"; shift 2
  local out
  out=$("$@" 2>&1 || true)
  echo "$out" | grep -qF "$pattern" && pass "$desc" || fail "$desc (pattern '$pattern' not found in output)"
}

assert_not_contains() {
  local desc="$1" pattern="$2"; shift 2
  local out
  out=$("$@" 2>&1 || true)
  echo "$out" | grep -qF "$pattern" && fail "$desc (pattern '$pattern' should not appear)" || pass "$desc"
}

assert_valid_json() {
  local desc="$1"; shift
  local out
  out=$("$@" 2>&1 || true)
  echo "$out" | python3 -c "import sys,json; json.load(sys.stdin)" &>/dev/null \
    && pass "$desc" || fail "$desc (output is not valid JSON)"
}

# Test 1: violations.css → exit 1
assert_exit "violations.css exits 1" 1 \
  bash "$LINT" "$FIXTURES/violations.css"

# Test 2: violations.css → banned-font-primary found
assert_contains "violations.css: banned-font-primary detected" "banned-font-primary" \
  bash "$LINT" "$FIXTURES/violations.css"

# Test 3: violations.css → pure-black found
assert_contains "violations.css: pure-black detected" "pure-black" \
  bash "$LINT" "$FIXTURES/violations.css"

# Test 4: violations.css → linear-timing found
assert_contains "violations.css: linear-timing detected" "linear-timing" \
  bash "$LINT" "$FIXTURES/violations.css"

# Test 5: clean.css → exit 0
assert_exit "clean.css exits 0" 0 \
  bash "$LINT" "$FIXTURES/clean.css"

# Test 6: clean.css → loader linear not flagged (infinite excluded)
assert_exit "clean.css: spin loader not flagged" 0 \
  bash "$LINT" "$FIXTURES/clean.css"

# Test 7: violations.css --mode brand → side-stripe NOT in output (product-only rule)
assert_not_contains "violations.css --mode brand: side-stripe absent" "side-stripe" \
  bash "$LINT" "$FIXTURES/violations.css" --mode brand

# Test 8: violations.css --json → valid JSON
assert_valid_json "violations.css --json produces valid JSON" \
  bash "$LINT" "$FIXTURES/violations.css" --json

echo ""
echo "Results: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]] && exit 0 || exit 1
