# Product Requirements Document (PRD) Template

## PRD-XXXX: {Feature Name}

**Date**: {date}
**Author**: {author}
**Status**: Draft | Review | Approved
**Version**: {version}

---

### 1. Executive Summary

{2-3 paragraphs: what this feature does, why it matters, who benefits}

### 2. Problem Statement

- **Current state**: {what exists today}
- **Pain points**: {what's broken or missing}
- **Impact**: {business/user impact of not solving}

### 3. User Personas

| Persona      | Role   | Primary Goal      | Key Pain Point |
| ------------ | ------ | ----------------- | -------------- |
| {persona_id} | {role} | {goal from story} | {pain point}   |

### 4. User Stories

{Table of all stories in this PRD}

| ID      | Title   | Points   | Persona   | Criteria |
| ------- | ------- | -------- | --------- | -------- |
| US-XXXX | {title} | {points} | {persona} | {count}  |

**Total story points**: {sum}
**Estimated complexity**: {Low/Medium/High}

### 5. Story Map

```
{Epic/Feature}
├── {Story Group 1: Core functionality}
│   ├── US-XXXX: {title} ({points} pts)
│   └── US-XXXX: {title} ({points} pts)
├── {Story Group 2: Supporting features}
│   └── US-XXXX: {title} ({points} pts)
└── {Story Group 3: Polish/edge cases}
    └── US-XXXX: {title} ({points} pts)
```

### 6. Success Metrics

| Metric   | Target   | How to Measure       |
| -------- | -------- | -------------------- |
| {metric} | {target} | {measurement method} |

### 7. Scope

**In scope**: {what's included}
**Out of scope**: {what's explicitly excluded}
**Future considerations**: {what might come later}

### 8. Dependencies

- **Internal**: {other features/teams}
- **External**: {third-party services, APIs}
- **Technical**: {infrastructure, libraries}

### 9. Timeline

| Phase                | Stories          | Points | Target |
| -------------------- | ---------------- | ------ | ------ |
| Phase 1: Foundation  | US-XXXX, US-XXXX | {pts}  | {date} |
| Phase 2: Core        | US-XXXX          | {pts}  | {date} |
| Phase 3: Integration | US-XXXX          | {pts}  | {date} |

### 10. Risks & Mitigations

| Risk   | Probability  | Impact       | Mitigation   |
| ------ | ------------ | ------------ | ------------ |
| {risk} | Low/Med/High | Low/Med/High | {mitigation} |

---

**Next step**: Generate PRPs for each implementation phase using `/story prp`
