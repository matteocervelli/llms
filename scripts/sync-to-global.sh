#!/bin/bash
# Sync script: Create symlinks from global .claude to project files
# This allows developing in project while commands are available globally

set -e

PROJECT_ROOT="/Users/matteocervelli/dev/projects/llms"
GLOBAL_CLAUDE="$HOME/.claude"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Syncing Project Commands to Global ===${NC}"
echo -e "${BLUE}Project: $PROJECT_ROOT/.claude/${NC}"
echo -e "${BLUE}Global:  $GLOBAL_CLAUDE/${NC}"
echo ""

# Function to sync directory
sync_directory() {
    local dir_name=$1
    local project_path="$PROJECT_ROOT/.claude/$dir_name"
    local global_path="$GLOBAL_CLAUDE/$dir_name"

    echo -e "${GREEN}Syncing: $dir_name${NC}"

    # Check if project directory exists
    if [ ! -d "$project_path" ]; then
        echo -e "${YELLOW}  ⊘ No project $dir_name directory, skipping${NC}"
        return
    fi

    # Create global directory if it doesn't exist
    mkdir -p "$global_path"

    # Get list of files
    local files=$(find "$project_path" -maxdepth 1 -type f -name "*.md")

    if [ -z "$files" ]; then
        echo -e "${YELLOW}  ⊘ No .md files in $project_path${NC}"
        return
    fi

    # Process each file
    for file in $files; do
        local filename=$(basename "$file")
        local global_file="$global_path/$filename"
        local project_file="$project_path/$filename"

        # Check if global file exists
        if [ -L "$global_file" ]; then
            # Already a symlink
            local current_target=$(readlink "$global_file")
            if [ "$current_target" = "$project_file" ]; then
                echo -e "${GREEN}  ✓ $filename already synced${NC}"
            else
                echo -e "${YELLOW}  ↷ $filename symlink exists but points elsewhere${NC}"
                echo -e "${YELLOW}    Current: $current_target${NC}"
                echo -e "${YELLOW}    Wanted:  $project_file${NC}"
                read -p "    Update symlink? (y/N) " -n 1 -r
                echo ""
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm "$global_file"
                    ln -s "$project_file" "$global_file"
                    echo -e "${GREEN}    ✓ Updated${NC}"
                fi
            fi
        elif [ -f "$global_file" ]; then
            # Regular file exists
            echo -e "${YELLOW}  ! $filename exists as regular file in global${NC}"
            read -p "    Replace with symlink? (y/N) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # Backup the file
                cp "$global_file" "$global_file.backup"
                echo -e "${YELLOW}    Backed up to $global_file.backup${NC}"
                rm "$global_file"
                ln -s "$project_file" "$global_file"
                echo -e "${GREEN}    ✓ Replaced with symlink${NC}"
            fi
        else
            # Create new symlink
            ln -s "$project_file" "$global_file"
            echo -e "${GREEN}  + Created symlink for $filename${NC}"
        fi
    done

    echo ""
}

# Sync each directory
sync_directory "commands"
sync_directory "agents"
sync_directory "skills"
sync_directory "prompts"

# Summary
echo -e "${GREEN}=== Sync Complete ===${NC}"
echo -e "${GREEN}✓ Project files symlinked to global${NC}"
echo -e "${GREEN}✓ Develop in project, changes apply globally${NC}"
echo -e "${GREEN}✓ Files tracked in git${NC}"
echo ""
echo -e "${YELLOW}To verify:${NC}"
echo "  ls -la ~/.claude/commands/"
echo ""
echo -e "${YELLOW}To run this sync again:${NC}"
echo "  ./scripts/sync-to-global.sh"
