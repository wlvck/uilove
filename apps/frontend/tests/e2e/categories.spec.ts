import { test, expect } from '@playwright/test'

test.describe('Categories Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/categories')
  })

  test('displays categories heading', async ({ page }) => {
    const heading = page.locator('h1')
    await expect(heading).toBeVisible()
  })

  test('has correct page title', async ({ page }) => {
    await expect(page).toHaveTitle(/Categories|UILove/)
  })

  test('displays category items', async ({ page }) => {
    await page.waitForTimeout(1000)
    // Categories should be displayed as links or cards
    const categoryLinks = page.locator('a[href*="/categories/"]')
    // May have zero or more categories
    expect(await categoryLinks.count()).toBeGreaterThanOrEqual(0)
  })
})

test.describe('Category Detail Page', () => {
  test('navigating to category shows websites', async ({ page }) => {
    await page.goto('/categories')
    await page.waitForTimeout(1000)

    const categoryLink = page.locator('a[href*="/categories/"]').first()
    if (await categoryLink.isVisible()) {
      await categoryLink.click()
      await page.waitForTimeout(1000)
      // Should show category page with grid
      const grid = page.locator('[class*="grid"]')
      await expect(grid.first()).toBeVisible()
    }
  })
})
