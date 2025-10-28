#!/bin/bash
# Watch script: Automatically sync changes to global as you develop

PROJECT_ROOT="/Users/matteocervelli/dev/projects/llms"
CLAUDE_DIR="$PROJECT_ROOT/.claude"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Watching for changes in .claude/ ===${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Check if fswatch is installed
if ! command -v fswatch &> /dev/null; then
    echo -e "${YELLOW}fswatch not found. Installing via homebrew...${NC}"
    brew install fswatch
fi

# Run initial copy
"$PROJECT_ROOT/scripts/copy-to-global.sh"

echo ""
echo -e "${GREEN}Now watching for changes...${NC}"
echo ""

# Watch for changes and copy
fswatch -o "$CLAUDE_DIR" | while read f; do
    echo -e "${YELLOW}[$(date +%H:%M:%S)] Change detected, copying...${NC}"
    "$PROJECT_ROOT/scripts/copy-to-global.sh" --quiet
    echo -e "${GREEN}[$(date +%H:%M:%S)] Copied to global${NC}"
    echo ""
done
