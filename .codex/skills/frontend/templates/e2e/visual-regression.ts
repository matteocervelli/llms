/**
 * Visual Regression Test Templates
 *
 * Screenshot comparison tests for UI consistency.
 */

import { test, expect } from "@playwright/test";

// =============================================================================
// Full Page Screenshots
// =============================================================================

test.describe("Visual Regression", () => {
  test("homepage matches baseline", async ({ page }) => {
    await page.goto("/");

    // Take full page screenshot
    await expect(page).toHaveScreenshot("homepage.png", {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test("login page matches baseline", async ({ page }) => {
    await page.goto("/login");

    await expect(page).toHaveScreenshot("login-page.png", {
      fullPage: true,
    });
  });

  test("dashboard matches baseline", async ({ page }) => {
    // Login first
    await page.goto("/login");
    await page.fill("#username", "user@example.com");
    await page.fill("#password", "ValidPassword123!");
    await page.click('button[type="submit"]');
    await page.waitForURL("/dashboard");

    await expect(page).toHaveScreenshot("dashboard.png", {
      fullPage: true,
    });
  });
});

// =============================================================================
// Component Screenshots
// =============================================================================

test.describe("Component Visual Tests", () => {
  test("modal dialog matches baseline", async ({ page }) => {
    await page.goto("/");
    await page.click('[data-testid="open-modal"]');

    // Screenshot of specific element
    const modal = page.locator(".modal");
    await expect(modal).toHaveScreenshot("modal.png");
  });

  test("navigation menu matches baseline", async ({ page }) => {
    await page.goto("/");

    const nav = page.locator("nav");
    await expect(nav).toHaveScreenshot("navigation.png");
  });

  test("footer matches baseline", async ({ page }) => {
    await page.goto("/");

    const footer = page.locator("footer");
    await expect(footer).toHaveScreenshot("footer.png");
  });
});

// =============================================================================
// Theme Visual Tests
// =============================================================================

test.describe("Theme Visual Tests", () => {
  test("light mode matches baseline", async ({ page }) => {
    await page.goto("/");

    await page.evaluate(() => {
      document.documentElement.setAttribute("data-theme", "light");
    });

    await expect(page).toHaveScreenshot("homepage-light.png", {
      fullPage: true,
    });
  });

  test("dark mode matches baseline", async ({ page }) => {
    await page.goto("/");

    await page.evaluate(() => {
      document.documentElement.setAttribute("data-theme", "dark");
    });

    await expect(page).toHaveScreenshot("homepage-dark.png", {
      fullPage: true,
    });
  });
});

// =============================================================================
// State Visual Tests
// =============================================================================

test.describe("State Visual Tests", () => {
  test("loading state matches baseline", async ({ page }) => {
    // Mock slow API
    await page.route("**/api/data", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 5000));
      await route.fulfill({ status: 200, body: "{}" });
    });

    await page.goto("/data");

    const loadingState = page.locator(".loading-skeleton");
    await expect(loadingState).toHaveScreenshot("loading-state.png");
  });

  test("error state matches baseline", async ({ page }) => {
    // Mock API error
    await page.route("**/api/data", (route) => {
      route.fulfill({ status: 500, body: "Error" });
    });

    await page.goto("/data");

    const errorState = page.locator(".error-message");
    await expect(errorState).toHaveScreenshot("error-state.png");
  });

  test("empty state matches baseline", async ({ page }) => {
    // Mock empty response
    await page.route("**/api/items", (route) => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({ items: [] }),
      });
    });

    await page.goto("/items");

    const emptyState = page.locator(".empty-state");
    await expect(emptyState).toHaveScreenshot("empty-state.png");
  });
});
