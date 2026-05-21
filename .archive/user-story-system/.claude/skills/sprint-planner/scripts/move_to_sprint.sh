#!/usr/bin/env bash
# move_to_sprint.sh - Move user stories to a sprint

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

# Paths in project root
STORIES_DIR="$PROJECT_ROOT/stories/yaml-source"
GENERATED_DOCS_DIR="$PROJECT_ROOT/stories/generated-docs"

# Path to user-story-generator scripts (sibling skill)
USER_STORY_GENERATOR_SCRIPTS="$(dirname "$SKILL_DIR")/user-story-generator/scripts"

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

# Function to update story YAML with sprint and status
update_story_yaml() {
    local story_file="$1"
    local sprint="$2"
    local status="${3:-ready}"

    if [[ ! -f "$story_file" ]]; then
        print_error "Story file not found: $story_file"
        return 1
    fi

    # Get current date
    local current_date=$(date +%Y-%m-%d)

    # Create backup
    cp "$story_file" "${story_file}.bak"

    # Update sprint and status
    # macOS sed requires -i '' for in-place editing
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^  sprint: .*$|  sprint: \"$sprint\"|" "$story_file"
        sed -i '' "s|^  status: .*$|  status: \"$status\"|" "$story_file"
        sed -i '' "s|^  updated_date: .*$|  updated_date: \"$current_date\"|" "$story_file"
    else
        sed -i "s|^  sprint: .*$|  sprint: \"$sprint\"|" "$story_file"
        sed -i "s|^  status: .*$|  status: \"$status\"|" "$story_file"
        sed -i "s|^  updated_date: .*$|  updated_date: \"$current_date\"|" "$story_file"
    fi

    # Remove backup if successful
    rm -f "${story_file}.bak"

    return 0
}

# Function to regenerate markdown
regenerate_markdown() {
    local story_id="$1"

    if command -v python3 &> /dev/null; then
        print_info "Regenerating Markdown for $story_id..."
        if python3 "$USER_STORY_GENERATOR_SCRIPTS/generate_story_from_yaml.py" --story-id "$story_id"; then
            print_success "Markdown regenerated"
            return 0
        else
            print_warning "Failed to regenerate Markdown"
            return 1
        fi
    else
        print_warning "python3 not found, skipping Markdown regeneration"
        return 1
    fi
}

# Function to move story to sprint
move_to_sprint() {
    local story_id="$1"
    local sprint="$2"
    local status="${3:-ready}"

    local story_file="$STORIES_DIR/${story_id}.yaml"

    # Check if story exists
    if [[ ! -f "$story_file" ]]; then
        print_error "Story not found: $story_id"
        return 1
    fi

    print_info "Moving $story_id to $sprint with status '$status'"

    # Update YAML
    if ! update_story_yaml "$story_file" "$sprint" "$status"; then
        print_error "Failed to update story file"
        return 1
    fi

    # Regenerate markdown
    regenerate_markdown "$story_id"

    print_success "Story $story_id moved to $sprint"

    return 0
}

# Function to move multiple stories
move_multiple() {
    local sprint="$1"
    local status="$2"
    shift 2
    local story_ids=("$@")

    local success_count=0
    local fail_count=0

    for story_id in "${story_ids[@]}"; do
        if move_to_sprint "$story_id" "$sprint" "$status"; then
            ((success_count++))
        else
            ((fail_count++))
        fi
    done

    echo ""
    print_info "Results:"
    print_success "  Successfully moved: $success_count"
    if [[ $fail_count -gt 0 ]]; then
        print_error "  Failed: $fail_count"
    fi

    return $([[ $fail_count -eq 0 ]] && echo 0 || echo 1)
}

# Function to list stories by status
list_by_status() {
    local status="$1"

    print_info "Stories with status: $status"
    echo ""

    local found=0
    for story_file in "$STORIES_DIR"/*.yaml; do
        if [[ -f "$story_file" ]]; then
            # Extract status from YAML (simple grep approach)
            local file_status=$(grep "^  status:" "$story_file" | sed 's/.*status: "\(.*\)"/\1/' | tr -d '"')
            if [[ "$file_status" == "$status" ]]; then
                local story_id=$(basename "$story_file" .yaml)
                local title=$(grep "^title:" "$story_file" | sed 's/title: "\(.*\)"/\1/' | tr -d '"')
                echo "  - $story_id: $title"
                ((found++))
            fi
        fi
    done

    if [[ $found -eq 0 ]]; then
        print_warning "No stories found with status: $status"
    else
        echo ""
        print_info "Total: $found stories"
    fi
}

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] <sprint> <story-ids...>

Move user stories to a sprint.

Arguments:
    sprint              Sprint identifier (e.g., "Sprint 1", "2025-W01")
    story-ids           One or more story IDs (e.g., US-0001 US-0002)

Options:
    -s, --status        Story status after move (default: ready)
                        Options: draft, backlog, ready, in_progress, blocked, in_review, done
    -l, --list          List stories by status (requires --status)
    -h, --help          Show this help message

Examples:
    # Move single story
    $0 "Sprint 1" US-0001

    # Move multiple stories
    $0 "Sprint 1" US-0001 US-0002 US-0003

    # Move with custom status
    $0 --status in_progress "Sprint 1" US-0001

    # List backlog stories
    $0 --list --status backlog

EOF
}

# Main script
main() {
    local sprint=""
    local status="ready"
    local list_mode=false
    local story_ids=()

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -s|--status)
                status="$2"
                shift 2
                ;;
            -l|--list)
                list_mode=true
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
                if [[ -z "$sprint" ]] && [[ "$list_mode" == false ]]; then
                    sprint="$1"
                else
                    story_ids+=("$1")
                fi
                shift
                ;;
        esac
    done

    # List mode
    if [[ "$list_mode" == true ]]; then
        list_by_status "$status"
        exit 0
    fi

    # Validate required arguments
    if [[ -z "$sprint" ]]; then
        print_error "Sprint identifier is required"
        usage
        exit 1
    fi

    if [[ ${#story_ids[@]} -eq 0 ]]; then
        print_error "At least one story ID is required"
        usage
        exit 1
    fi

    # Validate status
    valid_statuses=("draft" "backlog" "ready" "in_progress" "blocked" "in_review" "done" "discarded")
    if [[ ! " ${valid_statuses[@]} " =~ " ${status} " ]]; then
        print_error "Invalid status: $status"
        print_info "Valid statuses: ${valid_statuses[*]}"
        exit 1
    fi

    # Move stories
    if move_multiple "$sprint" "$status" "${story_ids[@]}"; then
        exit 0
    else
        exit 1
    fi
}

# Run main if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
