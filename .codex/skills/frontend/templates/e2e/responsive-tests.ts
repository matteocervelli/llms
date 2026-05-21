/**
 * Responsive Design Test Templates
 *
 * Test layouts across multiple viewport sizes.
 */

import { test, expect, devices } from "@playwright/test";

// =============================================================================
// Viewport Configuration
// =============================================================================

const viewports = [
  { name: "Desktop", device: devices["Desktop Chrome"] },
  { name: "Tablet", device: devices["iPad Pro"] },
  { name: "Mobile", device: devices["iPhone 12"] },
];

// =============================================================================
// Responsive Layout Tests
// =============================================================================

viewports.forEach(({ name, device }) => {
  test.describe(`${name} Layout`, () => {
    test.use(device);

    test("navigation menu displays correctly", async ({ page }) => {
      await page.goto("/");

      if (name === "Mobile") {
        // Mobile should show hamburger menu
        await expect(page.locator(".hamburger-menu")).toBeVisible();
        await expect(page.locator(".desktop-nav")).not.toBeVisible();
      } else {
        // Desktop/Tablet should show full navigation
        await expect(page.locator(".desktop-nav")).toBeVisible();
        await expect(page.locator(".hamburger-menu")).not.toBeVisible();
      }
    });

    test("images are responsive", async ({ page }) => {
      await page.goto("/products");

      const images = page.locator("img");
      const count = await images.count();

      for (let i = 0; i < count; i++) {
        const img = images.nth(i);
        const bbox = await img.boundingBox();
        if (bbox) {
          // Images should not overflow viewport
          expect(bbox.width).toBeLessThanOrEqual(device.viewport.width);
        }
      }
    });

    test("content is readable without horizontal scroll", async ({ page }) => {
      await page.goto("/");

      // Check for horizontal overflow
      const hasHorizontalScroll = await page.evaluate(() => {
        return (
          document.documentElement.scrollWidth >
          document.documentElement.clientWidth
        );
      });

      expect(hasHorizontalScroll).toBe(false);
    });

    test("touch targets are large enough", async ({ page }) => {
      if (name !== "Mobile") return;

      await page.goto("/");

      const interactiveElements = page.locator(
        'a, button, input, [role="button"]',
      );
      const count = await interactiveElements.count();

      for (let i = 0; i < count; i++) {
        const element = interactiveElements.nth(i);
        const bbox = await element.boundingBox();

        if (bbox && bbox.width > 0 && bbox.height > 0) {
          // Minimum touch target: 44x44 pixels
          expect(bbox.width).toBeGreaterThanOrEqual(44);
          expect(bbox.height).toBeGreaterThanOrEqual(44);
        }
      }
    });
  });
});

// =============================================================================
// Custom Viewport Tests
// =============================================================================

test.describe("Custom Viewport Tests", () => {
  test("layout at 1440px (large desktop)", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto("/");

    // Test specific layout expectations for large screens
    await expect(page.locator(".sidebar")).toBeVisible();
  });

  test("layout at 768px (tablet breakpoint)", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto("/");

    // Test tablet-specific layout
  });

  test("layout at 375px (mobile breakpoint)", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    // Test mobile-specific layout
  });
});
