# Feasibility Assessment — Patterns (L2)

## Complexity Scoring (Technical)

Rate your technical challenges across four dimensions:

| Dimension            | Low (1)                     | Medium (3)                          | High (5)                             |
| -------------------- | --------------------------- | ----------------------------------- | ------------------------------------ |
| Algorithm complexity | CRUD / standard patterns    | Custom logic, ML inference          | Novel algorithm, research-grade      |
| Integration depth    | REST API, standard auth     | Webhooks, event streams, auth flows | Real-time sync, proprietary protocol |
| Data volume/scale    | < 100k records, single user | Millions of records, multi-tenant   | Petabyte scale, global distribution  |
| Reliability bar      | Demo/internal only          | 99% uptime, some error tolerance    | 99.9%+ uptime, zero data loss        |

**Total ≥ 12**: Consider de-scoping or staged rollout. **Total ≥ 16**: Requires specialist hire or partner.

---

## Build vs. Buy Decision

For each hard technical dependency, apply this test:

1. **Is it core to your differentiation?** → Build (or build on top of a foundation)
2. **Is it a commodity that you need but don't own?** → Buy (auth, payments, email, maps)
3. **Is there an open-source option with acceptable license/risk?** → Use and contribute
4. **Does the vendor have lock-in risk?** → Evaluate switching cost before committing

**Heuristic**: If you'd be embarrassed to tell users you built your own auth/payments/email, don't.

---

## Dependency Risk Matrix

For each external dependency (API, dataset, vendor):

| Risk Dimension | Low                                    | High                                |
| -------------- | -------------------------------------- | ----------------------------------- |
| Availability   | 99.9%+ SLA, multiple regions           | No SLA, single point of failure     |
| Pricing        | Fixed / usage-based, stable            | Dynamic, can change without notice  |
| Vendor lock-in | Portable data format                   | Proprietary format, hard to migrate |
| API stability  | Versioned API, long deprecation window | Breaking changes without notice     |

**Mitigation for high-risk dependencies**: Adapter pattern (wrap in your own interface), cache layer, fallback path.

---

## Rough Cost Estimation (Order of Magnitude)

Use T-shirt sizing for MVP estimation:

| Size | Engineering Days | Notes                                         |
| ---- | ---------------- | --------------------------------------------- |
| XS   | 1–3 days         | Single endpoint, simple UI, existing patterns |
| S    | 3–10 days        | New feature area, some new patterns           |
| M    | 10–30 days       | New module, integration, testing overhead     |
| L    | 30–90 days       | New system, complex data model, team needed   |
| XL   | 90+ days         | Major product, full team, multi-quarter       |

**For infrastructure costs**: Start with $X/1000 users/month. If you can't estimate this, you haven't thought through scale yet.

---

## Time Feasibility — Opportunity Window Check

Questions to determine if timing matters:

- **Regulatory**: Is there a compliance deadline creating urgency for your users?
- **Platform**: Is a platform you rely on growing or shrinking? (riding a wave vs. fighting tide)
- **Seasonal**: Does your problem spike at certain times? (tax season, budget cycles)
- **Competitor timing**: Is a well-funded competitor about to enter your market?

**If timing doesn't matter**: That's usually fine — sustainable businesses don't require perfect timing.
**If timing matters a lot**: MVP scope must be ruthlessly minimal to hit the window.

---

## Anti-Patterns

- **Scope creep in MVP**: An MVP with 12 features is not an MVP
- **Ignoring infrastructure cost**: "It's just a cloud API" can get expensive at scale
- **Single-dependency architectures**: One vendor going down kills your product
- **Optimism bias on time**: Double your gut estimate and you'll be closer to reality
