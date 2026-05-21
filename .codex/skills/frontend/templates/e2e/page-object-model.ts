/**
 * Page Object Model Templates
 *
 * Base classes and examples for Playwright page objects.
 */

import { Page, Locator } from "@playwright/test";

// =============================================================================
// Base Page Class
// =============================================================================

export class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto(path: string) {
    await this.page.goto(path);
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState("networkidle");
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }

  async getTitle(): Promise<string> {
    return await this.page.title();
  }

  async clickElement(locator: Locator) {
    await locator.waitFor({ state: "visible" });
    await locator.click();
  }

  async fillInput(locator: Locator, value: string) {
    await locator.waitFor({ state: "visible" });
    await locator.fill(value);
  }

  async getText(locator: Locator): Promise<string> {
    await locator.waitFor({ state: "visible" });
    return (await locator.textContent()) || "";
  }
}

// =============================================================================
// Login Page Example
// =============================================================================

export class LoginPage extends BasePage {
  // Locators
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;
  readonly signUpLink: Locator;

  constructor(page: Page) {
    super(page);
    this.usernameInput = page.locator("#username");
    this.passwordInput = page.locator("#password");
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator(".error-message");
    this.forgotPasswordLink = page.locator('a[href="/forgot-password"]');
    this.signUpLink = page.locator('a[href="/signup"]');
  }

  // Actions
  async goto() {
    await super.goto("/login");
  }

  async login(username: string, password: string) {
    await this.fillInput(this.usernameInput, username);
    await this.fillInput(this.passwordInput, password);
    await this.clickElement(this.submitButton);
  }

  async clickForgotPassword() {
    await this.clickElement(this.forgotPasswordLink);
  }

  async clickSignUp() {
    await this.clickElement(this.signUpLink);
  }

  // Assertions helpers
  async getErrorMessage(): Promise<string> {
    return await this.getText(this.errorMessage);
  }

  async isLoginButtonEnabled(): Promise<boolean> {
    return await this.submitButton.isEnabled();
  }

  async waitForErrorMessage() {
    await this.errorMessage.waitFor({ state: "visible" });
  }
}

// =============================================================================
// Dashboard Page Example
// =============================================================================

export class DashboardPage extends BasePage {
  readonly welcomeMessage: Locator;
  readonly profileLink: Locator;
  readonly logoutButton: Locator;
  readonly profileName: Locator;

  constructor(page: Page) {
    super(page);
    this.welcomeMessage = page.locator(".welcome-message");
    this.profileLink = page.locator('a[href="/profile"]');
    this.logoutButton = page.locator('[data-testid="logout"]');
    this.profileName = page.locator(".profile-name");
  }

  async goToProfile() {
    await this.clickElement(this.profileLink);
  }

  async logout() {
    await this.clickElement(this.logoutButton);
  }

  async updateProfile(data: { firstName?: string; lastName?: string }) {
    // Implement profile update logic
  }
}
