# Go / No-Go Checkpoint — Patterns (L2)

## Scoring Rubric (Detailed)

### Criterion 1: Problem is real

| Evidence Level                                        | Score | Verdict                  |
| ----------------------------------------------------- | ----- | ------------------------ |
| Paid for a partial solution or workaround             | 5     | Strong Pass              |
| Active workarounds + 3+ interviews confirming urgency | 4     | Pass                     |
| 1-2 interviews + some support/forum data              | 3     | Conditional Pass         |
| Only inferred from analogous markets                  | 2     | Conditional (name risk)  |
| Assumption only, no external validation               | 1     | Fail — go validate first |

### Criterion 2: Segment is defined

| Definition Level                                   | Score | Verdict               |
| -------------------------------------------------- | ----- | --------------------- |
| Named companies/contacts who confirmed the problem | 5     | Strong Pass           |
| Specific role + context + industry + size defined  | 4     | Pass                  |
| Role + industry defined, size/context vague        | 3     | Conditional Pass      |
| "SMBs" or "developers" level of specificity        | 2     | Conditional (clarify) |
| "Everyone" or no segment defined                   | 1     | Fail                  |

### Criterion 3: Gap exists

| Gap Level                                                  | Score | Verdict                           |
| ---------------------------------------------------------- | ----- | --------------------------------- |
| Incumbents actively ignore this segment                    | 5     | Strong Pass                       |
| Clear feature gap + users complain about alternatives      | 4     | Pass                              |
| Marginal improvement over alternatives, not transformative | 3     | Conditional (name differentiator) |
| Alternatives exist and are good enough for most users      | 2     | Fail                              |
| You're building a clone with no differentiation            | 1     | Hard Fail                         |

### Criterion 4: Feasible to build

| Feasibility                                              | Score | Verdict                      |
| -------------------------------------------------------- | ----- | ---------------------------- |
| All three dimensions green, no hard dependencies         | 5     | Strong Pass                  |
| 2/3 green, 1 risky but mitigated                         | 4     | Pass                         |
| 1-2 dimensions risky, mitigation plan exists             | 3     | Conditional (document risks) |
| Hard dependency unresolved OR cost unprofitable at scale | 2     | Conditional (resolve first)  |
| Technically blocked or economically unviable             | 1     | Fail                         |

### Criterion 5: Worth doing now

| Timing Evidence                                            | Score | Verdict               |
| ---------------------------------------------------------- | ----- | --------------------- |
| Window closing (regulatory, platform, competitive timing)  | 5     | Strong Pass           |
| High opportunity cost of delay (users going to competitor) | 4     | Pass                  |
| Neutral timing — no urgency, no window                     | 3     | Pass (lower priority) |
| Team at capacity, better use of resources elsewhere        | 2     | Conditional           |
| Actively wrong time (market not ready, foundational gaps)  | 1     | Fail                  |

---

## Conditional Go — Required Mitigations

When verdict is Conditional Go, document this before proceeding:

```
Failing criterion: [criterion name]
Risk: [what could go wrong because this criterion failed]
Mitigation: [what you'll do to reduce the risk]
Validation point: [when / how you'll know if the mitigation worked]
Owner: [who is responsible for the mitigation]
```

A Conditional Go without documented mitigation is just wishful thinking.

---

## No-Go — Escalation Paths

When verdict is No-Go, choose one:

| Option             | When to use                                       | Next step                                     |
| ------------------ | ------------------------------------------------- | --------------------------------------------- |
| **Re-validate**    | Evidence is weak but intuition is strong          | Run 5 user interviews, return to problem mode |
| **Pivot scope**    | Problem is real but feasibility fails             | Re-run feasibility with reduced scope         |
| **Pivot segment**  | Problem exists but current segment is wrong       | Re-run problem mode for a different segment   |
| **Pivot solution** | Problem is real but gap doesn't exist             | Re-run competitive mode, find true gap        |
| **Park it**        | Timing is wrong but everything else is solid      | Add to backlog with a trigger condition       |
| **Kill it**        | Multiple criteria fail with no clear path forward | Document why, don't revisit for 6 months      |

---

## Anti-Patterns

- **Ignoring a failed criterion**: A 4/5 pass with a handwavy mitigation is not a real Conditional Go
- **Checkpoint without running problem/competitive/feasibility**: You're scoring on assumptions, not evidence
- **Going back to change scores to get a Go**: The checkpoint exists to stop bad ideas, not validate them
- **No owner for mitigations**: Risk without an owner is just hope
