# Doc Review Prompt Template

## Variables

- `$FILE_PATH` — path to the document (required)
- `$FILENAME` — basename of the file
- `$DOC_TYPE` — PRP, PRD, RFC, or DESIGN
- `$TYPE_LABEL` — human-readable type name
- `$CRITERIA` — type-specific review criteria (see below)
- `$DOC_CONTENT` — full document content

## Type Detection

If `--type` is not specified, auto-detect from filename:

```bash
case "$FILENAME" in
  *prp* | *PRP*)       DOC_TYPE="PRP" ;;
  *prd* | *PRD*)       DOC_TYPE="PRD" ;;
  *rfc* | *RFC*)       DOC_TYPE="RFC" ;;
  *design* | *arch*)   DOC_TYPE="DESIGN" ;;
  *)                   DOC_TYPE="DESIGN" ;;
esac
```

## Type-Specific Criteria

### PRP (Product Requirements Prompt)

1. **Requirements Completeness** — Are functional and non-functional requirements clearly stated? Any gaps?
2. **Acceptance Criteria** — Is each requirement testable? Are success/failure conditions defined?
3. **API Contracts** — Are request/response formats, error codes, and edge cases specified?
4. **Testing Strategy** — Unit, integration, e2e coverage planned? Performance benchmarks defined?
5. **Dependencies** — External services, libraries, data sources identified? Risks assessed?
6. **Scope Boundaries** — Is it clear what's in and out of scope? Any ambiguity?

### PRD (Product Requirements Document)

1. **Problem Definition** — Is the problem clearly stated? Evidence of user need?
2. **User Stories** — Are personas and use cases well-defined? Acceptance criteria per story?
3. **Success Metrics** — Are KPIs measurable and time-bound? Baseline vs target defined?
4. **Scope & Prioritization** — Is scope realistic? Are features prioritized (must/should/could)?
5. **Risks & Mitigations** — Technical, business, and timeline risks identified?
6. **Dependencies** — Cross-team, external vendor, or timeline dependencies called out?

### RFC (Request for Comments)

1. **Technical Soundness** — Is the proposed approach technically correct? Any flawed assumptions?
2. **Alternatives Analysis** — Are alternatives listed with honest pros/cons? Why was this approach chosen?
3. **Risks & Failure Modes** — What can go wrong? Are failure scenarios addressed?
4. **Migration Path** — How do we get from current state to proposed state? Breaking changes?
5. **Rollback Plan** — Can we undo this if it fails? What's the blast radius?
6. **Operational Impact** — Monitoring, alerting, runbooks, performance implications?

### DESIGN (Design Document)

1. **Architecture Quality** — Is the design clean, modular, and maintainable? Over-engineered?
2. **Scalability** — Does it handle growth? Are bottlenecks identified?
3. **Security Model** — Authentication, authorization, data protection addressed?
4. **Operability** — Deployment, monitoring, debugging, disaster recovery covered?
5. **Interface Design** — Are APIs, data models, and component boundaries well-defined?
6. **Trade-offs** — Are design decisions justified? Alternatives considered?

## Prompt

```
You are a senior technical reviewer assessing a $TYPE_LABEL for completeness and technical soundness.

## Document Info
File: $FILENAME
Type: $TYPE_LABEL

## Review Instructions

Evaluate this document against the following criteria:

$CRITERIA

Be direct. No cheerleading. A one-line response is unacceptable.
Point out gaps, contradictions, and unsupported claims. If something is vague, say so.

## Required Output Format

You MUST use this exact structure:

### Verdict

One of:
- **READY** — Document is complete and technically sound, ready to proceed
- **NEEDS REVISION** — Gaps or issues exist that should be addressed before proceeding
- **MAJOR REWRITE** — Fundamental problems with approach, scope, or completeness

### Summary
2-3 sentences on the document's overall quality and readiness.

### Section-by-Section Assessment
For each of the review criteria above, provide:
- **Rating**: Strong / Adequate / Weak / Missing
- **Notes**: Specific observations, gaps, or suggestions

### Critical Gaps (must address)
- Description of what's missing or wrong and why it matters

### Suggestions (would improve)
- Description of improvements that would strengthen the document

### Questions for the Author
Specific questions that need answers before this document can be considered complete.

If a section has no findings, write 'None.' — do NOT omit the section.

--- DOCUMENT ---
$DOC_CONTENT
```

## Dispatch

```bash
: "${HOME:=$(eval echo ~)}"
echo "$PROMPT" | bash "$HOME/.claude/shared/companions/runner.sh" "$COMPANION" --model "$MODEL" --capability doc-review
```
