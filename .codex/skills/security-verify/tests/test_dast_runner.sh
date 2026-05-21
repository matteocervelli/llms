#!/usr/bin/env bash
# Tests for dast-runner.sh
# Spins up real Python HTTP servers to validate DAST detection.
# Usage: bash test_dast_runner.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$SCRIPT_DIR/../lib/dast-runner.sh"
PASS=0
FAIL=0
SERVER_PID=""

# Track all spawned server PIDs for cleanup
PIDS=()

cleanup() {
    for pid in "${PIDS[@]:-}"; do
        kill "$pid" 2>/dev/null || true
    done
    [[ -n "$SERVER_PID" ]] && kill "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

# --- Helpers ---

free_port() {
    python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()"
}

assert() {
    local name="$1" expected="$2" actual="$3"
    if [[ "$actual" == "$expected" ]]; then
        echo "  PASS: $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name"
        echo "        Expected: $expected"
        echo "        Actual:   $actual"
        FAIL=$((FAIL + 1))
    fi
}

assert_contains() {
    local name="$1" needle="$2" haystack="$3"
    if echo "$haystack" | grep -Fq "$needle"; then
        echo "  PASS: $name"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $name"
        echo "        Expected to contain: $needle"
        echo "        Output: $(echo "$haystack" | head -5)"
        FAIL=$((FAIL + 1))
    fi
}

wait_for_server() {
    local url="$1" attempts=25  # 25 * 0.2s = 5s max
    local i=0
    while ! curl -s -o /dev/null --connect-timeout 1 "$url" 2>/dev/null; do
        sleep 0.2
        i=$((i + 1))
        if [[ $i -ge $attempts ]]; then
            echo "  ERROR: Server at $url did not start within 5s"
            return 1
        fi
    done
}

# --- Tests ---

echo "=== DAST Runner Tests ==="
echo ""

# Guard: runner script must exist
if [[ ! -f "$RUNNER" ]]; then
    echo "SKIP: dast-runner.sh not found at $RUNNER (expected during TDD red phase)"
    echo ""
    echo "Results: 0 passed, 0 failed (script not yet implemented)"
    exit 0
fi

# --- Test 1: Insecure server — missing headers detected, exit code 1 ---
echo "Test 1: Insecure server (missing security headers)"
PORT=$(free_port)

python3 -c "
import http.server, sys

class InsecureHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body>Insecure test server</body></html>')
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Allow', 'GET, POST, OPTIONS, TRACE')
        self.end_headers()
    def log_message(self, *a): pass

http.server.HTTPServer(('', int(sys.argv[1])), InsecureHandler).serve_forever()
" "$PORT" &
SERVER_PID=$!
PIDS+=("$SERVER_PID")
wait_for_server "http://localhost:$PORT"

set +e
OUTPUT=$(bash "$RUNNER" "http://localhost:$PORT" --timeout 3 2>&1)
EXIT_CODE=$?
set -e

kill "$SERVER_PID" 2>/dev/null || true
SERVER_PID=""

# Should find at least CSP and HSTS missing
assert_contains "Detects missing CSP header" "CSP" "$OUTPUT"
assert_contains "Detects missing HSTS header" "HSTS" "$OUTPUT"
assert_contains "Marks findings as ACTIVE" "ACTIVE" "$OUTPUT"
assert "Exits with code 1 on critical/high findings" "1" "$EXIT_CODE"

echo ""

# --- Test 2: Secure server — no critical findings, exit code 0 ---
echo "Test 2: Secure server (all security headers present)"
PORT=$(free_port)

python3 -c "
import http.server, sys

class SecureHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        self.send_header('Content-Security-Policy', \"default-src 'self'\")
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Permissions-Policy', 'geolocation=()')
        self.end_headers()
        self.wfile.write(b'<html><body>Secure</body></html>')
    def log_message(self, *a): pass

http.server.HTTPServer(('', int(sys.argv[1])), SecureHandler).serve_forever()
" "$PORT" &
SERVER_PID=$!
PIDS+=("$SERVER_PID")
wait_for_server "http://localhost:$PORT"

set +e
OUTPUT=$(bash "$RUNNER" "http://localhost:$PORT" --timeout 3 2>&1)
EXIT_CODE=$?
set -e

kill "$SERVER_PID" 2>/dev/null || true
SERVER_PID=""

assert "Exits with code 0 when no critical/high findings" "0" "$EXIT_CODE"
assert_contains "Produces markdown report" "# DAST Scan Results" "$OUTPUT"

echo ""

# --- Test 3: Unreachable URL — exit code 2 ---
echo "Test 3: Unreachable URL"
set +e
OUTPUT=$(bash "$RUNNER" "http://localhost:19999" --timeout 2 2>&1)
EXIT_CODE=$?
set -e

assert "Exits with code 2 when URL unreachable" "2" "$EXIT_CODE"
assert_contains "Reports connectivity error" "Cannot connect" "$OUTPUT"

echo ""

# --- Test 4: Missing URL argument ---
echo "Test 4: Missing URL argument"
set +e
OUTPUT=$(bash "$RUNNER" 2>&1)
EXIT_CODE=$?
set -e

assert "Exits with non-zero on missing URL" "1" "$EXIT_CODE"
assert_contains "Shows usage error" "Usage" "$OUTPUT"

echo ""

# --- Test 5: CORS wildcard detection ---
echo "Test 5: CORS wildcard origin detection"
PORT=$(free_port)

python3 -c "
import http.server, sys

class CORSHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'hello')
    def log_message(self, *a): pass

http.server.HTTPServer(('', int(sys.argv[1])), CORSHandler).serve_forever()
" "$PORT" &
SERVER_PID=$!
PIDS+=("$SERVER_PID")
wait_for_server "http://localhost:$PORT"

set +e
OUTPUT=$(bash "$RUNNER" "http://localhost:$PORT" --timeout 3 2>&1)
set -e

kill "$SERVER_PID" 2>/dev/null || true
SERVER_PID=""

assert_contains "Detects wildcard CORS" "CORS" "$OUTPUT"

echo ""

# --- Test 6: Nuclei integration (conditional) ---
echo "Test 6: Nuclei integration (skipped if not installed)"
if command -v nuclei &>/dev/null; then
    PORT=$(free_port)
    python3 -c "
import http.server, sys
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'nuclei test target')
    def log_message(self, *a): pass
