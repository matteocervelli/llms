#!/usr/bin/env bash
# deploy-global.sh - Deploy user story system globally

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SYSTEM_DIR="/Users/matteocervelli/dev/projects/llms/user-story-system"
GLOBAL_CLAUDE="$HOME/.claude"

echo -e "${BLUE}🚀 Deploying User Story System globally...${NC}"
echo ""

# Create directories
echo -e "${BLUE}📁 Creating global directories...${NC}"
mkdir -p "$GLOBAL_CLAUDE/skills"
mkdir -p "$GLOBAL_CLAUDE/commands"
mkdir -p "$GLOBAL_CLAUDE/agents"
echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# Symlink skills
echo -e "${BLUE}🔗 Symlinking skills...${NC}"
skills=("user-story-generator" "story-validator" "technical-annotator" "dependency-analyzer" "sprint-planner")
for skill in "${skills[@]}"; do
    # Remove existing symlink if it exists
    rm -f "$GLOBAL_CLAUDE/skills/$skill"
    # Create new symlink
    ln -sf "$SYSTEM_DIR/.claude/skills/$skill" "$GLOBAL_CLAUDE/skills/$skill"
    echo -e "  ${GREEN}✅${NC} $skill"
done
echo ""

# Symlink commands
echo -e "${BLUE}🔗 Symlinking commands...${NC}"
commands=("user-story-new" "user-story-refine" "user-story-annotate" "user-story-deps" "user-story-sprint")
for cmd in "${commands[@]}"; do
    # Remove existing symlink if it exists
    rm -f "$GLOBAL_CLAUDE/commands/$cmd.md"
    # Create new symlink
    ln -sf "$SYSTEM_DIR/.claude/commands/$cmd.md" "$GLOBAL_CLAUDE/commands/$cmd.md"
    echo -e "  ${GREEN}✅${NC} $cmd"
done
echo ""

# Symlink agents
echo -e "${BLUE}🔗 Symlinking agents...${NC}"
agents=("qa-validator-agent" "technical-annotator-agent" "story-orchestrator-agent")
for agent in "${agents[@]}"; do
    # Remove existing symlink if it exists
    rm -f "$GLOBAL_CLAUDE/agents/$agent.md"
    # Create new symlink
    ln -sf "$SYSTEM_DIR/.claude/agents/$agent.md" "$GLOBAL_CLAUDE/agents/$agent.md"
    echo -e "  ${GREEN}✅${NC} $agent"
done
echo ""

# Verification
echo -e "${YELLOW}📋 Verifying deployment...${NC}"
skill_count=$(ls -1 "$GLOBAL_CLAUDE/skills/" 2>/dev/null | grep -E "user-story|story-|dependency|sprint" | wc -l | tr -d ' ')
command_count=$(ls -1 "$GLOBAL_CLAUDE/commands/" 2>/dev/null | grep "user-story" | wc -l | tr -d ' ')
agent_count=$(ls -1 "$GLOBAL_CLAUDE/agents/" 2>/dev/null | grep -E "(validator|annotator|orchestrator)" | wc -l | tr -d ' ')

echo "  Skills: $skill_count symlinks"
echo "  Commands: $command_count symlinks"
echo "  Agents: $agent_count symlinks"
echo ""

if [ "$skill_count" -eq 5 ] && [ "$command_count" -eq 5 ] && [ "$agent_count" -eq 3 ]; then
    echo -e "${GREEN}✅ Deployment complete!${NC}"
else
    echo -e "${YELLOW}⚠️  Warning: Some symlinks may be missing${NC}"
    echo "  Expected: 5 skills, 5 commands, 3 agents"
    echo "  Found: $skill_count skills, $command_count commands, $agent_count agents"
fi

echo ""
echo -e "${BLUE}🎯 Test it:${NC}"
echo "  cd ~/any-project"
echo "  /user-story-new"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "  $SYSTEM_DIR/docs/DEPLOYMENT-GUIDE.md"
