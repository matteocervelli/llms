# User Story System Skills

This directory contains 5 specialized skills for the User Story Workflow System.

## Skills Overview

### 1. user-story-generator (Orchestrator)
**Type**: Orchestrator  
**File**: `user-story-generator/SKILL.md`  
**Lines**: 706  
**Purpose**: Main workflow for creating user stories from feature descriptions

**Key Features**:
- Interactive feature extraction with Q&A
- Intelligent story decomposition (2-8 stories)
- Automated INVEST validation
- Technical annotation coordination
- YAML and Markdown generation
- Optional GitHub integration

**Activation**: "Create user stories for [feature description]"

---

### 2. story-validator (Specialist)
**Type**: Specialist  
**File**: `story-validator/SKILL.md`  
**Lines**: 671  
**Purpose**: Validate stories against INVEST criteria and suggest improvements

**Key Features**:
- Single story or bulk validation
- INVEST criteria scoring (0-100)
- Specific issue identification
- Auto-fix suggestions
- Batch processing support

**Activation**: "Validate US-0001" or "Check story quality"

---

### 3. technical-annotator (Specialist)
**Type**: Specialist  
**File**: `technical-annotator/SKILL.md`  
**Lines**: 750  
**Purpose**: Add technical context and implementation guidance to stories

**Key Features**:
- Technology stack identification
- Specific implementation hints
- Component impact analysis
- Effort estimation (hours/days)
- Complexity assessment
- Risk identification

**Activation**: "Add technical notes to US-0001"

---

### 4. dependency-analyzer (Specialist)
**Type**: Specialist  
**File**: `dependency-analyzer/SKILL.md`  
**Lines**: 863  
**Purpose**: Analyze story dependencies and generate visual graphs

**Key Features**:
- Dependency graph building
- Circular dependency detection
- Blocking chain identification
- Independent story finding
- Bottleneck identification
- Mermaid diagram generation

**Activation**: "Check dependencies" or "Show dependency graph"

---

### 5. sprint-planner (Specialist)
**Type**: Specialist  
**File**: `sprint-planner/SKILL.md`  
**Lines**: 835  
**Purpose**: Plan sprints with capacity management and dependency checking

**Key Features**:
- Capacity-based story selection
- Dependency readiness checking
- Priority-based sorting
- Sprint plan validation
- Story status updates
- GitHub milestone integration

**Activation**: "Plan sprint with 40 story points"

---

## Skill Relationships

```
user-story-generator (Orchestrator)
    ├── Invokes → qa-validator-agent
    ├── Invokes → technical-annotator-agent
    └── Creates stories for other skills

story-validator (Specialist)
    └── Used by → user-story-generator
    └── Used independently

technical-annotator (Specialist)
    └── Used by → user-story-generator
    └── Used independently

dependency-analyzer (Specialist)
    └── Used before → sprint-planner
    └── Used independently

sprint-planner (Specialist)
    └── Uses data from → dependency-analyzer
    └── Used independently
```

## Integration with System Components

### Scripts Integration
All skills integrate with Python scripts in `/scripts/`:
- `validate_story_invest.py` - INVEST validation
- `generate_story_from_yaml.py` - Markdown generation
- `check_dependencies.py` - Dependency analysis
- `github_sync.py` - GitHub integration

### Agent Integration
Skills coordinate with agents in `.claude/agents/`:
- `qa-validator-agent` - Silent validation
- `technical-annotator-agent` - Silent annotation
- `story-orchestrator-agent` - Main workflow

### Configuration
All skills use `config/automation-config.yaml` for:
- File paths
- Validation rules
- Sprint defaults
- GitHub settings

## Usage Patterns

### Pattern 1: Create New Stories
```
1. user-story-generator skill
   → Extracts feature, generates stories
   → Automatically validates (story-validator)
   → Automatically annotates (technical-annotator)
   → Creates files and GitHub issues
```

### Pattern 2: Validate Existing Stories
```
1. story-validator skill
   → Validates single or bulk stories
   → Suggests fixes
   → Optionally applies auto-fixes
```

### Pattern 3: Plan Sprint
```
1. dependency-analyzer skill
   → Analyzes all dependencies
   → Identifies blockers and bottlenecks

2. sprint-planner skill
   → Selects stories based on capacity
   → Checks dependencies are satisfied
   → Updates story status
   → Creates GitHub milestone
```

## File Sizes and Complexity

| Skill | Lines | Size | Complexity |
|-------|-------|------|------------|
| user-story-generator | 706 | 20 KB | High (orchestrator) |
| story-validator | 671 | 19 KB | Medium |
| technical-annotator | 750 | 21 KB | Medium |
| dependency-analyzer | 863 | 27 KB | High |
| sprint-planner | 835 | 24 KB | High |
| **Total** | **3,825** | **111 KB** | - |

## Next Phase

Phase 6 will create slash commands that invoke these skills:
- `/user-story-new` → user-story-generator
- `/user-story-validate` → story-validator
- `/user-story-annotate` → technical-annotator
- `/user-story-deps` → dependency-analyzer
- `/user-story-sprint` → sprint-planner

---

**Status**: Phase 5 Complete ✅  
**Created**: 2025-01-03  
**Location**: `/Users/matteocervelli/dev/projects/llms/user-story-system/.claude/skills/`