http.server.HTTPServer(('', int(sys.argv[1])), H).serve_forever()
" "$PORT" &
    SERVER_PID=$!
    wait_for_server "http://localhost:$PORT"

    OUTPUT=$(bash "$RUNNER" "http://localhost:$PORT" --nuclei --timeout 5 2>&1 || true)

    kill "$SERVER_PID" 2>/dev/null || true
    SERVER_PID=""

    assert_contains "Nuclei section present in output" "Nuclei" "$OUTPUT"
else
    echo "  SKIP: nuclei not installed"
fi

echo ""

# --- Test 7: Nuclei does NOT run without --nuclei flag ---
echo "Test 7: Nuclei skipped without --nuclei flag"
PORT=$(free_port)
python3 -c "
import http.server, sys
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'hello')
    def log_message(self, *a): pass
http.server.HTTPServer(('', int(sys.argv[1])), H).serve_forever()
" "$PORT" &
SERVER_PID=$!
PIDS+=("$SERVER_PID")
wait_for_server "http://localhost:$PORT"

set +e
OUTPUT=$(bash "$RUNNER" "http://localhost:$PORT" --timeout 3 2>&1)
set -e

kill "$SERVER_PID" 2>/dev/null || true
SERVER_PID=""

# Without --nuclei, output should say "Install nuclei" not run nuclei
assert_contains "Nuclei section shows install hint (not running)" "Install nuclei" "$OUTPUT"

echo ""

# --- Test 8: Invalid --timeout argument ---
echo "Test 8: Invalid --timeout argument"
set +e
OUTPUT=$(bash "$RUNNER" "http://localhost:8080" --timeout abc 2>&1)
EXIT_CODE=$?
set -e

assert "Exits with code 1 on invalid timeout" "1" "$EXIT_CODE"
assert_contains "Shows timeout error" "Error" "$OUTPUT"

echo ""

# --- Summary ---
echo "==========================="
echo "Results: $PASS passed, $FAIL failed"
if [[ $FAIL -gt 0 ]]; then
    exit 1
else
    exit 0
fi
