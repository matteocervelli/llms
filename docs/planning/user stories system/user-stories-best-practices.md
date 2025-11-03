# User Stories: Design & Structure Best Practices

## Storage Schema

**Recommended YAML structure:**

```yaml
story_id: US-001
title: "Client views constraint priority matrix"
type: feature | enhancement | bug | spike

user:
  persona: "CEO consulting client"
  role: "decision_maker"
  
story:
  as_a: "CEO consulting client"
  i_want: "see my constraint analysis in a visual priority matrix"
  so_that: "I can quickly identify which bottlenecks to address first"

acceptance_criteria:
  - id: AC-001
    given: "I've completed the assessment"
    when: "I view results"
    then: "constraints are plotted by impact vs. effort"
    
  - id: AC-002
    given: "viewing the matrix"
    when: "I filter by category"
    then: "only selected categories display"

metadata:
  epic: "EP-001: Diagnostic Dashboard"
  priority: high | medium | low
  story_points: 5
  sprint: 2025-Q1-Sprint-3
  status: backlog | in_progress | review | done
  
dependencies:
  blocks: [US-003]
  blocked_by: [US-002]
  related: [US-004, US-005]

technical_notes: "Consider using D3.js for matrix visualization"
```

## Visual Representations

### 1. Story Map (Horizontal)

```
Epics:        │ Onboarding  │ Assessment  │ Results     │ Actions
──────────────┼─────────────┼─────────────┼─────────────┼────────────
User Journey: │ → Register  │ → Complete  │ → View      │ → Export
              │   Login     │   Questions │   Dashboard │   Share
              │   Setup     │   Save      │   Filters   │   Track
                    │             │            │            │
Release 1     │    ●●●           ●●          ●            
Release 2     │                  ●           ●●●          ●●
Release 3     │                              ●            ●●●
```

**Purpose:** Shows user journey horizontally with stories organized by epic and release priority.

### 2. Dependency Graph (Vertical)

```
EP-001: Diagnostic Dashboard
    │
    ├─ US-001: User authentication
    │   │
    │   └─ US-002: Session management
    │       │
    │       ├─ US-003: Dashboard access
    │       └─ US-004: Profile management
    │
    └─ US-005: Assessment module
        │
        ├─ US-006: Question flow
        └─ US-007: Progress tracking
```

**Purpose:** Visualizes blocking dependencies and build sequence.

### 3. Impact/Effort Matrix

```
High Impact │ 
           │  ●US-003      ●US-001
           │               
           │  ●US-007
           │         ●US-005  ●US-002
           │  
Low Impact │      ●US-006        ●US-004
           └─────────────────────────────
             Low Effort    High Effort
```

**Purpose:** Prioritization tool showing ROI of each story.

## File Organization

**Recommended directory structure:**

```
/product
  /epics
    EP-001-diagnostic-dashboard.md
    EP-002-scalability-assessment.md
  /stories
    /backlog
      US-001-auth.md
      US-002-session.md
    /sprint-2025-q1-01
      US-003-dashboard.md
    /sprint-2025-q1-02
      US-005-assessment.md
    /done
      US-004-profile.md
  /templates
    story-template.md
    acceptance-criteria-template.md
  /assets
    /wireframes
    /mockups
```

**Benefits:**
- Version controlled (Git)
- Searchable
- Sprint-organized
- Template consistency

## Story Document Template

