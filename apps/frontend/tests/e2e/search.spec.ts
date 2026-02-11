import { test, expect } from '@playwright/test'

test.describe('Search Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/search')
  })

  test('displays search heading', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Search')
  })

  test('has search input', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]')
    await expect(searchInput).toBeVisible()
  })

  test('search input is autofocused', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]')
    await expect(searchInput).toBeFocused()
  })

  test('can type in search input', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]')
    await searchInput.fill('minimal')
    await expect(searchInput).toHaveValue('minimal')
  })

  test('updates URL on search', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]')
    await searchInput.fill('design')
    await searchInput.press('Enter')
    await expect(page).toHaveURL(/q=design/)
  })

  test('shows results info after search', async ({ page }) => {
    const searchInput = page.locator('input[placeholder*="Search"]')
    await searchInput.fill('test')
    await searchInput.press('Enter')
    await page.waitForTimeout(1000)
    // Should show either "Found X results" or "No results found"
    const resultsInfo = page.locator('text=/Found|No results/')
    await expect(resultsInfo).toBeVisible()
  })
})

test.describe('Search with query param', () => {
  test('loads search query from URL', async ({ page }) => {
    await page.goto('/search?q=landing')
    const searchInput = page.locator('input[placeholder*="Search"]')
    await expect(searchInput).toHaveValue('landing')
  })

  test('performs search on page load with query', async ({ page }) => {
    await page.goto('/search?q=design')
    await page.waitForTimeout(1500)
    // Should show results info
    const resultsInfo = page.locator('text=/Found|No results/')
    await expect(resultsInfo).toBeVisible()
  })
})
