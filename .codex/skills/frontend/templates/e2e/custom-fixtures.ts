/**
 * Custom Playwright Fixtures Template
 *
 * Extend base test with custom fixtures for reusable test setup.
 */

import { test as base, Page } from "@playwright/test";
import { LoginPage } from "./page-object-model";
import { DashboardPage } from "./page-object-model";

// =============================================================================
// Test Data
// =============================================================================

export const testUsers = {
  validUser: {
    email: "user@example.com",
    password: "ValidPassword123!",
  },
  adminUser: {
    email: "admin@example.com",
    password: "AdminPassword123!",
  },
  newUser: {
    email: "newuser@example.com",
    password: "NewPassword123!",
    firstName: "John",
    lastName: "Doe",
  },
};

export const testProducts = {
  product1: {
    id: "item-123",
    name: "Test Product",
    price: 29.99,
  },
};

// =============================================================================
// Fixture Type Definitions
// =============================================================================

type MyFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page;
};

// =============================================================================
// Extended Test with Fixtures
// =============================================================================

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  authenticatedPage: async ({ page }, use) => {
    // Auto-login before test
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login("user@example.com", "ValidPassword123!");
    await page.waitForURL("/dashboard");
    await use(page);
  },
});

export { expect } from "@playwright/test";

// =============================================================================
// Usage Example
// =============================================================================

/*
// tests/e2e/features/profile.spec.ts
import { test, expect } from '../../fixtures/custom-fixtures';

test.describe('User Profile', () => {
  test('user can update profile information', async ({ authenticatedPage, dashboardPage }) => {
    // Already logged in via authenticatedPage fixture
    await dashboardPage.goToProfile();

    // Test continues with authenticated context
    await dashboardPage.updateProfile({
      firstName: 'Jane',
      lastName: 'Smith',
    });

    await expect(dashboardPage.profileName).toHaveText('Jane Smith');
  });
});
*/
