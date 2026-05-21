# Problem Framing — Patterns (L2)

## Jobs-to-Be-Done (JTBD) Framework

Frame the problem as a job the user is trying to accomplish, not a feature they want:

**Template**: "When [situation], I want to [motivation], so I can [expected outcome]."

**Good**: "When I onboard a new client, I want to capture all the data without back-and-forth email, so I can start the project faster."
**Bad**: "I want a form builder." (that's a solution, not a job)

The job stays stable; the solution can change. If you can't express the job, you don't understand the problem yet.

---

## Pain-Point Scoring Matrix

Score each observed pain point to prioritize:

| Dimension   | 1 (Low)             | 3 (Medium)         | 5 (High)                 |
| ----------- | ------------------- | ------------------ | ------------------------ |
| Frequency   | Monthly or less     | Weekly             | Daily / per workflow     |
| Severity    | Minor inconvenience | Slows work down    | Blocks progress entirely |
| Workaround  | Good workaround     | Partial workaround | No viable workaround     |
| Willingness | Won't pay           | Maybe pays         | Actively looking to pay  |

**Score = Frequency × Severity × (Workaround + Willingness) / 2**

Target: Total ≥ 30 before investing significant build time.

---

## User Segment Mapping

Three levels of segmentation:

1. **Firmographic**: Company size, industry, geography, revenue
2. **Behavioral**: How they currently solve the problem, tech stack, maturity
3. **Attitudinal**: How much they care about this problem (urgency, awareness)

**Avoid demographic-only segments** ("25-35 year olds") — they don't predict buying behavior.

**Best-fit segment formula**: High pain score + existing budget for a solution + decision-making authority.

---

## Evidence Hierarchy

Not all evidence is equal. Weight it accordingly:

| Type            | Weight | Example                                          |
| --------------- | ------ | ------------------------------------------------ |
| Observed (paid) | 5×     | User paid for a partial solution to this problem |
| Observed (free) | 3×     | User actively uses workarounds                   |
| Stated intent   | 2×     | User said they'd pay in an interview             |
| Inferred        | 1×     | Analogous market data, proxy signals             |
| Assumed         | 0.5×   | Gut feel, "seems obvious"                        |

**Red flag**: If all your evidence is assumed, stop and do 5 user interviews before proceeding.

---

## Anti-Patterns to Avoid

- **Solution-first framing**: "We need a dashboard" vs. "users can't track their progress"
- **Feature requests as problems**: A request for a feature is not evidence of a problem
- **Over-segmenting**: "Tech-savvy, 28-year-old, remote-working, Italian startup founders" — too narrow
- **Under-segmenting**: "SMBs" — not actionable; which SMBs, in which context?
- **Assuming urgency**: "Everyone has this problem" is not urgency evidence