```markdown
# US-001: Client Secure Login

**Epic:** [EP-001: Diagnostic Dashboard](../epics/EP-001-diagnostic-dashboard.md)
**Status:** In Progress | **Sprint:** 2025-Q1-Sprint-3 | **Points:** 5

## Story
As a **CEO consulting client**,
I want to **log in securely with my existing Google account**,
So that **I can access my diagnostic dashboard without managing another password**.

## Acceptance Criteria
- [ ] **AC-001:** Given I'm on login page, When I click "Continue with Google", Then I'm authenticated and redirected to dashboard
- [ ] **AC-002:** Given successful login, When I close browser, Then my session persists for 30 days
- [ ] **AC-003:** Given expired session, When I return, Then I'm prompted to re-authenticate

## Dependencies
- **Blocks:** [US-003: Dashboard Access](US-003-dashboard.md)
- **Blocked By:** None
- **Related:** [US-002: Session Management](US-002-session.md)

## Design Assets
- [Wireframe: Login Flow](../assets/wireframes/login-flow.png)
- [Mockup: OAuth Screen](../assets/mockups/oauth-google.png)

## Technical Notes
- Use OAuth2 with Google Provider
- Store refresh tokens encrypted in PostgreSQL
- Implement session middleware with Redis
- Consider rate limiting for security

## Definition of Done
- [ ] All acceptance criteria pass
- [ ] Unit tests >80% coverage
- [ ] Integration tests for OAuth flow
- [ ] Security review completed
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Product owner approval

## Discussion & Updates

### 2025-01-20
Discussed session timeout with team. Changed from 7 days to 30 days based on user feedback.

### 2025-01-18
Security review flagged refresh token storage. Updated to use encryption at rest.

---
**Created:** 2025-01-15 | **Last Updated:** 2025-01-20 | **Author:** Matteo
```

## Epic Template

```markdown
# EP-001: Diagnostic Dashboard

**Status:** In Progress | **Target:** Q1 2025

## Vision
Enable consulting clients to access, visualize, and act on their ScalabilityScore diagnostic results through an intuitive, secure dashboard.

## Business Value
- Reduces manual report delivery time by 80%
- Enables self-service access to insights
- Increases client engagement with methodology
- Creates foundation for SaaS product

## Success Metrics
- 90% of clients access dashboard within 7 days
- Average session time >5 minutes
- NPS score >50 for dashboard experience

## User Stories
- [x] [US-004: Profile Management](../stories/done/US-004-profile.md) - Done
- [ ] [US-001: Secure Login](../stories/sprint-2025-q1-03/US-001-auth.md) - In Progress
- [ ] [US-002: Session Management](../stories/backlog/US-002-session.md) - Backlog
- [ ] [US-003: Dashboard Access](../stories/backlog/US-003-dashboard.md) - Blocked by US-001

## Dependencies
- Authentication service (Supabase/Auth0)
- Data visualization library (D3.js/Recharts)
- Backend API for assessment data

## Design Assets
- [User Flow](../assets/flows/diagnostic-dashboard-flow.pdf)
- [Design System](../assets/design-system.md)

---
**Created:** 2025-01-10 | **Owner:** Matteo
```

## Database Schema (for tracking)

**If using structured storage:**

```sql
-- Epics
CREATE TABLE epics (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  status TEXT,
  target_quarter TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Stories
CREATE TABLE stories (
  id TEXT PRIMARY KEY,
  epic_id TEXT REFERENCES epics(id),
  title TEXT NOT NULL,
  type TEXT CHECK (type IN ('feature', 'enhancement', 'bug', 'spike')),
  persona TEXT,
  as_a TEXT,
  i_want TEXT,
  so_that TEXT,
  priority TEXT CHECK (priority IN ('high', 'medium', 'low')),
  story_points INTEGER,
  sprint TEXT,
  status TEXT CHECK (status IN ('backlog', 'in_progress', 'review', 'done')),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Acceptance Criteria
CREATE TABLE acceptance_criteria (
  id TEXT PRIMARY KEY,
  story_id TEXT REFERENCES stories(id),
  given_context TEXT,
  when_action TEXT,
  then_outcome TEXT,
  completed BOOLEAN DEFAULT FALSE
);

-- Dependencies
CREATE TABLE story_dependencies (
  story_id TEXT REFERENCES stories(id),
  depends_on_id TEXT REFERENCES stories(id),
  relationship TEXT CHECK (relationship IN ('blocks', 'blocked_by', 'related')),
  PRIMARY KEY (story_id, depends_on_id)
);
```

