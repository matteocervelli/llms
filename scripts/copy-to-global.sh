#!/bin/bash
# Copy script: Copy project .claude files to global ~/.claude
# This creates real file copies (not symlinks) for better compatibility

set -e

PROJECT_ROOT="/Users/matteocervelli/dev/projects/llms"
GLOBAL_CLAUDE="$HOME/.claude"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Quiet mode flag
QUIET=false
if [ "$1" = "--quiet" ]; then
    QUIET=true
fi

[ "$QUIET" = false ] && echo -e "${GREEN}=== Copying Project Commands to Global ===${NC}"

# Function to copy directory
copy_directory() {
    local dir_name=$1
    local project_path="$PROJECT_ROOT/.claude/$dir_name"
    local global_path="$GLOBAL_CLAUDE/$dir_name"

    [ "$QUIET" = false ] && echo -e "${BLUE}Copying: $dir_name${NC}"

    # Check if project directory exists
    if [ ! -d "$project_path" ]; then
        [ "$QUIET" = false ] && echo -e "${YELLOW}  ⊘ No project $dir_name directory${NC}"
        return
    fi

    # Create global directory if it doesn't exist
    mkdir -p "$global_path"

    # Get list of files
    local files=$(find "$project_path" -maxdepth 1 -type f -name "*.md" 2>/dev/null || true)

    if [ -z "$files" ]; then
        [ "$QUIET" = false ] && echo -e "${YELLOW}  ⊘ No .md files${NC}"
        return
    fi

    local count=0
    # Copy each file
    for file in $files; do
        local filename=$(basename "$file")
        local global_file="$global_path/$filename"

        # Always copy (overwrite if exists)
        cp "$file" "$global_file"
        count=$((count + 1))
    done

    [ "$QUIET" = false ] && echo -e "${GREEN}  ✓ Copied $count files${NC}"
}

# Copy each directory
copy_directory "commands"
copy_directory "agents"
copy_directory "skills"
copy_directory "prompts"

[ "$QUIET" = false ] && echo -e "${GREEN}✓ Sync complete${NC}"
