/**
 * API Mocking Test Templates
 *
 * Mock API responses for testing edge cases and error states.
 */

import { test, expect } from "@playwright/test";

// =============================================================================
// Response Timing Tests
// =============================================================================

test.describe("API Response Timing", () => {
  test("handles slow API response gracefully", async ({ page }) => {
    // Mock slow API
    await page.route("**/api/products", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 3000));
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ products: [] }),
      });
    });

    await page.goto("/products");

    // Should show loading state
    await expect(page.locator(".loading-spinner")).toBeVisible();

    // Should eventually show products
    await expect(page.locator(".product-list")).toBeVisible({ timeout: 5000 });
  });

  test("handles network timeout", async ({ page }) => {
    await page.route("**/api/products", (route) => {
      // Never fulfill, causing timeout
    });

    await page.goto("/products");

    // Should show timeout message
    await expect(page.locator(".timeout-message")).toBeVisible({
      timeout: 10000,
    });
  });
});

// =============================================================================
// Error Response Tests
// =============================================================================

test.describe("API Error Handling", () => {
  test("handles 500 error gracefully", async ({ page }) => {
    await page.route("**/api/products", (route) => {
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: "Internal server error" }),
      });
    });

    await page.goto("/products");

    await expect(page.locator(".error-message")).toBeVisible();
    await expect(page.locator(".error-message")).toContainText(
      "Failed to load",
    );
  });

  test("handles 404 error gracefully", async ({ page }) => {
    await page.route("**/api/products/123", (route) => {
      route.fulfill({
        status: 404,
        body: JSON.stringify({ error: "Not found" }),
      });
    });

    await page.goto("/products/123");

    await expect(page.locator(".not-found-message")).toBeVisible();
  });

  test("handles 401 unauthorized", async ({ page }) => {
    await page.route("**/api/protected", (route) => {
      route.fulfill({
        status: 401,
        body: JSON.stringify({ error: "Unauthorized" }),
      });
    });

    await page.goto("/protected");

    // Should redirect to login
    await expect(page).toHaveURL("/login");
  });

  test("handles 403 forbidden", async ({ page }) => {
    await page.route("**/api/admin", (route) => {
      route.fulfill({
        status: 403,
        body: JSON.stringify({ error: "Forbidden" }),
      });
    });

    await page.goto("/admin");

    await expect(page.locator(".access-denied")).toBeVisible();
  });

  test("handles network error", async ({ page }) => {
    await page.route("**/api/products", (route) => {
      route.abort("failed");
    });

    await page.goto("/products");

    await expect(page.locator(".network-error")).toBeVisible();
  });
});

// =============================================================================
// Mock Data Tests
// =============================================================================

test.describe("Mock Data Scenarios", () => {
  test("displays empty state correctly", async ({ page }) => {
    await page.route("**/api/products", (route) => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({ products: [] }),
      });
    });

    await page.goto("/products");

    await expect(page.locator(".empty-state")).toBeVisible();
    await expect(page.locator(".empty-state")).toContainText(
      "No products found",
    );
  });

  test("displays single item correctly", async ({ page }) => {
    await page.route("**/api/products", (route) => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({
          products: [{ id: 1, name: "Test Product", price: 29.99 }],
        }),
      });
    });

    await page.goto("/products");

    await expect(page.locator(".product-card")).toHaveCount(1);
    await expect(page.locator(".product-card")).toContainText("Test Product");
  });

  test("displays pagination with many items", async ({ page }) => {
    const products = Array.from({ length: 100 }, (_, i) => ({
      id: i + 1,
      name: `Product ${i + 1}`,
      price: 9.99,
    }));

    await page.route("**/api/products*", (route) => {
      route.fulfill({
        status: 200,
        body: JSON.stringify({ products: products.slice(0, 20), total: 100 }),
      });
    });

    await page.goto("/products");

    await expect(page.locator(".pagination")).toBeVisible();
    await expect(page.locator(".product-card")).toHaveCount(20);
  });
});

// =============================================================================
// Intercept and Modify
// =============================================================================

test.describe("Request Interception", () => {
  test("can modify request headers", async ({ page }) => {
    await page.route("**/api/**", (route) => {
      const headers = {
        ...route.request().headers(),
        "X-Custom-Header": "test-value",
      };
      route.continue({ headers });
    });

    await page.goto("/");
    // API calls will now include custom header
  });

  test("can log all API requests", async ({ page }) => {
    const requests: string[] = [];

    await page.route("**/api/**", (route) => {
      requests.push(route.request().url());
      route.continue();
    });

    await page.goto("/dashboard");

    // Verify expected API calls were made
    expect(requests).toContain(expect.stringContaining("/api/user"));
    expect(requests).toContain(expect.stringContaining("/api/data"));
  });
});
