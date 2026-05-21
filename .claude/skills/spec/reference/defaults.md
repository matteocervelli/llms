# Fast Mode Defaults

Applied when `--fast` flag is used. Every assumption is documented in the spec
with a `> Assumed:` prefix so the Codex review can flag disagreements.

| Decision | Default | Rationale |
|----------|---------|-----------|
| Self-referential FK | `ON DELETE SET NULL` | Children survive parent deletion; safe for tree reorganization |
| Tree structure | Adjacency list (`parent_id`) | Simple, sufficient for ≤5 levels; defer closure table |
| Status lifecycle | `draft → active → paused → done → cancelled` | Matches work_items pattern |
| Soft delete | No | Not in scope unless issue explicitly mentions it |
| PK type | UUID (`gen_random_uuid()`) | Consistent with new Nexus-domain tables |
| Cross-repo FK | Loose string unless FK table is known | Avoids migration coupling across repos |
| Test approach | `respx` for HTTP proxy, `unittest.mock` for service layer | Matches existing patterns |
| owner FK | FK to `agent_registry(agent_role)` ON DELETE SET NULL if table exists | Check codebase first |
