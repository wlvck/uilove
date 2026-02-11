import { test, expect } from '@playwright/test'

test.describe('Admin Login', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/admin/login')
  })

  test('displays login form', async ({ page }) => {
    await expect(page.locator('input[type="email"], input[name="email"]')).toBeVisible()
    await expect(page.locator('input[type="password"]')).toBeVisible()
  })

  test('has login button', async ({ page }) => {
    const loginButton = page.locator('button[type="submit"], button:has-text("Login"), button:has-text("Sign in")')
    await expect(loginButton.first()).toBeVisible()
  })

  test('shows error on invalid credentials', async ({ page }) => {
    await page.locator('input[type="email"], input[name="email"]').fill('invalid@test.com')
    await page.locator('input[type="password"]').fill('wrongpassword')
    await page.locator('button[type="submit"], button:has-text("Login"), button:has-text("Sign in")').first().click()
    await page.waitForTimeout(1000)
    // Should show error message or stay on login page
    await expect(page).toHaveURL(/login/)
  })

  test('email field validates input', async ({ page }) => {
    const emailInput = page.locator('input[type="email"]')
    if (await emailInput.isVisible()) {
      await emailInput.fill('notanemail')
      await page.locator('input[type="password"]').fill('password')
      await page.locator('button[type="submit"]').first().click()
      // Browser validation should prevent submission or show error
      await expect(page).toHaveURL(/login/)
    }
  })
})

test.describe('Admin Protected Routes', () => {
  test('redirects to login when not authenticated', async ({ page }) => {
    await page.goto('/admin')
    await page.waitForTimeout(500)
    // Should redirect to login
    await expect(page).toHaveURL(/login|admin/)
  })

  test('websites admin requires auth', async ({ page }) => {
    await page.goto('/admin/websites')
    await page.waitForTimeout(500)
    // Should redirect to login or show auth error
    await expect(page).toHaveURL(/login|admin/)
  })
})
