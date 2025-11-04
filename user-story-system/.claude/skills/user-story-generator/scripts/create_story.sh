#!/usr/bin/env bash
# create_story.sh - Create a new user story from template

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

# Paths within skill
TEMPLATE_PATH="$SKILL_DIR/templates/story-template.yaml"

# Paths in project root
STORIES_DIR="$PROJECT_ROOT/stories/yaml-source"
COUNTER_FILE="$PROJECT_ROOT/.story_counter"

# Ensure directories exist
mkdir -p "$STORIES_DIR"

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

# Function to get next story ID
get_next_id() {
    local counter=1

    if [[ -f "$COUNTER_FILE" ]]; then
        counter=$(cat "$COUNTER_FILE")
    fi

    echo "$counter"
}

# Function to increment counter
increment_counter() {
    local current=$(get_next_id)
    local next=$((current + 1))
    echo "$next" > "$COUNTER_FILE"
}

# Function to format story ID
format_story_id() {
    local counter=$1
    printf "US-%04d" "$counter"
}

# Function to create story file
create_story() {
    local title="$1"
    local persona="${2:-end_user}"

    # Get next ID
    local counter=$(get_next_id)
    local story_id=$(format_story_id "$counter")
    local story_file="$STORIES_DIR/${story_id}.yaml"

    # Check if file already exists
    if [[ -f "$story_file" ]]; then
        print_error "Story file already exists: $story_file"
        return 1
    fi

    # Check if template exists
    if [[ ! -f "$TEMPLATE_PATH" ]]; then
        print_error "Template not found: $TEMPLATE_PATH"
        return 1
    fi

    # Create story file from template
    print_info "Creating story: $story_id"
    print_info "Title: $title"
    print_info "Persona: $persona"

    # Copy template and update metadata
    cp "$TEMPLATE_PATH" "$story_file"

    # Get current date
    local current_date=$(date +%Y-%m-%d)
    local author="${USER:-unknown}"

    # Update story file with sed (cross-platform compatible)
    # macOS sed requires -i '' for in-place editing
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s|^id: \"\"$|id: \"$story_id\"|" "$story_file"
        sed -i '' "s|^title: \"\"$|title: \"$title\"|" "$story_file"
        sed -i '' "s|^  persona: \"\"$|  persona: \"$persona\"|" "$story_file"
        sed -i '' "s|^  created_date: \"\"$|  created_date: \"$current_date\"|" "$story_file"
        sed -i '' "s|^  updated_date: \"\"$|  updated_date: \"$current_date\"|" "$story_file"
        sed -i '' "s|^  author: \"\"$|  author: \"$author\"|" "$story_file"
    else
        sed -i "s|^id: \"\"$|id: \"$story_id\"|" "$story_file"
        sed -i "s|^title: \"\"$|title: \"$title\"|" "$story_file"
        sed -i "s|^  persona: \"\"$|  persona: \"$persona\"|" "$story_file"
        sed -i "s|^  created_date: \"\"$|  created_date: \"$current_date\"|" "$story_file"
        sed -i "s|^  updated_date: \"\"$|  updated_date: \"$current_date\"|" "$story_file"
        sed -i "s|^  author: \"\"$|  author: \"$author\"|" "$story_file"
    fi

    # Increment counter
    increment_counter

    print_success "Created story file: $story_file"
    print_info "Story ID: $story_id"
    print_info "Next available ID: $(format_story_id $(get_next_id))"

    # Generate markdown
    if command -v python3 &> /dev/null; then
        print_info "Generating Markdown documentation..."
        if python3 "$SCRIPT_DIR/generate_story_from_yaml.py" --story-id "$story_id"; then
            print_success "Markdown generated successfully"
        else
            print_warning "Failed to generate Markdown (you can generate it later)"
        fi
    else
        print_warning "python3 not found, skipping Markdown generation"
    fi

    echo ""
    print_info "Edit the story file to add details:"
    echo "  $story_file"
    echo ""
    print_info "Generate Markdown after editing:"
    echo "  python3 $SCRIPT_DIR/generate_story_from_yaml.py --story-id $story_id"

    return 0
}

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] <title>

Create a new user story from template.

Arguments:
    title               Story title (required)

Options:
    -p, --persona       Persona ID (default: end_user)
    -h, --help          Show this help message

Example:
    $0 "Add user authentication"
    $0 --persona ceo "Dashboard analytics view"

EOF
}

# Main script
main() {
    local title=""
    local persona="end_user"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--persona)
                persona="$2"
                shift 2
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
                if [[ -z "$title" ]]; then
                    title="$1"
                else
                    print_error "Multiple titles provided. Use quotes for multi-word titles."
                    usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$title" ]]; then
        print_error "Title is required"
        usage
        exit 1
    fi

    # Create story
    if create_story "$title" "$persona"; then
        exit 0
    else
        exit 1
    fi
}

# Run main if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