## Collaborative Tools

**For solo → small team:**

| Need | Tool | Why |
|------|------|-----|
| **Storage** | GitHub Issues/Projects or Linear | Version control, structured, searchable |
| **Visualization** | Miro/FigJam | Story mapping, dependency graphs |
| **Documentation** | Markdown in repo | Diffable, version controlled, no vendor lock-in |
| **Tracking** | Kanban board (GitHub Projects) | Simple, visual, integrated |

## Automation Opportunities (n8n/Python)

**Scripts to build:**

1. **Story Generator:** YAML → Markdown conversion
2. **Dependency Checker:** Validates no circular dependencies
3. **Story Map Generator:** Creates visual story map from YAML
4. **Sprint Report:** Generates burndown and velocity charts
5. **Definition of Done Checker:** Ensures all checkboxes completed before merging

**Example Python script:**

```python
import yaml
from pathlib import Path

def generate_story_markdown(yaml_file):
    with open(yaml_file) as f:
        story = yaml.safe_load(f)
    
    md = f"""# {story['story_id']}: {story['title']}

**Epic:** {story['metadata']['epic']}
**Status:** {story['metadata']['status']} | **Sprint:** {story['metadata']['sprint']} | **Points:** {story['metadata']['story_points']}

## Story
As a **{story['story']['as_a']}**,
I want to **{story['story']['i_want']}**,
So that **{story['story']['so_that']}**.

## Acceptance Criteria
"""
    
    for ac in story['acceptance_criteria']:
        md += f"- [ ] **{ac['id']}:** Given {ac['given']}, When {ac['when']}, Then {ac['then']}\n"
    
    return md

# Usage
Path('stories/US-001.md').write_text(
    generate_story_markdown('stories/US-001.yaml')
)
```

## Key Improvements to Your Workflow

### Add to Your Current Process:

1. **Story IDs** - Essential for tracking and referencing
2. **Dependency tracking** - Prevents blocking issues
3. **Design asset links** - Bridges UX and development
4. **Definition of Done** - Prevents scope creep
5. **Metadata tracking** - Enables velocity and reporting
6. **Epic organization** - Groups related stories
7. **Version history** - Track changes over time

### Quality Checklist Before Story is "Ready"

- [ ] Story ID assigned
- [ ] Follows INVEST criteria
- [ ] All acceptance criteria in Given/When/Then format
- [ ] Dependencies identified
- [ ] Story points estimated
- [ ] Epic assigned
- [ ] Linked to design assets (if applicable)
- [ ] Technical notes added (if applicable)
- [ ] Definition of Done defined

## Workflow Integration

**When creating new stories:**

1. Start with epic (if new feature area)
2. Create story YAML file with complete metadata
3. Generate markdown from YAML
4. Add to sprint board
5. Link design assets
6. Review dependencies
7. Estimate points with team (if applicable)

**During sprint:**

1. Move to "In Progress" when starting
2. Check off acceptance criteria as completed
3. Update technical notes with learnings
4. Add discussion updates to story document
5. Move to "Done" when Definition of Done met

## For Levero Specifically

**Recommended setup:**

```
/levero-product
  /epics
    EP-001-scalability-score.md
    EP-002-diagnostic-dashboard.md
    EP-003-quarter-sprint-planner.md
  /stories
    /yaml-source
      US-001-auth.yaml
      US-002-assessment.yaml
    /generated-docs
      US-001-auth.md
      US-002-assessment.md
  /scripts
    generate-stories.py
    check-dependencies.py
    story-map-generator.py
  /assets
    /wireframes
    /mockups
  story-template.yaml
  README.md
```

**Benefits for your context:**
- Version controlled in Git
- Automated with Python/n8n
- No dependency on external tools
- Scales from solo to team
- Integration-ready with development workflow

---

This structure gives you the foundation to systematically design, track, and communicate user stories from initial concept through delivery.
