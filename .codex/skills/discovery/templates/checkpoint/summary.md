# Go / No-Go Checkpoint

Five criteria. Each is pass/fail. All five must pass for a clean Go.

## Criteria

| #   | Criterion              | Question                                                 | Pass condition                       |
| --- | ---------------------- | -------------------------------------------------------- | ------------------------------------ |
| 1   | **Problem is real**    | Is there evidence beyond assumption?                     | Observed or inferred evidence exists |
| 2   | **Segment is defined** | Do you know exactly who you're building for?             | Named segment with clear context     |
| 3   | **Gap exists**         | Is there a market gap, or are you cloning a commodity?   | Clear differentiator identified      |
| 4   | **Feasible to build**  | Are all three feasibility dimensions green or mitigated? | No hard blockers; risks are named    |
| 5   | **Worth doing now**    | Is this the right problem at the right time?             | Opportunity cost of delay is high    |

## Scoring

- **5/5 pass** → **Go** — proceed to `/story create`
- **4/5 pass** → **Conditional Go** — flag the failing criterion as a risk; document mitigation before `/story`
- **3/5 or below** → **No-Go** — stop here; identify what needs to change before re-evaluating

## Verdict Format

```
Criterion 1 — Problem is real:    [Pass / Fail] — <one-line rationale>
Criterion 2 — Segment is defined: [Pass / Fail] — <one-line rationale>
Criterion 3 — Gap exists:         [Pass / Fail] — <one-line rationale>
Criterion 4 — Feasible to build:  [Pass / Fail] — <one-line rationale>
Criterion 5 — Worth doing now:    [Pass / Fail] — <one-line rationale>

Verdict: [Go / Conditional Go / No-Go]
Next step: [/story create | fix <criterion> | pivot to <alternative>]
```

---

Want the scoring rubric or escalation paths for a No-Go? Ask "show me patterns".
**Go verdict?** → Run `/story create` to define the feature scope.
