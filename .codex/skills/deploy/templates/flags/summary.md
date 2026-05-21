# Feature Flags — L1 Essentials

## Provider Comparison

| Provider        | Infra needed | Latency    | Best for                       |
| --------------- | ------------ | ---------- | ------------------------------ |
| LaunchDarkly    | None (SaaS)  | ~1ms SDK   | Teams, audit logs, targeting   |
| Flipt           | Self-hosted  | ~1ms local | Privacy-first, no vendor lock  |
| Env-based (DIY) | None         | 0ms        | Simple on/off, no SDK overhead |

## Non-Negotiable Rules

1. **Evaluate at request time** — never at startup or module import
2. **Never log flag values** — it's an info disclosure risk
3. **Every flag needs a TTL** — clean up within 1–2 sprints of full rollout
4. **Default to OFF** — flag evaluates to false if SDK fails/unreachable

## Minimal Implementation Pattern

```python
# FastAPI example — evaluate per request, not at startup
@router.get("/feature")
async def feature_endpoint(request: Request):
    user_key = get_user_key(request)
    if flag_client.variation("new-feature", {"key": user_key}, False):
        return new_implementation()
    return legacy_implementation()
```

## Next Steps

- For SDK patterns and Don't/Do/Best examples → ask for **patterns**
- For secrets/key management → `/security operations`
