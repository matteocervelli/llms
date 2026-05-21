/**
 * Authentication Setup Templates
 *
 * Reuse authentication state across tests for efficiency.
 */

import { test as setup, expect } from "@playwright/test";
import { LoginPage } from "./page-object-model";

// =============================================================================
// Auth State File Paths
// =============================================================================

const authFiles = {
  user: "playwright/.auth/user.json",
  admin: "playwright/.auth/admin.json",
};

// =============================================================================
// User Authentication Setup
// =============================================================================

setup("authenticate as user", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login("user@example.com", "ValidPassword123!");

  await page.waitForURL("/dashboard");

  // Save authentication state
  await page.context().storageState({ path: authFiles.user });
});

// =============================================================================
// Admin Authentication Setup
// =============================================================================

setup("authenticate as admin", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login("admin@example.com", "AdminPassword123!");

  await page.waitForURL("/admin/dashboard");

  // Save authentication state
  await page.context().storageState({ path: authFiles.admin });
});

// =============================================================================
// Playwright Config with Auth
// =============================================================================

/*
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    // Setup project - runs first
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
    },

    // User tests - uses saved auth
    {
      name: 'user-tests',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // Admin tests - uses saved admin auth
    {
      name: 'admin-tests',
      testMatch: /.*admin.*\.spec\.ts/,
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/admin.json',
      },
      dependencies: ['setup'],
    },

    // Unauthenticated tests
    {
      name: 'unauth-tests',
      testMatch: /.*unauth.*\.spec\.ts/,
      use: {
        ...devices['Desktop Chrome'],
        // No storageState = logged out
      },
    },
  ],
});
*/

// =============================================================================
// Test Using Auth State
// =============================================================================

/*
// tests/e2e/user/profile.spec.ts
import { test, expect } from '@playwright/test';

// This test runs with user authentication (from config)
test('user can view profile', async ({ page }) => {
  // Already authenticated - go directly to protected page
  await page.goto('/profile');

  await expect(page.locator('.profile-header')).toBeVisible();
});


// tests/e2e/admin/users.spec.ts
import { test, expect } from '@playwright/test';

// This test runs with admin authentication (from config)
test('admin can view user list', async ({ page }) => {
  await page.goto('/admin/users');

  await expect(page.locator('.user-table')).toBeVisible();
});
*/
