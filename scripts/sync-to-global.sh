#!/bin/bash
# Sync script: Create directory symlinks from global .claude to project directories
# This allows developing in project while commands/agents/skills are available globally

set -e

PROJECT_ROOT="/Users/matteocervelli/dev/projects/llms"
GLOBAL_CLAUDE="$HOME/.claude"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Syncing Project Directories to Global ===${NC}"
echo -e "${BLUE}Project: $PROJECT_ROOT/.claude/${NC}"
echo -e "${BLUE}Global:  $GLOBAL_CLAUDE/${NC}"
echo ""

# Function to sync directory via symlink
sync_directory() {
    local dir_name=$1
    local project_path="$PROJECT_ROOT/.claude/$dir_name"
    local global_path="$GLOBAL_CLAUDE/$dir_name"

    echo -e "${GREEN}Syncing: $dir_name${NC}"

    # Check if project directory exists
    if [ ! -d "$project_path" ]; then
        echo -e "${YELLOW}  ⊘ No project $dir_name directory, skipping${NC}"
        echo ""
        return
    fi

    # Check if global path exists
    if [ -L "$global_path" ]; then
        # Already a symlink
        local current_target=$(readlink "$global_path")
        if [ "$current_target" = "$project_path" ]; then
            echo -e "${GREEN}  ✓ $dir_name already synced${NC}"
        else
            echo -e "${YELLOW}  ↷ $dir_name symlink exists but points elsewhere${NC}"
            echo -e "${YELLOW}    Current: $current_target${NC}"
            echo -e "${YELLOW}    Wanted:  $project_path${NC}"
            echo -e "${RED}  ! Manual intervention required${NC}"
        fi
    elif [ -d "$global_path" ]; then
        # Regular directory exists
        echo -e "${YELLOW}  ! $dir_name exists as regular directory in global${NC}"
        echo -e "${YELLOW}    This will be backed up and replaced with symlink${NC}"

        # Backup the directory
        local backup_path="${global_path}.backup.$(date +%Y%m%d_%H%M%S)"
        mv "$global_path" "$backup_path"
        echo -e "${YELLOW}    Backed up to $backup_path${NC}"

        # Create symlink
        ln -s "$project_path" "$global_path"
        echo -e "${GREEN}  ✓ Created symlink for $dir_name${NC}"
    elif [ -f "$global_path" ]; then
        # Regular file exists (shouldn't happen)
        echo -e "${RED}  ! $dir_name exists as a file in global${NC}"
        echo -e "${RED}  ! Manual intervention required${NC}"
    else
        # Create new symlink
        ln -s "$project_path" "$global_path"
        echo -e "${GREEN}  + Created symlink for $dir_name${NC}"
    fi

    echo ""
}

# Sync each directory
sync_directory "commands"
sync_directory "agents"
sync_directory "skills"
sync_directory "hooks"
sync_directory "prompts"

# Summary
echo -e "${GREEN}=== Sync Complete ===${NC}"
echo -e "${GREEN}✓ Project directories symlinked to global${NC}"
echo -e "${GREEN}✓ Develop in project, changes apply globally${NC}"
echo -e "${GREEN}✓ Files tracked in git${NC}"
echo ""
echo -e "${YELLOW}To verify:${NC}"
echo "  ls -la ~/.claude/"
echo ""
echo -e "${YELLOW}To run this sync again:${NC}"
echo "  ./scripts/sync-to-global.sh"
