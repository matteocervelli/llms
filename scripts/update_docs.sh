#!/usr/bin/env bash
#
# update_docs.sh - Weekly Documentation Update Automation
#
# Automatically updates LLM provider documentation using the doc_fetcher tool.
# Designed for cron execution with comprehensive logging and optional email notifications.
#
# Usage:
#   ./scripts/update_docs.sh
#
# Cron Example (Sundays at 2 AM):
#   0 2 * * 0 cd ~/.claude/llms && ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1
#
# Exit Codes:
#   0 - Success (all documents updated or unchanged)
#   1 - Partial failure (some documents failed)
#   2 - Fatal error (script misconfiguration or environment issue)
#

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# ============================================================================
# CONFIGURATION
# ============================================================================

# Project paths (must be absolute or relative to script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_DIR="${PROJECT_ROOT}/logs/doc_fetcher"
MANIFEST_PATH="${PROJECT_ROOT}/manifests/docs.json"

# Log retention (days)
LOG_RETENTION_DAYS=30

# Email notification (optional)
# Set NOTIFY_EMAIL to enable email alerts on errors
# Example: NOTIFY_EMAIL="admin@example.com"
NOTIFY_EMAIL="${DOC_UPDATER_EMAIL:-}"  # Read from environment variable

# Python command (use system Python or venv)
PYTHON_CMD="${PYTHON_CMD:-python}"

# ============================================================================
# LOGGING FUNCTIONS
# ============================================================================

# Generate log filename with timestamp
get_log_filename() {
    echo "update_$(date +%Y%m%d_%H%M%S).log"
}

# Log message with timestamp
log_message() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*"
}

log_info() {
    log_message "INFO" "$@"
}

log_warn() {
    log_message "WARN" "$@"
}

log_error() {
    log_message "ERROR" "$@"
}

log_success() {
    log_message "SUCCESS" "$@"
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# Rotate old log files
rotate_logs() {
    log_info "Rotating logs older than ${LOG_RETENTION_DAYS} days..."

    local deleted_count=0

    # Find and delete old log files
    if command -v find >/dev/null 2>&1; then
        deleted_count=$(find "${LOG_DIR}" -name "update_*.log" -type f -mtime "+${LOG_RETENTION_DAYS}" -delete -print | wc -l | tr -d ' ')

        if [ "${deleted_count}" -gt 0 ]; then
            log_info "Deleted ${deleted_count} old log file(s)"
        else
            log_info "No old logs to delete"
        fi
    else
        log_warn "find command not available, skipping log rotation"
    fi
}

# Send email notification
send_email_notification() {
    local subject="$1"
    local body="$2"

    if [ -z "${NOTIFY_EMAIL}" ]; then
        return 0  # Email notifications disabled
    fi

    log_info "Sending email notification to ${NOTIFY_EMAIL}..."

    # Check if mail command is available
    if ! command -v mail >/dev/null 2>&1; then
        log_warn "mail command not found, skipping email notification"
        log_warn "Install mailutils: brew install mailutils (macOS) or apt install mailutils (Linux)"
        return 0
    fi

    # Send email
    echo "${body}" | mail -s "${subject}" "${NOTIFY_EMAIL}" 2>/dev/null || {
        log_warn "Failed to send email notification"
        return 1
    }

    log_success "Email notification sent successfully"
}

# Validate environment
validate_environment() {
    log_info "Validating environment..."

    # Check if running from correct directory
    if [ ! -f "${PROJECT_ROOT}/requirements.txt" ]; then
        log_error "Project root not found. Expected: ${PROJECT_ROOT}"
        log_error "Please run from project root: cd ~/.claude/llms && ./scripts/update_docs.sh"
        return 2
    fi

    # Check if Python is available
    if ! command -v "${PYTHON_CMD}" >/dev/null 2>&1; then
        log_error "Python not found. Please install Python 3.11+ or set PYTHON_CMD environment variable"
        return 2
    fi

    # Check Python version (3.11+)
    local python_version
    python_version=$("${PYTHON_CMD}" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")

    if ! awk -v ver="${python_version}" 'BEGIN {if (ver < 3.11) exit 1}'; then
        log_error "Python ${python_version} is too old. Required: Python 3.11+"
        return 2
    fi

    log_info "Using Python ${python_version}"

    # Check if doc_fetcher module is available
    if ! "${PYTHON_CMD}" -c "import src.tools.doc_fetcher" 2>/dev/null; then
        log_error "doc_fetcher module not found. Please install dependencies:"
        log_error "  cd ${PROJECT_ROOT} && pip install -r requirements.txt"
        return 2
    fi

    # Check if manifest exists
    if [ ! -f "${MANIFEST_PATH}" ]; then
        log_warn "Manifest not found: ${MANIFEST_PATH}"
        log_warn "No documents to update. Run 'python -m src.tools.doc_fetcher fetch --all' first."
        return 0  # Not fatal, just no work to do
    fi

    log_success "Environment validation passed"
    return 0
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main() {
    local log_file="${LOG_DIR}/$(get_log_filename)"
    local exit_code=0
    local start_time
    local end_time
    local duration

    # Create log directory if it doesn't exist
    mkdir -p "${LOG_DIR}"
    chmod 750 "${LOG_DIR}" 2>/dev/null || true

    # Redirect all output to log file (and still show on stdout)
    exec > >(tee -a "${log_file}") 2>&1

    log_info "========================================"
    log_info "Documentation Update - Starting"
    log_info "========================================"
    log_info "Project: ${PROJECT_ROOT}"
    log_info "Log: ${log_file}"
    log_info "Timestamp: $(date '+%Y-%m-%d %H:%M:%S %Z')"

    start_time=$(date +%s)

    # Rotate old logs
    rotate_logs

    # Validate environment
    if ! validate_environment; then
        exit_code=$?
        log_error "Environment validation failed with code ${exit_code}"

        send_email_notification \
            "[ERROR] Documentation Update - Environment Validation Failed" \
            "Environment validation failed. Please check the log at: ${log_file}"

        return "${exit_code}"
    fi

    # Check if manifest exists (might be empty after validation)
    if [ ! -f "${MANIFEST_PATH}" ]; then
        log_info "No manifest found. Nothing to update."
        log_info "========================================"
        log_success "Documentation Update - Completed (No Work)"
        log_info "========================================"
        return 0
    fi

    # Run doc_fetcher update command
    log_info "Starting documentation update..."
    log_info "Running: python -m src.tools.doc_fetcher update"
    log_info "----------------------------------------"

    if cd "${PROJECT_ROOT}" && "${PYTHON_CMD}" -m src.tools.doc_fetcher update; then
        exit_code=0
        log_success "Documentation update completed successfully"
    else
        exit_code=$?
        log_error "Documentation update failed with exit code ${exit_code}"

        # Send email notification on error
        send_email_notification \
            "[ERROR] Documentation Update Failed" \
            "Documentation update failed with exit code ${exit_code}. Please check the log at: ${log_file}"
    fi

    log_info "----------------------------------------"

    # Calculate duration
    end_time=$(date +%s)
    duration=$((end_time - start_time))

    log_info "========================================"
    if [ "${exit_code}" -eq 0 ]; then
        log_success "Documentation Update - Completed Successfully"
    else
        log_error "Documentation Update - Completed with Errors"
    fi
    log_info "========================================"
    log_info "Duration: ${duration} seconds"
    log_info "Exit Code: ${exit_code}"

    # Set log file permissions (owner read/write, group read, no world access)
    chmod 640 "${log_file}" 2>/dev/null || true

    return "${exit_code}"
}

# Run main function and exit with its exit code
main
exit $?
