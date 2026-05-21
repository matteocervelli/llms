# Feature Flags — Key Patterns (Don't/Do/Best)

## LaunchDarkly (Python SDK)

**Don't:** Initialize client per request

```python
# BAD — reconnects on every call
def get_flag():
    client = LDClient(Config("sdk-key"))
    return client.variation("flag", user, False)
```

**Do:** Singleton client, per-request evaluation

```python
# app/flags.py
import ldclient
from ldclient.config import Config

_client: ldclient.LDClient | None = None

def get_client() -> ldclient.LDClient:
    global _client
    if _client is None:
        _client = ldclient.LDClient(Config(settings.LD_SDK_KEY))
    return _client

# In endpoint
def is_enabled(flag_key: str, user_key: str, default: bool = False) -> bool:
    return get_client().variation(flag_key, {"key": user_key}, default)
```

**Best:** Wrap with context (user attributes for targeting)

```python
context = {"key": user_key, "email": user_email, "plan": user_plan}
enabled = get_client().variation("new-checkout", context, False)
```

---

## Flipt (self-hosted gRPC)

**Don't:** Use HTTP polling — use gRPC for latency

```python
# BAD — slow, no streaming
requests.get(f"http://flipt/api/v1/flags/{key}/evaluation")
```

**Do:** gRPC client with local caching

```python
from flipt.evaluation import EvaluationClient

client = EvaluationClient(url="grpc://flipt:9000")

def is_enabled(flag_key: str, entity_id: str) -> bool:
    response = client.boolean(flag_key, entity_id=entity_id)
    return response.enabled
```

**Best:** Deploy Flipt as a sidecar to minimize network hop

---

## Env-Based (DIY — no SDK)

**Don't:** Hardcode feature state in code

```python
# BAD — requires code change to toggle
ENABLE_NEW_DASHBOARD = True
```

**Do:** Read from environment, validated at startup

```python
# config.py
class Settings(BaseSettings):
    enable_new_dashboard: bool = False  # ENABLE_NEW_DASHBOARD=true in env

settings = Settings()
```

**Best:** Use a `feature_flags.yaml` loaded at startup with hot-reload

```yaml
# feature_flags.yaml
flags:
  new_dashboard:
    enabled: true
    rollout_percent: 50 # serve to 50% based on user_id hash
  beta_api:
    enabled: false
    expires: "2026-04-01" # TTL enforced in CI lint rule
```

```python
def is_in_rollout(flag: dict, user_id: str) -> bool:
    if not flag.get("enabled"):
        return False
    pct = flag.get("rollout_percent", 100)
    return (int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 100) < pct
```

---

## Cleanup Rule

Add to CI: flag keys must have `expires:` set or fail lint. Remove dead flags after full rollout.

```bash
# .github/workflows/flags-lint.yml
grep -r "flags:" feature_flags.yaml | while read flag; do
  if ! echo "$flag" | grep -q "expires:"; then
    echo "ERROR: Flag missing TTL" && exit 1
  fi
done
```
