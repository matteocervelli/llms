#!/usr/bin/env bash
# sync_github.sh - Wrapper for github_sync.py with enhanced CLI

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory and paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$(dirname "$(dirname "$SKILL_DIR")")")"

# Path to user-story-generator scripts
USER_STORY_GENERATOR_SCRIPTS="$(dirname "$(dirname "$SKILL_DIR")")/user-story-generator/scripts"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    print_error "python3 is required but not found"
    exit 1
fi

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    print_warning "GitHub CLI (gh) not found. Some features may not work."
    print_info "Install with: brew install gh"
fi

# Function to show usage
usage() {
    cat << EOF
Usage: $0 <command> [OPTIONS]

Sync user stories with GitHub issues.

Commands:
    create <story-id>           Create GitHub issue from story
    update <story-id>           Update existing GitHub issue
    sync <story-id>             Bi-directional sync (story ↔ issue)
    bulk <story-ids...>         Process multiple stories
    status                      Show GitHub sync status

Options:
    --dry-run                   Show what would be done without making changes
    --force                     Force operation even if warnings exist
    -h, --help                  Show this help message

Examples:
    # Create GitHub issue for a story
    $0 create US-0001

    # Update existing issue
    $0 update US-0001

    # Sync story with GitHub (bi-directional)
    $0 sync US-0001

    # Process multiple stories
    $0 bulk US-0001 US-0002 US-0003

    # Dry run to see what would happen
    $0 create US-0001 --dry-run

    # Check GitHub sync status
    $0 status

EOF
}

# Function to check GitHub authentication
check_gh_auth() {
    if command -v gh &> /dev/null; then
        if gh auth status &> /dev/null; then
            return 0
        else
            print_warning "GitHub CLI not authenticated"
            print_info "Run: gh auth login"
            return 1
        fi
    else
        print_warning "GitHub CLI not installed"
        return 1
    fi
}

# Function to create issue
create_issue() {
    local story_id="$1"
    local dry_run="${2:-false}"

    print_info "Creating GitHub issue for $story_id"

    local args="create $story_id"
    if [[ "$dry_run" == "true" ]]; then
        args="$args --dry-run"
    fi

    if python3 "$USER_STORY_GENERATOR_SCRIPTS/github_sync.py" $args; then
        print_success "Issue created successfully"
        return 0
    else
        print_error "Failed to create issue"
        return 1
    fi
}

# Function to update issue
update_issue() {
    local story_id="$1"
    local dry_run="${2:-false}"

    print_info "Updating GitHub issue for $story_id"

    local args="update $story_id"
    if [[ "$dry_run" == "true" ]]; then
        args="$args --dry-run"
    fi

    if python3 "$USER_STORY_GENERATOR_SCRIPTS/github_sync.py" $args; then
        print_success "Issue updated successfully"
        return 0
    else
        print_error "Failed to update issue"
        return 1
    fi
}

# Function to sync story with GitHub
sync_story() {
    local story_id="$1"
    local dry_run="${2:-false}"

    print_info "Syncing $story_id with GitHub"

    local args="sync $story_id"
    if [[ "$dry_run" == "true" ]]; then
        args="$args --dry-run"
    fi

    if python3 "$USER_STORY_GENERATOR_SCRIPTS/github_sync.py" $args; then
        print_success "Sync completed successfully"
        return 0
    else
        print_error "Sync failed"
        return 1
    fi
}

# Function to process multiple stories
bulk_process() {
    local command="$1"
    local dry_run="$2"
    shift 2
    local story_ids=("$@")

    print_info "Processing ${#story_ids[@]} stories in bulk"

    local args="bulk $command ${story_ids[*]}"
    if [[ "$dry_run" == "true" ]]; then
        args="$args --dry-run"
    fi

    if python3 "$USER_STORY_GENERATOR_SCRIPTS/github_sync.py" $args; then
        print_success "Bulk operation completed"
        return 0
    else
        print_error "Bulk operation failed"
        return 1
    fi
}

# Function to show sync status
show_status() {
    print_info "GitHub Sync Status"
    echo ""

    # Check GitHub authentication
    print_info "Checking GitHub authentication..."
    if check_gh_auth; then
        print_success "GitHub CLI authenticated"

        # Get current repo
        if git rev-parse --git-dir > /dev/null 2>&1; then
            local repo=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "Unknown")
            print_info "Current repository: $repo"
        else
            print_warning "Not in a git repository"
        fi
    else
        print_error "GitHub CLI not authenticated or not installed"
    fi

    echo ""

    # Count stories with GitHub issues
    local STORIES_DIR="$PROJECT_ROOT/stories/yaml-source"

    if [[ -d "$STORIES_DIR" ]]; then
        local total_stories=$(find "$STORIES_DIR" -name "*.yaml" | wc -l | tr -d ' ')
        local synced_stories=$(grep -l "issue_number:" "$STORIES_DIR"/*.yaml 2>/dev/null | wc -l | tr -d ' ')

        print_info "Stories status:"
        echo "  Total stories: $total_stories"
        echo "  Synced with GitHub: $synced_stories"
        echo "  Not synced: $((total_stories - synced_stories))"
    else
        print_warning "Stories directory not found"
    fi
}

# Main script
main() {
    local command=""
    local dry_run=false
    local force=false
    local args=()

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                dry_run=true
                shift
                ;;
            --force)
                force=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            -*)
                print_error "Unknown option: $1"
                usage
                exit 1
                ;;
            *)
                if [[ -z "$command" ]]; then
                    command="$1"
                else
                    args+=("$1")
                fi
                shift
                ;;
        esac
    done

    # Validate command
    if [[ -z "$command" ]]; then
        print_error "Command is required"
        usage
        exit 1
    fi

    # Execute command
    case $command in
        create)
            if [[ ${#args[@]} -ne 1 ]]; then
                print_error "create requires exactly one story ID"
                usage
                exit 1
            fi
            check_gh_auth || exit 1
            create_issue "${args[0]}" "$dry_run"
            ;;
        update)
            if [[ ${#args[@]} -ne 1 ]]; then
                print_error "update requires exactly one story ID"
                usage
                exit 1
            fi
            check_gh_auth || exit 1
            update_issue "${args[0]}" "$dry_run"
            ;;
        sync)
            if [[ ${#args[@]} -ne 1 ]]; then
                print_error "sync requires exactly one story ID"
                usage
                exit 1
            fi
            check_gh_auth || exit 1
            sync_story "${args[0]}" "$dry_run"
            ;;
        bulk)
            if [[ ${#args[@]} -lt 2 ]]; then
                print_error "bulk requires a command and at least one story ID"
                usage
                exit 1
            fi
            check_gh_auth || exit 1
            bulk_command="${args[0]}"
            bulk_story_ids=("${args[@]:1}")
            bulk_process "$bulk_command" "$dry_run" "${bulk_story_ids[@]}"
            ;;
        status)
            show_status
            ;;
        *)
            print_error "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

# Run main if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
