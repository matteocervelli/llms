# Playwright MCP to Node Module Migration Plan

## 1. Current State

The `e2e-accessibility-specialist` agent currently:
- Uses Playwright MCP tools (`mcp__playwright-mcp__*`) for browser automation
- Implements WCAG 2.1 Level AA compliance testing
- Performs E2E test implementation and accessibility verification
- Uses Axe-core for automated accessibility scanning
- Tests keyboard navigation, screen reader compatibility, and visual accessibility
- Validates against WCAG 2.1 standards and design system compliance

**Current MCP Dependencies**:
- `mcp__playwright-mcp__playwright_navigate`
- `mcp__playwright-mcp__playwright_screenshot`
- `mcp__playwright-mcp__playwright_click`
- `mcp__playwright-mcp__playwright_fill`
- `mcp__playwright-mcp__playwright_evaluate`

---

## 2. Migration Goals

**Primary Goal**: Replace Playwright MCP with direct `@playwright/test` Node module integration.

**Outcomes**:
- Eliminate MCP tool dependencies for Playwright operations
- Enable direct API control without intermediary layers
- Add visual design validation specific to frontend design systems
- Improve test execution speed and reliability
- Reduce context switching between MCP and native APIs

---

## 3. Technical Approach

### 3.1 Module Installation
```bash
npm install --save-dev @playwright/test @axe-core/playwright
```

### 3.2 API Migration Strategy

| Current MCP Call | New Direct API | Benefit |
|---|---|---|
| `mcp__playwright-mcp__playwright_navigate(url)` | `page.goto(url)` | Native Playwright API |
| `mcp__playwright-mcp__playwright_click(selector)` | `page.click(selector)` | Direct locator control |
| `mcp__playwright-mcp__playwright_fill(selector, value)` | `page.fill(selector, value)` | Native form interaction |
| `mcp__playwright-mcp__playwright_screenshot()` | `page.screenshot()` | Direct screenshot capture |
| `mcp__playwright-mcp__playwright_evaluate(fn)` | `page.evaluate(fn)` | DOM inspection & manipulation |

### 3.3 Locator-Based Refactoring

Migrate from string selectors to Playwright locators for better maintainability:

```typescript
// Before (MCP-style)
await mcp_click('.submit-button');

// After (Node module)
const submitButton = page.locator('[data-testid="submit-button"]');
await submitButton.click();
```

---

## 4. New Features to Add

### 4.1 Font Detection
- Validate Inter/Roboto presence in CSS computed styles
- Check font-loading API compliance (e.g., `document.fonts.ready`)
- Verify font weights match design system (400, 500, 600, 700)

### 4.2 Color Palette Analysis
- Extract computed colors from design system components
- Validate against approved palette (e.g., primary, secondary, neutral shades)
- Cross-reference with Axe color contrast checks
- Detect undeclared colors (potential design violations)

### 4.3 Animation Presence Check
- Detect CSS transitions/animations on interactive elements
- Verify animations respect `prefers-reduced-motion` media query
- Check animation duration compliance (< 500ms for UI feedback)
- Validate animations don't cause accessibility issues

### 4.4 Layout Asymmetry Detection
- Analyze spacing/padding consistency using computed styles
- Detect grid/flex layout violations
- Check alignment against design grid (e.g., 4px, 8px, 16px multiples)
- Flag unexpected layout asymmetries

---

## 5. Implementation Steps

1. **Setup**
   - Install `@playwright/test` and `@axe-core/playwright`
   - Create `playwright.config.ts` with design system project config
   - Initialize test directory structure

2. **Core Migration**
   - Replace all MCP tool calls with native Playwright API
   - Refactor selectors to use robust locator strategies
   - Update test assertion patterns

3. **Accessibility Base**
   - Integrate Axe-core with Playwright in base test fixture
   - Create helper function for WCAG 2.1 Level AA scanning
   - Implement keyboard navigation test utilities

4. **Design System Validators**
   - Build font detection module
   - Build color palette analyzer module
   - Build animation presence checker module
   - Build layout grid validator module

5. **Test Suite Organization**
   - Migrate existing E2E tests to new structure
   - Create design system validation tests
   - Implement visual regression snapshot tests

6. **Documentation & Examples**
   - Document new design validation APIs
   - Create example tests for each validator
   - Update accessibility testing guidelines

---

## 6. Validation Criteria

**Success Metrics**:
- [ ] All MCP Playwright calls replaced with direct API equivalents
- [ ] Existing WCAG 2.1 Level AA tests function identically
- [ ] New font detection catches missing Inter/Roboto declarations
- [ ] Color palette analyzer identifies design violations
- [ ] Animation checker validates motion accessibility
- [ ] Layout validator catches spacing inconsistencies
- [ ] Test execution time equal to or faster than MCP version
- [ ] All tests run in isolation without MCP service dependency
- [ ] New validators achieve 90%+ detection accuracy on known violations

**Quality Gates**:
- All tests pass on Chromium, Firefox, WebKit
- No test flakiness (run tests 5x consecutively)
- Full code coverage for validator modules (80%+)
- Accessibility report structure consistent with WCAG 2.1 standards

---

## 7. Rollback Plan

If migration encounters blockers:
1. Keep existing MCP agent as `e2e-accessibility-specialist-mcp` backup
2. Create feature branch to test new implementation
3. Parallel run both versions in CI during transition period
4. Revert to MCP version if validation criteria not met

---

## Timeline Estimate

- Phase 1 (Setup + Core Migration): 2-3 days
- Phase 2 (Design Validators): 3-4 days
- Phase 3 (Testing + Documentation): 2-3 days
- **Total**: 7-10 days

