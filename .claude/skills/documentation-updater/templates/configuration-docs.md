# Configuration Documentation Template

## .env.example Template

```bash
# Feature Name Configuration
FEATURE_API_KEY=your_api_key_here
FEATURE_TIMEOUT=30  # Request timeout in seconds
FEATURE_CACHE_TTL=3600  # Cache time-to-live in seconds
FEATURE_DEBUG=false  # Enable debug logging
FEATURE_MAX_RETRIES=3  # Maximum retry attempts
```

## Configuration Guide Template

````markdown
## Configuration Options

### Required Settings

#### FEATURE_API_KEY

- **Type**: string
- **Required**: Yes
- **Description**: API key for authentication
- **Example**: `sk_live_xxxxxxxxxxxx`
- **Where to get**: [URL to get API key]

### Optional Settings

#### FEATURE_TIMEOUT

- **Type**: integer
- **Required**: No
- **Default**: 30
- **Description**: Request timeout in seconds
- **Valid range**: 1-300

## Configuration Methods

### Environment Variables

```bash
export FEATURE_API_KEY=your_key
```
````

### Config File

```yaml
# config.yaml
feature:
  api_key: your_key
  timeout: 30
```

### Programmatic

```python
from llms.feature import configure

configure(api_key="your_key", timeout=30)
```

````

## TECH-STACK Entry Template

```markdown
### <Feature Name> (Added: YYYY-MM-DD)

**Dependencies**:
- **package-name** (version): [Description of why needed]
  - Purpose: [What it's used for]
  - License: [MIT, Apache, etc.]
  - Alternatives considered: [Other options]

**Security Considerations**:
- Vulnerability scan: [Clean/Issues found]
- Maintenance status: [Active/Inactive]
````
