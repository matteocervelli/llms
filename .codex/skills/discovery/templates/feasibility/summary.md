# Feasibility Assessment

Three dimensions. Each can kill the project independently.

## 1. Technical Feasibility

- **Core capability**: Do you have the technical skills/stack to build this?
- **Key risks**: What's the hardest part? (algorithm, integration, scale, data)
- **Dependencies**: External APIs, third-party data, hardware, regulatory requirements
- **Build vs buy**: Can the hard part be bought/licensed instead of built?

Verdict: **Viable** / **Risky** (name the risk) / **Blocked** (hard dependency missing)

## 2. Economic Feasibility

- **Cost to build**: Rough order of magnitude (days of work × rate, infrastructure, licenses)
- **Cost to operate**: Monthly recurring cost at target scale
- **Revenue path**: How does this make money, or what does it enable that makes money?
- **Break-even**: At what usage/revenue level does this pay for itself?

Verdict: **Profitable** / **Sustainable** (non-profit/internal tool) / **Unprofitable** (cost > value)

## 3. Time Feasibility

- **MVP scope**: What's the smallest version that validates the hypothesis?
- **Time to MVP**: Realistic estimate (err on the side of 2× your gut feeling)
- **Dependencies on timeline**: External events, team availability, deadlines
- **Opportunity window**: Is there a time constraint? Does speed matter here?

Verdict: **Now** / **Later** (blocked by X until Y date) / **Never** (window closed)

## Output

```
Technical: [Viable / Risky: <risk> / Blocked: <dependency>]
Economic:  [Profitable / Sustainable / Unprofitable]
Time:      [Now / Later: <reason> / Never: <reason>]
MVP scope: [2-sentence description]
```

---

Want scoring rubrics or build-vs-buy analysis? Ask "show me patterns" or continue with `/discovery checkpoint`.
