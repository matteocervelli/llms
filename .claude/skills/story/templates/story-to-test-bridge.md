# Story-to-Test Bridge — TDD Red Phase Generator

Maps acceptance criteria (Given/When/Then) to failing test stubs.

## Mapping Rules

### Given → Test Setup (Arrange)

| Given Pattern                       | Test Setup                                     |
| ----------------------------------- | ---------------------------------------------- |
| "user is logged in as {role}"       | `authenticated_client` fixture with role param |
| "database has {data}"               | Factory/fixture creating test data             |
| "{entity} exists with {state}"      | Create entity in test DB or mock               |
| "API {endpoint} returns {response}" | Mock/patch the external call                   |
| "system is in {state}"              | Configuration/environment setup                |

### When → Action (Act)

| When Pattern               | Test Action                           |
| -------------------------- | ------------------------------------- |
| "navigate to {path}"       | `client.get(path)` or page navigation |
| "submit {form}"            | `client.post(path, data=form_data)`   |
| "click {element}"          | E2E: `page.click(selector)`           |
| "call {function/endpoint}" | Direct function call or API request   |
| "upload {file}"            | `client.post(path, files=...)`        |
| "wait {duration}"          | Time mock or async wait               |

### Then → Assertion (Assert)

| Then Pattern                 | Assertion                                     |
| ---------------------------- | --------------------------------------------- |
| "see {content}"              | `assert "{content}" in response.text`         |
| "status code is {code}"      | `assert response.status_code == {code}`       |
| "redirected to {path}"       | `assert response.headers["location"] == path` |
| "{field} equals {value}"     | `assert result.field == value`                |
| "error message {msg}"        | `assert "{msg}" in response.text`             |
| "database contains {record}" | Query DB and assert record exists             |
| "email sent to {addr}"       | Assert mock mailer called                     |
| "file downloaded"            | Assert response content-disposition           |

## Pytest Output Format

```python
"""Tests generated from US-XXXX: {story_title}

TDD Red Phase — these tests MUST FAIL initially.
Implement the feature to make them pass (Green phase).
"""

import pytest
# TODO: Import modules under test once they exist


class TestUS_XXXX:
    """Tests for: {story_title}"""

    def test_{criterion_slug}(self):
        """Given {given}
        When {when}
        Then {then}"""
        # Arrange
        # TODO: {setup_hint from given}

        # Act
        # TODO: {action_hint from when}

        # Assert
        # TODO: {assertion_hint from then}
        assert False, "RED PHASE: Implement {story_title}"
```

## Jest Output Format

```typescript
/**
 * Tests generated from US-XXXX: {story_title}
 *
 * TDD Red Phase — these tests MUST FAIL initially.
 * Implement the feature to make them pass (Green phase).
 */

describe("US-XXXX: {story_title}", () => {
  test("{criterion_description}", () => {
    // Arrange
    // TODO: {setup_hint from given}

    // Act
    // TODO: {action_hint from when}

    // Assert
    // TODO: {assertion_hint from then}
    expect(true).toBe(false); // RED PHASE: Implement {story_title}
  });
});
```

## Test File Naming

| Framework | Pattern                                     | Example                                        |
| --------- | ------------------------------------------- | ---------------------------------------------- |
| pytest    | `tests/unit/test_US_XXXX_{feature_slug}.py` | `tests/unit/test_US_0012_dashboard_metrics.py` |
| jest      | `__tests__/US_XXXX_{feature_slug}.test.ts`  | `__tests__/US_0012_dashboard_metrics.test.ts`  |

## Grouping Rules

- One test file per story (group all criteria into one class/describe)
- Test function name: `test_{criterion_slug}` derived from the "then" clause
- If multiple stories share the same feature area, suggest grouping them into one file
- Always include the story ID in the test docstring/comment for traceability
